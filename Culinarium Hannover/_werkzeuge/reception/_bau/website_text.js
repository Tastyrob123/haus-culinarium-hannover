// Wortlaut der Culinarium-Website, wie ein Gast ihn sieht (28.10.2026): innerText jeder Seite, headless, nur lesen.
// Quelle für _bau/culinarium_wissen.py. Aufruf aus dem Projektordner: node _werkzeuge/reception/_bau/website_text.js [basis, Standard http://localhost:8765]
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const BASIS = process.argv[2] || 'http://localhost:8765';
const SEITEN = ['index', 'abend', 'abende', 'bar', 'leute', 'weg', 'dirty-chicken', 'impressum', 'datenschutz'];
const ZIEL = path.join(__dirname, 'website-text');
(async () => {
  const br = await chromium.launch({ headless: true });
  const c = await br.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  await c.route(/^(mailto|tel|sms):/, r => r.abort());
  const p = await c.newPage();
  for (const s of SEITEN) {
    await p.goto(`${BASIS}/${s}.html`, { waitUntil: 'networkidle' });
    const t = await p.evaluate(() => {
      // Beispieltermine und gespielte Zahlung («Vorschau · Termine und Zahlung sind nur simuliert») sind keine Angaben des Hauses: nie ins Wissen
      // «Gut zu wissen» (Startseite): jede Antwort liegt hinter ihrer Frage, ein Gast tippt sie an; fürs Wissen alle aufgeklappt
      document.querySelectorAll('.gt-a').forEach(e => { e.removeAttribute('hidden'); e.removeAttribute('aria-hidden'); });
      const st = document.createElement('style'); st.textContent = '*{text-transform:none!important}.gt-a{display:block!important;visibility:visible!important;position:static!important}'; document.head.appendChild(st);   // Wortlaut, nicht die Versalien der Schrift
      document.querySelectorAll('script,noscript,[hidden],[aria-hidden="true"],#termine-buchen,#tb-dialog,.tb').forEach(e => e.remove());
      // Überschriften als «## …» (eine Zeile, wie gesprochen): daran teilt «Das weiss der Chat» die Seiten in Abschnitte
      document.querySelectorAll('main h1, main h2, section h1, section h2').forEach(h => { const t = (h.getAttribute('aria-label') || h.innerText).replace(/\s+/g, ' ').trim(); if (t) h.innerText = '## ' + t; });
      return document.body.innerText;
    });
    const zeilen = []; const da = new Set();
    for (let z of t.split('\n')) { z = z.replace(/\s+/g, ' ').trim(); if (!z || /^[0-9]$/.test(z) || da.has(z)) continue; da.add(z); zeilen.push(z); }
    fs.writeFileSync(path.join(ZIEL, s + '.txt'), `Quelle: ${BASIS}/${s}.html\nAbgerufen: ${new Date().toISOString().slice(0, 10)}\n\n` + zeilen.join('\n') + '\n');
    console.log(s, zeilen.length, 'Zeilen');
  }
  await br.close();
})();
