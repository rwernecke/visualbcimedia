const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

async function run() {
  let puppeteer;
  try {
    puppeteer = require("puppeteer");
  } catch (error) {
    console.error(
      "Missing dependency: install Puppeteer with `npm install puppeteer` inside /Users/rafael/visualbcimedia/eeg-cheat-sheet."
    );
    process.exit(1);
  }

  const projectDir = __dirname;
  const inputPath = path.join(projectDir, "index.html");
  const outputDir = path.join(projectDir, "dist");
  const outputPath = path.join(outputDir, "the-eeg-cheat-sheet.pdf");

  fs.mkdirSync(outputDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: "new",
  });

  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(inputPath).href, {
      waitUntil: "networkidle0",
    });

    await page.pdf({
      path: outputPath,
      format: "Letter",
      printBackground: true,
      preferCSSPageSize: true,
    });

    console.log(`PDF generated at ${outputPath}`);
  } finally {
    await browser.close();
  }
}

run().catch((error) => {
  console.error(error);
  process.exit(1);
});
