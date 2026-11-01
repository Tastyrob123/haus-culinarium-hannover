// node klick.js <url> <bild> "<Text zum Anklicken>"  → nach dem Klick Bild + Fehler
const pw = require('playwright');
(async () => {
  const [url, bild, text] = process.argv.slice(2);
  const b = await pw.chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const fehl = [], kons = [];
  p.on('response', r => { if (r.status() >= 400) fehl.push(r.status() + ' ' + r.url().replace(/^https?:\/\/[^/]+/, '')); });
  p.on('pageerror', e => kons.push('PAGE ' + String(e).slice(0, 200)));
  await p.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
  await p.waitForTimeout(2500);
  await p.keyboard.press('Escape').catch(() => {});
  await p.getByText(text, { exact: true }).first().click({ timeout: 8000 }).catch(e => kons.push('KLICK ' + e.message.slice(0, 80)));
  await p.waitForTimeout(3000);
  await p.screenshot({ path: bild, type: 'jpeg', quality: 55 });
  console.log(JSON.stringify({ fehl: [...new Set(fehl)].filter(f => /\/(x|scratchpad)\//.test(f) || 1).slice(0, 12), kons }));
  await b.close();
})();
