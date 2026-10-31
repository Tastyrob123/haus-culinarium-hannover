const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright'); const messen = require('./messen.js');
const [,, LISTE, CSSX] = process.argv; const U = require('fs').readFileSync(LISTE, 'utf8').split('\n').filter(Boolean);
(async () => { for (const bn of ['chromium', 'webkit']) { const b = await pw[bn].launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  for (const u of U) { await p.goto(u, { waitUntil: 'load' }).catch(() => {}); await p.waitForTimeout(1300);
    const m = async () => (await p.evaluate(messen)).filter(x => x.art === 'text-mitte').map(x => x.sel.split(' > ').slice(-2).join(' > ') + ' · ' + x.info.split(' (')[0]);
    const vor = await m(); await p.addStyleTag({ content: CSSX }); await p.waitForTimeout(300); const nach = await m();
    console.log(bn, vor.length, '→', nach.length, u.replace('http://127.0.0.1:', '')); nach.forEach(x => console.log('     ', x)); }
  await b.close(); } })();
