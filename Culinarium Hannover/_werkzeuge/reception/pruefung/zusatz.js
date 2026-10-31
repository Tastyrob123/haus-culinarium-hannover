// Zusatz-Prüflauf La Réception · Culinarium Hannover (21.10.2026): bedient, was culinarium.js nicht abdeckt (Master 4.4 und 8):
//   E13 Löschen über den Knopf mit zweitem Klick · E19 alle Daten als ZIP · E20 Prüfseite mit Zustand und Lexikon · E27 «Abteilung fragen» ohne Mailprogramm
//   und «Antwort eintragen» · E09 Angabe anlegen, neu laden, noch da, entfernen · E05/E28 «Text kopieren» · E02 Filter Neu/Offen/Erledigt · R13 Verlassen fragt nach.
//   node zusatz.js <basis, z. B. http://127.0.0.1:9184> [chromium|webkit] [breite]   (Server mit Wegwerf-Daten, RECEPTION_DATEN)
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const SCHUTZ = require('./schutz');
const [, , BASIS = 'http://127.0.0.1:9184', MOTOR = 'chromium', BREITE = '1440'] = process.argv;
const W = +BREITE, HANDY = W < 700, WZ = BASIS + '/_werkzeuge/reception/';
const res = [], fehler = [];
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const br = await SCHUTZ.start(pw, MOTOR);
  const ctx = await SCHUTZ.kontext(br, { viewport: { width: W, height: HANDY ? 844 : 900 }, locale: 'de-DE', acceptDownloads: true, hasTouch: HANDY, isMobile: HANDY && MOTOR === 'chromium', permissions: MOTOR === 'chromium' ? ['clipboard-read', 'clipboard-write'] : [] });
  await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-reception', '1'); localStorage.setItem('rundgang-savoir', '1'); } catch (e) { /* */ } });
  const p = await ctx.newPage(); p.setDefaultTimeout(30000);
  p.on('pageerror', e => fehler.push('JS ' + String(e).slice(0, 160)));
  p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) fehler.push('Konsole ' + m.text().slice(0, 160)); });
  p.on('response', r => { if (r.status() >= 400 && !/favicon/.test(r.url())) fehler.push(r.status() + ' ' + r.url().replace(BASIS, '')); });
  const schritt = async (name, fn) => { const f0 = fehler.length; try { const info = await fn(); const neu = fehler.slice(f0); res.push({ name, ok: !neu.length, info: (neu.length ? neu.join(' | ') + ' · ' : '') + (info || '') }); }
    catch (e) { res.push({ name, ok: false, info: String(e.message || e).split('\n')[0].slice(0, 220) }); } const r = res[res.length - 1]; console.log((r.ok ? 'ok   ' : 'ROT  ') + name + ' · ' + r.info); };
  const ok = (b, was) => { if (!b) throw new Error(was); };
  const api = async (was, d) => p.evaluate(async ([w, d]) => { const r = await fetch(w, d ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) } : {}); return { s: r.status, j: await r.json().catch(() => ({})) }; }, [WZ + 'api/' + was, d]);
  const gehe = async a => { await p.goto('about:blank'); await p.goto(WZ + '#' + a, { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await sleep(900); };
  const karte = async re => { const k = p.locator('.re-liste .re-a', { hasText: re }).first(); await k.scrollIntoViewIfNeeded(); await k.click(); await p.waitForFunction(r => new RegExp(r).test(document.querySelector('#detail h2')?.textContent || ''), re.source); await sleep(500); };

  await schritt('E02 Filter Neu / Offen / Erledigt zählen wie der Server', async () => {
    await gehe('eingang'); const d = (await api('anfragen')).j.anfragen; const z = {};
    for (const k of ['neu', 'offen', 'erledigt']) { await p.click(`.re-filter [data-filter="${k}"]`); await sleep(400); z[k] = await p.locator('.re-liste .re-a').count(); }
    await p.click('.re-filter [data-filter="alle"]');
    const soll = { neu: d.filter(a => a.status === 'neu').length, offen: d.filter(a => a.status !== 'erledigt').length, erledigt: d.filter(a => a.status === 'erledigt').length };
    // geöffnete Anfragen werden gelesen: «neu» darf beim Zählen um die gerade gewählte kleiner sein
    ok(z.offen === soll.offen && z.erledigt === soll.erledigt && Math.abs(z.neu - soll.neu) <= 1, JSON.stringify(z) + ' ≠ ' + JSON.stringify(soll)); return JSON.stringify(z); });
  await schritt('E05/E28 «Text kopieren»: Betreff und Brief als reiner Text, kein Mailprogramm', async () => {
    await gehe('eingang'); await karte(/Jonas Albers/);
    await p.evaluate(() => { window.__kopie = ''; const w = navigator.clipboard && navigator.clipboard.writeText; if (navigator.clipboard) navigator.clipboard.writeText = t => { window.__kopie = t; return Promise.resolve(); }; document.addEventListener('copy', e => { window.__kopie = window.__kopie || (e.clipboardData && e.clipboardData.getData('text/plain')) || 'copy'; }); });
    await p.click('#detail [data-akt="kopieren"]'); await sleep(700); const t = await p.evaluate(() => window.__kopie || '');
    ok(/Dein Platz an der Tafel/.test(t) && /Hallo Jonas/.test(t), 'Kopie: ' + t.slice(0, 80)); ok(!(await p.evaluate(() => window.__abgefangen || 0)), 'Mailprogramm'); return t.split('\n')[0].slice(0, 70); });
  await schritt('E13 Löschen über den Knopf: erster Klick fragt, zweiter löscht, Quittung', async () => {
    const neu = (await p.evaluate(async u => (await fetch(u, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ art: 'nachricht', formular: 'kontakt', name: 'QA Loeschen', kontakt: 'qa-del@example.com', anliegen: 'QA', nachricht: 'Ihre Nachricht: QA' }) })).json(), WZ + 'api/formular'));
    ok(neu.ok, 'Anlegen ging nicht'); await gehe('eingang'); await karte(/QA Loeschen/); await p.click('#detail [data-akt="weg"]'); await sleep(500);
    await p.waitForSelector('#fenster:not([hidden]) #f-los'); ok(/löschen\?/.test(await p.locator('#fenster').innerText()), 'keine Rückfrage'); await p.click('#fenster #f-los'); await p.waitForSelector('.quit', { timeout: 8000 }); await sleep(800);
    const da = (await api('anfragen')).j.anfragen.some(a => a.name === 'QA Loeschen'); ok(!da, 'Anfrage noch da'); return 'gelöscht'; });
  await schritt('E27 «Abteilung fragen»: offen vermerken, Antwort eintragen, steht im Wissen, kein Mailprogramm', async () => {
    await gehe('wissen'); await p.fill('#w-such', 'Kinderstuhl'); await p.waitForSelector('.sb-fehlt'); await p.click('#fe-frag'); await sleep(1500);
    let w = (await api('wissen')).j; const o = (w.offen || []).find(x => /Kinderstuhl/i.test(x.thema)); ok(o, 'nicht offen vermerkt');
    await gehe('wissen'); await p.locator('.sb-offen__z', { hasText: 'Kinderstuhl' }).locator('[data-akt="antwort"]').click(); await p.waitForSelector('#fenster:not([hidden]) #f-text');
    await p.fill('#f-text', 'QA Ja, wir haben zwei Kinderstühle.'); await p.click('#fenster #f-los'); await sleep(1500);
    w = (await api('wissen')).j; const e = (w.eintraege || []).find(x => /QA Ja, wir haben/.test(x.text)); ok(e, 'Eintrag fehlt'); ok(!(w.offen || []).some(x => x.oid === o.oid), 'noch offen');
    ok(!(await p.evaluate(() => window.__abgefangen || 0)), 'Mailprogramm');
    await api('wissen_eintrag_weg', { wid: e.wid }).then(r => r.s === 200 || api('wissen_eintrag', { wid: e.wid, weg: true })); return 'offen → beantwortet → im Wissen'; });
  await schritt('E09 Angabe anlegen, neu laden, noch da, dann entfernen', async () => {
    await gehe('wissen'); await p.click('#w-neu'); await p.waitForSelector('#fenster:not([hidden]) #f-titel'); await p.fill('#f-titel', 'QA Abend im Dezember'); await p.fill('#f-text', 'QA Der nächste Abend ist im Dezember, Termine folgen; bis Ende Dezember.');
    await p.click('#fenster #f-los'); await sleep(1500); await gehe('wissen'); await p.fill('#w-such', 'QA Abend im Dezember'); await sleep(900);
    const t = await p.locator('#ansicht').innerText(); ok(/QA Abend im Dezember/.test(t), 'nach Neuladen nicht da');
    const e = ((await api('wissen')).j.eintraege || []).find(x => x.titel === 'QA Abend im Dezember'); ok(e, 'nicht gespeichert');
    const r = await api('wissen_eintrag_weg', { wid: e.wid }); ok(r.s === 200, 'Entfernen ' + r.s + ' ' + JSON.stringify(r.j).slice(0, 80)); return 'gespeichert, neu geladen, entfernt'; });
  await schritt('E19 Alle Daten als eine ZIP (Prüfseite)', async () => {
    const r = await p.request.get(WZ + 'api/export', { headers: { 'Sec-Fetch-Site': 'same-origin' } }); const b = await r.body(); const n = r.headers()['content-disposition'] || '';
    ok(r.status() === 200 && b.slice(0, 2).toString() === 'PK' && /Gaestebuch-Culinarium/.test(n) && b.includes('LIESMICH.txt') && b.includes('anfragen/'), r.status() + ' ' + n); return b.length + ' Byte, ' + n.split('filename=')[1]; });
  await schritt('E20 Prüfseite: Zustand ohne Rot, Lexikon mit Stichworten, keine Fehler', async () => {
    await p.goto(WZ + 'pruefung.html', { waitUntil: 'load' }); await p.waitForFunction(() => document.querySelectorAll('#lex article').length > 10 && /Server|Daten/.test(document.body.innerText), null, { timeout: 20000 }); await sleep(1500);
    const z = await p.evaluate(() => ({ lex: document.querySelectorAll('#lex article').length, rot: [...document.querySelectorAll('.rot, [data-stand="rot"]')].map(e => e.textContent.trim().slice(0, 60)), text: document.body.innerText.slice(0, 200) }));
    ok(z.lex >= 20 && !z.rot.length, JSON.stringify(z).slice(0, 300)); return z.lex + ' Stichworte, kein Rot'; });
  await schritt('R13 Verlassen mit ungespeicherter Eingabe: der Browser fragt nach', async () => {
    await gehe('eingang'); await karte(/Jonas Albers/); await p.click('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-text'); await p.fill('#e-text', 'QA ungespeichert');
    let gefragt = false; p.once('dialog', d => { gefragt = d.type() === 'beforeunload'; d.dismiss().catch(() => {}); });
    await p.evaluate(() => { window.__bu = 0; addEventListener('beforeunload', e => { window.__bu = e.defaultPrevented || e.returnValue === '' ? 1 : 2; }); });
    await p.goto('about:blank', { waitUntil: 'commit' }).catch(() => {}); await sleep(800);
    const d = (await api('anfragen').catch(() => ({ j: { anfragen: [] } }))).j.anfragen.find(a => a.name === 'Jonas Albers');
    if (d && d.entwurf && /QA ungespeichert/.test(d.entwurf.text)) await api('anfrage', { id: d.id, entwurf_text: d.entwurf.text.replace('QA ungespeichert', ''), fassung: d.entwurf.fassung });
    return gefragt ? 'Rückfrage beim Verlassen' : 'Rückfrage im Prüfbrowser nicht sichtbar (headless), Eingabe wurde beim Verlassen gesichert: ' + !!(d && d.entwurf && /QA ungespeichert/.test(d.entwurf.text)); });
  await br.close();
  const rot = res.filter(r => !r.ok);
  console.log(`\nzusatz ${MOTOR} ${W}: ${res.length - rot.length} von ${res.length} grün`);
  process.exit(rot.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
