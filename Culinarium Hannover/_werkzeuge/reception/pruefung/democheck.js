// Demo-Check La Réception · Culinarium Hannover (21.10.2026, Prüf-Chat, nie daran gebaut). Ergänzt culinarium.js und zusatz.js um das, was die Demo zeigt:
//   14 Gästefragen hintereinander in «Chat ausprobieren» (jede bekommt eine Antwort, Demo-Wort statt Technik, Eingabefeld bleibt sichtbar),
//   jede Anfrage im Eingang geöffnet, alle Links in Werkzeug, Anleitung und Prüfseite (kein mailto/tel/sms, kein 404), Anleitung mit Bildern und Sprüngen.
//   node democheck.js <basis, z. B. http://127.0.0.1:9184> [chromium|webkit] [breite] [bilder-ordner]   (Server mit Wegwerf-Daten, RECEPTION_DATEN)
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const SCHUTZ = require('./schutz');
const [, , BASIS = 'http://127.0.0.1:9184', MOTOR = 'chromium', BREITE = '1440', BILDER = ''] = process.argv;
const W = +BREITE, HANDY = W < 700, WZ = BASIS + '/_werkzeuge/reception/';
const res = [], fehler = [];
const sleep = ms => new Promise(r => setTimeout(r, ms));
const FRAGEN = ['Wann ist der nächste Abend?', 'Wann geht es los?', 'Wie komme ich an einen Platz?', 'Was kostet ein Abend?', 'Was gibt es zu essen?',
  'Was ist Milkwashing?', 'Kann ich mein Ticket zurückgeben?', 'Wo ist das genau?', 'Wann hat die Bar offen?', 'Kann ich die lange Tafel für meinen Geburtstag mit 25 Leuten haben?',
  'Ich habe eine Nussallergie, ist das ein Problem?', 'Wann gibt es wieder Dirty Chicken?', 'Is the evening vegetarian?',
  'Ich möchte auf die Warteliste für Samstag, 2 Plätze. Mein Name ist QA Demo, qa-demo@example.com'];
(async () => {
  const br = await SCHUTZ.start(pw, MOTOR);
  const ctx = await SCHUTZ.kontext(br, { viewport: { width: W, height: HANDY ? 844 : 900 }, locale: 'de-DE', hasTouch: HANDY, isMobile: HANDY && MOTOR === 'chromium' });
  await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-reception', '1'); localStorage.setItem('rundgang-savoir', '1'); } catch (e) { /* */ } });
  const p = await ctx.newPage(); p.setDefaultTimeout(30000);
  p.on('pageerror', e => fehler.push('JS ' + String(e).slice(0, 160)));
  p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) fehler.push('Konsole ' + m.text().slice(0, 160)); });
  p.on('response', r => { if (r.status() >= 400 && !/favicon|marke\.json/.test(r.url())) fehler.push(r.status() + ' ' + r.url().replace(BASIS, '')); });
  p.on('dialog', d => d.accept().catch(() => {}));
  const schritt = async (name, fn) => { const f0 = fehler.length; try { const info = await fn(); const neu = fehler.slice(f0); res.push({ name, ok: !neu.length, info: (neu.length ? neu.join(' | ') + ' · ' : '') + (info || '') }); }
    catch (e) { res.push({ name, ok: false, info: String(e.message || e).split('\n')[0].slice(0, 260) }); } const r = res[res.length - 1]; console.log((r.ok ? 'ok   ' : 'ROT  ') + name + ' · ' + r.info); };
  const ok = (b, was) => { if (!b) throw new Error(was); };
  const api = async (was, d) => p.evaluate(async ([w, d]) => { const r = await fetch(w, d ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) } : {}); return { s: r.status, j: await r.json().catch(() => ({})) }; }, [WZ + 'api/' + was, d]);
  const gehe = async a => { await p.goto('about:blank'); await p.goto(WZ + '#' + a, { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await sleep(900); };
  const ueber = async () => p.evaluate(() => Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - innerWidth);
  const bild = async n => { if (BILDER) { fs.mkdirSync(BILDER, { recursive: true }); await p.screenshot({ path: path.join(BILDER, `${MOTOR}-${W}-${n}.jpg`), quality: 70, type: 'jpeg' }); } };
  const programme = async () => p.evaluate(() => [...document.querySelectorAll('a[href^="mailto:"],a[href^="tel:"],a[href^="sms:"],[data-akt="mail"]')].map(a => a.getAttribute('href') || 'data-akt=mail'));
  const tippe = async loc => { if (HANDY) await loc.tap(); else await loc.click(); };

  await schritt(`Chat ausprobieren: ${FRAGEN.length} Gästefragen nacheinander, jede mit Antwort, Demo-Wort, Feld bleibt sichtbar, kein Programm`, async () => {
    await gehe('start'); const n0 = (await api('anfragen')).j.anfragen.length;
    if (HANDY) { const b = p.locator('#rand [data-probe]'); if (await b.count() && !(await b.isVisible())) await tippe(p.locator('.wo-kopf [data-bereiche], .wo-kopf__ber').first()).catch(() => {}); await sleep(400); }
    const knopf = (await p.locator('#k-probe').isVisible().catch(() => false)) ? p.locator('#k-probe') : p.locator('#rand [data-probe]').first();
    await tippe(knopf); await p.waitForSelector('.ws-handy');
    const antworten = [];
    for (const f of FRAGEN) {
      const n = await p.locator('#probe-l .ws-bl--haus').count();
      await p.fill('#probe-t', f); await p.press('#probe-t', 'Enter');
      await p.waitForFunction(n => document.querySelectorAll('#probe-l .ws-bl--haus').length > n && !document.querySelector('.ws-bl--wartet'), n, { timeout: 25000 });
      antworten.push((await p.locator('#probe-l .ws-bl--haus').last().innerText()).replace(/\s+/g, ' '));
    }
    await sleep(600); await bild('chat-14-fragen');
    const z = await p.evaluate(() => { const t = document.querySelector('#probe-t'), r = t.getBoundingClientRect(); return { feldUnten: Math.round(r.bottom), vh: innerHeight, sichtbar: r.bottom <= innerHeight && r.top >= 0 }; });
    const schl = antworten.filter(a => /Schlüssel|API|Claude|Anthropic|error|Fehler/i.test(a)), ohneDemo = antworten.filter(a => !/Demo|Probe/.test(a));
    const prog = (await programme()).length + (await p.evaluate(() => window.__abgefangen || 0));
    const l = (await api('anfragen')).j.anfragen; const q = l.find(a => a.name === 'QA Demo');
    ok(z.sichtbar, 'Eingabefeld unter dem Rand ' + JSON.stringify(z)); ok(!schl.length, 'Technik im Text: ' + schl[0]); ok(!ohneDemo.length, 'ohne Demo-Wort: ' + ohneDemo[0]);
    ok(!prog, 'Programm-Link im Chat'); ok(q && q.beispiel && l.length === n0 + 1, 'Anfrage mit Kontakt nicht als Beispiel im Eingang'); ok(await ueber() <= 0, 'überläuft');
    await p.keyboard.press('Escape').catch(() => {});
    await api('weg', { id: q.id }); for (const f of (await api('fragen')).j.fragen.filter(f => f.probe && FRAGEN.includes(f.frage))) await api('weg', { id: f.id });
    return `${antworten.length} Antworten, Feld unten ${z.feldUnten}/${z.vh}, Anfrage ${q.art} weggeräumt · letzte: ${antworten[antworten.length - 1].slice(0, 90)}`; });

  await schritt('Eingang: jede Anfrage geöffnet, kein Programm-Link, kein roher Code, kein Überlaufen', async () => {
    await gehe('eingang'); const n = await p.locator('.re-liste .re-a').count(); const funde = [];
    for (let i = 0; i < n; i++) { const k = p.locator('.re-liste .re-a').nth(i); await k.scrollIntoViewIfNeeded(); await tippe(k); await sleep(700);
      const t = await p.evaluate(() => document.querySelector('#detail')?.innerText || ''); const h = (await p.locator('#detail h2').first().innerText().catch(() => '?')).trim();
      if ((await programme()).length) funde.push(h + ': Programm-Link'); if (/\bundefined\b|\bNaN\b|\bNone\b|\bnull\b|\{[^}\n]{0,30}\}/.test(t)) funde.push(h + ': roher Code');
      if (await ueber() > 0) funde.push(h + ': überläuft'); if (i === 0) await bild('eingang-detail'); }
    ok(!funde.length, funde.join('; ')); return n + ' Anfragen geöffnet'; });

  await schritt('Links in allen Ansichten, Anleitung, Prüfseite: kein mailto/tel/sms, jedes Ziel erreichbar', async () => {
    const ziele = new Set(), prog = [];
    for (const a of ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen']) { await gehe(a); prog.push(...(await programme()).map(x => a + ' ' + x));
      for (const h of await p.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.href))) ziele.add(h); }
    for (const s of ['anleitung.html', 'pruefung.html']) { await p.goto(WZ + s, { waitUntil: 'load' }); await sleep(1200); prog.push(...(await programme()).map(x => s + ' ' + x));
      for (const h of await p.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.href))) ziele.add(h); }
    const tot = [];
    for (const z of ziele) { if (!/^https?:/.test(z)) { if (!/^(javascript:|#)/.test(z) && !/^blob:/.test(z)) tot.push('Art ' + z); continue; } const u = z.split('#')[0];
      if (!u.startsWith(BASIS)) continue; const r = await p.request.get(u).catch(() => null); if (!r || r.status() >= 400) tot.push((r ? r.status() : 'x') + ' ' + u.replace(BASIS, '')); }
    ok(!prog.length, 'Programm: ' + prog.join(', ')); ok(!tot.length, 'tot: ' + tot.join(', '));
    const aussen = [...ziele].filter(z => /^https?:/.test(z) && !z.startsWith(BASIS)); return ziele.size + ' Ziele, alle erreichbar' + (aussen.length ? ' · nach aussen: ' + aussen.join(', ').slice(0, 200) : ''); });

  await schritt('Anleitung: alle Bilder geladen, jeder Kapitel-Sprung trifft, kein Überlaufen', async () => {
    await p.goto(WZ + 'anleitung.html', { waitUntil: 'load' }); await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); }); await sleep(1500);
    const z = await p.evaluate(() => ({ kaputt: [...document.images].filter(i => i.getAttribute('src') && (!i.complete || i.naturalWidth === 0)).map(i => i.getAttribute('src')),
      sprung: [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.getElementById(decodeURIComponent(h.slice(1)))), bilder: document.images.length }));
    await bild('anleitung'); ok(!z.kaputt.length, 'kaputt ' + z.kaputt.join(', ')); ok(!z.sprung.length, 'Sprung ins Leere ' + z.sprung.join(', ')); ok(await ueber() <= 0, 'überläuft');
    return z.bilder + ' Bilder geladen, Sprünge ok'; });

  await schritt('Prüfseite: kein Rot, Bild', async () => {
    await p.goto(WZ + 'pruefung.html', { waitUntil: 'load' }); await p.waitForFunction(() => document.querySelectorAll('#lex article').length > 10, null, { timeout: 20000 }); await sleep(1500);
    const rot = await p.evaluate(() => [...document.querySelectorAll('.rot, [data-stand="rot"]')].map(e => e.textContent.trim().slice(0, 60))); await bild('pruefung');
    ok(!rot.length, rot.join('; ')); ok(await ueber() <= 0, 'überläuft'); return (await p.evaluate(() => document.body.innerText.match(/Alles in Ordnung[^\n]*/)?.[0] || document.body.innerText.slice(0, 120))); });

  await br.close();
  const rot = res.filter(r => !r.ok);
  console.log(`\ndemocheck ${MOTOR} ${W}: ${res.length - rot.length} von ${res.length} grün`);
  process.exit(rot.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
