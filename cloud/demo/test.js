// node test.js <url> <bild.jpg> [breite]  → Bild, fehlgeschlagene Anfragen, Konsolenfehler
const pw = require('playwright');
(async () => {
  const [url, bild, br] = process.argv.slice(2);
  const b = await pw.chromium.launch();
  const p = await b.newPage({ viewport: { width: +(br || 1440), height: 900 } });
  const fehl = [], kons = [];
  p.on('response', r => { if (r.status() >= 400) fehl.push(r.status() + ' ' + r.url().replace(/^https?:\/\/[^/]+/, '')); });
  p.on('requestfailed', r => fehl.push('FAIL ' + r.url().replace(/^https?:\/\/[^/]+/, '')));
  p.on('console', m => { if (m.type() === 'error') kons.push(m.text().slice(0, 200)); });
  p.on('pageerror', e => kons.push('PAGE ' + String(e).slice(0, 200)));
  await p.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(e => kons.push('GOTO ' + e.message.slice(0, 100)));
  await p.waitForTimeout(3000);
  await p.screenshot({ path: bild, type: 'jpeg', quality: 55 });
  const fremd = await p.evaluate(() => [...document.querySelectorAll('[src],[href]')].map(e => e.getAttribute('src') || e.getAttribute('href')).filter(v => /127\.0\.0\.1|localhost/.test(v)).slice(0, 10));
  console.log(JSON.stringify({ seite: p.url().replace(/^https?:\/\/[^/]+/, ''), fehl: [...new Set(fehl)].slice(0, 25), kons: [...new Set(kons)].slice(0, 15), fremd }, null, 1));
  await b.close();
})();
