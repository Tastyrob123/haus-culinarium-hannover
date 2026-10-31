const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright'); const messen = require('./messen.js');
const [,, URL, CSSX] = process.argv;
(async () => { for (const bn of ['chromium', 'webkit']) { const b = await pw[bn].launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(URL, { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const vor = (await p.evaluate(messen)).filter(x => x.art === 'text-mitte').map(x => x.sel.split(' > ').pop() + ' ' + x.info.split(' (')[0]);
  await p.addStyleTag({ content: CSSX }); await p.waitForTimeout(300);
  const nach = (await p.evaluate(messen)).filter(x => x.art === 'text-mitte').map(x => x.sel.split(' > ').pop() + ' ' + x.info.split(' (')[0]);
  console.log(bn, 'vorher', vor.length, 'nachher', nach.length); nach.slice(0, 8).forEach(x => console.log('   ', x)); await b.close(); } })();
