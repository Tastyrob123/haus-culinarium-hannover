// Fotografiert die Seiten für die Werkbank: node ansicht.js "<Projektordner>" [seite …]
//   _werkbank/ansichten/Rechner/<Name>.jpg, <Name> 2.jpg …   saubere Bildschirme (1440 × 900) an den Anfängen der Abschnitte
//   _werkbank/ansichten/Handy/<Name>.jpg, <Name> 2.jpg …     dieselben Stellen am Handy (390 × 844)
//   _werkbank/ansichten/liste.json                           was es gibt, für bau.py
// Jede Seite wird erst ganz durchgefahren, damit alles eingeblendet und geladen ist. Fotografiert wird, wenn die Bewegung steht.
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), HIER = path.join(ROOT, '_werkbank');
const plan = JSON.parse(fs.readFileSync(path.join(HIER, 'plan.json'), 'utf8'));
const BASE = plan.base, SEITEN = plan.seiten, WAHL = plan.wahl;
const nur = process.argv.slice(3);
const ruhe = async (p, ms) => { await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(ms); };
async function durchfahren(p, schritt) {
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h; y += schritt) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(240); }
  await p.evaluate(() => scrollTo(0, 0));
  await p.waitForTimeout(900);
}
(async () => {
  for (const d of ['ansichten/Rechner', 'ansichten/Handy']) fs.mkdirSync(path.join(HIER, d), { recursive: true });
  const listeDatei = path.join(HIER, 'ansichten', 'liste.json');
  const liste = fs.existsSync(listeDatei) ? JSON.parse(fs.readFileSync(listeDatei, 'utf8')) : {};
  const b = await chromium.launch({ headless: true });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  for (const [seite, name, max] of SEITEN) {
    if (nur.length && !nur.includes(seite)) continue;
    await p.goto(BASE + seite, { waitUntil: 'load' });
    await ruhe(p, seite === 'index.html' ? plan.start_ms + 1000 : 3200);
    for (const alt of fs.readdirSync(path.join(HIER, 'ansichten/Rechner'))) if (alt === name + '.jpg' || new RegExp('^' + name + ' \\d+\\.jpg$').test(alt)) fs.unlinkSync(path.join(HIER, 'ansichten/Rechner', alt));
    await p.screenshot({ path: path.join(HIER, 'ansichten/Rechner', name + '.jpg'), quality: 90 });
    if (seite === 'index.html') {   // Startseite für den Auftakt der Werkbank doppelt so scharf (Robert 11.10.2026: «das Hintergrundbild viel schärfer»)
      const hd = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 }); const q = await hd.newPage();
      await q.goto(BASE + seite, { waitUntil: 'load' }); await ruhe(q, plan.start_ms + 1000);
      await q.screenshot({ path: path.join(HIER, 'ansichten/Rechner', name + '.jpg'), quality: 92 }); await hd.close();
    }
    let n = 1; const st = [];
    if (max > 1) {
      await durchfahren(p, 450);
      // Anfänge der Abschnitte; lange Abschnitte bekommen Zwischenhalte, damit auch Seiten mit wenigen Abschnitten ganz gezeigt werden
      const orte = await p.evaluate(WAHL => {
        const vh = innerHeight, fuss = document.querySelector('footer'), ende = (fuss ? fuss.getBoundingClientRect().top + scrollY : document.documentElement.scrollHeight) - vh;
        const aus = [];
        [...document.querySelectorAll(WAHL)].forEach((e, i) => {
          const r = e.getBoundingClientRect(), oben = r.top + scrollY; if (r.height <= 260) return;
          const halte = Math.max(1, Math.round(r.height / (vh * 1.05)));
          for (let k = 0; k < halte; k++) { const f = k / halte, y = Math.round(oben + r.height * f - (k === 0 && e.classList.contains('bruch') ? 110 : (k ? 90 : 0))); if (y > vh * 0.6 && y <= ende + 10) aus.push([y, i, f]); }
        });
        return aus.sort((a, b) => a[0] - b[0]);
      }, WAHL);
      let paare = orte.filter((x, i, l) => i === 0 || x[0] - l[i - 1][0] > 520);
      while (paare.length > max - 1) paare.splice(Math.round(paare.length / 2), 1);
      // Feste Stellen aus dem Plan (plan.stellen[seite] = [[Abschnitt, Anteil] …]): Sprachfassungen halten an denselben Stellen wie die deutsche Fassung,
      // damit Ansicht k in jeder Sprache denselben Abschnitt zeigt und keine fehlt (Grand Beau-Rivage, ansicht_sprachen.py, 12.10.2026). Ohne den Schlüssel wie bisher.
      const fest = plan.stellen && plan.stellen[seite];
      if (fest) paare = await p.evaluate(([WAHL, fest]) => { const l = document.querySelectorAll(WAHL); return fest.map(([i, f]) => { const e = l[i]; if (!e || !e.getBoundingClientRect().height) return null; const r = e.getBoundingClientRect(); return [Math.round(r.top + scrollY + r.height * f - (f === 0 && e.classList.contains('bruch') ? 110 : (f ? 90 : 0))), i, f]; }).filter(Boolean); }, [WAHL, fest]);
      for (const [y, i, f] of paare) {
        await p.evaluate(v => scrollTo(0, v), Math.max(0, y - 1));
        await ruhe(p, 2600);
        n++; st.push([i, f]);
        await p.screenshot({ path: path.join(HIER, 'ansichten/Rechner', `${name} ${n}.jpg`), quality: 90 });
      }
    }
    liste[seite] = Object.assign(liste[seite] || {}, { name, rechner: n, stellen: st });
    console.log('Rechner', seite, n);
  }
  await ctx.close();
  const ctx2 = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const q = await ctx2.newPage();
  for (const [seite, name] of SEITEN) {
    if (nur.length && !nur.includes(seite)) continue;
    await q.goto(BASE + seite, { waitUntil: 'load' });
    await ruhe(q, seite === 'index.html' ? plan.start_ms + 1000 : 3200);
    for (const alt of fs.readdirSync(path.join(HIER, 'ansichten/Handy'))) if (alt === name + '.jpg' || new RegExp('^' + name + ' \\d+\\.jpg$').test(alt)) fs.unlinkSync(path.join(HIER, 'ansichten/Handy', alt));
    await q.screenshot({ path: path.join(HIER, 'ansichten/Handy', name + '.jpg'), quality: 90 });
    const st = (liste[seite] && liste[seite].stellen) || [];
    let hn = 1;
    if (st.length) {
      await durchfahren(q, 520);
      for (const [i, f] of st) {
        const y = await q.evaluate(([WAHL, i, f]) => { const e = document.querySelectorAll(WAHL)[i]; if (!e || !e.getBoundingClientRect().height) return null; const r = e.getBoundingClientRect(); return Math.round(r.top + scrollY + r.height * f - (f === 0 && e.classList.contains('bruch') ? 80 : (f ? 70 : 0))); }, [WAHL, i, f]);
        hn++;
        if (y === null) { fs.copyFileSync(path.join(HIER, 'ansichten/Handy', name + '.jpg'), path.join(HIER, 'ansichten/Handy', `${name} ${hn}.jpg`)); continue; }
        await q.evaluate(v => scrollTo(0, v), Math.max(0, y - 1));
        await ruhe(q, 2200);
        await q.screenshot({ path: path.join(HIER, 'ansichten/Handy', `${name} ${hn}.jpg`), quality: 90 });
      }
    }
    liste[seite].handy = hn;
    console.log('Handy', seite, hn);
  }
  fs.writeFileSync(listeDatei, JSON.stringify(liste, null, 1));
  // heutige Startseite des Hauses für den Vergleich (Hinweisfenster wird abgelehnt)
  if (plan.heute && !nur.length) {
    fs.mkdirSync(path.join(HIER, 'ansichten/Heute'), { recursive: true });
    const h = await b.newPage({ viewport: { width: 1440, height: 900 } });
    try {
      await h.goto(plan.heute, { waitUntil: 'load', timeout: 45000 });
      await h.waitForTimeout(3500);
      for (const t of ['ablehnen', 'nur notwendige', 'decline', 'reject', 'alle ablehnen']) { const ab = await h.$(`text=/^\\s*${t}\\s*$/i`); if (ab) { await ab.click().catch(() => {}); await h.waitForTimeout(1500); break; } }
      await h.screenshot({ path: path.join(HIER, 'ansichten/Heute', 'Startseite.jpg'), quality: 90 });
      console.log('Heute', h.url());
    } catch (e) { console.log('Heute fehlgeschlagen', String(e).slice(0, 200)); }
  }
  await b.close();
})();
