// node werkbank-wege.js <wege.json>  → sammelt alle Wege der Werkbank (Server auf Port 9088), Seiten bei 1440 und 390
const pw = require('playwright');
const fs = require('fs');
const START = ['werkbank/index.html', 'werkbank/ki.html', 'werkbank/karte.html', 'werkbank/geprueft/index.html', 'befund/index.html',
  'unterlagen/index.html', 'drucksachen/index.html', 'untersetzer/index.html', 'sticker/index.html', 'feed/index.html', 'mails/index.html',
  'material/index.html', 'werkbank/impressum.html', 'postkarten/index.html', 'beigaben/index.html'];
const O = 'http://127.0.0.1:9088/';
const T = (pr, ms) => Promise.race([pr, new Promise(r => setTimeout(() => r(null), ms))]);
const BEREICH = /^(werkbank|befund|unterlagen|drucksachen|untersetzer|sticker|feed|mails|material|postkarten|beigaben)\//;
(async () => {
  const b = await pw.chromium.launch();
  const wege = new Set(), besucht = new Set();
  const schlange = START.map(s => ({ w: s, t: 0 }));
  const sichern = () => fs.writeFileSync(process.argv[2], JSON.stringify([...wege].sort(), null, 1));
  while (schlange.length) {
    const { w, t } = schlange.shift();
    if (besucht.has(w)) continue; besucht.add(w);
    process.stderr.write('→ ' + w + '\n');
    for (const br of [1440, 390]) {
      const ctx = await b.newContext({ viewport: { width: br, height: 900 }, acceptDownloads: false });
      const p = await ctx.newPage();
      p.on('response', r => { const u = r.url(); if (u.startsWith(O) && r.status() === 200) wege.add(decodeURIComponent(u.slice(O.length).split(/[?#]/)[0])); });
      p.on('dialog', d => d.dismiss().catch(() => {}));
      const r = await T(p.goto(O + w, { waitUntil: 'load', timeout: 30000 }).catch(() => null), 35000);
      if (r && r.status() === 200) {
        await T(p.waitForLoadState('networkidle').catch(() => {}), 8000);
        await T(p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight && y < 40000; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); } }).catch(() => {}), 15000);
        await p.waitForTimeout(600);
        const links = (await T(p.evaluate(() => {
          const l = [...document.querySelectorAll('a[href],iframe[src],img[src],video[src],object[data],embed[src]')].map(e => e.href || e.src || e.data || '');
          document.querySelectorAll('[srcset]').forEach(e => e.srcset.split(',').forEach(s => { try { l.push(new URL(s.trim().split(' ')[0], location.href).href); } catch (x) {} }));
          return l;
        }).catch(() => []), 10000)) || [];
        for (const l of links) {
          if (typeof l !== 'string' || !l.startsWith(O)) continue;
          const ww = decodeURIComponent(l.slice(O.length).split(/[?#]/)[0]);
          if (/\.(pdf|jpe?g|png|webp|svg|gif|mp4|webm|avif)$/i.test(ww)) wege.add(ww);
          else if (/(\.html?|\/)$/i.test(ww) && BEREICH.test(ww)) { const h = ww.endsWith('/') ? ww + 'index.html' : ww; wege.add(h); if (t < 3) schlange.push({ w: h, t: t + 1 }); }
        }
      }
      await T(ctx.close(), 5000);
      if (!r || r.status() !== 200) break;
    }
    process.stderr.write(`${besucht.size} ${schlange.length} ${wege.size} ${w}\n`);
    if (besucht.size % 10 === 0) sichern();
  }
  sichern();
  process.stderr.write('FERTIG\n');
  await T(b.close(), 5000);
  process.exit(0);
})();
