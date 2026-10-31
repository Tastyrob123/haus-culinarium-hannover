// Regel text-mitte alt gegen neu auf denselben Seiten (30.10.2026): node tm_vergleich.js <adressen.txt> <alt-messen.js> <aus.json>
// Je Seite einmal laden, dann beide Fassungen der Regel auf demselben Zustand messen. Chromium und WebKit, 1440 und 390.
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright'); const fs = require('fs');
const neu = require('./messen.js'), alt = require(require('path').resolve(process.argv[3]));
const U = fs.readFileSync(process.argv[2], 'utf8').split('\n').filter(Boolean);
(async () => { const aus = [];
  for (const bn of ['chromium', 'webkit']) { const b = await pw[bn].launch();
    for (const W of (process.env.GR || '1440,390').split(',').map(Number)) { const c = await b.newContext({ viewport: { width: W, height: W < 700 ? 844 : W <= 1000 ? 650 : 900 }, hasTouch: W < 700, isMobile: W < 700 && bn === 'chromium' });
      await c.route('**/*', r => { const q = r.request(); if (/^(mailto|tel):/.test(q.url())) return r.abort(); return q.method() === 'GET' ? r.continue() : r.fulfill({ status: 200, body: '{}' }); });
      const p = await c.newPage();
      for (const u of U) { await p.goto(u, { waitUntil: 'load', timeout: 30000 }).catch(() => {}); await p.waitForTimeout(1500);
        const H = () => p.evaluate(() => document.documentElement.scrollHeight).catch(() => 0); for (let y = 0; y < Math.min(await H(), 20000); y += 700) { await p.evaluate(v => scrollTo(0, v), y).catch(() => {}); await p.waitForTimeout(40); }
        await p.evaluate(() => scrollTo(0, 0)).catch(() => {}); await p.waitForTimeout(600);
        const m = async f => (await p.evaluate(f).catch(() => [])).filter(x => (process.env.ARTEN || 'text-mitte').split(',').includes(x.art)).map(x => ({ sel: x.sel, text: x.text, info: x.info, r: x.r }));
        const a = await m(alt), n = await m(neu); const key = x => x.sel + '¦' + x.text;
        const weg = a.filter(x => !n.some(y => key(y) === key(x))), dazu = n.filter(x => !a.some(y => key(y) === key(x)));
        let bild = null; if (weg.length || dazu.length) { bild = `${bn}-${W}-${aus.length}.png`; await p.screenshot({ path: require('path').join(require('path').dirname(process.argv[4]), bild) }).catch(() => {}); }
        aus.push({ u, bn, W, alt: a.length, neu: n.length, weg, dazu, bild }); console.log(bn, W, 'alt', a.length, 'neu', n.length, 'weg', weg.length, 'dazu', dazu.length, u); }
      await c.close(); }
    await b.close(); }
  fs.writeFileSync(process.argv[4], JSON.stringify(aus, null, 1)); })();
