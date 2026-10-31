/* pruef.js · fester Durchlauf des Werkzeugs «website». Start im Ordner _Werkzeuge:
     node werkzeuge/website/pruef.js                        alles: beide Häuser, beide Welten, 1440 · 390 · 320
     node werkzeuge/website/pruef.js gasterntal land 1440   nur ein Ausschnitt (Haus, Welt, Breite; je auch mit Komma oder «alle»)

   Der Lauf rührt weder die echten Daten noch die echte Kopie an:
     · eigener Server auf Port 8972 mit Wegwerf-Daten (WERKZEUGE_DATEN), am Ende per PID beendet
     · eigene Wegwerf-Kopie der Seiten (WEBSITE_PROBE = werkzeuge/website/_probe-pruef-<pid>), frisch aus den Quellen der Häuser, am Ende gelöscht
     · der Browser läuft unsichtbar (headless), nie ein Fenster, nie ein Eingriff in einen anderen Browser
   Ist Port 8972 belegt, bricht der Lauf ab, statt etwas zu beenden (anderer Port: PRUEF_PORT=…; Safari-Kern: MOTOR=webkit).

   Teil 1 je Haus (ohne Browser): Byte-Gleichheit, Prüfung des Servers, Konflikt, Sperre, Bereiche an/aus, Foto · Link · Hinweis bis online und zurück, Lexikon.
   Teil 2 je Haus (Browser): Prüfseite auch ohne Werkzeug und ohne Server-Teil, Tür bei Startfehler, gesperrte Karte, ruhige Vorschau.
   Teil 3 je Haus × Welt × Breite (Browser): öffnen · Text und Zeit ändern · speichern · neu laden · Konflikt · Vorher/nachher · veröffentlichen ·
     Kopie zeigt den neuen Stand · Verlauf · zurückholen · Seite wieder alt. Dazu in jeder Ansicht: kein seitlicher Überlauf, keine Auswahl des
     Betriebssystems, Speichern-Knopf zu sehen, keine Fehler in der Konsole. */
const fs = require('fs'), path = require('path'), os = require('os'), crypto = require('crypto');
const { spawn, execFileSync } = require('child_process');

const HIER = __dirname, WURZEL = path.resolve(HIER, '..', '..');
const PORT = Number(process.env.PRUEF_PORT) || 8972, B = `http://127.0.0.1:${PORT}`;
const arg = (i, alle) => { const a = process.argv[2 + i]; return !a || a === 'alle' ? alle : a.split(','); };
const HAEUSER = arg(0, ['gasterntal', 'beau-rivage']), WELTEN = arg(1, ['land', 'grand']), BREITEN = arg(2, ['1440', '390', '320']).map(Number);
const NAME = { grand: 'Le Bureau', land: 'Der Schreibtisch' };
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'website-pruef-'));
const PROBE_NAME = `_probe-pruef-${process.pid}`, PROBE = path.join(HIER, PROBE_NAME);
/* Rahmen eines Hauses (RAHMEN=1, SERVER_SKRIPT=<Haus>/_werkzeuge/bureau/serve.py): dasselbe Werkzeug unter der Adresse des Hauses
   (/_werkzeuge/bureau/), mit Kopf, Rand, Startbild und Leiste aus dessen Werkzeug-Paket; Name aus dem Paket, kein Modus-Knopf. */
const RAHMEN = !!process.env.RAHMEN, SERVER_SKRIPT = process.env.SERVER_SKRIPT || '';
const ADR = (haus, q) => RAHMEN ? '/_werkzeuge/bureau/?' + [haus === 'gibt-es-nicht' ? 'haus=gibt-es-nicht' : '', q || ''].filter(Boolean).join('&') : `/werkzeuge/website/?haus=${haus}${q ? '&' + q : ''}`;
const KARTEN_WEG = RAHMEN ? '/_werkzeuge/carte/' : '/werkzeuge/karten/';
const OS_WAHL = 'select,datalist,input[type=date],input[type=time],input[type=datetime-local],input[type=month],input[type=week],input[type=color],input[type=file]';

let gezaehlt = 0, schlecht = [], KOPIERT = 0;
function pruef(wahr, was, mehr) {
  gezaehlt++;
  if (!wahr) { schlecht.push(was); console.log('FEHLT  ' + was + (mehr ? '  → ' + String(mehr).slice(0, 400) : '')); }
  else if (process.env.LAUT) console.log('gut    ' + was);
  return !!wahr;
}
const sha = roh => crypto.createHash('sha256').update(roh).digest('hex');
const warte = ms => new Promise(r => setTimeout(r, ms));
async function bis(fn, ms = 4000) { for (const ende = Date.now() + ms; Date.now() < ende; await warte(100)) if (await fn()) return true; return !!(await fn()); }

function findePlaywright() {
  if (process.env.PLAYWRIGHT_PFAD) return process.env.PLAYWRIGHT_PFAD;   // z. B. ~/Aussen-Pruefung/node_modules/playwright (dort liegt auch der Safari-Kern)
  const npx = path.join(os.homedir(), '.npm/_npx');
  for (const d of fs.existsSync(npx) ? fs.readdirSync(npx) : []) { const p = path.join(npx, d, 'node_modules/playwright'); if (fs.existsSync(p)) return p; }
  throw new Error('Playwright nicht gefunden (einmal: npx -y playwright --version)');
}
function shell() {
  const c = path.join(os.homedir(), 'Library/Caches/ms-playwright');
  for (const n of fs.readdirSync(c).filter(n => n.startsWith('chromium_headless_shell-')).sort().reverse()) {
    const p = path.join(c, n, 'chrome-headless-shell-mac-arm64/chrome-headless-shell');
    if (fs.existsSync(p)) return p;
  }
  return undefined;
}

async function api(methode, weg, daten) {
  const r = await fetch(B + weg, { method: methode, headers: daten ? { 'Content-Type': 'application/json', Origin: B } : { Origin: B }, body: daten ? JSON.stringify(daten) : undefined });
  let j = null;
  try { j = await r.json(); } catch (e) { /* keine lesbare Antwort */ }
  return { status: r.status, j: j || {} };
}
const X = weg => '/api/x/website/' + weg;
const stand = async haus => (await api('GET', X('stand/' + haus))).j;

function beschreibung(haus) {
  const b = JSON.parse(fs.readFileSync(path.join(HIER, 'haeuser', haus + '.json'), 'utf8'));
  const stamm = JSON.parse(fs.readFileSync(path.join(WURZEL, 'haeuser', haus, 'haus.json'), 'utf8'));
  return Object.assign(b, { quelle: path.join(stamm.quelle.replace(/^~/, os.homedir()), (b.kopie && b.kopie.unter) || ''), dateien: b.seiten.map(s => s.datei).flatMap(n => [n].concat((b.sprachen || []).map(s => s.ordner + '/' + n))) });
}
function lies(haus, teil, rel) { const p = path.join(PROBE, haus, teil, rel); return fs.existsSync(p) ? fs.readFileSync(p) : null; }
const GRUND = {};
function grundlageHash(haus) { return sha(beschreibung(haus).dateien.map(rel => { const a = lies(haus, 'grundlage', rel); return a ? sha(a) : '-'; }).join()); }
function onlineGleichGrundlage(haus) {
  return beschreibung(haus).dateien.filter(rel => { const a = lies(haus, 'grundlage', rel), b = lies(haus, 'online', rel); return a && (!b || sha(a) !== sha(b)); });
}
async function zurueckAufAnfang(haus) {
  /* nach einem gescheiterten Schritt: Entwurf weg, leerer Stand wieder live, damit der nächste Schritt sauber beginnt */
  await api('DELETE', '/api/entwurf/' + haus + '/website', { wer: 'pruef' });
  let s = await stand(haus);
  if (['texte', 'bilder', 'links', 'aus'].some(k => (s.daten[k] || []).length) || Object.keys(s.daten.hinweis || {}).length) {
    await api('PUT', '/api/entwurf/' + haus + '/website', { daten: { texte: [], bilder: [], links: [], aus: [], hinweis: {} }, erwartet: s.kennung, wer: 'pruef' });
    s = await stand(haus);
    await api('POST', X('veroeffentlichen/' + haus), { erwartet: s.kennung, wer: 'pruef', notiz: 'Aufräumen' });
  }
}

// ---------------------------------------------------------------- Teil 1: Server, ohne Browser
async function teilServer(haus) {
  const T = `[${haus} · Server] `;
  const b = beschreibung(haus);
  const ungleich = () => b.dateien.filter(rel => { const q = path.join(b.quelle, rel); const a = fs.existsSync(q) ? fs.readFileSync(q) : null, g = lies(haus, 'grundlage', rel), o = lies(haus, 'online', rel); return a && (!g || !o || sha(a) !== sha(g) || sha(a) !== sha(o)); });
  /* An den Quellen arbeiten andere Chats: wird eine Seite zwischen dem Kopieren und dem Vergleich neu gebaut, ist das kein Fehler des Werkzeugs.
     Solche Dateien (Quelle jünger als die Kopie) werden einmal nachgezogen und dann verglichen. Alles Weitere misst gegen diese Grundlage. */
  const neuer = ungleich().filter(rel => fs.statSync(path.join(b.quelle, rel)).mtimeMs > KOPIERT);
  for (const rel of neuer) for (const teil of ['grundlage', 'online']) fs.copyFileSync(path.join(b.quelle, rel), path.join(PROBE, haus, teil, rel));
  if (neuer.length) console.log(`${haus}: ${neuer.length} Seiten wurden an der Quelle während des Kopierens neu gebaut und nachgezogen`);
  const anders = ungleich();
  pruef(!anders.length, T + `Quelle, Grundlage und Online-Kopie Byte für Byte gleich (${b.dateien.length} Dateien), bevor das Werkzeug eingehängt ist`, anders.slice(0, 5));

  const info = (await api('GET', X('haus/' + haus))).j;
  pruef(info.seiten && info.seiten.length === b.seiten.length, T + 'Haus antwortet mit allen Seiten der Beschreibung');
  pruef(info.seiten.every(s => s.name && !/\.html$/.test(s.name)), T + 'jede Seite hat einen Namen, gelesen aus der Website', info.seiten.filter(s => !s.name || /\.html$/.test(s.name)).map(s => s.datei));
  GRUND[haus] = grundlageHash(haus);
  const s0 = await stand(haus);
  pruef(s0.offen === false && s0.aenderungen.length === 0, T + 'erster Stand: nichts offen');
  pruef(!onlineGleichGrundlage(haus).length, T + 'nach dem Einhängen (erster Stand angelegt): Online-Kopie weiter Byte für Byte gleich');

  const pr = (await api('GET', X('pruefung/' + haus))).j;
  const nein = (pr.punkte || []).filter(p => !p.gut);
  pruef(pr.punkte && pr.punkte.length >= 10 && !nein.length, T + `Prüfung des Servers: ${(pr.punkte || []).length} Punkte, alle in Ordnung`, nein.map(p => p.titel + ': ' + p.text));
  pruef((pr.punkte || []).some(p => p.id === 'unveraendert' && p.gut), T + 'ohne Änderung gibt die Schicht jede Seite Byte für Byte zurück');

  // Bereiche: eingeschaltete lesen ihre Felder, ausgeschaltete gibt es nicht
  const an = new Set(info.bereiche.map(x => x.key));
  for (const k of an) {
    const r = (await api('GET', X(`bereich/${haus}/${k}`))).j;
    pruef(r.eintraege && r.eintraege.length > 0 && !r.fehlt.length, T + `Bereich «${r.name || k}»: ${(r.eintraege || []).length} Einträge, kein Feld fehlt`, r.fehlt);
  }
  for (const k of Object.keys(b.bereiche || {}).filter(k => b.bereiche[k].an === false)) {
    const r = await api('GET', X(`bereich/${haus}/${k}`));
    pruef(r.status === 404 && r.j.stichwort === 'bereich-aus' && !an.has(k), T + `Bereich «${k}» ist ausgeschaltet: nicht in der Liste, Abruf abgelehnt`);
  }
  const z = (await api('GET', X('zahlen/' + haus))).j;
  pruef(z.zahl > 10, T + `Zeiten und Preise: ${z.zahl} Angaben`);
  const doppelt = z.gruppen.flatMap(g => g.zeilen).filter(x => new Set(x.orte.map(o => o.seite)).size !== x.orte.length);
  pruef(!doppelt.length, T + 'Zeiten und Preise: keine Zeile legt zwei Stellen derselben Seite zusammen (gleiche Zeit in zwei Restaurants bleibt zweierlei)', doppelt.slice(0, 3).map(x => x.vor + ' ' + x.t));

  // Konflikt: wer mit veralteter Kennung speichert, überschreibt nichts
  const v = (await api('GET', X(`seite/${haus}/${b.seiten[0].datei}`))).j;
  const frei = v.gruppen.flatMap(g => g.fest || g.zu ? [] : g.stellen.filter(st => !st.zu && st.tag === 'p' && st.t.length > 30));
  const st1 = frei[0], st2 = frei[1];
  const op = (st, text) => ({ art: 'text', seite: b.seiten[0].datei, h: st.h, n: st.n, neu: text });
  let r = await api('POST', X('aendern/' + haus), { ops: [op(st1, 'Erste Probe.')], erwartet: s0.kennung, wer: 'eins' });
  pruef(r.status === 200 && r.j.quittung && r.j.quittung[0].vorher === st1.t && r.j.quittung[0].nachher === 'Erste Probe.', T + 'Speichern antwortet mit Quittung: vorher (aus der Seite gelesen) und nachher');
  r = await api('POST', X('aendern/' + haus), { ops: [op(st2, 'Zweite Probe.')], erwartet: s0.kennung, wer: 'zwei' });
  const s1 = await stand(haus);
  pruef(r.status === 409 && r.j.stichwort === 'konflikt' && s1.aenderungen.length === 1 && s1.aenderungen[0].nachher === 'Erste Probe.', T + 'zweiter Schreiber mit alter Kennung: 409 Konflikt, nichts überschrieben');
  r = await api('POST', X('aendern/' + haus), { ops: [op(st1, st1.t)], erwartet: s1.kennung, wer: 'eins' });
  pruef(r.status === 200 && (await stand(haus)).offen === false, T + 'Text zurück auf den Wortlaut der Seite: die Änderung verschwindet, nichts offen');
  r = await api('POST', X('aendern/' + haus), { ops: [op(st1, st1.t)], erwartet: (await stand(haus)).kennung, wer: 'eins' });
  pruef(r.status === 200 && r.j.nichts === true && /Nichts geändert, nichts gespeichert/.test(r.j.meldung), T + 'Speichern ohne Änderung: «Nichts geändert, nichts gespeichert.»');
  r = await api('POST', X('aendern/' + haus), { ops: [op(st1, '<script>alert(1)</script><b onclick="x()">Fett</b> <a href="javascript:alert(1)">weg</a>')], erwartet: (await stand(haus)).kennung, wer: 'eins' });
  const roh = (await stand(haus)).daten.texte[0].neu;
  pruef(r.status === 200 && !/script|onclick|javascript/i.test(roh) && /<b>Fett<\/b>/.test(roh), T + 'Eingabe wird gesäubert: kein Skript, kein Ereignis, kein gefährlicher Link', roh);
  await api('DELETE', '/api/entwurf/' + haus + '/website', { wer: 'pruef' });

  // Sperre: Karten-Abschnitte gehören dem Werkzeug «karten»
  let gesperrt = null;
  for (const s of b.seiten) {
    const vv = (await api('GET', X(`seite/${haus}/${s.datei}`))).j;
    const g = vv.gruppen.flatMap(g2 => g2.stellen.filter(st => st.zu === 'karten').map(st => ({ seite: s.datei, st })))[0];
    if (g) { gesperrt = g; break; }
  }
  pruef(!!gesperrt && info.karten === true, T + 'es gibt gesperrte Karten-Abschnitte');
  if (gesperrt) {
    r = await api('POST', X('aendern/' + haus), { ops: [{ art: 'text', seite: gesperrt.seite, h: gesperrt.st.h, n: gesperrt.st.n, neu: 'Geändert' }], erwartet: (await stand(haus)).kennung, wer: 'pruef' });
    pruef(r.status === 423 && r.j.stichwort === 'gesperrt' && r.j.werkzeug === 'karten' && (await stand(haus)).offen === false, T + `gesperrte Stelle (${gesperrt.seite}) lässt sich nicht ändern: 423, Verweis auf «karten»`);
    const zz = z.gruppen.flatMap(g => g.zeilen).filter(x => x.h === gesperrt.st.h && x.orte.some(o => o.seite === gesperrt.seite && o.n === gesperrt.st.n));
    pruef(!zz.length, T + 'gesperrte Stellen stehen nicht unter «Zeiten und Preise»');
  }

  // Foto, Link, Hinweis: speichern, veröffentlichen, online ansehen, zurückholen
  const start = b.seiten[0].datei;
  const fotos = (await api('GET', X('fotos/' + haus))).j.fotos;
  const erstes = v.gruppen.flatMap(g => g.fotos.filter(f => !f.zu))[0];
  const anderes = fotos.find(f => f.b !== erstes.b && f.w > 0);
  const sp = (b.sprachen || [])[0];
  const ops = [{ art: 'bild', seite: start, b: erstes.b, n: erstes.n, neu: anderes.b, alt: 'Probe-Beschreibung', alt_sprachen: sp ? { [sp.code]: 'Probe description' } : {} },
               { art: 'hinweis', an: true, text: 'Probe-Hinweis für Gäste', von: '', bis: '31.12.2099', link: 'https://example.org/probe', linktext: 'Zur Probe', sprachen: sp ? { [sp.code]: { text: 'Probe notice', linktext: 'Probe link' } } : {} }];
  let nurSp = null;
  if (sp) {   // nur eine Übersetzung ändern, das Deutsche bleibt
    nurSp = (await api('GET', X(`stelle/${haus}/${start}/${st2.h}/${st2.n}`))).j;
    ops.push({ art: 'text', seite: start, h: st2.h, n: st2.n, neu: nurSp.original, sprachen: { [sp.code]: 'Nur diese Sprache Probe' } });
  }
  let linkSeite = null;
  if (an.has('unterlagen')) {
    const u = (await api('GET', X(`bereich/${haus}/unterlagen`))).j.eintraege[0];
    const lf = u.felder.find(f => f.art === 'link').teile[0];
    linkSeite = u.seite;
    ops.push({ art: 'link', seite: u.seite, h: lf.h, n: lf.n, neu: 'https://example.org/probe.pdf' });
  }
  r = await api('POST', X('aendern/' + haus), { ops, erwartet: (await stand(haus)).kennung, wer: 'pruef' });
  pruef(r.status === 200 && r.j.quittung.length === ops.length, T + 'Foto, Hinweis' + (linkSeite ? ', Link' : '') + ' gespeichert', JSON.stringify(r.j).slice(0, 300));
  if (nurSp) {
    const ae = (await stand(haus)).aenderungen.find(a => a.h === st2.h && a.seite === start);
    pruef(ae && ae.was === 'Übersetzung' && Object.values(ae.sprachen).every(Boolean), T + 'nur eine Übersetzung geändert: steht als «Übersetzung» im Entwurf, in keiner anderen Sprache «fehlt»', JSON.stringify(ae));
  }
  r = await api('POST', X('aendern/' + haus), { ops: [{ art: 'hinweis', an: true, text: 'x', von: '31.02.2026' }], erwartet: (await stand(haus)).kennung, wer: 'pruef' });
  pruef(r.status === 422 && r.j.stichwort === 'datum', T + 'ein Datum, das es nicht gibt, wird abgelehnt');
  r = await api('POST', X('aendern/' + haus), { ops: [{ art: 'link', seite: linkSeite || start, h: 'x', n: 0, neu: 'javascript:alert(1)' }], erwartet: (await stand(haus)).kennung, wer: 'pruef' });
  pruef(r.status === 404 || r.status === 422, T + 'ein Link an einer unbekannten Stelle wird abgelehnt');
  const sv = await stand(haus);
  r = await api('POST', X('veroeffentlichen/' + haus), { erwartet: 'falsch', wer: 'pruef' });
  pruef(r.status === 409, T + 'Veröffentlichen mit veralteter Kennung: 409, nichts veröffentlicht');
  r = await api('POST', X('veroeffentlichen/' + haus), { erwartet: sv.kennung, wer: 'pruef', notiz: 'Probe Foto Hinweis' });
  pruef(r.status === 200 && r.j.geschrieben.length >= b.dateien.length, T + `veröffentlicht: ${(r.j.geschrieben || []).length} Dateien geschrieben (Hinweis steht auf jeder Seite)`, JSON.stringify(r.j).slice(0, 300));
  const on = lies(haus, 'online', start).toString('utf8'), gr = lies(haus, 'grundlage', start).toString('utf8');
  const spenderBild = on.match(new RegExp('<img[^>]*' + anderes.b.replace(/[-]/g, '\\-') + '[^>]*alt="Probe-Beschreibung"'));
  pruef(!!spenderBild && on.includes('Probe-Hinweis für Gäste') && on.includes('data-bis="2099-12-31"') && !on.includes('data-ws-'), T + 'online: neues Foto mit neuer Beschreibung, Hinweis mit Enddatum, keine Marken des Werkzeugs im Quelltext');
  if (sp) {
    const en = lies(haus, 'online', sp.ordner + '/' + start).toString('utf8');
    pruef(en.includes('Probe notice') && en.includes('Probe link') && en.includes('alt="Probe description"') && en.includes('../assets') && !en.includes('Probe-Hinweis'), T + `Sprache ${sp.code}: Hinweis und Bildbeschreibung übersetzt, Foto mit dem Pfad der Sprachseite`);
    const sp2 = b.sprachen[1];
    if (sp2) pruef(lies(haus, 'online', sp2.ordner + '/' + start).toString('utf8').includes('Probe-Hinweis für Gäste'), T + `Sprache ${sp2.code} ohne Übersetzung: dort steht der deutsche Hinweis`);
    const mal = (text, stueck) => text.split(stueck).length - 1;
    const bisher2 = sp2 ? nurSp.sprachen.find(x => x.code === sp2.code).bisher_html : '';
    pruef(en.includes('Nur diese Sprache Probe') && !on.includes('Nur diese Sprache Probe') && mal(on, nurSp.original) === mal(gr, nurSp.original) &&
      (!sp2 || (bisher2 && mal(lies(haus, 'online', sp2.ordner + '/' + start).toString('utf8'), bisher2) === mal(lies(haus, 'grundlage', sp2.ordner + '/' + start).toString('utf8'), bisher2))),
      T + `nur ${sp.code} geändert: dort steht die neue Fassung, das Deutsche und ${sp2 ? sp2.code : 'die übrigen Sprachen'} bleiben Zeichen für Zeichen`);
  }
  if (linkSeite) pruef(lies(haus, 'online', linkSeite).toString('utf8').includes('href="https://example.org/probe.pdf"'), T + 'online: Link der Unterlage zeigt auf die neue Adresse');
  pruef(gr.length > 0 && on !== gr, T + 'online weicht jetzt von der Grundlage ab (nur die Online-Kopie wurde geschrieben)');
  const vl = (await api('GET', X('verlauf/' + haus))).j.verlauf;
  pruef(vl.length >= 1 && vl[0].unterschiede === ops.length, T + `Verlauf: voriger Stand liegt da, ${ops.length} Unterschiede zu heute`, JSON.stringify(vl[0]));
  r = await api('POST', '/api/zurueckholen/' + haus + '/website', { fassung: vl[0].fassung, wer: 'pruef' });
  const sz = await stand(haus);
  pruef(r.status === 200 && sz.offen && on === lies(haus, 'online', start).toString('utf8'), T + 'Zurückholen legt nur einen Entwurf an, online bleibt unverändert');
  r = await api('POST', X('veroeffentlichen/' + haus), { erwartet: sz.kennung, wer: 'pruef', notiz: 'zurück' });
  pruef(r.status === 200 && !onlineGleichGrundlage(haus).length, T + 'nach Zurückholen und Veröffentlichen: jede Seite wieder Byte für Byte wie gebaut', onlineGleichGrundlage(haus).slice(0, 4));

  // Reparatur: von Hand verstellte Seite wird erkannt und neu ausgegeben
  fs.appendFileSync(path.join(PROBE, haus, 'online', start), '<!-- verstellt -->');
  const pr2 = (await api('GET', X('pruefung/' + haus))).j;
  pruef(pr2.punkte.some(p => p.id === 'online' && !p.gut && p.lex === 'ausgabe'), T + 'Prüfung merkt eine von Hand verstellte Seite');
  r = await api('POST', X('reparieren/' + haus), { was: 'ausgeben', wer: 'pruef' });
  pruef(r.status === 200 && !onlineGleichGrundlage(haus).length, T + 'Reparatur «Seiten neu ausgeben» stellt sie wieder her');
  pruef(grundlageHash(haus) === GRUND[haus], T + 'die Grundlage (Seiten, wie das Haus sie gebaut hat) ist nach allem unberührt');
}

function ohneHaus() {
  /* Das Werkzeug kennt kein Haus: in seinem Code steht keine Kennung und kein Name eines Hauses. Was ein Haus hat, steht in haeuser/<haus>.json. */
  const worte = new Set();
  for (const d of fs.readdirSync(path.join(WURZEL, 'haeuser'))) {
    const p = path.join(WURZEL, 'haeuser', d, 'haus.json');
    if (!fs.existsSync(p)) continue;
    const h = JSON.parse(fs.readFileSync(p, 'utf8'));
    [h.kennung].concat(String(h.name || '').split(/[\s]+/)).filter(w => w && w.length >= 6).forEach(w => worte.add(w.toLowerCase()));
  }
  const funde = [];
  for (const d of ['api.py', 'schicht.py', 'ausgabe.py', 'website.js', 'website.css', 'index.html', 'pruefung.html', 'pruefung.css']) {
    const t = fs.readFileSync(path.join(HIER, d), 'utf8').toLowerCase();
    worte.forEach(w => { if (t.includes(w)) funde.push(d + ': ' + w); });
  }
  pruef(worte.size >= 3 && !funde.length, `[Bau] im Code des Werkzeugs steht kein Haus (gesucht: ${[...worte].join(', ')})`, funde);
  const eigen = ['website.css', 'pruefung.css', 'website.js', 'pruefung.js', 'index.html', 'pruefung.html'].flatMap(d => (fs.readFileSync(path.join(HIER, d), 'utf8').match(/#[0-9a-fA-F]{3,8}\b(?![\w-])|rgba?\([^)]*\)|font-family:\s*['"A-Za-z]/g) || []).filter(x => !/^font-family/.test(x)).map(x => d + ': ' + x));
  pruef(!eigen.length, '[Bau] keine eigene Farbe in den Dateien des Werkzeugs: alles kommt aus welt.css', eigen.slice(0, 5));
  const eszett = fs.readdirSync(HIER).filter(d => /\.(js|py|html|css)$/.test(d) && d !== 'pruef.js').map(d => path.join(HIER, d)).concat(fs.readdirSync(path.join(HIER, 'haeuser')).map(d => path.join(HIER, 'haeuser', d)))
    .filter(p => fs.readFileSync(p, 'utf8').includes('ß')).map(p => path.basename(p));
  pruef(!eszett.length, '[Bau] Schweizer Schreibweise: kein ß in den Dateien des Werkzeugs', eszett);
}

function lexikonVollstaendig() {
  const ganz = fs.readFileSync(path.join(HIER, 'pruefung.js'), 'utf8');
  const lex = ganz.slice(ganz.indexOf('const LEX = ['), ganz.indexOf('const LEX_GLEICH'));   // nur das Lexikon, nicht die Punkte und Reparaturen darunter
  const da = new Set([...lex.matchAll(/\{ id: '([\w-]+)', titel:/g)].map(m => m[1]));
  const gleich = (/const LEX_GLEICH = \{([^}]*)\}/.exec(ganz) || [, ''])[1];
  [...gleich.matchAll(/'?([\w-]+)'?:\s*'[\w-]+'/g)].forEach(m => da.add(m[1]));
  const gebraucht = new Set();
  const quellen = { 'api.py': [/Fehler\(\d+, '([\w-]+)'/g, /'stichwort': '([\w-]+)'/g, /lex='([\w-]+)'/g], 'website.js': [/stichwort: '([\w-]+)'/g, /pruefLink\('([\w-]+)'\)/g], '../../unterbau/serve.py': [/'stichwort': '([\w-]+)'/g, /Fehler\(\d+, '[^']*', '([\w-]+)'\)/g] };
  for (const [d, muster] of Object.entries(quellen)) { const t = fs.readFileSync(path.join(HIER, d), 'utf8'); muster.forEach(m => [...t.matchAll(m)].forEach(x => gebraucht.add(x[1]))); }
  const fehlen = [...gebraucht].filter(s => !da.has(s));
  pruef(gebraucht.size >= 25 && !fehlen.length, `[Lexikon] jedes der ${gebraucht.size} Stichworte aus api.py, website.js und serve.py hat einen Eintrag (${da.size} Einträge)`, fehlen);
  const dreiteilig = [...lex.matchAll(/\{ id: '([\w-]+)', titel: '[^']+',\s*sehen: '[^']+',\s*grund: '[^']+',\s*tun: '[^']+',/g)].length;
  pruef(dreiteilig === da.size - [...gleich.matchAll(/:\s*'[\w-]+'/g)].length && dreiteilig >= 30, `[Lexikon] jeder der ${dreiteilig} Einträge hat Sehen, Grund und Tun`);
}

// ---------------------------------------------------------------- Browser: Helfer
function neueSeite(kontext, fehler, wo) {
  return kontext.newPage().then(p => {
    p.on('pageerror', e => fehler.push(`${wo}: ${e}`));
    p.on('console', m => { if (m.type() === 'error') fehler.push(`${wo}: ${m.text().slice(0, 240)}`); });
    return p;
  });
}
async function bereit(p, ansicht) { await p.waitForSelector(`#ws-mitte[data-ws-bereit="${ansicht}"]`, { timeout: 30000 }); }
async function rahmenBereit(p) {
  await p.waitForFunction(() => { const f = [...document.querySelectorAll('iframe[data-ws-frame]')]; return f.length && f.every(x => x.contentDocument && x.contentDocument.readyState !== 'loading' && x.contentDocument.querySelector('[data-ws-e]')) && ![...document.querySelectorAll('.ws-vorschau__lage')].some(l => !l.hidden); }, null, { timeout: 30000 });
}
async function lage(p, T, wo, fenster) {
  const d = await p.evaluate(sel => {
    const k = document.querySelector('#ws-speichern'), r = k.getBoundingClientRect(), oben = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return { ueber: document.documentElement.scrollWidth - innerWidth, wahl: document.querySelectorAll(sel).length,
             knopf: r.width > 40 && r.top >= 0 && r.bottom <= innerHeight && r.left >= 0 && r.right <= innerWidth && getComputedStyle(k).visibility === 'visible', frei: !!oben && k.contains(oben),
             leiste: !!document.querySelector('#ws-leiste').childElementCount };
  }, OS_WAHL);
  pruef(d.ueber <= 0, T + `${wo}: kein seitlicher Überlauf`, d.ueber + ' px');
  pruef(d.wahl === 0, T + `${wo}: keine Auswahl des Betriebssystems`);
  if (fenster) pruef(d.knopf, T + `${wo}: Leiste mit Speichern-Knopf steht hinter dem Fenster an ihrem Platz`);
  else pruef(d.knopf && d.frei, T + `${wo}: Speichern-Knopf ganz zu sehen, nichts liegt darüber`, JSON.stringify(d));
  pruef(d.leiste, T + `${wo}: Leiste unten steht`);
}
async function nav(p, ansicht) {
  const auf = p.locator('#ws-menue-knopf, [data-wo-rand-knopf]').first();
  if (await auf.isVisible() && await auf.getAttribute('aria-expanded') !== 'true') await auf.click();
  await p.locator(`[data-ws-nav="${ansicht}"]`).click();
  await bereit(p, ansicht);
}
async function kandidaten(p) {
  return p.evaluate(() => {
    const d = document.querySelector('iframe[data-ws-frame="entwurf"]').contentDocument;
    const alle = [...d.querySelectorAll('main p[data-ws-e]')].filter(e => !e.closest('[data-ws-zu]') && !e.closest('dialog,[hidden]') && e.children.length === 0 && e.getBoundingClientRect().width > 40);
    const zahl = {};
    [...d.querySelectorAll('[data-ws-e]')].forEach(e => { zahl[e.getAttribute('data-ws-e')] = (zahl[e.getAttribute('data-ws-e')] || 0) + 1; });
    return alle.map(e => ({ h: e.getAttribute('data-ws-e'), n: +e.getAttribute('data-ws-n'), t: e.textContent.replace(/\s+/g, ' ').trim() })).filter(x => zahl[x.h] === 1 && x.t.length > 30 && x.t.length < 120 && !/[<>&"]/.test(x.t));
  });
}
async function klickStelle(p, st) {
  await p.evaluate(() => document.querySelectorAll('#ws-quittung > *').forEach(q => q.remove()));   // eine stehende Quittung kann über der Stelle liegen (im Rahmen des Hauses breiter); der Mensch schliesst sie mit ×
  const e = p.frameLocator('iframe[data-ws-frame="entwurf"]').locator(`[data-ws-e="${st.h}"][data-ws-n="${st.n}"]`);
  try { await e.click({ timeout: 5000 }); } catch (x) { await e.dispatchEvent('click'); }   // liegt etwas von der Seite des Hauses darüber: Klick direkt auf das Element
  await p.waitForSelector(`[data-ws-form="text"][data-ws-wahl$="|${st.h}|${st.n}"]`, { timeout: 15000 });
  await ruhe(p);
}
async function ruhe(p) {
  /* keine Anfrage unterwegs, zweimal hintereinander: dann ist die Ansicht fertig gezeichnet */
  for (let i = 0, still = 0; i < 200 && still < 2; i++) { still = (await p.evaluate(() => document.documentElement.getAttribute('data-ws-laeuft'))) === '0' ? still + 1 : 0; await warte(120); }
}
async function tippe(p, feld, text, ersetzen) {
  const f = p.locator(`[data-ws-form] [data-ws-feld="${feld}"]`);
  await f.scrollIntoViewIfNeeded();
  await f.evaluate((e, ganz) => { e.focus(); const r = document.createRange(); r.selectNodeContents(e); if (!ganz) r.collapse(false); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }, ersetzen);
  await p.keyboard.type(text, { delay: 2 });
}
async function speichern(p) {
  await p.evaluate(() => { const q = document.querySelector('[data-ws-quittung]'); if (q) q.remove(); });
  await p.locator('#ws-speichern').click();
}
const zuQuittung = p => p.locator('[data-ws-quittung] [aria-label="Schliessen"]').click();
const imRahmen = (p, zustand, fn, a) => p.evaluate(([z, f, a2]) => (new Function('d', 'a', 'return (' + f + ')(d, a)'))(document.querySelector(`iframe[data-ws-frame="${z}"]`).contentDocument, a2), [zustand, fn.toString(), a]);

// ---------------------------------------------------------------- Teil 2: Prüfseite, Startfehler, Sperre, ruhige Vorschau
async function teilSeiten(browser, haus) {
  const T = `[${haus} · Browser] `, fehler = [];
  const k = await browser.newContext({ viewport: { width: 1280, height: 860 } });
  const b = beschreibung(haus);

  let p = await neueSeite(k, fehler, 'Prüfseite');
  await p.goto(`${B}/werkzeuge/website/pruefung.html?haus=${haus}#lex-konflikt`);
  await p.waitForSelector('body[data-wsp-fertig] #wsp-server[data-fertig]', { timeout: 60000 });
  let d = await p.evaluate(() => ({ nein: [...document.querySelectorAll('.wsp-punkt[data-gut="nein"]')].map(e => e.textContent.trim().slice(0, 120)), punkte: document.querySelectorAll('.wsp-punkt').length,
    lex: document.querySelectorAll('.wsp-lex').length, auf: !!(document.querySelector('#lex-konflikt') || {}).open, teile: [...document.querySelectorAll('.wsp-lex dt')].slice(0, 3).map(e => e.textContent), ueber: document.documentElement.scrollWidth - innerWidth }));
  pruef(d.punkte >= 14 && !d.nein.length, T + `Prüfseite: ${d.punkte} Punkte, alle in Ordnung`, d.nein);
  pruef(d.lex >= 30 && d.auf && d.teile.join() === 'Sehen,Grund,Tun', T + `Prüfseite: Lexikon mit ${d.lex} Einträgen (Sehen, Grund, Tun), «Was tun?» öffnet den Eintrag`);
  pruef(d.ueber <= 0 && (await p.locator(OS_WAHL).count()) === 0, T + 'Prüfseite: kein Überlauf, keine Auswahl des Betriebssystems');
  const rep = p.locator('[data-reparatur="ausgeben"]');
  await rep.click();
  pruef(/noch einmal/.test(await rep.textContent()) && await p.locator('#wsp-meldung').isHidden(), T + 'Reparatur: der erste Druck führt nichts aus');
  await rep.click();
  await p.waitForSelector('#wsp-meldung[data-ergebnis="gut"]');
  pruef(/schon richtig|neu geschrieben/.test(await p.locator('#wsp-meldung').textContent()), T + 'Reparatur: der zweite Druck führt aus und meldet das Ergebnis');
  await p.close();

  // die Prüfung läuft, wenn das Werkzeug selbst nicht startet (website.js und website.css kommen nicht an)
  const k2 = await browser.newContext({ viewport: { width: 1280, height: 860 } });
  await k2.route(/\/werkzeuge\/website\/website\.(js|css)/, r => r.abort());
  p = await k2.newPage();
  await p.goto(`${B}/werkzeuge/website/pruefung.html?haus=${haus}`);
  await p.waitForSelector('body[data-wsp-fertig] #wsp-server[data-fertig]', { timeout: 60000 });
  d = await p.evaluate(() => ({ dateien: (document.querySelector('[data-punkt="dateien"]') || {}).dataset, server: document.querySelectorAll('#wsp-server .wsp-punkt[data-gut="ja"]').length, lex: document.querySelectorAll('.wsp-lex').length }));
  pruef(d.dateien && d.dateien.gut === 'nein' && d.server >= 12 && d.lex >= 30, T + 'Prüfseite läuft ohne das Werkzeug: meldet die fehlenden Dateien, prüft den Server trotzdem');
  await k2.close();

  // … und auch, wenn der Server-Teil nicht antwortet
  const k3 = await browser.newContext({ viewport: { width: 1280, height: 860 } });
  await k3.route(/\/api\//, r => r.abort());
  p = await k3.newPage();
  await p.goto(`${B}/werkzeuge/website/pruefung.html?haus=${haus}`);
  await p.waitForSelector('body[data-wsp-fertig]', { timeout: 30000 });
  d = await p.evaluate(() => ({ v: (document.querySelector('[data-punkt="verbindung"]') || {}).dataset, link: !!document.querySelector('[data-punkt="verbindung"] a[href="#lex-keine-verbindung"]'), lex: document.querySelectorAll('.wsp-lex').length }));
  pruef(d.v && d.v.gut === 'nein' && d.link && d.lex >= 30, T + 'Prüfseite ohne Server-Teil: sagt «antwortet nicht», führt zum Lexikon, das Lexikon steht');
  await k3.close();

  // Startfehler: eine Tür zur Prüfung
  p = await neueSeite(k, [], 'Startfehler');
  await p.goto(`${B}${ADR('gibt-es-nicht')}`);
  await p.waitForSelector('[data-ws-startfehler]', { timeout: 15000 });
  pruef(await p.locator('[data-ws-startfehler] a[href*="pruefung.html"]').isVisible() && await p.locator('#ws-speichern').isVisible(), T + 'Startfehler: Meldung mit Tür zur Prüfung, Speichern-Knopf trotzdem zu sehen');
  d = await p.evaluate(() => JSON.parse(localStorage.getItem('ws-fehler') || '[]'));
  pruef(d.length >= 1 && d[d.length - 1].stichwort === 'haus-unbekannt', T + 'Startfehler: das Werkzeug merkt sich den Fehler im Browser, die Prüfung kann ihn lesen');
  await p.close();

  // gesperrte Karte in der Vorschau, ruhige Vorschau
  let karten = null;
  for (const s of b.seiten) { const v = (await api('GET', X(`seite/${haus}/${s.datei}`))).j; if (v.gruppen.some(g => g.stellen.some(st => st.zu === 'karten'))) { karten = s.datei; break; } }
  p = await neueSeite(k, fehler, 'Sperre');
  await p.goto(`${B}${ADR(haus, 'seite=' + karten)}`);
  await p.waitForSelector('#ws-mitte[data-ws-bereit^="b:"]', { timeout: 30000 }); await rahmenBereit(p);
  const bewegung = () => imRahmen(p, 'entwurf', d2 => ({ ruhig: d2.defaultView.matchMedia('(prefers-reduced-motion: reduce)').matches, links: d2.querySelectorAll('link[rel="stylesheet"][href*="assets/"]').length,
    stile: d2.querySelectorAll('style[data-ws-von]').length, rest: /prefers-reduced-motion/.test([...d2.querySelectorAll('style[data-ws-von]')].map(s => s.textContent).join('')),
    laeuft: d2.getAnimations().filter(a => a.playState === 'running' && a.effect && a.effect.getComputedTiming().iterations !== Infinity && a.effect.target && a.effect.target.closest('[data-ws-e]'))
      .map(a => (a.animationName || a.transitionProperty || '?') + ' ' + Math.round(a.effect.getComputedTiming().duration) + 'ms') }));
  /* Beim Aufbau schalten Skripte der Seite kurz um (Reiter, Karten): das darf ausklingen. Nach zweieinhalb Sekunden bewegt sich an keiner Textstelle mehr etwas. */
  await bis(async () => !(await bewegung()).laeuft.length, 2500);
  d = await bewegung();
  pruef(d.ruhig && d.stile >= 1 && !d.links && !d.rest && d.laeuft.length === 0, T + `Vorschau ohne Einblend-Bewegung: die Regeln des Hauses für «weniger Bewegung» gelten immer (${d.stile} Stylesheets umgestellt)`, JSON.stringify(d));
  pruef((await p.locator('#ws-gruppen .ws-gr--zu, #ws-gruppen .ws-st[disabled]').count()) >= 1 && await p.locator(`#ws-gruppen a[href^="${KARTEN_WEG}"]`).count() >= 1, T + 'die Liste der Stellen zeigt die Karte als gesperrt, mit dem Weg zum Werkzeug «karten»');
  const zu = p.frameLocator('iframe[data-ws-frame="entwurf"]').locator('[data-ws-zu="karten"][data-ws-e]').first();
  try { await zu.click({ timeout: 5000 }); } catch (x) { await zu.dispatchEvent('click'); }
  await p.waitForSelector('[data-ws-gesperrt="karten"]', { timeout: 10000 });
  pruef(await p.locator(`[data-ws-gesperrt="karten"] a[href^="${KARTEN_WEG}"]`).isVisible() && (await p.locator('[data-ws-form]').count()) === 0, T + `Karten-Abschnitt (${karten}) ist gesperrt und führt zum Werkzeug «karten»`);
  await p.close();
  pruef(!fehler.length, T + 'keine Fehler in der Konsole', fehler.slice(0, 4).join(' | '));
  await k.close();
}

// ---------------------------------------------------------------- Teil 3: der Ablauf, je Haus × Welt × Breite
async function teilAblauf(browser, haus, welt, breite) {
  const T = `[${haus} · ${welt} · ${breite}] `, id = `${haus[0]}${welt[0]}${breite}`, fehler = [];
  const b = beschreibung(haus), start = b.seiten[0].datei, sp = (b.sprachen || [])[0], sp2 = (b.sprachen || [])[1];
  const info = (await api('GET', X('haus/' + haus))).j, web0 = 'b:' + info.website[0].key;
  const neuK = async () => { const k = await browser.newContext({ viewport: { width: breite, height: breite > 700 ? 900 : 780 } }); await k.addInitScript(w => { try { localStorage.setItem('werkzeuge-welt', w); localStorage.setItem('ws-wer', 'Probe'); } catch (e) { /* ohne Merken */ } }, welt); return k; };
  const kA = await neuK(), kB = await neuK();
  const A = await neueSeite(kA, fehler, 'A');
  try {
    // 1 öffnen: Übersicht wie im Le Bureau
    await A.goto(`${B}${ADR(haus)}`);
    await bereit(A, 'start');
    if (RAHMEN) {
      const k = await A.evaluate(() => ({ name: (document.querySelector('.wo-marke-w b') || {}).textContent, titel: document.title, soll: (window.WO_HAUS.namen || {}).website || WO.name('website'),
        gruss: document.querySelector('.ws-titel h1').textContent, kacheln: document.querySelectorAll('.ws-bereiche .ws-bk').length, aufgaben: document.querySelectorAll('.ws-aufgaben .ws-ag').length,
        sb: !!document.querySelector('.wo-sb.wo-sb--voll .wo-sb__foto img'), rand: document.querySelectorAll('#ws-rand .wo-re').length, maison: !!document.querySelector('#ws-kopf a[href="' + WO.haus.wege.zentrale + '"]') }));
      pruef(k.name === k.soll && k.titel.startsWith(k.soll) && k.sb && k.rand >= 8 && k.maison, T + `Rahmen des Hauses: Kopf «${k.soll}», Startbild mit Aussenfoto, Rand, Weg zur Zentrale`, JSON.stringify(k));
      pruef(/Guten (Morgen|Tag|Abend)\. Was ändern wir heute\?/.test(k.gruss) && k.kacheln === info.website.length && k.aufgaben >= 4, T + `Übersicht: Gruss, ${k.aufgaben} häufige Aufgaben, ${k.kacheln} Bereiche der Website als Kacheln`, JSON.stringify(k));
      await lage(A, T, 'Übersicht');
    } else {
    const kopf = await A.evaluate(() => ({ welt: document.documentElement.getAttribute('data-welt'), titel: document.title, name: document.querySelector('[data-werkzeug="website"]').textContent, knopf: !!document.querySelector('[data-welt-knopf][data-bereit]'),
      gruss: document.querySelector('.ws-titel h1').textContent, kacheln: document.querySelectorAll('.ws-bereiche .ws-bk').length, aufgaben: document.querySelectorAll('.ws-aufgaben .ws-ag').length,
      zeichen: !!document.querySelector('#ws-zeichen > *'), tapete: getComputedStyle(document.body).backgroundImage !== 'none' }));
    pruef(kopf.welt === welt && kopf.name === NAME[welt] && kopf.titel.startsWith(NAME[welt]) && kopf.knopf, T + `öffnet in der Welt ${welt}: «${NAME[welt]}», Modus-Knopf steht`, JSON.stringify(kopf));
    pruef(/Guten (Morgen|Tag|Abend)\. Was ändern wir heute\?/.test(kopf.gruss) && kopf.kacheln === info.website.length && kopf.aufgaben >= 4, T + `Übersicht: Gruss, ${kopf.aufgaben} häufige Aufgaben, ${kopf.kacheln} Bereiche der Website als Kacheln`, JSON.stringify(kopf));
    pruef(kopf.zeichen === !!info.kleid.zeichen && kopf.tapete === !!(info.kleid.tapete && info.welt === welt), T + 'Zeichen des Hauses im Kopf; die Tapete des Hauses liegt nur in seiner eigenen Welt auf dem Grund', JSON.stringify([kopf.zeichen, kopf.tapete]));
    await lage(A, T, 'Übersicht');
    // der Modus-Knopf wechselt Namen, Schrift und Farben, und zurück
    const kleid = () => A.evaluate(() => ({ welt: document.documentElement.getAttribute('data-welt'), name: document.querySelector('[data-werkzeug="website"]').textContent, titel: document.title,
      grund: getComputedStyle(document.body).backgroundColor, schrift: getComputedStyle(document.querySelector('.ws-kopf__titel')).fontFamily, rund: getComputedStyle(document.querySelector('.ws-rand')).borderRadius }));
    const k1 = await kleid();
    await A.locator('[data-welt-knopf]').click();
    const k2 = await kleid(), andere = welt === 'grand' ? 'land' : 'grand';
    pruef(k2.welt === andere && k2.name === NAME[andere] && k2.titel.startsWith(NAME[andere]) && k2.grund !== k1.grund && k2.schrift !== k1.schrift && k2.rund !== k1.rund, T + 'Modus-Knopf wechselt Namen, Schrift, Farben und Rundung', JSON.stringify(k2));
    await A.locator('[data-welt-knopf]').click();
    pruef(JSON.stringify(await kleid()) === JSON.stringify(k1), T + 'Modus-Knopf wechselt zurück');
    }
    await lage(A, T, 'nach dem Wechsel der Welt');
    await speichern(A);
    await A.waitForSelector('[data-ws-meldung]');
    pruef(/Nichts geändert, nichts gespeichert/.test(await A.locator('[data-ws-meldung]').textContent()), T + 'Speichern ohne Eingabe: «Nichts geändert, nichts gespeichert.»');
    await A.locator('[data-ws-meldung] [aria-label="Schliessen"]').click();

    // 2 Bereich öffnen (Kachel), einen Text ändern (Klick in der Seite) und speichern
    await A.locator('.ws-bereiche .ws-bk').first().click();
    await bereit(A, web0); await rahmenBereit(A);
    await lage(A, T, 'Bereich der Website');
    const K = await kandidaten(A);
    pruef(K.length >= 3, T + `Seite im Rahmen: ${K.length} freie Textstellen zum Anklicken gefunden`);
    const neu1 = `${K[0].t} Probe ${id}`;
    await klickStelle(A, K[0]);
    const vorTippen = await A.locator('#ws-speichern').getAttribute('data-ws-lage');
    await tippe(A, 'de', ` Probe ${id}`, false);
    if (sp) await tippe(A, sp.code, `Probe ${sp.code} ${id}`, true);
    pruef(vorTippen === 'ruhig' && await A.locator('#ws-speichern').getAttribute('data-ws-lage') === 'offen' && /1 Eingabe noch nicht gespeichert/.test(await A.locator('#ws-leiste').textContent()), T + 'die Stelle öffnet sich unter ihrer Zeile; die Leiste zählt die offene Eingabe, der Speichern-Knopf zeigt sie');
    const imBild = () => imRahmen(A, 'entwurf', (d, a) => d.querySelector(`[data-ws-e="${a.h}"][data-ws-n="${a.n}"]`).textContent.replace(/\s+/g, ' ').trim(), K[0]);
    pruef(await bis(async () => await imBild() === neu1), T + 'die Seite schreibt beim Tippen mit', await imBild());
    await lage(A, T, 'Stelle gewählt');
    // eine offene Eingabe geht beim Wechsel der Ansicht nicht verloren
    await nav(A, 'start'); await nav(A, web0); await rahmenBereit(A);
    pruef(await A.locator('#ws-speichern').getAttribute('data-ws-lage') === 'offen' && (await A.locator(`#ws-gruppen .ws-st.ws-offen[data-h="${K[0].h}"]`).count()) === 1, T + 'Ansicht gewechselt und zurück: die offene Eingabe ist noch da und an ihrer Zeile markiert');
    await speichern(A);
    await A.waitForSelector('[data-ws-quittung]', { timeout: 20000 });
    let q = await A.evaluate(() => ({ v: document.querySelector('[data-ws-q="vorher"]').textContent, n: document.querySelector('[data-ws-q="nachher"]').textContent, kn: [...document.querySelectorAll('[data-ws-quittung] button')].map(x => x.textContent) }));
    pruef(q.v === K[0].t && q.n === neu1, T + 'Quittung nach dem Speichern: vorher und nachher, Wort für Wort', JSON.stringify(q));
    pruef(q.kn.includes('Vorher/nachher ansehen') && q.kn.includes('Rückgängig'), T + 'Quittung hat «Vorher/nachher ansehen» und «Rückgängig»');
    pruef(await A.locator('#ws-leiste').getAttribute('data-ws-offen') === '1' && (breite <= 560 || await A.locator('#ws-leiste .marke, #ws-leiste .wo-marke').first().isVisible()) && await A.locator('#ws-speichern').getAttribute('data-ws-lage') === 'gespeichert', T + 'Leiste: Entwurf mit 1 Änderung, Marke «Entwurf», Knopf zeigt «Gespeichert»');
    await lage(A, T, 'Quittung');

    // Rückgängig, dann noch einmal speichern
    await A.locator('[data-ws-quittung] button', { hasText: 'Rückgängig' }).click();
    await A.waitForFunction(() => document.querySelector('#ws-leiste').getAttribute('data-ws-offen') === '0');
    pruef((await stand(haus)).offen === false, T + '«Rückgängig» nimmt das Speichern zurück');
    await ruhe(A); await rahmenBereit(A);
    await klickStelle(A, K[0]);
    await tippe(A, 'de', ` Probe ${id}`, false);
    if (sp) await tippe(A, sp.code, `Probe ${sp.code} ${id}`, true);
    await speichern(A);
    await A.waitForSelector('[data-ws-quittung]', { timeout: 20000 });
    await ruhe(A);
    await zuQuittung(A);

    // 3 eine Zeit ändern (Zeiten und Preise) und speichern
    await nav(A, 'zahlen');
    await lage(A, T, 'Zeiten und Preise');
    const zeilen = await A.locator('[data-ws-zahl]').evaluateAll(els => els.map((e, i) => ({ i, t: e.querySelector('.ws-zl__wert').textContent.trim(), orte: +e.getAttribute('data-ws-orte') })).filter(x => /\b\d{1,2}[.:]\d{2}\b/.test(x.t) && x.t.length < 70));
    let zeit = null;
    for (const z of zeilen.slice(0, 10)) {
      await A.locator('[data-ws-zahl]').nth(z.i).locator('.ws-zl__wert').click();
      await A.waitForSelector('[data-ws-form="text"] [data-ws-feld="de"]');
      await A.waitForFunction(t => document.querySelector('[data-ws-form="text"] [data-ws-feld="de"]').textContent.replace(/\s+/g, ' ').trim() === t, z.t, { timeout: 8000 }).catch(() => {});
      if (!(await A.locator('[data-ws-form="text"] [data-ws-feld="de"]').innerHTML()).includes('<')) { zeit = z; break; }
    }
    pruef(!!zeit, T + 'Zeiten und Preise: eine Zeit gefunden', JSON.stringify(zeilen.slice(0, 3)));
    const neuZeit = zeit.t.replace(/(\d{1,2}[.:])(\d{2})/, (m, a, c) => a + String((+c + 7) % 60).padStart(2, '0'));
    pruef(await A.locator('[data-ws-form="text"] [data-ws-orte]').getAttribute('data-ws-orte') === String(zeit.orte), T + `die Angabe nennt ihre ${zeit.orte} Stelle(n)`);
    await tippe(A, 'de', neuZeit, true);
    await speichern(A);
    await A.waitForSelector('[data-ws-quittung]', { timeout: 30000 });
    q = await A.evaluate(() => ({ v: document.querySelector('[data-ws-q="vorher"]').textContent, n: document.querySelector('[data-ws-q="nachher"]').textContent }));
    pruef(q.v === zeit.t && q.n === neuZeit, T + `Zeit geändert: «${zeit.t}» wird «${neuZeit}», Quittung stimmt`, JSON.stringify(q));
    const erwartet = 1 + zeit.orte;
    let s = await stand(haus);
    pruef(s.aenderungen.length === erwartet && await A.locator('#ws-leiste').getAttribute('data-ws-offen') === String(erwartet), T + `Entwurf: ${erwartet} Änderungen (1 Text, die Zeit an ${zeit.orte} Stelle(n))`, s.aenderungen.length);
    if (sp) {
      pruef(s.fehlt > 0 && (await A.locator('#ws-leiste [data-ws-fehlt]').count()) === 1 && /fehlen/.test(await A.locator('[data-ws-nav="sprachen"]').textContent()), T + `Leiste und Rand nennen fehlende Übersetzungen (${s.fehlt})`);
      const zz = s.aenderungen.filter(a => a.nachher === neuZeit);
      pruef(zz.length === zeit.orte && zz.every(a => Object.keys(a.sprachen).length >= 1 && Object.values(a.sprachen).every(Boolean)), T + 'nur die Zahl geändert: die Übersetzungen folgen mit der neuen Zahl (als Vorschlag gezeigt und mitgespeichert)', JSON.stringify(zz[0] && zz[0].sprachen));
    }
    await ruhe(A);
    await zuQuittung(A);

    // 4 neu laden: noch da, und das Werkzeug macht dort weiter, wo man war
    await nav(A, web0); await rahmenBereit(A);
    await A.reload();
    await bereit(A, web0); await rahmenBereit(A);
    pruef(await A.locator('#ws-leiste').getAttribute('data-ws-offen') === String(erwartet), T + 'nach dem Neuladen: Entwurf noch da, gleiche Ansicht');
    pruef(await imRahmen(A, 'entwurf', (d, a) => { const e = d.querySelector(`[data-ws-e="${a.h}"][data-ws-n="${a.n}"]`); return e.textContent.replace(/\s+/g, ' ').trim() + '|' + e.hasAttribute('data-ws-neu'); }, K[0]) === neu1 + '|true', T + 'nach dem Neuladen: die Seite zeigt den geänderten Text, markiert');
    const imBereich = s.aenderungen.filter(a => info.website[0].seiten.some(x => x.datei === a.seite)).length;
    pruef((await A.locator(`#ws-gruppen .ws-st.ws-geaendert[data-h="${K[0].h}"]`).count()) === 1 && (await A.locator(`[data-ws-nav="${web0}"] i, [data-ws-nav="${web0}"] .wo-zahl`).first().textContent()) === String(imBereich), T + `die Liste markiert die geänderte Stelle, der Rand zählt ${imBereich} am Bereich`);

    // 5 Konflikt: A tippt, B speichert zuerst, A speichert danach
    await klickStelle(A, K[1]);
    await tippe(A, 'de', ` Probe A ${id}`, false);
    const Bs = await neueSeite(kB, fehler, 'B');
    await Bs.goto(`${B}${ADR(haus)}`);
    await bereit(Bs, 'start');
    await nav(Bs, web0); await rahmenBereit(Bs);
    await klickStelle(Bs, K[2]);
    await tippe(Bs, 'de', ` Probe B ${id}`, false);
    await speichern(Bs);
    await Bs.waitForSelector('[data-ws-quittung]', { timeout: 20000 });
    await speichern(A);
    await A.waitForSelector('[data-ws-fenster="konflikt"]', { timeout: 20000 });
    s = await stand(haus);
    pruef(s.aenderungen.some(a => a.nachher.endsWith(`Probe B ${id}`)) && !s.aenderungen.some(a => a.nachher.endsWith(`Probe A ${id}`)) && s.aenderungen.length === erwartet + 1, T + 'Konflikt: das Fenster erscheint, die Änderung des anderen steht, nichts wurde überschrieben');
    pruef(/Probe B/.test(await A.locator('[data-ws-fenster="konflikt"]').textContent()), T + 'Konflikt: das Fenster nennt, was von anderer Seite kam');
    await lage(A, T, 'Konflikt-Fenster', true);
    await A.locator('[data-ws-fenster="konflikt"] .kn--d').click();
    await A.waitForSelector('[data-ws-quittung]', { timeout: 20000 });
    s = await stand(haus);
    pruef(s.aenderungen.length === erwartet + 2 && s.aenderungen.some(a => a.nachher.endsWith(`Probe A ${id}`)) && s.aenderungen.some(a => a.nachher.endsWith(`Probe B ${id}`)), T + 'Konflikt gelöst: beide Änderungen liegen im Entwurf');
    await Bs.close();
    await ruhe(A);
    await zuQuittung(A);

    // Rundgang durch jede Ansicht: Überlauf, Auswahl, Knopf
    for (const a of info.bereiche.map(x => 'haus:' + x.key).concat(['hinweis', 'verlauf'], sp ? ['sprachen'] : [])) {
      await nav(A, a);
      if (a.startsWith('haus:')) {
        await A.locator('.ws-eintrag summary').first().click();
        const feld = A.locator('.ws-eintrag[open] .ws-zl__wert:not([disabled])').first();
        if (await feld.count()) { await feld.click(); await A.waitForSelector('.ws-eintrag[open] [data-ws-form]'); await ruhe(A); }
      }
      await lage(A, T, a);
    }
    pruef((await A.locator('[data-ws-nav="sprachen"]').count()) === (sp ? 1 : 0), T + (sp ? 'Sprachen: eigene Ansicht' : 'Haus ohne weitere Sprachen: keine Ansicht «Sprachen»'));
    pruef(Object.keys(b.bereiche).filter(k => b.bereiche[k].an === false).every(k => !info.bereiche.some(x => x.key === k)) && (await A.locator('[data-ws-nav^="haus:"]').count()) === info.bereiche.length, T + `Rand: genau die ${info.bereiche.length} Bereiche des Hauses, ausgeschaltete fehlen`);
    if (sp) {
      const zs = await A.evaluate(() => ({ zeilen: document.querySelectorAll('[data-ws-sp]').length, fehlt: document.querySelectorAll('[data-ws-sp] .ws-fehlt').length }));
      pruef(zs.zeilen === s.aenderungen.length && zs.fehlt === s.fehlt, T + `Sprachen: ${zs.zeilen} Änderungen, ${zs.fehlt} Felder «fehlt» (wie in der Leiste)`, JSON.stringify(zs) + ' ' + s.fehlt);
    }

    // 6 Entwurf & Vergleich: jede Änderung, darunter vorher und nachher mit genau diesen Stellen
    if (breite >= 1180) { await A.locator('#ws-vgl').click(); await bereit(A, 'entwurf'); } else await nav(A, 'entwurf');
    pruef((await A.locator('[data-ws-aenderung]').count()) === s.aenderungen.length, T + `Entwurf: ${s.aenderungen.length} Änderungen, jede einzeln mit vorher und nachher`);
    await A.locator('[data-ws-auswahl="Seite"] .ws-auswahl__knopf').click();
    const opt = A.locator(`[data-ws-auswahl="Seite"] [role="option"][data-wert="${start}"]`);
    if (await opt.getAttribute('aria-selected') === 'true') await A.keyboard.press('Escape'); else { await opt.click(); await bereit(A, 'entwurf'); }
    await rahmenBereit(A);
    await lage(A, T, 'Entwurf & Vergleich');
    const soll = s.aenderungen.filter(a => a.seite === start && a.art === 'text').map(a => a.h + '|' + a.n).sort();
    const marken = fn => imRahmen(A, fn, d => [...d.querySelectorAll('[data-ws-neu]')].map(e => e.getAttribute('data-ws-e') + '|' + e.getAttribute('data-ws-n')).sort());
    const mv = await marken('vorher'), mn = await marken('nachher');
    pruef(JSON.stringify(mv) === JSON.stringify(soll) && JSON.stringify(mn) === JSON.stringify(soll) && soll.length >= 3, T + `Vorher, nachher: markiert sind genau die ${soll.length} geänderten Stellen dieser Seite, auf beiden Seiten`, JSON.stringify({ soll, mv, mn }));
    const text = (z, st) => imRahmen(A, z, (d, a) => d.querySelector(`[data-ws-e="${a.h}"][data-ws-n="${a.n}"]`).textContent.replace(/\s+/g, ' ').trim(), st);
    pruef(await text('vorher', K[0]) === K[0].t && await text('nachher', K[0]) === neu1, T + 'Vorher zeigt den alten, nachher den neuen Text');
    pruef((await A.locator('[data-ws-vgl]').count()) === s.aenderungen.filter(a => a.seite === start).length, T + 'die Liste darüber nennt dieselben Änderungen');

    // 7 veröffentlichen, die Kopie der Seite zeigt den neuen Stand
    await A.locator('#ws-raus').click();
    await A.waitForSelector('[data-ws-fenster="veroeffentlichen"]');
    if (sp) pruef(await A.locator('[data-ws-fehlt-hinweis]').isVisible(), T + 'vor dem Veröffentlichen: Hinweis auf fehlende Übersetzungen');
    await lage(A, T, 'Fenster Veröffentlichen', true);
    await A.locator('#ws-notiz').fill(`Probe ${id}`);
    await A.locator('[data-ws-fenster="veroeffentlichen"] .kn--d').click();
    await A.waitForSelector('[data-ws-veroeffentlicht]', { timeout: 60000 });
    const on = lies(haus, 'online', start).toString('utf8');
    pruef(on.includes(`Probe ${id}`) && on.includes(`Probe A ${id}`) && on.includes(`Probe B ${id}`) && !on.includes('data-ws-'), T + 'veröffentlicht: die Kopie der Seite enthält die neuen Texte, ohne Marken des Werkzeugs');
    const C = await neueSeite(kB, [], 'online');   // die Seite des Hauses selbst: ihre eigenen Abrufe (Wetter, Preise) gibt es auf diesem Server nicht, das ist kein Fehler des Werkzeugs
    await C.goto(`${B}/werkzeuge/website/${PROBE_NAME}/${haus}/online/${start}`, { waitUntil: 'domcontentloaded' });
    pruef((await C.evaluate(() => document.body.textContent.replace(/\s+/g, ' '))).includes(neu1), T + 'die Kopie der Seite zeigt im Browser den neuen Text');
    await C.close();
    const zeitSeiten = s.aenderungen.filter(a => a.nachher === neuZeit).map(a => a.seite);
    pruef(zeitSeiten.length === zeit.orte && zeitSeiten.every(n => lies(haus, 'online', n).toString('utf8').includes(neuZeit)), T + `die neue Zeit steht online auf ${new Set(zeitSeiten).size} Seite(n)`);
    if (sp) {
      pruef(zeitSeiten.every(n => lies(haus, 'online', sp.ordner + '/' + n).toString('utf8').includes(neuZeit)), T + `${sp.code}: die neue Zeit steht auch dort online`);
      const en = lies(haus, 'online', sp.ordner + '/' + start).toString('utf8');
      pruef(en.includes(`Probe ${sp.code} ${id}`) && !en.includes(neu1.slice(-40)), T + `${sp.code}: die Übersetzung steht online`);
      if (sp2) pruef(lies(haus, 'online', sp2.ordner + '/' + start).toString('utf8').includes(`Probe ${id}`), T + `${sp2.code}: ohne Übersetzung steht dort der neue deutsche Text`);
    }
    pruef((await stand(haus)).offen === false && await A.locator('#ws-leiste').getAttribute('data-ws-offen') === '0' && /Veröffentlicht/.test(await A.locator('#ws-lage, #ws-kopf .wo-kopf__mitte small').first().textContent()), T + 'nach dem Veröffentlichen: nichts mehr offen, der Kopf nennt den Tag');

    // 8 unter «Frühere Fassungen» sichtbar
    await bereit(A, 'verlauf');
    await lage(A, T, 'Frühere Fassungen');
    const erste = await A.locator('[data-ws-fassung]').first().textContent();
    pruef(new RegExp(`${erwartet + 2} Unterschiede`).test(erste) && erste.includes(`Probe ${id}`), T + `Frühere Fassungen: der vorige Stand liegt oben, ${erwartet + 2} Unterschiede zu heute, mit Notiz`, erste.slice(0, 200));
    pruef(/Veröffentlicht · Probe/.test(await A.locator('[data-ws-protokoll]').textContent()), T + 'Protokoll: wer veröffentlicht hat');

    // 9 zurückholen, Seite wieder alt
    await A.locator('[data-ws-fassung]').first().locator('button', { hasText: 'Zurückholen' }).click();
    await A.waitForSelector('[data-ws-fenster="zurueckholen"]');
    await A.locator('[data-ws-fenster="zurueckholen"] .kn--d').click();
    await bereit(A, 'entwurf');
    pruef(lies(haus, 'online', start).toString('utf8') === on && await A.locator('#ws-leiste').getAttribute('data-ws-offen') === String(erwartet + 2), T + 'Zurückholen: liegt als Entwurf da, online noch unverändert');
    await A.locator('#ws-raus').click();
    await A.waitForSelector('[data-ws-fenster="veroeffentlichen"]');
    await A.locator('[data-ws-fenster="veroeffentlichen"] .kn--d').click();
    await A.waitForSelector('[data-ws-veroeffentlicht]', { timeout: 60000 });
    const rest = onlineGleichGrundlage(haus);
    pruef(!rest.length && grundlageHash(haus) === GRUND[haus], T + `zurückgeholt und veröffentlicht: alle ${b.dateien.length} Dateien wieder Byte für Byte wie gebaut, Grundlage unberührt`, rest.slice(0, 4));
    /* Der Browser schreibt jede 4xx-Antwort als Zeile in die Konsole. Die 409 beim Konflikt ist die erwartete Antwort des Speichers:
       genau diese eine Zeile ist erlaubt, jede andere zählt als Fehler. */
    const konflikt = fehler.filter(f => /^A: Failed to load resource: the server responded with a status of 409/.test(f));
    const rest2 = fehler.filter(f => !konflikt.includes(f));
    pruef(konflikt.length === 1 && !rest2.length, T + 'keine Fehler in der Konsole (ausser der einen erwarteten Zeile zur 409 des Konflikts)', rest2.slice(0, 4).join(' | ') + ' · 409: ' + konflikt.length);
  } catch (e) {
    const bild = path.join(TMP, `fehler-${id}.png`);
    await A.screenshot({ path: bild }).catch(() => {});
    pruef(false, T + 'Ablauf bricht ab', `${e.message.split('\n')[0]} · Bild: ${bild} · Konsole: ${fehler.slice(0, 3).join(' | ')}`);
    await zurueckAufAnfang(haus);
  }
  await kA.close(); await kB.close();
}

// ---------------------------------------------------------------- Lauf
(async () => {
  try { await fetch(B + '/api/haus/x'); console.error(`Port ${PORT} ist belegt. Der Lauf beendet nichts, was er nicht selbst gestartet hat. Bitte den anderen Lauf abwarten.`); process.exit(2); } catch (e) { /* frei */ }
  const umgebung = Object.assign({}, process.env, { WERKZEUGE_DATEN: path.join(TMP, 'daten'), WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' });
  console.log(`Wegwerf-Kopie der Seiten: ${PROBE_NAME} · Wegwerf-Daten: ${TMP}`);
  KOPIERT = Date.now();
  console.log(execFileSync('python3', [path.join(HIER, 'probe.py'), ...HAEUSER], { env: umgebung, encoding: 'utf8' }).trim());
  const server = spawn('python3', [SERVER_SKRIPT || path.join(WURZEL, 'unterbau', 'serve.py'), String(PORT)], { cwd: SERVER_SKRIPT ? path.dirname(path.dirname(path.dirname(SERVER_SKRIPT))) : WURZEL, env: umgebung, stdio: ['ignore', 'ignore', fs.openSync(path.join(TMP, 'server.log'), 'w')] });
  let browser = null;
  const ende = async code => {
    if (browser) await browser.close().catch(() => {});
    server.kill();   // nur der eigene Server, per PID
    fs.rmSync(PROBE, { recursive: true, force: true });
    process.exit(code);
  };
  process.on('SIGINT', () => ende(130));
  try {
    for (let i = 0; i < 50; i++) { try { await fetch(B + '/api/haus/' + HAEUSER[0]); break; } catch (e) { await warte(200); } }
    console.log(`Server gestartet (PID ${server.pid}) auf ${B}`);
    const pw = require(findePlaywright());
    browser = process.env.MOTOR === 'webkit' ? await pw.webkit.launch({ headless: true }) : await pw.chromium.launch({ headless: true, executablePath: shell() });   // MOTOR=webkit: derselbe Lauf im Safari-Kern
    ohneHaus();
    lexikonVollstaendig();
    for (const haus of HAEUSER) {
      const t = Date.now();
      await teilServer(haus);
      await teilSeiten(browser, haus);
      console.log(`${haus}: Server und Prüfseite geprüft (${Math.round((Date.now() - t) / 1000)} s)`);
      for (const welt of WELTEN) for (const breite of BREITEN) {
        const t2 = Date.now(), vorher = schlecht.length;
        await teilAblauf(browser, haus, welt, breite);
        console.log(`${haus} · ${welt} · ${breite}: ${schlecht.length === vorher ? 'in Ordnung' : (schlecht.length - vorher) + ' FEHLEN'} (${Math.round((Date.now() - t2) / 1000)} s)`);
      }
    }
  } catch (e) {
    pruef(false, 'Der Lauf bricht ab', e.stack || e);
  }
  console.log(schlecht.length ? `NICHT BESTANDEN · ${schlecht.length} von ${gezaehlt} Prüfungen fehlen · Bilder und Server-Ausgabe: ${TMP}` : `BESTANDEN · ${gezaehlt} Prüfungen · Häuser ${HAEUSER.join(', ')} · Welten ${WELTEN.join(', ')} · Breiten ${BREITEN.join(', ')}`);
  await ende(schlecht.length ? 1 : 0);
})();
