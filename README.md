# VisualBCI Media

This repository now keeps two active pieces:

- `eeg-cheat-sheet/` for the EEG guide and PDF workflow
- `motion-reels/` for silent 9:16 motion-graphics webpages used as reel visuals

## Motion Reels

The new reel workflow is intentionally simple:

- full-screen vertical webpage
- dark background
- animated EEG line
- large kinetic text
- subtle fade and slide transitions
- one scene per script
- designed around 8-second reels

Preview locally:

```bash
cd /Users/rafael/visualbcimedia/motion-reels
python3 -m http.server 4174
```

Open `http://localhost:4174/index.html?scene=1`

## EEG Cheat Sheet

The EEG cheat sheet remains unchanged and stays in:

```text
/Users/rafael/visualbcimedia/eeg-cheat-sheet
```

Its local instructions are in:

```text
/Users/rafael/visualbcimedia/eeg-cheat-sheet/README.md
```
