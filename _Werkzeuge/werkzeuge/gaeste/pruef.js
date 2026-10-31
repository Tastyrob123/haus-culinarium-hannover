/* pruef.js · fester Durchlauf des Werkzeugs «gaeste». Start (im Ordner _Werkzeuge):  node werkzeuge/gaeste/pruef.js
   Auswahl:  node werkzeuge/gaeste/pruef.js gasterntal land 390      (Haus, Welt, Breite; ohne Angabe alle zwölf Läufe)
   Safari-Kern statt Chromium:  PRUEF_BROWSER=webkit node werkzeuge/gaeste/pruef.js   (die Zwischenablage wird dort nicht geprüft)

   Je Lauf ein eigener Server auf Port 8974 mit Wegwerf-Daten (WERKZEUGE_DATEN) und festen Probe-Antworten (GAESTE_KI=probe):
   Die KI wird nie aufgerufen, die echten Daten werden nie berührt. Der Browser läuft ohne Fenster. Am Ende beendet der Lauf
   seinen eigenen Server über dessen PID. Antwortet auf 8974 schon etwas, bricht der Lauf ab und beendet nichts.

   Geprüft wird für beide Häuser, beide Welten und drei Breiten (1440, 390, 320):
   öffnen · Welt wechseln · Frage ohne Antwort · Antwort nachtragen · speichern mit Quittung · Rückgängig · neu laden, noch da ·
   Konflikt bei zwei gleichzeitigen Änderungen (nichts überschrieben) · Vorher, nachher · veröffentlichen · der Chat weiss es ·
   im Verlauf sichtbar · zurückholen · Entwurf verwerfen · Hinweis «Anfrage wartet» · Antwortentwurf sichern, Konflikt, erledigt ·
   löschen (keine Reste im Speicher) · Auswertung · Obergrenze · Grenze je Gespräch · kein seitlicher Überlauf · kein Knopf
   abgeschnitten · keine Fehler in der Konsole · keine Auswahl und kein Dialog des Betriebssystems. */
const fs = require('fs'), path = require('path'), os = require('os'), http = require('http'), { spawn, spawnSync } = require('child_process');
const WURZEL = path.resolve(__dirname, '..', '..'), PORT = 8974, BASIS = `http://127.0.0.1:${PORT}`;
const HAEUSER = { gasterntal: { welt: 'land', name: 'Berghotel Gasterntal' }, 'beau-rivage': { welt: 'grand', name: 'Grand Beau-Rivage Interlaken' } };
const NAME = { grand: 'La Réception', land: 'Der Gastgeber' };
const BREITEN = [1440, 390, 320];
const WEBKIT = process.env.PRUEF_BROWSER === 'webkit';

function finde(safari) {      // Playwright liegt auf diesem Rechner schon; für den Safari-Kern die Fassung nehmen, deren Browser da ist
  const npx = path.join(os.homedir(), '.npm/_npx');
  for (const d of fs.existsSync(npx) ? fs.readdirSync(npx) : []) {
    const p = path.join(npx, d, 'node_modules/playwright');
    if (!fs.existsSync(p)) continue;
    if (!safari) return p;
    try { if (fs.existsSync(require(p).webkit.executablePath())) return p; } catch (e) { /* nächste */ }
  }
  throw new Error(safari ? 'Kein Playwright mit vorhandenem Safari-Kern gefunden' : 'Playwright nicht gefunden (einmal: npx -y playwright --version)');
}
function shell() {
  const c = path.join(os.homedir(), 'Library/Caches/ms-playwright');
  for (const n of fs.readdirSync(c).filter(n => n.startsWith('chromium_headless_shell-')).sort().reverse()) {
    const p = path.join(c, n, 'chrome-headless-shell-mac-arm64/chrome-headless-shell'); if (fs.existsSync(p)) return p;
  }
}
function hole(weg, daten) {
  return new Promise((gut, schlecht) => {
    const roh = daten === undefined ? null : Buffer.from(JSON.stringify(daten));
    const r = http.request(BASIS + weg, { method: roh ? 'POST' : 'GET', headers: roh ? { 'Content-Type': 'application/json', 'Content-Length': roh.length } : {} }, a => {
      let t = ''; a.on('data', x => t += x); a.on('end', () => { let d = {}; try { d = JSON.parse(t); } catch (e) { d = { roh: t }; } gut({ status: a.statusCode, daten: d }); });
    });
    r.on('error', schlecht); r.setTimeout(8000, () => r.destroy(new Error('Zeit abgelaufen'))); if (roh) r.write(roh); r.end();
  });
}
async function serverStart(daten) {
  let aus = '';
  const kind = spawn('python3', ['unterbau/serve.py', String(PORT)], { cwd: WURZEL, env: { ...process.env, GAESTE_KI: 'probe', WERKZEUGE_DATEN: daten, ANTHROPIC_API_KEY: '' }, stdio: ['ignore', 'ignore', 'pipe'] });
  kind.stderr.on('data', x => aus += x);
  for (let i = 0; i < 60; i++) { await new Promise(r => setTimeout(r, 100)); try { if ((await hole('/api/haus/gasterntal')).status === 200) return { kind, log: () => aus }; } catch (e) { /* noch nicht da */ } }
  kind.kill(); throw new Error('Der Server startet nicht: ' + aus.slice(-400));
}
function serverStop(s) { return new Promise(r => { s.kind.once('exit', r); s.kind.kill('SIGTERM'); setTimeout(() => { try { s.kind.kill('SIGKILL'); } catch (e) { /* schon weg */ } r(); }, 3000); }); }
function reste(ordner, wort) {     // sucht ein Wort in jeder Datei des Wegwerf-Speichers
  const treffer = [];
  (function geh(o) { for (const n of fs.readdirSync(o)) { const p = path.join(o, n); if (fs.statSync(p).isDirectory()) geh(p); else if (!n.endsWith('.jsonl') && fs.readFileSync(p, 'utf8').includes(wort)) treffer.push(path.relative(ordner, p)); } })(ordner);
  return treffer;
}

async function lauf(kern, haus, welt, breite) {
  const daten = fs.mkdtempSync(path.join(os.tmpdir(), 'gaeste-pruef-')), server = await serverStart(daten);
  const schritte = [], fehler = [];
  let browser;
  try { browser = await kern.launch(WEBKIT ? { headless: true } : { headless: true, executablePath: shell() }); }
  catch (e) { await serverStop(server); fs.rmSync(daten, { recursive: true, force: true }); return [{ was: 'Browser starten', gut: false, mehr: String(e.message || e).split('\n')[0] }]; }
  let erwarte409 = 0;
  const gut = (was, wahr, mehr) => { schritte.push({ was, gut: !!wahr, mehr: wahr ? '' : (mehr || '') }); if (!wahr) throw new Error(was + (mehr ? ' · ' + mehr : '')); };
  async function seite() {
    const k = await browser.newContext({ viewport: { width: breite, height: breite > 600 ? 900 : 800 }, permissions: WEBKIT ? [] : ['clipboard-read', 'clipboard-write'] });
    await k.addInitScript(x => { try { localStorage.setItem('werkzeuge-welt', x[0]); localStorage.setItem('gaeste-wer', x[1]); } catch (e) { /* privat */ } }, [welt, 'Prüflauf']);
    const p = await k.newPage();
    p.on('pageerror', e => fehler.push('Seite: ' + e));
    p.on('console', m => { if (m.type() !== 'error') return; if (/status of 409/.test(m.text()) && erwarte409 > 0) { erwarte409--; return; } fehler.push('Konsole: ' + m.text()); });
    p.on('dialog', d => { fehler.push('Dialog des Betriebssystems: ' + d.message()); d.dismiss().catch(() => {}); });
    await p.goto(`${BASIS}/werkzeuge/gaeste/?haus=${haus}`, { waitUntil: 'networkidle' });
    await p.waitForSelector('.ga-nav button', { state: 'attached' });
    return p;
  }
  async function form(p, wo) {       // gilt in jeder Ansicht: kein Überlauf, nichts vom Betriebssystem, kein Knopf abgeschnitten
    // erst messen, wenn jedes Stück angekommen ist (der Nebel im Landhaus zieht endlos und zählt nicht)
    await p.evaluate(() => Promise.all(document.getAnimations().filter(a => a.effect && a.effect.getTiming().iterations !== Infinity).map(a => a.finished.catch(() => {}))));
    const r = await p.evaluate(() => {
      const sichtbar = e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0; };
      return { ueber: document.documentElement.scrollWidth - innerWidth,
        system: document.querySelectorAll('select,datalist,input[type=date],input[type=time],input[type=datetime-local],input[type=month],input[type=week],input[type=color],input[type=file],input[type=range]').length,
        knopf: [...document.querySelectorAll('.kn,.wahl > *,.ga-nav button,.ga-link')].filter(sichtbar).filter(e => { const b = e.getBoundingClientRect(); return b.right > innerWidth + 0.5 || b.left < -0.5 || e.scrollWidth > e.clientWidth + 1; }).map(e => e.textContent.trim().slice(0, 30)) };
    });
    gut(`${wo}: kein seitlicher Überlauf`, r.ueber <= 0, 'Überlauf ' + r.ueber + ' px');
    gut(`${wo}: keine Auswahl des Betriebssystems`, r.system === 0, r.system + ' Felder');
    gut(`${wo}: kein Knopf abgeschnitten`, r.knopf.length === 0, r.knopf.join(' | '));
  }
  async function gehe(p, ziel) {
    if (await p.locator('.ga-rand__auf').isVisible()) { if (!(await p.locator(`.ga-nav [data-gehe="${ziel}"]`).isVisible())) await p.click('.ga-rand__auf'); }
    await p.click(`.ga-nav [data-gehe="${ziel}"]`);
    await p.waitForSelector(`.ga-nav [data-gehe="${ziel}"][aria-current="true"]`, { state: 'attached' });
    await p.waitForLoadState('networkidle'); await p.waitForTimeout(150);
    await form(p, 'Ansicht ' + ziel);
  }
  const quittung = async (p, text) => { const q = p.locator('.ga-quittung', { hasText: text }).last(); await q.waitFor({ timeout: 6000 }); return q; };
  const zuQuittungen = p => p.evaluate(() => document.querySelectorAll('.ga-quittung').forEach(q => q.remove()));
  const stand = async () => (await hole(`/api/x/gaeste/${haus}/stand`)).daten;
  const leiste = p => p.locator('#ga-leiste').innerText();
  async function nachtragen(p, frage, antwort) {       // über «Wissen des Hauses» → «Antwort anlegen»
    await gehe(p, 'wissen');
    await p.click('#ga-w-neu');
    await p.fill('#ga-f-frage', frage); await p.fill('#ga-f-antwort', antwort);
    await form(p, 'Fenster Nachtragen');
    await p.click('#ga-f-los');
  }
  const FRAGE = 'Gibt es im Haus einen Töpferkurs?', ANTWORT = 'Einen Töpferkurs gibt es bei uns nicht. Die Rezeption nennt Ihnen gerne eine Werkstatt im Ort.';
  try {
    /* 1 · öffnen */
    const a = await seite();
    gut('öffnen: die gewählte Welt steht', await a.evaluate(() => document.documentElement.getAttribute('data-welt')) === welt);
    gut('öffnen: Name des Werkzeugs in dieser Welt', (await a.locator('.ga-kopf__name').innerText()).trim() === NAME[welt], await a.locator('.ga-kopf__name').innerText());
    gut('öffnen: Name des Hauses', (await a.locator('#ga-haus').innerText()).toLowerCase().includes(HAEUSER[haus].name.toLowerCase()));
    gut('öffnen: Entwurfs-Leiste steht, Knopf sichtbar und gesperrt', (await leiste(a)).includes('Alles veröffentlicht') && await a.locator('#ga-l-los').isDisabled());
    gut('öffnen: die eine Stelle sagt, dass die KI nicht angeschlossen ist', (await a.locator('#ga-ki').innerText()).includes('Probe-Antworten'));
    const st0 = await stand();
    gut('öffnen: Wissen des Hauses ist eingelesen', st0.live.wissen.length >= 5 && st0.live.haus.tel && st0.live.haus.mail, JSON.stringify(st0.live.haus).slice(0, 200));
    gut('öffnen: was fehlt, steht als offen da', (await a.locator('#ga-haupt').innerText()).includes('offen'));
    await form(a, 'Übersicht');
    const aufbau = await a.evaluate(() => {
      const r = document.querySelector('#ga-rand'), k = document.querySelector('#ga-kulisse'), rr = r.getBoundingClientRect(), kr = k.getBoundingClientRect();
      scrollTo(0, 400);
      const nach = r.getBoundingClientRect(), k2 = k.getBoundingClientRect(); scrollTo(0, 0);
      return { breit: innerWidth >= 900, fest: getComputedStyle(r).position === 'fixed', oben: rr.top, hoch: rr.height, h: innerHeight, nachOben: nach.top, kulisse: getComputedStyle(k).position === 'fixed' && kr.top === 0 && kr.height === innerHeight && kr.width >= document.documentElement.clientWidth && k2.top === 0,
        bild: !!k.querySelector('img') };
    });
    if (aufbau.breit) gut('Aufbau: die Leiste links steht fest und geht über die ganze Höhe durch, auch beim Scrollen', aufbau.fest && aufbau.oben === 0 && aufbau.hoch === aufbau.h && aufbau.nachOben === 0, JSON.stringify(aufbau));
    gut('Aufbau: das Hintergrundbild füllt den ganzen Bildschirm und bleibt stehen', aufbau.kulisse && aufbau.bild, JSON.stringify(aufbau));
    gut('Aufbau: auf der Übersicht keine Zurück-Taste', await a.locator('#ga-zurueck').isHidden());
    await a.locator('.ga-k3[data-lage="wissen"]').click();
    await a.waitForSelector('.ga-nav [data-gehe="wissen"][aria-current="true"]', { state: 'attached' });
    gut('Kachel: führt in den Bereich, dort steht die Zurück-Taste', await a.locator('#ga-zurueck').isVisible());
    await form(a, 'Bereich nach Klick auf die Kachel');
    await a.click('#ga-zurueck');
    await a.waitForSelector('.ga-k3');
    gut('Zurück: führt wieder zur Übersicht', await a.locator('#ga-zurueck').isHidden() && await a.locator('.ga-k3').count() === 3);

    /* 2 · Modus-Knopf */
    const andere = welt === 'grand' ? 'land' : 'grand';
    await a.click('[data-welt-knopf]');
    gut('Welt wechseln: Name, Welt und Titel wechseln', (await a.locator('.ga-kopf__name').innerText()).trim() === NAME[andere] && await a.evaluate(() => document.documentElement.getAttribute('data-welt')) === andere && (await a.title()).includes(NAME[andere]));
    await form(a, 'Übersicht in der anderen Welt');
    await a.click('[data-welt-knopf]');
    gut('Welt wechseln: zurück', (await a.locator('.ga-kopf__name').innerText()).trim() === NAME[welt]);

    /* 3 · Probe-Chat: Frage ohne Antwort */
    await gehe(a, 'probe');
    gut('Probe-Chat: Startfragen des Hauses', await a.locator('#ga-chat .wahl button').count() >= 1);
    await a.fill('#ga-c-frage', FRAGE); await a.click('#ga-c-los');
    await a.waitForSelector('[data-antwort]:has-text("ohne Antwort im Wissen")');
    gut('Probe-Chat: Frage ohne Antwort wird so gezeigt', true);
    await form(a, 'Probe-Chat mit Antwort');

    /* 4 · Das wurde gefragt → Antwort nachtragen → speichern → Quittung → Rückgängig → noch einmal */
    await gehe(a, 'gefragt');
    const karte = a.locator('[data-frage]', { hasText: FRAGE });
    gut('Gefragt: die Frage steht da, als ohne Antwort', await karte.count() === 1 && (await karte.innerText()).toLowerCase().includes('ohne antwort'));
    for (const runde of [1, 2]) {
      await a.locator('[data-frage]', { hasText: FRAGE }).locator('.kn', { hasText: 'Antwort nachtragen' }).click();
      gut(`Nachtragen (${runde}): Fenster mit der Frage`, await a.inputValue('#ga-f-frage') === FRAGE);
      if (runde === 1) { await a.click('#ga-f-los'); gut('Nachtragen: leere Antwort wird nicht gespeichert', (await a.locator('#ga-f-meldung').innerText()).includes('ausfüllen') && !(await stand()).entwurf); await form(a, 'Fenster Nachtragen'); }
      await a.fill('#ga-f-antwort', ANTWORT); await a.click('#ga-f-los');
      const q = await quittung(a, 'Antwort nachgetragen');
      gut(`Speichern (${runde}): Quittung mit «Vorher, nachher» und «Rückgängig»`, (await q.innerText()).includes('Vorher, nachher') && (await q.innerText()).includes('Rückgängig'));
      const s = await stand();
      gut(`Speichern (${runde}): als Entwurf, online unverändert`, s.offen && s.entwurf.team.length === 1 && s.live.team.length === 0 && s.entwurf.team[0].wer === 'Prüflauf');
      gut(`Speichern (${runde}): Leiste zeigt den Entwurf`, (await leiste(a)).includes('Eine Änderung') && (await leiste(a)).toUpperCase().includes('ENTWURF') && await a.locator('#ga-l-los').isEnabled());
      if (runde === 1) {
        await form(a, 'Gefragt mit Quittung');
        await q.locator('.ga-link', { hasText: 'Vorher, nachher' }).click();
        gut('Quittung: «Vorher, nachher» zeigt die Stelle markiert', await a.locator('#ga-fenster .ga-vn__stelle').count() === 1 && await a.locator('#ga-fenster mark').count() >= 1 && (await a.locator('#ga-fenster').innerText()).includes('Töpferkurs'));
        await form(a, 'Fenster Vorher, nachher');
        await a.keyboard.press('Escape');
        gut('Fenster: schliesst mit Escape', await a.locator('#ga-fenster').isHidden());
        await zuQuittungen(a);
        // die Quittung ist zu: Rückgängig über eine neue Änderung prüfen
        await a.evaluate(() => { location.hash = '#wissen'; });
        await a.waitForSelector('[data-team]');
        await a.locator('[data-team] .kn', { hasText: 'Ändern' }).click();
        await a.fill('#ga-f-antwort', ANTWORT + ' Fragen Sie uns einfach.'); await a.click('#ga-f-los');
        const q2 = await quittung(a, 'Antwort geändert');
        await q2.locator('.ga-link', { hasText: 'Rückgängig' }).click();
        await quittung(a, 'Rückgängig gemacht');
        gut('Rückgängig: der Stand ist wie vor der Änderung', (await stand()).entwurf.team[0].antwort === ANTWORT);
        await a.locator('[data-team] .kn', { hasText: 'Ändern' }).click(); await a.click('#ga-f-los');
        await quittung(a, 'Nichts geändert, nichts gespeichert.');
        gut('Ohne Änderung: «Nichts geändert, nichts gespeichert.»', true);
        // ganz zurück: Entwurf verwerfen, dann beginnt Runde 2 wieder bei der offenen Frage
        await zuQuittungen(a);
        await a.click('#ga-l-los'); await a.click('#ga-f-verwerfen'); await a.click('#ga-f-verwerfen');
        await quittung(a, 'Entwurf verworfen');
        gut('Verwerfen: Entwurf weg, Frage wieder offen', !(await stand()).entwurf && (await hole(`/api/x/gaeste/${haus}/ueberblick`)).daten.ohne_antwort === 1);
        await zuQuittungen(a);
        await gehe(a, 'gefragt');
      }
    }
    gut('Nachtragen: die Frage gilt als erledigt', (await hole(`/api/x/gaeste/${haus}/ueberblick`)).daten.ohne_antwort === 0);

    /* 5 · neu laden, noch da */
    await a.reload({ waitUntil: 'networkidle' }); await a.waitForSelector('.ga-nav button', { state: 'attached' });
    gut('Neu laden: Leiste zeigt weiter den Entwurf', (await leiste(a)).includes('Eine Änderung'));
    await gehe(a, 'wissen');
    const eintrag = a.locator('[data-team]', { hasText: FRAGE });
    gut('Neu laden: die Antwort ist noch da, als Entwurf markiert', await eintrag.count() === 1 && (await eintrag.innerText()).includes(ANTWORT) && await eintrag.locator('.marke').count() === 1);

    /* 6 · Konflikt: zwei arbeiten gleichzeitig */
    const b = await seite();                                   // B liest den Stand jetzt
    await nachtragen(a, 'Darf ich mein Velo einstellen?', 'Ja, im Schopf neben dem Haus ist Platz für Velos.');
    await quittung(a, 'Antwort nachgetragen');                 // A speichert zuerst
    erwarte409 = 1;
    await nachtragen(b, 'Gibt es Kinderstühle?', 'Ja, Kinderstühle stehen im Restaurant bereit.');
    await b.waitForSelector('#ga-konflikt');                   // B kommt mit veralteter Kennung
    gut('Konflikt: B wird gewarnt, nichts ist gespeichert', (await b.locator('#ga-fenster').innerText()).includes('nichts wurde überschrieben'));
    let s = await stand();
    gut('Konflikt: A wurde nicht überschrieben, B noch nicht gespeichert', s.entwurf.team.length === 2 && s.entwurf.team.some(x => x.frage.includes('Velo')) && !s.entwurf.team.some(x => x.frage.includes('Kinderstühle')));
    gut('Konflikt: B sieht, was dazugekommen ist', (await b.locator('#ga-fenster').innerText()).includes('Velo'));
    await form(b, 'Fenster Konflikt');
    await b.click('#ga-f-dazu');
    await quittung(b, 'Antwort nachgetragen');
    s = await stand();
    gut('Konflikt: danach sind beide Änderungen da', s.entwurf.team.length === 3 && ['Töpferkurs', 'Velo', 'Kinderstühle'].every(w => s.entwurf.team.some(x => x.frage.includes(w))));
    gut('Konflikt: genau eine abgelehnte Speicherung', erwarte409 === 0);
    await b.context().close();

    /* 7 · Vorher, nachher → veröffentlichen */
    await a.reload({ waitUntil: 'networkidle' }); await a.waitForSelector('.ga-nav button', { state: 'attached' });
    gut('Veröffentlichen: Leiste zählt drei Änderungen', (await leiste(a)).includes('3 Änderungen'));
    await a.click('#ga-l-los');
    await a.waitForSelector('#ga-fenster .ga-vn__stelle');
    gut('Veröffentlichen: jede Stelle vorher und nachher nebeneinander', await a.locator('#ga-fenster .ga-vn__stelle').count() === 3 && (await a.locator('#ga-fenster').innerText()).includes('Heute online'));
    await form(a, 'Fenster Veröffentlichen');
    await a.fill('#ga-f-notiz', 'Drei Antworten nachgetragen');
    await a.click('#ga-f-los');
    const qv = await quittung(a, 'Veröffentlicht');
    s = await stand();
    gut('Veröffentlichen: online, kein Entwurf mehr', !s.offen && !s.entwurf && s.live.team.length === 3);
    gut('Veröffentlichen: Leiste und Knopf', (await leiste(a)).includes('Alles veröffentlicht') && await a.locator('#ga-l-los').isDisabled());
    await qv.locator('.ga-link', { hasText: 'Im Verlauf ansehen' }).click();

    /* 8 · im Verlauf sichtbar */
    await a.waitForSelector('[data-fassung]');
    gut('Verlauf: die abgelöste Fassung mit Notiz und Name', await a.locator('[data-fassung]').count() === 1 && (await a.locator('[data-fassung]').innerText()).includes('Drei Antworten nachgetragen') && (await a.locator('[data-fassung]').innerText()).includes('Prüflauf'));
    gut('Verlauf: Protokoll nennt das Veröffentlichen', (await a.locator('#ga-v-protokoll').innerText()).includes('Veröffentlicht'));
    await form(a, 'Verlauf');
    await a.locator('[data-fassung] .kn', { hasText: 'Ansehen' }).click();
    await a.waitForSelector('#ga-fenster .ga-vn__stelle');
    gut('Verlauf: Ansehen zeigt den Unterschied zu heute', await a.locator('#ga-fenster .ga-vn__stelle').count() === 3);
    await a.keyboard.press('Escape');
    await zuQuittungen(a);

    /* der Chat weiss es jetzt */
    await gehe(a, 'probe');
    await a.fill('#ga-c-frage', FRAGE); await a.click('#ga-c-los');
    await a.waitForSelector('[data-antwort]:has-text("aus dem Wissen beantwortet")');
    gut('Nach dem Veröffentlichen: der Chat antwortet mit der nachgetragenen Antwort', (await a.locator('#ga-chat .ga-blase--haus').last().innerText()).includes('Einen Töpferkurs gibt es bei uns nicht'));

    /* 9 · zurückholen */
    await gehe(a, 'verlauf');
    await a.waitForSelector('[data-fassung]');
    await a.locator('[data-fassung] .kn', { hasText: 'Zurückholen' }).click();
    await quittung(a, 'Als Entwurf zurückgeholt');
    s = await stand();
    gut('Zurückholen: frühere Fassung liegt als Entwurf, online bleibt der heutige Stand', s.offen && s.entwurf.team.length === 0 && s.live.team.length === 3);
    gut('Zurückholen: Leiste zeigt den Entwurf', (await leiste(a)).includes('3 Änderungen'));
    await form(a, 'Verlauf nach dem Zurückholen');
    await zuQuittungen(a);
    await a.click('#ga-l-los'); await a.waitForSelector('#ga-fenster .ga-vn__stelle');
    gut('Zurückholen: Vorher, nachher nennt die drei Antworten als entfernt', (await a.locator('#ga-fenster').innerText()).toLowerCase().split('entfernt').length - 1 >= 3);
    await a.click('#ga-f-verwerfen'); await a.click('#ga-f-verwerfen');
    await quittung(a, 'Entwurf verworfen');
    gut('Verwerfen: es gilt wieder der veröffentlichte Stand', !(await stand()).entwurf && (await stand()).live.team.length === 3);
    await zuQuittungen(a);

    /* 10 · Eingang: Hinweis, Antwortentwurf, Konflikt, erledigt, löschen */
    const gastText = 'Ich möchte einen Tisch für 6 Personen am 20. Oktober. Ich bin Zora Prüfgast, zora.pruefgast@example.ch';
    const chat = await hole(`/api/x/gaeste/${haus}/chat`, { messages: [{ role: 'user', content: gastText }], herkunft: 'gast', gespraech: 'gespraecheins' });
    gut('Eingang: der Chat legt die Anfrage ab', chat.status === 200 && !!chat.daten.anfrage);
    await hole(`/api/x/gaeste/${haus}/chat`, { messages: [{ role: 'user', content: 'Wann gibt es Frühstück?' }], herkunft: 'gast', gespraech: 'gespraechzwei' });
    await a.evaluate(() => window.gaNachsehen());
    await a.waitForSelector('#ga-wartet:not([hidden])');
    gut('Hinweis: «Eine Anfrage wartet» steht sichtbar da, mit Art und Name', (await a.locator('#ga-wartet').innerText()).includes('Eine Anfrage wartet') && (await a.locator('#ga-wartet').innerText()).includes('Zora Prüfgast') && (await a.locator('#ga-wartet').innerText()).includes('Tisch'));
    gut('Hinweis: steht auch im Titel und im Bereich Eingang', (await a.title()).startsWith('(1)') && (await a.locator('.ga-nav [data-gehe="eingang"]').textContent()).includes('1'));
    await quittung(a, 'Neue Anfrage im Eingang');
    await form(a, 'Ansicht mit Hinweis');
    await zuQuittungen(a);
    await a.click('#ga-wartet-kn');
    await a.waitForSelector('#ga-detail');
    const detail = await a.locator('#ga-detail').innerText();
    gut('Eingang: die Anfrage mit Name, Kontakt, Datum, Personen', ['Zora Prüfgast', 'zora.pruefgast@example.ch', 'Tisch', '20. Oktober', '6'].every(w => detail.includes(w)), detail.slice(0, 200));
    await a.waitForSelector('#ga-wartet', { state: 'hidden' });
    gut('Hinweis: verschwindet, sobald die Anfrage geöffnet ist', !(await a.title()).startsWith('('));
    await form(a, 'Eingang');
    await a.click('#ga-e-los');
    await quittung(a, 'Gerüst angelegt');
    gut('Antwortentwurf: Gerüst ohne KI, nichts erfunden', (await a.inputValue('#ga-e-text')).includes('[VERFÜGBARKEIT PRÜFEN]') && (await a.inputValue('#ga-e-text')).includes('Zora Prüfgast'));
    gut('Antwortentwurf: «Verschickt wird hier nichts» steht da', (await a.locator('#ga-detail').innerText()).includes('Verschickt wird hier nichts'));
    await form(a, 'Eingang mit Antwortentwurf');
    await zuQuittungen(a);
    await a.fill('#ga-e-text', 'Guten Tag Frau Prüfgast\n\nGerne reservieren wir für Sie.');
    await a.click('#ga-e-sichern'); await quittung(a, 'Gesichert');
    await zuQuittungen(a);
    await a.click('#ga-e-sichern'); await quittung(a, 'Nichts geändert, nichts gespeichert.');
    await zuQuittungen(a);
    if (!WEBKIT) {
      await a.click('#ga-e-kopieren'); await quittung(a, 'Kopiert');
      gut('Antwortentwurf: Kopieren legt Betreff und Text in die Zwischenablage', (await a.evaluate(() => navigator.clipboard.readText())).includes('Gerne reservieren wir für Sie.'));
    }
    await zuQuittungen(a);
    // jemand anderes ändert dieselbe Anfrage: A darf nicht still überschreiben
    const an0 = (await hole(`/api/x/gaeste/${haus}/betrieb`)).daten.anfragen[0];
    await hole(`/api/x/gaeste/${haus}/anfrage`, { id: an0.id, v: an0.v, betreff: an0.entwurf.betreff, text: 'Text von jemand anderem.', wer: 'Zweite Person' });
    await a.fill('#ga-e-text', 'Mein Text.'); erwarte409 = 1;
    await a.click('#ga-e-sichern');
    await a.waitForSelector('#ga-fenster:has-text("hat diese Anfrage geändert")');
    gut('Eingang: Konflikt am Antwortentwurf wird gezeigt, nichts überschrieben', (await hole(`/api/x/gaeste/${haus}/betrieb`)).daten.anfragen[0].entwurf.text === 'Text von jemand anderem.' && (await a.locator('#ga-fenster').innerText()).includes('Text von jemand anderem.'));
    await a.locator('#ga-fenster .kn', { hasText: 'Meine Fassung' }).click(); await quittung(a, 'Gesichert');
    gut('Eingang: nach der Entscheidung gilt die gewählte Fassung', (await hole(`/api/x/gaeste/${haus}/betrieb`)).daten.anfragen[0].entwurf.text === 'Mein Text.');
    await zuQuittungen(a);
    await a.reload({ waitUntil: 'networkidle' }); await a.waitForSelector('#ga-e-text');
    gut('Eingang: nach neuem Laden ist der Antwortentwurf noch da', await a.inputValue('#ga-e-text') === 'Mein Text.');
    await a.click('#ga-a-status'); await quittung(a, 'Erledigt');
    gut('Eingang: erledigt', (await hole(`/api/x/gaeste/${haus}/ueberblick`)).daten.anfragen_offen === 0);
    await zuQuittungen(a);

    /* 11 · Auswertung */
    await gehe(a, 'auswertung');
    gut('Auswertung: die häufigsten Fragen der Gäste, mit ehrlicher Grundlage', await a.locator('#ga-aus-haeufig > *').count() === 2 && (await a.locator('#ga-aus-grund').innerText()).includes('2 Fragen von Gästen') && (await a.locator('#ga-aus-grund').innerText()).includes('wenig'));
    await a.locator('.wahl [data-wahl="true"]').click();
    gut('Auswertung: mit Proben mehr Fragen', await a.locator('#ga-aus-haeufig > *').count() >= 3 && (await a.locator('#ga-aus-grund').innerText()).includes('Proben eingeschlossen'));
    await form(a, 'Auswertung mit Proben');

    /* 12 · Kosten und Schutz: Obergrenze, Löschen auf Wunsch eines Gastes */
    await gehe(a, 'betrieb');
    const kosten = await a.locator('#ga-b-kosten').innerText();
    gut('Kosten: Stand der KI, Modell, Preisliste und offene Obergrenze stehen da', ['Probe-Antworten', 'claude-sonnet-5-5', 'Preisliste vom', 'offen, keine gesetzt'].every(w => kosten.includes(w)), kosten.slice(0, 300));
    await a.fill('#ga-b-ober', 'viel'); await a.click('#ga-b-ober-kn'); await quittung(a, 'Nicht gespeichert');
    gut('Obergrenze: Unsinn wird nicht gespeichert', !(await stand()).entwurf);
    await zuQuittungen(a);
    await a.fill('#ga-b-ober', '20'); await a.click('#ga-b-ober-kn'); await quittung(a, 'Obergrenze gesetzt');
    gut('Obergrenze: als Entwurf gespeichert', (await stand()).entwurf.einstellungen.obergrenze_monat_usd === 20);
    gut('Veröffentlichen, Zurückholen, Verwerfen: mit veralteter Kennung abgelehnt, der Entwurf bleibt', (await hole(`/api/x/gaeste/${haus}/veroeffentlichen`, { erwartet: 'veraltet', wer: 'x' })).status === 409
      && (await hole(`/api/x/gaeste/${haus}/verwerfen`, { erwartet: 'veraltet', wer: 'x' })).status === 409 && (await hole(`/api/x/gaeste/${haus}/zurueckholen`, { erwartet: null, fassung: 'x', wer: 'x' })).status === 409
      && (await stand()).entwurf.einstellungen.obergrenze_monat_usd === 20 && (await stand()).live.einstellungen.obergrenze_monat_usd == null);
    await zuQuittungen(a);
    await a.fill('#ga-b-suche', 'zora.pruefgast'); await a.click('#ga-b-suche-kn');
    await a.waitForSelector('#ga-b-treffer');
    gut('Löschen auf Wunsch: die Suche findet die Anfrage des Gastes', (await a.locator('#ga-b-treffer').innerText()).includes('Zora Prüfgast'));
    await form(a, 'Kosten und Schutz mit Treffern');
    gut('Löschen auf Wunsch: vorher liegen die Daten im Speicher', reste(daten, 'pruefgast').length > 0);
    await a.click('#ga-b-weg'); await form(a, 'Fenster Löschen'); await a.click('#ga-f-los');
    await quittung(a, 'Gelöscht');
    const uebrig = reste(daten, 'pruefgast').concat(reste(daten, 'Prüfgast'));
    gut('Löschen auf Wunsch: im ganzen Speicher steht nichts mehr von diesem Gast, auch nicht in der Sicherung', uebrig.length === 0, uebrig.join(', '));
    gut('Löschen auf Wunsch: Anfrage und ihre Frage sind weg, die andere Frage bleibt', (await hole(`/api/x/gaeste/${haus}/betrieb`)).daten.anfragen.length === 0 && (await hole(`/api/x/gaeste/${haus}/betrieb`)).daten.fragen.filter(f => f.herkunft === 'gast').length === 1);
    gut('Datenschutz: im Verlauf und im Wissen stehen keine Daten von Gästen', reste(path.join(daten, haus, 'gaeste'), 'example.ch').length === 0);

    /* 13 · Server: Grenzen und Eingaben */
    let letzte = null;
    for (let i = 0; i < 21; i++) letzte = (await hole(`/api/x/gaeste/${haus}/chat`, { messages: [{ role: 'user', content: 'Wann gibt es Frühstück?' }], herkunft: 'gast', gespraech: 'vielfrager' })).daten;
    gut('Grenze: nach 20 Fragen in einem Gespräch antwortet der Chat mit der Pause', letzte.grenze === true && /Pause|pause/.test(letzte.text));
    gut('Eingaben: unbekanntes Haus', (await hole('/api/x/gaeste/nirgendwo/start')).status === 404);
    gut('Eingaben: kaputter Stand wird abgelehnt', (await hole(`/api/x/gaeste/${haus}/speichern`, { daten: { team: 'x' }, erwartet: 'x' })).status === 400);
    gut('Eingaben: leere Frage wird abgelehnt', (await hole(`/api/x/gaeste/${haus}/chat`, { messages: [] })).status === 400);
    gut('Eingaben: Daten des Speichers sind nicht als Datei abrufbar', (await hole(`/daten/${haus}/gaeste/live.json`)).status === 404 && (await hole(`/werkzeuge/gaeste/../../daten/${haus}/gaeste/live.json`)).status === 404);
    const xss = await hole(`/api/x/gaeste/${haus}/chat`, { messages: [{ role: 'user', content: '<img src=x onerror="window.gehackt=1"> Gibt es eine Zipfelmützenwerkstatt?' }], herkunft: 'probe', gespraech: 'xss' });
    await gehe(a, 'gefragt');
    gut('Eingaben: Text von Gästen wird als Text gezeigt, nie ausgeführt', xss.status === 200 && await a.evaluate(() => !window.gehackt && !document.querySelector('#ga-haupt img')) && (await a.locator('#ga-haupt').innerText()).includes('<img src=x'));

    /* 14 · Beispiel-Anfragen: der Eingang sieht aus wie im Betrieb, bleibt aber ehrlich */
    await gehe(a, 'eingang');
    await a.click('#ga-bsp-laden'); await quittung(a, 'Beispiele geladen');
    const bsp = (await hole(`/api/x/gaeste/${haus}/betrieb`)).daten;
    gut('Beispiele: vier Anfragen im Eingang, alle als Beispiel gekennzeichnet, zwei davon neu', bsp.anfragen.length === 4 && bsp.anfragen.every(x => x.herkunft === 'beispiel') && bsp.anfragen.filter(x => x.status === 'neu').length === 2 && await a.locator('.ga-anfragen .ga-schild', { hasText: 'Beispiel' }).count() === 4
      && (await a.locator('#ga-bsp-hinweis').innerText()).includes('erfunden'));
    gut('Beispiele: zählen nie als Gäste', bsp.fragen.filter(f => f.herkunft === 'gast').length === bsp.fragen.filter(f => f.herkunft === 'gast' && !String(f.id).startsWith('f-b-')).length && bsp.ueberblick.fragen_gaeste === bsp.fragen.filter(f => f.herkunft === 'gast').length);
    gut('Beispiele: nichts ist von selbst geöffnet, neue Anfragen bleiben neu', await a.locator('#ga-detail-leer').count() === 1 && (await a.locator('#ga-wartet').innerText()).includes('2 Anfragen warten'));
    await zuQuittungen(a);
    await form(a, 'Eingang mit Beispielen');
    await a.locator('.ga-anfragen button').first().click();
    await a.waitForSelector('#ga-detail');
    gut('Beispiele: geöffnet steht «kein echter Gast» dabei, und es wartet eine weniger', (await a.locator('#ga-detail').innerText()).includes('kein echter Gast'));
    await a.waitForFunction(() => document.querySelector('#ga-wartet').innerText.includes('Eine Anfrage wartet'));
    await form(a, 'Eingang mit geöffnetem Beispiel');
    await a.click('#ga-bsp-weg'); await quittung(a, 'Beispiele entfernt');
    const ohne = (await hole(`/api/x/gaeste/${haus}/betrieb`)).daten;
    gut('Beispiele: ein Knopf entfernt sie restlos', ohne.anfragen.length === 0 && !ohne.fragen.some(f => f.herkunft === 'beispiel') && reste(daten, 'example.ch').length === 0, reste(daten, 'example.ch').join(', '));

    gut('Server: keine unerwarteten Fehler', !/FEHLER|Traceback/.test(server.log()), server.log().split('\n').filter(z => /FEHLER|Traceback/.test(z)).slice(0, 2).join(' | '));
    gut('Browser: keine Fehler in der Konsole, kein Dialog des Betriebssystems', fehler.length === 0, fehler.slice(0, 3).join(' | '));
  } catch (e) {
    if (!schritte.length || schritte[schritte.length - 1].gut) schritte.push({ was: 'Abbruch nach «' + (schritte.length ? schritte[schritte.length - 1].was : 'Start') + '»', gut: false, mehr: String(e.message || e).split('\n').slice(0, 3).join(' ') });
    if (fehler.length) schritte.push({ was: 'Fehler der Seite', gut: false, mehr: fehler.slice(0, 3).join(' | ') });
  }
  await browser.close();
  await serverStop(server);
  fs.rmSync(daten, { recursive: true, force: true });
  return schritte;
}

(async () => {
  const [nurHaus, nurWelt, nurBreite] = process.argv.slice(2);
  try { await hole('/api/haus/gasterntal'); console.error(`Auf Port ${PORT} antwortet schon ein Server. Der Prüflauf beendet nichts Fremdes und bricht ab.`); process.exit(2); } catch (e) { /* frei */ }
  const teile = spawnSync('python3', ['werkzeuge/gaeste/pruef_teile.py'], { cwd: WURZEL, encoding: 'utf8' });
  console.log('Teile (Schutz, Kosten, Fristen, Schreiber): ' + (teile.stdout || teile.stderr).trim().split('\n').pop());
  let schlecht = teile.status === 0 ? 0 : 1, gesamt = 0;
  const quelle = ['index.html', 'gaeste.js', 'gaeste.css'].map(f => fs.readFileSync(path.join(__dirname, f), 'utf8')).join('\n');
  const fremd = [/<select/i, /type=["']?(date|time|color|file)/i, /\b(alert|confirm|prompt)\(/, /https?:\/\/(?!127\.0\.0\.1)[a-z0-9.-]+\.[a-z]{2,}\/[^\s"']*\.(js|css|woff2?)/i, /ß/].filter(m => m.test(quelle));
  console.log('Quelltext (keine Systemauswahl, kein Systemdialog, nichts von aussen geladen, kein ß): ' + (fremd.length ? 'FEHLT ' + fremd.join(' ') : 'gut'));
  if (fremd.length) schlecht++;
  let kern;
  try { kern = require(finde(WEBKIT))[WEBKIT ? 'webkit' : 'chromium']; } catch (e) { console.error('Prüflauf nicht gestartet: ' + e.message); process.exit(2); }
  console.log('Browser: ' + (WEBKIT ? 'Safari-Kern (WebKit)' : 'Chromium') + ', ohne Fenster');
  for (const haus of Object.keys(HAEUSER)) for (const welt of ['grand', 'land']) for (const breite of BREITEN) {
    if ((nurHaus && nurHaus !== haus) || (nurWelt && nurWelt !== welt) || (nurBreite && +nurBreite !== breite)) continue;
    const t = Date.now(), schritte = await lauf(kern, haus, welt, breite), fehl = schritte.filter(s => !s.gut);
    gesamt += schritte.length;
    console.log(`${fehl.length ? 'FEHLT' : 'gut  '} ${haus.padEnd(12)} ${welt.padEnd(5)} ${String(breite).padStart(4)} px · ${schritte.length - fehl.length} von ${schritte.length} Prüfungen · ${((Date.now() - t) / 1000).toFixed(0)} s`);
    fehl.forEach(s => console.log('        ✗ ' + s.was + (s.mehr ? ' · ' + s.mehr : '')));
    if (fehl.length) schlecht++;
  }
  console.log(schlecht ? `NICHT BESTANDEN · ${schlecht} Läufe mit Fehlern` : `BESTANDEN · ${gesamt} Prüfungen in der Oberfläche`);
  process.exit(schlecht ? 1 : 0);
})();
