#!/usr/bin/env node
// Abnahme-Tor · Bewegung beim Scrollen (Kriterien 34 «flüssig» und 37 «Bewegung»), WebKit.
// Je Seite: (1) mit Bewegung langsam durchscrollen, jede Bildfolge messen (Bilder über 50 ms = Ruckler), laufende Animationen und ihre Eigenschaften
// erfassen (nur transform/opacity erlaubt), nach dem Scrollen nach Stücken suchen, die unsichtbar hängen geblieben sind;
// (2) mit prefers-reduced-motion: alles sofort sichtbar, keine langen Bewegungen.
// Aufruf: node bewegung-tor.js <ziele.json> <ausgabe-ordner> [--nur k1,k2] [--groesse 1440x900]
const path = require('path'), fs = require('fs');
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const [ZIELE, AUS] = process.argv.slice(2);
let ziele = JSON.parse(fs.readFileSync(ZIELE, 'utf8')).ziele; if (arg('nur')) ziele = ziele.filter(z => arg('nur').split(',').includes(z.k));
const [W, H] = arg('groesse', '1440x900').split('x').map(Number);
fs.mkdirSync(path.join(AUS, 'bilder'), { recursive: true });
const warte = ms => new Promise(r => setTimeout(r, ms));

const messeScroll = async (p) => p.evaluate(async () => {
  const frames = []; let laufend = true, letzte = performance.now();
  const tick = t => { frames.push(t - letzte); letzte = t; if (laufend) requestAnimationFrame(tick); }; requestAnimationFrame(tick);
  const eigenschaften = new Set(), animiert = new Set(); let maxAnim = 0;
  const sammle = () => { const a = document.getAnimations().filter(x => { const t = x.effect && x.effect.getTiming && x.effect.getTiming(); return !t || !(+t.duration <= 50) || t.iterations === Infinity; }); maxAnim = Math.max(maxAnim, a.length);   // Übergänge ≤ 50 ms sind Sprünge, keine Bewegung
    for (const x of a) { const ef = x.effect; if (!ef || !ef.getKeyframes) continue; const tgt = ef.target; if (tgt) animiert.add(tgt.tagName + '.' + String(tgt.className.baseVal ?? tgt.className).split(' ')[0]);
      if (x.transitionProperty) eigenschaften.add(x.transitionProperty); for (const k of ef.getKeyframes()) for (const p of Object.keys(k)) if (!['offset', 'easing', 'composite', 'computedOffset'].includes(p)) eigenschaften.add(p); } };
  const hoch = document.documentElement.scrollHeight, schritt = Math.max(40, innerHeight / 18);
  for (let y = 0; y <= hoch; y += schritt) { scrollTo(0, y); sammle(); await new Promise(r => setTimeout(r, 40)); }
  await new Promise(r => setTimeout(r, 1800)); sammle(); laufend = false;
  const f = frames.slice(2).filter(x => x < 1000); const sortiert = [...f].sort((a, b) => a - b);
  // Stücke im Fenster, die nach dem Scrollen unsichtbar geblieben sind (Auftritt nicht ausgelöst)
  const unsichtbar = []; for (let y = 0; y <= hoch; y += innerHeight * .8) { scrollTo(0, y); await new Promise(r => setTimeout(r, 900));
    for (const e of document.querySelectorAll('body *')) { const r = e.getBoundingClientRect(); if (r.width < 30 || r.height < 14 || r.bottom < 0 || r.top > innerHeight) continue;
      const c = getComputedStyle(e); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity >= .1) continue; let a = e.parentElement, schon = false; while (a) { const ca = getComputedStyle(a); if (+ca.opacity < .1 || ca.visibility === 'hidden' || ca.display === 'none') { schon = true; break; } a = a.parentElement; }
      if (!schon && (e.innerText || '').trim() || (!schon && e.querySelector('img'))) unsichtbar.push({ sel: e.tagName.toLowerCase() + '.' + String(e.className.baseVal ?? e.className).trim().split(/\s+/).slice(0, 2).join('.'), text: (e.innerText || '').trim().slice(0, 40), y: Math.round(r.top + scrollY) }); } }
  const u = [...new Map(unsichtbar.map(x => [x.sel + x.text, x])).values()].slice(0, 20);
  return { bilder: f.length, ruckler: f.filter(x => x > 50).length, p95: sortiert[Math.floor(sortiert.length * .95)] || 0, mittel: f.reduce((a, b) => a + b, 0) / Math.max(1, f.length), maxAnim, animiert: [...animiert].slice(0, 30), eigenschaften: [...eigenschaften], unsichtbar: u };
});

(async () => {
  const b = await pw.webkit.launch(); const erg = [];
  for (const z of ziele) for (const url of [z.url, ...(z.startExtra || [])]) {
    const r = { k: z.k, name: z.name, url, funde: [] };
    for (const reduce of [false, true]) {
      const ctx = await b.newContext({ viewport: { width: W, height: H }, reducedMotion: reduce ? 'reduce' : 'no-preference', locale: 'de-DE' });
      await ctx.route('**/*', q => q.request().method() === 'GET' || q.request().method() === 'HEAD' ? q.continue() : q.fulfill({ status: 200, body: '{}' }));
      await ctx.addInitScript(v => { try { for (const [k, w] of Object.entries(v || {})) localStorage.setItem(k, w); } catch (e) { } }, z.localStorage || {});
      const p = await ctx.newPage(); const t0 = Date.now();
      await p.goto(url, { waitUntil: 'load', timeout: 30000 }).catch(() => { }); const lade = Date.now() - t0; await warte(1200);
      const m = await messeScroll(p).catch(e => ({ fehler: String(e).slice(0, 120) }));
      await p.evaluate(() => scrollTo(0, 0)); await warte(400);
      const bild = `${z.k}-${(url.split('?')[1] || 'start').replace(/\W+/g, '')}-${reduce ? 'ruhig' : 'bewegt'}.jpg`;
      await p.screenshot({ path: path.join(AUS, 'bilder', bild), type: 'jpeg', quality: 70 }).catch(() => { });
      r[reduce ? 'ruhig' : 'bewegt'] = { ...m, ladezeit: lade, bild };
      if (m.fehler) r.funde.push({ k: 34, info: 'Messung fehlgeschlagen: ' + m.fehler });
      else if (!reduce) {
        if (m.ruckler > 2 || m.p95 > 34) r.funde.push({ k: 34, info: `Scrollen ruckelt: ${m.ruckler} Bilder über 50 ms, 95 % der Bilder unter ${Math.round(m.p95)} ms (${m.bilder} Bilder)` });
        if (!m.maxAnim) r.funde.push({ k: 37, info: 'Keine Bewegung beim Scrollen (keine Animation lief)' });
        const fremd = m.eigenschaften.filter(x => !/^(transform|opacity|translate|scale|rotate|filter|clip-path|all)$/.test(x));
        if (fremd.length) r.funde.push({ k: 37, info: `Animiert auch ${fremd.slice(0, 6).join(', ')} (erlaubt nur transform/opacity)` });
        if (m.unsichtbar.length) r.funde.push({ k: 37, info: `${m.unsichtbar.length} Stücke bleiben nach dem Scrollen unsichtbar: ${m.unsichtbar.slice(0, 3).map(x => '«' + (x.text || x.sel) + '»').join(', ')}` });
      } else {
        if (m.unsichtbar.length) r.funde.push({ k: 37, info: `reduced-motion: ${m.unsichtbar.length} Stücke bleiben unsichtbar: ${m.unsichtbar.slice(0, 3).map(x => '«' + (x.text || x.sel) + '»').join(', ')}` });
        if (m.maxAnim > 6) r.funde.push({ k: 37, info: `reduced-motion: trotzdem ${m.maxAnim} Animationen gleichzeitig` });
      }
      await ctx.close();
    }
    erg.push(r); console.log(z.k, url.split('/').pop(), r.funde.length ? r.funde.map(f => 'K' + f.k + ' ' + f.info).join(' | ') : 'ok', `· ${r.bewegt && r.bewegt.bilder} Bilder, ${r.bewegt && r.bewegt.maxAnim} Animationen`);
    fs.writeFileSync(path.join(AUS, 'bewegung.json'), JSON.stringify({ zeit: new Date().toISOString(), groesse: [W, H], seiten: erg }, null, 1));
  }
  await b.close();
})();
