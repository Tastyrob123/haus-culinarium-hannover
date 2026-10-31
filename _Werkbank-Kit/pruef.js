// Sichtprüfung der Werkbank: node werkbank/pruef.js [--m] [abschnitt …]  → Bilder je Abschnitt nach $OUT
const path = require('path'), fs = require('fs');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ART = process.env.ART || 'chromium';
const M = process.argv.includes('--m'), nur = process.argv.slice(2).filter(a => !a.startsWith('--'));
const OUT = process.env.OUT || path.join(require('os').tmpdir(), 'werkbank-pruef');
const URL_ = process.env.URL_ || 'http://127.0.0.1:8912/werkbank/';
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await PW[ART].launch({ headless: true });
  const ctx = await b.newContext(M ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true } : { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  const fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); });
  p.on('pageerror', e => fehler.push(String(e)));
  p.on('response', r => { if (r.status() >= 400) fehler.push(r.status() + ' ' + r.url()); });
  await p.goto(URL_, { waitUntil: 'load' });
  await p.waitForTimeout(4600);
  const ids = await p.evaluate(() => ['oben'].concat([...document.querySelectorAll('main section[id]')].map(s => s.id)));
  const vh = M ? 844 : 900;
  for (const id of ids) {
    if (nur.length && !nur.includes(id)) { continue; }
    await p.evaluate(i => { const e = document.getElementById(i); scrollTo(0, i === 'oben' ? 0 : e.getBoundingClientRect().top + scrollY - 6); }, id);
    await p.waitForTimeout(id === 'gefuege' ? 5200 : 2900);
    await p.screenshot({ path: path.join(OUT, (M ? 'm-' : 'd-') + id + '.jpg'), quality: 78 });
    const h = await p.evaluate(i => document.getElementById(i).getBoundingClientRect().height, id);
    let n = 1;
    while (h > vh * (n + 0.25) && id !== 'oben' && n < 4) { await p.evaluate(v => scrollBy(0, v), vh - 90); await p.waitForTimeout(2300); n++; await p.screenshot({ path: path.join(OUT, (M ? 'm-' : 'd-') + id + '-' + n + '.jpg'), quality: 78 }); }
  }
  // einmal ganz durch bis zum Fuss, wie ein Gast: erst danach zählt, was nicht eingeblendet ist (lange Abschnitte und der Fuss liegen sonst nie im Bild; Familie Maeder, 17.10.2026)
  if (!nur.length) { const hh = await p.evaluate(() => document.documentElement.scrollHeight); for (let y = 0; y <= hh; y += Math.round(vh * 0.6)) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(260); } await p.waitForTimeout(1200); }
  const quer = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  const tot = await p.evaluate(() => [...document.querySelectorAll('a[href^="#"]')].filter(a => a.getAttribute('href').length > 1 && !document.querySelector(a.getAttribute('href'))).map(a => a.getAttribute('href')));
  const verst = nur.length ? '-' : await p.evaluate(() => [...document.querySelectorAll('[data-a],.zt')].filter(e => { const r = e.getBoundingClientRect(); return r.right > 0 && r.left < innerWidth; }).filter(e => !e.classList.contains('da'))   /* Karten seitlich ausserhalb eines Bands erscheinen erst beim Blättern (Familie Maeder, 17.10.2026) */.map(e => (e.className || e.tagName) + ':' + e.textContent.slice(0, 20)).slice(0, 6));
  console.log(M ? 'Handy' : 'Rechner', 'Abschnitte', ids.length, 'Quer-Überlauf', quer, 'tote Anker', JSON.stringify(tot), 'nicht eingeblendet', JSON.stringify(verst), fehler.length ? 'FEHLER ' + JSON.stringify(fehler.slice(0, 8)) : 'keine Fehler');
  await b.close();
})();
