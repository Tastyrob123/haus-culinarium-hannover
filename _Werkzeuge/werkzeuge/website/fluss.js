/* fluss.js · Flüssigkeit des Werkzeugs «website» gedrosselt messen (Regel 55, Master Werkzeug-Bau 8). Liest nur, speichert nichts.
     node werkzeuge/website/fluss.js <adresse-des-werkzeugs> [ausgabe.json]
   Beispiel: node werkzeuge/website/fluss.js "http://127.0.0.1:8970/werkzeuge/website/?haus=schloessli"
   Je Drosselung (Prozessor 1×, 4×, 6×, Chromium, unsichtbar): Öffnen bis die Übersicht steht · Scrollen der Übersicht (Bildabstand p95 und längster) ·
   Bereich öffnen bis die Liste der Stellen steht · Bereich bis die Seite in der Vorschau steht · Zeiten & Preise öffnen.
   Playwright: PLAYWRIGHT_PFAD, sonst ~/Aussen-Pruefung/node_modules/playwright. */
const path = require('path'), fs = require('fs'), os = require('os');
const pw = require(process.env.PLAYWRIGHT_PFAD || path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const [ADR, AUS] = process.argv.slice(2);
if (!ADR) { console.error('Adresse fehlt.'); process.exit(2); }
const mit = (adr, q) => adr + (adr.includes('?') ? '&' : '?') + q;

async function lauf(browser, rate) {
  const k = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  await k.addInitScript(() => { try { localStorage.setItem('ws-wer', 'Messung'); } catch (e) { /* ohne */ } });
  const s = await k.newPage();
  const cdp = await k.newCDPSession(s);
  await cdp.send('Emulation.setCPUThrottlingRate', { rate });
  const r = { rate };
  let t = Date.now();
  await s.goto(mit(ADR, 'ansicht=start'));
  await s.waitForSelector('.ws-bereiche .ws-bk', { timeout: 30000 });
  r.oeffnen_ms = Date.now() - t;
  r.scroll = await s.evaluate(() => new Promise(fertig => {
    const d = []; let vor = performance.now(), y = 0;
    const schritt = jetzt => { d.push(jetzt - vor); vor = jetzt; y += 22; window.scrollTo(0, y); if (d.length < 90) requestAnimationFrame(schritt); else { d.shift(); d.sort((a, b) => a - b); fertig({ p95_ms: +d[Math.floor(d.length * .95)].toFixed(1), laengster_ms: +d[d.length - 1].toFixed(1) }); } };
    requestAnimationFrame(schritt);
  }));
  t = Date.now();
  await s.locator('.ws-bereiche .ws-bk').first().click({ force: true });   // ohne auf das Ende des Schwebens zu warten: ein Mensch klickt schon währenddessen
  await s.waitForSelector('#ws-gruppen .ws-gr, #ws-gruppen details', { timeout: 30000 });
  r.bereich_liste_ms = Date.now() - t;
  await s.waitForFunction(() => { const f = document.querySelector('iframe[data-ws-frame]'); return f && f.closest('.ws-vorschau') && !f.closest('.ws-vorschau').querySelector('.ws-vorschau__lage:not([hidden])') ? true : !!(f && f.contentDocument && f.contentDocument.body && f.contentDocument.body.childElementCount); }, null, { timeout: 30000 });
  r.bereich_seite_ms = Date.now() - t;
  t = Date.now();
  await s.goto(mit(ADR, 'ansicht=zahlen'));
  await s.waitForSelector('.ws-karte, .ws-zl', { timeout: 30000 });
  r.zeiten_preise_ms = Date.now() - t;
  await k.close();
  return r;
}

(async () => {
  const browser = await pw.chromium.launch({ headless: true });
  const werte = [];
  try { for (const rate of [1, 4, 6]) werte.push(await lauf(browser, rate)); } finally { await browser.close(); }
  const aus = { adresse: ADR, zeit: new Date().toISOString(), last: os.loadavg()[0].toFixed(1), werte };
  console.log(JSON.stringify(aus, null, 1));
  if (AUS) fs.writeFileSync(AUS, JSON.stringify(aus, null, 1));
})();
