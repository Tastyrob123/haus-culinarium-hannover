/* Le Livre · Culinarium Hannover · Bildschirmbilder 1440 × 900 und 390 × 844 für La Maison, die Werkbank und den Oberchef (Safari-Kern, ohne Rundgang-Schild).
   node _werkzeuge/livre/pruefung/schirm.js <zielordner>   (Server :9085) */
const pw = require(process.env.HOME + '/Aussen-Pruefung/node_modules/playwright');
(async () => { const out = process.argv[2]; const b = await pw.webkit.launch();
  for (const [W, H] of [[1440, 900], [390, 844]]) {
    for (const [a, n] of [['start', 'uebersicht'], ['bilder', 'fotos'], ['foto', 'foto'], ['dateien', 'dateien'], ['pruefung', 'pruefung'], ['buch', 'markenbuch']]) {
      const c = await b.newContext({ viewport: { width: W, height: H }, reducedMotion: 'reduce', ...(W < 700 ? { hasTouch: true } : {}) });
      await c.addInitScript(() => localStorage.setItem('rundgang-culinarium-livre', '1'));
      const p = await c.newPage();
      await p.goto('http://127.0.0.1:9085/_werkzeuge/livre/' + (a === 'buch' ? 'buch.html' : '#' + (a === 'foto' ? 'bilder' : a)), { waitUntil: 'load' }); await p.waitForTimeout(3000);
      if (a === 'pruefung') { await p.locator('#li-bsp').click(); await p.waitForTimeout(1500); await p.evaluate(() => scrollTo(0, 0)); }
      if (a === 'foto') { const k = p.locator('#li-raster .li-f[data-k="team_alle"]'); for (let i = 0; i < 4 && !(await k.count()); i++) { await p.evaluate(() => scrollTo(0, document.body.scrollHeight)); await p.waitForTimeout(600); }
        await k.evaluate(e => e.scrollIntoView({ block: 'center' })); await p.waitForTimeout(300); await k.click({ force: true }); await p.waitForSelector('#fenster .li-det'); await p.waitForTimeout(1200);
        await p.locator('[data-vn="schieber"]').click(); await p.waitForTimeout(500); }
      await p.screenshot({ path: `${out}/livre-${n}-${W}.png` }); await c.close();
    }
  }
  await b.close(); })();
