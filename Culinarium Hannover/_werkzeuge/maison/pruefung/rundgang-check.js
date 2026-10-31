// Tresen mit ?rundgang: jeder Zustand des Rundgangs bedient (Weiter, Zurück mit ←, Überspringen, Escape, «Los geht’s»), WebKit + Chromium, 1440/1000/390.
// Aufruf: node pruefung/rundgang-check.js [webkit|chromium]   Bilder: pruefung/rundgang-3010/
const pw = require('playwright'), path = require('path');
const MOTOR = process.argv[2] || 'webkit', URL = 'http://127.0.0.1:9081/_werkzeuge/maison/?rundgang', BILD = path.join(__dirname, 'rundgang-3010');
let gruen = 0, rot = 0; const ok = (w, t, b, x) => { b ? gruen++ : rot++; if (!b) console.log('ROT', MOTOR, w, t, x === undefined ? '' : JSON.stringify(x)); };
(async () => {
  const b = await pw[MOTOR].launch();
  for (const [W, H] of [[1440, 900], [1000, 650], [390, 844]]) {
    const w = W + 'x' + H, hand = W < 700;
    const neu = async () => { const ctx = await b.newContext({ viewport: { width: W, height: H }, hasTouch: hand, isMobile: hand && MOTOR === 'chromium' }); const page = await ctx.newPage(); const f = [];
      page.on('pageerror', e => f.push(e.message)); await page.goto(URL, { waitUntil: 'load' }); const k = await page.waitForSelector('.rdg-karte', { timeout: 15000 }).catch(() => null); await page.waitForTimeout(700); return { ctx, page, f, k }; };
    const stand = page => page.evaluate(() => { const k = document.querySelector('.rdg-karte'), g = document.querySelector('.rdg-kegel'); if (!k) return null; const r = k.getBoundingClientRect(), q = g.getBoundingClientRect();
      return { nr: (k.querySelector('.rdg-zier span') || {}).textContent, titel: (k.querySelector('h3') || {}).textContent, karteImBild: r.left >= -1 && r.right <= innerWidth + 1 && r.top >= -1 && r.bottom <= innerHeight + 1,
        kegel: q.width > 8 && q.height > 8 && q.bottom > 0 && q.top < innerHeight, deckt: !(r.right <= q.left || r.left >= q.right || r.bottom <= q.top || r.top >= q.bottom) && innerWidth > 700, knoepfe: [...k.querySelectorAll('button')].map(x => x.textContent.trim()) }; });
    const frei = page => page.evaluate(() => !document.querySelector('.rdg-karte,.rdg-sperre,.rdg-kegel') && localStorage.getItem('rundgang-culinarium-maison') === '1');
    const klick = async (page, sel) => { const e = await page.$(sel); if (hand) await e.tap(); else await e.click(); await page.waitForTimeout(800); };
    // 1 alle Schritte mit «Weiter», Bild je Schritt, am Ende «Los geht’s»
    { const { ctx, page, f, k } = await neu(); ok(w, '?rundgang öffnet die Karte', !!k);
      const titel = []; for (let n = 0; n < 8 && (await page.$('.rdg-karte')); n++) { const s = await stand(page); titel.push(s.titel);
        ok(w, `Schritt ${n + 1} Karte ganz im Bild`, s.karteImBild, s); ok(w, `Schritt ${n + 1} Ziel hervorgehoben`, s.kegel, s); ok(w, `Schritt ${n + 1} Karte deckt das Ziel nicht`, !s.deckt, s);
        if (MOTOR === 'webkit' && W !== 1000) await page.screenshot({ path: path.join(BILD, `${MOTOR}-${W}-schritt-${n + 1}.png`) });
        await klick(page, '.rdg-los'); }
      ok(w, 'fünf Schritte, letzter «Los geht’s» schliesst', titel.length === 5 && await frei(page), titel);
      // danach bedienbar: scrollen und ein Fenster lässt sich anklicken (kein Deckel übrig)
      const oben = await page.evaluate(() => { scrollTo(0, 600); const a = document.querySelector('.m-f5__k, .rw-g a'); scrollTo(0, 0); const r = a.getBoundingClientRect(); const e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return !!(e && e.closest('a')); });
      ok(w, 'nach dem Rundgang ist die Seite frei bedienbar', oben); ok(w, 'ohne Fehler (Durchgang)', !f.length, f); await ctx.close(); }
    // 2 Zurück mit ← und vor mit →, dann «Überspringen» in Schritt 3
    { const { ctx, page, f } = await neu();
      await klick(page, '.rdg-los'); const s2 = await stand(page); await page.keyboard.press('ArrowLeft'); await page.waitForTimeout(700); const s1 = await stand(page);
      ok(w, '← geht einen Schritt zurück', s1 && /1 von/.test(s1.nr) && /2 von/.test(s2.nr), [s1 && s1.nr, s2 && s2.nr]);
      await page.keyboard.press('ArrowRight'); await page.waitForTimeout(500); await page.keyboard.press('Enter'); await page.waitForTimeout(700); const s3 = await stand(page);
      ok(w, '→ und Enter gehen weiter', s3 && /3 von/.test(s3.nr), s3 && s3.nr);
      ok(w, '«Überspringen» da (nicht im letzten Schritt)', s3 && s3.knoepfe.some(t => /Überspringen/.test(t)), s3 && s3.knoepfe);
      await klick(page, '.rdg-zu'); ok(w, '«Überspringen» schliesst und merkt es sich', await frei(page)); ok(w, 'ohne Fehler (Zurück/Überspringen)', !f.length, f); await ctx.close(); }
    // 3 Escape im ersten Schritt
    { const { ctx, page, f } = await neu(); await page.keyboard.press('Escape'); await page.waitForTimeout(500);
      ok(w, 'Escape schliesst', await frei(page)); ok(w, 'ohne Fehler (Escape)', !f.length, f); await ctx.close(); }
    // 4 ohne ?rundgang, schon gesehen: kein Rundgang von selbst
    { const ctx = await b.newContext({ viewport: { width: W, height: H } }); const page = await ctx.newPage();
      await page.goto(URL.replace('?rundgang', ''), { waitUntil: 'load' }); await page.waitForTimeout(3000);
      ok(w, 'ohne ?rundgang startet nichts von selbst', !(await page.$('.rdg-karte'))); await ctx.close(); }
  }
  await b.close(); console.log(`${MOTOR}: ${gruen} grün, ${rot} rot`);
})();
