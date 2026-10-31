/* Bildschirmbilder Das Besucherbuch · Berghotel Gasterntal für die Stube, die Werkbank (Laptop) und die Lieferung: Safari-Kern 1440 × 900 und 390 × 844,
   jede Ansicht, ?gruss=tag, Beispielwerte; dazu das Schild «Kurzer Rundgang» (ohne Automaten-Kennung). Vorlage: Carlton _pruefung-1016/bilder.js.
   node bilder.js [basis]   → bilder/webkit-1440-<ansicht>.png, bilder/webkit-390-<ansicht>.png, bilder/schirm-1440.png (für La Maison / Laptop) */
const path = require('path'), fs = require('fs');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const BASIS = process.argv[2] || 'http://localhost:8988/_werkzeuge/registre/';
const ZIEL = path.join(__dirname, 'bilder');
const ANSICHTEN = ['start', 'besuche', 'herkunft', 'zeit', 'seiten', 'verlauf', 'buchung', 'zaehlung'];
const BEREIT = () => window.BG_REGISTRE === 1 && document.documentElement.classList.contains('auftakt-da');
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  const b = await PW.webkit.launch();
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: w > 600 ? 1 : 2, hasTouch: w < 600 });
    for (const v of ANSICHTEN) {
      const p = await ctx.newPage();
      await p.goto(BASIS + '?gruss=tag#' + v); await p.waitForFunction(BEREIT);
      await p.waitForTimeout(3400);   /* Bühne und Blätter sind angekommen */
      const breit = await p.evaluate(() => document.documentElement.scrollWidth);
      await p.screenshot({ path: path.join(ZIEL, `webkit-${w}-${v}.png`) });
      if (w === 1440 && v === 'start') fs.copyFileSync(path.join(ZIEL, `webkit-${w}-${v}.png`), path.join(ZIEL, 'schirm-1440.png'));
      console.log(w, v, 'Breite', breit);
      await p.close();
    }
    await ctx.close();
    const c2 = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: w > 600 ? 1 : 2 });
    await c2.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }));
    const p2 = await c2.newPage(); await p2.goto(BASIS + '?gruss=tag#start'); await p2.waitForSelector('.rdg-schild', { timeout: 15000 }); await p2.waitForTimeout(1100);
    await p2.screenshot({ path: path.join(ZIEL, `webkit-${w}-schild.png`) });
    await p2.click('.rdg-los'); await p2.waitForTimeout(900); await p2.screenshot({ path: path.join(ZIEL, `webkit-${w}-rundgang.png`) });
    await c2.close();
  }
  await b.close();
})();
