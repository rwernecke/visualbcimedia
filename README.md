# VisualBCI Video Pipeline

This repository contains a starter pipeline for generating the first VisualBCI
educational lesson video, "What is EEG?", plus short-form reel plans derived
from the same lesson.

The project follows the structure requested in the PDF instructions:

```text
visualbci_video_pipeline/
  generate_audio.py
  build_timings.py
  scenes.py
  render_modal.py
  compose_video.py
  generate_reels.py

  audio/
  video/
  captions/
  reels/
  final/
```

## What it does today

- stores the first lesson script and visual direction
- generates narration text files and a `pocket-tts` command plan
- estimates per-segment timings
- builds a scene manifest for animation/rendering
- generates an SRT caption file
- creates ffmpeg command plans for the full lesson and three reels

## Quick start

```bash
python3 visualbci_video_pipeline/generate_audio.py
python3 visualbci_video_pipeline/build_timings.py
python3 visualbci_video_pipeline/scenes.py
python3 visualbci_video_pipeline/render_modal.py
python3 visualbci_video_pipeline/compose_video.py
python3 visualbci_video_pipeline/generate_reels.py
```

Outputs are written into the subfolders under
`visualbci_video_pipeline/`.

## External tools

The scaffold assumes these tools may later be used:

- `pocket-tts` for narration with the `alba` voice
- `manim` for educational visuals
- `modal` for cloud rendering orchestration
- `ffmpeg` for composition and reel exports

If those tools are not installed, the scripts still generate manifests and
shell command plans so the pipeline can be reviewed and extended.
