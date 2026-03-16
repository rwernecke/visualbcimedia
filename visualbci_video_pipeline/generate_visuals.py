from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

from config import (
    GENERATED_VIDEO_DIR,
    OPENAI_API_KEY,
    OPENAI_VIDEO_MODEL,
    OPENAI_VIDEO_SECONDS,
    OPENAI_VIDEO_SIZE,
    ROOT,
    ensure_directories,
)
from script_data import SEGMENTS


def run_curl(args: list[str]) -> dict:
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def openai_ready() -> bool:
    return bool(OPENAI_API_KEY)


def create_openai_video(prompt: str) -> str:
    payload = run_curl(
        [
            "curl",
            "-sS",
            "https://api.openai.com/v1/videos",
            "-H",
            f"Authorization: Bearer {OPENAI_API_KEY}",
            "-F",
            f"model={OPENAI_VIDEO_MODEL}",
            "-F",
            f"prompt={prompt}",
            "-F",
            f"seconds={OPENAI_VIDEO_SECONDS}",
            "-F",
            f"size={OPENAI_VIDEO_SIZE}",
        ]
    )
    if "id" not in payload:
        raise RuntimeError(f"OpenAI video create failed: {payload}")
    return payload["id"]


def wait_for_openai_video(video_id: str) -> dict:
    while True:
        payload = run_curl(
            [
                "curl",
                "-sS",
                f"https://api.openai.com/v1/videos/{video_id}",
                "-H",
                f"Authorization: Bearer {OPENAI_API_KEY}",
            ]
        )
        status = payload.get("status")
        print(f"{video_id}: {status}")
        if status == "completed":
            return payload
        if status == "failed":
            raise RuntimeError(f"OpenAI video generation failed for {video_id}: {payload}")
        time.sleep(5)


def download_openai_video(video_id: str, output_path: Path) -> None:
    subprocess.run(
        [
            "curl",
            "-sS",
            f"https://api.openai.com/v1/videos/{video_id}/content",
            "-H",
            f"Authorization: Bearer {OPENAI_API_KEY}",
            "-o",
            str(output_path),
        ],
        check=True,
    )


def build_prompt(segment: dict) -> str:
    return (
        f"{segment['image_prompt']}. "
        "Viral Instagram Reel visual, extremely cinematic, broad public appeal, smooth camera movement, premium sci-fi brain aesthetic, no text overlays."
    )


def main() -> None:
    ensure_directories()
    command_plan = GENERATED_VIDEO_DIR / "generate_visuals.sh"
    commands = ["#!/usr/bin/env bash", "set -euo pipefail", ""]

    for segment in SEGMENTS:
        output_path = GENERATED_VIDEO_DIR / f"{segment['id']}.mp4"
        meta_path = GENERATED_VIDEO_DIR / f"{segment['id']}.json"
        prompt = build_prompt(segment)
        commands.append(
            "curl -sS https://api.openai.com/v1/videos "
            "-H 'Authorization: Bearer $OPENAI_API_KEY' "
            f"-F model={OPENAI_VIDEO_MODEL} "
            f"-F seconds={OPENAI_VIDEO_SECONDS} "
            f"-F size={OPENAI_VIDEO_SIZE} "
            f"-F prompt={json.dumps(prompt)}"
        )
        if openai_ready():
            video_id = create_openai_video(prompt)
            meta_path.write_text(json.dumps({"id": video_id, "prompt": prompt}, indent=2) + "\n", encoding="utf-8")
            print(f"Created {segment['id']} -> {video_id}")
            wait_for_openai_video(video_id)
            download_openai_video(video_id, output_path)
            print(f"Downloaded {output_path}")

    command_plan.write_text("\n".join(commands) + "\n", encoding="utf-8")
    command_plan.chmod(0o755)

    if openai_ready():
        print(f"Generated provider videos in {GENERATED_VIDEO_DIR}")
    else:
        print(f"Wrote provider video plan to {command_plan}")


if __name__ == "__main__":
    main()
