from __future__ import annotations

import json
import os
import subprocess

from config import AUDIO_DIR, FRAME_RATE, ROOT, VIDEO_DIR, ensure_directories
from common import read_json, run_command


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


def main() -> None:
    ensure_directories()
    manifest = read_json(VIDEO_DIR / "scene_manifest.json")
    assets_dir = VIDEO_DIR / "assets"
    segments_dir = VIDEO_DIR / "segments"
    assets_dir.mkdir(parents=True, exist_ok=True)
    segments_dir.mkdir(parents=True, exist_ok=True)

    for index, scene in enumerate(manifest["scenes"], start=1):
        audio_path = AUDIO_DIR / f"{index:02}_{scene['id']}.wav"
        slide_path = assets_dir / f"{index:02}_{scene['id']}_slide.png"
        render_png(
            {
                "mode": "slide",
                "title": scene["title"],
                "body": scene["narration"],
                "accent": scene["visual_brief"],
            },
            str(slide_path),
        )

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
            caption_filters.append(
                f"movie='{escaped}'[cap{cue_index}]"
            )
            base_input = "base" if cue_index == 1 else f"v{cue_index - 1}"
            caption_filters.append(
                f"[{base_input}][cap{cue_index}]overlay=(W-w)/2:H-h-70:enable='between(t,{cue['start'] - scene['start']:.3f},{cue['end'] - scene['start']:.3f})'[v{cue_index}]"
            )

        waveform = "showwaves=s=1600x180:mode=cline:colors=0x00d4ff:rate=30"
        tail = f"v{len(scene['caption_cues'])}" if scene["caption_cues"] else "base"
        filter_parts = [
            "[0:v]fps=30,format=yuv420p[bg]",
            f"[1:a]{waveform}[sw]",
            "[bg][sw]overlay=(W-w)/2:H-235[base]",
        ]
        filter_parts.extend(caption_filters)
        filter_complex = ";".join(filter_parts)

        output_path = segments_dir / f"{index:02}_{scene['id']}.mp4"
        args = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-framerate",
            str(FRAME_RATE),
            "-i",
            str(slide_path),
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
        run_command(args)

    (VIDEO_DIR / "render_notes.txt").write_text(
        "Rendered slide-based segment videos with baked captions and waveform overlays.\n",
        encoding="utf-8",
    )
    print(f"Rendered segment videos in {segments_dir}")


if __name__ == "__main__":
    main()
