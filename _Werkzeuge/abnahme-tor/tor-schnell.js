#!/usr/bin/env node
// Abnahme-Tor · schnelle Fassung (31.10.2026). Gleiche Strenge wie tor.js (dieselben Messfunktionen messen.js und seite.js,
// jeder Zustand gegen jedes Kriterium), aber ein Bruchteil der Zeit:
//   1. Ein Browser bleibt offen. Zustände werden an Ort und Stelle erkundet und wieder zurückgenommen (Escape, Zurück, Reiter erneut),
//      statt für jeden Zustand einen frischen Browser zu starten und den ganzen Klickweg nachzuspielen (das war 11 von 13 Sekunden).
//      Nur wenn der Rückweg nicht am Ausgangspunkt ankommt, wird der Weg einmal frisch nachgespielt (wird gezählt: «nachgespielt»).
//   2. Einblend-Animationen sind während der Messung aus (Bewegung prüft bewegung-tor.js eigens). Gewartet wird auf Netz und DOM, nicht auf feste Fristen.
//   3. Alle Breiten (1440, 1280, 1000, 390) werden im selben Fenster durch Grössenwechsel gemessen: jeder Zustand in jeder Breite,
//      nicht nur Stichproben. Ergebnis in derselben Form wie tor.js (inventar.json, bilder/, stich-<W>.json, stich-<W>/), auswertung.py liest es unverändert.
//   4. Gleiches Layout wird erkannt (Gerüst der sichtbaren Elemente + Fundmenge): im Inventar steht «gleichWie», die Tafel kann es zusammenfassen.
//      Gemessen wird trotzdem jeder Zustand (die Fotos einer Sammlung haben verschiedene Seitenverhältnisse, also verschiedene Funde).
// Aufruf: node tor-schnell.js <ziele.json> <ausgabe-ordner> --nur <k> [--browser webkit] [--breiten 1440,1280,1000,390] [--max 700] [--tiefe 4]
const path = require('path'), fs = require('fs');
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const S = require('./seite.js');
const S2 = require('./seite-schnell.js');
const messen = require('../messlauf/messen.js');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const [ZIELE, AUS] = process.argv.slice(2);
const CFG = JSON.parse(fs.readFileSync(ZIELE, 'utf8'));
const z = CFG.ziele.find(x => x.k === arg('nur')); if (!z) { console.error('--nur <k> fehlt oder unbekannt'); process.exit(2); }
const BROWSER = arg('browser', 'webkit');
const BREITEN = arg('breiten', '1440,1280,1000,390').split(',').map(Number);
const HOEHE = { 1440: 900, 1280: 800, 1000: 650, 390: 844 };
const [W, H] = [BREITEN[0], HOEHE[BREITEN[0]] || 900];   // Erkundung in der ersten Breite
const MAX = +arg('max', z.max || 700), TIEFE = +arg('tiefe', z.tiefe || 4);
const GEFAHR = z.gefahrExtra ? CFG.gefahr + '|' + z.gefahrExtra : CFG.gefahr;
const stilAusBlatt = f => { const b = JSON.parse(fs.readFileSync(f, 'utf8')); const fam = new Set(['marke', 'wortmarke']);
  for (const r of Object.values(b.rollen || {})) { const sch = [].concat(r.schrift || []); const bild = [].concat(r.rolle || []).some(x => /^(plakat|plakatfett|kopf)$/.test(x));
    if (r.versalien === true || bild) for (const x of sch) fam.add(String(x).replace(/\s*\(.*$/, '').replace(/\s+\d+$/, '').trim()); }
  const rudi = (b.trenner && b.trenner.rudi || ' / ').trim(), menue = (b.trenner && b.trenner.menue || ' | ').trim();
  return { versalienNur: [...fam].join('|'), versalienErlaubt: [...fam].map(x => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), trenner: menue, rudi, quelle: f }; };
const STIL = CFG.stilblatt && fs.existsSync(CFG.stilblatt) ? Object.assign({}, CFG.stil || {}, stilAusBlatt(CFG.stilblatt)) : (CFG.stil || {});
const OPT = { gefahr: GEFAHR, bereich: z.bereich || z.url.replace(/[^/]*$/, ''), dokument: CFG.dokument, dokumentNicht: CFG.dokumentNicht || '', ohne: z.ohne || '', stil: STIL };
const ORDNER = path.join(AUS, z.k), BILDER = path.join(ORDNER, 'bilder');
fs.mkdirSync(BILDER, { recursive: true }); for (const b of BREITEN.slice(1)) fs.mkdirSync(path.join(ORDNER, 'stich-' + b), { recursive: true });
const warte = ms => new Promise(r => setTimeout(r, ms));
const KRIT = { oval: 1, ueberlauf: 2, gekuerzt: 2, rand: 2, wort: 2, reihe: 3, ueberlappt: 5, anschnitt: 5, einzelwort: 7, beschnitten: 13, 'zier-x': 24, 'text-mitte': 35 };
const T0 = Date.now(); let zuletzt = Date.now();
const log = (...a) => { zuletzt = Date.now(); console.log(new Date().toISOString().slice(11, 19), z.k, ...a); };
const HMIN = +process.env.TOR_HAENGER_MIN || 6;
// Schlaf des Macs (Akku, Deckel zu) ist kein Hänger: springt die Uhr zwischen zwei Takten um mehr als 90 s, war der Rechner weg → Zähler zurücksetzen
let takt = Date.now(); const schlief = () => { const jetzt = Date.now(), weg = jetzt - takt > 90e3; takt = jetzt; if (weg) { zuletzt = jetzt; console.log(new Date().toISOString().slice(11, 19), z.k, 'Mac war weg (Schlaf), weiter'); } return weg; };
setInterval(() => { if (schlief()) return; if (Date.now() - zuletzt > HMIN * 60e3) { console.log(new Date().toISOString().slice(11, 19), z.k, `HÄNGER: ${HMIN} Minuten ohne Fortschritt, Lauf beendet`); process.exit(3); } }, 30e3).unref();
let hierZu = null;   // Zustand, in dem die Seite gerade steht
const zaehler = { nachgespielt: 0, rueckweg: { escape: 0, zurueck: 0, reiter: 0, neuladen: 0 }, frist: 0 };
const ohneZahlen = s => String(s).replace(/[\d.,:%]+/g, '#');

(async () => {
  let browser = await pw[BROWSER].launch({ headless: true });
  let ctx, page, kontexte = 0; const NEUSTART = +process.env.TOR_NEUSTART || 60;
  const fehler = []; let offen = 0;   // offene Netz-Anfragen
  const frisch = async () => { const alt = browser; await Promise.race([alt.close().catch(() => { }), warte(15000)]); browser = await pw[BROWSER].launch({ headless: true }); ctx = null; };
  const neuerKontext = async (vorwissen = true) => {
    if (ctx) await Promise.race([ctx.close().catch(() => { }), warte(15000)]);
    if (++kontexte % NEUSTART === 0) await frisch();
    ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, locale: 'de-DE', timezoneId: 'Europe/Berlin', acceptDownloads: false, reducedMotion: process.env.TOR_BEWEGUNG ? 'no-preference' : 'reduce' });
    offen = 0;
    await ctx.route('**/*', r => { const q = r.request(), u = q.url();
      if (/^(mailto|tel):/.test(u)) return r.abort();
      if (q.method() !== 'GET' && q.method() !== 'HEAD') return r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true,"tor":true}' });
      return r.continue(); });
    ctx.on('request', () => offen++); ctx.on('requestfinished', () => offen = Math.max(0, offen - 1)); ctx.on('requestfailed', () => offen = Math.max(0, offen - 1));
    await ctx.addInitScript(v => { try { for (const [k, w] of Object.entries(v.ls || {})) localStorage.setItem(k, w); } catch (e) { } window.open = () => null; window.print = () => { };
      // Animationen aus (nur für die Messung; Bewegung misst bewegung-tor.js): Endzustand sofort, keine 2,5-s-Wartezeit je Schritt
      if (!v.bewegung) { const s = () => { if (document.getElementById('tor-ruhe')) return; const st = document.createElement('style'); st.id = 'tor-ruhe'; st.setAttribute('data-messlauf-aus', ''); st.textContent = '*,*::before,*::after{animation-duration:1ms!important;animation-delay:0s!important;transition-duration:1ms!important;transition-delay:0s!important;scroll-behavior:auto!important}'; (document.head || document.documentElement).appendChild(st); };
        if (document.head) s(); else document.addEventListener('DOMContentLoaded', s); } }, { ls: vorwissen ? (z.localStorage || {}) : {}, bewegung: !!process.env.TOR_BEWEGUNG });
    page = await ctx.newPage();
    ctx.on('page', p => { if (p !== page) p.close().catch(() => { }); });
    page.on('dialog', d => d.dismiss().catch(() => { }));
    page.on('pageerror', e => fehler.push(String(e.message).slice(0, 160)));
  };
  await neuerKontext();

  // Ruhe: Netz leer und DOM 150 ms ohne Änderung (höchstens «max» ms), dazu laufende endliche Animationen abwarten (sind auf 1 ms gestellt)
  // Ruhe: Netz leer (bis 4 s: ein Foto im Editor lädt länger als 1,5 s, sonst wird der Zustand zu früh gelesen), Bilder fertig, DOM 250 ms still
  const ruhe = async (max = 1500) => { const t0 = Date.now(); zuletzt = Date.now();
    while (offen > 0 && Date.now() - t0 < Math.max(max, 4000)) await warte(40);
    await page.evaluate(async () => { const t0 = Date.now(); while (Date.now() - t0 < 3000 && [...document.images].some(i => !i.complete && i.getBoundingClientRect().width > 0)) await new Promise(r => setTimeout(r, 60)); }).catch(() => { });
    await page.evaluate(m => new Promise(res => { let t; const done = () => { mo.disconnect(); res(); }; const mo = new MutationObserver(() => { clearTimeout(t); t = setTimeout(done, 250); }); mo.observe(document.documentElement, { subtree: true, childList: true, attributes: true, characterData: true }); t = setTimeout(done, 250); setTimeout(done, m); }), Math.max(400, max - (Date.now() - t0))).catch(() => { });
    await page.evaluate(async () => { const t0 = Date.now(); while (Date.now() - t0 < 1500) { const a = document.getAnimations().filter(x => x.playState === 'running' && x.effect && x.effect.getTiming().iterations !== Infinity && +x.effect.getTiming().duration > 50); if (!a.length) break; await new Promise(r => setTimeout(r, 60)); } }).catch(() => { }); };
  const lade = async url => { zuletzt = Date.now();
    const ok = await Promise.race([page.goto(url, { waitUntil: 'load', timeout: 25000 }).then(() => true).catch(() => true), warte(45000).then(() => false)]);
    if (!ok) { log('Laden hängt, Browser neu'); await frisch(); await neuerKontext(); await Promise.race([page.goto(url, { waitUntil: 'load', timeout: 30000 }).catch(() => { }), warte(60000)]); }
    await warte(z.warte ? Math.min(z.warte, 600) : 250); await ruhe(2500); };
  const menueAuf = async () => page.evaluate(() => { const t = document.querySelector('.wo-kopf__ber[aria-expanded="false"], .wo-kopf__ber:not([aria-expanded="true"])') || [...document.querySelectorAll('[aria-expanded="false"],button')].find(e => { const r = e.getBoundingClientRect(); return r.width > 0 && /men[üu]|navigation|bereiche|☰/i.test((e.innerText || '') + ' ' + (e.getAttribute('aria-label') || '')); }); if (t) { t.click(); return true; } return false; }).catch(() => false);
  const klickZiel = async () => { zuletzt = Date.now(); const l = page.locator('[data-tor="ziel"]').first();
    try { await l.scrollIntoViewIfNeeded({ timeout: 2000 }); await l.click({ timeout: 3000 }); }
    catch (e) { const ok = await page.evaluate(() => { const e = document.querySelector('[data-tor="ziel"]'); if (!e) return false; e.click(); return true; }).catch(() => false); if (!ok) return false; }
    await warte(120); await ruhe(1500); return true; };
  const schritt = async s => {
    if (s.ziel === 'seite') { await lade(s.href); if (s.gruppe === 'einstieg' && z.einstiegWarte) { await page.waitForSelector(z.einstiegWarte, { state: 'visible', timeout: 15000 }).catch(() => { }); await ruhe(800); } return true; }
    if (s.ziel === 'dokklick') { const ok = await page.evaluate(([re, nicht]) => { const R = new RegExp(re), N = nicht ? new RegExp(nicht) : null; const d = [...document.querySelectorAll('*')].filter(e => typeof e.className === 'string' && R.test(' ' + e.className + ' ') && !(N && N.test(' ' + e.className + ' ')) && e.getBoundingClientRect().height >= 300).sort((a, b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height)[0];
        if (!d) return false; const t = [...d.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2) && e.getBoundingClientRect().width > 20).sort((a, b) => parseFloat(getComputedStyle(b).fontSize) - parseFloat(getComputedStyle(a).fontSize))[0];
        if (!t) return false; document.querySelectorAll('[data-tor="ziel"]').forEach(e => e.removeAttribute('data-tor')); t.setAttribute('data-tor', 'ziel'); return true; }, [CFG.dokument, CFG.dokumentNicht || '']).catch(() => false);
      if (!ok) return false; }
    else { let ok = await page.evaluate(S.finde, s).catch(() => false);
      if (!ok || !(await page.locator('[data-tor="ziel"]').first().isVisible().catch(() => false))) { if (await menueAuf()) { await ruhe(600); ok = await page.evaluate(S.finde, s).catch(() => false); } }
      if (!ok) return false; }
    return klickZiel(); };
  // Weg frisch nachspielen (nur, wenn der Rückweg nicht ankommt)
  const nachspielen = async weg => { zaehler.nachgespielt++; hierZu = null; await neuerKontext(); await lade(z.url);
    for (const s of weg) { const r = await Promise.race([schritt(s), warte(90000).then(() => 'frist')]); if (r === 'frist') { log('SCHRITT HÄNGT, Browser neu:', (s.text || '').slice(0, 40)); await frisch(); await neuerKontext(); return false; } if (!r) return false; } return true; };
  const sig = async () => Promise.race([page.evaluate(S.signatur, OPT).catch(() => null), warte(60000).then(() => null)]);
  const kern = s => s ? [s.weg, s.aktiv.map(ohneZahlen).join(','), s.fenster.map(ohneZahlen).join(','), s.dok.gross + ':' + s.dok.lage.join(',')].join('¶') : null;
  const schluessel = s => s ? kern(s) + '¶' + s.titel.map(ohneZahlen).join('|') : null;   // Kennung eines Zustands (wie tor.js, nur ohne Zahlen in Titeln)

  // ---------- Messung eines Zustands in allen Breiten ----------
  let nr = 0; const stich = {}; for (const b of BREITEN.slice(1)) stich[b] = [];
  const messeHier = async (zu, w, h, ordner, bildName) => {
    const y0 = await page.evaluate(() => scrollY).catch(() => 0);
    const hoch = () => page.evaluate(() => document.documentElement.scrollHeight).catch(() => 0);
    for (let y = 0; y < Math.min(await hoch(), 14000); y += h * .8) { await page.evaluate(v => scrollTo(0, v), y).catch(() => { }); await warte(25); }
    await page.evaluate(() => scrollTo(0, 0)).catch(() => { }); await ruhe(600);
    await page.evaluate(S.verdeckte).catch(() => 0);
    const m = await Promise.race([page.evaluate(messen), warte(20000).then(() => [{ art: 'fehler', sel: '', text: '', info: 'Messung über 20 s', r: { x: 0, y: 0, w: 1, h: 1 } }])]).catch(e => [{ art: 'fehler', sel: '', text: '', info: String(e).slice(0, 120), r: { x: 0, y: 0, w: 1, h: 1 } }]);
    const e = await page.evaluate(S.ergaenzung, OPT).catch(e => ({ funde: [{ k: 0, art: 'fehler', info: String(e).slice(0, 120) }], doks: [], bilder: [] }));
    const sy = await page.evaluate(() => scrollY).catch(() => 0);
    const echt = f => { if (f.art === 'oval') { const g = f.info.match(/([\d.]+) × ([\d.]+)/); if (g && Math.max(+g[1], +g[2]) / Math.min(+g[1], +g[2]) > 2) return false; }
      if (f.art === 'reihe') { const hh = f.info.match(/Höhe (\d+)–(\d+)/); if (hh && +hh[2] / +hh[1] > 1.4) return false; } return true; };
    zu.funde = [...m.filter(echt).map(f => ({ k: KRIT[f.art] ?? 0, art: f.art, sel: f.sel, text: f.text, info: f.info, r: f.fest ? f.r : { ...f.r, y: f.r.y + sy } })), ...e.funde];
    zu.bild = `${bildName}.jpg`;
    await page.screenshot({ path: path.join(ordner, zu.bild), type: 'jpeg', quality: 70 }).catch(() => { zu.bild = null; });
    if (y0 > 40) { await page.evaluate(v => scrollTo(0, v), y0).catch(() => { }); await warte(150); zu.bildOrt = `${bildName}-ort.jpg`;
      await page.screenshot({ path: path.join(ordner, zu.bildOrt), type: 'jpeg', quality: 70 }).catch(() => { zu.bildOrt = null; }); await page.evaluate(() => scrollTo(0, 0)).catch(() => { }); }
    const ph = await hoch() || h;
    const clip = (r, rand) => { const x = Math.max(0, r.x - rand), y = Math.max(0, r.y - rand); return { x, y, width: Math.min(w - x, r.w + 2 * rand), height: Math.min(ph - y, r.h + 2 * rand) }; };
    zu.doks = []; zu.kacheln = [];
    for (const [i, d] of e.doks.entries()) { if (d.r.h < 110 || d.r.w < 70 || d.r.x < 0 || d.r.x + d.r.w > w + 2) continue; const f = `${bildName}-d${i}.png`; const c = clip(d.r, 0); if (c.width < 20 || c.height < 20) continue;
      await page.screenshot({ path: path.join(ordner, f), clip: c, fullPage: true }).then(() => zu.doks.push({ datei: f, r: d.r, sel: d.sel })).catch(() => { }); }
    for (const [i, d] of e.bilder.entries()) { if (d.r.x < 0 || d.r.x + d.r.w > w + 2) continue; const f = `${bildName}-k${i}.png`; const c = clip(d.r, 0); if (c.width < 20 || c.height < 20) continue;
      await page.screenshot({ path: path.join(ordner, f), clip: c, fullPage: true }).then(() => zu.kacheln.push({ datei: f, r: d.r, sel: d.sel })).catch(() => { }); }
    await page.evaluate(() => document.querySelectorAll('[data-messlauf-aus="verdeckt"]').forEach(e => e.removeAttribute('data-messlauf-aus'))).catch(() => { });
    await page.evaluate(() => scrollTo(0, 0)).catch(() => { });
  };
  const messe = async (zu, versuch = 0) => {
    try { await messeRoh(zu); }
    catch (e) { if (versuch >= 1 || !/crashed|closed|Target/i.test(String(e))) throw e;
      log(zu.id, 'BROWSER ABGESTÜRZT beim Messen, neu starten und nachspielen'); zaehler.absturz = (zaehler.absturz || 0) + 1;
      await frisch(); if (!(await nachspielen(zu.weg || []))) throw e; hierZu = null; await messe(zu, versuch + 1); } };
  const messeRoh = async zu => {
    const t0 = Date.now();
    await messeHier(zu, W, H, BILDER, zu.id);
    zu.skelett = await page.evaluate(S2.skelett).catch(() => '');
    zu.dauer = {}; zu.dauer[W] = Date.now() - t0;
    for (const b of BREITEN.slice(1)) { const t1 = Date.now(); const h = HOEHE[b] || 800;
      await page.setViewportSize({ width: b, height: h }); await ruhe(800);
      const s = { id: zu.id, name: zu.name, art: zu.art };
      await messeHier(s, b, h, path.join(ORDNER, 'stich-' + b), zu.id);
      // Handy: Menü einmal offen messen (wie der Messlauf «Menü offen»), nur in Start- und Navigationszuständen
      if (b < 700 && ['start', 'navigation', 'reiter', 'unterseite'].includes(zu.art) && await menueAuf()) { await ruhe(600); const sm = { id: zu.id + 'm', name: zu.name + ' · Menü offen', art: 'menue' }; await messeHier(sm, b, h, path.join(ORDNER, 'stich-' + b), zu.id + 'm'); s.menueOffen = sm; stich[b].push(sm); await page.keyboard.press('Escape').catch(() => { }); await menueZu(); }
      stich[b].push(s); zu.dauer[b] = Date.now() - t1; }
    await page.setViewportSize({ width: W, height: H }); await ruhe(800);
  };
  const menueZu = async () => page.evaluate(() => { const t = document.querySelector('.wo-kopf__ber[aria-expanded="true"],[aria-expanded="true"]'); if (t) t.click(); }).catch(() => { });
  const sichere = (fertig = false) => {
    fs.writeFileSync(path.join(ORDNER, 'inventar.json'), JSON.stringify({ zeit: new Date().toISOString(), browser: BROWSER, groesse: [W, H], breiten: BREITEN, werkzeug: z, zustaende, kanten, nichtErreicht, fehler: fehler.slice(0, 50), zaehler, dauerMin: Math.round((Date.now() - T0) / 6000) / 10, voll: fertig ? zustaende.length < MAX : undefined, tor: 'schnell' }, null, 1));
    for (const b of BREITEN.slice(1)) fs.writeFileSync(path.join(ORDNER, `stich-${b}.json`), JSON.stringify({ zeit: new Date().toISOString(), browser: BROWSER, groesse: [b, HOEHE[b] || 800], zustaende: stich[b] }, null, 1)); };

  const art = (k, vorher, nachher) => {
    if (!k) return 'start';
    if (k.ziel === 'dokklick') return 'editor-leiste';
    if (k.ziel === 'seite') return 'unterseite';
    if (nachher.dok.gross && !vorher.dok.gross) return 'dokument';
    if (nachher.fenster.length > vorher.fenster.length) return /neu|erstell|anleg|\+/i.test(k.text) ? 'neu-erstellen' : 'fenster';
    if (k.rolle === 'tab' || /reiter|tab/.test(k.gruppe)) return 'reiter';
    if (k.wo !== 'haupt') return 'navigation';
    return /neu|erstell|anleg/i.test(k.text) ? 'neu-erstellen' : 'ansicht'; };

  // ---------- Inventar ----------
  const zustaende = [], bekannt = new Map(), bekanntWeg = new Map(), geklickt = new Set(), kanten = [], nichtErreicht = [];
  const wegKey = w => (w || []).map(s => s.key || s.text).join('→');
  const eltern = x => x.weg && x.weg.length ? bekanntWeg.get(wegKey(x.weg.slice(0, -1))) : null;

  const neu = async (weg, k, vorher, s, tiefe) => {
    const id = String(++nr).padStart(3, '0');
    const name = k ? (vorher.name === 'Start' ? '' : vorher.name + ' → ') + (k.ziel === 'dokklick' ? 'Leiste am Dokument' : k.text.split(' ').slice(0, 7).join(' ')) : 'Start';
    const zu = { id, k: z.k, werkzeug: z.name, name, art: art(k, vorher || s, s), tiefe, weg, sig: s.sig, url: page.url(), titel: s.titel, aktiv: s.aktiv, fenster: s.fenster, dok: s.dok, inhalt: s.inhalt, steuer: k ? { text: k.text, wo: k.wo, gruppe: k.gruppe } : null };
    zu.kern = kern(s); zu.eltern = weg.length ? (bekanntWeg.get(wegKey(weg.slice(0, -1))) || {}).id : null;
    await messe(zu); bekannt.set(schluessel(s), zu); bekanntWeg.set(wegKey(weg), zu); zustaende.push(zu);
    const fk = zu.funde.map(f => f.art + '|' + f.sel + '|' + ohneZahlen(f.info || '')).sort().join('¦');
    const g = zustaende.find(q => q !== zu && q.skelett && q.skelett === zu.skelett && q.fundeKey === fk); zu.fundeKey = fk; if (g) zu.gleichWie = g.gleichWie || g.id;
    log(id, zu.art, name.slice(0, 60), '·', zu.funde.length, 'Funde', '·', Object.values(zu.dauer).reduce((a, b) => a + b, 0) / 1000 + ' s', zu.gleichWie ? '· wie ' + zu.gleichWie : '');
    sichere();
    return zu; };

  // Ausgangspunkt eines Zustands wiederherstellen, billig: Escape (Fenster), Zurück (Adresse), Reiter erneut, sonst Weg nachspielen
  const zurueck = async (x, s, sx, billig) => {
    const zielKern = sx ? kern(sx) : x.kern;
    const nahe = n => { const [w1, a1, f1, d1] = kern(n).split('¶'), [w2, a2, f2, d2] = zielKern.split('¶'); if (w1 !== w2 || f1 !== f2 || d1 !== d2) return false; const A = a2 ? a2.split(',') : [], B = new Set(a1 ? a1.split(',') : []); if (!A.length) return !B.size; return A.filter(v => B.has(v)).length >= Math.ceil(A.length / 2); };
    const da = async () => { const n = await sig(); if (!n) return null; if (kern(n) === zielKern) return n; if (nahe(n)) { zaehler.rueckweg.nahe = (zaehler.rueckweg.nahe || 0) + 1; return n; } return null; };
    let n;
    if (s && s.fenster.length > (sx ? sx.fenster.length : x.fenster.length)) { await page.keyboard.press('Escape').catch(() => { }); await ruhe(500); if ((n = await da())) { zaehler.rueckweg.escape++; return n; }
      await page.evaluate(() => { const b = [...document.querySelectorAll('dialog[open] button,[role=dialog] button,[class*="fenster"] button,[class*="rechts"] button,[class*="dialog"] button,[class*="modal"] button')].find(b => /schlie|zu\b|×|✕|abbrech|fertig/i.test((b.innerText || '') + ' ' + (b.getAttribute('aria-label') || '') + ' ' + b.className)); if (b) b.click(); }).catch(() => { }); await ruhe(500); if ((n = await da())) { zaehler.rueckweg.escape++; return n; } }
    const ohneAnker = u => String(u).split('#')[0];
    if (ohneAnker(page.url()) !== ohneAnker(x.url)) { await page.goBack({ timeout: 8000 }).catch(() => { }); await ruhe(1200);
      if (/^about:blank/.test(page.url())) { await page.goForward({ timeout: 8000 }).catch(() => { }); await ruhe(1200); } else if ((n = await da())) { zaehler.rueckweg.zurueck++; return n; } }
    const letzter = x.weg[x.weg.length - 1];
    if (letzter && letzter.ziel !== 'dokklick' && letzter.ziel !== 'seite') { if (await page.evaluate(S.finde, letzter).catch(() => false)) { await klickZiel(); if ((n = await da())) { zaehler.rueckweg.reiter++; return n; } } }
    if (!x.weg.length) { // zum Start: den Navigationspunkt der Start-Ansicht anklicken (die Werkzeuge merken sich die letzte Ansicht, Neuladen hilft nicht)
      const ok = await page.evaluate(akt => { document.querySelectorAll('[data-tor="ziel"]').forEach(e => e.removeAttribute('data-tor')); const t = e => (e.innerText || e.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 50); const el = [...document.querySelectorAll('nav button,nav a,aside button,aside a,header button,header a,[role=tab],[data-ansicht],[data-gehe]')].find(e => akt.includes(t(e)) && e.getBoundingClientRect().width > 0); if (!el) return false; el.setAttribute('data-tor', 'ziel'); return true; }, x.aktiv || []).catch(() => false);
      if (process.env.TOR_SPUR) console.log('SPUR start-nav gefunden:', ok, 'url', page.url());
      if (ok && await klickZiel()) { if ((n = await da())) { zaehler.rueckweg.reiter++; return n; } if (process.env.TOR_SPUR) { const q = await sig(); console.log('SPUR nach start-nav:', q && kern(q).slice(0, 100)); } }
      await lade(z.url); if ((n = await da())) { zaehler.rueckweg.neuladen++; return n; } }
    if (billig) return null;
    if (process.env.TOR_SPUR) { const q = await sig(); console.log('SPUR zurueck zu', x.id, 'scheitert; ist:', q && kern(q).slice(0, 140), '| soll:', zielKern.slice(0, 140), '| aktiv:', JSON.stringify(x.aktiv)); }
    if (await nachspielen(x.weg)) { hierZu = x; if ((n = await da())) return n; }
    return null; };

  await lade(z.url); let s0 = await sig();
  for (let v = 0; v < 3 && (!s0 || !s0.titel.length); v++) { await warte(1500); await lade(z.url); s0 = await sig(); }
  await neu([], null, null, s0, 0);
  if (z.localStorage && Object.keys(z.localStorage).length) {
    await neuerKontext(false); await lade(z.url); const s = await sig(); if (s && !bekannt.has(schluessel(s))) { const zu = await neu([], { text: 'Erster Besuch', wo: 'haupt', gruppe: '', ziel: 'erstbesuch' }, bekannt.get(schluessel(s0)), s, 0); zu.art = 'erstbesuch'; zu.weg = null; bekanntWeg.set('', bekannt.get(schluessel(s0))); }
    await neuerKontext(); await lade(z.url); }

  const schlange = [bekannt.get(schluessel(s0))];
  for (const u of z.startExtra || []) { const k = { ziel: 'seite', href: u, text: u.split('/').pop() || u, wo: 'haupt', gruppe: 'einstieg', key: 'einstieg|' + u };
    if (await nachspielen([k])) { const s = await sig(); if (s && !bekannt.has(schluessel(s))) schlange.push(await neu([k], k, bekannt.get(schluessel(s0)), s, 1)); } }

  // Erkundung: Breite zuerst, aber an Ort und Stelle. Ein Zustand wird betreten, seine Kandidaten der Reihe nach geklickt,
  // nach jedem Klick wird der Ausgangspunkt billig wiederhergestellt; neue Zustände kommen hinten in die Schlange.
  const istHier = async x => { const n = await sig(); return n && kern(n) === x.kern ? n : null; };
  // Zustand betreten, ohne den Weg von vorn zu gehen: vom jetzigen Zustand zum gemeinsamen Vorfahren zurück (billig), dann die restlichen Schritte
  const betrete = async x => {
    if (hierZu === x) { const n = await istHier(x); if (n) return n; }
    let cur = hierZu; const vorfahr = c => c && wegKey(x.weg).startsWith(wegKey(c.weg)) && (x.weg.length === c.weg.length || wegKey(x.weg.slice(0, c.weg.length)) === wegKey(c.weg));
    const SP = (...a) => process.env.TOR_SPUR && console.log('SPUR betrete', x.id, ...a);
    for (let i = 0; cur && !vorfahr(cur) && i < 6; i++) { const e = eltern(cur); if (!e) { SP('kein Eltern von', cur.id); cur = null; break; } const s = await sig(); const n = await zurueck(e, s, null, true); if (!n) { SP('Rückweg zu', e.id, 'kommt nicht an; ist:', s && kern(s).slice(0, 120), '| soll:', e.kern.slice(0, 120)); cur = null; break; } cur = e; }
    if (cur) { let ok = true; for (const s of x.weg.slice(cur.weg.length)) { if (!(await schritt(s))) { SP('Schritt scheitert von', cur.id, ':', (s.text || '').slice(0, 30)); ok = false; break; } }
      if (ok) { const n = await istHier(x); if (n) { hierZu = x; return n; } const q = await sig(); SP('nach Schritten nicht da; ist:', q && kern(q).slice(0, 120), '| soll:', x.kern.slice(0, 120)); } }
    else SP('kein Vorfahr; hierZu', hierZu && hierZu.id);
    // Die Schritte des Zielwegs direkt vom jetzigen Zustand aus gehen (Navigationspunkte sind von überall erreichbar)
    if (hierZu || cur) { let ok = true; for (const s of x.weg) { if (s.ziel === 'seite' && s.gruppe !== 'einstieg' && page.url().split('#')[0] === String(s.href).split('#')[0]) continue; if (!(await schritt(s))) { ok = false; break; } }
      if (ok) { const n = await istHier(x); if (n) { zaehler.rueckweg.direkt = (zaehler.rueckweg.direkt || 0) + 1; hierZu = x; return n; } } SP('direkt nicht angekommen'); }
    const ok = await nachspielen(x.weg); hierZu = ok ? x : null; return ok ? await istHier(x) || await sig() : null; };
  let seitNeustart = 0;
  while (schlange.length && zustaende.length < MAX) {
    const x = schlange.shift(); if (x.tiefe >= TIEFE || !x.weg) continue;
    if (zustaende.length - seitNeustart >= NEUSTART) { seitNeustart = zustaende.length; log('Browser frisch nach', zustaende.length, 'Zuständen'); await frisch(); hierZu = null; }
    try { await erkunde(x); } catch (e) { log(x.id, 'FEHLER im Zustand, weiter:', String(e).slice(0, 120)); zaehler.fehler = (zaehler.fehler || 0) + 1; await frisch(); hierZu = null; }
  }
  async function erkunde(x) {
    let hier = await betrete(x); if (!hier) { nichtErreicht.push({ id: x.id, name: x.name }); return; }
    // vor dem Sammeln einmal durchrollen: nachgeladene Listen und erst beim Hinrollen gezeigte Stücke (z. B. die 232 Fotos) sind sonst nicht da
    const durchrollen = async () => { const hoch = () => page.evaluate(() => document.documentElement.scrollHeight).catch(() => 0); for (let y = 0; y < Math.min(await hoch(), 14000); y += H * .8) { await page.evaluate(v => scrollTo(0, v), y).catch(() => { }); await warte(25); } await page.evaluate(() => scrollTo(0, 0)).catch(() => { }); await ruhe(400); };
    await durchrollen();
    let kand = await Promise.race([page.evaluate(S.kandidaten, OPT).catch(() => []), warte(60000).then(() => [])]);
    for (let v = 0; v < 2 && !kand.length; v++) { await warte(1500); hier = (await betrete(x)) || hier; kand = await page.evaluate(S.kandidaten, OPT).catch(() => []); }
    const proGruppe = {}; const liste = [];
    for (const k of kand) { const key = k.gruppe + '|' + k.text + '|' + k.nr; const kette = x.weg.length && x.weg[x.weg.length - 1].key === key;
      if (geklickt.has(key) && !kette) continue; k.key = key;
      if (k.gruppenZahl > 8 && k.wo === 'haupt') { proGruppe[k.gruppe] = (proGruppe[k.gruppe] || 0) + 1; if (proGruppe[k.gruppe] > 3) { (x.rest = x.rest || {})[k.gruppe] = (x.rest[k.gruppe] || []).concat([k]); continue; } }
      liste.push(k); }
    const dokGruppen = new Set();
    const bediene = async k => {
      geklickt.add(k.key);
      if (!(await schritt(k))) return;
      const s = await sig(); if (!s) return;
      kanten.push({ von: x.id, text: k.text, wo: k.wo, gruppe: k.gruppe, nach: s.sig });
      if (schluessel(s) !== schluessel(hier)) {
        const sk = schluessel(s);
        if (!bekannt.has(sk) && zustaende.length < MAX) { const zu = await neu([...x.weg, { ...k, key: k.key }], k, x, s, x.tiefe + 1); schlange.push(zu); if (s.dok.gross) dokGruppen.add(k.gruppe); }
        else if (bekannt.has(sk) && s.dok.gross) dokGruppen.add(k.gruppe);
        const n = await zurueck(x, s, hier) || await wiederHin(x); if (!n) { hierZu = null; return 'weg'; } hier = n; hierZu = x;
      } else if (page.url().split('#')[0] !== x.url.split('#')[0]) { const n = await zurueck(x, s, hier) || await wiederHin(x); if (!n) { hierZu = null; return 'weg'; } hier = n; } };
    // letzter Versuch, den Zustand wieder zu betreten: frisch nachspielen und auch einen nahen Zustand annehmen
    const wiederHin = async () => { if (!(await nachspielen(x.weg))) return null; const n = await sig(); if (!n) return null; if (kern(n) === x.kern) return n;
      const [w1, a1, f1, d1] = kern(n).split('¶'), [w2, , f2, d2] = x.kern.split('¶'); if (w1 === w2 && f1 === f2 && d1 === d2) { zaehler.rueckweg.nahe = (zaehler.rueckweg.nahe || 0) + 1; return n; } return null; };
    const FRIST = (+process.env.TOR_KLICK_MIN || 2) * 60e3;
    const mitFrist = async k => { let t; const start = Date.now(); const r = await Promise.race([bediene(k), new Promise(ok => { const f = () => { if (Date.now() - takt > 90e3 || Date.now() - start < FRIST - 5e3) { takt = Date.now(); t = setTimeout(f, FRIST); } else ok('frist'); }; t = setTimeout(f, FRIST); })]); clearTimeout(t);
      if (r !== 'frist') return r;
      zaehler.frist++; log(x.id, 'KLICK HÄNGT, übersprungen:', (x.name || '').slice(0, 50), '→', (k.text || '').slice(0, 40)); nichtErreicht.push({ id: x.id, name: x.name, klick: k.text, grund: 'Klick hängt' });
      await frisch(); const ok = await nachspielen(x.weg); hierZu = ok ? x : null; if (!ok) return 'weg'; hier = await sig() || hier; };
    const abbruch = (k, offen) => { log(x.id, 'ZUSTAND NICHT WIEDER ERREICHT nach', (k.text || '').slice(0, 40), '·', offen, 'Klicks offen', x.wiederholt ? '' : '→ kommt noch einmal in die Schlange'); nichtErreicht.push({ id: x.id, name: x.name, klick: k.text, grund: 'Rückweg scheitert', offen }); if (!x.wiederholt) { x.wiederholt = true; schlange.push(x); } };
    for (const [i, k] of liste.entries()) { if (zustaende.length >= MAX) break; if ((await mitFrist(k)) === 'weg') { abbruch(k, liste.length - i - 1); return; } }
    for (const [g, rest] of Object.entries(x.rest || {})) {
      if (dokGruppen.has(g) || /vorlage|stueck|dok|doc|medium|karte|plakat|brief|mail/i.test(g)) { for (const [i, k] of rest.entries()) { if (zustaende.length >= MAX) break; if ((await mitFrist(k)) === 'weg') { abbruch(k, rest.length - i - 1); return; } } }
      else { // gleichartige Stücke ohne Dokument: dazu längster und kürzester Text, nicht nur die ersten drei
        const nachLaenge = [...rest].sort((a, b) => (b.text || '').length - (a.text || '').length); const extra = [nachLaenge[0], nachLaenge[nachLaenge.length - 1]].filter((k, i, a) => k && a.indexOf(k) === i);
        for (const [i, k] of extra.entries()) { if (zustaende.length >= MAX) break; if ((await mitFrist(k)) === 'weg') { abbruch(k, extra.length - i - 1); return; } }
        x.gleichartig = (x.gleichartig || []).concat([{ gruppe: g, zahl: rest.length + 3, bedient: 3 + extra.length }]); } }
    // Editor: hohes und queres Dokument einmal mit offener Leiste
    if (hier.dok.gross && !x.leisteProbe) { const lage = hier.dok.lage[0]; const schon = zustaende.filter(q => q.art === 'editor-leiste' && q.dok.lage[0] === lage).length;
      if (schon < 2) { x.leisteProbe = true; const k = { ziel: 'dokklick', key: 'dok|' + x.id, text: 'Leiste am Dokument', wo: 'haupt', gruppe: 'dok' }; if (await schritt(k)) { const s = await sig(); if (s && schluessel(s) !== schluessel(hier) && !bekannt.has(schluessel(s))) await neu([...x.weg, k], k, x, s, x.tiefe + 1); const n = await zurueck(x, s, hier); if (n) { hier = n; hierZu = x; } else hierZu = null; } } }
  }
  log('Inventar fertig:', zustaende.length, 'Zustände', nichtErreicht.length ? `(${nichtErreicht.length} nicht erreicht)` : '', '·', Math.round((Date.now() - T0) / 60000), 'min ·', JSON.stringify(zaehler));
  sichere(true);
  await browser.close();
})();
