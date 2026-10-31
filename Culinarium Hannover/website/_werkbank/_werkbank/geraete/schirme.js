// Werkbank Culinarium (28.10.2026, Vorlage Schäfli): Bildschirm-Inhalte für die beiden Geräte der Werkbank (Gehäuse aus Blender, übernommen vom Grand Beau-Rivage; der Inhalt ist vom Ruedihus):
//   Handy   die echte Feed-Seite (feed/index.html), nur die Bildschirmfläche, 393 × 851 CSS-Pixel, dreifache Dichte   → schirm-feed.png
//   Laptop  das Studio so, wie es beim Klick im Bildschirm lädt (1440 × 932, das Seitenverhältnis des Bildschirms)      → schirm-studio.jpg
// node _werkbank/geraete/schirme.js [feed] [studio]     (Server der Website muss laufen)
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const HIER = __dirname, B = 'http://127.0.0.1:' + (process.env.WB_PORT || 9088) + '/';
const L = JSON.parse(fs.readFileSync(path.join(HIER, 'laptop.json'), 'utf8'));
const nur = process.argv.slice(2);
const CSS = `.devwrap{animation:none!important;opacity:1!important;transform:none!important}
#device{width:393px!important;height:851px!important;padding:0!important;border-radius:0!important;box-shadow:none!important}
.screen{border-radius:0!important}.island{display:none!important}`;
(async () => {
  const b = await chromium.launch({ headless: true });
  if (!nur.length || nur.includes('feed')) {
    const p = await b.newPage({ viewport: { width: 1300, height: 1000 }, deviceScaleFactor: 3 });
    await p.goto(B + 'feed/index.html', { waitUntil: 'load' });
    await p.addStyleTag({ content: CSS });
    await p.evaluate(() => { document.querySelector('.screen').insertAdjacentHTML('beforeend', '<i style="position:absolute;left:50%;bottom:9px;width:136px;height:5px;margin-left:-68px;border-radius:3px;background:#fff;z-index:50"></i>'); return document.fonts.ready; });
    await p.waitForTimeout(6000);
    const ok = await p.evaluate(() => [...document.querySelectorAll('#device img:not(#pimg)')].filter(i => i.getBoundingClientRect().top < 900).every(i => i.complete && i.naturalWidth > 0));
    await (await p.$('.screen')).screenshot({ path: path.join(HIER, 'schirm-feed-sb.png') });
    console.log('feed', ok ? 'ok' : 'BILD FEHLT'); await p.close();
  }
  if (!nur.length || nur.includes('studio')) {
    const [w, h] = L.fenster;
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    try { await p.clock.setFixedTime(new Date('2026-10-12T11:00:00')); } catch (e) { console.log('Uhr nicht stellbar', String(e).slice(0, 80)); }   // «Guten Tag.» statt der Tageszeit der Aufnahme
    await p.goto(B + 'studio/', { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(5000);
    await p.screenshot({ path: path.join(HIER, 'schirm-studio.jpg'), quality: 90 });
    console.log('studio', await p.title(), p.url()); await p.close();
  }
  await b.close();
})();
