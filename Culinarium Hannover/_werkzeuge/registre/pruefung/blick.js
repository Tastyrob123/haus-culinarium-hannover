/* Schneller Blick: jede Ansicht in Chromium (und WebKit mit ?wk=1), 1440 × 900 und 390 × 844, Konsolenfehler, seitliches Verrutschen, Bild je Ansicht.
   node pruefung/blick.js [chromium|webkit] [ansicht …]   → pruefung/bilder/blick-<browser>-<breite>-<ansicht>.png */
const path = require('path');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = 'http://127.0.0.1:' + (process.env.PORT || 9086) + '/_werkzeuge/registre/';
const browser = process.argv[2] || 'chromium';
const ANS = process.argv.slice(3).length ? process.argv.slice(3) : ['start', 'besuche', 'herkunft', 'zeit', 'seiten', 'verlauf', 'buchung', 'zaehlung'];
(async () => {
  const br = await PW[browser].launch();
  let fehler = 0;
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const ctx = await br.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
    await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-culinarium-registre', '1'); } catch (e) {} });
    const p = await ctx.newPage();
    p.on('console', m => { if (m.type() === 'error') { fehler++; console.log('KONSOLE', w, m.text()); } });
    p.on('pageerror', e => { fehler++; console.log('SEITENFEHLER', w, e.message); });
    p.on('response', r => { if (r.status() >= 400) { fehler++; console.log('ANTWORT', r.status(), r.url()); } });
    for (const a of ANS) {
      await p.goto('about:blank');
      await p.goto(B + '?gruss=tag#' + a);
      await p.waitForFunction(() => window.BG_REGISTRE === 1, null, { timeout: 15000 });
      await p.waitForTimeout(500);
      await p.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
      await p.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 8000 }).catch(() => {});
      await p.waitForTimeout(300);
      const breit = await p.evaluate(wv => { let m = 0, wer = ''; document.querySelectorAll('body *').forEach(el => { const r = el.getBoundingClientRect(); if (r.width && r.right > wv + 1 && getComputedStyle(el).position !== 'fixed' && el.id !== 'zeichen' && !el.closest('svg defs')) { if (r.right - wv > m) { m = r.right - wv; wer = el.className || el.tagName; } } }); return [Math.round(m), String(wer).slice(0, 60), document.documentElement.scrollWidth]; }, w);
      if (breit[0] > 1) console.log('RAGT', w, a, breit);
      const leer = await p.evaluate(() => [...document.images].filter(i => i.complete && !i.naturalWidth).map(i => i.getAttribute('src')));
      if (leer.length) { fehler++; console.log('LEERES BILD', w, a, leer); }
      await p.screenshot({ path: path.join(__dirname, 'bilder', `blick-${browser}-${w}-${a}.png`), fullPage: true });
    }
    await ctx.close();
  }
  await br.close();
  console.log('fertig, Fehler:', fehler);
})();
