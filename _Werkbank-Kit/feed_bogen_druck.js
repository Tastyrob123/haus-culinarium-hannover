// Rendert die Tafeln und Plakate eines Feed-Bogens: node feed_bogen_druck.js <feed/_bogen.html> <feed/_stuecke>
// Ein Browser, unsichtbar, ohne Server (Datei direkt). Jeder Abschnitt .st wird in voller Grösse als PNG abgelegt (data-id.png).
const path = require('path');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const [, , DATEI, ZIEL] = process.argv;
(async () => {
  const b = await chromium.launch();
  try {
    const p = await b.newPage({ viewport: { width: 3200, height: 1600 }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.resolve(DATEI), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => null))));
    await p.waitForTimeout(500);
    for (const s of await p.$$('section.st')) {
      const id = await s.getAttribute('data-id');
      await s.screenshot({ path: path.join(ZIEL, id + '.png') });
    }
    console.log('Bogen-Tafeln gerendert');
  } finally { await b.close(); }
})();
