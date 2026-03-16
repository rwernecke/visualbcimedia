# The VisualBCI EEG Guide

Files:

- `index.html` - full guide layout and content
- `styles.css` - screen and print styling optimized for PDF output
- `generate-pdf.js` - Puppeteer-based export script
- `package.json` - local preview and PDF export scripts

Preview locally:

1. `cd /Users/rafael/visualbcimedia/eeg-cheat-sheet`
2. `npm run preview`
3. Open `http://localhost:4173/index.html`

Export PDF:

1. `cd /Users/rafael/visualbcimedia/eeg-cheat-sheet`
2. `npm install`
3. `npm run pdf`

Output:

- `dist/the-eeg-cheat-sheet.pdf`

Notes:

- The layout is set to US Letter via print CSS.
- Print backgrounds are enabled in Puppeteer export.
- The first page is designed so the title block, subtitle, intro paragraph, and `Inside this guide` card work well as a teaser crop.
