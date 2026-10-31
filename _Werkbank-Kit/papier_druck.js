// Druckt die gesetzten Drucksachen und Etiketten: node papier_druck.js "<Projektordner>" [id …]
//   drucksachen/pdf/<kurz>-<id>.pdf   jede Seite in ihrem eigenen Format (einzeln gedruckt, mit pdfunite zusammengefügt)
//   _werkbank/roh/papier/<name>.png   Vorschaubilder mit durchsichtigem Grund (papier_seiten.py macht daraus WebP)
//   <etiketten>/pdf/…                 Druckbogen A3 und jedes Etikett einzeln
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), HIER = path.join(ROOT, '_werkbank');
const P = JSON.parse(fs.readFileSync(path.join(HIER, 'plan.json'), 'utf8'));
const plan = JSON.parse(fs.readFileSync(path.join(HIER, 'papier_plan.json'), 'utf8'));
const nur = process.argv.slice(3);
const ROH = path.join(HIER, 'roh', 'papier'), ET = P.etiketten_ordner;
(async () => {
  for (const d of [ROH, path.join(ROOT, 'drucksachen/pdf'), path.join(ROOT, ET, 'pdf'), path.join(HIER, 'roh', 'einzel')]) fs.mkdirSync(d, { recursive: true });
  const b = await chromium.launch();
  const lade = async (p, id) => { await p.goto(P.base + '_werkbank/satz/' + id + '.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500); };
  const drucke = async (p, id, zielpdf) => {
    await p.evaluate(() => document.documentElement.className = 'einzeln');
    await p.emulateMedia({ media: 'print' });
    const n = await p.evaluate(() => document.querySelectorAll('.blatt').length), teile = [];
    for (let i = 0; i < n; i++) {
      const m = await p.evaluate(i => { document.querySelectorAll('.blatt').forEach((x, k) => x.classList.toggle('dran', k === i)); const x = document.querySelectorAll('.blatt')[i]; return [x.dataset.b, x.dataset.h]; }, i);
      const t = path.join(HIER, 'roh', 'einzel', id + '-' + i + '.pdf');
      await p.pdf({ path: t, width: m[0] + 'mm', height: m[1] + 'mm', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' });
      teile.push(t);
    }
    if (teile.length === 1) fs.copyFileSync(teile[0], zielpdf); else execFileSync('pdfunite', [...teile, zielpdf]);
    await p.emulateMedia({ media: 'screen' });
    return n;
  };
  const bilder = async (p, namen) => {
    await p.evaluate(() => document.documentElement.className = 'vorschau');
    await p.waitForTimeout(200);
    const bl = await p.$$('.blatt');
    for (const [name, nr] of namen) await bl[nr - 1].screenshot({ path: path.join(ROH, name + '.png'), omitBackground: true });
  };
  for (const d of plan.druck) {
    if (nur.length && !nur.includes(d.id)) continue;
    const p = await b.newPage({ viewport: { width: 1300, height: 1300 }, deviceScaleFactor: 3 });
    await lade(p, d.id);
    await bilder(p, d.vorschau);
    const n = await drucke(p, d.id, path.join(ROOT, 'drucksachen/pdf', P.kurz + '-' + d.id + '.pdf'));
    console.log(d.id, n, 'Seiten');
    await p.close();
  }
  if (!nur.length || nur.includes('etiketten')) {
    const p = await b.newPage({ viewport: { width: 1300, height: 1300 }, deviceScaleFactor: 3 });
    await lade(p, 'etiketten');
    await bilder(p, plan.etiketten.map((e, i) => [e.id, i + 1]));
    await drucke(p, 'etiketten', path.join(ROOT, ET, 'pdf', P.kurz + '-' + ET + '-einzeln.pdf'));
    await lade(p, 'etiketten-bogen');
    await drucke(p, 'etiketten-bogen', path.join(ROOT, ET, 'pdf', P.kurz + '-' + ET + '-druckbogen-a3.pdf'));
    await p.evaluate(() => document.documentElement.className = '');
    await (await p.$('.blatt')).screenshot({ path: path.join(ROH, 'etiketten-bogen.png') });
    console.log('etiketten', plan.etiketten.length);
    await p.close();
  }
  await b.close();
})();
