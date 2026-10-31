// Postkarten drucken und zeigen (Prüfchat Gestaltung 29.10.2026): node _werkbank/postkarten_druck.js "<website/_werkbank>"
//   postkarten/pdf/<kurz>-postkarten-druck.pdf (mit Beschnitt), -sammelbogen-a3.pdf; _werkbank/roh/postkarten/pkNN-v|h.png, bogen.png, faecher.png, staender.png
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), HIER = path.join(ROOT, '_werkbank');
const P = JSON.parse(fs.readFileSync(path.join(HIER, 'plan.json'), 'utf8'));
const plan = JSON.parse(fs.readFileSync(path.join(HIER, 'postkarten_plan.json'), 'utf8'));
const ROH = path.join(HIER, 'roh', 'postkarten'), EIN = path.join(HIER, 'roh', 'einzel-postkarten');
for (const d of [ROH, EIN, path.join(ROOT, 'postkarten/pdf')]) fs.mkdirSync(d, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const lade = async (p, id) => { await p.goto(P.base + '_werkbank/satz/' + id + '.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600); };
  const drucke = async (p, id, ziel) => {
    await p.evaluate(() => document.documentElement.className = 'einzeln'); await p.emulateMedia({ media: 'print' });
    // nur die obersten Blätter sind Seiten; Karten, die im Sammelbogen stecken, bleiben immer sichtbar
    await p.evaluate(() => { window.__bl = [...document.querySelectorAll('.blatt')].filter(x => !x.parentElement.closest('.blatt')); document.querySelectorAll('.blatt .blatt').forEach(x => x.classList.add('dran')); });
    const n = await p.evaluate(() => window.__bl.length), teile = [];
    for (let i = 0; i < n; i++) {
      const m = await p.evaluate(i => { window.__bl.forEach((x, k) => x.classList.toggle('dran', k === i)); const x = window.__bl[i]; return [x.dataset.b, x.dataset.h]; }, i);
      const t = path.join(EIN, id + '-' + i + '.pdf'); await p.pdf({ path: t, width: m[0] + 'mm', height: m[1] + 'mm', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' }); teile.push(t);
    }
    execFileSync('pdfunite', [...teile, ziel]); await p.emulateMedia({ media: 'screen' });
  };
  const p = await b.newPage({ viewport: { width: 1300, height: 1300 }, deviceScaleFactor: 3 });
  await lade(p, 'postkarten');
  await p.evaluate(() => document.documentElement.className = 'vorschau'); await p.waitForTimeout(200);
  const bl = await p.$$('.blatt');
  for (let n = 0; n < plan.karten.length; n++) { await bl[2 * n].screenshot({ path: path.join(ROH, plan.karten[n].id + '-v.png') }); await bl[2 * n + 1].screenshot({ path: path.join(ROH, plan.karten[n].id + '-h.png') }); }
  await lade(p, 'postkarten-druck'); await drucke(p, 'postkarten-druck', path.join(ROOT, 'postkarten/pdf', P.kurz + '-postkarten-druck.pdf'));
  await lade(p, 'postkarten-bogen'); await drucke(p, 'postkarten-bogen', path.join(ROOT, 'postkarten/pdf', P.kurz + '-postkarten-sammelbogen-a3.pdf'));
  await p.evaluate(() => document.documentElement.className = ''); await p.setViewportSize({ width: 1700, height: 1300 });
  const p2 = await b.newPage({ viewport: { width: 1700, height: 1250 }, deviceScaleFactor: 2 });
  await p2.goto(P.base + '_werkbank/satz/postkarten-bogen.html'); await p2.evaluate(() => document.fonts.ready); await p2.waitForTimeout(600);
  await (await p2.$('.blatt')).screenshot({ path: path.join(ROH, 'bogen.png') });
  // Fächer: alle Vorderseiten übereinander gefächert
  const K = plan.karten, n = K.length, D = {}; for (const k of K) D[k.id] = 'data:image/png;base64,' + fs.readFileSync(path.join(ROH, k.id + '-v.png')).toString('base64');
  const BAR = 'data:image/webp;base64,' + fs.readFileSync(path.join(HIER, 'satz', 'bild', 'barnacht.webp')).toString('base64');
  // Mondtänzerin (letztes Plakat) in der Mitte oben, die übrigen nach aussen
  const mitte = K.length - 3, folge = K.map((k, i) => i).filter(i => i !== mitte), pos = []; folge.forEach((i, j) => pos.push([i, (j % 2 ? 1 : -1) * (Math.floor(j / 2) + 1)])); pos.push([mitte, 0]);
  const stufen = Math.ceil(folge.length / 2), faecher = pos.sort((x, y) => Math.abs(y[1]) - Math.abs(x[1])).map(([i, st]) => `<img src="${D[K[i].id]}" style="position:absolute;left:50%;top:110px;width:270px;margin-left:-135px;transform-origin:50% 230%;transform:rotate(${st * 36 / stufen}deg);box-shadow:0 18px 40px -16px rgba(0,0,0,.55);border-radius:3px">`).join('');
  await p2.setViewportSize({ width: 1400, height: 900 });
  await p2.setContent(`<body style="margin:0;background:transparent"><div id="f" style="position:relative;width:1400px;height:900px">${faecher}</div></body>`); await p2.waitForTimeout(1500);
  await (await p2.$('#f')).screenshot({ path: path.join(ROH, 'faecher.png'), omitBackground: true });
  // Kartenständer an der Bar: Holzständer mit drei Fächern, davor die Theke bei Nacht
  const reihe = (ks, y) => ks.map((k, i) => `<img src="${D[k.id]}" style="position:absolute;left:${70 + i * 175}px;top:${y}px;width:150px;transform:rotate(${[-2, 1.5, -1, 2, -1.5][i % 5]}deg);box-shadow:0 10px 18px -8px rgba(0,0,0,.7);border-radius:2px">`).join('');
  const staender = `<div id="s" style="position:relative;width:1400px;height:900px;overflow:hidden;background:#16151a">
    <img src="${BAR}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:blur(6px) brightness(.55)">
    <div style="position:absolute;left:330px;top:70px;width:740px;height:780px;background:linear-gradient(#3a2a20,#2a1d16);border-radius:6px;box-shadow:0 40px 80px -20px rgba(0,0,0,.8)">
      ${reihe(K.slice(0, 4), 30)}${reihe(K.slice(4, 8), 275)}${reihe(K.slice(8, 12), 520)}
      ${[230, 475, 720].map(y => `<i style="position:absolute;left:0;right:0;top:${y}px;height:34px;background:linear-gradient(#4d3828,#2e2018);box-shadow:0 6px 10px rgba(0,0,0,.5)"></i>`).join('')}
    </div>
    <div style="position:absolute;left:0;right:0;bottom:0;height:70px;background:linear-gradient(#2b1f19,#140f0c)"></div></div>`;
  await p2.setContent(`<body style="margin:0">${staender}</body>`); await p2.waitForTimeout(2000);
  await (await p2.$('#s')).screenshot({ path: path.join(ROH, 'staender.png') });
  console.log('postkarten', plan.karten.length); await b.close();
})();
