#!/usr/bin/env bash
set -euo pipefail

ffmpeg -y -f concat -safe 0 -i visualbci_video_pipeline/video/segments/concat_list.txt \
  -c:v libx264 -c:a aac \
  visualbci_video_pipeline/final/what_is_eeg_full.mp4
