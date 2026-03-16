#!/usr/bin/env bash
set -euo pipefail

say -v 'Reed' -o /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/01_hook.aiff -f /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/01_hook.txt
ffmpeg -y -i /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/01_hook.aiff /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/01_hook.wav
say -v 'Reed' -o /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/02_measurements.aiff -f /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/02_measurements.txt
ffmpeg -y -i /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/02_measurements.aiff /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/02_measurements.wav
say -v 'Reed' -o /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/03_brain_waves.aiff -f /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/03_brain_waves.txt
ffmpeg -y -i /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/03_brain_waves.aiff /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/03_brain_waves.wav
say -v 'Reed' -o /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/04_importance.aiff -f /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/04_importance.txt
ffmpeg -y -i /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/04_importance.aiff /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/04_importance.wav

ffmpeg -y -f concat -safe 0 -i /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/concat_list.txt -c copy /Users/rafael/visualbcimedia/visualbci_video_pipeline/audio/final_narration.wav
