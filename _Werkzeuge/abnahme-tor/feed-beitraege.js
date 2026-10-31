#!/usr/bin/env node
// Abnahme-Tor · Werkbank-Feed: jeden Beitrag (div.t) öffnen, messen (messen.js) und aufnehmen, Grössen nach Wahl, WebKit.
// Die Beiträge sind keine Knöpfe; das Inventar des Tors erreicht sie nicht. Aufruf: node feed-beitraege.js <ausgabe> 1440x900 390x844 …
const path = require('path'), fs = require('fs');
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const messen = require('../messlauf/messen.js');
const [AUS, ...gr] = process.argv.slice(2); fs.mkdirSync(path.join(AUS, 'bilder'), { recursive: true });
(async () => { const b = await pw.webkit.launch(); const erg = [];
  for (const g of gr) { const [W, H] = g.split('x').map(Number);
    const ctx = await b.newContext({ viewport: { width: W, height: H }, isMobile: W < 700, hasTouch: W < 700 });
    await ctx.route('**/*', q => ['GET', 'HEAD'].includes(q.request().method()) ? q.continue() : q.fulfill({ status: 200, body: '{}' }));
    const p = await ctx.newPage(); await p.goto('http://127.0.0.1:9088/feed/index.html', { waitUntil: 'load' }); await p.waitForTimeout(2500);
    const n = await p.locator('#grid .t').count();
    for (let i = 0; i < n; i++) {
      if (i === 0) { const loc = p.locator('#grid .t').nth(0); await loc.scrollIntoViewIfNeeded().catch(() => { }); await loc.click({ force: true, timeout: 5000 }).catch(() => { }); }
      else await p.locator('#nach').click({ force: true, timeout: 5000 }).catch(() => { });   // weiter mit «Nächster ›» durch alle Beiträge
      await p.waitForTimeout(1300);
      const m = await p.evaluate(messen).catch(e => [{ art: 'fehler', info: String(e).slice(0, 100) }]);
      const offen = await p.evaluate(() => { const q = document.querySelector('#post'); return q && q.getAttribute('aria-hidden') !== 'true'; });
      const platz = await p.evaluate(() => { const q = document.querySelector('#post'); return q ? (q.innerText.match(/\[[^\]]{2,30}\]|Lorem|undefined|Probe/g) || []) : []; });   // K23: Arbeitsstand sichtbar
      if (platz.length) m.push({ art: 'platzhalter-text', text: platz.slice(0, 4).join(' '), info: 'sichtbarer Platzhalter im Beitrag' });
      const bild = `${W}-${String(i + 1).padStart(2, '0')}.jpg`; await p.screenshot({ path: path.join(AUS, 'bilder', bild), type: 'jpeg', quality: 70 });
      erg.push({ groesse: W, beitrag: i + 1, offen, funde: m.map(f => ({ art: f.art, text: (f.text || '').slice(0, 60), info: (f.info || '').slice(0, 120), sel: f.sel })), bild });
      console.log(W, i + 1, offen ? 'offen' : 'NICHT OFFEN', m.length, 'Funde');
    }
    await ctx.close(); }
  fs.writeFileSync(path.join(AUS, 'beitraege.json'), JSON.stringify(erg, null, 1)); await b.close(); })();
