from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "audio"
VIDEO_DIR = ROOT / "video"
CAPTIONS_DIR = ROOT / "captions"
REELS_DIR = ROOT / "reels"
FINAL_DIR = ROOT / "final"

ALL_DIRS = [AUDIO_DIR, VIDEO_DIR, CAPTIONS_DIR, REELS_DIR, FINAL_DIR]

BG = "#0f0f1a"
CYAN = "#00d4ff"
WHITE = "#ffffff"
GOLD = "#ffd700"

VOICE = "alba"
FALLBACK_VOICE = "Samantha"
FALLBACK_VOICE_RATE = 168
FALLBACK_AUDIO_FILTER = (
    "highpass=f=80,"
    "lowpass=f=8500,"
    "acompressor=threshold=-18dB:ratio=2.5:attack=5:release=120:makeup=3,"
    "alimiter=limit=0.92"
)
FULL_VIDEO_FILENAME = "what_is_eeg_full.mp4"
FULL_VIDEO_RESOLUTION = (1920, 1080)
FULL_VIDEO_ASPECT = "16:9"
REEL_RESOLUTION = (1080, 1920)
REEL_ASPECT = "9:16"
REEL_CROP = "crop=607:1080:(in_w-607)/2:0"
FRAME_RATE = 30
SLIDE_FONT = "/System/Library/Fonts/Supplemental/Avenir Next.ttc"
CAPTION_FONT = "/System/Library/Fonts/Supplemental/GillSans.ttc"


def ensure_directories() -> None:
    for directory in ALL_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
