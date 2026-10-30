// Renders design/cover-sources/*.svg to src/assets/images/<name>.webp (1376x768).
// Needs Playwright available (npx playwright install chromium; npm i --no-save playwright).
const { chromium } = require('playwright');
const sharp = require('sharp');
const { readdirSync, readFileSync } = require('node:fs');
const { join, basename } = require('node:path');
const dir = join(__dirname, 'cover-sources');
const out = join(__dirname, '..', 'src', 'assets', 'images');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1376, height: 768 } });
  for (const f of readdirSync(dir).filter((f) => f.endsWith('.svg'))) {
    await page.setContent(`<body style="margin:0">${readFileSync(join(dir, f), 'utf8')}</body>`);
    const png = await page.screenshot({ type: 'png' });
    const name = basename(f, '.svg') + '.webp';
    await sharp(png).webp({ quality: 85 }).toFile(join(out, name));
    console.log('wrote', name);
  }
  await browser.close();
})();
