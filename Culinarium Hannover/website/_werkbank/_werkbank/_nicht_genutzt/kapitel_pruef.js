// Prüfung der Werkbank in Kapiteln (Ruedihus, Werkbank-Chat 17.10.2026; Kopie aus dem Waldhotel Doldenhorn): node _werkbank/kapitel_pruef.js [chromium|webkit] [1440|390] [ziel]
// Unsichtbar (headless, eigener Browser, nichts im Vordergrund). mailto: und tel: werden abgefangen und nie ausgeführt.
// Fährt die Seite ganz durch, meldet Fehler, fehlende Dateien, seitliches Überlaufen, Scrollen in Bildern/Kacheln/Bändern, unsichtbar Gebliebenes,
// bedient Register, Befunde, Werkzeug-Reiter, «Einmal ändern», die Bänder und den Fächer im Fuss und nimmt jeden Abschnitt als Bild auf.
const path = require('path'), fs = require('fs');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const art = process.argv[2] || 'chromium', breite = +(process.argv[3] || 1440);
const ziel = process.argv[4] || path.join(__dirname, '..', '_qa', 'kapitel', `${art}-${breite}`);
const URL_ = process.env.URL_ || 'http://127.0.0.1:8917/werkbank/';
fs.mkdirSync(ziel, { recursive: true });
(async () => {
  const b = await PW[art].launch({ headless: true });
  const handy = breite < 700;
  const ctx = await b.newContext({ viewport: { width: breite, height: handy ? 844 : 900 }, deviceScaleFactor: 1, isMobile: handy && art === 'chromium', hasTouch: handy });
  const p = await ctx.newPage();
  const fehler = [], fehlt = [], mail = [];
  p.on('pageerror', x => fehler.push('Seitenfehler: ' + x.message));
  p.on('console', m => { if (m.type() === 'error') fehler.push('Konsole: ' + m.text().slice(0, 200)); });
  p.on('response', r => { if (r.status() >= 400 && !/favicon/.test(r.url())) fehlt.push(r.status() + ' ' + r.url()); });
  await p.route(/^(mailto|tel):/, r => { mail.push(r.request().url()); r.abort(); });
  await p.addInitScript(() => { document.addEventListener('click', ev => { const a = ev.target.closest && ev.target.closest('a[href^="mailto:"],a[href^="tel:"]'); if (a) { ev.preventDefault(); window.__mail = (window.__mail || 0) + 1; } }, true); });
  await p.goto(URL_, { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(1500);
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h + 900; y += 500) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(160); }
  await p.waitForTimeout(1200);
  const befund = await p.evaluate(() => {
    const aus = { ueber: document.documentElement.scrollWidth - innerWidth, kapitel: [], scrollt: [], unsichtbar: [], bilder: [], mailto: document.querySelectorAll('a[href^="mailto:"]').length, preis: [] };
    for (const id of ['worum', 'register', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8', 'ag-wochen', 'schluss', 'uebersicht']) if (!document.getElementById(id)) aus.kapitel.push(id);
    for (const el of document.querySelectorAll('main *, footer *')) {
      const s = getComputedStyle(el);
      if (/(auto|scroll)/.test(s.overflowX + s.overflowY) && (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) && el.clientHeight > 40)
        aus.scrollt.push((el.className && el.className.baseVal === undefined ? el.className : el.tagName) + ' ' + el.scrollWidth + 'x' + el.scrollHeight + '/' + el.clientWidth + 'x' + el.clientHeight);
    }
    for (const el of document.querySelectorAll('[data-a]')) { const r = el.getBoundingClientRect(); if (r.width && getComputedStyle(el).opacity === '0' && !el.closest('.ins-t,.wfa__texte>div,.rgw,.fb,.bfk-tafel,.ins-mini')) aus.unsichtbar.push(el.className + ' ' + (el.textContent || '').trim().slice(0, 40)); }
    for (const im of document.images) if (im.complete && im.naturalWidth === 0 && im.getAttribute('src') && !im.getAttribute('src').startsWith('data:')) aus.bilder.push(im.getAttribute('src'));
    const txt = document.body.innerText;
    for (const m of txt.matchAll(/(Beispiel\s*CHF|CHF\s*[\d’']+[^\n]{0,30}(im Monat|monatlich))/g)) aus.preis.push(m[0]);
    for (const w of ['Werkbank', 'Koh Phangan', 'Siargao', 'Instagram-Profil von Tasty', 'Zeitfenster', 'zwanzig Minuten', 'Material']) if (txt.includes(w)) aus.preis.push('Wort: ' + w);
    return aus;
  });
  // Bedienen
  const klick = [];
  async function k(name, fn) { try { await fn(); klick.push('ok ' + name); } catch (x) { klick.push('FEHLER ' + name + ': ' + String(x).slice(0, 140)); } }
  await k('Register Pfeil', async () => { await p.locator('#register [data-f="1"]').scrollIntoViewIfNeeded(); await p.click('#register [data-f="1"]'); await p.waitForTimeout(500); const t = await p.locator('#register .wfa__texte>div.an h3').textContent(); if (!/Marke/.test(t)) throw t; });
  await k('Befund 3 und Pfeil', async () => { const i = p.locator('#k1 .bfp-i').nth(2); await i.scrollIntoViewIfNeeded(); await i.click(); await p.waitForTimeout(300); if (!(await p.locator('#k1 .bfn-s.an[data-b="2"]').count())) throw 'Seite'; await p.locator('#k1 .bfn-s.an .bfn-wahl button').nth(1).click(); await p.waitForTimeout(300); if (!(await p.locator('#k1 .bfn-s.an .bfn-g.an[data-g="1"]').count())) throw 'Beleg 2'; const y0 = await p.locator('#k1 .bfn-s.an h3').evaluate(h => h.getBoundingClientRect().top); await p.locator('#k1 .bfn-s.an .bfn-pf[data-f="1"]').click(); await p.waitForTimeout(300); if (!(await p.locator('#k1 .bfn-s.an[data-b="3"]').count())) throw 'Pfeil'; const y1 = await p.locator('#k1 .bfn-s.an h3').evaluate(h => h.getBoundingClientRect().top); if (Math.abs(y1 - y0) > 1) throw 'Titel springt ' + y0 + '→' + y1; });
  await k('KI-Seite', async () => { const r = await p.request.get(new URL('ki.html', URL_).href); if (r.status() !== 200) throw r.status(); if (!(await p.locator('a[href="ki.html"]').count())) throw 'kein Verweis'; });
  await k('Werkzeug-Reiter', async () => { const r = p.locator('#k5 .ins-r'); const n = await r.count(); for (let i = 0; i < n; i++) { await r.nth(i).scrollIntoViewIfNeeded(); await r.nth(i).click(); await p.waitForTimeout(450); if ((await r.nth(i).getAttribute('aria-selected')) !== 'true') throw 'Reiter ' + i; } await r.nth(0).click(); });
  await k('Einmal ändern', async () => { const w = p.locator('.fb__w'); const n = await w.count(); if (n < 4) throw 'nur ' + n + ' Szenen'; await w.nth(1).scrollIntoViewIfNeeded(); await w.nth(1).click(); await p.waitForTimeout(600); });
  await k('Band Wochen', async () => { const v = p.locator('#ag-wochen [data-vor]'); await v.scrollIntoViewIfNeeded(); const x0 = await p.locator('#ag-wochen .band').evaluate(e => e.scrollLeft); await v.click(); await p.waitForTimeout(900); const x1 = await p.locator('#ag-wochen .band').evaluate(e => e.scrollLeft); if (!(x1 > x0)) throw 'Band rückt nicht ' + x0 + '→' + x1; });
  await k('Fächer Fuss', async () => { const f = p.locator('#uebersicht [data-f="1"]'); await f.scrollIntoViewIfNeeded(); await f.click(); await p.waitForTimeout(400); });
  if (!handy) await k('Laptop öffnet Die Stube', async () => { await p.locator('#k5 .ins-r').nth(0).click(); const e = p.locator('#k5 .ins-dev__e'); await e.scrollIntoViewIfNeeded(); await p.waitForTimeout(600); await e.click(); await p.waitForSelector('#k5 iframe.ins-live', { timeout: 15000 }); await p.waitForTimeout(3000); const src = await p.locator('#k5 iframe.ins-live').getAttribute('src'); klick.push('  iframe ' + src); });
  // Bilder je Abschnitt
  for (const id of ['brief', 'worum', 'register', 'k1', 'ag-vorschlag', 'k2', 'unterlagen', 'k5', 'papier', 'geprueft', 'k8', 'ag-wochen', 'schluss', 'uebersicht', 'seiten']) {
    const el = await p.$(id === 'uebersicht' || id === 'ag-vorschlag' ? '#' + id : `section:has(#${id}), #${id}`);
    if (!el) continue;
    await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(1300);
    await p.screenshot({ path: path.join(ziel, id + '.jpg'), type: 'jpeg', quality: 70 });
  }
  const mailtoKlick = await p.evaluate(() => window.__mail || 0);
  const erg = { art, breite, befund, klick, fehler: fehler.slice(0, 20), fehlt: fehlt.slice(0, 20), mailAbgefangen: mail.concat(mailtoKlick ? ['Klicks auf mailto/tel: ' + mailtoKlick] : []) };
  fs.writeFileSync(path.join(ziel, 'ergebnis.json'), JSON.stringify(erg, null, 1));
  console.log(JSON.stringify(erg, null, 1));
  await b.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
