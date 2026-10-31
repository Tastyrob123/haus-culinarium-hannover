// Rechnet das Muster eines Hauses (SVG als Daten-Adresse in _werkbank/muster.txt) als Bild: node muster_bild.js "<Projektordner>" <breite> <hoehe>
// → _werkbank/muster.png in doppelter Grösse. Ein Bild als Kachel ist beim Scrollen billiger als ein verwickelter Pfad, der bei jedem Bild neu gezeichnet wird.
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), b = +process.argv[3], h = +process.argv[4];
(async () => {
  const br = await chromium.launch(), p = await br.newPage({ viewport: { width: b, height: h }, deviceScaleFactor: 2 });
  const url = fs.readFileSync(path.join(ROOT, '_werkbank', 'muster.txt'), 'utf8');
  await p.setContent(`<body style="margin:0;background:transparent"><div style="width:${b}px;height:${h}px;background:url(&quot;${url.replace(/"/g, '&quot;')}&quot;) 0 0/${b}px ${h}px"></div>`);
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(ROOT, '_werkbank', 'muster.png'), omitBackground: true });
  await br.close(); console.log('muster.png', b * 2, h * 2);
})();
