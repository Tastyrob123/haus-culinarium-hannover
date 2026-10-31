#!/usr/bin/env node
/* Bild einer Seite, unsichtbar: node bild.js <url> <ausgabe.png> [breite] [hoehe] [chromium|webkit] [voll]
   Fehler der Konsole und Netzantworten ab 400 werden ausgegeben; mailto/tel und Anfragen ausser GET/HEAD werden abgewiesen. */
const pw = require('playwright');
(async () => {
  const [url, aus, b = '1440', h = '900', kern = 'chromium', voll] = process.argv.slice(2);
  const br = await pw[kern].launch();
  try {
    const ctx = await br.newContext({ viewport: { width: +b, height: +h }, deviceScaleFactor: 1 });
    const p = await ctx.newPage(); const fehler = [];
    await p.route('**/*', r => { const q = r.request(); if (!['GET', 'HEAD'].includes(q.method()) || /^(mailto|tel):/.test(q.url())) return r.abort(); r.continue(); });
    p.on('console', m => { if (m.type() === 'error') fehler.push('KONSOLE ' + m.text()); });
    p.on('pageerror', e => fehler.push('SKRIPT ' + e.message));
    p.on('response', r => { if (r.status() >= 400) fehler.push('NETZ ' + r.status() + ' ' + r.url()); });
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1600);
    const sw = await p.evaluate(() => { let m = 0; document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && getComputedStyle(e).position !== 'fixed') m = Math.max(m, r.right); }); return { doc: document.documentElement.scrollWidth, weit: Math.round(m) }; });
    await p.screenshot({ path: aus, fullPage: !!voll });
    console.log(JSON.stringify({ url, kern, b: +b, ...sw, fehler }));
  } finally { await br.close(); }
})();
