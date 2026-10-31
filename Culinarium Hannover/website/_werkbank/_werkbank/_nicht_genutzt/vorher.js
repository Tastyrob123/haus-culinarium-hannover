// Vorher/Nachher für die Werkbank der Taverne zum Schäfli (21.10.2026, Vorlage Schlössli): je Seite die heutige Seite des Hauses und der Entwurf,
// oberster Bildschirm 1440 × 900 mit doppelter Pixeldichte.   node _werkbank/vorher.js [slug …]
//   → _werkbank/ansichten/Vorher/<slug>-alt.jpg und <slug>-neu.jpg   (gelesen von H.VORHER im Kit-Bau)
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const HIER = __dirname, ZIEL = path.join(HIER, 'ansichten', 'Vorher');
const NEU = 'http://127.0.0.1:' + (process.env.WB_PORT || 9068) + '/';
const PAARE = [
  ['startseite', 'https://www.schaefli-wigoltingen.ch/', 'index.html'],
  ['karten', 'https://www.schaefli-wigoltingen.ch/karten-1', 'karte.html'],
  ['events', 'https://www.schaefli-wigoltingen.ch/events', 'anlaesse.html'],
  ['haus', 'https://www.schaefli-wigoltingen.ch/uber-uns', 'haus.html'],
  ['kontakt', 'https://www.schaefli-wigoltingen.ch/kontakt', 'kontakt.html'],
];
const nur = process.argv.slice(2);
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  const b = await chromium.launch({ headless: true });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, locale: 'de-CH' });
  for (const [s, alt, neu, stelle] of PAARE) {
    if (nur.length && !nur.includes(s)) continue;
    const p = await ctx.newPage(); p.setDefaultTimeout(240000);
    try {
      const r = await p.goto(alt, { waitUntil: 'load', timeout: 45000 }); await p.waitForTimeout(3500);
      for (const t of ['ablehnen', 'nur notwendige', 'nur essenzielle', 'decline', 'reject', 'alle ablehnen']) { const ab = await p.$(`text=/^\\s*${t}\\s*$/i`); if (ab) { await ab.click().catch(() => {}); await p.waitForTimeout(1500); break; } }
      await p.evaluate(async () => { for (let y = 0; y < Math.min(document.body.scrollHeight, 6000); y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });
      await p.waitForTimeout(4000);
      if (stelle) { await p.evaluate(t => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) { if (n.textContent.includes(t) && n.parentElement.offsetParent) { const r = n.parentElement.getBoundingClientRect(); scrollTo(0, Math.max(0, r.top + scrollY - 420)); return; } } }, stelle); await p.waitForTimeout(1500); }
      await p.screenshot({ path: path.join(ZIEL, s + '-alt.jpg'), quality: 90 });
      console.log('heute', s, r && r.status(), p.url(), await p.title());
    } catch (e) { console.log('alt fehlgeschlagen', s, String(e).slice(0, 160)); }
    await p.goto(NEU + neu, { waitUntil: 'load' }); await p.evaluate(() => document.fonts && document.fonts.ready);
    await p.waitForTimeout(neu === 'index.html' ? 6200 : 3800);
    await p.screenshot({ path: path.join(ZIEL, s + '-neu.jpg'), quality: 90 });
    await p.close(); console.log('Vorher/Nachher', s);
  }
  await b.close();
})();
