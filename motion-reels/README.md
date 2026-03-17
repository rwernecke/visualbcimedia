# Motion Reels

Simple local motion-graphics pages for silent 8-second vertical reels.

## What this is

- dark full-screen 9:16 webpage
- animated EEG line
- large kinetic text
- subtle fade and slide transitions
- one scene per script

## Preview locally

From `/Users/rafael/visualbcimedia/motion-reels` run:

```bash
python3 -m http.server 4174
```

Then open [http://localhost:4174/index.html](http://localhost:4174/index.html)

## Choose a scene

Use the `scene` query param:

- [http://localhost:4174/index.html?scene=1](http://localhost:4174/index.html?scene=1)
- [http://localhost:4174/index.html?scene=2](http://localhost:4174/index.html?scene=2)
- [http://localhost:4174/index.html?scene=3](http://localhost:4174/index.html?scene=3)

Edit the `scenes` array in `/Users/rafael/visualbcimedia/motion-reels/app.js` to replace the demo copy with your reel scripts.

## Notes

- The old video pipeline was not deleted in this pass.
- I kept this isolated so we can transition safely without disturbing unrelated files or your current edits.
