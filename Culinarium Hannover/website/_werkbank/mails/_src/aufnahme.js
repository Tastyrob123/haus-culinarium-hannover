// Mails von Culinarium (Vorlage Schäfli, 28.10.2026): x und Wortmarke als PNG für die Mails (einmal) und der obere Teil jeder Mail als Bild für die Werkbank, doppelte Dichte.
// node mails/_src/aufnahme.js   (Server 9088 läuft; vorher python3 mails/_src/bau.py)  → mails/img/zeichen.png, _werkbank/ansichten/Mails/NN.jpg
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.join(__dirname, '..', '..'), B = 'http://127.0.0.1:' + (process.env.WB_PORT || 9088) + '/';
const liste = JSON.parse(fs.readFileSync(path.join(__dirname, 'werkbank.json'), 'utf8'));
(async () => {
  const b = await chromium.launch({ headless: true });
  const z = await b.newPage({ viewport: { width: 400, height: 540 }, deviceScaleFactor: 1 });
  // Culinarium: das C in Orange (Zeichen des Hauses, Kriterium 24; vorher das x) und die Wortmarke in Warmweiß, als PNG für die Mails (Mailprogramme zeigen kein SVG)
  const x = fs.readFileSync(path.join(ROOT, '_werkbank/eigen/zeichen-c.svg'), 'utf8').replace(/fill="(currentColor|#000)"/, 'fill="#ef7649"');
  await z.setContent('<body style="margin:0;background:transparent"><div id="z" style="width:200px">' + x.replace('<svg ', '<svg style="display:block;width:200px;height:auto" ') + '</div></body>');
  fs.mkdirSync(path.join(ROOT, 'mails/img'), { recursive: true });
  await (await z.$('#z')).screenshot({ path: path.join(ROOT, 'mails/img/zeichen.png'), omitBackground: true });
  const wm = fs.readFileSync(path.join(ROOT, '..', 'assets/zeichen/marke.svg'), 'utf8');
  await z.setViewportSize({ width: 900, height: 200 });
  await z.setContent('<body style="margin:0;background:transparent">' + wm + '<div id="w" style="width:880px;color:#faf4f4"><svg viewBox="0 0 364.78 40.36" style="display:block;width:880px;height:auto" fill="currentColor"><use href="#wm"/></svg></div></body>');
  await (await z.$('#w')).screenshot({ path: path.join(ROOT, 'mails/img/wortmarke.png'), omitBackground: true });
  await z.close();
  const ziel = path.join(ROOT, '_werkbank/ansichten/Mails'); fs.mkdirSync(ziel, { recursive: true });
  for (const [nr, ordner] of liste) {
    const p = await b.newPage({ viewport: { width: 640, height: 900 }, deviceScaleFactor: 2 });
    await p.goto(B + 'mails/' + ordner + '/index.html', { waitUntil: 'load' }); await p.waitForTimeout(1200);
    await p.screenshot({ path: path.join(ziel, nr + '.jpg'), quality: 88, clip: { x: 0, y: 0, width: 640, height: 940 }, fullPage: true });
    console.log('Mail', nr, ordner); await p.close();
  }
  await b.close();
})();
