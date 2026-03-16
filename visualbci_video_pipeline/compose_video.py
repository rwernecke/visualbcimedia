from __future__ import annotations

from config import CAPTIONS_DIR, ensure_directories
from common import format_srt_timestamp, read_json


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


def main() -> None:
    ensure_directories()
    timings = read_json(CAPTIONS_DIR.parent / "audio" / "timings.json")
    srt_path = CAPTIONS_DIR / "what_is_eeg.srt"
    srt_path.write_text(build_srt(timings), encoding="utf-8")
    print(f"Wrote captions to {srt_path}")
    print("Skipped full video composition. This pipeline is reel-only.")


if __name__ == "__main__":
    main()
