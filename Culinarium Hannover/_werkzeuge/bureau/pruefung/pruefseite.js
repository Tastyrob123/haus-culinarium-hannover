/* pruefseite.js · Prüfseite von Le Bureau (Culinarium) im Kleid des Hauses ansehen: Punkte, Termine, Lexikon-Sprung. node pruefseite.js <bild.png> [breite] */
const path = require('path'), os = require('os');
const pw = require(process.env.PLAYWRIGHT_PFAD || path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
(async () => {
  const br = await pw[process.env.MOTOR || 'chromium'].launch({ headless: true });
  const p = await (await br.newContext({ viewport: { width: +(process.argv[3] || 1440), height: 900 } })).newPage(), f = [];
  p.on('pageerror', e => f.push(e.message)); p.on('console', m => { if (m.type() === 'error') f.push(m.text()); });
  await p.goto('http://127.0.0.1:9082/werkzeuge/website/pruefung.html?haus=culinarium#lex-termin-plaetze', { waitUntil: 'load' });
  await p.waitForFunction(() => !document.querySelector('.wsp-wartet'), null, { timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(800);
  const r = await p.evaluate(() => ({ titel: document.title, punkte: [...document.querySelectorAll('.wsp-punkt')].map(x => x.getAttribute('data-gut')),
    termine: [...document.querySelectorAll('#cu-termine-punkte .wsp-punkt')].map(x => x.textContent), offen: !!document.querySelector('#lex-termin-plaetze[open]'),
    zurueck: document.getElementById('wsp-zurueck').getAttribute('href') }));
  await p.screenshot({ path: process.argv[2] });
  console.log(JSON.stringify(Object.assign(r, { fehler: f })));
  await br.close();
})();
