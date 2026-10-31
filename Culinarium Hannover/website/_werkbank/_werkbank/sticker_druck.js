// Sticker und Beigaben drucken (Prüfchat Gestaltung 29.10.2026, nach papier_druck.js des Kits):
//   node _werkbank/sticker_druck.js "<website/_werkbank>" [sticker|beigaben]
//   sticker/pdf/<kurz>-sticker-einzeln.pdf, -druckbogen-a3.pdf, _werkbank/roh/sticker/<id>.png
//   beigaben/pdf/<kurz>-<id>.pdf, _werkbank/roh/beigaben/<name>.png
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), HIER = path.join(ROOT, '_werkbank');
const P = JSON.parse(fs.readFileSync(path.join(HIER, 'plan.json'), 'utf8'));
const nur = process.argv[3] || 'beide';
(async () => {
  const b = await chromium.launch();
  const lade = async (p, id) => { await p.goto(P.base + '_werkbank/satz/' + id + '.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500); };
  const drucke = async (p, id, zielpdf, einzel) => {
    fs.mkdirSync(einzel, { recursive: true });
    await p.evaluate(() => document.documentElement.className = 'einzeln');
    await p.emulateMedia({ media: 'print' });
    const n = await p.evaluate(() => document.querySelectorAll('.blatt').length), teile = [];
    for (let i = 0; i < n; i++) {
      const m = await p.evaluate(i => { document.querySelectorAll('.blatt').forEach((x, k) => x.classList.toggle('dran', k === i)); const x = document.querySelectorAll('.blatt')[i]; return [x.dataset.b, x.dataset.h]; }, i);
      const t = path.join(einzel, id + '-' + i + '.pdf');
      await p.pdf({ path: t, width: m[0] + 'mm', height: m[1] + 'mm', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' });
      teile.push(t);
    }
    if (teile.length === 1) fs.copyFileSync(teile[0], zielpdf); else execFileSync('pdfunite', [...teile, zielpdf]);
    await p.emulateMedia({ media: 'screen' });
  };
  const bilder = async (p, ordner, namen) => {
    fs.mkdirSync(ordner, { recursive: true });
    await p.evaluate(() => document.documentElement.className = 'vorschau'); await p.waitForTimeout(200);
    const bl = await p.$$('.blatt');
    for (const [name, nr] of namen) await bl[nr - 1].screenshot({ path: path.join(ordner, name + '.png'), omitBackground: true });
  };
  const einzel = path.join(HIER, 'roh', 'einzel-sticker');
  if (nur !== 'beigaben') {
    const plan = JSON.parse(fs.readFileSync(path.join(HIER, 'sticker_plan.json'), 'utf8'));
    fs.mkdirSync(path.join(ROOT, 'sticker/pdf'), { recursive: true });
    const p = await b.newPage({ viewport: { width: 1300, height: 1300 }, deviceScaleFactor: 3 });
    await lade(p, 'sticker');
    await bilder(p, path.join(HIER, 'roh', 'sticker'), plan.etiketten.map((e, i) => [e.id, i + 1]));
    await drucke(p, 'sticker', path.join(ROOT, 'sticker/pdf', P.kurz + '-sticker-einzeln.pdf'), einzel);
    await lade(p, 'sticker-bogen');
    await drucke(p, 'sticker-bogen', path.join(ROOT, 'sticker/pdf', P.kurz + '-sticker-druckbogen-a3.pdf'), einzel);
    await p.evaluate(() => document.documentElement.className = '');
    await (await p.$('.blatt')).screenshot({ path: path.join(HIER, 'roh', 'sticker', 'etiketten-bogen.png') });
    console.log('sticker', plan.etiketten.length); await p.close();
  }
  if (nur !== 'sticker' && fs.existsSync(path.join(HIER, 'beigaben_plan.json'))) {
    const plan = JSON.parse(fs.readFileSync(path.join(HIER, 'beigaben_plan.json'), 'utf8'));
    fs.mkdirSync(path.join(ROOT, 'beigaben/pdf'), { recursive: true });
    for (const d of plan.druck) {
      const p = await b.newPage({ viewport: { width: 1300, height: 1300 }, deviceScaleFactor: 3 });
      await lade(p, 'beigabe-' + d.id);
      await bilder(p, path.join(HIER, 'roh', 'beigaben'), d.vorschau);
      await drucke(p, 'beigabe-' + d.id, path.join(ROOT, 'beigaben/pdf', P.kurz + '-' + d.id + '.pdf'), einzel);
      console.log('beigabe', d.id); await p.close();
    }
  }
  await b.close();
})();
