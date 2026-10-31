/* Le Livre · Culinarium Hannover · Flüssigkeit auf schwachem Gerät (Regel 55): Hauptfaden gedrosselt (4× / 6×), echte Rad-Ereignisse bis ganz unten,
   im Bildarchiv werden dabei alle Kacheln nachgeladen. Vorlage Carlton _werkbank/mess.js. Nur messen, wenn `uptime` unter 8 liegt.
   BASIS=http://127.0.0.1:9085/ node _werkzeuge/livre/pruefung/fluss.js            → ergebnisse/fluss.jsonl (je Ansicht, Drosselung, Breite eine Zeile) */
const path = require('path'), fs = require('fs'), os = require('os');
const { chromium } = require(path.join(process.env.HOME, 'Aussen-Pruefung/node_modules/playwright'));
const BASIS = process.env.BASIS || 'http://127.0.0.1:9085/', URL0 = BASIS + '_werkzeuge/livre/';
const AUS = path.join(__dirname, 'ergebnisse', 'fluss.jsonl');
(async () => {
  const last = os.loadavg()[0];
  if (last >= 8 && !process.env.TROTZDEM) { console.log(`Rechnerlast ${last.toFixed(1)}: nicht gemessen (Regel 55 / F26, erst unter 8)`); process.exit(3); }
  const b = await chromium.launch({ headless: true });
  for (const [W, H] of [[1440, 900], [390, 844]]) for (const CPU of (process.env.CPU || '4,6').split(',').map(Number)) for (const a of (process.env.ANSICHTEN || 'start,bilder,dateien,pruefung,buch').split(',')) {
    const mob = W < 600;
    const ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: mob ? 2 : 1, isMobile: mob, hasTouch: mob });
    await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-culinarium-livre', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const cdp = await ctx.newCDPSession(p);
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: CPU });
    const t0 = Date.now();
    await p.goto(a === 'buch' ? URL0 + 'buch.html' : URL0 + '#' + a, { waitUntil: 'load' });
    await p.waitForSelector(a === 'buch' ? 'section.blatt' : '#ansicht [data-r]', { timeout: 60000 });
    const lade = Date.now() - t0;
    await p.evaluate(() => { window.__f = []; let l = performance.now(); (function s(t) { window.__f.push(t - l); l = t; requestAnimationFrame(s); })(performance.now());
      window.__cls = 0; window.__wo = []; try { new PerformanceObserver(x => x.getEntries().forEach(e => { if (!e.hadRecentInput) { window.__cls += e.value; window.__wo.push(Math.round(e.startTime) + 'ms ' + e.value.toFixed(3) + ' ' + e.sources.map(s => s.node ? (s.node.id || s.node.className || s.node.tagName) : '?').join(',')); } })).observe({ type: 'layout-shift', buffered: true }); } catch (e) {} });
    await p.waitForTimeout(1500);
    await p.evaluate(() => { window.__f = []; });
    await p.mouse.move(W / 2, H / 2);
    for (let i = 0, h = 1e9, y = 0; i < 400 && y < h - H - 2; i++) { if (mob) await p.evaluate(() => scrollBy(0, 120)); else await p.mouse.wheel(0, 120); await p.waitForTimeout(34); [y, h] = await p.evaluate(() => [scrollY, document.documentElement.scrollHeight]); }
    await p.waitForTimeout(500);
    const r = await p.evaluate(() => { const f = window.__f.slice(2).filter(x => x > 0 && x < 3000).sort((a, b) => a - b); const q = k => f[Math.floor(f.length * k)] || 0; const e = performance.getEntriesByType('resource');
      return { bilder: f.length, p50: +q(.5).toFixed(1), p95: +q(.95).toFixed(1), max: +(f[f.length - 1] || 0).toFixed(1), ueber33: f.filter(x => x > 33).length, cls: +window.__cls.toFixed(4), kb: Math.round(e.reduce((a, x) => a + (x.transferSize || x.encodedBodySize || 0), 0) / 1024), kacheln: document.querySelectorAll('.li-f').length, wo: (window.__wo || []).slice(0, 4) }; });
    const z = { zeit: new Date().toISOString(), last: +os.loadavg()[0].toFixed(1), ansicht: a, cpu: CPU, fenster: W + 'x' + H, lade_ms: lade, ...r };
    console.log(JSON.stringify(z)); fs.appendFileSync(AUS, JSON.stringify(z) + '\n');
    await ctx.close();
  }
  await b.close();
})();
