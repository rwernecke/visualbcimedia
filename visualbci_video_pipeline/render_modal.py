from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

from config import AUDIO_DIR, FRAME_RATE, GENERATED_VIDEO_DIR, REEL_RESOLUTION, ROOT, VIDEO_DIR, ensure_directories
from common import read_json, run_command

SCENE_CLASS_MAP = {
    "beginner_mistake": "BeginnerMistakeScene",
    "brain_electricity": "BrainElectricityScene",
    "no_phd": "NoPhDScene",
}


def resolve_manim_binary() -> str | None:
    for env_name in [".venv", ".venv312"]:
        local_manim = ROOT.parent / env_name / "bin" / "manim"
        if local_manim.exists():
            return str(local_manim)
    return shutil.which("manim")


def render_png(spec: dict, output_path: str) -> None:
    spec_path = VIDEO_DIR / "tmp_spec.json"
    cache_dir = VIDEO_DIR / ".swift-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    env = os.environ.copy()
    env["SWIFT_MODULECACHE_PATH"] = str(cache_dir)
    env["CLANG_MODULE_CACHE_PATH"] = str(cache_dir)
    subprocess.run(
        ["swift", str(ROOT / "render_card.swift"), str(spec_path), output_path],
        check=True,
        env=env,
    )
    spec_path.unlink(missing_ok=True)


def ffmpeg_escape(path: str) -> str:
    return path.replace("\\", "\\\\").replace(":", "\\:").replace("'", r"\'")


def manim_output_path(media_dir: Path, scene_name: str, output_name: str) -> Path:
    matches = sorted(media_dir.rglob(output_name))
    if not matches:
        raise FileNotFoundError(f"Could not locate Manim output for {scene_name}")
    return matches[-1]


def render_manim_scene(media_dir: Path, scene_id: str, output_name: str) -> Path:
    scene_class = SCENE_CLASS_MAP[scene_id]
    manim_bin = resolve_manim_binary()
    if not manim_bin:
        raise FileNotFoundError("Manim is not installed")
    run_command(
        [
            manim_bin,
            str(ROOT / "manim_scene.py"),
            scene_class,
            "--media_dir",
            str(media_dir),
            "--format=mp4",
            "--output_file",
            output_name,
            "--disable_caching",
            "-qk",
        ]
    )
    return manim_output_path(media_dir, scene_class, output_name)


def resolve_visual_source(media_dir: Path, scene_id: str, output_name: str) -> Path:
    generated_path = GENERATED_VIDEO_DIR / f"{scene_id}.mp4"
    if generated_path.exists():
        return generated_path
    return render_manim_scene(media_dir, scene_id, output_name)


def build_render_commands(manifest: dict) -> str:
    media_dir = VIDEO_DIR / "manim_media"
    manim_bin = resolve_manim_binary() or "manim"
    lines = ["#!/usr/bin/env bash", "set -euo pipefail", ""]
    for index, scene in enumerate(manifest["scenes"], start=1):
        scene_class = SCENE_CLASS_MAP[scene["id"]]
        output_name = f"{index:02}_{scene['id']}.mp4"
        lines.append(
            f"{manim_bin} "
            f"{ROOT / 'manim_scene.py'} {scene_class} "
            f"--media_dir {media_dir} --format=mp4 --output_file {output_name} --disable_caching -qk"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    ensure_directories()
    manifest = read_json(VIDEO_DIR / "scene_manifest.json")
    assets_dir = VIDEO_DIR / "assets"
    segments_dir = VIDEO_DIR / "segments"
    media_dir = VIDEO_DIR / "manim_media"
    assets_dir.mkdir(parents=True, exist_ok=True)
    segments_dir.mkdir(parents=True, exist_ok=True)
    media_dir.mkdir(parents=True, exist_ok=True)

    command_plan = build_render_commands(manifest)
    (VIDEO_DIR / "render_commands.sh").write_text(command_plan, encoding="utf-8")

    if resolve_manim_binary() is None:
        (VIDEO_DIR / "render_notes.txt").write_text(
            "Manim is not installed locally. Render commands were written to render_commands.sh; install Manim to generate scene visuals, then rerun this script.\n",
            encoding="utf-8",
        )
        print(f"Wrote Manim render plan to {VIDEO_DIR / 'render_commands.sh'}")
        return

    for index, scene in enumerate(manifest["scenes"], start=1):
        audio_path = AUDIO_DIR / f"{index:02}_{scene['id']}.wav"
        caption_filters = []

        for cue_index, cue in enumerate(scene["caption_cues"], start=1):
            caption_path = assets_dir / f"{index:02}_{scene['id']}_caption_{cue_index:02}.png"
            render_png(
                {
                    "mode": "caption",
                    "words": cue["words"],
                    "highlight_index": cue["highlight_index"],
                },
                str(caption_path),
            )
            escaped = ffmpeg_escape(str(caption_path))
            caption_filters.append(f"movie='{escaped}'[cap{cue_index}]")
            base_input = "base" if cue_index == 1 else f"v{cue_index - 1}"
            caption_filters.append(
                f"[{base_input}][cap{cue_index}]overlay=(W-w)/2:H-h-70:enable='between(t,{cue['start'] - scene['start']:.3f},{cue['end'] - scene['start']:.3f})'[v{cue_index}]"
            )

        output_name = f"{index:02}_{scene['id']}.mp4"
        rendered_scene = resolve_visual_source(media_dir, scene["id"], output_name)
        waveform = "showwaves=s=1600x180:mode=cline:colors=0x00d4ff|0x50fa7b:rate=30"
        tail = f"v{len(scene['caption_cues'])}" if scene["caption_cues"] else "base"
        width, height = REEL_RESOLUTION
        filter_parts = [
            f"[0:v]fps=30,scale={width}:{height},format=yuv420p[bg]",
            f"[1:a]{waveform}[sw]",
            "[bg][sw]overlay=(W-w)/2:H-h-360[base]",
        ]
        filter_parts.extend(caption_filters)
        filter_complex = ";".join(filter_parts)

        output_path = segments_dir / output_name
        run_command(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(rendered_scene),
                "-i",
                str(audio_path),
                "-filter_complex",
                filter_complex,
                "-map",
                f"[{tail}]",
                "-map",
                "1:a",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-shortest",
                str(output_path),
            ]
        )

    (VIDEO_DIR / "render_notes.txt").write_text(
        "Rendered provider-generated reel visuals when available, otherwise Manim fallback, then layered captions and waveform overlays with ffmpeg.\n",
        encoding="utf-8",
    )
    print(f"Rendered segment videos in {segments_dir}")


if __name__ == "__main__":
    main()
