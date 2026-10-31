/* pruef.js · fester Durchlauf des Werkzeugs «karten». Start:  node werkzeuge/karten/pruef.js   (aus dem Ordner _Werkzeuge)

   Läuft unsichtbar auf Port 8973 mit Wegwerf-Daten (WERKZEUGE_DATEN), nie gegen die echten. Den eigenen Server beendet
   der Lauf am Ende per PID. Kein Fenster, nichts wird hochgeladen. Ist der Port belegt, bricht der Lauf ab.

   Je Haus (gasterntal, beau-rivage) × Welt (grand, land) × Breite (1440, 390, 320):
     öffnen → Preis ändern → speichern → neu laden, noch da → Konflikt bei zwei gleichzeitigen Änderungen →
     Vorher / nachher → veröffentlichen → PDF enthält den neuen Preis → im Verlauf sichtbar → zurückholen → PDF wieder alt.
     Dazu: kein seitlicher Überlauf, keine Fehler in der Konsole, keine Auswahl und kein Dialog des Betriebssystems,
     die Karte folgt der Welt des Hauses, der Knopf wechselt die Welt des Werkzeugs.
   Einmal je Haus: neuer Eintrag (geführt, mit «So steht es auf der Karte»), ausblenden, zurücknehmen, verschieben, Klick in die
     Karte, direkt in der Karte schreiben, Daten der Karte, Karte einrichten, neue Rubrik, «nichts geändert», eingeschleuste
     Zeichen, Umbruchregeln und Vorschau gegen PDF für jede Karte, Kontrolle des veröffentlichten Stands.
   Einmal: ein drittes Haus aus einer Datei, ohne dass am Werkzeug etwas geändert wird; Sprachfassung wird als veraltet erkannt;
     Start ohne Haus und mit kaputtem Entwurf.

   Ausgabe: je Prüfung eine Zeile, am Ende BESTANDEN oder NICHT BESTANDEN (Exitcode 1). Bericht: _qa/pruef-letzter-lauf.txt
   Nur zum Entwickeln: PRUEF_NUR=werkzeug lässt die zwölf Durchläufe aus (zählt nicht als bestanden). */
const fs = require('fs'), path = require('path'), os = require('os'), { spawn, execFileSync } = require('child_process');
const HIER = __dirname, WURZEL = path.resolve(HIER, '..', '..'), PORT = 8973, BASIS = `http://127.0.0.1:${PORT}`;
const HAEUSER = {
  gasterntal: { welt: 'land', karte: 'karte-2026', gericht: 'Tagesssuppe', nicht: 'Schwynswurscht', alt: '10.50', tippe: r => `${11 + r}.5`, neu: r => `${11 + r}.50`, zweites: 'Linseneintopf', zweitesTippe: r => `${40 + r}`, zweitesNeu: r => `${40 + r}.00`, drittes: 'Hobelchäs', rubrik: 'Suppä' },
  'beau-rivage': { welt: 'grand', karte: 'ambiance', gericht: 'Mango Garnelen Salat', nicht: '\u0000', alt: 'CHF 18', tippe: r => `${30 + r}`, neu: r => `CHF ${30 + r}`, zweites: 'Citrus Salat', zweitesTippe: r => `${50 + r}`, zweitesNeu: r => `CHF ${50 + r}`, drittes: 'Burrata Salat', rubrik: 'Vorspeisen' }
};
const NAMEN = { grand: 'La Carte', land: 'Die Tafel' };
const zeilen = []; let schlecht = 0, gezaehlt = 0, ort = '';
function pruef(wahr, was, mehr) { gezaehlt++; if (!wahr) schlecht++; const z = `${wahr ? 'gut  ' : 'FEHLT'} ${ort} · ${was}${!wahr && mehr ? ' → ' + mehr : ''}`; zeilen.push(z); if (!wahr) console.log(z); return wahr; }

function finde() { const npx = path.join(os.homedir(), '.npm/_npx'); for (const d of fs.existsSync(npx) ? fs.readdirSync(npx) : []) { const p = path.join(npx, d, 'node_modules/playwright'); if (fs.existsSync(p)) return p; } throw new Error('Playwright nicht gefunden (einmal: npx -y playwright --version)'); }
function shell() { const c = path.join(os.homedir(), 'Library/Caches/ms-playwright'); if (!fs.existsSync(c)) return undefined; for (const n of fs.readdirSync(c).filter(n => n.startsWith('chromium_headless_shell-')).sort().reverse()) { const p = path.join(c, n, 'chrome-headless-shell-mac-arm64/chrome-headless-shell'); if (fs.existsSync(p)) return p; } return undefined; }
/* Text einer PDF. Über eine Datei im Wegwerf-Ordner und mit Frist: über die Standardeingabe blieb pdftotext unter Last einmal ohne Ende stehen. */
let ABLAGE = os.tmpdir(), pdfNr = 0;
function pdfText(base64) {
  const datei = path.join(ABLAGE, `pruef-${process.pid}-${++pdfNr}.pdf`);
  fs.writeFileSync(datei, Buffer.from(base64, 'base64'));
  try { return execFileSync('pdftotext', ['-layout', datei, '-'], { timeout: 30000, stdio: ['ignore', 'pipe', 'pipe'] }).toString('utf8'); } finally { fs.rmSync(datei, { force: true }); }
}
const api = async (methode, weg, koerper) => { const r = await fetch(BASIS + weg, { method: methode, headers: koerper ? { 'Content-Type': 'application/json' } : {}, body: koerper ? JSON.stringify(koerper) : undefined }); return { status: r.status, d: await r.json() }; };
async function pdfZeilen(haus, karte) { const r = await api('GET', `/api/x/karten/pdf/${haus}/${karte}`); if (r.status !== 200) return { fehler: JSON.stringify(r.d).slice(0, 200), zeilen: [] }; return { zeilen: pdfText(r.d.pdf).split('\n'), nachgedruckt: r.d.nachgedruckt, seiten: r.d.seiten }; }
const zeileMit = (zz, name, nicht) => zz.find(z => z.includes(name) && !z.includes(nicht)) || '';

async function seite(kontext, haus, erlaubt) {   // erlaubt: Meldung der Konsole, die in diesem Schritt absichtlich entsteht
  const p = await kontext.newPage(); p.fehler = []; p.dialoge = 0;
  p.on('pageerror', e => p.fehler.push(String(e)));
  p.on('console', m => { if (m.type() === 'error' && !(erlaubt && erlaubt.test(m.text()))) p.fehler.push(m.text()); });
  p.on('dialog', d => { p.dialoge++; d.dismiss().catch(() => {}); });
  await p.goto(`${BASIS}/werkzeuge/karten/?haus=${haus}`, { waitUntil: 'load' });
  await bereit(p);
  return p;
}
async function bereit(p) { await p.waitForFunction(() => window.KT && KT.bereit() && KT.vorschau(), null, { timeout: 12000 }); await p.waitForTimeout(350); }
const reihe = (p, name) => p.locator('.kt-r').filter({ has: p.locator('.kt-r__t > b', { hasText: name }) }).first();
const ueberlauf = p => p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
const quittung = (p, text) => p.locator('#kt-meldung .kt-quit', { hasText: text }).last().waitFor({ timeout: 15000 }).then(() => true, () => false);
const meldungen = p => p.locator('#kt-meldung').innerText();
const leisteText = p => p.locator('#kt-leiste').innerText();
const fensterText = p => p.locator('#kt-fenster').innerText();
const fensterZu = p => p.locator('#kt-fenster').waitFor({ state: 'hidden', timeout: 8000 }).then(() => true, () => false);
const vorschauText = p => p.frameLocator('#kt-vorschau').locator('body').innerText();
const mitte = l => l.evaluate(el => el.scrollIntoView({ block: 'center' }));   // in die Mitte holen: am unteren Rand liegt die Leiste darüber
const taste = async (p, name, akt) => { const r = reihe(p, name); await mitte(r); await r.hover(); await r.locator(`[data-akt="${akt}"]`).click(); };   // die Tasten einer Zeile erscheinen beim Überfahren
async function preisAendern(p, name, tippe) {
  await mitte(reihe(p, name)); await reihe(p, name).locator('.kt-r__t').click();
  await p.waitForFunction(() => document.activeElement && document.activeElement.id === 'f-name', null, { timeout: 5000 }).catch(() => {});   // das Fenster setzt die Schreibmarke kurz nach dem Öffnen ins erste Feld; erst danach tippen
  await p.locator('#kt-fenster #f-preis, #kt-fenster [data-preis]').first().fill(tippe);
  await p.click('#f-ok');
}
async function veroeffentliche(p, notiz) {
  await p.click('#kt-leiste [data-akt="veroeffentlichen"]');
  await p.fill('#v-wer', 'Prüflauf'); await p.fill('#v-notiz', notiz);
  await p.click('#v-ok');
  const gut = await p.locator('#v-fertig').waitFor({ timeout: 30000 }).then(() => true, () => false);
  if (gut) await p.click('#kt-fenster .kt-fenster__kn [data-zu]');
  return gut;
}
const amEnde = el => { const d = el.ownerDocument, r = d.createRange(); r.selectNodeContents(el); r.collapse(false); const s = d.getSelection(); s.removeAllRanges(); s.addRange(r); };

async function durchlauf(b, haus, welt, breite, r) {
  const H = HAEUSER[haus]; ort = `${haus} · ${welt} · ${breite}`;
  const kontext = await b.newContext({ viewport: { width: breite, height: 900 } });
  await kontext.addInitScript(x => { try { localStorage.setItem('werkzeuge-welt', x); } catch (e) {} }, welt);
  const anfang = (await api('GET', `/api/stand/${haus}/karten`)).d;
  const p = await seite(kontext, haus);
  // öffnen
  pruef(await p.evaluate(() => document.documentElement.getAttribute('data-welt')) === welt, 'öffnet in der gewählten Welt');
  pruef((await p.locator('.kt-oben__marke b').innerText()).trim().toLowerCase() === NAMEN[welt].toLowerCase(), `heisst «${NAMEN[welt]}»`);
  pruef(await ueberlauf(p) <= 0, 'kein seitlicher Überlauf', String(await ueberlauf(p)));
  pruef(await p.locator('select, datalist, input[type=date], input[type=time], input[type=datetime-local], input[type=month], input[type=week], input[type=color], input[type=file], input[type=range], input[type=checkbox], input[type=radio]').count() === 0, 'keine Auswahl des Betriebssystems');
  pruef(await p.frameLocator('#kt-vorschau').locator('html').getAttribute('data-welt') === H.welt, 'die Karte folgt der Welt des Hauses');
  pruef((await vorschauText(p)).includes(H.alt), 'Vorschau zeigt den alten Preis');
  // Kleid des Hauses: sein Zeichen im Werkzeug und auf der Karte, sein Foto an der Karte, seine Tapete nur in seiner eigenen Welt
  const kleid = await p.evaluate(() => ({ zeichen: document.querySelectorAll('#kt-oben .kt-zeichen--bild svg, #kt-kopf .kt-zeichen--bild svg').length, foto: document.querySelectorAll('#kt-rand .kt-kw__f--foto').length, tapete: getComputedStyle(document.documentElement).getPropertyValue('--kt-tapete').trim(), karte: document.getElementById('kt-vorschau').contentDocument.querySelectorAll('.kt-deck__m svg, .kt-leiste__z svg').length }));
  pruef(kleid.zeichen === 2 && kleid.foto >= 1 && kleid.karte >= 2, 'Zeichen des Hauses in Kopfleiste, Kopf und auf der Karte, Foto an der Karte', JSON.stringify(kleid));
  pruef(haus === 'beau-rivage' ? !!kleid.tapete === (welt === H.welt) : !kleid.tapete, 'Tapete des Hauses liegt nur in seiner eigenen Welt auf dem Raum', kleid.tapete);
  const vs = await p.evaluate(() => KT.vorschau());
  pruef(vs.regeln.length === 0 && vs.ueberlauf.length === 0, 'Umbruch: kein Gericht allein, keine Rubrik getrennt, nichts läuft über', JSON.stringify(vs.regeln.concat(vs.ueberlauf)));
  // Preis ändern, speichern
  await preisAendern(p, H.gericht, H.tippe(r));
  pruef(await quittung(p, 'Gericht gespeichert'), 'Quittung nach dem Speichern');
  const qt = await meldungen(p);
  pruef(qt.includes(H.neu(r)) && qt.includes(H.alt), 'Quittung nennt alten und neuen Preis in der Schreibweise des Hauses', qt);
  pruef(/Rückgängig/i.test(qt) && /Vorher \/ nachher/i.test(qt), 'Quittung bietet «Rückgängig» und «Vorher / nachher»');
  pruef((await reihe(p, H.gericht).innerText()).includes(H.neu(r)), 'Liste zeigt den neuen Preis');
  pruef(/Entwurf/i.test(await leisteText(p)) && /1 Änderung/.test(await leisteText(p)), 'Leiste: Entwurf, 1 Änderung', await leisteText(p));
  pruef((await api('GET', `/api/stand/${haus}/karten`)).d.kennung_live === anfang.kennung_live, 'veröffentlichter Stand unberührt');
  await p.waitForFunction(x => document.getElementById('kt-vorschau').contentDocument.body.innerText.includes(x), H.neu(r), { timeout: 8000 }).catch(() => {});
  pruef((await vorschauText(p)).includes(H.neu(r)), 'Vorschau zeigt den neuen Preis');
  // neu laden, noch da
  await p.reload({ waitUntil: 'load' }); await bereit(p);
  pruef((await reihe(p, H.gericht).innerText()).includes(H.neu(r)), 'nach neuem Laden noch da');
  // Konflikt: zwei Seiten, beide mit demselben Stand; die erste speichert, die zweite will danach speichern
  const q = await seite(kontext, haus, /409 \(Conflict\)/);   // der Browser vermerkt die absichtlich ausgelöste Antwort 409
  await preisAendern(p, H.zweites, H.zweitesTippe(r));
  pruef(await quittung(p, H.zweitesNeu(r)), 'erste Seite speichert eine zweite Änderung');
  const dazwischen = (await api('GET', `/api/stand/${haus}/karten`)).d.kennung_entwurf;
  await taste(q, H.drittes, 'aus');
  const kf = await q.locator('#kt-fenster', { hasText: 'Inzwischen hat jemand anderes gespeichert' }).waitFor({ timeout: 8000 }).then(() => true, () => false);
  pruef(kf && /stichwort: konflikt/i.test(await fensterText(q)), 'zweite Seite: Konflikt wird gemeldet, mit Stichwort', await fensterText(q));
  pruef((await api('GET', `/api/stand/${haus}/karten`)).d.kennung_entwurf === dazwischen, 'Konflikt hat nichts überschrieben');
  await q.click('#k-neu'); await fensterZu(q); await q.waitForTimeout(500);
  pruef((await reihe(q, H.zweites).innerText()).includes(H.zweitesNeu(r)) && !/Ausgeblendet/.test(await reihe(q, H.drittes).innerText()), 'zweite Seite zeigt nach dem Laden den Stand der ersten, ohne die abgewiesene Änderung');
  pruef(q.fehler.length === 0 && q.dialoge === 0, 'zweite Seite: keine Fehler in der Konsole (ausser der absichtlichen Antwort 409), kein Dialog des Betriebssystems', JSON.stringify(q.fehler));
  await q.close();
  // Vorher / nachher
  await p.click('#kt-leiste [data-akt="vgl"]');
  const vt = await fensterText(p);
  pruef(vt.includes(H.alt) && vt.includes(H.neu(r)) && vt.includes(H.zweitesNeu(r)) && /2 Stellen im Entwurf/.test(vt), 'Vorher / nachher zeigt beide Änderungen mit altem und neuem Preis');
  pruef(await ueberlauf(p) <= 0, 'kein seitlicher Überlauf (Fenster)');
  await p.click('#kt-fenster .kt-fenster__kn [data-zu]');
  // veröffentlichen
  const notiz = `Prüflauf ${haus} ${welt} ${breite}`;
  pruef(await veroeffentliche(p, notiz), 'veröffentlicht, Bestätigung mit Seitenzahl');
  const nach = (await api('GET', `/api/stand/${haus}/karten`)).d;
  pruef(!nach.offen && nach.entwurf === null && nach.kennung_live === dazwischen, 'live ist genau der geprüfte Entwurf, kein Entwurf mehr offen');
  let pdf = await pdfZeilen(haus, H.karte);
  pruef(pdf.nachgedruckt === false, 'die PDF lag schon bereit (beim Veröffentlichen gedruckt)', pdf.fehler);
  pruef(zeileMit(pdf.zeilen, H.gericht, H.nicht).includes(H.neu(r)), 'PDF: der neue Preis steht in der Zeile des Gerichts', zeileMit(pdf.zeilen, H.gericht, H.nicht));
  pruef(zeileMit(pdf.zeilen, H.zweites, '\u0000').includes(H.zweitesNeu(r)), 'PDF: auch die zweite Änderung steht in ihrer Zeile');
  pruef((await api('GET', `/api/x/karten/kontrolle/${haus}`)).d.gut === true, 'Kontrolle: Form stimmt, jede PDF = Daten');
  await p.click('#kt-oben [data-akt="pdf"]');
  pruef(await p.locator('#kt-meldung a[href^="blob:"]').waitFor({ timeout: 15000 }).then(() => true, () => false), '«PDF öffnen» liefert die PDF');
  // im Verlauf sichtbar
  await p.click('#kt-oben [data-akt="verlauf"]');
  await p.locator('#vl .kt-verlauf__z').first().waitFor({ timeout: 8000 });
  pruef((await p.locator('#vl .kt-verlauf__z').first().innerText()).toLowerCase().includes(notiz.toLowerCase()), 'im Verlauf sichtbar, mit Name und Notiz', await p.locator('#vl .kt-verlauf__z').first().innerText());
  // zurückholen
  await p.locator('#vl .kt-verlauf__z').first().locator('[data-d]').click();
  pruef(await quittung(p, 'Fassung im Entwurf'), 'zurückgeholt: liegt als Entwurf vor, noch nicht online');
  pruef((await api('GET', `/api/stand/${haus}/karten`)).d.kennung_live === dazwischen, 'Zurückholen allein ändert die veröffentlichte Karte nicht');
  pruef(await veroeffentliche(p, 'zurück'), 'frühere Fassung veröffentlicht');
  pdf = await pdfZeilen(haus, H.karte);
  const z = zeileMit(pdf.zeilen, H.gericht, H.nicht);
  pruef(z.includes(H.alt) && !z.includes(H.neu(r)), 'PDF wieder alt', z);
  pruef((await api('GET', `/api/stand/${haus}/karten`)).d.kennung_live === anfang.kennung_live, 'Daten wieder genau wie vor dem Durchlauf');
  // Modus-Knopf
  await p.click('[data-welt-knopf]'); await p.waitForTimeout(200);
  const andere = welt === 'grand' ? 'land' : 'grand';
  pruef(await p.evaluate(() => document.documentElement.getAttribute('data-welt')) === andere && (await p.locator('.kt-oben__marke b').innerText()).trim().toLowerCase() === NAMEN[andere].toLowerCase(), 'Modus-Knopf wechselt Welt und Namen');
  pruef(await p.frameLocator('#kt-vorschau').locator('html').getAttribute('data-welt') === H.welt, 'die Karte bleibt dabei in der Welt des Hauses');
  pruef(await ueberlauf(p) <= 0, 'kein seitlicher Überlauf nach dem Wechsel');
  pruef(p.fehler.length === 0, 'keine Fehler in der Konsole', JSON.stringify(p.fehler));
  pruef(p.dialoge === 0, 'kein Dialog des Betriebssystems');
  await kontext.close();
}

async function werkzeug(b, haus) {     // einmal je Haus, am Rechner, in der Welt des Hauses
  const H = HAEUSER[haus]; ort = `${haus} · Werkzeug`;
  const kontext = await b.newContext({ viewport: { width: 1440, height: 900 } });
  await kontext.addInitScript(x => { try { localStorage.setItem('werkzeuge-welt', x); } catch (e) {} }, H.welt);
  const anfang = (await api('GET', `/api/stand/${haus}/karten`)).d;
  const p = await seite(kontext, haus);
  // nichts geändert
  await mitte(reihe(p, H.gericht)); await reihe(p, H.gericht).locator('.kt-r__t').click();
  await p.locator('#kt-mini').waitFor(); await p.waitForFunction(() => { const f = document.getElementById('kt-mini'); return f && f.contentDocument && f.contentDocument.body && f.contentDocument.body.innerText.trim().length > 3; }, null, { timeout: 20000 }).catch(() => {});
  pruef((await p.frameLocator('#kt-mini').locator('body').innerText()).includes(H.gericht) && await p.frameLocator('#kt-mini').locator('html').getAttribute('data-welt') === H.welt, 'Fenster zeigt «So steht es auf der Karte», in der Welt des Hauses');
  await p.click('#f-ok');
  pruef(await quittung(p, 'Nichts geändert, nichts gespeichert.'), 'ohne Änderung: «Nichts geändert, nichts gespeichert.»');
  pruef((await api('GET', `/api/stand/${haus}/karten`)).d.entwurf === null, 'ohne Änderung entsteht kein Entwurf');
  await p.click('#kt-leiste [data-akt="speichern"]');
  pruef(await quittung(p, 'Alles ist gespeichert.'), 'der Knopf «Alles gespeichert» ist immer da und sagt, dass nichts offen ist');
  // Klick in die Karte öffnet den Eintrag
  await p.frameLocator('#kt-vorschau').locator('[data-k$=".name"]', { hasText: H.gericht }).first().click();
  pruef(await p.locator('#kt-fenster #f-name').inputValue().then(x => x.includes(H.gericht), () => false), 'Klick auf einen Text der Karte öffnet den Eintrag');
  await p.click('#kt-fenster .kt-fenster__kn [data-zu]');
  // neuer Eintrag: Rubrik wählen, dann das Fenster mit der Vorschau
  await p.evaluate(() => scrollTo(0, 0));
  await p.click('[data-akt="neu"]');
  await p.locator('#g-r button', { hasText: H.rubrik }).first().click();
  await p.waitForFunction(() => document.activeElement && document.activeElement.id === 'f-name', null, { timeout: 5000 }).catch(() => {});
  await p.fill('#f-name', 'Prüfgericht'); await p.fill('#f-de', 'Zeile der Prüfung'); await p.fill('#f-en', 'Line of the check'); await p.fill('#f-preis', '9');
  await p.click('#f-al-auf'); await p.click('#f-allergene [data-al="milch"]');
  await p.waitForFunction(() => { const f = document.getElementById('kt-mini'); return f && f.contentDocument && /Enthält: Milch/.test(f.contentDocument.body.innerText); }, null, { timeout: 8000 }).catch(() => {});
  const schau = await p.frameLocator('#kt-mini').locator('body').innerText();
  const neun = await p.evaluate(() => KT.preisForm('9', ['CHF 18', 'CHF 15'])) === 'CHF 9' && await p.evaluate(() => KT.preisForm('9', ['10.50', '16.00'])) === '9.00' && await p.evaluate(() => KT.preisForm('12,5', ['11,5', '9'])) === '12,5';
  pruef(neun, 'Preis in der Schreibweise des Hauses (CHF 9 · 9.00 · 12,5)');
  pruef(schau.includes('Prüfgericht') && /Enthält: Milch/.test(schau) && schau.includes('Line of the check'), 'das Fenster zeigt den neuen Eintrag, wie er gedruckt wird, bevor er gespeichert ist', schau);
  await p.click('#f-ok');
  pruef(await quittung(p, 'Gericht auf der Karte'), 'neuer Eintrag gespeichert');
  await p.waitForFunction(() => document.getElementById('kt-vorschau').contentDocument.body.innerText.includes('Prüfgericht'), null, { timeout: 8000 }).catch(() => {});
  const vt = await vorschauText(p);
  pruef(vt.includes('Prüfgericht') && vt.includes('Line of the check') && vt.includes('Enthält: Milch'), 'neuer Eintrag steht in der Karte, mit englischer Zeile und Allergen');
  pruef(/neu/i.test((await reihe(p, 'Prüfgericht').locator('.kt-chip').allInnerTexts()).join(' ')), 'in der Liste als «Neu» gekennzeichnet');
  let vs = await p.evaluate(() => KT.vorschau());
  pruef(vs.regeln.length === 0 && vs.ueberlauf.length === 0, 'Umbruch stimmt auch mit dem neuen Eintrag', JSON.stringify(vs.regeln));
  // ausblenden statt löschen
  await taste(p, 'Prüfgericht', 'aus');
  pruef(await quittung(p, 'Ausgeblendet'), 'ausgeblendet, mit Quittung');
  await p.waitForFunction(() => !document.getElementById('kt-vorschau').contentDocument.body.innerText.includes('Prüfgericht'), null, { timeout: 8000 }).catch(() => {});
  pruef(!(await vorschauText(p)).includes('Prüfgericht') && await reihe(p, 'Prüfgericht').count() === 1, 'ausgeblendet: nicht mehr auf der Karte, in der Liste noch da');
  // Rückgängig
  await p.locator('#kt-meldung .kt-quit', { hasText: 'Ausgeblendet' }).last().locator('button', { hasText: 'Rückgängig' }).click();
  pruef(await quittung(p, 'Zurückgenommen'), '«Rückgängig» nimmt die letzte Änderung zurück');
  await p.waitForFunction(() => document.getElementById('kt-vorschau').contentDocument.body.innerText.includes('Prüfgericht'), null, { timeout: 8000 }).catch(() => {});
  pruef((await vorschauText(p)).includes('Prüfgericht'), 'nach Rückgängig wieder auf der Karte');
  // entfernen: mit Rückfrage, und «Rückgängig» holt es zurück
  await taste(p, 'Prüfgericht', 'weg');
  const rf = /blenden Sie es lieber aus/.test(await fensterText(p));
  await p.click('#ja');
  pruef(rf && await quittung(p, 'Von der Karte genommen') && await reihe(p, 'Prüfgericht').waitFor({ state: 'detached', timeout: 8000 }).then(() => true, () => false), 'entfernen: Rückfrage rät zum Ausblenden, danach ist der Eintrag aus Liste und Entwurf');
  await p.locator('#kt-meldung .kt-quit', { hasText: 'Von der Karte genommen' }).last().locator('button', { hasText: 'Rückgängig' }).click();
  pruef(await reihe(p, 'Prüfgericht').waitFor({ timeout: 10000 }).then(() => true, () => false), 'entfernt und zurückgenommen: der Eintrag ist wieder da');
  await p.waitForTimeout(500);
  // Schalter Karte / Website wie im Original: die Website-Ansicht sagt, dass noch kein Haus angeschlossen ist
  await p.evaluate(() => scrollTo(0, 0)); await p.click('.kt-ansicht [data-ansicht="website"]');
  const web = await p.locator('#kt-web').isVisible() && await p.locator('#kt-seiten').isHidden() && /noch nicht angeschlossen/i.test(await p.locator('#kt-vzahl').innerText());
  await p.click('.kt-ansicht [data-ansicht="karte"]'); await p.waitForTimeout(500);
  pruef(web && await p.locator('#kt-seiten').isVisible() && /wie in der pdf/i.test(await p.locator('#kt-vzahl').innerText()), 'Schalter «Karte / Website»: Website sagt, dass sie noch nicht angeschlossen ist; Karte zeigt wieder die Seiten');
  // verschieben
  const vorher = await p.locator('.kt-r__t > b').allInnerTexts();
  await taste(p, 'Prüfgericht', 'hoch');
  pruef(await quittung(p, 'Reihenfolge gespeichert'), 'verschoben, mit Quittung');
  const danach = await p.locator('.kt-r__t > b').allInnerTexts();
  pruef(danach.indexOf('Prüfgericht') === vorher.indexOf('Prüfgericht') - 1, 'steht eine Zeile höher');
  // direkt in der Karte schreiben
  await p.click('[data-m="frei"]'); await p.waitForTimeout(900);
  pruef(await p.locator('body').evaluate(x => x.classList.contains('kt-frei')) && await p.locator('#kt-liste').isHidden(), 'Weg «Fortgeschritten»: die Liste weicht, die Karte füllt die Fläche');
  const stelle = p.frameLocator('#kt-vorschau').locator('[data-k$=".name"]', { hasText: 'Prüfgericht' }).first();
  await stelle.click(); await stelle.evaluate(amEnde); await p.keyboard.type(' direkt');
  pruef(/Nicht gespeicherte Änderungen/.test(await leisteText(p)), 'Leiste meldet Geschriebenes als noch nicht gespeichert', await leisteText(p));
  await p.click('#kt-leiste [data-akt="speichern"]');
  await p.click('[data-m="einfach"]');     // sofort danach, noch während gespeichert wird: der Wechsel wartet das Speichern ab
  pruef(await quittung(p, 'Im Entwurf gespeichert'), 'Geschriebenes gespeichert');
  await p.waitForTimeout(600);
  pruef(!(await p.locator('body').evaluate(x => x.classList.contains('kt-frei'))) && await p.locator('#kt-fenster').isHidden(), 'Wechsel des Wegs gleich nach «Speichern»: wartet das Speichern ab, keine Rückfrage, nichts verloren');
  // Wechsel mit ungespeicherter Eingabe: Rückfrage; «Abbrechen» bleibt und verliert nichts, «Speichern» speichert und wechselt
  for (const speichernJa of [false, true]) {
    const davor = (await api('GET', `/api/stand/${haus}/karten`)).d.kennung_entwurf;
    if (!(await p.locator('body').evaluate(x => x.classList.contains('kt-frei')))) { await p.click('[data-m="frei"]'); await p.waitForTimeout(900); }
    const st2 = p.frameLocator('#kt-vorschau').locator('[data-k$=".name"]', { hasText: 'Prüfgericht direkt' }).first();
    if (!speichernJa) { await st2.click(); await st2.evaluate(amEnde); await p.keyboard.type('x'); }
    await p.click('[data-m="einfach"]');
    const frage = await p.locator('#kt-fenster', { hasText: 'Erst speichern, dann wechseln?' }).waitFor({ timeout: 5000 }).then(() => true, () => false);
    if (frage) await p.click(speichernJa ? '#ja' : '#kt-fenster .kt-fenster__kn [data-zu]');
    await fensterZu(p); await p.waitForTimeout(700);
    const danach2 = (await api('GET', `/api/stand/${haus}/karten`)).d.kennung_entwurf, frei = await p.locator('body').evaluate(x => x.classList.contains('kt-frei'));
    pruef(frage && (speichernJa ? (!frei && danach2 !== davor) : (frei && danach2 === davor && /Nicht gespeicherte/.test(await leisteText(p)))), `ungespeicherte Eingabe und Wechsel des Wegs: Rückfrage, «${speichernJa ? 'Speichern' : 'Abbrechen'}» tut genau das`);
  }
  await p.locator('#kt-meldung .kt-quit', { hasText: 'Im Entwurf gespeichert' }).last().locator('button', { hasText: 'Rückgängig' }).click();
  pruef(await quittung(p, 'Zurückgenommen'), 'das zuletzt Geschriebene zurückgenommen'); await p.waitForTimeout(500);
  const rt = await reihe(p, 'Prüfgericht direkt').innerText();
  pruef(/Englisch nachziehen/i.test(rt), 'Deutsch geändert, Englisch nicht: der Eintrag ist markiert «Englisch nachziehen»', rt);
  await p.click('#kt-leiste [data-akt="veroeffentlichen"]');
  pruef(/Englisch ist bei 1 Eintrag noch nicht nachgezogen/.test(await fensterText(p)), 'vor dem Veröffentlichen steht der Hinweis auf die fehlende Übersetzung');
  await p.click('#kt-fenster .kt-fenster__kn [data-zu]');
  // Daten der Karte (Weg Fortgeschritten)
  await p.click('[data-m="frei"]'); await p.waitForTimeout(700); await p.evaluate(() => scrollTo(0, 0)); await p.click('[data-akt="daten"]');
  const roh = await p.locator('#j-t').inputValue(); let datenGut = false; try { datenGut = Array.isArray(JSON.parse(roh).teile); } catch (e) {}
  await p.fill('#j-t', '{kaputt'); await p.click('#j-ok');
  pruef(datenGut && /kein gültiges Format/.test(await p.locator('#j-f').innerText()), '«Daten der Karte»: die Karte als Text, ungültiger Text wird abgelehnt');
  await p.click('#kt-fenster .kt-fenster__kn [data-zu]'); await p.click('[data-m="einfach"]'); await p.waitForTimeout(600);
  // Karte einrichten: Zeitraum
  await p.click('#kt-rand [data-akt="karte"]'); await p.fill('#k-von', '31.02.2027'); await p.click('#k-ok');
  const falsch = /Tag\.Monat\.Jahr/.test(await p.locator('#k-f').innerText());
  await p.fill('#k-von', '01.05.2027'); await p.fill('#k-bis', '31.10.2027'); await p.click('#k-ok');
  pruef(falsch && await quittung(p, 'Karte eingerichtet') && (await api('GET', `/api/stand/${haus}/karten`)).d.entwurf.karten.find(e => e.id === H.karte).gilt.bis === '2027-10-31', 'Karte einrichten: falsches Datum abgelehnt, Zeitraum gespeichert');
  // Probe-PDF aus dem Entwurf
  const probe = await api('POST', `/api/x/karten/probe/${haus}/${H.karte}`, {});
  pruef(probe.status === 200 && probe.d.aus === 'entwurf' && probe.d.bericht.ok, 'Probe-PDF aus dem Entwurf: PDF = Daten, Umbruch stimmt', JSON.stringify(probe.d.bericht || probe.d).slice(0, 300));
  await p.click('#kt-leiste [data-akt="probe"]');
  pruef(await p.locator('#kt-meldung .kt-quit[data-pdf="probe"] a[href^="blob:"]').waitFor({ timeout: 20000 }).then(() => true, () => false), '«Probe-PDF» in der Leiste liefert die Probe');
  // Form wird geprüft: kaputte Daten kommen nicht in den Entwurf
  const st = (await api('GET', `/api/stand/${haus}/karten`)).d, kaputt = JSON.parse(JSON.stringify(st.entwurf)); kaputt.karten[0].karte.teile[1].posten[0] = { t: 'unbekannt' };
  const ab = await api('PUT', `/api/x/karten/entwurf/${haus}`, { daten: kaputt, erwartet: st.kennung_entwurf, wer: 'pruef' });
  pruef(ab.status === 422 && ab.d.stichwort === 'pruefung', 'Daten in falscher Form werden abgelehnt (422, Stichwort pruefung)');
  // neue Rubrik: gespeichert, aber ohne Gericht noch nicht auf der Karte; die Probe-PDF stimmt trotzdem mit den Daten
  await mitte(p.locator('.kt-neu-zeile [data-akt="rubrik-neu"]').last()); await p.locator('.kt-neu-zeile [data-akt="rubrik-neu"]').last().click(); await p.fill('#r-t', 'Prüfrubrik'); await p.click('#r-ok');
  pruef(await quittung(p, 'Rubrik angelegt'), 'neue Rubrik gespeichert');
  await p.waitForTimeout(600);
  const leerR = await api('POST', `/api/x/karten/probe/${haus}/${H.karte}`, {});
  pruef((await p.locator('#kt-liste').innerText()).includes('Prüfrubrik') && !(await vorschauText(p)).includes('Prüfrubrik') && leerR.d.bericht.ok, 'leere Rubrik: in der Liste da, auf der Karte erst mit einem Eintrag; PDF = Daten');
  // Zeichen aus einer Eingabe werden als Text gezeigt, nie ausgeführt
  const s2 = (await api('GET', `/api/stand/${haus}/karten`)).d, boese = JSON.parse(JSON.stringify(s2.entwurf));
  boese.karten[0].karte.teile[1].posten.find(u => u.t === 'gericht').name = '<img src=x onerror="window.KT_EINGESCHLEUST=1">Probe';
  await api('PUT', `/api/x/karten/entwurf/${haus}`, { daten: boese, erwartet: s2.kennung_entwurf, wer: 'pruef' });
  await p.reload({ waitUntil: 'load' }); await bereit(p);
  const drin = await p.evaluate(() => !!(window.KT_EINGESCHLEUST || document.getElementById('kt-vorschau').contentWindow.KT_EINGESCHLEUST || document.querySelector('#kt-liste img, #kt-rand img, #kt-kopf img') || document.getElementById('kt-vorschau').contentDocument.querySelector('img')));
  pruef(!drin && (await p.locator('#kt-liste').innerText()).includes('<img src=x'), 'eingeschleuste Zeichen stehen als Text da und werden nicht ausgeführt (Liste und Karte)');
  await p.click('#kt-leiste [data-akt="vgl"]');
  const drin2 = await p.evaluate(() => !!(window.KT_EINGESCHLEUST || document.querySelector('#kt-fenster img')));
  pruef(!drin2, 'auch im Fenster «Vorher / nachher» nicht'); await p.click('#kt-fenster .kt-fenster__kn [data-zu]');
  // Entwurf verwerfen
  await p.click('#kt-leiste [data-akt="verwerfen"]'); await p.click('#ja');
  pruef(await quittung(p, 'Entwurf verworfen'), 'Entwurf verworfen');
  const ende = (await api('GET', `/api/stand/${haus}/karten`)).d;
  pruef(ende.entwurf === null && ende.kennung_live === anfang.kennung_live, 'danach gilt wieder der veröffentlichte Stand, unverändert');
  // jede Karte des Hauses: Umbruchregeln, Vorschau gegen PDF
  const karten = ende.live.karten.map(e => e.id);
  for (const id of karten) {
    if (karten.length > 1) { await p.evaluate(() => scrollTo(0, 0)); await p.click(`.kt-kw[data-z="${id}"]`); await p.waitForFunction(x => location.hash === '#' + x, id); await p.waitForTimeout(1100); }
    vs = await p.evaluate(() => KT.vorschau());
    pruef(vs && vs.regeln.length === 0 && vs.ueberlauf.length === 0 && vs.seiten > 1, `Karte «${id}»: ${vs && vs.seiten} Seiten, Umbruchregeln eingehalten`, JSON.stringify(vs && vs.regeln.concat(vs.ueberlauf)));
    // Vorschau und PDF: gleich viele Seiten, und auf jeder Seite steht derselbe Text (also derselbe Umbruch)
    const sv = await p.frameLocator('#kt-vorschau').locator('.kt-blatt').allInnerTexts();
    const antwort = await api('GET', `/api/x/karten/pdf/${haus}/${id}`);
    const sp = antwort.status === 200 ? pdfText(antwort.d.pdf).split('\f') : [];
    if (sp.length && !sp[sp.length - 1].trim()) sp.pop();
    const w = t => (t.normalize('NFC').replace(/ﬁ/g, 'fi').replace(/ﬂ/g, 'fl').replace(/ﬀ/g, 'ff').replace(/ß/g, 'ss').toLowerCase().match(/[\p{L}\p{N}]/gu) || []).sort().join('');   // Zeichen statt Wörter: gesperrte Versalzeilen liest pdftotext buchstabenweise
    const ungleich = sv.findIndex((t, n) => w(t) !== w(sp[n] || ''));
    pruef(sv.length === sp.length && ungleich < 0, `Karte «${id}»: Vorschau und PDF haben dieselben ${sv.length} Seiten mit demselben Text je Seite`, `Vorschau ${sv.length}, PDF ${sp.length}, erste ungleiche Seite ${ungleich + 1}`);
  }
  pruef(p.fehler.length === 0 && p.dialoge === 0, 'keine Fehler in der Konsole, kein Dialog des Betriebssystems', JSON.stringify(p.fehler));
  await kontext.close();
}

async function drittesHaus(b, env) {
  ort = 'drittes Haus';
  const roh = JSON.parse(fs.readFileSync(path.join(HIER, '_qa', 'probehaus.json'), 'utf8'));
  const tmp = path.join(env.WERKZEUGE_DATEN, 'probehaus-eingabe.json'); fs.writeFileSync(tmp, JSON.stringify(roh));
  let aus = ''; try { aus = execFileSync('python3', [path.join(HIER, 'einlesen.py'), '--datei', tmp, 'probehaus'], { env, cwd: WURZEL }).toString(); } catch (e) { aus = String(e.stdout || e); }
  fs.unlinkSync(tmp);
  pruef(/1 Karte\(n\) im Speicher/.test(aus), 'ein drittes Haus kommt aus einer Datei in den Speicher, ohne Änderung am Werkzeug', aus);
  const kontext = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await seite(kontext, 'probehaus', /404/);
  pruef((await p.locator('#kt-liste').innerText()).includes('Beispielsuppe'), 'das Werkzeug zeigt die Karte des dritten Hauses');
  pruef(await p.locator('#kt-kopf .kt-zeichen:not(.kt-zeichen--bild)').count() === 1 && await p.locator('#kt-rand .kt-kw__f:not(.kt-kw__f--foto)').count() === 1 && (await vorschauText(p)).toLowerCase().includes('probehaus'), 'ohne Kleid: Ring mit Anfangsbuchstaben, Kachel mit Initiale, die Karte druckt den Namen des Hauses');
  const vs = await p.evaluate(() => KT.vorschau());
  pruef(vs.regeln.length === 0 && vs.ueberlauf.length === 0, 'anderes Format (A5), Umbruchregeln eingehalten', JSON.stringify(vs.regeln.concat(vs.ueberlauf)));
  let u = (await api('GET', '/api/x/karten/uebersicht/probehaus')).d;
  pruef(u.sprachen[0].fassungen.length === 1 && u.sprachen[0].fassungen[0].aktuell === false, 'Sprachfassung «en» mit fremdem Stand gilt als veraltet');
  // Fassung auf den heutigen deutschen Stand setzen → aktuell; dann Deutsch ändern → wieder veraltet
  let st = (await api('GET', '/api/stand/probehaus/karten')).d, d = JSON.parse(JSON.stringify(st.live));
  d.karten[0].fassungen.en.stand_de = u.sprachen[0].kennung_de;
  const r = await api('PUT', '/api/x/karten/entwurf/probehaus', { daten: d, erwartet: st.kennung_live, wer: 'pruef' });
  u = (await api('GET', '/api/x/karten/uebersicht/probehaus')).d;
  pruef(r.status === 200 && u.sprachen[0].fassungen[0].aktuell === true, 'Sprachfassung, die zum deutschen Stand passt, gilt als aktuell');
  await p.reload({ waitUntil: 'load' }); await bereit(p);
  await preisAendern(p, 'Beispielsuppe', '12,5');
  pruef(await quittung(p, 'Gericht gespeichert') && (await reihe(p, 'Beispielsuppe').innerText()).includes('12,5'), 'Preis in der Schreibweise des dritten Hauses (Komma, eine Stelle)');
  u = (await api('GET', '/api/x/karten/uebersicht/probehaus')).d;
  pruef(u.sprachen[0].fassungen[0].aktuell === false, 'Deutsch geändert: die Sprachfassung gilt sofort als veraltet');
  await p.click('#kt-leiste [data-akt="veroeffentlichen"]');
  pruef(/Sprachfassungen \(Musterkarte EN\) werden nicht mit geändert/.test(await fensterText(p)), 'vor dem Veröffentlichen steht, dass die Sprachfassung zurückbleibt');
  await p.fill('#v-wer', 'Prüflauf'); await p.click('#v-ok');
  pruef(await p.locator('#v-fertig').waitFor({ timeout: 30000 }).then(() => true, () => false), 'drittes Haus: veröffentlicht');
  const pdf = await pdfZeilen('probehaus', 'muster');
  pruef(zeileMit(pdf.zeilen, 'Beispielsuppe', '\u0000').includes('12,5') && pdf.zeilen.join(' ').includes('Enthält: Glutenhaltiges Getreide, Milch'), 'drittes Haus: PDF mit neuem Preis und Allergenen', zeileMit(pdf.zeilen, 'Beispielsuppe', '\u0000'));
  pruef((await api('GET', '/api/x/karten/kontrolle/probehaus')).d.gut === true, 'drittes Haus: Kontrolle gut');
  pruef(p.fehler.length === 0 && p.dialoge === 0, 'keine Fehler in der Konsole (ausser der fehlenden haus.json, die der Stamm anlegt)', JSON.stringify(p.fehler));
  // Start ohne Haus und mit einem Entwurf, der sich nicht zeigen lässt: es bleibt eine Tür, nichts geht still kaputt
  const o = await kontext.newPage(); await o.goto(`${BASIS}/werkzeuge/karten/`, { waitUntil: 'load' }); await o.waitForTimeout(600);
  pruef(/startet nicht/.test(await o.locator('body').innerText()) && /haus-fehlt/.test(await o.locator('body').innerText()), 'ohne ?haus=: verständliche Meldung mit Stichwort statt leerer Seite');
  st = (await api('GET', '/api/stand/probehaus/karten')).d;
  await api('PUT', '/api/entwurf/probehaus/karten', { daten: { schema: 1, haus: 'probehaus', karten: 'kaputt' }, erwartet: st.kennung_live, wer: 'pruef' });   // am Werkzeug vorbei, über den allgemeinen Weg
  await o.goto(`${BASIS}/werkzeuge/karten/?haus=probehaus`, { waitUntil: 'load' }); await o.waitForTimeout(700);
  pruef(await o.locator('#kt-entwurf-weg').count() === 1, 'kaputter Entwurf (am Werkzeug vorbei gespeichert): das Werkzeug bietet an, ihn zu verwerfen');
  const kv = await api('POST', '/api/x/karten/veroeffentlichen/probehaus', { wer: 'pruef' });
  pruef(kv.status === 422 && kv.d.stichwort === 'pruefung', 'kaputter Entwurf lässt sich über das Werkzeug nicht veröffentlichen');
  await o.click('#kt-entwurf-weg'); await o.waitForFunction(() => window.KT && KT.bereit(), null, { timeout: 8000 }).catch(() => {}); await o.waitForTimeout(400);
  pruef((await o.locator('body').innerText()).includes('Beispielsuppe') && (await api('GET', '/api/stand/probehaus/karten')).d.entwurf === null, 'nach dem Verwerfen läuft das Werkzeug wieder mit der veröffentlichten Karte');
  await kontext.close();
}

(async () => {
  const daten = fs.mkdtempSync(path.join(os.tmpdir(), 'karten-pruef-'));
  const env = Object.assign({}, process.env, { WERKZEUGE_DATEN: daten });
  ABLAGE = daten;
  let server, b, start = Date.now(), nur = process.env.PRUEF_NUR || '';
  const kurz = e => String(e.message || e).split('\n').slice(0, 8).join(' | ');
  try {
    if (await fetch(BASIS + '/api/haus/gasterntal').then(() => true, () => false)) throw new Error(`Port ${PORT} ist belegt. Der Lauf startet seinen eigenen Server und beendet keinen fremden.`);
    console.log(execFileSync('python3', [path.join(HIER, 'einlesen.py'), 'alle'], { env, cwd: WURZEL }).toString().trim());
    server = spawn('python3', [path.join(WURZEL, 'unterbau', 'serve.py'), String(PORT)], { env, cwd: WURZEL, stdio: ['ignore', 'ignore', 'pipe'] });
    let serverAus = ''; server.stderr.on('data', x => { serverAus += String(x); });
    for (let i = 0; i < 50; i++) { if (await fetch(BASIS + '/api/haus/gasterntal').then(r => r.ok, () => false)) break; await new Promise(r => setTimeout(r, 120)); }
    const { chromium } = require(finde());
    b = await chromium.launch({ headless: true, executablePath: shell() });
    let r = 0;
    for (const haus of Object.keys(HAEUSER)) {
      for (const welt of ['grand', 'land']) for (const breite of [1440, 390, 320]) {
        if (nur) continue;
        try { await durchlauf(b, haus, welt, breite, r++); } catch (e) { pruef(false, 'Durchlauf abgebrochen', kurz(e)); }
        console.log(`  ${haus} · ${welt} · ${breite}: ${schlecht ? schlecht + ' Fehler bisher' : 'gut'}`);
      }
      try { await werkzeug(b, haus); } catch (e) { pruef(false, 'Durchlauf abgebrochen', kurz(e)); }
      console.log(`  ${haus} · Werkzeug: ${schlecht ? schlecht + ' Fehler bisher' : 'gut'}`);
    }
    try { await drittesHaus(b, env); } catch (e) { pruef(false, 'Durchlauf abgebrochen', kurz(e)); }
    /* Lädt der Browser neu oder schliesst er die Seite, während eine Anfrage läuft, schreibt der Server «Broken pipe» samt Spur.
       Das ist ein abgebrochener Aufruf, kein Fehler des Werkzeugs (nachgestellt mit einem rohen Aufruf, der sofort auflegt).
       Alles andere zählt: jede Zeile FEHLER ohne diesen Grund und jede Spur, die nicht mit einem solchen Abbruch endet. */
    const ABBRUCH = /BrokenPipeError|ConnectionResetError|ConnectionAbortedError/;
    const sz = serverAus.split('\n');
    const echte = sz.filter(z => /^FEHLER /.test(z) && !ABBRUCH.test(z));
    const spuren = sz.filter(z => /^Traceback/.test(z)).length;
    const enden = sz.filter(z => /^[A-Za-z_.]*(Error|Exception|Warning)\b.*:/.test(z) || /^[A-Za-z_.]*(Error|Exception)$/.test(z));
    const fremd = enden.filter(z => !ABBRUCH.test(z));
    const abgebrochen = sz.filter(z => /^FEHLER /.test(z) && ABBRUCH.test(z)).length;
    ort = 'Server'; pruef(!echte.length && !fremd.length && spuren <= enden.length, 'keine Fehler in der Ausgabe des Servers', echte.concat(fremd).join(' · ').slice(0, 300) || `${spuren} Spuren, ${enden.length} erklärt`);
    if (abgebrochen) console.log(`  Hinweis: ${abgebrochen} Aufruf(e) hat der Browser selbst abgebrochen (Seite neu geladen); der Server schreibt dazu «Broken pipe».`);
  } catch (e) { ort = 'Lauf'; pruef(false, 'Lauf abgebrochen', String(e.message || e)); }
  finally {
    if (b) await b.close();
    if (server) server.kill();
    fs.rmSync(daten, { recursive: true, force: true });
  }
  const schluss = `${schlecht ? 'NICHT BESTANDEN' : nur ? 'TEILLAUF (zählt nicht als bestanden)' : 'BESTANDEN'} · ${gezaehlt} Prüfungen, ${schlecht} Fehler · ${Math.round((Date.now() - start) / 1000)} s · ${new Date().toLocaleString('de-CH')}`;
  fs.writeFileSync(path.join(HIER, '_qa', 'pruef-letzter-lauf.txt'), zeilen.concat(['', schluss]).join('\n') + '\n');
  console.log(schluss);
  process.exit(schlecht || nur ? 1 : 0);
})();
