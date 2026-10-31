// Leistung: Zeit bis zum ersten sichtbaren Knopf (ab Navigationsbeginn), Chromium, ungedrosselt und CPU 4× gedrosselt, Median aus N Läufen.
// node leistung.js <url> [selektor] [läufe]
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const [,, URL, SEL = '.wo-kn, .wo-sb button, .wo-sb a.wo-kn, main button, button', N = '5'] = process.argv;
const med = a => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
(async () => { const b = await pw.chromium.launch(); const erg = {};
  for (const [name, rate] of [['ungedrosselt', 1], ['gedrosselt 4×', 4]]) { const t = [], lcp = [];
    for (let i = 0; i < +N; i++) { const c = await b.newContext({ viewport: { width: 1440, height: 900 } }); const p = await c.newPage();
      await c.addInitScript(() => { try { for (const k of Object.keys(localStorage)) if (k.startsWith('rundgang')) localStorage.removeItem(k); ['maison','bureau','carte','reception','livre','registre'].forEach(w => localStorage.setItem('rundgang-culinarium-' + w, '1')); localStorage.setItem('rundgang-reception', '1'); } catch (e) {} });
      const cdp = await c.newCDPSession(p); await cdp.send('Network.setCacheDisabled', { cacheDisabled: true }); await cdp.send('Emulation.setCPUThrottlingRate', { rate });
      await p.goto(URL, { waitUntil: 'commit' });
      await p.waitForFunction(sel => { const e = [...document.querySelectorAll(sel)].find(x => { const r = x.getBoundingClientRect(); const c = getComputedStyle(x); return r.width > 20 && r.height > 20 && r.top < innerHeight && c.visibility !== 'hidden' && +c.opacity > 0.9; }); return e ? performance.now() : false; }, SEL, { polling: 'raf', timeout: 30000 }).then(h => h.jsonValue()).then(v => t.push(v)).catch(() => t.push(NaN));
      await c.close(); }
    erg[name] = { median_ms: Math.round(med(t)), laeufe: t.map(Math.round) }; }
  console.log(JSON.stringify({ url: URL, ...erg })); await b.close(); })();
