// Druckt die gesetzten Unterlagen: node satz_druck.js "<Projektordner>" [ziel …]  → unterlagen/pdf/<ziel>.pdf
// Jede Seite wird so gross gesetzt, wie sie trägt (höchstens 118 %), und verkleinert, bis nichts mehr überläuft.
const path = require('path'), fs = require('fs');
// preferCSSPageSize: Seitengrösse aus @page, sonst rundet Chrome die Seite breiter als das Blatt und rechts bleibt ein weisser Streifen (GBR 11.10.2026)
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), HIER = path.join(ROOT, '_werkbank');
const P = JSON.parse(fs.readFileSync(path.join(HIER, 'plan.json'), 'utf8'));
const plan = JSON.parse(fs.readFileSync(path.join(HIER, 'unterlagen.json'), 'utf8'));
const nur = process.argv.slice(3).filter(a => !a.startsWith('--')), bild = process.argv.includes('--bild');
(async () => {
  fs.mkdirSync(path.join(ROOT, 'unterlagen/pdf'), { recursive: true });
  const b = await chromium.launch();
  for (const d of plan) {
    if (nur.length && !nur.includes(d.ziel)) continue;
    const p = await b.newPage({ viewport: { width: 1300, height: 1400 }, deviceScaleFactor: 1.5 });
    await p.goto(P.base + '_werkbank/satz/u-' + d.ziel + '.html', { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
    const pass = await p.evaluate(() => {
      const aus = [];
      document.querySelectorAll('.blatt').forEach(bl => {
        const inh = bl.querySelector('.inhalt'); if (!inh || bl.dataset.fest) { aus.push('-'); return; }
        const zuviel = () => {
          let r = inh.scrollHeight / inh.clientHeight;
          // Unterkante des Inhalts gegen die Innenkante des Blatts: scrollHeight zählt den unteren Innenabstand eines Flex-Kastens nicht mit,
          // Inhalt konnte deshalb unbemerkt bis an den Blattrand laufen
          const innen = (k) => { const q = k.getBoundingClientRect(), c = getComputedStyle(k); const o = q.top + parseFloat(c.paddingTop), u = q.bottom - parseFloat(c.paddingBottom);
            const tief = Math.max(o, ...[...k.children].filter(x => getComputedStyle(x).position !== 'absolute').map(x => x.getBoundingClientRect().bottom)); return u > o ? (tief - o) / (u - o) : 1; };
          r = Math.max(r, innen(inh)); bl.querySelectorAll('.sp').forEach(s => { if (s.children.length > 1) r = Math.max(r, innen(s)); });
          bl.querySelectorAll('.sp').forEach(s => { const k = [...s.children].reduce((a, c) => a + c.getBoundingClientRect().height + parseFloat(getComputedStyle(c).marginTop) + parseFloat(getComputedStyle(c).marginBottom), 0); r = Math.max(r, k / s.getBoundingClientRect().height, s.scrollWidth / s.clientWidth); });
          return r;
        };
        let s = +(bl.dataset.max || 1.18); bl.style.setProperty('--s', s);
        let zu = null;   // kleinstes Mass, das nachweislich überläuft
        for (let i = 0; i < 9; i++) { const r = zuviel(); if (r <= 1.001) break; zu = s; s = s / r * 0.985; bl.style.setProperty('--s', s); }
        // Die Höhe schrumpft nicht gleichmässig mit dem Mass, der Schritt oben landet deshalb oft mehrere Prozent zu tief.
        // Zwischen «passt» und «läuft über» halbieren, bis das grösste Mass gefunden ist, das noch passt.
        if (zu !== null && zuviel() <= 1.001) {
          let gut = s;
          for (let i = 0; i < 7; i++) { const m = (gut + zu) / 2; bl.style.setProperty('--s', m); if (zuviel() <= 1.001) gut = m; else zu = m; }
          s = gut; bl.style.setProperty('--s', s);
        }
        aus.push(Math.round(s * 100) + (zuviel() > 1.005 ? '!' : ''));
      });
      return aus.join(' ');
    });
    console.log(d.ziel, 'Schriftmass je Seite in %:', pass);
    if (bild) { fs.mkdirSync(path.join(HIER, 'roh', 'blick'), { recursive: true }); const bl = await p.$$('.blatt'); for (let i = 0; i < bl.length; i++) await bl[i].screenshot({ path: path.join(HIER, 'roh', 'blick', `${d.ziel}-${String(i + 1).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 82 }); }
    await p.emulateMedia({ media: 'print' });
    await p.pdf({ path: path.join(ROOT, 'unterlagen/pdf', d.ziel + '.pdf'), width: d.b + 'mm', height: d.h + 'mm', preferCSSPageSize: true, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    await p.close();
  }
  await b.close();
})();
