#!/usr/bin/env node
// Messlauf: öffnet in jedem Werkzeug jede Ansicht (Navigation, Reiter, Menüs, «Neu», Dialoge, Rundgang) und misst
// Text-Überlauf, Text am Rand, abgeschnittene Wörter, ovale Knöpfe, ungleiche Kachelreihen, Überschneidungen, Anschnitt.
// Aufruf: node messlauf.js <ziele.json> <ausgabe-ordner> [--nur k1,k2] [--browser chromium|webkit] [--groesse 1440,390]
const path = require('path'), fs = require('fs');
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const messen = require('./messen.js');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const [ZIELE, AUS] = process.argv.slice(2);
let ziele = JSON.parse(fs.readFileSync(ZIELE, 'utf8'));
if (arg('nur')) ziele = ziele.filter(z => arg('nur').split(',').includes(z.k));
const BROWSER = (arg('browser', 'chromium,webkit')).split(',');
const GROESSEN = [[1440, 900], [1280, 800], [1000, 650], [390, 844]].filter(([w]) => (arg('groesse', '1440,1280,390')).split(',').includes(String(w)));
fs.mkdirSync(path.join(AUS, 'bilder'), { recursive: true });
const GEFAHR = /l[öo]schen|entfern|senden|abschick|ver[öo]ffentlich|hochlad|online stellen|abmeld|zur[üu]cksetz|leeren|drucken|herunterlad|download|speicher|[üu]bernehm|best[äa]tig|freigeb|bezahl|verwerf|archivier|abmelden|logout|ausloggen|ki fragen|erzeugen|generier|neu laden/i;
const NEBEN = /neu|erstell|anleg|bearbeit|[äa]nder|[öo]ffn|ansehen|vorschau|mehr|details|men[üu]|optionen|w[äa]hl|filter|sortier|hinzuf|einf[üu]g|ausklapp|zeig|vergleich|fassung|liste|karte|tag|woche|monat|seite|editor|leiste|einstellung/i;
const warte = ms => new Promise(r => setTimeout(r, ms));

// Kandidaten in der Seite markieren (data-ml) und beschreiben
const sammle = (art) => {
  const sicht = e => { const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false; for (let x = e; x; x = x.parentElement) { const c = getComputedStyle(x); if (c.display === 'none' || c.visibility === 'hidden') return false; } return true; };
  const pfad = e => { const p = []; for (let x = e; x && x !== document.body && p.length < 3; x = x.parentElement) { let t = x.tagName.toLowerCase(); if (x.id) { p.unshift(t + '#' + x.id); break; } const k = typeof x.className === 'string' ? x.className.trim().split(/\s+/).filter(c => !/^(an|aktiv|offen|ist-)/.test(c)).slice(0, 2) : []; if (k.length) t += '.' + k.join('.'); p.unshift(t); } return p.join('>'); };
  const t = e => (e.innerText || e.getAttribute('aria-label') || e.title || '').trim().replace(/\s+/g, ' ').slice(0, 50);
  const selbeSeite = a => { if (!a.matches('a[href]')) return true; const h = a.getAttribute('href'); if (/^(mailto|tel|javascript):/.test(h)) return false; if (a.target === '_blank') return false; if (h.startsWith('#') || h.startsWith('?')) return true; try { const u = new URL(a.href); return u.origin === location.origin && u.pathname === location.pathname; } catch (e) { return false; } };
  let el;
  if (art === 'nav') el = [...document.querySelectorAll('aside button,aside a[href],aside [data-gehe],nav button,nav a[href],[role=tablist] [role=tab],[class*="rand"] button,[class*="rand"] [data-gehe],[class*="reiter"] button,[class*="leiste"] button,header button,[data-ansicht],[data-gehe],[data-zeige]')];
  else el = [...document.querySelectorAll('button,[role=tab],[role=button],summary,[aria-haspopup],[aria-expanded],a[href^="#"],a[href^="?"],[data-gehe],[data-zeige],[data-oeffne],select')].filter(e => sicht(e));
  el = [...new Set(el)].filter(selbeSeite);
  return el.map((e, i) => { e.setAttribute('data-ml', art + i); return { id: art + i, key: pfad(e) + '|' + t(e), text: t(e), sicht: sicht(e), echteNav: !!e.closest('aside,nav,[role=tablist],[class*="rand"],[class*="reiter"]') && !e.closest('main,article') && !(e.matches('[aria-pressed]') && e.closest('[role=group]')), toggle: e.matches('[aria-expanded],[aria-haspopup],summary') || /men[üu]|navigation|☰/i.test(t(e) + ' ' + (e.className || '')), tab: e.matches('[role=tab]') }; });
};
// Inhalt einer Ansicht: Überschriften, Kacheln, Bilder im Hauptbereich (ohne Kopf, Rand, Fuss)
const signatur = () => {
  const sicht = e => { const r = e.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return false; for (let x = e; x; x = x.parentElement) { const c = getComputedStyle(x); if (c.display === 'none' || c.visibility === 'hidden') return false; } return !(e.closest('details:not([open])') && !e.closest('summary')); };
  const raus = e => e.closest('header,aside,nav,footer,[class*="rand"],[class*="kopf"],[class*="leiste"],.rdg-karte,[role=dialog]');
  const t = [...document.querySelectorAll('h1,h2,h3,h4,figcaption,[class*="titel"],[class*="__t"],button,a')].filter(e => sicht(e) && !raus(e)).map(e => (e.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 60)).filter(Boolean);
  const bilder = [...document.querySelectorAll('img,[style*="background-image"]')].filter(e => sicht(e) && !raus(e)).map(e => { const u = e.currentSrc || e.src || (e.style.backgroundImage.match(/url\(["']?([^"')]+)/) || [])[1] || ''; return { u: u.split('?')[0].replace(/-(\d+)(\.\w+)$/, '$2'), alt: (e.alt || '').slice(0, 60) }; });
  const h = [...document.querySelectorAll('main h1, main h2, h1, h2')].find(e => sicht(e) && !raus(e));
  return { titel: h ? h.innerText.trim().slice(0, 60) : '', t: [...new Set(t)], bilder };
};
const offeneDialoge = () => [...document.querySelectorAll('dialog[open],[role=dialog],[aria-modal="true"],[class*="fenster"],[class*="dialog"],[class*="modal"],[class*="schublade"],[class*="leiste--offen"]')].filter(e => { const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return r.width > 40 && r.height > 40 && c.display !== 'none' && c.visibility !== 'hidden' && +c.opacity > 0.1; }).length;

(async () => {
  const funde = []; const zustaende = []; const bilderGesehen = new Set();
  for (const bn of BROWSER) {
    const browser = await pw[bn].launch({ headless: true });
    for (const [W, H] of GROESSEN) {
      const hand = W < 700;
      for (const z of ziele) {
        const ctx = await browser.newContext({ viewport: { width: W, height: H }, locale: 'de-DE', timezoneId: 'Europe/Berlin', hasTouch: hand, isMobile: hand && bn === 'chromium', acceptDownloads: false });
        if (process.env.TOR_UHR) await ctx.clock.setFixedTime(new Date(process.env.TOR_UHR)).catch(() => { });
        await ctx.route('**/*', r => { const q = r.request(); const u = q.url();
          if (/^(mailto|tel):/.test(u)) return r.abort();
          if (q.method() !== 'GET' && q.method() !== 'HEAD') return r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true,"messlauf":true}' });
          return r.continue(); });
        const page = await ctx.newPage(); page.setDefaultTimeout(8000);
        const LAUT = process.env.ML_LAUT; const t0 = Date.now(); const log = m => LAUT && console.log(`  ${((Date.now() - t0) / 1000).toFixed(1)}s ${m}`);
        ctx.on('page', p => { if (p !== page) p.close().catch(() => {}); });
        page.on('dialog', d => d.dismiss().catch(() => {}));
        const wo = `${bn} ${W}`;
        const lade = async (url) => { await page.goto(url || z.url, { waitUntil: 'load', timeout: 30000 }).catch(() => {}); await warte(z.warte || 1800); };
        const ruhe = async () => { await page.evaluate(async () => { const t0 = Date.now();
            while (Date.now() - t0 < 1500) { const a = document.getAnimations().filter(x => x.playState === 'running' && x.effect && x.effect.getTiming().iterations !== Infinity); if (!a.length) break; await new Promise(r => setTimeout(r, 120)); } }).catch(() => {}); await warte(150); };
        const zustand = async (name) => { log('Zustand ' + name);
          // Seite einmal durchrollen, damit eingeblendete Inhalte stehen, Bewegung abwarten, dann die ganze Seite messen
          // die Höhe bei jedem Schritt neu lesen: nachgeladene Bilder machen die Seite länger (30.10.2026, Titel unten in der Gästebuch-Anleitung standen noch nicht)
          const hoch = () => page.evaluate(() => document.documentElement.scrollHeight).catch(() => 0);
          for (let y = 0; y < Math.min(await hoch(), 15000); y += H * 0.8) { await page.evaluate(v => scrollTo(0, v), y).catch(() => {}); await warte(60); }
          await page.evaluate(() => scrollTo(0, 0)).catch(() => {}); await ruhe();
          log('  messen');
          const f = await Promise.race([page.evaluate(messen), warte(20000).then(() => [{ art: 'fehler', sel: '', text: '', info: 'Messung über 20 s', r: { x: 0, y: 0, w: 1, h: 1 } }])]).catch(e => [{ art: 'fehler', sel: '', text: '', info: String(e).slice(0, 120), r: { x: 0, y: 0, w: 1, h: 1 } }]);
          zustaende.push({ wo, k: z.k, name, zahl: f.length });
          for (const x of f) {
            const key = [z.k, wo, x.art, x.sel, x.text, x.info.replace(/[\d.]+/g, '#')].join('¦');
            const alt = funde.find(g => g.key === key); if (alt) { if (!alt.zustaende.includes(name)) alt.zustaende.push(name); continue; }
            const bild = `${z.k}-${bn}-${W}-${funde.length}.jpg`;
            const eintrag = { key, k: z.k, name: z.name, browser: bn, breite: W, art: x.art, sel: x.sel, text: x.text, info: x.info, zustand: name, zustaende: [name], url: page.url(), bild: null };
            funde.push(eintrag);
            // Ausschnittbild: zur Stelle rollen, Rahmen setzen, Ausschnitt
            try { // die markierten Elemente ins Bild holen und ihre Fläche jetzt messen
              const idx = f.indexOf(x); const r = await page.evaluate(i => { const els = [...document.querySelectorAll(`[data-ml-f~="f${i}"]`)]; if (!els.length) return null;
                  els[0].scrollIntoView({ block: 'center', inline: 'nearest' }); const rs = els.map(e => e.getBoundingClientRect()).filter(q => q.width > 0);
                  if (!rs.length) return null; const l = Math.min(...rs.map(q => q.left)), t = Math.min(...rs.map(q => q.top)), rr = Math.max(...rs.map(q => q.right)), b = Math.max(...rs.map(q => q.bottom));
                  return { x: Math.round(l), y: Math.round(t), w: Math.round(rr - l), h: Math.round(b - t) }; }, idx).catch(() => null) || x.r;
              await ruhe(); const pad = 28;
              const clip = { x: Math.max(0, r.x - pad), y: Math.max(0, r.y - pad) }; clip.width = Math.min(W - clip.x, r.w + 2 * pad); clip.height = Math.min(H - clip.y, Math.max(r.h + 2 * pad, 40));
              if (clip.width > 10 && clip.height > 10 && r.y < H && r.y + r.h > 0) {
                await page.evaluate(r => { const d = document.createElement('div'); d.className = 'ml-rahmen'; d.style.cssText = `position:fixed;left:${r.x - 3}px;top:${r.y - 3}px;width:${r.w + 6}px;height:${r.h + 6}px;outline:2px solid #ff1f5a;outline-offset:0;z-index:2147483647;pointer-events:none;border-radius:4px`; document.body.appendChild(d); }, r);
                await page.screenshot({ path: path.join(AUS, 'bilder', bild), clip, type: 'jpeg', quality: 80 }); eintrag.bild = bild;
                await page.evaluate(() => document.querySelectorAll('.ml-rahmen').forEach(d => d.remove()));
              } } catch (e) { }
          }
          await page.evaluate(() => scrollTo(0, 0)).catch(() => {});
        };
        const klick = async (id) => { const l = page.locator(`[data-ml="${id}"]`).first();
          try { await l.scrollIntoViewIfNeeded({ timeout: 2000 }); if (hand) await l.tap({ timeout: 3000 }); else await l.click({ timeout: 3000 }); await warte(700); return true; } catch (e) { return false; } };
        const schliessen = async () => { for (let i = 0; i < 3; i++) { if (!(await page.evaluate(offeneDialoge).catch(() => 0))) return; await page.keyboard.press('Escape').catch(() => {}); await warte(300);
            const zu = page.locator('dialog[open] button:is([aria-label*="chlie"],[aria-label*="Zu"],[class*="zu"]), [role=dialog] button:is([aria-label*="chlie"],[class*="zu"]), button:has-text("Schliessen"), button:has-text("Schließen"), button:has-text("Abbrechen"), button:has-text("×")').first();
            if (await zu.count()) await zu.click({ timeout: 1500 }).catch(() => {}); await warte(300); } };
        const nebenRunde = async (name, tiefe) => {
          const ks = (await page.evaluate(sammle, 'neben').catch(() => [])).filter(k => k.sicht && k.text && !GEFAHR.test(k.text) && (k.tab || k.toggle || NEBEN.test(k.text)));
          const start = page.url(); let n = 0;
          for (const k of ks.filter(k => !nebenGesehen.has(k.key)).slice(0, z.neben ?? 8)) {
            nebenGesehen.add(k.key);
            if (!(await page.locator(`[data-ml="${k.id}"]`).count())) continue;
            if (!(await klick(k.id))) continue; n++;
            if (page.url().split('#')[0].split('?')[0] !== start.split('#')[0].split('?')[0]) { await zustand(`${name} → ${k.text}`); await lade(start); await page.evaluate(sammle, 'neben').catch(() => {}); continue; }
            await zustand(`${name} → ${k.text}`);
            await schliessen();
            if (k.toggle) { await klick(k.id); }
          }
          return n;
        };
        const navSig = []; let navLinks = []; let menuGesehen = false; const nebenGesehen = new Set();
        try {
          // Start
          await lade(); await zustand('Start');
          await nebenRunde('Start', 1);
          // jeder Navigationspunkt (frisch geladen)
          await lade(); const nav = (await page.evaluate(sammle, 'nav')).filter(k => k.text && !GEFAHR.test(k.text) && !/rundgang|anleitung|hilfe/i.test(k.text));
          navLinks = await page.evaluate(() => [...document.querySelectorAll('aside a[href],nav a[href],[class*="rand"] a[href]')].filter(a => !/^(#|\?|mailto|tel|javascript)/.test(a.getAttribute('href'))).map(a => ({ text: (a.innerText || a.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 50), href: a.href.split('#')[0] === location.href.split('#')[0] ? '' : a.href, key: (a.className || '') + ' ' + (a.closest('[class]') || {}).className })).filter(x => x.text)).catch(() => []);
          const gemacht = new Set();
          for (const k of nav.slice(0, z.nav ?? 40)) {
            if (gemacht.has(k.key)) continue; gemacht.add(k.key);
            // ohne Neuladen weiterklicken (die Werkzeuge wechseln Ansichten in der Seite); nur wenn der Punkt fehlt oder die Seite gewechselt hat, neu laden
            let neu = await page.evaluate(sammle, 'nav').catch(() => []); let m = neu.find(x => x.key === k.key);
            if (!m || page.url().split(/[?#]/)[0] !== z.url.split(/[?#]/)[0]) { await lade(); neu = await page.evaluate(sammle, 'nav'); m = neu.find(x => x.key === k.key); }
            if (!m) continue;
            await schliessen();
            if (!m.sicht) { // Menü öffnen (Handy); am Bildschirm verborgene Punkte gehören zu anderen Ansichten
              if (!hand) continue;
              const t = neu.find(x => x.toggle && x.sicht); if (t) { await klick(t.id); if (!menuGesehen) { menuGesehen = true; await zustand('Menü offen'); } } }
            const vorSig = await page.evaluate(signatur).catch(() => null);
            if (!(await klick(m.id))) continue;
            await zustand(k.text);
            const sig = await page.evaluate(signatur).catch(() => null);
            // nur echte Ansichtswechsel vergleichen: Sprungmarken und das Zeichen oben (führt zur Übersicht) ändern den Inhalt nicht
            const gleichWieVorher = vorSig && sig && JSON.stringify([vorSig.t, vorSig.bilder]) === JSON.stringify([sig.t, sig.bilder]);
            if (sig && !gleichWieVorher && m.echteNav && !m.toggle && !/marke|logo/i.test(k.key)) navSig.push({ name: k.text, url: page.url(), ...sig });
            await nebenRunde(k.text, 1);
          }
          // Rundgang
          if (z.rundgang !== false) {
            await lade(z.url + (z.url.includes('?') ? '&' : '?') + 'rundgang'); let schritt = 0;
            for (; schritt < 16; schritt++) {
              await zustand(`Rundgang ${schritt + 1}`);
              let w = page.locator('.rdg-los:visible').first();
              if (!(await w.count())) w = page.locator('button:visible').filter({ hasText: /weiter|n[äa]chst|›|→|los|verstanden|fertig/i }).first();
              if (!(await w.count())) break; await w.click({ timeout: 2500 }).catch(() => {}); await warte(800);
            }
          }
          // zusätzliche Wege (z. B. Editor mit offener Leiste)
          for (const x of z.extra || []) { await lade(x.url || z.url); for (const s of x.klicks || []) { await page.locator(s).first().click({ timeout: 4000 }).catch(() => {}); await warte(900); } await zustand(x.name); }
        } catch (e) { funde.push({ k: z.k, name: z.name, browser: bn, breite: W, art: 'fehler', sel: '', text: '', info: 'Lauf abgebrochen: ' + String(e).slice(0, 160), zustand: '', zustaende: [] }); }
        // Navigationslinks mit verschiedenen Namen auf dieselbe Adresse
        { const ziel = new Map(); for (const k of navLinks) { if (!k.href || /marke|logo/i.test(k.key)) continue; const l = ziel.get(k.href) || []; if (!l.includes(k.text)) l.push(k.text); ziel.set(k.href, l); }
          for (const [h, l] of ziel) if (l.length > 1) funde.push({ key: [z.k, wo, 'doppelt', h].join('¦'), k: z.k, name: z.name, browser: bn, breite: W, art: 'doppelt', sel: 'Navigation', text: l.map(t => `«${t}»`).join(' und '), info: `führen auf dieselbe Adresse ${h}`, zustand: 'Start', zustaende: ['Start'], url: z.url, bild: null }); }
        // doppelte Navigationspunkte und gemischte Inhalte
        const menge = x => new Set([...x.t, ...x.bilder.map(b => 'B:' + b.u)]);
        for (let i = 0; i < navSig.length; i++) for (let j = i + 1; j < navSig.length; j++) {
          const a = menge(navSig[i]), b = menge(navSig[j]); if (a.size < 3 || b.size < 3) continue;
          const gem = [...a].filter(x => b.has(x)).length, jac = gem / (a.size + b.size - gem);
          if (navSig[i].name === navSig[j].name) continue;
          if (jac >= 0.8) funde.push({ key: [z.k, wo, 'doppelt', navSig[i].name, navSig[j].name].join('¦'), k: z.k, name: z.name, browser: bn, breite: W, art: 'doppelt', sel: 'Navigation', text: `«${navSig[i].name}» und «${navSig[j].name}»`, info: `zeigen im Wesentlichen dasselbe (${Math.round(jac * 100)} % gleiche Titel/Kacheln/Bilder, Titel «${navSig[i].titel}» / «${navSig[j].titel}»)`, zustand: navSig[i].name, zustaende: [navSig[i].name, navSig[j].name], url: navSig[i].url, bild: null });
        }
        for (const x of navSig) {
          const plakat = x.bilder.filter(b => /plakat|poster/i.test(b.u + ' ' + b.alt)).length, foto = x.bilder.filter(b => !/plakat|poster|logo|zeichen|marke|icon|\.svg/i.test(b.u + ' ' + b.alt)).length;
          if ((/foto|bild/i.test(x.name) && plakat > 0 && !/plakat/i.test(x.name)) || (/plakat/i.test(x.name) && foto > 2 && plakat > 0 && !/foto|bild/i.test(x.name)))
            funde.push({ key: [z.k, wo, 'gemischt', x.name].join('¦'), k: z.k, name: z.name, browser: bn, breite: W, art: 'gemischt', sel: 'Navigation', text: `«${x.name}»`, info: `zeigt ${plakat} Plakate und ${foto} Fotos gemischt`, zustand: x.name, zustaende: [x.name], url: x.url, bild: null });
        }
        await ctx.close();
        console.log(`${wo} ${z.k}: ${funde.filter(f => f.k === z.k && f.browser === bn && f.breite === W).length} Funde, ${zustaende.filter(s => s.k === z.k && s.wo === wo).length} Zustände`);
        fs.writeFileSync(path.join(AUS, 'funde.json'), JSON.stringify({ zeit: new Date().toISOString(), funde, zustaende }, null, 1));
      }
    }
    await browser.close();
  }
  console.log('FERTIG', funde.length, 'Funde');
})();
