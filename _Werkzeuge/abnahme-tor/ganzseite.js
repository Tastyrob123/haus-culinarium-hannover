#!/usr/bin/env node
// Abnahme-Tor · Augenprüfung: ganze Seite nach langsamem Durchscrollen (alle Auftritte ausgelöst), in Streifen geschnitten, WebKit.
// Aufruf: node ganzseite.js <ausgabe-ordner> <breite>x<höhe> <name>=<url> …
const path = require('path'), fs = require('fs');
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const [AUS, G, ...ziele] = process.argv.slice(2); const [W, H] = G.split('x').map(Number); fs.mkdirSync(AUS, { recursive: true });
(async () => { const b = await pw.webkit.launch();
  for (const z of ziele) { const i = z.indexOf('='), name = z.slice(0, i), url = z.slice(i + 1);
    const ctx = await b.newContext({ viewport: { width: W, height: H }, locale: 'de-DE', isMobile: W < 700, hasTouch: W < 700 });
    await ctx.route('**/*', q => ['GET', 'HEAD'].includes(q.request().method()) ? q.continue() : q.fulfill({ status: 200, body: '{}' }));
    const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'load', timeout: 45000 }).catch(() => { }); await p.waitForTimeout(1500);
    const hoch = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < hoch; y += H / 3) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(120); }
    // Bild für Bild wie ein Mensch beim Scrollen (eine Aufnahme der ganzen Seite zeigt in WebKit die Auftritte nicht)
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(900); let n = 0;
    for (let y = 0; ; y += H) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(1100);
      await p.screenshot({ path: path.join(AUS, `${name}-${W}-${String(n++).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 70 });
      if (y + H >= hoch) break; }
    console.log(name, W, hoch); await ctx.close(); }
  await b.close(); })();
