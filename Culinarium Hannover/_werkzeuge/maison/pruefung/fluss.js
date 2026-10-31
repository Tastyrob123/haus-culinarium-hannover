#!/usr/bin/env node
/* Flüssigkeit von La Maison · Culinarium Hannover (Regel 55): fertige Seite, Chromium, CPU 4× und 6× gedrosselt, ganze Seite in Rad-Schritten, am Rechner zusätzlich
   zweimal mit dem Zeiger über alle sechs Gefache (Vorschauwechsel). Misst Bildabstände (rAF), längstes Bild, Bilder über 33 ms, Layoutverschiebung, Gewicht. */
const path = require('path'), os = require('os'), fs = require('fs');
module.paths.push(path.join(os.homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
const BASIS = process.argv[2] || 'http://127.0.0.1:9081/_werkzeuge/maison/';
(async () => {
  const b = await pw.chromium.launch({ headless: true });
  const aus = [];
  for (const [B, H] of [[1440, 900], [390, 844]]) for (const dr of [4, 6]) {
    const ctx = await b.newContext({ viewport: { width: B, height: H }, deviceScaleFactor: B < 1000 ? 3 : 2 });
    const page = await ctx.newPage(); const cdp = await ctx.newCDPSession(page);
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: dr });
    let gewicht = 0, anfragen = 0;
    page.on('response', async r => { anfragen++; try { const x = await r.body(); gewicht += x.length; } catch (e) {} });
    await page.addInitScript(() => { window.__cls = 0; new PerformanceObserver(l => l.getEntries().forEach(e => { if (!e.hadRecentInput) window.__cls += e.value; })).observe({ type: 'layout-shift', buffered: true });
      window.__t = []; (function f(t) { window.__t.push(t); requestAnimationFrame(f); })(performance.now()); });
    await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(2500);
    await page.evaluate(() => { window.__t = []; });
    let zeiger = null;
    if (B >= 1000) {
      await page.evaluate(() => document.querySelector('.hz-tafel').scrollIntoView({ block: 'center' })); await page.waitForTimeout(800);
      await page.evaluate(() => { window.__t = []; });
      const z = await page.$$('.hz-z a');
      for (let r = 0; r < 2; r++) for (const x of z) { const bb = await x.boundingBox(); await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2, { steps: 6 }); await page.waitForTimeout(260); }
      zeiger = await page.evaluate(() => { const d = []; for (let i = 1; i < window.__t.length; i++) d.push(window.__t[i] - window.__t[i - 1]); return Math.max(...d); });
      await page.evaluate(() => { scrollTo(0, 0); window.__t = []; }); await page.waitForTimeout(400);
    }
    const hoch = await page.evaluate(() => document.documentElement.scrollHeight);
    await page.mouse.move(B / 2, H / 2);
    for (let y = 0; y < hoch; y += 240) { await page.mouse.wheel(0, 240); await page.waitForTimeout(50); }
    await page.waitForTimeout(600);
    const m = await page.evaluate(() => { const d = []; for (let i = 1; i < window.__t.length; i++) d.push(window.__t[i] - window.__t[i - 1]); d.sort((a, b) => a - b);
      return { bilder: d.length, p50: d[Math.floor(d.length * .5)], p95: d[Math.floor(d.length * .95)], laengstes: d[d.length - 1], ueber33: d.filter(x => x > 33.4).length, cls: window.__cls }; });
    aus.push({ groesse: `${B}x${H}`, drossel: dr, ...m, zeiger_laengstes: zeiger, gewicht_mb: +(gewicht / 1e6).toFixed(2), anfragen });
    await ctx.close();
  }
  await b.close();
  fs.writeFileSync(path.join(__dirname, 'fluss-ergebnis.json'), JSON.stringify({ zeit: new Date().toISOString(), last: os.loadavg()[0].toFixed(1), aus }, null, 1));
  console.log('Last', os.loadavg()[0].toFixed(1)); aus.forEach(x => console.log(JSON.stringify(x, (k, v) => typeof v === 'number' ? +v.toFixed(4) : v)));
})().catch(e => { console.error(String(e)); process.exit(1); });
