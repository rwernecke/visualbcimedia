#!/usr/bin/env bash
set -euo pipefail

ffmpeg -ss 0.0 -to 9.39 -i visualbci_video_pipeline/final/what_is_eeg_full.mp4 -vf "crop=607:1080:(in_w-607)/2:0,scale=1080:1920" -c:v libx264 -c:a aac visualbci_video_pipeline/reels/reel_01.mp4
ffmpeg -ss 9.39 -to 21.9 -i visualbci_video_pipeline/final/what_is_eeg_full.mp4 -vf "crop=607:1080:(in_w-607)/2:0,scale=1080:1920" -c:v libx264 -c:a aac visualbci_video_pipeline/reels/reel_02.mp4
ffmpeg -ss 35.64 -to 50.36 -i visualbci_video_pipeline/final/what_is_eeg_full.mp4 -vf "crop=607:1080:(in_w-607)/2:0,scale=1080:1920" -c:v libx264 -c:a aac visualbci_video_pipeline/reels/reel_03.mp4
