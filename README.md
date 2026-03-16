# Viral Brain Video Pipeline

This repository contains a short-form brain video pipeline optimized for
Instagram Reels and TikTok. The stack is:

- `manim` for visuals
- `ElevenLabs` for voice
- `ffmpeg` for captions, composition, and vertical exports

The current content direction prioritizes curiosity, beautiful visuals, strong
hooks, short duration, and high production quality over lectures or product
promotion.

```text
visualbci_video_pipeline/
  manim_scene.py
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

- stores short, hook-first brain reel scripts
- generates ElevenLabs narration command plans
- estimates timings from rendered or fallback audio
- builds a Manim scene manifest for each segment
- overlays animated captions and waveform styling with ffmpeg
- creates ffmpeg command plans for the assembled full video and reels

## Quick start

```bash
python3 visualbci_video_pipeline/generate_audio.py
python3 visualbci_video_pipeline/build_timings.py
python3 visualbci_video_pipeline/scenes.py
python3 visualbci_video_pipeline/render_modal.py
python3 visualbci_video_pipeline/compose_video.py
python3 visualbci_video_pipeline/generate_reels.py
```

Outputs are written into the subfolders under `visualbci_video_pipeline/`.

## Requirements

- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `manim`
- `ffmpeg`

If ElevenLabs credentials or Manim are missing, the pipeline still writes the
required command plans and manifests so the workflow can be completed once the
environment is ready.
