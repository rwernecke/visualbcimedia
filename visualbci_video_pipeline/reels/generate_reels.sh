#!/usr/bin/env bash
set -euo pipefail

ffmpeg -i /Users/rafael/visualbcimedia/visualbci_video_pipeline/video/segments/01_beginner_mistake.mp4 -vf scale=1080:1920 -c:v libx264 -c:a aac /Users/rafael/visualbcimedia/visualbci_video_pipeline/reels/reel_01.mp4
ffmpeg -i /Users/rafael/visualbcimedia/visualbci_video_pipeline/video/segments/02_brain_electricity.mp4 -vf scale=1080:1920 -c:v libx264 -c:a aac /Users/rafael/visualbcimedia/visualbci_video_pipeline/reels/reel_02.mp4
ffmpeg -i /Users/rafael/visualbcimedia/visualbci_video_pipeline/video/segments/03_no_phd.mp4 -vf scale=1080:1920 -c:v libx264 -c:a aac /Users/rafael/visualbcimedia/visualbci_video_pipeline/reels/reel_03.mp4
