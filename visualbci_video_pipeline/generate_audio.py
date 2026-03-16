from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from config import (
    AUDIO_DIR,
    ELEVENLABS_API_KEY,
    ELEVENLABS_MODEL_ID,
    ELEVENLABS_VOICE_HINT,
    ELEVENLABS_VOICE_ID,
    FALLBACK_AUDIO_FILTER,
    ensure_directories,
)
from common import media_duration, run_command
from script_data import SEGMENTS, TOPIC


def fallback_duration(text: str) -> float:
    word_count = max(len(text.split()), 1)
    return round(max(word_count / 2.8, 3.0), 2)


def render_silence(output_wav: Path, duration: float) -> None:
    run_command(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=22050:cl=mono",
            "-t",
            str(duration),
            str(output_wav),
        ]
    )


def normalize_audio(source_path: Path, output_wav: Path) -> None:
    run_command(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(source_path),
            "-af",
            FALLBACK_AUDIO_FILTER,
            str(output_wav),
        ]
    )


def elevenlabs_ready() -> bool:
    return bool(ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID)


def elevenlabs_command(text_path: Path, raw_path: Path) -> str:
    return (
        "curl -sS https://api.elevenlabs.io/v1/text-to-speech/"
        f"{ELEVENLABS_VOICE_ID}/stream "
        "-H 'Content-Type: application/json' "
        "-H 'Accept: audio/mpeg' "
        "-H 'xi-api-key: $ELEVENLABS_API_KEY' "
        f"-d @<(jq -n --rawfile text {text_path} "
        "'{text:$text,model_id:\""
        f"{ELEVENLABS_MODEL_ID}"
        "\",voice_settings:{stability:0.42,similarity_boost:0.82,style:0.18,use_speaker_boost:true}}') "
        f"> {raw_path}"
    )


def render_elevenlabs_audio(text: str, raw_path: Path) -> None:
    request = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream",
        data=json.dumps(
            {
                "text": text,
                "model_id": ELEVENLABS_MODEL_ID,
                "voice_settings": {
                    "stability": 0.42,
                    "similarity_boost": 0.82,
                    "style": 0.18,
                    "use_speaker_boost": True,
                },
            }
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
            "xi-api-key": ELEVENLABS_API_KEY,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        raw_path.write_bytes(response.read())


def main() -> None:
    ensure_directories()

    narration_path = AUDIO_DIR / "what_is_eeg_narration.txt"
    command_plan_path = AUDIO_DIR / "generate_audio_commands.sh"
    final_audio_path = AUDIO_DIR / "final_narration.wav"
    concat_list_path = AUDIO_DIR / "concat_list.txt"

    lines = [f"Topic: {TOPIC}", ""]
    commands = ["#!/usr/bin/env bash", "set -euo pipefail", ""]
    concat_entries: list[str] = []
    using_elevenlabs = elevenlabs_ready()

    for index, segment in enumerate(SEGMENTS, start=1):
        text = segment["text"].strip()
        text_path = AUDIO_DIR / f"{index:02}_{segment['id']}.txt"
        raw_path = AUDIO_DIR / f"{index:02}_{segment['id']}.mp3"
        output_wav = AUDIO_DIR / f"{index:02}_{segment['id']}.wav"
        text_path.write_text(text + "\n", encoding="utf-8")

        if using_elevenlabs:
            commands.append(elevenlabs_command(text_path, raw_path))
            commands.append(f"ffmpeg -y -i {raw_path} -af \"{FALLBACK_AUDIO_FILTER}\" {output_wav}")
            try:
                render_elevenlabs_audio(text, raw_path)
                normalize_audio(raw_path, output_wav)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
                raw_path.unlink(missing_ok=True)

        if media_duration(output_wav) <= 0:
            silence_seconds = fallback_duration(text)
            commands.append(
                f"ffmpeg -y -f lavfi -i anullsrc=r=22050:cl=mono -t {silence_seconds} {output_wav}"
            )
            render_silence(output_wav, silence_seconds)

        raw_path.unlink(missing_ok=True)
        concat_entries.append(f"file '{output_wav}'")
        lines.extend([f"[{segment['title']}]", text, ""])

    concat_list_path.write_text("\n".join(concat_entries) + "\n", encoding="utf-8")
    commands.extend(
        [
            "",
            f"ffmpeg -y -f concat -safe 0 -i {concat_list_path} -af \"{FALLBACK_AUDIO_FILTER}\" {final_audio_path}",
        ]
    )
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
            "-af",
            FALLBACK_AUDIO_FILTER,
            str(final_audio_path),
        ]
    )

    narration_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    command_plan_path.write_text("\n".join(commands) + "\n", encoding="utf-8")
    command_plan_path.chmod(0o755)

    summary_lines = [
        "Voice engine: ElevenLabs",
        f"Voice target: {ELEVENLABS_VOICE_HINT}",
        f"Voice status: {'configured' if using_elevenlabs else 'missing ELEVENLABS_API_KEY / ELEVENLABS_VOICE_ID, using silence fallback'}",
        "",
    ]
    for index, segment in enumerate(SEGMENTS, start=1):
        output_wav = AUDIO_DIR / f"{index:02}_{segment['id']}.wav"
        summary_lines.append(
            f"{index:02} {segment['title']}: {media_duration(output_wav):.2f}s"
        )
    (AUDIO_DIR / "audio_summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"Wrote narration text to {narration_path}")
    print(f"Rendered narration audio to {final_audio_path}")
    print(f"Wrote TTS command plan to {command_plan_path}")


if __name__ == "__main__":
    main()
