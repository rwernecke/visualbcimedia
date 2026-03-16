from __future__ import annotations

from config import (
    CAPTIONS_DIR,
    FINAL_DIR,
    FULL_VIDEO_FILENAME,
    FULL_VIDEO_RESOLUTION,
    VIDEO_DIR,
    ensure_directories,
)
from common import format_srt_timestamp, read_json, run_command


def build_srt(timings: dict) -> str:
    lines = []
    for index, segment in enumerate(timings["segments"], start=1):
        lines.extend(
            [
                str(index),
                f"{format_srt_timestamp(segment['start'])} --> {format_srt_timestamp(segment['end'])}",
                segment["text"],
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_ffmpeg_plan() -> str:
    return "\n".join(
        [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            "",
            "ffmpeg -y -f concat -safe 0 -i visualbci_video_pipeline/video/segments/concat_list.txt \\",
            "  -c:v libx264 -c:a aac \\",
            f"  visualbci_video_pipeline/final/{FULL_VIDEO_FILENAME}",
        ]
    )


def main() -> None:
    ensure_directories()

    timings = read_json(CAPTIONS_DIR.parent / "audio" / "timings.json")
    srt_path = CAPTIONS_DIR / "what_is_eeg.srt"
    compose_path = FINAL_DIR / "compose_full_video.sh"
    concat_list_path = VIDEO_DIR / "segments" / "concat_list.txt"
    final_video_path = FINAL_DIR / FULL_VIDEO_FILENAME

    srt_path.write_text(build_srt(timings), encoding="utf-8")
    concat_lines = []
    for index, segment in enumerate(timings["segments"], start=1):
        concat_lines.append(f"file '{VIDEO_DIR / 'segments' / f'{index:02}_{segment['id']}.mp4'}'")
    concat_list_path.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    compose_path.write_text(build_ffmpeg_plan() + "\n", encoding="utf-8")
    compose_path.chmod(0o755)
    run_command(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list_path),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            str(final_video_path),
        ]
    )

    print(f"Wrote captions to {srt_path}")
    print(f"Rendered full lesson video to {final_video_path}")
    print(f"Wrote full-video ffmpeg plan to {compose_path}")


if __name__ == "__main__":
    main()
