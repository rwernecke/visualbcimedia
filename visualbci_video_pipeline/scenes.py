from __future__ import annotations

from config import BG, CYAN, GOLD, GREEN, VIDEO_DIR, WHITE, ensure_directories
from common import read_json, write_json
from script_data import SEGMENTS, TOPIC


def build_caption_cues(word_timings: list[dict], window: int = 3) -> list[dict]:
    cues = []
    words = [entry["word"] for entry in word_timings]
    for idx, entry in enumerate(word_timings):
        start_idx = max(0, idx - 1)
        end_idx = min(len(words), start_idx + window)
        if end_idx - start_idx < window:
            start_idx = max(0, end_idx - window)
        phrase = words[start_idx:end_idx]
        highlight = idx - start_idx
        cues.append(
            {
                "start": entry["start"],
                "end": entry["end"],
                "words": phrase,
                "highlight_index": highlight,
            }
        )
    return cues


def main() -> None:
    ensure_directories()

    timings = read_json(VIDEO_DIR.parent / "audio" / "timings.json")
    timing_map = {segment["id"]: segment for segment in timings["segments"]}

    scene_manifest = {
        "topic": TOPIC,
        "style": {
            "background": BG,
            "accent": CYAN,
            "secondary": GREEN,
            "text": WHITE,
            "highlight": GOLD,
            "direction": "Short-form viral brain visuals with glowing neurons, electric pulses, and cinematic motion.",
        },
        "scenes": [],
    }

    for segment in SEGMENTS:
        timing = timing_map[segment["id"]]
        scene_manifest["scenes"].append(
            {
                "id": segment["id"],
                "title": segment["title"],
                "start": timing["start"],
                "end": timing["end"],
                "duration": timing["duration"],
                "narration": segment["text"],
                "hook": segment.get("hook", ""),
                "visual_brief": segment["visual"],
                "image_prompt": segment.get("image_prompt", ""),
                "caption_cues": build_caption_cues(timing["word_timings"]),
            }
        )

    output_path = VIDEO_DIR / "scene_manifest.json"
    write_json(output_path, scene_manifest)
    print(f"Wrote scene manifest to {output_path}")


if __name__ == "__main__":
    main()
