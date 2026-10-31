// Kriterium 24: nur die Regel zier-x über eine Liste von Adressen (Start jeder Seite, durchgerollt). node zier_x.js <adressen.txt>
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright'); const fs = require('fs'); const messen = require('./messen.js');
const U = fs.readFileSync(process.argv[2], 'utf8').split('\n').filter(Boolean);
(async () => { const b = await pw.chromium.launch(); const c = await b.newContext({ viewport: { width: 1440, height: 900 } });
  await c.route('**/*', r => { const q = r.request(); if (/^(mailto|tel):/.test(q.url())) return r.abort(); return q.method() === 'GET' ? r.continue() : r.fulfill({ status: 200, body: '{}' }); });
  const p = await c.newPage(); const aus = [];
  for (const u of U) { await p.goto(u, { waitUntil: 'load', timeout: 30000 }).catch(() => {}); await p.waitForTimeout(1500);
    const H = await p.evaluate(() => document.documentElement.scrollHeight).catch(() => 0); for (let y = 0; y < Math.min(H, 20000); y += 700) { await p.evaluate(v => scrollTo(0, v), y).catch(() => {}); await p.waitForTimeout(50); }
    const f = (await p.evaluate(messen).catch(() => [])).filter(x => x.art === 'zier-x'); aus.push({ u, f }); console.log(f.length, u); for (const x of f) console.log('   ', x.sel.slice(-60), '|', x.info); }
  fs.writeFileSync(process.argv[2] + '.json', JSON.stringify(aus, null, 1)); await b.close(); })();
