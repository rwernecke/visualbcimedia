from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "audio"
VIDEO_DIR = ROOT / "video"
GENERATED_VIDEO_DIR = VIDEO_DIR / "generated"
CAPTIONS_DIR = ROOT / "captions"
REELS_DIR = ROOT / "reels"
FINAL_DIR = ROOT / "final"

ALL_DIRS = [AUDIO_DIR, VIDEO_DIR, GENERATED_VIDEO_DIR, CAPTIONS_DIR, REELS_DIR, FINAL_DIR]

BG = "#0f0f1a"
CYAN = "#00d4ff"
GREEN = "#50fa7b"
WHITE = "#ffffff"
GOLD = "#ffd700"

TTS_PROVIDER = os.getenv("BRAINREELS_TTS_PROVIDER", "elevenlabs").lower()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
ELEVENLABS_VOICE_HINT = os.getenv("ELEVENLABS_VOICE_HINT", "Adam / Antoni / Josh")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_VIDEO_MODEL = os.getenv("OPENAI_VIDEO_MODEL", "sora-2-pro")
OPENAI_VIDEO_SECONDS = os.getenv("OPENAI_VIDEO_SECONDS", "8")
OPENAI_VIDEO_SIZE = os.getenv("OPENAI_VIDEO_SIZE", "1024x1792")
FALLBACK_AUDIO_FILTER = (
    "highpass=f=80,"
    "lowpass=f=8500,"
    "acompressor=threshold=-18dB:ratio=2.5:attack=5:release=120:makeup=3,"
    "alimiter=limit=0.92"
)
REEL_RESOLUTION = (1080, 1920)
REEL_ASPECT = "9:16"
FRAME_RATE = 30
SLIDE_FONT = "/System/Library/Fonts/Supplemental/Avenir Next.ttc"
CAPTION_FONT = "/System/Library/Fonts/Supplemental/GillSans.ttc"


def ensure_directories() -> None:
    for directory in ALL_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
