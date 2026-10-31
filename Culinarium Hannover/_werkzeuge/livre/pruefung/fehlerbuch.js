// Le Livre · Culinarium Hannover · Fehlerbuch 10a, die Zeilen, die kein anderer Lauf misst (28.10.2026), gegen den Prüfserver :9085.
//   NODE_PATH=~/Aussen-Pruefung/node_modules node _werkzeuge/livre/pruefung/fehlerbuch.js chromium|webkit
// 58  kein roher Vorlagen-Code ({…}, undefined, NaN, None, null) in keiner Ansicht, keinem Fenster, Markenbuch, Anleitung
// 127 Titel im Kopf überdeckt nie einen Knopf (920, 1000, 1100, 1240 px, jede Ansicht)
// 115 Rundgang-Schild steht fest über der Leiste unten rechts, auch nach geänderter Fenstergrösse
// 66  Titelzeilen auf dunkler Fläche (Kopf, Bühnen) hell
const pw = require('playwright'), fs = require('fs'), path = require('path');
const U = (process.env.BASIS || 'http://127.0.0.1:9085/') + '_werkzeuge/livre/', motor = process.argv[2] || 'chromium';
const zeilen = []; const Z = (nr, was, ok, m = '') => zeilen.push(`${ok ? 'ok  ' : 'FEHL'} ${nr} ${was}${m !== '' ? ' · ' + m : ''}`);
const ROH = /\{[a-z_]+\}|\bundefined\b|\bNaN\b|\bNone\b|\bnull\b|\[object Object\]/;
(async () => {
  const b = await pw[motor].launch();
  let c = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  await c.addInitScript(() => { try { localStorage.setItem('rundgang-culinarium-livre', '1'); } catch (e) {} });
  let p = await c.newPage();
  const roh = [];
  for (const a of ['#start', '#bilder', '#dateien', '#pruefung', 'buch.html', 'anleitung.html', 'buch/logo-richtig-falsch/index.html']) {
    await p.goto('about:blank'); await p.goto(U + a, { waitUntil: 'load' }); await p.waitForTimeout(2200);
    if (a === '#pruefung') { await p.locator('#li-bsp').click(); await p.waitForTimeout(1200); }
    const t = await p.evaluate(() => document.body.innerText + ' ' + [...document.querySelectorAll('[title],[aria-label],[alt]')].map(e => (e.getAttribute('title') || '') + ' ' + (e.getAttribute('aria-label') || '') + ' ' + (e.getAttribute('alt') || '')).join(' '));
    const m = t.match(ROH); if (m) roh.push(a + ': ' + m[0]);
    if (a === '#bilder') for (const k of ['pass4', 'ws00', 'team_alle', 'p_DbYnkdkjrNy']) {
      const l = p.locator(`#li-raster .li-f[data-k="${k}"]`);
      for (let i = 0; i < 6 && !(await l.count()); i++) { await p.evaluate(() => scrollTo(0, document.body.scrollHeight)); await p.waitForTimeout(500); }
      await l.evaluate(e => e.scrollIntoView({ block: 'center' })); await l.click({ force: true }); await p.waitForSelector('#fenster .li-det'); await p.waitForTimeout(500);
      const ft = await p.locator('#fenster').innerText(); const mm = ft.match(ROH); if (mm) roh.push('Foto ' + k + ': ' + mm[0]);
      await p.keyboard.press('Escape'); await p.waitForTimeout(200);
    }
  }
  Z(58, 'Kein roher Vorlagen-Code in Ansichten, Foto-Fenstern, Markenbuch, Anleitung', roh.length === 0, roh.join(' | ') || '7 Seiten, 4 Fenster');
  // 66 Titel auf dunkler Fläche hell
  await p.goto('about:blank'); await p.goto(U + '#start', { waitUntil: 'load' }); await p.waitForTimeout(2000);
  const hell = await p.evaluate(() => [...document.querySelectorAll('#kopf b, #kopf strong, .wo-sb h1, .wo-sb__h')].map(e => { const m = getComputedStyle(e).color.match(/\d+/g).map(Number); return (m[0] + m[1] + m[2]) / 3; }));
  Z(66, 'Titelzeilen auf dunkler Fläche (Kopf, Startbild) hell', hell.length > 0 && hell.every(x => x > 200), hell.map(Math.round).join(' '));
  // 127 Kopf
  const kopf = [];
  for (const w of [920, 1000, 1100, 1240]) for (const a of ['start', 'bilder', 'dateien', 'pruefung']) {
    await p.setViewportSize({ width: w, height: 800 }); await p.goto('about:blank'); await p.goto(U + '#' + a, { waitUntil: 'load' }); await p.waitForTimeout(1200);
    const r = await p.evaluate(() => { const t = document.querySelector('#kopf .wo-kopf__mitte'); if (!t) return 'ohne Titel'; const tb = t.getBoundingClientRect();
      const kn = [...document.querySelectorAll('#kopf a, #kopf button')].filter(x => !t.contains(x) && x.offsetParent).map(x => x.getBoundingClientRect());
      return kn.some(k => !(k.right <= tb.left || k.left >= tb.right || k.bottom <= tb.top || k.top >= tb.bottom)) ? 'überdeckt' : ''; });
    if (r) kopf.push(`${w} ${a}: ${r}`);
  }
  Z(127, 'Titel im Kopf überdeckt bei 920, 1000, 1100, 1240 px nie einen Knopf', kopf.length === 0, kopf.join(' | ') || '16 Messungen');
  await c.close();
  // 115 Rundgang-Schild
  c = await b.newContext({ viewport: { width: 1440, height: 900 } });
  await c.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); });   // das Schild zeigt sich Prüfbrowsern sonst nie (rundgang.js)
  p = await c.newPage();
  await p.goto(U + '#bilder', { waitUntil: 'load' }); await p.waitForSelector('.rdg-schild', { timeout: 12000 }).catch(() => {}); await p.waitForTimeout(900);
  const lage = async () => p.evaluate(() => { const s = document.querySelector('.rdg-schild'), l = document.querySelector('#leiste'); if (!s) return null; const a = s.getBoundingClientRect(), b = l.getBoundingClientRect(); return [Math.round(innerWidth - a.right), Math.round(b.top - a.bottom)]; });
  const l1 = await lage(); await p.evaluate(() => scrollTo(0, 2400)); await p.waitForTimeout(600); const l2 = await lage();
  await p.setViewportSize({ width: 1100, height: 760 }); await p.waitForTimeout(700); const l3 = await lage();
  Z(115, 'Rundgang-Schild fest über der Leiste unten rechts, wandert beim Scrollen nicht, sitzt nach neuer Fenstergrösse wieder über der Leiste', !!l1 && JSON.stringify(l1) === JSON.stringify(l2) && !!l3 && l3[1] >= 0 && l3[1] < 40, JSON.stringify([l1, l2, l3]));
  await b.close();
  const aus = [`Le Livre · Culinarium · Fehlerbuch 10a · ${motor} · ${new Date().toLocaleString('de-DE')}`, ...zeilen, `${zeilen.filter(z => z.startsWith('ok')).length} von ${zeilen.length} ok`].join('\n');
  fs.writeFileSync(path.join(__dirname, 'ergebnisse', `fehlerbuch-${motor}.txt`), aus + '\n'); console.log(aus);
})().catch(e => { console.log(zeilen.join('\n')); console.log('ABBRUCH', e.message.split('\n')[0]); process.exit(1); });
