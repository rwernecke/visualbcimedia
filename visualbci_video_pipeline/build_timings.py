from __future__ import annotations

from config import AUDIO_DIR, ensure_directories
from common import media_duration, words_per_second, write_json
from script_data import SEGMENTS, TOPIC


def word_timings(text: str, start: float, duration: float) -> list[dict]:
    words = text.split()
    if not words:
        return []

    slice_length = duration / len(words)
    entries = []
    cursor = start
    for word in words:
        word_start = round(cursor, 3)
        word_end = round(cursor + slice_length, 3)
        entries.append({"word": word, "start": word_start, "end": word_end})
        cursor = word_end
    return entries


def main() -> None:
    ensure_directories()

    timings = []
    cursor = 0.0

    for index, segment in enumerate(SEGMENTS, start=1):
        audio_path = AUDIO_DIR / f"{index:02}_{segment['id']}.wav"
        if audio_path.exists():
            estimated_seconds = round(media_duration(audio_path), 2)
        else:
            estimated_seconds = max(segment["target_seconds"], round(words_per_second(segment["text"]), 1))
        start = round(cursor, 2)
        end = round(start + estimated_seconds, 2)
        timings.append(
            {
                "id": segment["id"],
                "title": segment["title"],
                "start": start,
                "end": end,
                "duration": round(estimated_seconds, 2),
                "text": segment["text"],
                "word_timings": word_timings(segment["text"], start, estimated_seconds),
            }
        )
        cursor = end

    payload = {
        "topic": TOPIC,
        "total_duration": round(cursor, 2),
        "segments": timings,
    }
    output_path = AUDIO_DIR / "timings.json"
    write_json(output_path, payload)
    print(f"Wrote estimated timings to {output_path}")


if __name__ == "__main__":
    main()
