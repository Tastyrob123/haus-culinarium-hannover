/* fluss-termine.js · Flüssigkeit der Ansicht «Termine» gedrosselt (Regel 55), am echten Server 9082, nur lesen. node fluss-termine.js [aus.json]
   Je Drosselung 1×, 4×, 6× (Chromium): Ansicht öffnen bis die Plakate stehen · Tippen im Preisfeld bis die Leiste «1 Eingabe» zeigt · «Neuer Abend» bis die Karte steht ·
   Scrollen der Ansicht (Bildabstand p95 und längster). Gespeichert wird nichts (Eingaben werden verworfen, Verlassen ohne Rückfrage). */
const path = require('path'), fs = require('fs'), os = require('os');
const pw = require(process.env.PLAYWRIGHT_PFAD || path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const B = 'http://127.0.0.1:9082/_werkzeuge/bureau/?ansicht=e:termine';
(async () => {
  const br = await pw.chromium.launch({ headless: true }), aus = [];
  for (const rate of [1, 4, 6]) {
    const k = await br.newContext({ viewport: { width: 1440, height: 900 } });
    await k.addInitScript(() => { try { localStorage.setItem('rundgang-culinarium-bureau', '1'); } catch (e) {} });
    const s = await k.newPage(); const cdp = await k.newCDPSession(s);
    await cdp.send('Emulation.setCPUThrottlingRate', { rate });
    const r = { rate }; let t = Date.now();
    await s.goto(B); await s.waitForSelector('.cu-t .cu-pl', { timeout: 30000 }); r.oeffnen_ms = Date.now() - t;
    await s.waitForTimeout(600);
    t = Date.now(); await s.locator('[data-cu-termin="b1"] input[name="preis"]').fill('91');
    await s.waitForFunction(() => /1 Eingabe/.test(document.querySelector('#ws-leiste').textContent)); r.tippen_ms = Date.now() - t;
    /* im Browser gemessen (Klick bis die neue Karte gezeichnet ist, nächstes Bild): Playwrights click() wartet zuerst, bis der Knopf im schwebenden Startbild ruhig steht */
    r.neuer_abend_ms = await s.evaluate(() => new Promise(fertig => { const t = performance.now(); document.querySelector('[data-cu-neu]').click(); requestAnimationFrame(() => fertig(Math.round(performance.now() - t))); }));
    await s.waitForFunction(() => document.querySelectorAll('.cu-t').length === 5);
    r.scroll = await s.evaluate(() => new Promise(fertig => { const d = []; let vor = performance.now(), y = 0;
      const schritt = jetzt => { d.push(jetzt - vor); vor = jetzt; y += 22; window.scrollTo(0, y); if (d.length < 120) requestAnimationFrame(schritt); else { d.sort((a, b) => a - b); fertig({ p95_ms: +d[Math.floor(d.length * .95)].toFixed(1), laengster_ms: +d[d.length - 1].toFixed(1) }); } };
      requestAnimationFrame(schritt); }));
    aus.push(r); console.log(JSON.stringify(r));
    await k.close();
  }
  await br.close();
  if (process.argv[2]) fs.writeFileSync(process.argv[2], JSON.stringify(aus, null, 1));
})();
