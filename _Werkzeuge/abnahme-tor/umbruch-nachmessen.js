#!/usr/bin/env node
// Abnahme-Tor · K7 nachmessen: Titel (h1–h4) nach dem Durchscrollen und Ende aller Auftritte, Zeilen über die Lage jedes Wortes.
// Aufruf: node umbruch-nachmessen.js <breite>x<höhe> <url> …
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const [G, ...urls] = process.argv.slice(2); const [W, H] = G.split('x').map(Number);
(async () => { const b = await pw.webkit.launch();
  for (const url of urls) { const ctx = await b.newContext({ viewport: { width: W, height: H }, isMobile: W < 700, hasTouch: W < 700 }); const p = await ctx.newPage();
    await p.goto(url, { waitUntil: 'load', timeout: 45000 }).catch(() => { }); await p.waitForTimeout(1200);
    const hoch = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < hoch; y += H / 2) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(250); }
    await p.waitForTimeout(1500);
    // je Titel in die Mitte scrollen und den Auftritt abwarten: ausserhalb des Bildes liegen die Zeilen der Auftritte übereinander
    const n = await p.evaluate(() => document.querySelectorAll('h1,h2,h3,h4').length); const r = [];
    for (let i = 0; i < n; i++) { const ok = await p.evaluate(i => { const h = document.querySelectorAll('h1,h2,h3,h4')[i]; const rr = h.getBoundingClientRect(); if (rr.width < 2) return false; h.scrollIntoView({ block: 'center' }); return true; }, i); if (!ok) continue; await p.waitForTimeout(900);
      r.push(...await p.evaluate(i => { const aus = [];
      for (const h of [document.querySelectorAll('h1,h2,h3,h4')[i]]) { const rr = h.getBoundingClientRect(); if (rr.width < 2 || getComputedStyle(h).visibility === 'hidden') continue;
        const woerter = []; const tw = document.createTreeWalker(h, NodeFilter.SHOW_TEXT);
        for (let n; (n = tw.nextNode());) { const t = n.textContent; const re = /\S+/g; let m; while ((m = re.exec(t))) { const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length); const q = rg.getClientRects()[0]; if (q && q.width) woerter.push({ w: m[0], y: Math.round(q.top + q.height / 2) }); } }
        if (woerter.length < 2) continue; const zeilen = []; for (const x of woerter) { const z = zeilen.find(z => Math.abs(z.y - x.y) < 8); z ? z.w.push(x.w) : zeilen.push({ y: x.y, w: [x.w] }); }
        zeilen.sort((a, b) => a.y - b.y); const letzte = zeilen[zeilen.length - 1];
        const nurNr = z => z.w.length === 1 && /^\d{1,2}$/.test(z.w[0]); const zl = zeilen.filter(z => !nurNr(z)); const lz = zl[zl.length - 1];
        if (zl.length > 1 && lz.w.length === 1) aus.push(zl.map(z => z.w.join(' ')).join(' / ')); }
      return aus; }, i)); }
    console.log(W, url.replace(/^https?:\/\/[^/]+/, ''), r.length ? JSON.stringify(r) : 'ok'); await ctx.close(); }
  await b.close(); })();
