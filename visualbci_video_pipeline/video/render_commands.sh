#!/usr/bin/env bash
set -euo pipefail

# Example cloud render flow for scene generation
modal run /Users/rafael/visualbcimedia/visualbci_video_pipeline/render_modal.py

# Example local manim render fallback
manim -pql visualbci_video_pipeline/manim_scene.py VisualBCILessonScene
