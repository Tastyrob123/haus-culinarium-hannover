#!/usr/bin/env node
// Abnahme-Tor · Dokumente der Plakatwerkstatt. Setzt jedes Dokument mit der Satz-Maschine des Werkzeugs selbst (DS.setze/DS.seiteDom),
// so wie die Werkstatt es zeigt, und prüft jedes Blatt: am Modell in mm gegen stilblatt.json, im gerenderten Blatt (Zeilen, Schrift),
// und mit der eigenen Druckprüfung des Werkzeugs (DS.pruefe). Bild je Blatt für Bildprüfung (Löcher) und Augenprüfung.
// Quellen, alle aus dem Werkzeug gelesen:
//   Vorlagen     haeuser/<haus>/vorlagen/index.json → jede Art, jede Vorlage
//   Arten        «Neu erstellen» / «Arten und Vorlagen»: jede Art × jeder ihrer Aufbauten × jedes ihrer Formate (ARTEN, INHALT in start.js)
//   Entwerfen    die Beispiel-Aufträge des Editors, beantwortet von der Probe-Antwort des Servers (entwerfen.json, siehe README)
//   Muster       Reiter «Vorlagen» im Editor: jeder Aufbau × jedes Format × jeder Grund aus den Auswahlfeldern
//   Vorschläge   «Abend beschreiben»: DSPlakat.plakatDoc je Motiv der Sammlung, in den Formaten der Vorschläge
// Aufruf: node dok-tor.js <werkstatt-url> <ausgabe-ordner> [--browser webkit] [--nur vorlagen,entwerfen,muster,vorschlaege]
const path = require('path'), fs = require('fs');
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const [URL, AUS] = process.argv.slice(2);
const NUR = arg('nur', 'vorlagen,arten,entwerfen,muster,vorschlaege').split(',');
const BILDER = path.join(AUS, 'blatt'); fs.mkdirSync(BILDER, { recursive: true });
const PX = 1100;   // längste Seite eines Blatts in px

// läuft im Browser: ein Dokument setzen, zeigen, prüfen
function pruefeDok(a) {
  const { spec, STIL, PX } = a, M = DS.M, B = DS.B;
  const doc = spec.doc || DS.dokument(M, { name: spec.titel, format: spec.format, seiten: spec.seiten });
  const fk = doc.formatKey, f = doc.format, u = Math.min(f.b, f.h);
  const S = PX / Math.max(f.b + 2 * B, f.h + 2 * B);
  let wirt = document.getElementById('tor-wirt');
  if (!wirt) { wirt = document.createElement('div'); wirt.id = 'tor-wirt'; wirt.style.cssText = 'position:fixed;left:0;top:0;z-index:2147483647;background:#808080;padding:20px;display:flex;gap:20px;align-items:flex-start'; document.body.appendChild(wirt); }
  wirt.innerHTML = '';
  const F = [];
  const fund = (k, art, info, seite, el) => F.push({ k, art, info, seite, r: el ? { x: (el.x + B) * S, y: (el.y + B) * S, w: (el.w || 0) * S, h: (el.h || DS.elHoehe(M, el) || 0) * S } : null, text: el && el.text ? el.text.replace(/\s+/g, ' ').slice(0, 60) : '' });
  const R = STIL.rollen, ERLAUBT = new Set(Object.values(R).flatMap(r => r.rolle));
  const SCHRIFT = { titel: /fraunces(?!.*zeile)/i, kapitale: /zeile/i, text: /instrument/i, kursiv: /instrument/i, mono: /dm ?mono/i, plakat: /urbanist/i, plakatfett: /urbanist/i };
  // Mindestgrade nach Zweck: ein Aufbau aus mindestgrade_zweck wird wie das dort genannte Format gemessen (Menükarte am Platz wie DL, in jedem Format)
  const mindFuer = aufbau => { for (const z of Object.values(STIL.mindestgrade_zweck || {})) if ((z.aufbau || []).includes(aufbau)) return (STIL.mindestgrade_mm || {})[z.wie]; return (STIL.mindestgrade_mm || {})[fk]; };
  const kat = r => ({ titel: 'titel', kapitale: 'titel', kopf: 'titel', text: 'text', kursiv: 'text', mono: 'etikett', plakat: 'etikett', plakatfett: 'titel' })[r];
  const hex = c => { if (!c) return null; if (c[0] === '#') return c.toLowerCase(); const w = STIL.farben.werte[c]; return w ? w.toLowerCase() : null; };
  const PALETTE = new Set(Object.values(STIL.farben.werte).map(x => x.toLowerCase()));
  const ZIER = new RegExp('(^|\\s)(' + STIL.schmuck.zierzeichen_verboten.map(z => z.replace(/[*.]/g, '\\$&')).join('|') + ')(\\s|$)');
  // Kriterium 24 «zier-x» (Robert 29.10.2026, Regel wie messen.js): kein x/× als Zier- oder Trennzeichen. Erlaubt: Namen (Momo x Rudi, MOMO X RUDI X GAST),
  // Masse zwischen Zahlen (148 × 210). Fund: allein stehendes x, x zwischen zwei Wörtern, die übrigen Zierzeichen des Stilblatts.
  const zierX = t => { let r = String(t).replace(/\bmomo(\s*[x×]\s*[\p{L}][\p{L}'’.-]*)+/giu, 'NAME').replace(/\d\s*[x×]\s*\d/g, 'MASS');
    if (/(^|\s)[x×](\s|$)/i.test(r)) return 'x als Zier- oder Trennzeichen';
    if (ZIER.test(r)) return 'Zierzeichen im Text'; return null; };
  const BILDAUFBAU = /^(plakat|plakathoch|plakatganz|plakatrueck|buehne|ansicht)$/;
  const seitenInfo = [];
  doc.seiten.forEach((s, i) => {
    const sp = (spec.seiten && spec.seiten[i]) || {}; const aufbau = sp.vorlage || s.quelle || ''; const ton = sp.ton || '';
    const blatt = DS.seiteDom(M, doc, i, S, {}); blatt.dataset.tor = 'blatt' + i; wirt.appendChild(blatt);
    const MIND = mindFuer(aufbau);
    const kinder = [...blatt.children];
    const els = s.el.map((el, j) => Object.assign({}, el, { h: el.h || (el.typ === 'text' || el.typ === 'zeichen' ? DS.elHoehe(M, el) : el.h), dom: kinder[j] }));
    const texte = els.filter(e => e.typ === 'text' && (e.text || '').trim());
    // ---- K12 Stil laut stilblatt.json
    for (const e of texte) {
      if (!ERLAUBT.has(e.rolle)) fund(12, 'rolle', `Rolle «${e.rolle}» gibt es im Stilblatt nicht`, i, e);
      for (const r of Object.values(R)) if (r.nur_bei && r.rolle.includes(e.rolle) && !r.nur_bei.includes(aufbau)) fund(12, 'rolle', `Rolle «${e.rolle}» (${r.schrift}) nur bei ${r.nur_bei.join('/')}, hier Aufbau «${aufbau}»`, i, e);
      const cs = e.dom ? getComputedStyle(e.dom.querySelector('*') || e.dom) : null;
      const fam = cs ? cs.fontFamily.split(',')[0].replace(/["']/g, '').trim() : ''; if (cs && ERLAUBT.has(e.rolle) && fam !== 'DS-' + e.rolle) fund(12, 'schrift', `Rolle «${e.rolle}» gesetzt in ${fam} statt in der Schrift der Rolle`, i, e);
      if (cs && /italic|oblique/.test(cs.fontStyle) && R.text.kursiv === false && /text|kursiv/.test(e.rolle)) fund(12, 'kursiv', 'Kursiv, das Haus setzt Text nicht kursiv', i, e);
      const gross = e.gross || (cs && cs.textTransform === 'uppercase') || (e.text === e.text.toUpperCase() && /[A-ZÄÖÜ]{3}/.test(e.text));
      if (STIL.verboten.versalien_in_rolle.includes(e.rolle) && gross) fund(12, 'versalien', `Versalien in der Rolle «${e.rolle}»`, i, e);
      const smax = e.rolle === 'kapitale' ? (R.rudis_zeile.sperr_max || .08) : STIL.verboten.sperr_max;
      if ((e.sperr || 0) > smax + 1e-6) fund(12, 'sperrung', `Sperrung ${e.sperr} em über ${smax}`, i, e);
      if (aufbau === 'menue' && e.rolle === 'titel' && /\S\s*\/\s*\S/.test(e.text)) fund(12, 'trenner', `Trenner «/» in der Menükarte, das Haus trennt mit «|»`, i, e);
      if (e.rolle === 'kapitale' && /\s\|\s/.test(e.text)) fund(12, 'trenner', `Trenner «|» in Rudis Zeile, dort «/»`, i, e);
      if (/\S\s*\|\s*$/m.test(e.text) || /^\s*\|/m.test(e.text)) fund(12, 'trenner', 'Trenner am Zeilenende oder -anfang', i, e);
      // Farben je Grund
      if (STIL.farben[ton] && !BILDAUFBAU.test(aufbau)) { const k = kat(e.rolle), erl = STIL.farben[ton][k] || []; const c = hex(e.farbe), akz = erl.includes('akzent');
        const ok = !c || erl.some(n => hex(n) === c) || (akz && !PALETTE.has(c)) || (akz && c === hex('messing'));
        if (!ok) fund(12, 'farbe', `Farbe ${e.farbe} für ${k} auf Grund «${ton}» (erlaubt: ${erl.join(', ')})`, i, e); }
      // Mindestgrade
      // Zierzeichen, Arbeitsstand, Platzhalter
      const zx = zierX(e.text); if (zx) fund(24, 'zierzeichen', `${zx}: «${e.text.replace(/\s+/g, ' ').slice(0, 40)}»`, i, e);
      if (/gew[äa]hlt:|offen:|\bprobe\b|todo|lorem|xxx|\bfassung [a-z]\b/i.test(e.text)) fund(23, 'arbeitsstand', `Arbeitsstand sichtbar: «${e.text.replace(/\s+/g, ' ').slice(0, 40)}»`, i, e);
      if (/(\S…|…\s|\s…$)/.test(e.text) && !/^…/.test(e.text.trim())) fund(23, 'unvollstaendig', `Unvollständiger Text mit «…»: «${e.text.replace(/\s+/g, ' ').slice(0, 50)}»`, i, e);
      if (/\b(undefined|null|NaN)\b|\[object /.test(e.text)) fund(23, 'programmtext', `Programmtext auf dem Blatt: «${e.text.replace(/\s+/g, ' ').slice(0, 40)}»`, i, e);
      if (/\[[^\]]*\]/.test(e.text)) fund(14, 'platzhalter', `Platzhalter sichtbar: ${e.text.match(/\[[^\]]*\]/g).slice(0, 3).join(' ')}`, i, e);
    }
    if (MIND) {
      const titel = texte.filter(e => /^(titel|kapitale|plakatfett|kopf)$/.test(e.rolle)).sort((a, b) => b.gr - a.gr)[0];
      if (titel && MIND.titel && !BILDAUFBAU.test(aufbau) && titel.gr < MIND.titel - .05) fund(8, 'grad', `Haupttitel ${titel.gr.toFixed(1)} mm, Mindestgrad ${MIND.titel} mm (Format ${fk}, Aufbau ${aufbau})`, i, titel);
      for (const [k, rollen] of [['text', /^(text|kursiv)$/], ['etikett', /^(mono|plakat)$/]]) { const zu = texte.filter(e => rollen.test(e.rolle) && MIND[k] && e.gr < MIND[k] - .05);
        if (zu.length) { const kl = zu.sort((a, b) => a.gr - b.gr)[0]; fund(8, 'grad', `${zu.length} ${k === 'text' ? 'Textzeilen' : 'Etiketten'} unter dem Mindestgrad ${MIND[k]} mm (kleinste ${kl.gr.toFixed(2)} mm), Format ${fk}, Aufbau ${aufbau}`, i, kl); } }
    }
    // ---- Linien zwischen Posten: nur Luft oder kurzer feiner Strich (6–8 mm), keine groben Linien
    if (!BILDAUFBAU.test(aufbau)) { const lang = els.filter(e => e.typ === 'linie' && Math.max(e.w || 0, e.h || 0) > Math.max(8.5, (STIL.linien.titellinie.laenge_anteil_u[1] + .02) * u));
      const tl = STIL.linien.titellinie.laenge_anteil_u.map(x => (x * u).toFixed(1));
      if (lang.length) fund(12, 'linie', `${lang.length} Linie${lang.length > 1 ? 'n' : ''} bis ${Math.round(Math.max(...lang.map(e => Math.max(e.w || 0, e.h || 0))))} mm lang: Titellinie laut Stilblatt ${tl[0]}–${tl[1]} mm, zwischen Posten nur Luft oder ein kurzer Strich von 6–8 mm`, i, lang[0]); }
    // ---- Blatt ohne Inhalt: kein Titel und kein Lesetext (nur Etiketten, Linien, Bild) ausser bei Rudis Plakaten mit gemalter Kopfzeile
    if (!/^(plakat|plakathoch|plakatganz|plakatrueck|ansicht)$/.test(aufbau) && !texte.some(e => /^(titel|kapitale|text|kursiv|plakatfett|kopf)$/.test(e.rolle))) fund(4, 'leer', `Blatt ohne Titel und ohne Text (Aufbau «${aufbau}»): nur ${texte.length} Etikett${texte.length === 1 ? '' : 'en'}`, i, null);
    // ---- Achse: eine Achse je Seite, Textelemente mittig
    const quer = f.b > f.h * 1.05;   // im Querformat: Bild links, Text rechts bei achse.ausnahmen_quer (fenster, geteilt)
    // Zweispaltige Querformate (achse.zweispaltig_quer, Entscheid Oberchef 30.10.): nur in den dort genannten Formaten; dort steht jeder Text
    // mittig auf einer von zwei Spaltenachsen. Dieselben Aufbauten in anderen Querformaten behalten die eine Mittelachse.
    const ZQ = STIL.achse.zweispaltig_quer, zwei = !!(ZQ && quer && (ZQ.aufbauten || []).includes(aufbau) && (ZQ.formate || []).includes(fk));
    const querAus = quer && (STIL.achse.ausnahmen_quer || []).includes(aufbau) && !(ZQ && (ZQ.aufbauten || []).includes(aufbau));
    if (zwei) { const mitten = texte.filter(e => (e.text || '').trim()).map(e => e.x + e.w / 2), tol = STIL.achse.mittig_toleranz_mm;
      const li = mitten.filter(m => m < f.b / 2), re = mitten.filter(m => m >= f.b / 2), med = a => a.slice().sort((x, y) => x - y)[Math.floor(a.length / 2)];
      const aL = li.length ? med(li) : null, aR = re.length ? med(re) : null;
      if ((aL === null || aR === null) && !els.some(b => b.typ === 'bild' && b.w * (b.h || 0) > f.b * f.h * .15)) fund(12, 'achse', `zweispaltiges Querformat mit nur einer Spalte (Aufbau «${aufbau}», ${fk})`, i, null);   // Bild als zweite Spalte (Gutschein mit Plakat) ist erlaubt
      for (const e of texte) { if (!(e.text || '').trim()) continue; const m = e.x + e.w / 2, a = m < f.b / 2 ? aL : aR;
        if (e.ausr && e.ausr !== 'c') fund(12, 'achse', `Text ${e.ausr === 'l' ? 'links' : 'rechts'}bündig, die Spalte hat eine Mittelachse`, i, e);
        else if (a !== null && Math.abs(m - a) > tol) fund(12, 'achse', `Text ${(m - a).toFixed(1)} mm neben der Achse seiner Spalte`, i, e); } }
    else if (!STIL.achse.ausnahmen_aufbau.includes(aufbau) && !BILDAUFBAU.test(aufbau) && !querAus) {
      for (const e of texte) { const zeit = /\d{1,2}[:.]\d{2}/.test(e.text) || texte.some(o => o !== e && Math.abs(o.y - e.y) < 1.5 && o.ausr !== 'c');
        if (e.ausr && e.ausr !== 'c' && !zeit) fund(12, 'achse', `Text ${e.ausr === 'l' ? 'links' : 'rechts'}bündig, das Blatt hat eine Mittelachse`, i, e);
        else if (e.ausr === 'c' && Math.abs(e.x + e.w / 2 - f.b / 2) > STIL.achse.mittig_toleranz_mm) fund(12, 'achse', `Mittelachse des Textes ${(e.x + e.w / 2 - f.b / 2).toFixed(1)} mm neben der Blattmitte`, i, e); }
    }
    // ---- Marke: höchstens eine Wortmarke, nicht Zeichen und Wortmarke zusammen, Dirty Chicken mit eigenem Zeichen
    const zeichen = els.filter(e => e.typ === 'zeichen'); const wm = zeichen.filter(e => e.z === 2), c = zeichen.filter(e => e.z !== 2);
    if (wm.length > STIL.marke.wortmarke_je_seite_max) fund(14, 'marke', `${wm.length} Wortmarken auf einer Seite`, i, wm[1]);
    if (!STIL.marke.zeichen_und_wortmarke_zusammen && wm.length && c.length) fund(14, 'marke', 'Zeichen und Wortmarke zusammen auf einer Seite', i, c[0]);
    if (ton === 'dc' && c.some(e => e.z !== 3)) fund(24, 'zeichen', 'Dirty-Chicken-Blatt mit Culinarium-Zeichen statt zeichen3', i, c.find(e => e.z !== 3));
    // ---- Überschneidungen von Texten und Zeichen
    const teile = els.filter(e => (e.typ === 'text' && (e.text || '').trim()) || e.typ === 'zeichen');
    for (let a = 0; a < teile.length; a++) for (let b = a + 1; b < teile.length; b++) { const p = teile[a], q = teile[b];
      const ix = Math.min(p.x + p.w, q.x + q.w) - Math.max(p.x, q.x), iy = Math.min(p.y + p.h, q.y + q.h) - Math.max(p.y, q.y);
      if (ix > .5 && iy > .5) fund(5, 'ueberlappt', `«${(p.text || 'Zeichen').slice(0, 20)}» überdeckt «${(q.text || 'Zeichen').slice(0, 20)}» (${ix.toFixed(1)} × ${iy.toFixed(1)} mm)`, i, p); }
    // ---- Komposition (Blätter mit Rahmen und ohne Bildfläche): Gruppe zwischen Kopf/Rahmen und Fusszeile
    // Rahmen des Blatts; ohne gezeichneten Rahmen gilt der Rahmenabstand laut Stilblatt (Story, Aushang ohne Linie)
    const rahmen = els.find(e => e.typ === 'rahmen') || (() => { const a = STIL.linien.rahmen.abstand_anteil_u * u; return { x: a, y: a, w: f.b - 2 * a, h: f.h - 2 * a, ohneLinie: true }; })(); const bildGross = els.some(e => (e.typ === 'bild' || e.typ === 'flaeche') && e.w * (e.h || 0) > f.b * f.h * .25);
    if (rahmen && !bildGross && !BILDAUFBAU.test(aufbau) && aufbau !== 'geteilt') {
      const innen = els.filter(e => (e.typ === 'text' && (e.text || '').trim()) || e.typ === 'zeichen' || e.typ === 'linie').filter(e => e.y >= rahmen.y - .1 && e.y + e.h <= rahmen.y + rahmen.h + .1).sort((a, b) => a.y - b.y);
      const fuss = innen.filter(e => e.slot === 'fuss' || (e.rolle === 'mono' && e.y > rahmen.y + rahmen.h * .85)).pop();
      // Kopfzeile: kleine Etikett-Zeile oben am Rahmen (wie die Fusszeile unten), gehört nicht zur Gruppe
      const k0 = innen[0], kopf = k0 && k0 !== fuss && k0.typ === 'text' && /^(mono|plakat)$/.test(k0.rolle) && k0.y - rahmen.y < .12 * u && innen[1] && innen[1].y - (k0.y + k0.h) > 1.5 * k0.gr ? k0 : null;
      const gruppe = innen.filter(e => e !== fuss && e !== kopf);
      if (gruppe.length >= 2) {
        const oben = Math.min(...gruppe.map(e => e.y)), unten = Math.max(...gruppe.map(e => e.y + e.h));
        const frei0 = kopf ? kopf.y + kopf.h : rahmen.y, frei1 = fuss ? fuss.y : rahmen.y + rahmen.h, frei = frei1 - frei0;
        const fuell = (unten - oben) / frei;
        if (fuell < STIL.komposition.fuellung_min) fund(11, 'fuellung', `Inhalt füllt nur ${Math.round(fuell * 100)} % der freien Höhe (mindestens ${Math.round(STIL.komposition.fuellung_min * 100)} %): wenig Inhalt = grösser, nicht leerer`, i, null);
        const fmax = (STIL.komposition.fuellung_max_aufbau || {})[aufbau] ?? STIL.komposition.fuellung_max;   // Ausnahme je Aufbau vor der allgemeinen Grenze (Oberchef 29.10.2026)
        if (fuell > fmax) fund(11, 'fuellung', `Inhalt füllt ${Math.round(fuell * 100)} % der freien Höhe (höchstens ${Math.round(fmax * 100)} %${fmax !== STIL.komposition.fuellung_max ? ' für «' + aufbau + '»' : ''})`, i, null);
        const mitte = (oben + unten) / 2, soll = (frei0 + frei1) / 2 - .04 * frei;
        if (Math.abs(mitte - soll) > STIL.komposition.toleranz_mitte_anteil * frei) fund(10, 'mitte', `Gruppe ${Math.abs(mitte - soll).toFixed(1)} mm ${mitte < soll ? 'über' : 'unter'} der optischen Mitte (erlaubt ${(STIL.komposition.toleranz_mitte_anteil * frei).toFixed(1)} mm)`, i, null);
        const tz = texte.filter(e => /text|kursiv/.test(e.rolle)).map(e => e.gr * (e.zeile || 1.4)).sort((a, b) => a - b);
        const zeile = tz.length ? tz[tz.length >> 1] : u * STIL.groessen_anteil_u.aushang.text * 1.4;
        let bis = gruppe[0].y + gruppe[0].h;
        for (let g = 1; g < gruppe.length; g++) { const e = gruppe[g]; const luecke = e.y - bis;
          if (luecke > STIL.komposition.loch_max_textzeilen * zeile) fund(10, 'loch', `Loch von ${luecke.toFixed(1)} mm (${(luecke / zeile).toFixed(1)} Textzeilen, erlaubt ${STIL.komposition.loch_max_textzeilen}) vor «${(e.text || e.typ).replace(/\s+/g, ' ').slice(0, 24)}»`, i, { x: rahmen.x, y: bis, w: rahmen.w, h: luecke });
          bis = Math.max(bis, e.y + e.h); }
        const z0 = gruppe[0]; if (z0.typ === 'zeichen' && gruppe[1]) { const abst = gruppe[1].y - (z0.y + z0.h); if (abst > .6 * z0.w) fund(10, 'zeichen', `Zeichen steht ${abst.toFixed(1)} mm über der nächsten Zeile (höchstens 0,6 × Zeichenbreite = ${(.6 * z0.w).toFixed(1)} mm): oben angeheftet`, i, z0); }
        const kopfAbst = (kopf ? kopf.y : oben) - rahmen.y, fussAbst = fuss ? rahmen.y + rahmen.h - (fuss.y + fuss.h) : null;
        if (fuss && Math.abs(kopfAbst - fussAbst) > STIL.komposition.kopf_fuss_gleich_toleranz_mm && (kopf || kopfAbst < fussAbst)) fund(10, 'kopf', `${kopf ? 'Kopfzeile' : 'Kopf'} ${kopfAbst.toFixed(1)} mm, Fusszeile ${fussAbst.toFixed(1)} mm vom Rahmen: Kopf und Fuss nicht gleich weit vom Rahmen`, i, kopf || gruppe[0]);
        if (!kopf && kopfAbst < .08 * u - .1 && z0.typ === 'zeichen') fund(10, 'zeichen', `Zeichen nur ${kopfAbst.toFixed(1)} mm unter dem Rahmen (mindestens 8 % u = ${(.08 * u).toFixed(1)} mm)`, i, z0);
      }
    }
    // ---- gerenderte Zeilen: Einzelwort (K7), Zeilenkästen berühren sich (K27), Text breiter als sein Kasten (K2)
    for (const e of texte) {
      if (!e.dom) continue;
      const tn = []; const w = document.createTreeWalker(e.dom, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.textContent.trim()) tn.push(n);
      const worte = []; for (const t of tn) { const re = /\S+/g; let m; while ((m = re.exec(t.textContent))) { const g = document.createRange(); g.setStart(t, m.index); g.setEnd(t, m.index + m[0].length); const q = [...g.getClientRects()].filter(q => q.width > .3); if (q.length) worte.push({ w: m[0], top: q[0].top, bottom: q[0].bottom, h: q[0].height }); } }
      const zeilen = []; for (const x of worte) { const z = zeilen.find(z => Math.abs(z.top - x.top) < x.h * .5); if (z) { z.w.push(x.w); z.bottom = Math.max(z.bottom, x.bottom); } else zeilen.push({ top: x.top, bottom: x.bottom, w: [x.w] }); }
      zeilen.sort((a, b) => a.top - b.top);
      // Rudis Zeilen als Stapel: jede Zeile genau ein ganzes Glied (Gestaltung 30.10.) ist kein Einzelwort
      const glieder = String(e.text || '').split(/\s*[\/|]\s*|\n/).map(x => x.trim()).filter(Boolean), zt = zeilen.map(z => z.w.filter(x => !/^[|/]$/.test(x)).join(' ').trim());
      const stapel = glieder.length > 1 && zt.length === glieder.length && zt.every((t, j) => t === glieder[j]);
      // Rudis Zeilen (Gestaltung 30.10., Vorgabe Oberchef): nie ein Glied allein in der letzten Zeile, auch kein zweiwortiges, ausser im Stapel (je Zeile ein Glied)
      if (!stapel && glieder.length >= 3 && e.rolle === 'kapitale' && zeilen.length > 1) { let rest = zt.slice(), je = []; let gi = 0;
        for (const t of rest) { let n = 0, acc = ''; while (gi < glieder.length && (acc ? acc + ' ' : '') + glieder[gi] !== t && t.startsWith((acc ? acc + ' ' : '') + glieder[gi])) { acc = (acc ? acc + ' ' : '') + glieder[gi]; gi++; n++; } if (gi < glieder.length && (acc ? acc + ' ' : '') + glieder[gi] === t) { gi++; n++; } je.push(n); }
        if (je[je.length - 1] === 1 && gi === glieder.length) fund(7, 'glied-allein', `Glied «${zt[zt.length - 1]}» allein in der letzten Zeile (Glieder je Zeile: ${je.join(' + ')})`, i, e); }
      if (!stapel && zeilen.length > 1 && /titel|kapitale|plakat|plakatfett|kopf/.test(e.rolle) && worte.length >= 3) { const l = zeilen[zeilen.length - 1].w; if (l.length === 1 && !/^[|/·–—&+-]$/.test(l[0])) fund(7, 'einzelwort', `«${l[0]}» allein in der letzten Zeile`, i, e); }
      if (zeilen.length > 1 && /titel|kapitale|plakat|plakatfett|kopf/.test(e.rolle)) { const r0 = e.dom.getBoundingClientRect(), bl = e.dom.closest('.blatt').getBoundingClientRect();   // Bildprüfung entscheidet: Tinte der Zeilen berührt sich?
        F.push({ k: 27, art: 'zeilen-kandidat', seite: i, zeilen: zeilen.length, info: 'mehrzeiliger Titel', text: e.text.replace(/\s+/g, ' ').slice(0, 60), r: { x: r0.left - bl.left, y: r0.top - bl.top, w: r0.width, h: r0.height } }); }
      // Wort über zwei Zeilen ohne Trennstrich («Signatur / e Drinks»)
      if (getComputedStyle(e.dom.querySelector('*') || e.dom).hyphens !== 'auto') { const geteilt = []; for (const t of tn) { const re = /[\p{L}]{3,}/gu; let m; while ((m = re.exec(t.textContent))) { const g = document.createRange(); g.setStart(t, m.index); g.setEnd(t, m.index + m[0].length); const q = [...g.getClientRects()].filter(q => q.width > .3); if (q.length > 1 && Math.abs(q[0].top - q[q.length - 1].top) > 2) geteilt.push(m[0]); } }
        if (geteilt.length) fund(2, 'wortbruch', `Wort ohne Trennstrich über zwei Zeilen: «${geteilt[0]}»`, i, e); }
      const inner = e.dom.firstElementChild || e.dom; if (inner.scrollWidth > inner.clientWidth + 1 && inner.clientWidth > 0) fund(2, 'ueberlauf', `Text ${inner.scrollWidth} px breit in Kasten ${inner.clientWidth} px`, i, e);
    }
    seitenInfo.push({ aufbau, ton, b: f.b, h: f.h, S, B, rand: B * S });
  });
  // ---- eigene Druckprüfung des Werkzeugs
  const KARTE = [[/Stil:/, 12], [/Platzhalter/, 14], [/am Rand/, 2], [/Kopfzeile/, 13], [/dpi/, 13], [/Foto fehlt/, 4], [/ausserhalb/, 5], [/Beschnitt/, 5], [/mit KI erzeugt/, 19], [/leeres Textfeld/, 4]];
  try { for (const p of DS.pruefe(M, doc)) { if (p.stufe !== 'rot' && !/mit KI|Beschnitt|am Rand/.test(p.text)) continue; const k = (KARTE.find(([r]) => r.test(p.text)) || [0, 0])[1]; if (!k || (k === 14 && F.some(x => x.k === 14 && x.seite === p.seite))) continue;
      const el = doc.seiten[p.seite].el.find(e => e.id === p.id); fund(k, 'druckpruefung', 'Druckprüfung: ' + p.text, p.seite, el); } } catch (e) { fund(0, 'fehler', 'Druckprüfung: ' + e.message, 0, null); }
  return { funde: F, seiten: seitenInfo, format: fk, name: doc.name };
}

(async () => {
  const STIL = JSON.parse(fs.readFileSync(arg('stilblatt'), 'utf8'));
  const b = await pw[arg('browser', 'webkit')].launch();
  const ctx = await b.newContext({ viewport: { width: 2600, height: 1500 }, deviceScaleFactor: 1, locale: 'de-DE' });
  await ctx.route('**/*', r => { const q = r.request(); if (q.method() !== 'GET' && q.method() !== 'HEAD') return r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' }); return r.continue(); });
  await ctx.addInitScript(() => { try { localStorage.setItem('ds-culinarium-willkommen', '1'); } catch (e) { } });
  const p = await ctx.newPage(); const fehler = []; p.on('pageerror', e => fehler.push(e.message));
  await p.goto(URL, { waitUntil: 'load' }); await p.waitForFunction(() => window.DS && DS.M && DS.VORLAGEN && window.DSPlakat, null, { timeout: 30000 }); await p.waitForTimeout(1500);
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(`window.__pruefe = ${pruefeDok.toString()}`);
  // Dokumentliste aus dem Werkzeug
  const liste = [];
  if (NUR.includes('vorlagen')) liste.push(...await p.evaluate(async () => { const ix = await (await fetch('haeuser/culinarium/vorlagen/index.json', { cache: 'no-store' })).json(); const out = [];
    for (const a of ix) { if (a.eingebaut) continue;   // eingebaute Vorlagen (Speisekarte, Getränkekarte, Menü-Einleger) kommen aus start.js und stecken in der Quelle «Arten»
      const d = await (await fetch(`haeuser/culinarium/vorlagen/${a.art}.json`, { cache: 'no-store' })).json();
      d.vorlagen.forEach((v, i) => out.push({ quelle: 'Vorlage', gruppe: a.art, titel: v.titel, format: d.format, seiten: [{ vorlage: v.vorlage, ton: v.ton, inhalt: v.inhalt, stil: v.stil }], vid: v.id })); }
    return out; }));
  if (NUR.includes('arten')) liste.push(...await p.evaluate(async () => { const t = await (await fetch('start.js', { cache: 'no-store' })).text();
    const inh = t.slice(t.indexOf('const INHALT = '), t.indexOf('\n', t.indexOf('const INHALT = '))), art = t.slice(t.indexOf('const ARTEN = ['), t.indexOf('];', t.indexOf('const ARTEN = [')) + 2);
    const { INHALT, ARTEN } = new Function('DS', inh + '\n' + art + '\nreturn { INHALT, ARTEN };')(DS); const out = [];
    for (const a of ARTEN) { if (a.leer) continue; for (const [v, ton] of a.vorlagen) for (const fk of (a.formate || [a.format])) { if (!DS.FORMATE[fk]) continue;
      out.push({ quelle: 'Art', gruppe: a.key, titel: `${a.name} · ${DS.VORLAGEN[v] ? DS.VORLAGEN[v].name : v} · ${DS.FORMATE[fk].name} · ${ton}`, format: fk, seiten: [{ vorlage: v, ton, inhalt: (INHALT[a.key] && INHALT[a.key][v]) || DS.BEISPIEL[v] }] }); } }
    return out; }));
  if (NUR.includes('entwerfen')) { const ew = path.join(AUS, 'entwerfen.json'); if (fs.existsSync(ew)) liste.push(...JSON.parse(fs.readFileSync(ew, 'utf8'))); }
  if (NUR.includes('muster')) liste.push(...await p.evaluate(() => { const fm = [...document.querySelectorAll('#vorlageFormat option')].map(o => o.value), tn = [...document.querySelectorAll('#vorlageTon option')].map(o => o.value); const out = [];
    for (const [k, v] of Object.entries(DS.VORLAGEN)) for (const fk of fm.filter(fk => !v.formate || v.formate.includes(fk))) for (const t of tn)   // nur Formate, für die der Aufbau gemacht ist (DS.VORLAGEN[k].formate)
      out.push({ quelle: 'Muster', gruppe: k, titel: `${v.name} · ${DS.FORMATE[fk].name} · ${t}`, format: fk, seiten: [{ vorlage: k, ton: t, inhalt: DS.BEISPIEL[k] }] });
    return out; }));
  if (NUR.includes('vorschlaege')) liste.push(...await p.evaluate(() => { const out = []; for (const m of DSPlakat.motive()) for (const fk of ['ig11', 'a3h', 'story']) out.push({ quelle: 'Vorschlag', gruppe: 'Abend beschreiben', titel: `${m.titel} · ${DS.FORMATE[fk].name}`, format: fk, motiv: m.key,
      seiten: [{ vorlage: 'plakat', ton: 'hell' }, { vorlage: 'plakatrueck', ton: 'dunkel' }] }); return out; }));
  // Schrift je Rolle: liefert das Werkzeug für jede Rolle die Datei, die das Stilblatt nennt?
  const schriften = await p.evaluate(() => DS.M.schriften); const werkzeugFunde = [];
  const norm = t => String(t).toLowerCase().replace(/[^a-z0-9]/g, '');
  for (const r of Object.values(STIL.rollen)) for (const rolle of r.rolle) { const soll = [].concat(r.schrift).map(norm), ist = norm((schriften[rolle] || {}).datei || '');
    if (!soll.some(x => ist.includes(x))) werkzeugFunde.push({ k: 12, art: 'schrift', info: `Rolle «${rolle}» lädt ${(schriften[rolle] || {}).datei || 'keine Datei'}, Stilblatt: ${[].concat(r.schrift).join(' oder ')}` }); }
  console.log('Dokumente aus dem Werkzeug:', liste.length, Object.entries(liste.reduce((a, x) => (a[x.quelle] = (a[x.quelle] || 0) + 1, a), {})).map(x => x.join(' ')).join(', '));
  const erg = [];
  for (const [n, spec] of liste.entries()) {
    const id = String(n + 1).padStart(4, '0');
    let r;
    try {
      if (spec.motiv) r = await p.evaluate(a => { a.spec.doc = DSPlakat.plakatDoc({ motiv: a.spec.motiv, format: a.spec.format, titel: '' }); return window.__pruefe(a); }, { spec, STIL, PX });
      else r = await p.evaluate(a => window.__pruefe(a), { spec, STIL, PX });
    } catch (e) { erg.push({ id, ...spec, fehler: e.message.slice(0, 200), funde: [{ k: 0, art: 'fehler', info: 'Setzen fehlgeschlagen: ' + e.message.slice(0, 120) }] }); continue; }
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(120);
    const bilder = [];
    if (!process.argv.includes('--ohne-bilder')) for (let i = 0; i < r.seiten.length; i++) { const f = `${id}-${i}.png`; await p.locator(`#tor-wirt [data-tor="blatt${i}"]`).screenshot({ path: path.join(BILDER, f) }).then(() => bilder.push(f)).catch(() => { }); }
    const { seiten, ...s0 } = spec; erg.push({ id, quelle: spec.quelle, gruppe: spec.gruppe, titel: spec.titel, format: r.format, aufbau: seiten.map(x => x.vorlage), ton: seiten.map(x => x.ton), funde: r.funde, seitenInfo: r.seiten, bilder, vid: spec.vid });
    if (n % 25 === 0) { console.log(id, spec.quelle, spec.titel.slice(0, 50), r.funde.length, 'Funde'); fs.writeFileSync(path.join(AUS, 'dokumente.json'), JSON.stringify({ zeit: new Date().toISOString(), dokumente: erg, fehler }, null, 1)); }
  }
  fs.writeFileSync(path.join(AUS, 'dokumente.json'), JSON.stringify({ zeit: new Date().toISOString(), url: URL, werkzeugFunde, dokumente: erg, fehler: fehler.slice(0, 40) }, null, 1));
  console.log('FERTIG', erg.length, 'Dokumente,', erg.reduce((a, x) => a + x.funde.length, 0), 'Funde');
  await b.close();
})();
