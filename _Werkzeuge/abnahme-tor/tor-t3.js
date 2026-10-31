#!/usr/bin/env node
// Abnahme-Tor · Inventar und Messung in einem Lauf (OBERCHEF-PAKET «Abnahme-Tor vor Robert», ROBERTS-KRITERIEN.md).
// Das Inventar wird aus dem Werkzeug selbst gelesen: jede bedienbare Stelle wird angeklickt, jeder neue Zustand (Navigation, Reiter,
// Fenster, «Neu erstellen», Vorlage, Dokument, Editor mit offener Leiste, Unterseite) kommt ins Inventar und wird sofort gemessen.
// Kommt ein Zustand im Werkzeug dazu, steht er beim nächsten Lauf im Inventar, ohne dass jemand eine Liste pflegt.
// Tor-3-Kopie (30.10.2026): Stichprobe speichert nach jedem Zustand, --ab N setzt nach Hänger fort.
// Aufruf: node tor.js <ziele.json> <ausgabe-ordner> --nur <k> [--browser webkit] [--groesse 1440x900] [--max 450] [--tiefe 4]
//         node tor.js <ziele.json> <ausgabe-ordner> --nur <k> --stichprobe 1280x800   (spielt Zustände des Inventars in anderer Grösse nach)
const path = require('path'), fs = require('fs');
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const S = require('./seite.js');
const messen = require('../messlauf/messen.js');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const [ZIELE, AUS] = process.argv.slice(2);
const CFG = JSON.parse(fs.readFileSync(ZIELE, 'utf8'));
const z = CFG.ziele.find(x => x.k === arg('nur')); if (!z) { console.error('--nur <k> fehlt oder unbekannt'); process.exit(2); }
const BROWSER = arg('browser', 'webkit');
const STICH = arg('stichprobe');
const [W, H] = (STICH || arg('groesse', '1440x900')).split('x').map(Number);
const MAX = +arg('max', z.max || 450), TIEFE = +arg('tiefe', z.tiefe || 4);
const GEFAHR = z.gefahrExtra ? CFG.gefahr + '|' + z.gefahrExtra : CFG.gefahr;   // je Ziel zusätzlich gesperrte Klicks (z. B. Schritte einer Führung, die das Tor festhalten)
// K12 aus dem Stilblatt des Hauses (CFG.stilblatt): Versalien nur in Rollen mit «versalien: true» und den Bild-Rollen (plakat, plakatfett, kopf),
// Rudis Zeilen (Versalien mit Trenner «/») sind Hausregel; «/» zwischen Wörtern ist nur in gemischt geschriebenen Lesezeilen falsch (Menü «|»).
const stilAusBlatt = f => { const b = JSON.parse(fs.readFileSync(f, 'utf8')); const fam = new Set(['marke', 'wortmarke']);
  for (const r of Object.values(b.rollen || {})) { const sch = [].concat(r.schrift || []); const bild = [].concat(r.rolle || []).some(x => /^(plakat|plakatfett|kopf)$/.test(x));
    if (r.versalien === true || bild) for (const x of sch) fam.add(String(x).replace(/\s*\(.*$/, '').replace(/\s+\d+$/, '').trim()); }
  const rudi = (b.trenner && b.trenner.rudi || ' / ').trim(), menue = (b.trenner && b.trenner.menue || ' | ').trim();
  return { versalienNur: [...fam].join('|'), versalienErlaubt: [...fam].map(x => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), trenner: menue, rudi, quelle: f }; };
const STIL = CFG.stilblatt ? Object.assign({}, CFG.stil || {}, stilAusBlatt(CFG.stilblatt)) : (CFG.stil || {});
const OPT = { gefahr: GEFAHR, bereich: z.bereich || z.url.replace(/[^/]*$/, ''), dokument: CFG.dokument, dokumentNicht: CFG.dokumentNicht || '', ohne: z.ohne || '', stil: STIL };
const ORDNER = path.join(AUS, z.k), BILDER = path.join(ORDNER, STICH ? 'stich-' + W : 'bilder');
fs.mkdirSync(BILDER, { recursive: true });
const warte = ms => new Promise(r => setTimeout(r, ms));
const KRIT = { oval: 1, ueberlauf: 2, gekuerzt: 2, rand: 2, wort: 2, reihe: 3, ueberlappt: 5, anschnitt: 5, einzelwort: 7, beschnitten: 13, 'zier-x': 24, 'text-mitte': 35 };
let zuletzt = Date.now();
const log = (...a) => { zuletzt = Date.now(); console.log(new Date().toISOString().slice(11, 19), z.k, ...a); };
// Wächter: hängt das Werkzeug (z. B. ein Klick wartet ewig), endet der Lauf nach 6 Minuten ohne Fortschritt; das Inventar bleibt bis dahin gespeichert, der Hänger steht im Protokoll
const HMIN = +process.env.TOR_HAENGER_MIN || 6;   // bei hoher Last länger warten (Oberchef 30.10.: Last bis 270)
setInterval(() => { if (Date.now() - zuletzt > HMIN * 60e3) { console.log(new Date().toISOString().slice(11, 19), z.k, `HÄNGER: ${HMIN} Minuten ohne Fortschritt, Lauf beendet`); process.exit(3); } }, 30e3).unref();

(async () => {
  const browser = await pw[BROWSER].launch({ headless: true });
  const hand = W < 700;
  // Jeder Weg beginnt in einem frischen Browserkontext: die Werkzeuge merken sich Ansicht, Ablage und Entwürfe im Browser,
  // sonst verschiebt das Durchklicken selbst den Ausgangspunkt (Gegenprobe 29.10.: 47 Zustände nicht wieder erreicht)
  let ctx, page;
  const fehler = [];
  const neuerKontext = async (vorwissen = true) => {
    if (ctx) await ctx.close().catch(() => { });
    ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, locale: 'de-DE', timezoneId: 'Europe/Berlin', hasTouch: hand, acceptDownloads: false });
    await ctx.route('**/*', r => { const q = r.request(), u = q.url();
      if (/^(mailto|tel):/.test(u)) return r.abort();
      if (q.method() !== 'GET' && q.method() !== 'HEAD') return r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true,"tor":true}' });
      return r.continue(); });
    await ctx.addInitScript(v => { try { for (const [k, w] of Object.entries(v || {})) localStorage.setItem(k, w); } catch (e) { } window.open = () => null; window.print = () => { }; }, vorwissen ? (z.localStorage || {}) : {});
    page = await ctx.newPage();
    ctx.on('page', p => { if (p !== page) p.close().catch(() => { }); });
    page.on('dialog', d => d.dismiss().catch(() => { }));
    page.on('pageerror', e => fehler.push(String(e.message).slice(0, 160)));
  };
  await neuerKontext();

  const ruhe = async () => { await page.evaluate(async () => { const t0 = Date.now();
      while (Date.now() - t0 < 2500) { const a = document.getAnimations().filter(x => x.playState === 'running' && x.effect && x.effect.getTiming().iterations !== Infinity); if (!a.length) break; await new Promise(r => setTimeout(r, 100)); } }).catch(() => { }); await warte(120); };
  const lade = async url => { await page.goto(url, { waitUntil: 'load', timeout: 30000 }).catch(() => { }); await warte(z.warte || 1400); await ruhe(); };
  const menueAuf = async () => page.evaluate(() => { const t = document.querySelector('.wo-kopf__ber[aria-expanded="false"], .wo-kopf__ber:not([aria-expanded="true"])') || [...document.querySelectorAll('[aria-expanded="false"],button')].find(e => { const r = e.getBoundingClientRect(); return r.width > 0 && /men[üu]|navigation|bereiche|☰/i.test((e.innerText || '') + ' ' + (e.getAttribute('aria-label') || '')); }); if (t) { t.click(); return true; } return false; }).catch(() => false);
  const schritt = async s => {
    if (s.ziel === 'seite') { await lade(s.href); if (s.gruppe === 'einstieg' && z.einstiegWarte) { await page.waitForSelector(z.einstiegWarte, { state: 'visible', timeout: 15000 }).catch(() => { }); await warte(900); } return true; }   // z. B. Rundgang-Karte erscheint erst nach Ruhe der Seite
    if (s.ziel === 'dokklick') { const ok = await page.evaluate(([re, nicht]) => { const R = new RegExp(re), N = nicht ? new RegExp(nicht) : null; const d = [...document.querySelectorAll('*')].filter(e => typeof e.className === 'string' && R.test(' ' + e.className + ' ') && !(N && N.test(' ' + e.className + ' ')) && e.getBoundingClientRect().height >= 300).sort((a, b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height)[0];
        if (!d) return false; const t = [...d.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2) && e.getBoundingClientRect().width > 20).sort((a, b) => parseFloat(getComputedStyle(b).fontSize) - parseFloat(getComputedStyle(a).fontSize))[0];
        if (!t) return false; document.querySelectorAll('[data-tor="ziel"]').forEach(e => e.removeAttribute('data-tor')); t.setAttribute('data-tor', 'ziel'); return true; }, [CFG.dokument, CFG.dokumentNicht || '']).catch(() => false);
      if (!ok) return false; }
    else { let ok = await page.evaluate(S.finde, s).catch(() => false);
      if (!ok || !(await page.locator('[data-tor="ziel"]').first().isVisible().catch(() => false))) { if (await menueAuf()) { await warte(500); ok = await page.evaluate(S.finde, s).catch(() => false); } }   // Tor 3: Rand am Handy auch öffnen, wenn das Ziel bei geschlossenem Rand nicht gefunden wird (cu-messlauf 30.10.)
      if (!ok) return false; }
    const l = page.locator('[data-tor="ziel"]').first();
    try { await l.scrollIntoViewIfNeeded({ timeout: 2000 }); if (hand) await l.tap({ timeout: 3000 }); else await l.click({ timeout: 3000 }); }
    catch (e) { const ok = await page.evaluate(() => { const e = document.querySelector('[data-tor="ziel"]'); if (!e) return false; e.click(); return true; }).catch(() => false); if (!ok) return false; }
    await warte(650); await ruhe(); return true;
  };
  const ZT = process.env.TOR_ZEIT ? (...a) => console.log('  zeit', ((Date.now() - T0) / 1000).toFixed(1), ...a) : () => { }; let T0 = Date.now();
  const gehe = async weg => { T0 = Date.now(); await neuerKontext(); await lade(z.url); ZT('geladen'); for (const s of weg) { if (!(await schritt(s))) { ZT('schritt fehlt', s.text); return false; } ZT('schritt', (s.text || '').slice(0, 30)); } return true; };
  const sig = () => page.evaluate(S.signatur, OPT).catch(() => null);

  let nr = 0;
  const messe = async (zu) => {
    const y0 = await page.evaluate(() => scrollY).catch(() => 0);   // Lage des Zustands (z. B. Rundgang-Schritt weiter unten), für das Bild am Ort
    const hoch = await page.evaluate(() => document.documentElement.scrollHeight).catch(() => 0);
    for (let y = 0; y < Math.min(hoch, 14000); y += H * .8) { await page.evaluate(v => scrollTo(0, v), y).catch(() => { }); await warte(50); }
    await page.evaluate(() => scrollTo(0, 0)).catch(() => { }); await ruhe(); ZT('gescrollt', hoch);
    await page.evaluate(S.verdeckte).catch(() => 0); ZT('verdeckte');
    const m = await page.evaluate(messen).catch(e => [{ art: 'fehler', sel: '', text: '', info: String(e).slice(0, 120), r: { x: 0, y: 0, w: 1, h: 1 } }]);
    const e = await page.evaluate(S.ergaenzung, OPT).catch(e => ({ funde: [{ k: 0, art: 'fehler', info: String(e).slice(0, 120) }], doks: [], bilder: [] }));
    ZT('messen+ergaenzung'); const sy = await page.evaluate(() => scrollY).catch(() => 0);
    // Messlauf-Funde, die keine Fehler im Sinn der Kriterien sind: Kapselformen (Breite > 2 × Höhe) sind keine Rundknöpfe;
    // Kacheln eines bewusst gemischten Rasters (Grössen um mehr als 40 % verschieden) sind keine Reihe gleicher Karten
    const echt = f => { if (f.art === 'oval') { const g = f.info.match(/([\d.]+) × ([\d.]+)/); if (g && Math.max(+g[1], +g[2]) / Math.min(+g[1], +g[2]) > 2) return false; }
      if (f.art === 'reihe') { const h = f.info.match(/Höhe (\d+)–(\d+)/); if (h && +h[2] / +h[1] > 1.4) return false; } return true; };
    zu.funde = [...m.filter(echt).map(f => ({ k: KRIT[f.art] ?? 0, art: f.art, sel: f.sel, text: f.text, info: f.info, r: f.fest ? f.r : { ...f.r, y: f.r.y + sy } })), ...e.funde];
    zu.bild = `${zu.id}.jpg`;
    await page.screenshot({ path: path.join(BILDER, zu.bild), type: 'jpeg', quality: 70 }).catch(() => { zu.bild = null; });
    if (y0 > 40) { await page.evaluate(v => scrollTo(0, v), y0).catch(() => { }); await warte(900); zu.bildOrt = `${zu.id}-ort.jpg`;
      await page.screenshot({ path: path.join(BILDER, zu.bildOrt), type: 'jpeg', quality: 70 }).catch(() => { zu.bildOrt = null; }); await page.evaluate(() => scrollTo(0, 0)).catch(() => { }); }
    const ph = await page.evaluate(() => document.documentElement.scrollHeight).catch(() => H);
    const clip = (r, rand) => { const x = Math.max(0, r.x - rand), y = Math.max(0, r.y - rand); return { x, y, width: Math.min(W - x, r.w + 2 * rand), height: Math.min(ph - y, r.h + 2 * rand) }; };
    zu.doks = []; zu.kacheln = [];
    if (!STICH || true) {
      for (const [i, d] of e.doks.entries()) { if (d.r.h < 110 || d.r.w < 70 || d.r.x < 0 || d.r.x + d.r.w > W + 2) continue; const f = `${zu.id}-d${i}.png`; const c = clip(d.r, 0); if (c.width < 20 || c.height < 20) continue;
        await page.screenshot({ path: path.join(BILDER, f), clip: c, fullPage: true }).then(() => zu.doks.push({ datei: f, r: d.r, sel: d.sel })).catch(() => { }); }
      for (const [i, d] of e.bilder.entries()) { if (d.r.x < 0 || d.r.x + d.r.w > W + 2) continue; const f = `${zu.id}-k${i}.png`; const c = clip(d.r, 0); if (c.width < 20 || c.height < 20) continue;
        await page.screenshot({ path: path.join(BILDER, f), clip: c, fullPage: true }).then(() => zu.kacheln.push({ datei: f, r: d.r, sel: d.sel })).catch(() => { }); }
    }
    ZT('bilder', zu.doks.length, zu.kacheln.length); await page.evaluate(() => document.querySelectorAll('[data-messlauf-aus="verdeckt"]').forEach(e => e.removeAttribute('data-messlauf-aus'))).catch(() => { });
    await page.evaluate(() => scrollTo(0, 0)).catch(() => { });
  };

  const art = (k, vorher, nachher) => {
    if (!k) return 'start';
    if (k.ziel === 'dokklick') return 'editor-leiste';
    if (k.ziel === 'seite') return 'unterseite';
    if (nachher.dok.gross && !vorher.dok.gross) return 'dokument';
    if (nachher.fenster.length > vorher.fenster.length) return /neu|erstell|anleg|\+/i.test(k.text) ? 'neu-erstellen' : 'fenster';
    if (k.rolle === 'tab' || /reiter|tab/.test(k.gruppe)) return 'reiter';
    if (k.wo !== 'haupt') return 'navigation';
    return /neu|erstell|anleg/i.test(k.text) ? 'neu-erstellen' : 'ansicht';
  };

  // ---------- Stichprobe: Zustände des Inventars in anderer Grösse nachspielen ----------
  if (STICH) {
    const inv = JSON.parse(fs.readFileSync(path.join(ORDNER, 'inventar.json'), 'utf8')).zustaende;
    const wahl = inv.filter((x, i) => ['start', 'navigation', 'reiter', 'unterseite'].includes(x.art) || i % (+arg('jede', 5)) === 0).slice(0, +arg('stichmax', 70));
    const [ti, tn] = (arg('teil', '1/1')).split('/').map(Number);   // Stichprobe in Teilen parallel: --teil 2/4 nimmt jeden vierten Zustand ab dem zweiten
    const AB = +arg('ab', 0);   // Tor 3: ab dem N-ten Zustand weitermachen (nach Hänger)
    const OHNE = new Set((arg('ohne-ids', '') || '').split(',').filter(Boolean));   // Tor 3: Zustände, die nur über einen Inventar-Weg entstehen (Foto hinter offenem Fenster angeklickt)
    const NUR = new Set((arg('ids', '') || '').split(',').filter(Boolean));   // Tor 3: nur diese Zustände (Nachholen)
    const wahlT = (NUR.size ? inv.filter(x => NUR.has(x.id)) : wahl.filter((x, i) => i % tn === ti - 1 && !OHNE.has(x.id))).slice(AB);
    const DATEI = path.join(ORDNER, arg('datei') ? arg('datei') : AB ? `stich-${W}-ab${AB}.json` : (tn > 1 ? `stich-${W}-t${ti}.json` : `stich-${W}.json`));
    const sichere = () => fs.writeFileSync(DATEI, JSON.stringify({ zeit: new Date().toISOString(), browser: BROWSER, groesse: [W, H], zustaende: aus }, null, 1));   // Tor 3: nach jedem Zustand gespeichert
    const aus = [];
    for (const x of wahlT) {
      const zu = { id: x.id, name: x.name, art: x.art };
      if (x.art === 'erstbesuch' || !Array.isArray(x.weg)) { await neuerKontext(false); await lade(z.url); await messe(zu); aus.push(zu); log(`stich ${W}`, x.id, zu.funde.length, 'Funde'); continue; }   // erster Besuch ohne Vorwissen hat keinen Weg
      // Tor 3: Zeitgrenze je Zustand (2 min); hängt der Zustand, wird er als «haenger» vermerkt, der Kontext neu geöffnet und weitergemacht
      const GRENZE = +arg('grenze', 120) * 1000; let zeit;
      const erg = await Promise.race([(async () => { const ok = await gehe(x.weg); if (!ok) return 'ne'; await messe(zu); return 'ok'; })(), new Promise(r => { zeit = setTimeout(() => r('zeit'), GRENZE); })]);
      clearTimeout(zeit);
      if (erg === 'zeit') { zu.nichtErreicht = true; zu.haenger = true; aus.push(zu); log(`stich ${W}`, x.id, 'HÄNGT (Zeitgrenze), neuer Kontext'); sichere(); zuletzt = Date.now(); await neuerKontext(true).catch(() => { }); continue; }
      if (erg === 'ne') { zu.nichtErreicht = true; aus.push(zu); sichere(); continue; }
      aus.push(zu); log(`stich ${W}`, x.id, zu.funde.length, 'Funde'); sichere();
    }
    sichere();
    await browser.close(); return;
  }

  // ---------- Inventar: Zustände aus dem Werkzeug lesen ----------
  const zustaende = [], bekannt = new Map(), geklickt = new Set(), kanten = [], nichtErreicht = [];
  const neu = async (weg, k, vorher, s, tiefe) => {
    const id = String(++nr).padStart(3, '0');
    const name = k ? (vorher.name === 'Start' ? '' : vorher.name + ' → ') + (k.ziel === 'dokklick' ? 'Leiste am Dokument' : k.text.split(' ').slice(0, 7).join(' ')) : 'Start';
    const zu = { id, k: z.k, werkzeug: z.name, name, art: art(k, vorher || s, s), tiefe, weg, sig: s.sig, url: page.url(), titel: s.titel, aktiv: s.aktiv, fenster: s.fenster, dok: s.dok, inhalt: s.inhalt, steuer: k ? { text: k.text, wo: k.wo, gruppe: k.gruppe } : null };
    await messe(zu); bekannt.set(s.sig, zu); zustaende.push(zu);
    log(id, zu.art, name.slice(0, 70), '·', zu.funde.length, 'Funde');
    fs.writeFileSync(path.join(ORDNER, 'inventar.json'), JSON.stringify({ zeit: new Date().toISOString(), browser: BROWSER, groesse: [W, H], werkzeug: z, zustaende, kanten, nichtErreicht, fehler: fehler.slice(0, 50) }, null, 1));
    return zu;
  };

  await gehe([]); let s0 = await sig();
  for (let v = 0; v < 3 && (!s0 || !s0.titel.length); v++) { await warte(2500); await gehe([]); s0 = await sig(); }
  await neu([], null, null, s0, 0);
  // Begrüssung/Erstbesuch: Werkzeug ohne Vorwissen einmal als eigener Zustand
  if (z.localStorage && Object.keys(z.localStorage).length) {
    await neuerKontext(false); await lade(z.url); const s = await sig(); if (s && !bekannt.has(s.sig)) { const zu = await neu([], { text: 'Erster Besuch', wo: 'haupt', gruppe: '', ziel: 'erstbesuch' }, bekannt.get(s0.sig), s, 0); zu.art = 'erstbesuch'; zu.weg = null; } }

  const schlange = [bekannt.get(s0.sig)];
  // weitere Einstiege (z. B. ?rundgang): je ein Startzustand, der wie der Start weiter erkundet wird
  for (const u of z.startExtra || []) { const k = { ziel: 'seite', href: u, text: u.split('/').pop() || u, wo: 'haupt', gruppe: 'einstieg', key: 'einstieg|' + u };
    if (await gehe([k])) { const s = await sig(); if (s && !bekannt.has(s.sig)) schlange.push(await neu([k], k, bekannt.get(s0.sig), s, 1)); } }
  while (schlange.length && zustaende.length < MAX) {
    const x = schlange.shift(); if (x.tiefe >= TIEFE || !x.weg) continue;
    if (!(await gehe(x.weg))) { nichtErreicht.push({ id: x.id, name: x.name }); continue; }
    let hier = await sig(); if (!hier) continue;
    let kand = await page.evaluate(S.kandidaten, OPT).catch(() => []);
    for (let v = 0; v < 3 && !kand.length; v++) { await warte(2500); if (!(await gehe(x.weg))) break; hier = await sig() || hier; kand = await page.evaluate(S.kandidaten, OPT).catch(() => []); }
    // gleichartige Gruppen (z. B. 231 Fotos): erst drei; führt eine davon zu einem Dokument, alle
    const proGruppe = {}; const liste = [];
    for (const k of kand) { const key = k.gruppe + '|' + k.text + '|' + k.nr; const kette = x.weg.length && x.weg[x.weg.length - 1].key === key;
      if (geklickt.has(key) && !kette) continue; k.key = key;
      if (k.gruppenZahl > 8 && k.wo === 'haupt') { proGruppe[k.gruppe] = (proGruppe[k.gruppe] || 0) + 1; if (proGruppe[k.gruppe] > 3) { (x.rest = x.rest || {})[k.gruppe] = (x.rest[k.gruppe] || []).concat([k]); continue; } }
      liste.push(k); }
    const dokGruppen = new Set();
    const bediene = async k => {
      geklickt.add(k.key);
      const vorUrl = page.url();
      if (!(await schritt(k))) return;
      const s = await sig(); if (!s) return;
      kanten.push({ von: x.id, text: k.text, wo: k.wo, gruppe: k.gruppe, nach: s.sig });
      if (s.sig !== hier.sig) {
        if (!bekannt.has(s.sig) && zustaende.length < MAX) { const zu = await neu([...x.weg, { ...k, key: k.key }], k, x, s, x.tiefe + 1); schlange.push(zu); if (s.dok.gross) dokGruppen.add(k.gruppe); }
        else if (bekannt.has(s.sig) && s.dok.gross) dokGruppen.add(k.gruppe);
        if (!(await gehe(x.weg))) return 'weg'; hier = await sig() || hier;
      } else if (page.url() !== vorUrl) { if (!(await gehe(x.weg))) return 'weg'; }
    };
    for (const k of liste) { if (zustaende.length >= MAX) break; if ((await bediene(k)) === 'weg') break; }
    for (const [g, rest] of Object.entries(x.rest || {})) {
      if (dokGruppen.has(g) || /vorlage|stueck|dok|doc|medium|karte|plakat|brief|mail/i.test(g)) { for (const k of rest) { if (zustaende.length >= MAX) break; if ((await bediene(k)) === 'weg') break; } }
      else x.gleichartig = (x.gleichartig || []).concat([{ gruppe: g, zahl: rest.length + 3 }]);
    }
    // Editor: hohes und queres Dokument einmal mit offener Leiste (Klick auf die grösste Schrift im Dokument)
    if (hier.dok.gross && !x.leisteProbe) { const lage = hier.dok.lage[0]; const schon = zustaende.filter(q => q.art === 'editor-leiste' && q.dok.lage[0] === lage).length;
      if (schon < 2) { x.leisteProbe = true; const k = { ziel: 'dokklick', key: 'dok|' + x.id, text: 'Leiste am Dokument', wo: 'haupt', gruppe: 'dok' }; if (await schritt(k)) { const s = await sig(); if (s && s.sig !== hier.sig && !bekannt.has(s.sig)) await neu([...x.weg, k], k, x, s, x.tiefe + 1); } } }
  }
  log('Inventar fertig:', zustaende.length, 'Zustände', nichtErreicht.length ? `(${nichtErreicht.length} nicht erreicht)` : '');
  fs.writeFileSync(path.join(ORDNER, 'inventar.json'), JSON.stringify({ zeit: new Date().toISOString(), browser: BROWSER, groesse: [W, H], werkzeug: z, zustaende, kanten, nichtErreicht, fehler: fehler.slice(0, 50), voll: zustaende.length < MAX }, null, 1));
  await browser.close();
})();
