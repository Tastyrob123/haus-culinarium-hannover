// Breiten-Lauf La Réception · Culinarium Hannover (28.10.2026): Fehlerbuch 10a «jede Ansicht bei 920, 1000, 1024, 1100, 1240 auf seitliches Überragen,
// jedes Element gegen die Fensterbreite» (Schäfli Le Registre / L’Imprimerie), «Titel im Kopf überdeckt nie einen Knopf, kürzt mit …» (Schlössli, Schäfli),
// «Werkzeug-Titel bei 390 gegen die Breite seines Kopfbilds» (Schlössli La Carte) und «Titelzeile auf dunkler Fläche hell» (Schlössli Reservationsbuch).
//   node breiten.js <basis, z. B. http://127.0.0.1:9184> [chromium|webkit]
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const SCHUTZ = require('./schutz');
const [, , BASIS = 'http://127.0.0.1:9184', MOTOR = 'chromium'] = process.argv;
const WZ = BASIS + '/_werkzeuge/reception/', sleep = ms => new Promise(r => setTimeout(r, ms));
const ANSICHTEN = ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen'], BREITEN = [390, 920, 1000, 1024, 1100, 1240, 1440];
(async () => {
  const br = await SCHUTZ.start(pw, MOTOR); const rot = [], zeilen = [];
  for (const W of BREITEN) {
    const ctx = await SCHUTZ.kontext(br, { viewport: { width: W, height: W < 700 ? 844 : 900 }, locale: 'de-DE' });
    await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-reception', '1'); localStorage.setItem('rundgang-savoir', '1'); } catch (e) { /* */ } });
    const p = await ctx.newPage(); p.setDefaultTimeout(30000);
    for (const a of ANSICHTEN) {
      await p.goto('about:blank'); await p.goto(WZ + '#' + a, { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await sleep(1200);
      if (a === 'eingang') { const k = p.locator('.re-liste .re-a', { hasText: 'Mira Schulte' }).first(); await k.scrollIntoViewIfNeeded(); await k.click(); await sleep(900); }
      const m = await p.evaluate(W => {
        const raus = [...document.querySelectorAll('#kopf *, #rand *, #ansicht *, #leiste *')].filter(e => { const r = e.getBoundingClientRect(), st = getComputedStyle(e);
          if (!r.width || st.visibility === 'hidden' || e.closest('[hidden], .wo-rand:not(.wo-auf)') && W < 700 && e.closest('#rand')) return false;
          if (r.right <= W + 1 || e.closest('.ws-wahl__l, .lf, [data-lauf]')) return false;
          let rahmen = null;
          for (let x = e.parentElement; x && x !== document.body; x = x.parentElement) { const o = getComputedStyle(x).overflowX;
            if (o === 'auto' || o === 'scroll') return x.getBoundingClientRect().right > W + 1;   // in einem rollenden Streifen: zählt nur, wenn der Streifen selbst hinausragt
            if ((o === 'hidden' || o === 'clip') && !rahmen) rahmen = x; }
          return rahmen ? rahmen.getBoundingClientRect().right > W + 1 : true; }).map(e => (e.className && e.className.baseVal === undefined ? String(e.className).split(' ')[0] : e.tagName) + ' ' + Math.round(e.getBoundingClientRect().right));
        const t = document.querySelector('#kopf .wo-kopf__mitte b'), kn = [...document.querySelectorAll('#kopf .wo-kopf__r > *')];
        const tr = t ? t.getBoundingClientRect() : null, ueber = tr && tr.width ? kn.filter(k => { const r = k.getBoundingClientRect(); return r.width && r.left < tr.right - 1 && r.right > tr.left + 1 && r.top < tr.bottom && r.bottom > tr.top; }).length : 0;
        const h1 = document.querySelector('#ansicht .wo-sb h1, #ansicht .wo-sb__h'), hb = h1 ? h1.getBoundingClientRect() : null, sb = document.querySelector('#ansicht .wo-sb'), sr = sb ? sb.getBoundingClientRect() : null;
        const farbe = h1 ? getComputedStyle(h1).color : '', hell = farbe ? (m => m && (+m[1] + +m[2] + +m[3]) / 3 > 200)(farbe.match(/(\d+), (\d+), (\d+)/)) : true;
        return { raus: raus.slice(0, 4), ueber, titel: hb && sr ? Math.round(hb.right - sr.right) : 0, hell, sw: document.documentElement.scrollWidth - W };
      }, W);
      const f = [];
      if (m.raus.length) f.push('ragt hinaus: ' + m.raus.join(', ')); if (m.sw > 0) f.push('seitlich ' + m.sw + ' px'); if (m.ueber) f.push('Kopftitel über ' + m.ueber + ' Knopf');
      if (m.titel > 1) f.push('Bühnentitel ragt ' + m.titel + ' px über die Bühne'); if (!m.hell) f.push('Titel auf dunkler Bühne nicht hell');
      zeilen.push(`${W} ${a}: ${f.length ? 'ROT ' + f.join(' · ') : 'ok'}`); if (f.length) rot.push(`${W} ${a}`);
    }
    await ctx.close();
  }
  await br.close();
  console.log(zeilen.join('\n')); console.log(`\nbreiten ${MOTOR}: ${zeilen.length - rot.length} von ${zeilen.length} grün`);
  fs.mkdirSync(path.join(__dirname, 'lauf'), { recursive: true }); fs.writeFileSync(path.join(__dirname, 'lauf', `breiten-${MOTOR}.txt`), zeilen.join('\n') + '\n');
  process.exit(rot.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
