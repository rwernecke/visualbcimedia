from __future__ import annotations

import shutil

from config import (
    AUDIO_DIR,
    FALLBACK_AUDIO_FILTER,
    FALLBACK_VOICE,
    FALLBACK_VOICE_RATE,
    VOICE,
    ensure_directories,
)
from common import media_duration, run_command
from script_data import SEGMENTS, TOPIC


def resolve_voice() -> str:
    if shutil.which("pocket-tts"):
        return VOICE
    return FALLBACK_VOICE


def main() -> None:
    ensure_directories()

    narration_path = AUDIO_DIR / "what_is_eeg_narration.txt"
    command_plan_path = AUDIO_DIR / "generate_audio_commands.sh"
    final_audio_path = AUDIO_DIR / "final_narration.wav"
    concat_list_path = AUDIO_DIR / "concat_list.txt"

    lines = [f"Topic: {TOPIC}", ""]
    commands = ["#!/usr/bin/env bash", "set -euo pipefail", ""]
    concat_entries = []
    use_pocket_tts = shutil.which("pocket-tts") is not None
    voice_name = resolve_voice()

    for index, segment in enumerate(SEGMENTS, start=1):
        text = segment["text"].strip()
        segment_text_path = AUDIO_DIR / f"{index:02}_{segment['id']}.txt"
        output_aiff = AUDIO_DIR / f"{index:02}_{segment['id']}.aiff"
        output_wav = AUDIO_DIR / f"{index:02}_{segment['id']}.wav"
        segment_text_path.write_text(text + "\n", encoding="utf-8")

        if use_pocket_tts:
            commands.append(
                f"pocket-tts --voice {VOICE} --text-file {segment_text_path} --output {output_wav}"
            )
            run_command(
                [
                    "pocket-tts",
                    "--voice",
                    VOICE,
                    "--text",
                    text,
                    "--output",
                    str(output_wav),
                ]
            )
        else:
            commands.append(
                f"say -v '{voice_name}' -r {FALLBACK_VOICE_RATE} -o {output_aiff} -f {segment_text_path}"
            )
            commands.append(
                f"ffmpeg -y -i {output_aiff} -af \"{FALLBACK_AUDIO_FILTER}\" {output_wav}"
            )
            run_command(
                [
                    "say",
                    "-v",
                    voice_name,
                    "-r",
                    str(FALLBACK_VOICE_RATE),
                    "-o",
                    str(output_aiff),
                    "-f",
                    str(segment_text_path),
                ]
            )
            run_command(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(output_aiff),
                    "-af",
                    FALLBACK_AUDIO_FILTER,
                    str(output_wav),
                ]
            )

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
        f"Requested voice: {VOICE}",
        f"Voice used: {voice_name}",
        f"Fallback rate: {FALLBACK_VOICE_RATE}",
        f"Fallback filter: {FALLBACK_AUDIO_FILTER}",
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
