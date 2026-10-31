// Eine Regel (ML_ART) über eine Liste von Adressen: Start jeder Seite, durchgerollt; Chromium und WebKit, 1440 und 390. node nur_regel.js <adressen.txt> [ausgabe.json]
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright'); const fs = require('fs'); const messen = require('./messen.js');
const ART = process.env.ML_ART || 'zier-x'; const U = fs.readFileSync(process.argv[2], 'utf8').split('\n').filter(Boolean);
const BR = (process.env.ML_BROWSER || 'chromium,webkit').split(','), GR = (process.env.ML_GROESSE || '1440,390').split(',').map(Number);
(async () => { const aus = [];
  for (const bn of BR) { const b = await pw[bn].launch();
    for (const W of GR) { const c = await b.newContext({ viewport: { width: W, height: W < 700 ? 844 : 900 }, hasTouch: W < 700, isMobile: W < 700 && bn === 'chromium' });
      await c.route('**/*', r => { const q = r.request(); if (/^(mailto|tel):/.test(q.url())) return r.abort(); return q.method() === 'GET' ? r.continue() : r.fulfill({ status: 200, body: '{}' }); });
      const p = await c.newPage();
      for (const u of U) { await p.goto(u, { waitUntil: 'load', timeout: 30000 }).catch(() => {}); await p.waitForTimeout(1500);
        const H = () => p.evaluate(() => document.documentElement.scrollHeight).catch(() => 0); for (let y = 0; y < Math.min(await H(), 20000); y += 700) { await p.evaluate(v => scrollTo(0, v), y).catch(() => {}); await p.waitForTimeout(40); }
        await p.evaluate(() => scrollTo(0, 0)).catch(() => {}); await p.waitForTimeout(600);
        const f = (await p.evaluate(messen).catch(() => [])).filter(x => ART.split(',').includes(x.art)); aus.push({ u, bn, W, f: f.map(x => ({ art: x.art, sel: x.sel, text: x.text, info: x.info })) }); console.log(bn, W, f.length, u); }
      await c.close(); }
    await b.close(); }
  fs.writeFileSync(process.argv[3] || (process.argv[2] + '.json'), JSON.stringify(aus, null, 1)); })();
