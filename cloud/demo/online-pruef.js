// node online-pruef.js <basis-url> → öffnet Werkbank-Seiten und die sieben Werkzeug-Demos online bei vier Breiten
// und meldet je Seite: fehlende Dateien (4xx), kaputte Bilder, leere Hintergrundbilder, Skriptfehler.
const pw = require('playwright');
const BASIS = process.argv[2].replace(/\/?$/, '/');
const SEITEN = ['index.html', 'werkbank/index.html', 'werkbank/ki.html', 'werkbank/karte.html', 'werkbank/geprueft/index.html', 'befund/index.html',
  'unterlagen/index.html', 'drucksachen/index.html', 'untersetzer/index.html', 'sticker/index.html', 'feed/index.html', 'mails/index.html',
  'material/index.html', 'postkarten/index.html', 'beigaben/index.html',
  'werkzeuge/maison/index.html', 'werkzeuge/bureau/index.html', 'werkzeuge/carte/index.html', 'werkzeuge/reception/index.html',
  'werkzeuge/livre/index.html', 'werkzeuge/registre/index.html', 'werkzeuge/imprimerie/index.html'];
(async () => {
  const b = await pw.chromium.launch();
  let fehlerGesamt = 0;
  for (const s of SEITEN) {
    for (const br of [1440, 1000, 700, 390]) {
      const p = await b.newPage({ viewport: { width: br, height: 900 } });
      const fehl = new Set(), err = new Set();
      p.on('response', r => { if (r.status() >= 400 && r.url().startsWith(BASIS)) fehl.add(r.status() + ' ' + r.url().slice(BASIS.length)); });
      p.on('pageerror', e => err.add(String(e).slice(0, 120)));
      let st = 0;
      try { const r = await p.goto(BASIS + s, { waitUntil: 'networkidle', timeout: 60000 }); st = r ? r.status() : 0; } catch (e) { err.add('GOTO ' + e.message.slice(0, 80)); }
      await p.waitForTimeout(2500);
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight && y < 30000; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } }).catch(() => {});
      await p.waitForTimeout(2000);
      const kaputt = await p.evaluate(() => [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute('src') && i.getBoundingClientRect().width > 0).map(i => i.currentSrc || i.src).slice(0, 8)).catch(() => []);
      const leer = await p.evaluate(async () => {
        const urls = [...document.querySelectorAll('[style*="background"]')].map(e => (getComputedStyle(e).backgroundImage.match(/url\("?([^")]+)"?\)/) || [])[1]).filter(Boolean);
        const out = [];
        for (const u of [...new Set(urls)].slice(0, 40)) { const ok = await new Promise(r => { const i = new Image(); i.onload = () => r(true); i.onerror = () => r(false); i.src = u; }); if (!ok) out.push(u); }
        return out.slice(0, 8);
      }).catch(() => []);
      const text = await p.evaluate(() => document.body ? document.body.innerText.trim().length : 0).catch(() => 0);
      const kurz = u => u.replace(BASIS, '');
      const probleme = [...fehl].length + kaputt.length + leer.length + err.size + (text < 50 ? 1 : 0) + (st >= 400 ? 1 : 0);
      fehlerGesamt += probleme;
      console.log(`${probleme ? 'FEHLER' : 'ok    '} ${br} ${s} status=${st} text=${text}` + (probleme ? ' ' + JSON.stringify({ fehl: [...fehl].slice(0, 8), kaputt: kaputt.map(kurz), leer: leer.map(kurz), err: [...err] }) : ''));
      await p.close();
    }
  }
  console.log('PROBLEME GESAMT: ' + fehlerGesamt);
  await b.close();
})();
