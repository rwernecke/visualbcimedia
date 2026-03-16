#!/usr/bin/env bash
set -euo pipefail

/Users/rafael/visualbcimedia/.venv312/bin/manim /Users/rafael/visualbcimedia/visualbci_video_pipeline/manim_scene.py BeginnerMistakeScene --media_dir /Users/rafael/visualbcimedia/visualbci_video_pipeline/video/manim_media --format=mp4 --output_file 01_beginner_mistake.mp4 --disable_caching -qk
/Users/rafael/visualbcimedia/.venv312/bin/manim /Users/rafael/visualbcimedia/visualbci_video_pipeline/manim_scene.py BrainElectricityScene --media_dir /Users/rafael/visualbcimedia/visualbci_video_pipeline/video/manim_media --format=mp4 --output_file 02_brain_electricity.mp4 --disable_caching -qk
/Users/rafael/visualbcimedia/.venv312/bin/manim /Users/rafael/visualbcimedia/visualbci_video_pipeline/manim_scene.py NoPhDScene --media_dir /Users/rafael/visualbcimedia/visualbci_video_pipeline/video/manim_media --format=mp4 --output_file 03_no_phd.mp4 --disable_caching -qk
