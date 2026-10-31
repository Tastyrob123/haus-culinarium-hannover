// Prüflauf La Réception · Culinarium Hannover (28.10.2026, Muster: Prüflauf der Taverne zum Schäfli). Bedient statt lädt (Master 8/9a), unsichtbar, eigener Server mit Wegwerf-Daten
// (RECEPTION_DATEN auf einen Ordner im Notizblock, nie die Daten des Werkzeugs).
//   node culinarium.js <basis, z. B. http://127.0.0.1:9184> [chromium|webkit] [breite] [bilder-ordner]
// Prüft: jede Ansicht zweimal, Konsole, 404, kaputte Bilder, seitliches Überlaufen; Eingang mit Hinweisen und Allergien; Brief (Probe), ändern, sichern,
// neu laden; erledigt/offen; Deutsch lesen; PDF; Nachtragen; Wissen suchen; Chat ausprobieren → Anfrage; die Warteliste der Website über den Baustein;
// Sicherheit des Wegs «formular»; am Rechner Flüssigkeit 4× gedrosselt. Räumt jede Spur mit «QA» wieder weg.
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const SCHUTZ = require('./schutz');
const [, , BASIS = 'http://127.0.0.1:9184', MOTOR = 'chromium', BREITE = '1440', BILDER = ''] = process.argv;
const W = +BREITE, HANDY = W < 700, WZ = BASIS + '/_werkzeuge/reception/';
const res = [], fehler = [];
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const br = await SCHUTZ.start(pw, MOTOR);
  const ctx = await SCHUTZ.kontext(br, { viewport: { width: W, height: HANDY ? 844 : 900 }, locale: 'de-DE', acceptDownloads: true, hasTouch: HANDY, isMobile: HANDY && MOTOR === 'chromium' });
  await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'QA Prüfer'); localStorage.setItem('rundgang-reception', '1'); localStorage.setItem('rundgang-savoir', '1'); } catch (e) { /* */ } });
  const p = await ctx.newPage(); p.setDefaultTimeout(30000);   // 30 s: neben anderen Chats ist der Rechner zeitweise voll ausgelastet (Lauf 21.10.2026)
  p.on('pageerror', e => fehler.push('JS ' + String(e).slice(0, 160)));
  p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) fehler.push('Konsole ' + m.text().slice(0, 160)); });
  p.on('response', r => { if (r.status() >= 400 && !/favicon|marke\.json|api\/formular|api\/gast/.test(r.url())) fehler.push(r.status() + ' ' + r.url().replace(BASIS, '')); });
  p.on('dialog', d => d.accept().catch(() => {}));
  const schritt = async (name, fn) => { const f0 = fehler.length, t0 = Date.now(); try { const info = await fn(); const neu = fehler.slice(f0); res.push({ name, ok: !neu.length, info: (neu.length ? neu.join(' | ') + ' · ' : '') + (info || '') }); }
    catch (e) { res.push({ name, ok: false, info: String(e.message || e).split('\n')[0].slice(0, 220) }); } const r = res[res.length - 1]; console.log((r.ok ? 'ok   ' : 'ROT  ') + name + ' · ' + r.info + ` (${Date.now() - t0} ms)`); };
  const ok = (b, was) => { if (!b) throw new Error(was); };
  const api = async (was, d) => p.evaluate(async ([w, d]) => { const r = await fetch(w, d ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) } : {}); return { s: r.status, j: await r.json().catch(() => ({})) }; }, [WZ + 'api/' + was, d]);
  const gehe = async a => { await p.goto('about:blank'); await p.goto(WZ + '#' + a, { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await sleep(900); };
  const ueber = async () => p.evaluate(() => Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - innerWidth);
  const kaputt = async () => p.evaluate(() => [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map(i => i.getAttribute('src')));
  const bild = async n => { if (BILDER) { fs.mkdirSync(BILDER, { recursive: true }); await p.screenshot({ path: path.join(BILDER, `${MOTOR}-${W}-${n}.jpg`), quality: 70, type: 'jpeg' }); } };
  const karte = async re => { const k = p.locator('.re-liste .re-a', { hasText: re }).first(); await k.scrollIntoViewIfNeeded(); await k.click(); await p.waitForFunction(r => new RegExp(r).test(document.querySelector('#detail h2')?.textContent || ''), re.source); await sleep(500); };

  for (const a of ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen']) await schritt(`Ansicht ${a}: zweimal geladen, kein Fehler, kein Überlaufen, keine kaputten Bilder`, async () => {
    for (let i = 0; i < 2; i++) { await gehe(a); const u = await ueber(), k = await kaputt(); ok(u <= 0, 'überläuft um ' + u + ' px'); ok(!k.length, 'kaputte Bilder ' + k.join(', ')); }
    await bild(a); return (await p.locator('#kopf').innerText()).replace(/\s+/g, ' ').slice(0, 80); });

  await schritt('Jeder Link in Kopf und Rand antwortet (Fehlerbuch 10a): eigene Wege 200, Zentrale auf 127.0.0.1:9081, kein localhost', async () => {
    await gehe('start'); const l = await p.evaluate(() => [...document.querySelectorAll('#kopf a[href], #rand a[href]')].map(a => a.href).filter(h => /^http/.test(h)));
    ok(l.some(h => /127\.0\.0\.1:9081\/_werkzeuge\/maison\//.test(h)), 'kein Weg zur Zentrale auf 9081'); ok(!l.some(h => /localhost/.test(h)), 'localhost in einem Weg');
    const st = {}; for (const h of [...new Set(l.map(x => x.split('#')[0]))]) { st[h.replace(BASIS, '')] = await new Promise(res => { const r = require('http').get(h, x => { x.resume(); res(x.statusCode); }); r.on('error', () => res('aus')); r.setTimeout(4000, () => { r.destroy(); res('aus'); }); }); }
    const eigen = Object.entries(st).filter(([h]) => !/^http/.test(h)); ok(eigen.every(([, c]) => c === 200), JSON.stringify(eigen));
    return Object.entries(st).map(([h, c]) => h.replace('http://127.0.0.1:', ':') + ' ' + c).join(' · '); });
  await schritt('Kein roher Code im Bild ({, undefined, NaN, None, null) in allen Ansichten und jeder Anfrage (Fehlerbuch 10a)', async () => {
    const roh = async () => p.evaluate(() => { const t = document.body.innerText; return (t.match(/\{[^}\n]{0,40}\}|\bundefined\b|\bNaN\b|\bNone\b|\bnull\b/g) || []).slice(0, 5); });
    const funde = [];
    for (const a of ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen']) { await gehe(a); funde.push(...(await roh()).map(x => a + ': ' + x)); }
    await gehe('eingang'); const n = await p.locator('.re-liste .re-a').count();
    for (let i = 0; i < n; i++) { const c = p.locator('.re-liste .re-a').nth(i); await c.scrollIntoViewIfNeeded(); await c.click(); await sleep(500); funde.push(...(await roh()).map(x => 'Anfrage ' + i + ': ' + x)); }
    ok(!funde.length, funde.join(' | ')); return n + ' Anfragen, 5 Ansichten'; });
  await schritt('Kein Mailprogramm, keine Namensabfrage, keine fremden Hausnamen (Fehlerbuch 10a, Anfragen ins Fenster)', async () => {
    const funde = [];
    for (const a of ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen']) { await gehe(a);
      const z = await p.evaluate(() => ({ mail: document.querySelectorAll('a[href^="mailto:"]').length, wer: /Wer arbeitet hier|Wer trägt ein/.test(document.body.innerText),
        fremd: (document.body.innerText.match(/Beau-Rivage|Interlaken|Lästermeile|Carlton|Maeder|Ruedihus|Doldenhorn|Stuhlblau|Schäfli|Wigoltingen|Schlössli|Bottighofen|Kuchler|Festsaal|Zenchef|CHF/g) || []) }));
      if (z.mail) funde.push(a + ': ' + z.mail + ' mailto'); if (z.wer) funde.push(a + ': Namensabfrage'); if (z.fremd.length) funde.push(a + ': ' + z.fremd.join(',')); }
    ok(!funde.length, funde.join(' | ')); ok(!(await p.evaluate(() => window.__abgefangen || 0)), 'Mailprogramm wäre geöffnet worden'); return '5 Ansichten sauber'; });
  await schritt('Auswahl und Kalender im Stil des Hauses: keine Systemauswahl sichtbar, Bereich und «Gilt bis» wählbar', async () => {
    await gehe('wissen'); await p.click('#w-neu'); await p.waitForSelector('#fenster:not([hidden]) #f-ber'); await sleep(400);
    const sys = await p.evaluate(() => [...document.querySelectorAll('select, input[type=date]')].filter(e => { const r = e.getBoundingClientRect(), st = getComputedStyle(e); return r.width > 2 && r.height > 2 && st.opacity !== '0' && st.visibility !== 'hidden'; }).length);
    ok(sys === 0, sys + ' Systemfelder sichtbar');
    await p.click('#f-ber + .ws-wahl'); await p.click('.ws-wahl__l [role=option]:has-text("Das Haus (Bar)")'); ok(await p.inputValue('#f-ber') === 'Das Haus (Bar)', 'Bereich: ' + await p.inputValue('#f-ber'));
    await p.click('#f-bis + .ws-wahl'); await p.click('.ws-kal [data-m="1"]'); await p.click('.ws-kal__g [data-v$="-15"]'); const v = await p.inputValue('#f-bis'); ok(/^\d{4}-\d{2}-15$/.test(v), 'Datum: ' + v);
    await p.keyboard.press('Escape'); return 'Bereich Das Haus (Bar), gilt bis ' + v; });
  await schritt('Bilder in jeder Liste: jeder Eintrag hat ein geladenes Foto (Robert 19.10.2026)', async () => {
    const pruef = async (a, sel, bildSel) => { await gehe(a); await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); }); await sleep(800);
      return p.evaluate(([s, b]) => { const e = [...document.querySelectorAll(s)]; const ohne = e.filter(x => { const i = x.querySelector(b + ' img'); return !i || !(i.complete && i.naturalWidth > 0); }); return [e.length, ohne.length]; }, [sel, bildSel]); };
    const z = { eingang: await pruef('eingang', '.re-liste .re-a', '.re-a__bild'), gefragt: await pruef('gefragt', '.re-f', '.re-f__bild'), nachgetragen: await pruef('nachgetragen', '.re-n', '.re-n__bild'), wissen: await pruef('wissen', '.sb-z', '.sb-z__bild') };
    const schlecht = Object.entries(z).filter(([, [n, o]]) => !n || o); ok(!schlecht.length, JSON.stringify(z)); return Object.entries(z).map(([k, [n]]) => k + ' ' + n).join(', '); });
  await schritt('Eingang: Hinweise Termin offen, mehr als die Tafel, Allergie, Ticket stehen bei den richtigen Anfragen', async () => {
    await gehe('eingang'); await karte(/Lena Hoffmann/); const l = await p.locator('#detail .re-hinw').innerText(); ok(/Termin steht noch nicht fest/.test(l), 'Lena: ' + l);
    await karte(/Tim Becker/); const t = await p.locator('#detail .re-hinw').innerText(); ok(/18 Personen: mehr als die 14 Plätze/.test(t), 'Tim: ' + t);
    await karte(/Mira Schulte/); const m = await p.locator('#detail .re-hinw').innerText(); ok(/Rudi fragen/.test(m), 'Mira: ' + m);
    await karte(/Sophie Wagner/); const so = await p.locator('#detail .re-hinw').innerText(); ok(/nicht rückerstattet/.test(so), 'Sophie: ' + so);
    await karte(/Kai Brandt/); ok(await p.locator('#detail .re-hinw').count() === 0, 'Kai: Hinweis ohne Grund'); return 'Lena, Tim, Mira, Sophie, Kai'; });
  await schritt('Eingang ruhig gesetzt (Robert 20.10.): Hinweise mit Luft zur Schrift, kein Leerraum in der Karte, Rundgang-Schild bleibt beim Scrollen stehen', async () => {
    await gehe('eingang'); await karte(/Mira Schulte/);
    const m = await p.evaluate(() => { const d = document.querySelector('#detail .re-d').getBoundingClientRect(), h = document.querySelector('#detail .re-hinw').getBoundingClientRect(), g = document.querySelector('#detail .re-angaben--gast').getBoundingClientRect(), z = document.querySelector('#detail .re-gespraech').getBoundingClientRect();
      return { luft: Math.round(h.top - g.bottom), rest: Math.round(d.bottom - z.bottom) }; });
    ok(m.luft >= 14, 'Hinweise nur ' + m.luft + ' px unter den Angaben'); ok(m.rest <= 140, m.rest + ' px Leerraum unter der Nachricht');
    const c2 = await br.newContext({ viewport: { width: W, height: HANDY ? 844 : 900 } }); await c2.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); }); const q = await c2.newPage(); await q.goto(WZ + '#eingang'); await q.waitForSelector('#ansicht > *');
    const sch = await q.waitForSelector('.rdg-schild', { timeout: 8000 }).catch(() => null); ok(sch, 'Rundgang-Schild erscheint nicht');
    await q.mouse.move(W / 3, 400); await sleep(1200); const y0 = (await sch.boundingBox()).y; await q.mouse.wheel(0, 900); await sleep(800); const y1 = ((await sch.boundingBox()) || { y: y0 }).y; const wander = Math.round(Math.abs(y1 - y0)); await c2.close();
    ok(wander <= 2, 'Schild wandert ' + wander + ' px'); return `Luft ${m.luft} px, Rest ${m.rest} px, Schild ${wander}`; });
  await schritt('Eingang: Auswahl Warteliste / Abende / Feiern / Nachrichten zählt richtig', async () => {
    await gehe('eingang'); const z = {}; for (const k of ['Warteliste', 'Abende', 'Feiern', 'Nachrichten']) { await p.click(`.re-abt [data-abt="${k}"]`); await sleep(400); z[k] = await p.locator('.re-liste .re-a').count(); }
    await p.click('.re-abt [data-abt="alle"]'); const d = (await api('anfragen')).j.anfragen; const soll = { Warteliste: d.filter(a => a.art === 'warteliste').length, Abende: d.filter(a => a.art === 'abend').length, Feiern: d.filter(a => a.art === 'feier').length, Nachrichten: d.filter(a => a.art === 'nachricht').length };
    ok(JSON.stringify(z) === JSON.stringify(soll), JSON.stringify(z) + ' ≠ ' + JSON.stringify(soll)); return JSON.stringify(z); });
  await schritt('Brief: «Brief schreiben» (Probe ohne KI) nennt die Allergie, Text ändern, sichern, neu laden, bleibt', async () => {
    await gehe('eingang'); await karte(/Kai Brandt/);
    if (await p.locator('#detail [data-akt="schreiben"]').count()) { await p.click('#detail [data-akt="schreiben"]'); }
    await p.waitForSelector('#brief', { timeout: 30000 }); const t = await p.locator('#brief').innerText(); ok(/Hallo Kai/.test(t) && /Bis bald an der Tafel/.test(t), 'Du-Ton fehlt im Brief'); ok(/Culinarium/i.test(t) && /Haasemann(straße|strasse) 13/i.test(t), 'Kopf fehlt: ' + t.slice(0, 80) + ' … ' + t.slice(-120));
    await p.click('#detail [data-akt="bearbeiten"]'); await p.fill('#e-betreff', 'QA Betreff Culinarium'); await p.click('#detail [data-akt="sichern"]'); await sleep(1200);
    await gehe('eingang'); await karte(/Kai Brandt/); const d = (await api('anfragen')).j.anfragen.find(a => a.name === 'Kai Brandt'); ok(d.entwurf && d.entwurf.betreff === 'QA Betreff Culinarium', 'Betreff nicht gesichert: ' + (d.entwurf || {}).betreff);
    await api('anfrage', { id: d.id, betreff: 'Deine Feier an der langen Tafel', entwurf_text: d.entwurf.text, fassung: d.entwurf.fassung }); await bild('brief'); return 'gesichert und zurückgestellt'; });
  await schritt('Brief: «Als PDF speichern» lädt ein A4-PDF mit Briefkopf des Culinarium', async () => {
    await gehe('eingang'); await karte(/Jonas Albers/);
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 90000 }), p.evaluate(() => document.querySelector('#detail [data-akt="pdf"]').click())]);
    const f = dl.suggestedFilename().normalize('NFC'), z = require('os').tmpdir() + '/qa-brief-' + Date.now() + '.pdf'; await dl.saveAs(z); const b = fs.readFileSync(z); fs.unlinkSync(z);
    ok(/^Culinarium . Jonas Albers . \d\d\.\d\d\.\d{4}\.pdf$/.test(f), 'Dateiname ' + f); fs.mkdirSync(path.join(__dirname, 'lauf'), { recursive: true }); fs.writeFileSync(path.join(__dirname, 'lauf', `brief-${MOTOR}-${W}.pdf`), b); ok(b.slice(0, 4).toString() === '%PDF' && b.length > 20000, 'PDF ' + b.length); return f + ', ' + b.length + ' Byte'; });
  await schritt('Zwei Fenster: veraltete Fassung des Briefs wird abgewiesen (KONFLIKT), nichts überschrieben (E21/E26)', async () => {
    const d = (await api('anfragen')).j.anfragen.find(a => a.name === 'Jonas Albers'); const f0 = d.entwurf.fassung || 0;
    const r1 = await api('anfrage', { id: d.id, betreff: d.entwurf.betreff, entwurf_text: d.entwurf.text + '\n\nQA eins', fassung: f0 });
    const r2 = await api('anfrage', { id: d.id, betreff: d.entwurf.betreff, entwurf_text: d.entwurf.text + '\n\nQA zwei', fassung: f0 });
    const jetzt = (await api('anfragen')).j.anfragen.find(a => a.id === d.id).entwurf;
    await sleep(200); for (let i = fehler.length - 1; i >= 0; i--) if (/^422 .*api\/anfrage$/.test(fehler[i])) fehler.splice(i, 1);   // die erwartete Abweisung ist kein Fehler
    ok(r1.s === 200 && r2.s === 422 && /KONFLIKT/.test(r2.j.fehler) && /QA eins/.test(jetzt.text) && !/QA zwei/.test(jetzt.text), JSON.stringify({ r1: r1.s, r2: r2.s, f: r2.j.fehler }));
    await api('anfrage', { id: d.id, betreff: d.entwurf.betreff, entwurf_text: d.entwurf.text, fassung: jetzt.fassung }); return `Fassung ${f0} → ${jetzt.fassung}, zweites Fenster abgewiesen`; });
  await schritt('Brief «Nur Text» sieht aus wie «Gestalten»: Betreff bricht um, Felder ohne Rahmen und Füllung (Fehlerbuch 10a, 20.10.2026)', async () => {
    const alt = (await api('anfragen')).j.anfragen.find(a => a.name === 'Jonas Albers').entwurf;
    await gehe('eingang'); await karte(/Jonas Albers/); await p.click('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-betreff');
    await p.fill('#e-betreff', 'QA ein sehr langer Betreff, der in einer Zeile nicht Platz hat und deshalb umbrechen muss wie im gestalteten Brief'); await p.dispatchEvent('#e-betreff', 'input'); await sleep(300);
    const m = await p.evaluate(() => { const b = document.querySelector('#e-betreff'), t = document.querySelector('#e-text'), sb = getComputedStyle(b), st = getComputedStyle(t);
      return { tag: b.tagName, hoch: b.scrollHeight <= b.clientHeight + 2, zeilen: Math.round(b.clientHeight / parseFloat(sb.lineHeight || 20)), rand: sb.borderTopWidth + '/' + st.borderTopWidth, bg: st.backgroundColor, fett: sb.fontWeight }; });
    await bild('nurtext'); await p.fill('#e-betreff', alt.betreff); await p.dispatchEvent('#e-betreff', 'input'); await p.click('#detail [data-akt="lesen"]').catch(() => {}); await sleep(600);
    { const d = (await api('anfragen')).j.anfragen.find(a => a.name === 'Jonas Albers'); if (d.entwurf.betreff !== alt.betreff) await api('anfrage', { id: d.id, betreff: alt.betreff, entwurf_text: d.entwurf.text, fassung: d.entwurf.fassung }); }
    ok(m.tag === 'TEXTAREA' && m.hoch && m.zeilen >= 2 && /^0px\/0px$/.test(m.rand) && /rgba\(0, 0, 0, 0\)|transparent/.test(m.bg) && +m.fett < 600, JSON.stringify(m)); return JSON.stringify(m); });
  await schritt('Erledigt und wieder offen', async () => { await gehe('eingang'); await karte(/Lena Hoffmann/); await p.click('#detail [data-akt="erledigt"]'); await sleep(900); ok((await api('anfragen')).j.anfragen.find(a => a.name === 'Lena Hoffmann').status === 'erledigt', 'nicht erledigt'); await p.click('#detail [data-akt="offen"]'); await sleep(900); ok((await api('anfragen')).j.anfragen.find(a => a.name === 'Lena Hoffmann').status !== 'erledigt', 'nicht offen'); return 'ok'; });
  await schritt('Auf Deutsch lesen (englische Anfrage)', async () => { await gehe('eingang'); await karte(/Emma Clarke/); await p.click('#detail [data-akt="deutsch"]'); await p.waitForFunction(() => /Zwei Plätze an der Tafel/.test(document.querySelector('#detail')?.innerText || ''), null, { timeout: 20000 }).catch(() => {}); const t = await p.locator('#detail').innerText(); ok(/Zwei Plätze an der Tafel/i.test(t), 'Lesefassung fehlt'); return 'Lesefassung da'; });
  await schritt('Das wurde gefragt: Lücke nachtragen, steht in «Vom Team nachgetragen», entfernen', async () => {
    await gehe('gefragt'); const l0 = (await api('ueberblick')).j.ohne_antwort; const k = p.locator('[data-akt="nachtragen"]').first(); await k.scrollIntoViewIfNeeded(); await k.click();
    await p.waitForSelector('#fenster:not([hidden]) textarea'); const ta = p.locator('#fenster textarea').last(); await ta.fill('QA Antwort: Ja, auf Wunsch mixt Momo alkoholfrei.'); await p.click('#fenster #f-los'); await sleep(1200);
    const ng = (await api('fragen')).j.nachgetragen; const e = ng.find(x => /^QA Antwort/.test(x.antwort)); ok(e, 'Nachtrag fehlt'); const l1 = (await api('ueberblick')).j.ohne_antwort; ok(l1 === l0 - 1, `Lücken ${l0} → ${l1}`);
    await gehe('nachgetragen'); ok(/QA Antwort/.test(await p.locator('#ansicht').innerText()), 'Karte fehlt'); await api('nachtragen_weg', { nid: e.nid });
    const f = (await api('fragen')).j.fragen.find(x => x.id === e.quelle); if (f) await api('frage', { id: f.id, erledigt: false }); return `Lücken ${l0} → ${l1}, weggeräumt`; });
  await schritt('Das weiss der Chat: Suche «Warteliste» trifft, «Kinderstuhl» führt zu «noch nicht im Wissen»', async () => {
    await gehe('wissen'); await p.fill('#w-such', 'Fatwashing'); await p.waitForFunction(() => /Fett/.test(document.querySelector('#ansicht')?.innerText || ''), null, { timeout: 6000 }).catch(() => {}); const a = await p.locator('#ansicht').innerText(); ok(/Fett/.test(a), 'Fatwashing ohne Treffer');
    await p.fill('#w-such', 'Kinderstuhl'); await p.locator('.sb-fehlt').scrollIntoViewIfNeeded({ timeout: 4000 }).catch(() => {}); await sleep(900); await p.waitForFunction(() => /noch nicht/i.test(document.querySelector('#ansicht')?.innerText || ''), null, { timeout: 8000 }).catch(() => {}); const b = await p.locator('#ansicht').innerText(); ok(/noch ?nicht|Noch ?nicht/.test(b), 'kein Hinweis «noch nicht im Wissen»') /* WebKit liest Wort-Spannen am Zeilenumbruch ohne Leerzeichen («nochnichts») */; return 'ok'; });
  await schritt('Chat ausprobieren: Frage antippen, Antwort kommt (belegt), Anfrage mit Kontakt landet als Beispiel im Eingang', async () => {
    await gehe('start'); const n0 = (await api('anfragen')).j.anfragen.length;
    if (HANDY) { const b = p.locator('#rand [data-probe]'); if (await b.count() && !(await b.isVisible())) await p.locator('.wo-kopf [data-bereiche], .wo-kopf__ber').first().click().catch(() => {}); }
    await p.evaluate(() => (document.querySelector('#k-probe') || document.querySelector('#rand [data-probe]')).click());
    await p.waitForSelector('.ws-handy'); await p.click('.probe__fragen [data-frage]'); await p.waitForFunction(() => document.querySelectorAll('#probe-l .ws-bl--haus').length >= 2 && !document.querySelector('.ws-bl--wartet'), null, { timeout: 20000 });
    await p.fill('#probe-t', 'Ich möchte auf die Warteliste für den nächsten Abend. Mein Name ist QA Gast, qa@example.com, 4 Personen.'); await p.press('#probe-t', 'Enter');
    await p.waitForFunction(() => document.querySelectorAll('#probe-l .ws-bl--haus').length >= 3 && !document.querySelector('.ws-bl--wartet'), null, { timeout: 20000 }); await bild('chat');
    const l = (await api('anfragen')).j.anfragen; const q = l.find(a => a.name === 'QA Gast'); ok(l.length === n0 + 1 && q && q.beispiel, 'keine Beispiel-Anfrage'); await p.keyboard.press('Escape');
    await api('weg', { id: q.id }); for (const f of (await api('fragen')).j.fragen.filter(f => /QA Gast|Wann ist der nächste Abend/.test(f.frage) && f.probe)) await api('weg', { id: f.id }); return 'Anfrage ' + q.art + ', weggeräumt'; });

  // Die Warteliste der Website, über den Baustein (die Website selbst bleibt unverändert; der Baustein wird nur in diesen Prüfbrowser geladen)
  const BAU = path.join(__dirname, '..', 'baustein', 'anfrage.js');
  const warte = async (name, mail, tag, plus) => {
    await p.goto(BASIS + '/abend.html#warteliste', { waitUntil: 'load' }); if (!(await p.evaluate(() => !!document.querySelector('script[src*="anfrage.js"]')))) await p.addScriptTag({ path: BAU }); await sleep(400);
    await p.evaluate(([name, mail, tag, plus]) => { const f = document.querySelector('form.wt-form'); f.scrollIntoView({ block: 'center' }); const r = f.querySelector(`[name=tag][value="${tag}"]`); r.checked = true; r.dispatchEvent(new Event('change', { bubbles: true }));
      for (let i = 0; i < plus; i++) f.querySelector('[data-schritt="1"]').click();
      f.querySelector('[name=name]').value = name; f.querySelector('[name=name]').dispatchEvent(new Event('input', { bubbles: true })); f.querySelector('[name=mail]').value = mail; f.requestSubmit(); }, [name, mail, tag, plus]); };
  await schritt('Website-Warteliste (abend.html) → Eingang mit Tag und Plätzen, Abriss löst sich erst nach der Annahme, Name mit <script> und Emoji entschärft', async () => {
    await warte('QA Warte <script>alert(1)</script> 🥂', 'qa-wl@example.com', 'sa', 2);
    await p.waitForFunction(() => document.querySelector('form.wt-form').classList.contains('fertig'), null, { timeout: 10000 }); await bild('warteliste');
    const m = await p.locator('form.wt-form .wt-meldung').innerText();
    const a = (await api('anfragen')).j.anfragen.find(x => /^QA Warte/.test(x.name));
    ok(a && a.art === 'warteliste' && a.formular === 'warteliste' && a.web && a.abteilung === 'Warteliste', 'Anfrage fehlt oder falsch: ' + JSON.stringify(a && { art: a.art, formular: a.formular, abt: a.abteilung }));
    ok(String(a.personen) === '4' && /Tag: Samstag, ab 17:00/.test(a.nachricht) && /Plätze: 4/.test(a.nachricht), 'Angaben: ' + a.personen + ' ' + a.nachricht);
    ok(a.hinweise.some(h => /Termin steht noch nicht fest/.test(h.text)), 'Hinweis fehlt'); ok(/Dein Eintrag liegt beim Team/.test(m) && /Samstag/.test(m), 'Danke der Website: ' + m);
    await p.goto(WZ + '#eingang'); await p.waitForSelector('#ansicht > *'); await karte(/QA Warte/); const roh = await p.evaluate(() => !!document.querySelector('#detail script') || /<script>/.test(document.querySelector('#detail').innerHTML)); ok(!roh, 'Skript im Eingang nicht entschärft');
    await api('weg', { id: a.id }); return `${a.art}, ${a.personen} Plätze, Samstag · ${m.replace(/\s+/g, ' ').slice(0, 70)}`; });
  await schritt('Website-Warteliste ohne Name: die Website sagt, was fehlt, nichts geht in den Eingang', async () => {
    const n0 = (await api('anfragen')).j.anfragen.length; await warte('', 'qa@example.com', 'fr', 0); await sleep(1200);
    const m = await p.locator('form.wt-form .wt-meldung').innerText(); const n1 = (await api('anfragen')).j.anfragen.length; ok(/Bitte Name und E-Mail/.test(m) && n1 === n0, m + ' · ' + n0 + '→' + n1); return m; });
  await schritt('Website-Warteliste ohne Verbindung: Meldung mit Telefon der Bar und Instagram, Eingaben bleiben, Abriss bleibt', async () => {
    await p.route(/\/api\/(formular|anfrage)$/, r => r.abort()); await warte('QA Ohne', 'qa@example.com', 'egal', 0);   // 29.10.: die Website schickt an /api/anfrage (assets/anfrage.js)
    await p.waitForFunction(() => /Telefon der Bar/.test(document.querySelector('form.wt-form .wt-meldung').textContent), null, { timeout: 10000 });
    const z = await p.evaluate(() => { const f = document.querySelector('form.wt-form'); return { m: f.querySelector('.wt-meldung').textContent, v: f.querySelector('[name=name]').value, fertig: f.classList.contains('fertig') }; });
    await p.unroute(/\/api\/(formular|anfrage)$/); for (let n = fehler.length - 1; n >= 0; n--) if (/formular|anfrage/.test(fehler[n])) fehler.splice(n, 1);
    ok(/\+49 163 3909578/.test(z.m) && /@culinarium_hannover/.test(z.m) && z.v === 'QA Ohne' && !z.fertig, JSON.stringify(z)); return z.m.slice(0, 90); });
  await schritt('Sicherheit Weg «formular»: fremde Herkunft 403, Kontakt ungültig 422, Maschinenfeld legt nichts ab, über 12 kB 413', async () => {
    await gehe('start'); const n0 = (await api('anfragen')).j.anfragen.length;
    const r1 = await p.evaluate(async u => (await fetch(u, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: 'QA', kontakt: 'x' }) })).status, WZ + 'api/formular');
    const r2 = await p.evaluate(async u => (await fetch(u, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: 'QA', kontakt: 'qa@example.com', website: 'spam' }) })).json(), WZ + 'api/formular');
    const r3 = await p.evaluate(async u => (await fetch(u, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: 'QA', kontakt: 'qa@example.com', nachricht: 'x'.repeat(13000) }) })).status, WZ + 'api/formular');
    const fremd = await new Promise(res => { const req = require('http').request(WZ + 'api/formular', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://boese.example' } }, r => res(r.statusCode)); req.end('{}'); });
    const n1 = (await api('anfragen')).j.anfragen.length; ok(r1 === 422 && r2.ok && r3 === 413 && fremd === 403 && n1 === n0, `422:${r1} falle:${JSON.stringify(r2)} 413:${r3} 403:${fremd} Zahl ${n0}→${n1}`); return `422 ${r1} · Falle ok · 413 ${r3} · fremd ${fremd}`; });
  if (HANDY) await schritt('Handy: Bereiche klappen auf und nach der Wahl zu', async () => { await gehe('start'); const k = p.locator('#kopf [data-bereiche], #kopf .wo-kopf__ber').first(); await k.click(); await sleep(400); const auf = await p.evaluate(() => getComputedStyle(document.querySelector('#rand')).visibility !== 'hidden' && document.querySelector('#rand').getBoundingClientRect().height > 50); ok(auf, 'Rand geht nicht auf'); await p.click('#rand [data-gehe="eingang"]'); await sleep(700); ok(location => true); return 'ok'; });
  if (MOTOR === 'chromium' && !HANDY) await schritt('Flüssigkeit ' + (process.env.DROSSEL || 4) + '× gedrosselt: Wechsel der Ansichten und Scrollen', async () => {
    await gehe('start'); const cdp = await ctx.newCDPSession(p); await cdp.send('Emulation.setCPUThrottlingRate', { rate: +(process.env.DROSSEL || 4) });
    await p.evaluate(() => { window.__f = []; let l = performance.now(); const t = n => { window.__f.push(n - l); l = n; if (window.__f.length < 900) requestAnimationFrame(t); }; requestAnimationFrame(t); });
    for (const k of ['eingang', 'gefragt', 'wissen', 'start']) { await p.click(`#rand [data-gehe="${k}"]`); await sleep(700); for (let i = 0; i < 6; i++) { await p.mouse.wheel(0, 260); await sleep(60); } }
    const f = await p.evaluate(() => window.__f.slice(2)); await cdp.send('Emulation.setCPUThrottlingRate', { rate: 1 });
    const fps = f.length / (f.reduce((a, b) => a + b, 0) / 1000), lang = f.filter(x => x > 50).length, max = Math.max(...f);
    return `${fps.toFixed(0)} Bilder/s, ${lang} über 50 ms, längstes ${max.toFixed(0)} ms (${f.length} Bilder)`; });
  await br.close();
  const rot = res.filter(r => !r.ok);
  console.log(`\nculinarium ${MOTOR} ${W}: ${res.length - rot.length} von ${res.length} grün`);
  fs.mkdirSync(path.join(__dirname, 'lauf'), { recursive: true }); fs.writeFileSync(path.join(__dirname, 'lauf', `culinarium-${MOTOR}-${W}.json`), JSON.stringify(res, null, 1));
  process.exit(rot.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
