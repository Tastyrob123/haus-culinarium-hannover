// Rendert die Tafeln des Feeds und das Profilbild: node feed_druck.js "<Projektordner>"   (vorher python3 feed.py, danach noch einmal für die Raster-Bilder)
// Mit --handy: nimmt das Handy der Feed-Seite für die Werkbank auf (_werkbank/ansichten/Ziele/feed-handy.png, feed-raster.png).
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), HIER = path.join(ROOT, '_werkbank');
const B = JSON.parse(fs.readFileSync(path.join(HIER, 'plan.json'), 'utf8')).base;
(async () => {
  const b = await chromium.launch();
  if (!process.argv.includes('--handy')) {
    const p = await b.newPage({ viewport: { width: 1100, height: 1400 }, deviceScaleFactor: 1 });
    await p.goto(B + 'feed/_tafeln.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(700);
    for (const k of await p.$$('.k')) { const nr = await k.getAttribute('data-nr'); await k.screenshot({ path: path.join(ROOT, 'feed/posts', String(nr).padStart(2, '0') + '.jpg'), type: 'jpeg', quality: 92 }); }
    await (await p.$('#av')).screenshot({ path: path.join(ROOT, 'feed/avatar-roh.png') });
    console.log('Tafeln gerendert');
    await p.close();
  } else {
    const Z = path.join(HIER, 'ansichten', 'Ziele'); fs.mkdirSync(Z, { recursive: true });
    const p = await b.newPage({ viewport: { width: 1300, height: 1000 }, deviceScaleFactor: 2 });
    await p.goto(B + 'feed/index.html', { waitUntil: 'load' }); await p.waitForTimeout(4200);
    await (await p.$('#device')).screenshot({ path: path.join(Z, 'feed-handy.png'), omitBackground: true });
    await p.evaluate(() => { document.getElementById('scroll').scrollTop = 330; }); await p.waitForTimeout(500);
    await (await p.$('#device')).screenshot({ path: path.join(Z, 'feed-raster.png'), omitBackground: true });
    console.log('Handy aufgenommen');
    await p.close();
  }
  await b.close();
})();
