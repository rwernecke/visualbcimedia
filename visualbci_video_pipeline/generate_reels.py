from __future__ import annotations

from config import REELS_DIR, REEL_ASPECT, REEL_RESOLUTION, VIDEO_DIR, ensure_directories
from common import read_json, run_command, write_json
from script_data import REELS


def main() -> None:
    ensure_directories()

    timings = read_json(REELS_DIR.parent / "audio" / "timings.json")
    timing_map = {segment["id"]: segment for segment in timings["segments"]}
    reel_specs = []
    command_lines = ["#!/usr/bin/env bash", "set -euo pipefail", ""]
    width, height = REEL_RESOLUTION

    for index, reel in enumerate(REELS, start=1):
        selected = [timing_map[segment_id] for segment_id in reel["segment_ids"]]
        start = min(item["start"] for item in selected)
        end = max(item["end"] for item in selected)
        duration = round(end - start, 2)
        source_path = VIDEO_DIR / "segments" / f"{index:02}_{reel['segment_ids'][0]}.mp4"
        target_path = REELS_DIR / f"{reel['id']}.mp4"

        reel_specs.append(
            {
                "id": reel["id"],
                "title": reel["title"],
                "start": start,
                "end": end,
                "duration": duration,
                "aspect_ratio": REEL_ASPECT,
                "resolution": f"{width}x{height}",
                "source": str(source_path),
            }
        )
        command_lines.append(
            "ffmpeg "
            f"-i {source_path} "
            f"-vf scale={width}:{height} "
            f"-c:v libx264 -c:a aac {target_path}"
        )
        run_command(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(source_path),
                "-vf",
                f"scale={width}:{height}",
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                str(target_path),
            ]
        )

    write_json(REELS_DIR / "reel_plan.json", {"clips": reel_specs})
    command_path = REELS_DIR / "generate_reels.sh"
    command_path.write_text("\n".join(command_lines) + "\n", encoding="utf-8")
    command_path.chmod(0o755)
    print(f"Wrote reel plan to {REELS_DIR / 'reel_plan.json'}")
    print(f"Rendered reels and wrote ffmpeg plan to {command_path}")


if __name__ == "__main__":
    main()
