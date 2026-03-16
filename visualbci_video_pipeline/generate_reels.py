from __future__ import annotations

from config import FINAL_DIR, REELS_DIR, REEL_ASPECT, REEL_CROP, REEL_RESOLUTION, ensure_directories
from common import read_json, run_command, write_json
from script_data import REELS


def main() -> None:
    ensure_directories()

    timings = read_json(REELS_DIR.parent / "audio" / "timings.json")
    timing_map = {segment["id"]: segment for segment in timings["segments"]}
    reel_specs = []
    command_lines = ["#!/usr/bin/env bash", "set -euo pipefail", ""]

    for reel in REELS:
        selected = [timing_map[segment_id] for segment_id in reel["segment_ids"]]
        start = min(item["start"] for item in selected)
        end = max(item["end"] for item in selected)
        duration = round(end - start, 2)
        width, height = REEL_RESOLUTION

        reel_specs.append(
            {
                "id": reel["id"],
                "title": reel["title"],
                "start": start,
                "end": end,
                "duration": duration,
                "aspect_ratio": REEL_ASPECT,
                "resolution": f"{width}x{height}",
                "crop": REEL_CROP,
            }
        )
        command_lines.append(
            "ffmpeg "
            f"-ss {start} -to {end} "
            "-i visualbci_video_pipeline/final/what_is_eeg_full.mp4 "
            f"-vf \"{REEL_CROP},scale={width}:{height}\" "
            f"-c:v libx264 -c:a aac visualbci_video_pipeline/reels/{reel['id']}.mp4"
        )
        run_command(
            [
                "ffmpeg",
                "-y",
                "-ss",
                str(start),
                "-to",
                str(end),
                "-i",
                str(FINAL_DIR / "what_is_eeg_full.mp4"),
                "-vf",
                f"{REEL_CROP},scale={width}:{height}",
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                str(REELS_DIR / f"{reel['id']}.mp4"),
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
