// Vorschaubilder für die Link-Galerie am Ende der Werkbank: node ziele.js "<Projektordner>"  →  _werkbank/ansichten/Ziele/<name>.jpg
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), HIER = path.join(ROOT, '_werkbank');
const plan = JSON.parse(fs.readFileSync(path.join(HIER, 'plan.json'), 'utf8'));
const Z = path.join(HIER, 'ansichten', 'Ziele');
(async () => {
  fs.mkdirSync(Z, { recursive: true });
  const br = await chromium.launch(), p = await br.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
  for (const [name, pfad] of [['unterlagen', 'unterlagen/index.html'], ['drucksachen', 'drucksachen/index.html'], ['etiketten', plan.etiketten_ordner + '/index.html'], ['material', 'material/index.html']]) {
    if (!fs.existsSync(path.join(ROOT, pfad))) continue;
    await p.goto(plan.base + pfad, { waitUntil: 'load' }); await p.waitForTimeout(3200);
    const r = await p.evaluate(() => { const e = document.querySelector('.auslage').getBoundingClientRect(); return [e.left, e.top, e.width, e.height]; });
    await p.screenshot({ path: path.join(Z, name + '.jpg'), quality: 90, clip: { x: Math.max(0, r[0] - 20), y: Math.max(0, r[1] - 20), width: r[2] + 40, height: (r[2] + 40) * 0.75 } });
    console.log(name);
  }
  await br.close();
})();
