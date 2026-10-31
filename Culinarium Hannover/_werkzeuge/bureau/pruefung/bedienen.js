/* bedienen.js · Abnahme von Le Bureau (Culinarium Hannover, 28.10.2026, aus dem Lauf des Schäfli) nach Master Werkzeug-Bau 4.2 und 8: jede Funktion wird BEDIENT, nicht nur geladen.
   node bedienen.js [chromium|webkit|firefox] [1440|390|320]
   Eigener Server (freier Port ab 9073) mit Wegwerf-Daten (WERKZEUGE_DATEN) und Wegwerf-Kopie der Seiten (WEBSITE_PROBE), beides am Ende gelöscht,
   eigener Prozess am Ende per PID beendet. Browser unsichtbar. Echte Daten und die Website des Hauses werden nie angefasst.
   Ergebnis: eine Zeile je Prüfung, am Ende BESTANDEN / NICHT BESTANDEN; Bilder in pruefung/bilder/bedienen-<motor>-<breite>-*.png. */
const fs = require('fs'), path = require('path'), os = require('os'), net = require('net'), crypto = require('crypto');
const { spawn, execFileSync } = require('child_process');
const pw = require(process.env.PLAYWRIGHT_PFAD || path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const MOTOR = process.argv[2] || 'chromium', BREITE = Number(process.argv[3] || 1440), HOEHE = Number(process.argv[4]) || (BREITE < 700 ? 844 : 900);
const HIER = __dirname, BUREAU = path.resolve(HIER, '..');
const STAMM = path.join(os.homedir(), 'Desktop/Website-Projekte/_Werkzeuge'), WS = path.join(STAMM, 'werkzeuge/website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'bureau-culinarium-')), PROBE = path.join(WS, `_probe-bureau-${process.pid}`);
const BILDER = path.join(HIER, 'bilder');
fs.mkdirSync(BILDER, { recursive: true });
let n = 0; const rot = [];
function pruef(ok, was, mehr) { n++; console.log((ok ? 'gut    ' : 'FEHLT  ') + was + (!ok && mehr ? '  → ' + String(mehr).slice(0, 300) : '')); if (!ok) rot.push(was); return ok; }
const warte = ms => new Promise(r => setTimeout(r, ms));
async function bis(fn, ms = 8000) { for (const e = Date.now() + ms; Date.now() < e; await warte(120)) { try { if (await fn()) return true; } catch (x) { } } return false; }
const freierPort = () => new Promise(r => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });

(async () => {
  const PORT = Number(process.env.PORT) || await freierPort(), B = `http://127.0.0.1:${PORT}`;
  execFileSync('python3', [path.join(WS, 'probe.py'), 'culinarium'], { env: Object.assign({}, process.env, { WEBSITE_PROBE: PROBE }) });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { env: Object.assign({}, process.env, { WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' }), stdio: ['ignore', 'pipe', 'pipe'] });
  /* Aufräumen auch bei Abbruch (Fund 28.10.2026: in einer Schleife im Hintergrund blieben Prüfserver und Wegwerf-Kopien liegen) */
  const weg = () => { try { srv.kill('SIGKILL'); } catch (e) {} try { fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); } catch (e) {} };
  process.on('exit', weg); process.on('SIGINT', () => process.exit(130)); process.on('SIGTERM', () => process.exit(143)); process.on('unhandledRejection', e => { console.log('FEHLT  Lauf ohne Abbruch  → ' + (e && e.stack || e)); process.exit(1); });
  let serverText = ''; srv.stdout.on('data', d => serverText += d); srv.stderr.on('data', d => serverText += d);
  await bis(async () => (await fetch(B + '/_werkzeuge/bureau/')).ok, 15000);
  const ONLINE = path.join(PROBE, 'culinarium/online'), GRUND = path.join(PROBE, 'culinarium/grundlage');
  const sha = f => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
  const seiten = fs.readdirSync(GRUND).filter(f => f.endsWith('.html'));
  const vorher = Object.fromEntries(seiten.map(f => [f, sha(path.join(ONLINE, f))]));
  const WEB = path.resolve(BUREAU, '../../website');   // die echte Website: wird nie beschrieben (10a «Demo-Sperre»: Prüfsumme vor und nach jedem Schreibweg)
  const webSumme = () => crypto.createHash('sha256').update(fs.readdirSync(WEB).filter(f => f.endsWith('.html')).sort().concat(['assets/buchen.js']).map(f => f + ':' + sha(path.join(WEB, f))).join('|')).digest('hex');
  const webVorher = webSumme();
  const br = await pw[MOTOR].launch({ headless: true });
  const ctx = await br.newContext({ viewport: { width: BREITE, height: HOEHE }, deviceScaleFactor: 1, acceptDownloads: false });
  const p = await ctx.newPage(); const konsole = [];
  p.on('console', m => { if (m.type() === 'error' && !/409 \(Conflict\)|status of 4(09|13|22)|Failed to load resource/.test(m.text())) konsole.push(m.text()); });
  p.on('pageerror', e => konsole.push('SEITE: ' + e.message));
  p.on('dialog', d => d.accept());
  if (process.env.LAUT) { p.on('request', r => { if (r.method() === 'POST') console.log('REQ', r.url(), (r.postData() || '').slice(0, 300)); }); p.on('response', async r => { if (r.request().method() === 'POST') console.log('ANT', r.status(), (await r.text().catch(() => '')).slice(0, 300)); }); }
  const bild = async name => p.screenshot({ path: path.join(BILDER, `bedienen-${MOTOR}-${BREITE}x${HOEHE}-${name}.png`) });
  const ueberlauf = async was => pruef(await p.evaluate(b => document.documentElement.scrollWidth <= b + 1, BREITE), `${was}: kein seitliches Verrutschen bei ${BREITE}`);
  const geh = async (ansicht, q = '') => { await p.goto('about:blank'); await p.goto(B + '/_werkzeuge/bureau/?ansicht=' + encodeURIComponent(ansicht) + q, { waitUntil: 'load', timeout: 60000 }); await bis(() => p.evaluate(a => document.querySelector('#ws-mitte').getAttribute('data-ws-bereit') === a, ansicht), 15000); };
  const rand = async () => { if (BREITE < 900) { const k = p.locator('[data-wo-rand-knopf]'); if (await k.count() && (await k.getAttribute('aria-expanded')) !== 'true') await k.click(); } };
  const speichern = async () => { await p.locator('#ws-speichern').click(); await bis(() => p.locator('[data-ws-quittung], [data-ws-meldung]').count(), 10000); };
  const stand = async () => (await fetch(B + '/api/x/website/stand/culinarium')).json();
  try {
    // ---------------- Übersicht, Rahmen
    await geh('start');
    await warte(800);
    const wn = await p.evaluate(() => WO_HAUS.namen.website);
    pruef(await p.locator('.wo-kopf .wo-marke-w b, .wo-kopf b').first().textContent().then(t => t.includes(wn)).catch(() => false), 'R05 Kopf: Name des Werkzeugs aus der einen Stelle (' + wn + ')');
    pruef(await p.locator('[data-ws-anleitung]').count() === 1, 'Startbild: Knopf «Anleitung»');
    const anl = await fetch(B + '/_werkzeuge/bureau/anleitung.html'); pruef(anl.ok, 'Anleitung antwortet (200)', anl.status);
    pruef(await p.locator('.wo-aufg > .wo-ag').count() === 7, 'Häufig gebraucht: sieben Kacheln (4 + 3), «Neuer Abend» zuerst', await p.locator('.wo-aufg > .wo-ag').count());
    const bkb = await p.evaluate(() => [...document.querySelectorAll('.wo-ber .wo-bk__b img')].map(i => i.getBoundingClientRect().width > 40));
    pruef(bkb.length === 8 && bkb.every(Boolean), 'Bereiche: acht Kacheln, jede mit sichtbarem Foto (Fehlerbuch «Bilder in jeder Liste»)', JSON.stringify(bkb));
    pruef(!(await p.locator('#ws-raus').count()) && !(await p.locator('#ws-vgl').count()), 'Leiste: ohne Entwurf keine ausgegrauten Knöpfe (nur Speichern)');
    pruef(await p.locator('#ws-speichern[data-ws-lage="ruhig"]').count() === 1, 'R09 Speichern-Knopf sichtbar, ruhig');
    await ueberlauf('Übersicht'); await bild('uebersicht');
    // ---------------- Angaben des Hauses (E)
    await geh('angaben');
    const tel = p.locator('[data-ws-angabe="telefon"]');
    pruef(await tel.inputValue() === '+49 163 3909578', 'E Telefon steht mit dem Wert der Website');
    pruef(/Steht an \d+ Stellen und als \d+ Links auf \d+ Seiten/.test(await p.locator('.ws-ang__lage').first().textContent()), 'E «steht n× auf m Seiten» bei Telefon');
    await tel.fill('+49 163 3909599');
    pruef(/1 Eingabe/.test(await p.locator('#ws-leiste').textContent()), 'R10 Eingabe wartet gelb («1 Eingabe noch nicht gespeichert»)');
    pruef(await p.locator('#ws-speichern[data-ws-lage="offen"]').count() === 1, 'R09 Speichern-Knopf gelb bei offener Eingabe');
    const igc = p.locator('[data-ws-angabe="ig-culinariumhannover"]'); await igc.fill('instagram ohne https');
    pruef(await p.locator('.ws-ang__warn:not([hidden])').count() >= 1, 'E Prüfung beim Tippen: Link ohne https:// wird gemeldet');
    await igc.fill('https://www.instagram.com/culinarium_hannover/');
    await speichern(); await warte(600);
    if (process.env.LAUT) console.log('QUITT', await p.locator('#ws-quittung').innerHTML(), await p.locator('#ws-leiste').textContent());
    pruef(await p.locator('[data-ws-quittung]').count() === 1, 'R11 Quittung nach dem Speichern');
    pruef(await p.locator('#ws-speichern[data-ws-lage="gespeichert"]').count() === 1, 'R09 Speichern-Knopf grün «Gespeichert»');
    let st = await stand();
    if (process.env.LAUT) console.log('STAND', st.offen, st.aenderungen.length, JSON.stringify(st.aenderungen.slice(0,3)));
    pruef(st.aenderungen.filter(a => a.art === 'text').length >= 9 && st.aenderungen.filter(a => a.art === 'link').length >= 9, 'E Telefon an allen Stellen und in allen Links zum Anrufen geändert', st.aenderungen.length);
    await geh('angaben');
    pruef(await p.locator('[data-ws-angabe="telefon"]').inputValue() === '+49 163 3909599', 'Speichern → neu laden → noch da (Telefon)');
    const r422 = await fetch(B + '/api/x/website/aendern/culinarium', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: B }, body: JSON.stringify({ ops: [{ art: 'angabe', key: 'telefon', neu: 'kein telefon' }], erwartet: st.kennung }) });
    pruef(r422.status === 422 && (await r422.json()).stichwort === 'angabe-telefon', 'E Server weist ungültiges Telefon ab (422, Stichwort)');
    // Ungewöhnliche Eingaben: <script>, Emoji, Umlaute, 5000 Zeichen, leer
    const ruhe = p.locator('[data-ws-angabe="ort"]');
    await ruhe.fill('<script>alert(1)</script> 30449 Hannover 🍷 Ä Ö Ü');
    await speichern(); await warte(500);
    const wegs = await (await fetch(B + '/api/x/website/vorschau/culinarium/entwurf/de/weg.html')).json();
    pruef(!/<script>alert\(1\)/.test(wegs.html) && /🍷 Ä Ö Ü/.test(wegs.html), 'Ungewöhnlich: <script> kommt nicht auf die Seite, Emoji und Umlaute schon');
    await ruhe.fill(''); await speichern(); await warte(400);
    pruef(await p.locator('[data-ws-meldung="leer"]').count() >= 1, 'Ungewöhnlich: leeres Feld wird mit Stichwort abgewiesen');
    await geh('angaben');
    await p.locator('[data-ws-angabe="ort"]').fill('x'.repeat(5000)); await speichern(); await warte(400);
    pruef(await p.locator('[data-ws-meldung="zu-lang"]').count() >= 1, 'Ungewöhnlich: 5000 Zeichen werden mit Stichwort abgewiesen');
    await geh('angaben'); await p.locator('[data-ws-angabe="ort"]').fill('30449 Hannover');
    if (await p.locator('#ws-speichern[data-ws-lage="offen"]').count()) await speichern();
    await ueberlauf('Angaben'); await bild('angaben');
    // ---------------- Google-Texte (I)
    await geh('google');
    const gt = p.locator('[data-ws-seo="abend.html"] [data-ws-gt="titel"]');
    await gt.fill('Der Abend · Culinarium Hannover-Linden');
    pruef(/^\d+ \/ 60$/.test(await p.locator('[data-ws-seo="abend.html"] .ws-gt__zahl').first().textContent()), 'I Zähler 60 beim Titel');
    pruef(/Der Abend · Culinarium/.test(await p.locator('[data-ws-seo="abend.html"] .ws-gt__vt').textContent()), 'I Vorschau wie bei Google schreibt mit');
    await speichern(); await warte(400);
    await geh('google');
    pruef(await p.locator('[data-ws-seo="abend.html"] [data-ws-gt="titel"]').inputValue() === 'Der Abend · Culinarium Hannover-Linden', 'Speichern → neu laden → noch da (Google-Titel)');
    const gb = await p.evaluate(() => [...document.querySelectorAll('.ws-gt__bild img')].map(i => i.getAttribute('src')));
    pruef(gb.length === 9 && new Set(gb).size === 9, 'I jede Seite mit eigenem Foto, keins doppelt', gb.length + '/' + new Set(gb).size);
    await ueberlauf('Google-Texte'); await bild('google');
    // ---------------- Foto tauschen und eigenes Foto hochladen (D)
    await geh('haus:abende');
    const ein = p.locator('details.ws-eintrag').nth(1); await ein.locator('summary').click(); await warte(400);
    await ein.locator('button.ws-foto').first().click({ force: true });
    await bis(() => p.locator('[data-ws-fenster="bild"]').count());
    pruef(await p.locator('[data-ws-fenster="bild"] .ws-fwahl').count() > 50, 'D Foto tauschen: Fotos des Hauses zur Wahl');
    const jpg = n => path.join(DATEN, n);
    execFileSync('python3', ['-c', `from PIL import Image\nImage.new('RGB',(1600,1067),(125,67,58)).save('${jpg('gross.jpg')}',quality=90)\nImage.new('RGB',(400,300),(125,67,58)).save('${jpg('klein.jpg')}')\nopen('${jpg('text.jpg')}','w').write('kein bild')`]);
    await p.locator('#ws-hoch').setInputFiles(jpg('klein.jpg'));
    await bis(() => p.locator('[data-ws-meldung="bild-klein"]').count());
    pruef(await p.locator('[data-ws-meldung="bild-klein"]').count() === 1, 'D Foto mit 400 px wird abgewiesen (Stichwort bild-klein)');
    await p.locator('#ws-hoch').setInputFiles({ name: 'brief.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.4') });
    pruef(await bis(() => p.locator('[data-ws-meldung="bild-art"]').count()), 'D Datei ohne Bild wird abgewiesen (Stichwort bild-art)');
    await p.locator('#ws-hoch').setInputFiles({ name: 'riesig.jpg', mimeType: 'image/jpeg', buffer: Buffer.alloc(30 * 1024 * 1024) });
    pruef(await bis(() => p.locator('[data-ws-meldung="bild-gross"]').count()), 'D Foto mit 30 MB wird schon im Browser abgewiesen (S03)');
    await p.locator('#ws-hoch').setInputFiles({ name: 'falsch.jpg', mimeType: 'image/jpeg', buffer: fs.readFileSync(jpg('text.jpg')) });
    pruef(await bis(() => p.locator('[data-ws-meldung="bild-art"]').count() >= 2 || p.locator('[data-ws-meldung="bild-art"]').count()), 'D Text mit Endung .jpg wird vom Server abgewiesen');
    await p.locator('#ws-hoch').setInputFiles(jpg('gross.jpg'));
    pruef(await bis(() => p.locator('.ws-hoch').textContent().then(t => /übernommen \(1600 auf 1067/.test(t)), 15000), 'D eigenes Foto hochgeladen, neu gesetzt (1600 auf 1067)');
    const eig = fs.readdirSync(path.join(DATEN, 'culinarium/website-fotos')).filter(f => f.endsWith('.webp'));
    pruef(eig.length === 4 && fs.existsSync(path.join(GRUND, 'assets/bild', eig[0])), 'D vier Liefergrössen als WebP, in der Kopie verteilt', eig.join(','));
    await bild('foto-fenster');
    await p.locator('[data-ws-fenster="bild"] .kn--d').click();
    pruef(await bis(() => p.locator('[data-ws-quittung]').count(), 8000), 'F27 Quittung nach Fototausch mit eigenem Foto (auch im Safari-Kern)');
    st = await stand();
    pruef(st.aenderungen.some(a => a.art === 'bild' && /^u-/.test(a.nachher)), 'D getauschtes Foto im Entwurf');
    // ---------------- Netz weg beim Speichern: Meldung, Eingabe bleibt
    await geh('angaben');
    await p.locator('[data-ws-angabe="strasse"]').fill('Haasemannstraße 15');
    await ctx.setOffline(true);
    await p.locator('#ws-speichern').click();
    pruef(await bis(() => p.locator('[data-ws-meldung="keine-verbindung"]').count()), 'Netz weg: Meldung «antwortet nicht» mit Stichwort');
    pruef(/1 Eingabe/.test(await p.locator('#ws-leiste').textContent()), 'Netz weg: Eingabe bleibt offen');
    await ctx.setOffline(false);
    await speichern(); await warte(400);
    await geh('angaben');
    pruef(await p.locator('[data-ws-ang-zurueck="strasse"]').count() === 1, 'E04 «Wie ursprünglich» bei geänderter Angabe');
    // ---------------- Termine (Culinarium): Daten aus website/assets/buchen.js, Entwurf, Leiste, Vorschau
    const T = async () => (await fetch(B + '/_werkzeuge/bureau/api/termine')).json();
    const buchen = async teil => (await fetch(B + teil + 'assets/buchen.js')).text();
    const ONL = '/werkzeuge/website/' + path.basename(PROBE) + '/culinarium/online/';
    const roh = fs.readFileSync(path.join(GRUND, 'assets/buchen.js'), 'utf8');
    await geh('e:termine');
    let tl = await T();
    pruef(tl.ursprung.length === 4 && await p.locator('.cu-t').count() === 4, 'Termine: die vier Abende aus buchen.js stehen da, nichts abgetippt', tl.ursprung.length);
    pruef(await p.locator('.cu-t .cu-pl').count() === 4, 'Termine: jeder Abend mit seinem Plakat (Bilder in jeder Liste)');
    pruef(await p.locator('[data-cu-termin="b4"] .cu-pl--voll').count() === 1, 'Termine: ausgebuchter Abend als ausgebucht gezeigt');
    pruef(await p.locator('#ws-rand [data-ws-nav="e:termine"]').count() === 1 || BREITE < 900, 'Termine im Rand unter «Das Haus»');
    await p.locator('[data-cu-termin="b1"] input[name="preis"]').fill('95');
    pruef(/1 Eingabe/.test(await p.locator('#ws-leiste').textContent()) && await p.locator('#ws-speichern[data-ws-lage="offen"]').count() === 1, 'Termine: Eingabe wartet gelb in der Leiste (R10)');
    pruef(await p.locator('[data-cu-termin="b1"].cu-t--offen').count() === 1, 'Termine: geänderte Karte markiert');
    await p.locator('[data-cu-neu]').click(); await warte(400);
    const neuId = await p.evaluate(() => [...document.querySelectorAll('.cu-t')].map(k => k.getAttribute('data-cu-termin')).find(i => /^n/.test(i)));
    pruef(!!neuId && await p.locator('.cu-t').count() === 5 && /Samstag, 26\. Dezember 2026 ab 17:00/.test(await p.locator(`[data-cu-termin="${neuId}"] .cu-t__wann`).textContent()), 'Termine: «Neuer Abend» schlägt eine Woche nach dem letzten vor, mit dessen Zeit', neuId);
    await p.locator(`[data-cu-termin="${neuId}"] input[name="plaetze"]`).fill('0');
    pruef(await p.locator(`[data-cu-termin="${neuId}"] .cu-t__fehler:not([hidden])`).count() === 1, 'Termine: 0 Plätze beim Tippen gemeldet');
    await p.locator('#ws-speichern').click(); await warte(700);
    pruef(await p.locator('[data-ws-meldung="termin-plaetze"]').count() >= 1, 'Termine: Server weist 0 Plätze ab (Stichwort termin-plaetze), nichts gespeichert', await p.locator('#ws-quittung').textContent());
    pruef((await T()).entwurf === null, 'Termine: nach Abweisung kein Entwurf');
    await p.locator(`[data-cu-termin="${neuId}"] input[name="plaetze"]`).fill('12');
    await p.locator('[data-cu-weg="b4"]').click(); await warte(300);
    await p.locator('#ws-speichern').click();
    pruef(await bis(() => p.locator('[data-cu-termine="gespeichert"]').count(), 8000), 'Termine: Quittung nach dem Speichern (R11) mit «Rückgängig»');
    tl = await T();
    pruef(tl.wartet && tl.entwurf.length === 4 && tl.entwurf.find(t => t.id === 'b1').preis === 95 && tl.entwurf.some(t => t.id === neuId && t.plaetze === 12) && !tl.entwurf.some(t => t.id === 'b4'), 'Termine: Entwurf mit Preis, neuem Abend, ohne den herausgenommenen');
    const nStamm = (await stand()).aenderungen.length;
    pruef(new RegExp('Entwurf: ' + (nStamm + 3) + ' Änderungen warten').test(await p.locator('#ws-leiste').textContent()) && await p.locator('#ws-raus').count() === 1, 'Termine: Leiste zählt die drei Termin-Änderungen zum Entwurf, «Veröffentlichen» da', await p.locator('#ws-leiste').textContent());
    await geh('e:termine');
    pruef(await p.locator('[data-cu-termin="b1"] input[name="preis"]').inputValue() === '95', 'Speichern → neu laden → noch da (Termin-Preis)');
    pruef(await p.locator('.cu-v__z[data-cu-v]').count() === 3, 'Termine: Vorher, nachher mit drei Zeilen (neu, geändert, entfällt)');
    const vsEntwurf = await buchen('/_werkzeuge/bureau/vorschau/'), vsOnline = await buchen(ONL);
    pruef(/preis: 95/.test(vsEntwurf) && vsEntwurf.includes(neuId) && vsOnline === roh, 'Termine: Vorschau zeigt den Entwurf, die Website noch den alten Stand');
    await p.locator('.cu-vs__rahmen').scrollIntoViewIfNeeded();   // Vorschau lädt erst im Bild (loading=lazy)
    pruef(await bis(() => p.evaluate(() => { try { return document.querySelector('.cu-vs__rahmen').contentDocument.querySelectorAll('.tb-p').length; } catch (e) { return 0; } }), 10000), 'Termine: Vorschau der Seite «Der Abend» zeichnet die Plakate');
    const k409 = await fetch(B + '/_werkzeuge/bureau/api/termine/speichern', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: B }, body: JSON.stringify({ termine: tl.entwurf, erwartet: 'alt' }) });
    pruef(k409.status === 409 && (await k409.json()).stichwort === 'konflikt', 'Termine: zweites Fenster mit altem Stand bekommt 409 KONFLIKT (L13)');
    const k400 = await fetch(B + '/_werkzeuge/bureau/api/termine/speichern', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: B }, body: JSON.stringify({ termine: [{ id: 'x', datum: '2026-02-30', zeit: '19:00', preis: 89, plaetze: 14 }], erwartet: tl.kennung }) });
    pruef(k400.status === 400 && (await k400.json()).stichwort === 'termin-datum', 'Termine: 30. Februar abgewiesen (termin-datum)');
    const kx = await fetch(B + '/_werkzeuge/bureau/api/termine/speichern', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: B }, body: JSON.stringify({ termine: [{ id: 'x', datum: '2026-12-01', zeit: '<script>', preis: 89, plaetze: 14 }], erwartet: tl.kennung }) });
    pruef(kx.status === 400, 'Termine: <script> als Uhrzeit abgewiesen');
    const kf = await fetch(B + '/_werkzeuge/bureau/api/termine/speichern', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://boese.example' }, body: '{}' });
    pruef(kf.status === 403, 'Termine: fremde Herkunft 403 (S01)');
    await ueberlauf('Termine'); await bild('termine');
    // ---------------- Vorher, nachher und Veröffentlichen
    await geh('entwurf');
    pruef(await p.locator('#ws-vgl').count() === 1 && await p.locator('#ws-raus').count() === 1, 'Leiste: mit Entwurf «Vorher, nachher» und «Veröffentlichen» da');
    pruef(await p.locator('[data-ws-eigen-entwurf="termine"] .ws-liste-klein p').count() === 3, 'Entwurf & Vergleich nennt die drei Termin-Änderungen mit Weg in die Ansicht');
    await bild('entwurf');
    await p.locator('#ws-raus').click();
    await bis(() => p.locator('[data-ws-fenster="veroeffentlichen"]').count());
    pruef(await p.locator('[data-ws-fenster="veroeffentlichen"] [data-ws-eigen="termine"] p').count() === 3, 'Veröffentlichen: Fenster nennt die drei Termin-Änderungen');
    await p.locator('#ws-notiz').fill('Abnahme Bureau');
    await p.locator('[data-ws-fenster="veroeffentlichen"] .kn--d').click();
    pruef(await bis(() => p.locator('[data-ws-veroeffentlicht]').count(), 30000), 'R12 «Ist online.» nach Veröffentlichen');
    const bOn = await buchen(ONL);
    pruef(/preis: 95/.test(bOn) && bOn.includes(neuId) && !/id: 'b4'|id: "b4"|\bid: b4\b/.test(bOn) && /culinarium-termine-vorschau-[0-9a-f]{12}/.test(bOn), 'Termine veröffentlicht: Website liefert die neuen Termine (eigener Schlüssel im Browser-Speicher)');
    pruef(!(await T()).wartet, 'Termine: nach dem Veröffentlichen wartet nichts mehr');
    const t0 = Date.now();
    const online = fs.readFileSync(path.join(ONLINE, 'weg.html'), 'utf8'), okarte = fs.readFileSync(path.join(ONLINE, 'abend.html'), 'utf8');
    pruef(/\+49 163 3909599/.test(online) && /tel:\+491633909599/.test(online) && /Haasemannstraße 15/.test(online), 'Veröffentlichen sichtbar auf der Probe-Kopie: Telefon, Link zum Anrufen, Strasse');
    pruef(/<title>Der Abend · Culinarium Hannover-Linden<\/title>/.test(okarte), 'Veröffentlichen: Google-Titel auf der Seite');
    pruef(/assets\/bild\/u-[0-9a-f]{12}-\d+\.webp/.test(fs.readFileSync(path.join(ONLINE, 'abende.html'), 'utf8')) && fs.readdirSync(path.join(ONLINE, 'assets/bild')).some(f => /^u-/.test(f)), 'Veröffentlichen: eigenes Foto auf der Seite und in der Kopie');
    const http = await (await fetch(B + '/werkzeuge/website/' + path.basename(PROBE) + '/culinarium/online/weg.html')).text();
    pruef(/\+49 163 3909599/.test(http) && Date.now() - t0 < 5000, 'Veröffentlichen: Seite liefert den neuen Stand innert 5 s');
    // ---------------- Frühere Fassungen: zurückholen
    await geh('verlauf');
    await bild('verlauf');
    const fass = p.locator('[data-ws-fassung]');
    pruef(await fass.count() >= 1, 'R14 Frühere Fassungen mit Datum und Notiz', await fass.count());
    pruef(/Ursprünglicher Stand/.test(await fass.last().textContent()), 'R14 «Ursprünglicher Stand» steht unten');
    pruef(!(await p.locator('#ws-wer').count()) && /Team Culinarium/.test(await p.locator('[data-ws-protokoll]').textContent()), 'Fehlerbuch: keine Namensabfrage, Protokoll mit «Team Culinarium»');
    await fass.last().locator('button', { hasText: 'Zurückholen' }).click();
    await bis(() => p.locator('.ws-fenster__blatt').count());
    await p.locator('.ws-fenster__blatt .kn--d').click();
    await bis(async () => (await stand()).offen, 8000);
    st = await stand();
    pruef(st.offen && st.aenderungen.length > 0, 'R14 Zurückholen legt in den Entwurf, nicht direkt online');
    pruef(fs.readFileSync(path.join(ONLINE, 'weg.html'), 'utf8').includes('+49 163 3909599'), 'R14 Website bleibt bis zum Veröffentlichen beim neuen Stand');
    await geh('entwurf'); await p.locator('#ws-raus').click(); await bis(() => p.locator('[data-ws-fenster="veroeffentlichen"]').count());
    await p.locator('[data-ws-fenster="veroeffentlichen"] .kn--d').click(); await bis(() => p.locator('[data-ws-veroeffentlicht]').count(), 30000);
    const nachher = Object.fromEntries(seiten.map(f => [f, sha(path.join(ONLINE, f))]));
    const anders = seiten.filter(f => nachher[f] !== vorher[f]);
    pruef(!anders.length, 'Zurückholen auf den Ursprung: alle 9 Seiten Byte für Byte wie vorher', anders.join(','));
    // ---------------- Termine: frühere Fassungen, Ursprung zurückholen → Byte für Byte
    await geh('e:termine');
    pruef(await p.locator('.cu-vl__z:not(.cu-vl__z--beispiel)').count() === 2 && /Ursprünglicher Stand/.test(await p.locator('.cu-vl__z').last().textContent()), 'Termine: frühere Fassung mit Notiz, unten «Ursprünglicher Stand» (R14)');
    await p.locator('[data-cu-holen="ursprung"]').click();
    pruef(await bis(async () => (await T()).wartet), 'Termine: Ursprung in den Entwurf geholt, nicht direkt online');
    pruef((await buchen(ONL)).includes(neuId), 'Termine: Website bleibt bis zum Veröffentlichen beim veröffentlichten Stand');
    await p.locator('#ws-raus').click(); await bis(() => p.locator('[data-ws-fenster="veroeffentlichen"]').count());
    await p.locator('[data-ws-fenster="veroeffentlichen"] .kn--d').click(); await bis(() => p.locator('[data-ws-veroeffentlicht]').count(), 30000);
    pruef(await buchen(ONL) === roh, 'Termine: Ursprung veröffentlicht → buchen.js Byte für Byte wie gebaut');
    await bild('termine-verlauf');
    // ---------------- Rundgang (R18)
    await p.goto(B + '/_werkzeuge/bureau/?ansicht=start&rundgang', { waitUntil: 'networkidle' });
    pruef(await bis(() => p.locator('.rdg-karte').count(), 25000), 'R18 Rundgang startet mit ?rundgang');
    let schritte = 0;
    while (await p.locator('.rdg-karte').count() && schritte < 8) { schritte++; if (schritte === 2) await bild('rundgang'); await p.locator('.rdg-karte .rdg-los').click(); await warte(500); }
    pruef(schritte >= 4 && schritte <= 5, 'R18 Rundgang: vier bis fünf Schritte, dann zu', schritte);
    // ---------------- Fehlermelder an den Server (R03)
    await p.evaluate(() => setTimeout(() => { throw new Error('Probe-Fehler aus der Abnahme'); }, 0)); await warte(800);
    const fl = await (await fetch(B + '/_werkzeuge/bureau/api/fehler')).json();
    pruef(fl.fehler.some(f => /Probe-Fehler aus der Abnahme/.test(f.text)), 'R03 Skriptfehler kommt beim Server an');
    // ---------------- Handy: Rand klappt zu nach der Wahl (R07)
    if (BREITE < 900) {
      await geh('start'); await rand();
      await p.locator('#ws-rand button[data-ws-nav="google"]').click(); await warte(700);
      pruef(!(await p.evaluate(() => document.documentElement.classList.contains('wo-rand-auf'))), 'R07 Handy: Rand schliesst sich nach der Wahl');
    }
    // ---------------- Sicherheit (S01–S03), mit dem Server dieses Laufs
    const fremd = await fetch(B + '/api/x/website/aendern/culinarium', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://boese.example' }, body: '{}' });
    pruef(fremd.status === 403, 'S01 fremde Herkunft 403', fremd.status);
    const gross = await fetch(B + '/api/x/website/aendern/culinarium', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: B }, body: 'x'.repeat(3_100_000) });
    pruef(gross.status === 413, 'S03 Anfrage über 3 MB 413', gross.status);
    pruef(webSumme() === webVorher || process.env.WEBSITE_BAUT, 'Echte Website unverändert (Prüfsumme aller Seiten und buchen.js vor und nach allen Schreibwegen)');
    const echt = konsole.filter(t => !/Probe-Fehler aus der Abnahme/.test(t));
    pruef(!echt.length, 'keine Fehler in der Konsole (ausser dem absichtlichen Probe-Fehler für R03)', echt.join(' | '));
  } catch (e) { pruef(false, 'Lauf ohne Abbruch', e.stack || e); }
  await br.close();
  srv.kill();
  fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true });
  if (rot.length && process.env.LAUT) console.log(serverText.slice(-3000));
  console.log((rot.length ? 'NICHT BESTANDEN · ' + rot.length + ' von ' : 'BESTANDEN · ') + n + ' Prüfungen · ' + MOTOR + ' ' + BREITE);
  process.exit(rot.length ? 1 : 0);
})();
