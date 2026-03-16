from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path
from typing import Any

from config import ensure_directories


def write_json(path: Path, payload: Any) -> None:
    ensure_directories()
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True)


def shell_quote(path: Path | str) -> str:
    return shlex.quote(str(path))


def media_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()
    try:
        return float(output)
    except ValueError:
        return 0.0


def words_per_second(text: str) -> float:
    word_count = len(text.split())
    return max(word_count / 2.4, 1.0)


def format_srt_timestamp(seconds: float) -> str:
    total_ms = round(seconds * 1000)
    hours = total_ms // 3_600_000
    minutes = (total_ms % 3_600_000) // 60_000
    secs = (total_ms % 60_000) // 1000
    millis = total_ms % 1000
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
