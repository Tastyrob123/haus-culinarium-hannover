/* anleitung_bilder.js · echte Bildschirme für anleitung.html (Le Bureau, Culinarium), 1440 × 900, mit eigenem Wegwerf-Server und Wegwerf-Daten
   (ein Beispiel-Entwurf: ein Termin-Preis und ein Google-Titel), am Ende gelöscht. node anleitung_bilder.js → ../anleitung/*.webp */
const fs = require('fs'), path = require('path'), os = require('os'), net = require('net');
const { spawn, execFileSync } = require('child_process');
const pw = require(process.env.PLAYWRIGHT_PFAD || path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const BUREAU = path.resolve(__dirname, '..'), WS = path.join(os.homedir(), 'Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'bureau-anl-')), PROBE = path.join(WS, `_probe-anl-${process.pid}`), ZIEL = path.join(BUREAU, 'anleitung');
const warte = ms => new Promise(r => setTimeout(r, ms));
const frei = () => new Promise(r => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });
(async () => {
  const PORT = await frei(), B = `http://127.0.0.1:${PORT}`;
  execFileSync('python3', [path.join(WS, 'probe.py'), 'culinarium'], { env: Object.assign({}, process.env, { WEBSITE_PROBE: PROBE }) });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { env: Object.assign({}, process.env, { WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' }), stdio: 'ignore' });
  /* Aufräumen auch bei Abbruch (Fund 28.10.2026: in einer Schleife im Hintergrund blieben Prüfserver und Wegwerf-Kopien liegen) */
  const weg = () => { try { srv.kill('SIGKILL'); } catch (e) {} try { fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); } catch (e) {} };
  process.on('exit', weg); process.on('SIGINT', () => process.exit(130)); process.on('SIGTERM', () => process.exit(143)); process.on('unhandledRejection', e => { console.log('FEHLT  Lauf ohne Abbruch  → ' + (e && e.stack || e)); process.exit(1); });
  for (let i = 0; i < 60; i++) { try { if ((await fetch(B + '/_werkzeuge/bureau/')).ok) break; } catch (e) {} await warte(250); }
  const br = await pw.chromium.launch({ headless: true });
  const ctx = await br.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-culinarium-bureau', '1'); } catch (e) {} });
  const p = await ctx.newPage();
  const geh = async a => { await p.goto(B + '/_werkzeuge/bureau/?ansicht=' + encodeURIComponent(a), { waitUntil: 'load' }); await p.waitForSelector('#ws-mitte[data-ws-bereit]', { timeout: 20000 }); await warte(1400); };
  const bild = async n => { const f = path.join(DATEN, n + '.png'); await p.screenshot({ path: f }); return f; };
  const fertig = [];
  await geh('start'); fertig.push(['uebersicht', await bild('uebersicht')]);
  await geh('e:termine'); await p.locator('[data-cu-termin="b1"] input[name="preis"]').fill('95'); await p.locator('#ws-speichern').click(); await warte(1500);
  await geh('e:termine'); await p.evaluate(() => window.scrollTo(0, 330)); await warte(700); fertig.push(['termine', await bild('termine')]);
  await geh('b:start'); await warte(1500); await p.waitForFunction(() => !document.body.innerText.includes('Seite wird gesetzt'), null, { timeout: 20000 }).catch(() => {}); await warte(800); fertig.push(['bereich', await bild('bereich')]);
  await geh('haus:abende'); const ein = p.locator('details.ws-eintrag').nth(1); await ein.locator('summary').click(); await warte(400);
  await ein.locator('button.ws-foto').first().click({ force: true }); await p.waitForSelector('[data-ws-fenster="bild"]'); await warte(1200); fertig.push(['foto', await bild('foto')]);
  await geh('angaben'); fertig.push(['angaben', await bild('angaben')]);
  await geh('google'); await p.locator('[data-ws-seo="abend.html"] [data-ws-gt="titel"]').fill('Der Abend · Culinarium, Food-Pairing in Linden'); await p.locator('#ws-speichern').click(); await warte(1500);
  await geh('google'); await p.locator('[data-ws-seo="abend.html"]').scrollIntoViewIfNeeded(); await warte(600); fertig.push(['google', await bild('google')]);
  await geh('entwurf'); fertig.push(['entwurf', await bild('entwurf')]);
  await geh('verlauf'); fertig.push(['verlauf', await bild('verlauf')]);
  await br.close(); srv.kill();
  fs.mkdirSync(ZIEL, { recursive: true });
  execFileSync('python3', ['-c', 'import sys\nfrom PIL import Image\nfor a,b in zip(sys.argv[1::2],sys.argv[2::2]): Image.open(a).convert("RGB").save(b,"WEBP",quality=82)', ...fertig.flatMap(([n, f]) => [f, path.join(ZIEL, n + '.webp')])]);
  fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true });
  console.log('Anleitung: ' + fertig.length + ' Bilder in ' + ZIEL);
})();
