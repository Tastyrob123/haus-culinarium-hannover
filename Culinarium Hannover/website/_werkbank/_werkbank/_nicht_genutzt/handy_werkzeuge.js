// Werkbank Ruedihus (Werkbank-Chat 17.10.2026 spät, Regel 15 «Ein Laptop»): die Stube, die sechs Werkzeuge und die Analyse am Handy,
// damit in den Fächern nie zwei Laptops nebeneinander stehen. 390 × 844, doppelte Dichte, nur lesen (jede Anfrage ausser GET/HEAD wird abgefangen).
//   node _werkbank/handy_werkzeuge.js [name …]   → _werkbank/ansichten/Werkzeuge-Handy/<name>.jpg   (Hausserver :8917 muss laufen)
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const H = 'http://127.0.0.1:8917', A = path.join(__dirname, 'ansichten', 'Werkzeuge-Handy');
const ZIELE = { maison: H + '/_werkzeuge/maison/?gruss=abend', bureau: H + '/studio/', carte: H + '/_werkzeuge/carte/', reception: H + '/_werkzeuge/reception/',
  livre: H + '/_werkzeuge/livre/', registre: H + '/_werkzeuge/registre/', imprimerie: H + '/_werkzeuge/imprimerie/', analyse: 'https://ruedihus-analyse.tastystudios.ch/?cb=' + Date.now() };
const nur = process.argv.slice(2);
(async () => {
  fs.mkdirSync(A, { recursive: true });
  const b = await chromium.launch();
  for (const [name, url] of Object.entries(ZIELE)) {
    if (nur.length && !nur.includes(name)) continue;
    const c = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    await c.route(/^(mailto|tel):/, r => r.abort());
    await c.route('**/*', r => ['GET', 'HEAD'].includes(r.request().method()) ? r.continue() : r.fulfill({ status: 204, body: '' }));
    await c.addInitScript(() => { try { for (let i = 0; i < localStorage.length; i++) {} ['rundgang-bureau', 'rundgang-rh-livre', 'rundgang-livre', 'rundgang-rh-registre', 'rundgang-ruedihus-carte', 'rundgang-carte', 'rundgang-reception', 'rundgang-rh-reception', 'rundgang-maison', 'rundgang-imprimerie', 'rundgang-rh-imprimerie'].forEach(k => localStorage.setItem(k, '1')); localStorage.setItem('lc-wer', 'Probe'); ['ruedihus', 'landgasthof-ruedihus', 'rh'].forEach(h => { localStorage.setItem('ds-' + h + '-willkommen', '1'); localStorage.setItem('ds-' + h + '-beispiele2', '1'); }); localStorage.setItem('lc-rolle', 'direktion'); localStorage.setItem('lc-modus', 'einfach'); } catch (e) {} });
    const p = await c.newPage(); const f = [];
    p.on('pageerror', e => f.push(e.message));
    await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => f.push(e.message));
    await p.waitForTimeout(3500);
    await p.addStyleTag({ content: '[class*="rundgang"],.rdg,.rdg-fenster,#rundgang{display:none!important}' }).catch(() => {});
    await p.evaluate(y => window.scrollTo(0, y), name === 'analyse' ? 150 : 0); await p.waitForTimeout(1200);   // Analyse: oben liegt ein weicher Verlauf im Himmel (Robert 18.10.: «verblurrt»), deshalb ab dem Namen
    await p.screenshot({ path: path.join(A, name + '.jpg'), type: 'jpeg', quality: 90 });
    console.log(name, f.length ? 'Fehler: ' + f.join(' | ').slice(0, 160) : 'ok');
    await c.close();
  }
  await b.close();
})();
