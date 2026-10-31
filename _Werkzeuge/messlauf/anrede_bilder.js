// Anrede 29.10.: Startansicht je Werkzeug, WebKit 1440×900 (und 390). node anrede_bilder.js <ordner> <vorher|nachher>
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright'); const path = require('path');
const [,, OUT, WANN] = process.argv;
const Z = [['tresen', 'http://127.0.0.1:9081/_werkzeuge/maison/'], ['schaufenster', 'http://127.0.0.1:9082/_werkzeuge/bureau/'], ['pairing-karte', 'http://127.0.0.1:9083/_werkzeuge/carte/'],
  ['gaestebuch', 'http://127.0.0.1:9084/_werkzeuge/reception/'], ['markenbuch', 'http://127.0.0.1:9085/_werkzeuge/livre/'], ['besucherliste', 'http://127.0.0.1:9086/_werkzeuge/registre/']];
(async () => { const b = await pw.webkit.launch();
  for (const [W, H] of [[1440, 900], [390, 844]]) { const c = await b.newContext({ viewport: { width: W, height: H }, hasTouch: W < 700 }); await c.route(/^(mailto|tel):/, r => r.abort());
    // Rundgang nicht von selbst öffnen lassen
    await c.addInitScript(() => { try { for (const w of ['maison','bureau','carte','reception','livre','registre']) localStorage.setItem('rundgang-culinarium-' + w, '1'); } catch (e) {} });
    const p = await c.newPage();
    for (const [k, u] of Z) { await p.goto(u, { waitUntil: 'load' }).catch(() => {}); await p.waitForTimeout(2500); await p.screenshot({ path: path.join(OUT, `${k}-${WANN}-${W}.jpg`), type: 'jpeg', quality: 80 }); }
    await c.close(); }
  await b.close(); console.log('fertig'); })();
