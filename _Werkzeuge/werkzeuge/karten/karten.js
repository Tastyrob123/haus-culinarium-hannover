/* karten.js · das Werkzeug «karten» (Grandhotel: La Carte · Landhaus: Die Tafel). Für jedes Haus dasselbe: ?haus=<kennung>.
   Aufbau und Abläufe eins zu eins nach La Carte am Grand Beau-Rivage (mission-control/mc.js, Robert 11./12.10.2026):
   Zwei Wege: «Einfach» (Liste mit Fenstern: hinzufügen, ändern, ausblenden, verschieben) und «Fortgeschritten» (direkt in der
   Karte schreiben, dazu die Daten der Karte als Text). Jede Änderung landet zuerst im Entwurf; «Veröffentlichen» macht daraus
   die neue PDF. Was hier anders ist als dort, weil es für jedes Haus gelten muss:
     · Daten nur über den gemeinsamen Speicher (ein Entwurf je Haus, Konflikt statt Überschreiben), nie über Dateien.
     · Die Karte steht in einem eigenen Rahmen (druck.html): sie bleibt in der Welt des Hauses, während der Knopf oben
       die Welt des Werkzeugs wechselt. Derselbe Satz druckt die PDF.
     · Ausblenden statt löschen. Angaben zum Preis («33cl», «Portion»), Tafeln mit festen Spalten, Allergene, Zeitraum.
     · Keine Fotos und kein Zeichen des Hauses (die liefert später «marke»): Ring mit Anfangsbuchstaben, Kachel mit Initiale.
   Ohne Bibliothek. */
(() => {
'use strict';
const HAUS = (window.Welt && Welt.haus) || '';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const h = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const kopie = x => JSON.parse(JSON.stringify(x));
const sauber = t => String(t == null ? '' : t).replace(/ /g, ' ').replace(/\s+/g, ' ').trim();
const sv = d => `<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
const PF = sv('<path d="M3 11 11 3M4.5 3H11v6.5"/>');
const SYM = {
  hoch: sv('<path d="m2.5 9 4.5-4.5L11.5 9"/>'), runter: sv('<path d="m2.5 5 4.5 4.5L11.5 5"/>'), zu: sv('<path d="m3 3 8 8M11 3l-8 8"/>'),
  auge: '<svg viewBox="0 0 16 14" aria-hidden="true"><path d="M1 7s2.6-4.5 7-4.5S15 7 15 7s-2.6 4.5-7 4.5S1 7 1 7Z"/><circle cx="8" cy="7" r="1.9"/></svg>',
  augezu: '<svg viewBox="0 0 16 14" aria-hidden="true"><path d="M1 7s2.6-4.5 7-4.5S15 7 15 7s-2.6 4.5-7 4.5S1 7 1 7Z"/><path d="m3 1 10 12"/></svg>',
  korb: sv('<path d="M2.5 4h9M5.5 4V2.5h3V4M3.5 4l.6 7.5h5.8L10.5 4"/>'), plus: sv('<path d="M7 2.5v9M2.5 7h9"/>'), haken: sv('<path d="m2.5 7.5 3 3 6-7"/>')
};
const ART = { gericht: 'Gericht', zeile: 'Zeile', rubrik: 'Rubrik', land: 'Zwischentitel', zw: 'Kleiner Zwischentitel', kopf: 'Spaltenkopf', notiz: 'Hinweis', frei: 'Textblock' };

const GESCHRIEBEN = new Set();   // im Weg Fortgeschritten seit dem letzten Speichern geschriebene Stellen
let STAND = null;                // Antwort des Speichers: live, entwurf, Kennungen, offen
let DOC = null;                  // Arbeitsstand aller Karten des Hauses: der Entwurf, sonst der veröffentlichte Stand
let UEBER = { haus: { kennung: HAUS, name: HAUS, welt: 'grand', kleid: null }, pdf: {}, allergene: {}, sprachen: [] };
let ZSVG = '';                   // Zeichnung des Hauses (kleid/<haus>/zeichen.svg, von kleid.py auf reine Formen beschränkt)
let ANSICHT = 'karte';           // Vorschau: Karte (wie die PDF) oder Website (wartet, bis ein Haus angeschlossen ist)
let Z = '', BASIS = '', MODUS = 'einfach', OFFEN = false, UNDO = [], BLITZ = null, SETZ = 0, LETZTE = null, GRUEN = false, laufend = null;
const ZM = { einfach: 0.6, frei: 0.78 };   // Grösse der Vorschau je Weg
try { MODUS = localStorage.getItem('karten-modus') === 'frei' ? 'frei' : 'einfach'; ZM.einfach = +(localStorage.getItem('karten-zoom-einfach') || 0.6); ZM.frei = +(localStorage.getItem('karten-zoom-frei') || 0.78); } catch (e) { /* ohne Speicher geht es auch */ }

// ---------------------------------------------------------------- Verbindung
async function ruf(methode, weg, koerper) {
  let r, d;
  try { r = await fetch(weg, { method: methode, cache: 'no-store', headers: koerper ? { 'Content-Type': 'application/json' } : {}, body: koerper ? JSON.stringify(koerper) : undefined }); }
  catch (e) { throw Object.assign(new Error('Keine Verbindung zum Server. Bitte prüfen Sie, ob er läuft, und versuchen Sie es noch einmal.'), { stichwort: 'server-stumm' }); }
  try { d = await r.json(); } catch (e) { d = { fehler: 'Die Antwort des Servers ist nicht lesbar.', stichwort: 'antwort-unlesbar' }; }
  if (!r.ok) throw Object.assign(new Error(d.fehler || 'Das hat nicht geklappt.'), { status: r.status, stichwort: d.stichwort || '', antwort: d });
  return d;
}
const H = () => encodeURIComponent(HAUS);
const wer = () => { try { return localStorage.getItem('karten-wer') || ''; } catch (e) { return ''; } };
const erwartet = () => STAND.kennung_entwurf || STAND.kennung_live;

// ---------------------------------------------------------------- Meldungen
function sag(titel, text = '', knoepfe = [], fehl = false, dauer) {
  const m = document.createElement('div');
  m.className = 'kt-quit' + (fehl ? ' kt-fehl' : ''); m.setAttribute('role', fehl ? 'alert' : 'status');
  m.innerHTML = `<div><b>${h(titel)}</b>${text ? `<span>${h(text)}</span>` : ''}</div>` + knoepfe.map((k, i) => k.href ? `<a href="${h(k.href)}" target="_blank" rel="noopener">${h(k.t)}</a>` : `<button type="button" data-i="${i}">${h(k.t)}</button>`).join('');
  m.addEventListener('click', ev => { const b = ev.target.closest('button[data-i]'); if (b) { m.remove(); knoepfe[+b.dataset.i].f(); } });
  const ort = $('#kt-meldung'); ort.appendChild(m);
  while (ort.children.length > 2) ort.firstElementChild.remove();   // höchstens zwei Quittungen auf einmal, die neueste unten
  setTimeout(() => m.remove(), dauer || (fehl ? 12000 : 7000));
  return m;
}

// ---------------------------------------------------------------- Daten-Hilfen
const eintrag = (id, d) => ((d || DOC).karten || []).find(e => e.id === (id || Z));
const D = () => eintrag().karte;
const teile = () => D().teile;
const geaendert = () => JSON.stringify(DOC) !== JSON.stringify(STAND.live);
const karteAnders = id => JSON.stringify(eintrag(id)) !== JSON.stringify(eintrag(id, STAND.live));
function setzePfad(o, pfad, wert) {
  const k = pfad.split('.'); let x = o;
  for (let i = 0; i < k.length - 1; i++) x = x[/^\d+$/.test(k[i]) ? +k[i] : k[i]];
  const l = k[k.length - 1]; x[/^\d+$/.test(l) ? +l : l] = wert;
}
/* Preis in der Schreibweise des Hauses: «18» → «CHF 18», «12» → «CHF 12.00», «9» → «9.00», «12,5» bleibt, je nach den Nachbarn */
function preisForm(ein, nachbarn) {
  const t = String(ein || '').trim().replace(/\s+/g, ' ');
  const m = t.match(/^(?:chf\s*)?(\d{1,5})(?:[.,](\d{1,2}))?$/i);
  if (!m) return t;         // was keine reine Zahl ist, bleibt, wie es geschrieben wurde
  const bsp = nachbarn.filter(Boolean), mitStellen = bsp.filter(x => /\d[.,]\d{1,2}$/.test(x));
  const chf = bsp.length > 0 && bsp.filter(x => /^CHF\s/i.test(x)).length * 2 > bsp.length;
  const komma = bsp.filter(x => /\d,\d/.test(x)).length > bsp.filter(x => /\d\.\d/.test(x)).length;
  const immer = bsp.length > 0 && mitStellen.length * 2 >= bsp.length;
  const zwei = mitStellen.filter(x => /\d[.,]\d\d$/.test(x)).length * 2 >= mitStellen.length;
  let z = m[1];
  if (m[2] || immer) z += (komma ? ',' : '.') + (zwei ? ((m[2] || '') + '00').slice(0, 2) : (m[2] || '0'));
  return (chf ? 'CHF ' : '') + z;
}
function nachbarPreise(ti, i) {   // zuerst die Preise derselben Rubrik, sonst die der Karte
  const aus = u => (u.t === 'zeile' ? [u.preis] : (u.preise || []).concat(...(u.zeilen || []).map(z => z.preise || []))).filter(Boolean);
  const p = teile()[ti].posten;
  if (p.length) { let a = Math.min(Math.max(i, 0), p.length - 1), b = a; while (a > 0 && p[a].t !== 'rubrik') a--; while (b + 1 < p.length && p[b + 1].t !== 'rubrik') b++; const nah = p.slice(a, b + 1).flatMap(aus); if (nah.length) return nah.slice(0, 40); }
  return teile().flatMap(t => (t.posten || []).flatMap(aus)).slice(0, 60);
}
/* Rubrik-Blöcke eines Teils: [start, ende) je Rubrik */
function bloecke(ti) {
  const p = teile()[ti].posten, aus = [];
  p.forEach((u, i) => { if (u.t === 'rubrik') aus.push([i, p.length]); });
  aus.forEach((b, j) => { if (aus[j + 1]) b[1] = aus[j + 1][0]; });
  return aus;
}
function rubrikVon(ti, i) { const p = teile()[ti].posten; for (let j = Math.min(i, p.length - 1); j >= 0; j--) if (p[j].t === 'rubrik') return p[j]; return null; }
/* Spaltenköpfe, unter denen ein Eintrag steht (Tafel mit mehreren Preisen je Zeile) */
function koepfeFuer(ti, i) { const p = teile()[ti].posten; for (let j = Math.min(i, p.length - 1); j >= 0; j--) { if ((p[j].t === 'rubrik' || p[j].t === 'zw') && (p[j].koepfe || []).length) return p[j].koepfe; if (p[j].t === 'rubrik') return null; } return null; }
function preisText(u) { if (u.t === 'zeile') return u.preis || ''; const e = u.einheiten || []; return (u.preise || []).map((p, i) => [e[i], p].filter(Boolean).join(' ')).filter(Boolean).join(' · '); }
const nameVon = u => u.name || u.titel || u.text || ((u.zeilen || [])[0] || {}).text || '';
function datumText(iso) { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || ''); return m ? `${m[3]}.${m[2]}.${m[1]}` : ''; }
function datumLesen(t) {    // Tag.Monat.Jahr schreiben, als JJJJ-MM-TT ablegen (kein Kalender des Betriebssystems)
  t = String(t || '').trim(); if (!t) return '';
  const m = /^(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})$/.exec(t); if (!m) return null;
  const d = new Date(Date.UTC(+m[3], +m[2] - 1, +m[1]));
  if (d.getUTCFullYear() !== +m[3] || d.getUTCMonth() !== +m[2] - 1 || d.getUTCDate() !== +m[1]) return null;
  return `${m[3]}-${('0' + m[2]).slice(-2)}-${('0' + m[1]).slice(-2)}`;
}
function zeitText(iso) { const m = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/.exec(iso || ''); return m ? `${m[3]}.${m[2]}.${m[1]} ${m[4]}:${m[5]}` : (iso || ''); }
const kurzname = n => { const m = /«(.*)»/.exec(n || ''); return m ? m[1] : (n || ''); };
/* Kachel der Karte: Anfangsbuchstaben der gross geschriebenen Wörter («La Petite Suisse» → LPS), bis das Haus Fotos liefert */
const initialen = n => { const w = (n || '').split(/[\s’'\-]+/).filter(x => /^\p{Lu}/u.test(x)).map(x => x[0]); return (w.length ? w : [((n || '').match(/[\p{L}\p{N}]/u) || [''])[0].toUpperCase()]).slice(0, 3).join(''); };
/* Zeichen des Hauses. Hat das Haus ein Kleid, ist es seine Zeichnung (rund oder als Schriftzug), sonst ein Ring mit den Anfangsbuchstaben. */
const kleid = () => UEBER.haus.kleid || {};
const kleidDatei = name => name ? `kleid/${H()}/${encodeURIComponent(name)}` : '';
const zeichen = () => {
  if (ZSVG) { const m = kleid().zeichen_mass || [1, 1]; return `<span class="kt-zeichen kt-zeichen--bild${m[0] / m[1] > 1.6 ? ' kt-zeichen--breit' : ''}" aria-hidden="true">${ZSVG}</span>`; }
  const w = (UEBER.haus.name || '').split(/[\s-]+/).filter(Boolean); return `<span class="kt-zeichen" aria-hidden="true">${h((w.length > 1 ? w[0][0] + w[1][0] : (w[0] || '').slice(0, 2)).toUpperCase())}</span>`;
};
/* Tapete des Hauses liegt nur in seiner eigenen Welt auf dem Raum: wechselt der Knopf die Welt, bleibt die Fläche der anderen Welt frei */
function kleide() { const t = kleid().tapete && Welt.welt() === UEBER.haus.welt ? `url("${kleidDatei(kleid().tapete)}")` : ''; if (t) document.documentElement.style.setProperty('--kt-tapete', t); else document.documentElement.style.removeProperty('--kt-tapete'); }

// ---------------------------------------------------------------- Vergleich veröffentlicht ↔ Entwurf (alle Karten des Hauses)
function stuecke(e) {
  const aus = [], k = e.karte;
  let rub = '';
  aus.push({ ort: 'Karte', art: 'karte', u: { t: 'karte', text: [k.name, k.fuss, e.gilt.von && 'gilt von ' + datumText(e.gilt.von), e.gilt.bis && 'gilt bis ' + datumText(e.gilt.bis)].filter(Boolean).join(' · ') } });
  k.teile.forEach((t, ti) => {
    if (t.art === 'deckel') { aus.push({ ort: 'Deckblatt', art: 'deckel', u: Object.assign({ t: 'deckel' }, t), ti }); return; }
    t.posten.forEach((u, i) => { if (u.t === 'rubrik') rub = u.titel; aus.push({ ort: u.t === 'rubrik' ? 'Rubrik' : rub, art: u.t, u, ti, i }); });
  });
  aus.forEach(x => { const c = Object.assign({}, x.u); delete c.s; x.voll = JSON.stringify(c); });
  return aus;
}
function vergleich(a, b) {   // a: vorher, b: nachher (ganze Dokumente)
  const aus = [];
  [...new Set(a.karten.map(e => e.id).concat(b.karten.map(e => e.id)))].forEach(id => {
    const ea = eintrag(id, a), eb = eintrag(id, b), karte = kurzname((eb || ea).karte.name);
    if (!ea || !eb) { aus.push({ art: ea ? 'weg' : 'neu', karte, kid: id, [ea ? 'a' : 'b']: { ort: 'Karte', art: 'karte', u: { t: 'karte', text: (ea || eb).karte.name } } }); return; }
    const A = stuecke(ea), B = stuecke(eb), n = A.length, m = B.length;
    const L = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1));
    for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) L[i][j] = A[i].voll === B[j].voll ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
    const wegA = [], neuB = [];
    let i = 0, j = 0, lueckeA = [], lueckeB = [];
    const schliesse = () => {   // was zwischen zwei gleichen Stücken liegt: gleiche Art der Reihe nach = geändert
      while (lueckeA.length && lueckeB.length && lueckeA[0].art === lueckeB[0].art) aus.push({ art: 'anders', karte, kid: id, a: lueckeA.shift(), b: lueckeB.shift() });
      wegA.push(...lueckeA); neuB.push(...lueckeB); lueckeA = []; lueckeB = [];
    };
    while (i < n || j < m) {
      if (i < n && j < m && A[i].voll === B[j].voll) { schliesse(); i++; j++; }
      else if (j < m && (i === n || L[i][j + 1] >= L[i + 1][j])) lueckeB.push(B[j++]);
      else lueckeA.push(A[i++]);
    }
    schliesse();
    wegA.slice().forEach(x => { const k = neuB.findIndex(y => y.voll === x.voll); if (k >= 0) { const y = neuB.splice(k, 1)[0]; wegA.splice(wegA.indexOf(x), 1); aus.push({ art: 'verschoben', karte, kid: id, a: x, b: y }); } });
    wegA.forEach(x => aus.push({ art: 'weg', karte, kid: id, a: x })); neuB.forEach(y => aus.push({ art: 'neu', karte, kid: id, b: y }));
  });
  return aus;
}
function zustand() {   // je Eintrag der offenen Karte im Entwurf: neu / anders / verschoben
  const st = {};
  if (!STAND) return st;
  vergleich(STAND.live, DOC).forEach(v => { if (v.kid === Z && v.b && v.b.i !== undefined) st[v.b.ti + '.' + v.b.i] = v.art; });
  return st;
}

// ---------------------------------------------------------------- Kopfleiste und Rand
function pdfZeit(id) { const p = UEBER.pdf[id]; return p && p.vorhanden && p.erzeugt ? 'PDF vom ' + zeitText(p.erzeugt) : ''; }
function oben() {
  const k = D(), g = geaendert();
  $('#kt-zeichen-oben').outerHTML = zeichen().replace('<span class="', '<span id="kt-zeichen-oben" class="');
  $('#kt-oben-haus').textContent = 'Karten · ' + UEBER.haus.name;
  $('#kt-oben-titel').textContent = k.name;
  $('#kt-oben-stand').textContent = OFFEN ? 'Nicht gespeichert' : g ? 'Entwurf wartet' : pdfZeit(Z) || 'Wie veröffentlicht';
  document.title = Welt.name('karten') + ' · ' + UEBER.haus.name;
}
function rand() {
  $('#kt-rand').innerHTML = `
    <div class="kt-karten"><p class="kt-kap"><span>Ihre Karten</span></p>${DOC.karten.map(e => { const n = kurzname(e.karte.name); return `<button class="kt-kw" type="button" data-z="${h(e.id)}" aria-current="${e.id === Z}">${(kleid().fotos || {})[e.id] ? `<span class="kt-kw__f kt-kw__f--foto" aria-hidden="true" style="background-image:url('${kleidDatei(kleid().fotos[e.id])}')"></span>` : `<span class="kt-kw__f" aria-hidden="true" data-n="${initialen(n).length}">${h(initialen(n))}</span>`}<b>${h(n)}</b><small>${h([e.karte.gruppe, pdfZeit(e.id)].filter(Boolean).join(' · '))}</small>${karteAnders(e.id) ? '<i class="marke">Entwurf</i>' : ''}</button>`; }).join('')}</div>
    <div class="kt-modus" role="group" aria-label="Art der Bearbeitung"><button type="button" data-m="einfach" aria-pressed="${MODUS === 'einfach'}">Einfach</button><button type="button" data-m="frei" aria-pressed="${MODUS === 'frei'}">Fortgeschritten</button></div>
    <p class="kt-modus__t">${MODUS === 'einfach' ? 'Gerichte und Getränke in einer Liste: hinzufügen, ändern, ausblenden, entfernen, verschieben. Rechts steht sofort die Karte.' : 'Sie schreiben direkt in der Karte. Jeder Text lässt sich ändern, auch Überschriften, Hinweise und das Deckblatt. Dazu die Daten der Karte als Text.'}</p>
    <div class="kt-wege"><p class="kt-kap"><span>Wege</span></p>
      <button type="button" data-akt="verlauf">Frühere Fassungen <span aria-hidden="true">↺</span></button>
      <button type="button" data-akt="pdf">PDF der Karte öffnen <span aria-hidden="true">↗</span></button>
      <button type="button" data-akt="karte">Karte einrichten <span aria-hidden="true">→</span></button></div>`;
  oben();
}

// ---------------------------------------------------------------- Kopf
function kopf() {
  const k = D(), nm = (k.name || '').match(/^(.*?)\s*«(.*)»\s*$/);
  $('#kt-kopf').innerHTML = `<div class="kt-kopf__in">${zeichen()}<h1>${nm ? `${h(nm[1])} <em>${h(nm[2])}.</em>` : h(k.name || '')}</h1><p class="kt-kopf__u"><span>${h(k.gruppe || 'Karte')}</span><i></i><span>${MODUS === 'einfach' ? 'Einfach' : 'Fortgeschritten'}</span></p>
    <p class="kt-satz">${MODUS === 'einfach' ? 'Ein Klick auf einen Eintrag öffnet ihn. Jede Änderung wird sofort als Entwurf gespeichert und steht rechts in der Karte. Die PDF bleibt, wie sie ist, bis Sie unten auf «Veröffentlichen» drücken.'
      : 'Klicken Sie in der Karte auf einen Text und schreiben Sie. Gespeichert wird mit dem Knopf unten. Neue Gerichte und Rubriken legen Sie im Weg «Einfach» an, oder Sie ändern die Daten der Karte direkt.'}</p></div>
    <div class="kt-kopf__kn">${MODUS === 'einfach' ? `<button class="kn kn--d" type="button" data-akt="neu">Neuer Eintrag<i>${SYM.plus}</i></button>` : `<button class="kn" type="button" data-akt="daten">Daten der Karte<i>${PF}</i></button>`}</div>`;
}

// ---------------------------------------------------------------- Liste (Einfach)
const rund = (akt, name, bild) => `<button class="kt-rund" type="button" data-akt="${akt}" title="${h(name)}" aria-label="${h(name)}">${SYM[bild]}</button>`;
function zeileHTML(u, ti, i, st) {
  const chip = (st === 'neu' ? '<i class="kt-chip">Neu</i>' : st === 'anders' ? '<i class="kt-chip">Geändert</i>' : st === 'verschoben' ? '<i class="kt-chip">Verschoben</i>' : '')
    + (u.aus ? '<i class="kt-chip">Ausgeblendet</i>' : '') + (u.uebersetzung === 'offen' ? '<i class="kt-chip">Englisch nachziehen</i>' : '');
  const pfeile = rund('hoch', 'Nach oben', 'hoch') + rund('runter', 'Nach unten', 'runter') + rund('weg', 'Entfernen', 'korb');
  const auge = (was) => rund('aus', u.aus ? `${was} wieder zeigen` : `${was} vorübergehend ausblenden`, u.aus ? 'augezu' : 'auge');
  const d = `data-ti="${ti}" data-i="${i}"`;
  if (u.t === 'rubrik') return `<div class="kt-r kt-r--rubrik${u.aus ? ' kt-aus' : ''}" ${d}><button type="button" class="kt-r__t" data-akt="edit"><b>${h(u.titel)}</b>${u.en || u.zusatz ? `<small>${h([u.en, u.zusatz].filter(Boolean).join(' · '))}</small>` : ''}${chip}</button><div class="kt-r__k"><button class="kn kn--klein kn--ohne" type="button" data-akt="neu-hier">Eintrag hinzufügen</button>${pfeile}${auge('Rubrik')}</div></div>`;
  if (u.t === 'land' || u.t === 'zw' || u.t === 'kopf') return `<div class="kt-r kt-r--klein${u.t === 'land' ? ' kt-r--land' : ''}" ${d}><button type="button" class="kt-r__t" data-akt="edit"><b>${h(u.text)}</b>${(u.koepfe || []).length ? `<small>${h(u.koepfe.join(' · '))}</small>` : ''}${chip}</button><div class="kt-r__k">${pfeile}</div></div>`;
  if (u.t === 'notiz' || u.t === 'frei') return `<div class="kt-r kt-r--klein kt-r--notiz${u.aus ? ' kt-aus' : ''}" ${d}><button type="button" class="kt-r__t" data-akt="edit"><b>${h(u.t === 'frei' ? u.zeilen.map(z => z.text).join(' ') : u.text)}</b>${chip}</button><div class="kt-r__k">${auge('Text')}${pfeile}</div></div>`;
  const z = u.t === 'gericht' ? (u.zeilen || []).filter(x => !x.en && !(x.preise || []).length).map(x => x.text).join(' · ') : '';
  return `<div class="kt-r${u.aus ? ' kt-aus' : ''}" ${d}><button type="button" class="kt-r__t" data-akt="edit"><b>${h(u.name)}</b>${u.zusatz ? `<small>${h(u.zusatz)}</small>` : ''}${chip}${z ? `<span>${h(z)}</span>` : ''}</button><span class="kt-r__p">${(u.einheiten || []).some(Boolean) ? (u.preise || []).map((x, n) => h([u.einheiten[n], x].filter(Boolean).join(' '))).join('<br>') : h(preisText(u))}</span>
    <div class="kt-r__k">${auge('Eintrag')}${pfeile}</div></div>`;
}
function liste() {
  const st = zustand();
  $('#kt-liste').innerHTML = teile().map((t, ti) => {
    if (t.art === 'deckel') return `<div class="kt-teil"><div class="kt-r kt-r--deckel" data-ti="${ti}">${zeichen()}<button type="button" class="kt-r__t" data-akt="edit-deckel"><b>${h(t.titel)}</b><span>${h(t.unter || 'Deckblatt')}${t.zeilen && t.zeilen.length ? ' · ' + h(t.zeilen.join(' · ')) : ''}</span></button><div class="kt-r__k"><button class="kn kn--klein kn--ohne" type="button" data-akt="edit-deckel">Deckblatt ändern</button></div></div></div>`;
    return `<div class="kt-teil" data-teil="${ti}">${t.posten.map((u, i) => zeileHTML(u, ti, i, st[ti + '.' + i])).join('')}
      <div class="kt-neu-zeile"><button class="kn kn--klein kn--ohne" type="button" data-akt="neu-ende" data-ti="${ti}">Eintrag am Ende</button><button class="kn kn--klein kn--ohne" type="button" data-akt="rubrik-neu" data-ti="${ti}">Neue Rubrik</button></div></div>`;
  }).join('');
  if (BLITZ) { const r = $(`.kt-r[data-ti="${BLITZ[0]}"][data-i="${BLITZ[1]}"]`); if (r) { r.classList.add('kt-blitz'); r.scrollIntoView({ block: 'nearest' }); } }
}

// ---------------------------------------------------------------- Vorschau: druck.html im Rahmen, derselbe Satz wie die PDF
let rahmenLos, miniLos = null;
const rahmen = new Promise(r => { rahmenLos = r; });
window.KT_VORSCHAU_BEREIT = w => { const id = w.frameElement && w.frameElement.id; if (id === 'kt-mini') { if (miniLos) miniLos(w); return; } haengeAn(w); rahmenLos(w); };
function haengeAn(w) {
  const d = w.document, stelle = ev => ev.target && ev.target.closest ? ev.target.closest('[data-k]') : null;
  d.addEventListener('click', ev => {   // Weg Einfach: Klick auf einen Text der Karte öffnet den Eintrag
    if (MODUS !== 'einfach') return;
    const el = stelle(ev); if (!el) return;
    const k = el.getAttribute('data-k'), m = k.match(/^teile\.(\d+)(?:\.posten\.(\d+))?/);
    if (k === 'fuss') return karteFenster();
    if (!m) return;
    if (m[2] === undefined) return deckelFenster(+m[1]);
    eintragFenster({ ti: +m[1], i: +m[2] });
  });
  d.addEventListener('input', ev => {   // Weg Fortgeschritten: direkt in der Karte schreiben
    const el = stelle(ev); if (!el || MODUS !== 'frei') return;
    setzePfad(D(), el.getAttribute('data-k'), sauber(el.textContent));
    GESCHRIEBEN.add(el.getAttribute('data-k')); el.setAttribute('data-neu', '1');
    OFFEN = JSON.stringify(DOC) !== BASIS; leiste();
  });
  d.addEventListener('keydown', ev => { if (stelle(ev) && ev.key === 'Enter') { ev.preventDefault(); ev.target.blur(); } if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 's') { ev.preventDefault(); if (OFFEN) speichern('Im Entwurf gespeichert'); } });
  d.addEventListener('paste', ev => { if (!stelle(ev)) return; ev.preventDefault(); d.execCommand('insertText', false, (ev.clipboardData.getData('text/plain') || '').replace(/\s+/g, ' ')); });
  d.addEventListener('focusout', ev => { if (MODUS === 'frei' && stelle(ev)) setTimeout(() => { if (!d.activeElement || !d.activeElement.closest('[data-k]')) vorschau(); }, 150); });
}
const kopt = () => ({ welt: UEBER.haus.welt, haus: UEBER.haus.name, allergene: UEBER.allergene, zeichen: ZSVG, zeichenMass: kleid().zeichen_mass, tapete: kleidDatei(kleid().tapete) });   // was der Satz vom Haus braucht
const vopt = () => { const sc = $('#kt-seiten'), st = getComputedStyle(sc); return { ...kopt(), pfade: true, bearbeiten: MODUS === 'frei', unterschrift: true, reihe: MODUS === 'frei', massstab: ZM[MODUS], breite: Math.floor(sc.clientWidth - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight)) }; };
async function vorschau() {
  const nr = ++SETZ, w = await rahmen, sc = $('#kt-seiten'), f = $('#kt-vorschau');
  if (nr !== SETZ) return;
  const oben = sc.scrollTop, fensterOben = window.scrollY;
  let r;
  try { r = await w.KT_DRUCK.zeige(D(), vopt()); } catch (e) { $('#kt-vzahl').textContent = 'Die Karte lässt sich nicht setzen'; return; }
  if (nr !== SETZ) return;
  LETZTE = r;
  f.style.height = r.hoehe + 'px';
  if (ANSICHT === 'karte') $('#kt-vzahl').textContent = `${r.seiten} ${r.seiten === 1 ? 'Seite' : 'Seiten'}, wie in der PDF`;
  const verstoss = r.regeln.concat(r.ueberlauf);
  $('#kt-umbruch').hidden = !verstoss.length; $('#kt-umbruch').textContent = verstoss.length ? 'Der Umbruch stimmt noch nicht: ' + verstoss[0] : '';
  if (MODUS === 'frei') $$('[data-k]', w.document).forEach(el => { el.setAttribute('contenteditable', 'plaintext-only'); if (el.contentEditable !== 'plaintext-only') el.setAttribute('contenteditable', 'true'); el.setAttribute('spellcheck', 'true'); if (GESCHRIEBEN.has(el.getAttribute('data-k'))) el.setAttribute('data-neu', '1'); });
  if (BLITZ && MODUS === 'einfach') {   // zur Seite mit dem geänderten Eintrag
    const s = r.wo.findIndex(x => x.teil === BLITZ[0] && x.i.includes(BLITZ[1])), blatt = $$('.kt-blatt', w.document)[s];
    if (blatt) sc.scrollTop = Math.max(0, blatt.getBoundingClientRect().top - w.document.documentElement.getBoundingClientRect().top - 10); else sc.scrollTop = oben;
    BLITZ = null;
  } else sc.scrollTop = oben;
  if (MODUS === 'frei') window.scrollTo(0, fensterOben);
}
async function neuPassen() { const w = await rahmen; if (!LETZTE) return; const m = w.KT_DRUCK.passe(vopt()); $('#kt-vorschau').style.height = m.hoehe + 'px'; }

// ---------------------------------------------------------------- Leiste
function leiste() {
  oben();
  const g = geaendert(), n = g ? vergleich(STAND.live, DOC).length : 0;
  $('#kt-leiste').innerHTML = `<div class="kt-leiste__t"><b>${OFFEN ? 'Nicht gespeicherte Änderungen' : g ? `<i class="marke">Entwurf</i>${n} ${n === 1 ? 'Änderung' : 'Änderungen'}` : 'Die PDF ist auf dem neuesten Stand.'}</b>
      <span>${OFFEN ? 'Speichern legt sie im Entwurf ab. Die PDF ändert sich erst beim Veröffentlichen.' : g ? 'Noch nicht in der PDF. <button class="kt-link" type="button" data-akt="verwerfen">Entwurf verwerfen</button>' : 'Jede Änderung wartet zuerst als Entwurf.'}</span></div>
    <button class="kn kn--klein kn--ohne" type="button" data-akt="vgl"${g ? '' : ' disabled'}>Vorher / nachher</button>
    <button class="kn kn--klein kn--ohne" type="button" data-akt="probe">Probe-PDF</button>
    <button class="kn kn--klein${OFFEN ? ' kt-gold' : GRUEN ? '' : ' kt-ruhig'}" type="button" data-akt="speichern">${OFFEN ? 'Speichern' : GRUEN ? 'Gespeichert' : 'Alles gespeichert'}<i>${GRUEN && !OFFEN ? SYM.haken : PF}</i></button>
    <button class="kn kt-gold" type="button" data-akt="veroeffentlichen"${g || OFFEN ? '' : ' disabled'}>Veröffentlichen<i>${PF}</i></button>`;
}
/* Vorschau: Karte oder Website. Die Website-Ansicht zeigt ehrlich, dass noch kein Haus angeschlossen ist. */
function ansicht() {
  const web = ANSICHT === 'website';
  $('#kt-seiten').hidden = web; $('#kt-web').hidden = !web; $('.kt-vorschau__z').hidden = web;
  $$('.kt-ansicht button').forEach(b => b.setAttribute('aria-pressed', b.dataset.ansicht === ANSICHT));
  if (web) $('#kt-vzahl').textContent = 'Website: noch nicht angeschlossen'; else vorschau();
}
function alles() { document.body.classList.toggle('kt-frei', MODUS === 'frei'); kleide(); rand(); kopf(); if (MODUS === 'einfach') liste(); ansicht(); leiste(); }

// ---------------------------------------------------------------- Speichern (immer als Entwurf, nie still)
function speichern(was, text, ohneUndo) { if (!laufend) laufend = schreibe(was, text, ohneUndo).finally(() => { laufend = null; }); return laufend; }
async function schreibe(was, text, ohneUndo) {
  const vorher = BASIS;
  if (GESCHRIEBEN.size) uebersetzungPruefen();
  let r;
  try { r = await ruf('PUT', `/api/x/karten/entwurf/${H()}`, { daten: DOC, erwartet: erwartet(), wer: wer() }); }
  catch (e) {
    if (e.status === 409) { konflikt(was || 'Ihre Eingaben'); return false; }
    sag('Nicht gespeichert', e.message + (e.stichwort ? ' (Stichwort: ' + e.stichwort + ')' : ''), [], true); return false;
  }
  STAND = r.stand; OFFEN = false; GESCHRIEBEN.clear();
  if (!r.geaendert) { sag('Nichts geändert, nichts gespeichert.'); leiste(); return true; }
  if (!ohneUndo) UNDO.push(vorher);
  BASIS = JSON.stringify(DOC);
  GRUEN = true; setTimeout(() => { GRUEN = false; if (!OFFEN && STAND) leiste(); }, 2600);
  rand(); leiste(); if (MODUS === 'einfach') liste(); else vorschau();
  sag(was || 'Im Entwurf gespeichert', text || 'Die PDF ändert sich erst beim Veröffentlichen.', (ohneUndo ? [] : [{ t: 'Rückgängig', f: rueckgaengig }]).concat(geaendert() ? [{ t: 'Vorher / nachher', f: vglFenster }] : []));
  ruf('GET', `/api/x/karten/uebersicht/${H()}`).then(u => { UEBER = u; }).catch(() => {});
  return true;
}
function uebersetzungPruefen() {   // Deutsch geschrieben, Englisch nicht: der Eintrag merkt sich «Englisch nachziehen»
  const je = new Map();
  GESCHRIEBEN.forEach(pfad => {
    const m = /^teile\.(\d+)\.posten\.(\d+)\.(.*)$/.exec(pfad); if (!m) return;
    const u = (D().teile[+m[1]].posten || [])[+m[2]]; if (!u) return;
    const z = /^zeilen\.(\d+)\.text$/.exec(m[3]), en = m[3] === 'en' || (z && u.zeilen[+z[1]] && u.zeilen[+z[1]].en), b = je.get(u) || { de: false, en: false };
    if (en) b.en = true; else if (!/^(preise|einheiten|koepfe|preis)/.test(m[3]) && !/\.preise\./.test(m[3])) b.de = true;
    je.set(u, b);
  });
  je.forEach((b, u) => { const hatEn = (typeof u.en === 'string' && u.en) || (u.zeilen || []).some(z => z.en); if (b.en) delete u.uebersetzung; else if (b.de && hatEn) u.uebersetzung = 'offen'; });
}
async function rueckgaengig() {
  if (!UNDO.length) return sag('Nichts zum Zurücknehmen.');
  DOC = JSON.parse(UNDO.pop());
  if (await speichern('Zurückgenommen', 'Der Entwurf steht wieder wie vor der letzten Änderung.', true)) alles();
}
async function tun(fn, was, text, blitz) {   // Änderung im Weg Einfach: anwenden, sofort speichern, neu zeichnen
  const alt = JSON.stringify(DOC);
  if (fn() === false || JSON.stringify(DOC) === alt) { DOC = JSON.parse(alt); return sag('Nichts geändert, nichts gespeichert.'); }
  BLITZ = blitz || null;
  liste(); vorschau();
  if (!(await speichern(was, text))) { DOC = JSON.parse(alt); if (STAND) alles(); return false; }   // nicht gespeichert: zurück zum Stand davor
  return true;
}
function konflikt(was) {
  fenster(`<h2>Nicht <em>gespeichert.</em></h2><p class="kt-satz">Inzwischen hat jemand anderes gespeichert. Ihre Änderung («${h(was)}») wurde nicht gespeichert und nichts wurde überschrieben. Laden Sie den neuen Stand und nehmen Sie Ihre Änderung dort noch einmal vor.</p>
    <p class="kt-mono">Stichwort: konflikt</p><div class="kt-fenster__kn"><button class="kn kn--d" type="button" id="k-neu">Neuen Stand laden<i>${PF}</i></button></div>`, true);
  $('#kt-fenster').onclick = null;
  $('#k-neu').addEventListener('click', async () => { zu(); try { await lade(Z, true); sag('Der neue Stand ist geladen.'); } catch (e) { sag('Nicht geladen', e.message, [], true); } });
}

// ---------------------------------------------------------------- Fenster
function fenster(html, schmal) {
  const f = $('#kt-fenster');
  f.innerHTML = `<div class="kt-fenster__k${schmal ? ' kt-schmal' : ''}" role="dialog" aria-modal="true"><button class="kt-rund kt-fenster__zu" type="button" data-zu aria-label="Schliessen">${SYM.zu}</button>${html}</div>`;
  f.hidden = false; f.oninput = null;
  f.onclick = ev => { if (ev.target === f || ev.target.closest('[data-zu]')) zu(); };
  const erst = $('input:not([readonly]),textarea', f) || $('.kt-fenster__kn button', f); if (erst) setTimeout(() => erst.focus(), 30);
}
function zu() { const f = $('#kt-fenster'); f.hidden = true; f.innerHTML = ''; f.oninput = null; f.onclick = null; miniLos = null; }
function frage(titel, text, ja, f) {
  fenster(`<h2>${titel}</h2><p class="kt-satz">${h(text)}</p><div class="kt-fenster__kn"><button class="kn kn--klein kn--ohne" type="button" data-zu>Abbrechen</button><button class="kn kn--d" type="button" id="ja">${h(ja)}<i>${PF}</i></button></div>`, true);
  $('#ja').addEventListener('click', () => { zu(); f(); });
}
/* ein Eintrag so, wie er auf der Karte steht: derselbe Satz, in der Welt des Hauses */
function miniFeld() { const los = new Promise(r => { miniLos = r; }); miniFeld.los = los; return '<p class="kt-mono">So steht es auf der Karte</p><div class="kt-mini"><iframe id="kt-mini" title="So steht es auf der Karte" src="druck.html"></iframe></div>'; }
async function mini(u) {
  const los = miniFeld.los, w = await los, f = $('#kt-mini'); if (!f || miniFeld.los !== los) return;
  try { const m = await w.KT_DRUCK.mini(D(), u, { ...kopt(), breite: f.clientWidth, massstab: 0.62 }); if ($('#kt-mini') === f) f.style.height = Math.max(40, m.hoehe) + 'px'; } catch (e) { /* die Vorschau im Fenster ist Zugabe */ }
}
const feld = (id, titel, wert, hilfe = '', mehr = false) => `<div class="feld"><label for="${id}">${h(titel)}</label>${mehr ? `<textarea id="${id}" rows="2" spellcheck="true">${h(wert)}</textarea>` : `<input id="${id}" type="text" autocomplete="off" value="${h(wert)}">`}${hilfe ? `<small>${hilfe}</small>` : ''}</div>`;
const v = id => { const el = $('#' + id); return el ? el.value : ''; };
const zeilenAus = id => v(id).split('\n').map(sauber).filter(Boolean);

/* Eintrag bearbeiten oder neu anlegen. ort: { ti, i } (bearbeiten) oder { ti, nach } (neu nach Index, -1 = ganz oben) */
function eintragFenster(ort) {
  const neu = ort.i === undefined;
  const p = teile()[ort.ti].posten;
  const u0 = neu ? null : kopie(p[ort.i]);
  let u = neu ? null : kopie(p[ort.i]);
  let art = neu ? (ort.art || vermutlich(ort.ti, ort.nach)) : u.t;
  if (neu) u = leer(art);
  const stelle = neu ? Math.max(ort.nach, 0) : ort.i;
  const rub = rubrikVon(ort.ti, stelle), koepfe = koepfeFuer(ort.ti, stelle), np = nachbarPreise(ort.ti, stelle);
  const arten = neu ? ['gericht', 'zeile', 'notiz', 'land'] : [art];
  let mitAngabe = !!(u.einheiten || []).some(Boolean), allergeneAuf = !!(u.allergene || []).length;
  const tafel = () => koepfe && (!(u.preise || []).length || u.preise.length === koepfe.length);
  const preisFelder = () => {
    if (tafel()) return `<div class="kt-preise" data-tafel="1"><p class="kt-klein">Diese Rubrik hat feste Spalten. Ein leeres Feld bleibt auf der Karte leer.</p>${koepfe.map((k, n) => `<div class="kt-preis kt-preis--tafel"><div class="feld"><span>Spalte</span><input type="text" value="${h(k)}" readonly tabindex="-1" aria-label="Spalte"></div><div class="feld"><label for="f-p${n}">Preis</label><input id="f-p${n}" data-preis type="text" inputmode="decimal" autocomplete="off" value="${h((u.preise || [])[n] || '')}"></div></div>`).join('')}</div>`;
    const pr = (u.preise || []).length ? u.preise : [''], ein = u.einheiten || [];
    return `<div class="kt-preise" id="f-preise">${pr.map((x, n) => `<div class="kt-preis"><div class="feld"><label for="f-e${n}">Angabe zum Preis</label><input id="f-e${n}" data-einheit type="text" autocomplete="off" value="${h(ein[n] || '')}"></div><div class="feld"><label for="f-p${n}">Preis</label><input id="f-p${n}" data-preis type="text" inputmode="decimal" autocomplete="off" value="${h(x)}"></div><button type="button" class="kt-rund" data-preis-weg aria-label="Diesen Preis entfernen">${SYM.zu}</button></div>`).join('')}
      <p class="kt-klein">Beim Preis genügt die Zahl: «9» wird zu «${h(preisForm('9', np))}». Die Angabe ist freiwillig, zum Beispiel «33cl» oder «Portion».</p><div><button type="button" class="kt-link" id="f-preis-dazu">Weiterer Preis</button></div></div>`;
  };
  const felder = () => {
    if (art === 'gericht') {
      const de = (u.zeilen || []).filter(z => !z.en && !(z.preise || []).length).map(z => z.text).join('\n'), en = (u.zeilen || []).filter(z => z.en).map(z => z.text).join('\n');
      const mp = (u.zeilen || []).some(z => (z.preise || []).length), strukt = mitAngabe || tafel();
      return feld('f-name', 'Name', u.name) + (strukt ? feld('f-zusatz', 'Zusatz hinter dem Namen', u.zusatz || '', 'Klein gesetzt. Darf leer bleiben.') + preisFelder()
        : `<div class="kt-zw2">${feld('f-zusatz', 'Zusatz hinter dem Namen', u.zusatz || '', 'Klein, z. B. «4cl» oder «1 dl.». Darf leer bleiben.')}${feld('f-preis', 'Preis', (u.preise || []).join(' · '), 'Mehrere Preise mit · trennen. «18» wird zu «' + h(preisForm('18', np)) + '». <button type="button" class="kt-link" id="f-mit-angabe">Preis mit Angabe («33cl», «Portion»)</button>')}</div>`)
        + feld('f-de', 'Beschreibung', de, 'Zutaten oder Herkunft, wie auf der Karte. Eine neue Zeile mit Enter.', true)
        + feld('f-en', 'Englisch', en, u.uebersetzung === 'offen' ? 'Die deutsche Zeile wurde geändert, die englische noch nicht. Bitte nachziehen oder unten bestätigen.' : 'Steht etwas heller darunter.', true)
        + (mp ? '<p class="kt-klein">Dieser Eintrag hat Zeilen mit eigenem Preis. Die ändern Sie im Weg «Fortgeschritten» direkt in der Karte.</p>' : '')
        + (allergeneAuf ? `<div class="feld"><span>Allergene (erscheinen unter dem Gericht)</span><div class="kt-chips" id="f-allergene">${Object.entries(UEBER.allergene).map(([k, w]) => `<button type="button" data-al="${h(k)}" aria-pressed="${(u.allergene || []).includes(k)}">${h(w)}</button>`).join('')}</div></div>` : '<p><button type="button" class="kt-link" id="f-al-auf">Allergene angeben</button></p>');
    }
    if (art === 'zeile') return feld('f-name', 'Name', u.name, 'So, wie es in der Zeile steht, mit Herkunft oder Prozent.') + feld('f-preis', 'Preis', u.preis || '', 'Nur die Zahl genügt. «9» wird zu «' + h(preisForm('9', np)) + '».');
    if (art === 'rubrik') return feld('f-titel', 'Titel', u.titel) + feld('f-en', 'Englisch', u.en || '', 'Steht kleiner unter dem Titel. Darf leer bleiben.') + feld('f-zusatz', 'Zusatz', u.zusatz || '', 'Zum Beispiel «ab 2 Personen». Darf leer bleiben.')
      + ((u.koepfe || []).length ? feld('f-koepfe', 'Spaltenköpfe', u.koepfe.join('\n'), 'Je Zeile ein Kopf. Die Zahl der Köpfe bleibt gleich.', true) : '');
    if (art === 'frei') return feld('f-zeilen', 'Text', (u.zeilen || []).map(z => z.text).join('\n'), 'Jede Zeile hier ist eine Zeile auf der Karte.', true)
      + ((u.zeilen || []).some(z => (z.preise || []).length) ? '<p class="kt-klein">Dieser Block hat Zeilen mit eigenem Preis. Die Preise ändern Sie im Weg «Fortgeschritten» direkt in der Karte.</p>' : '');
    if (art === 'notiz') return feld('f-text', 'Hinweis', u.text, '', true) + `<div class="feld"><span>Sprache</span><div class="kt-chips" id="f-sprache"><button type="button" data-sp="de" aria-pressed="${!u.en}">Deutsch (normal)</button><button type="button" data-sp="en" aria-pressed="${!!u.en}">Englisch (heller)</button></div></div>`;
    return feld('f-text', ART[art], u.text) + ((u.koepfe || []).length ? feld('f-koepfe', 'Spaltenköpfe', u.koepfe.join('\n'), 'Je Zeile ein Kopf. Die Zahl der Köpfe bleibt gleich.', true) : '');
  };
  const lese = () => {
    const x = kopie(u);
    if ($('#f-koepfe')) x.koepfe = zeilenAus('f-koepfe');
    if (art === 'gericht') {
      x.name = sauber(v('f-name')); const zs = sauber(v('f-zusatz')); if (zs) x.zusatz = zs; else delete x.zusatz;
      const alt = u.zeilen || [], deA = alt.filter(z => !z.en && !(z.preise || []).length).map(z => z.text), enA = alt.filter(z => z.en).map(z => z.text), de = zeilenAus('f-de'), en = zeilenAus('f-en');
      if (de.join('\n') !== deA.join('\n') || en.join('\n') !== enA.join('\n')) x.zeilen = alt.filter(z => (z.preise || []).length).concat(de.map(text => ({ text })), en.map(text => ({ text, en: true })));
      if ($('#f-preis')) { x.preise = v('f-preis').split(/\s*[·|]\s*/).map(sauber).filter(Boolean).map(t => preisForm(t, np)); delete x.einheiten; }
      else if ($('[data-tafel]', $('#kt-fenster'))) { x.preise = $$('#kt-fenster [data-preis]').map(e => preisForm(e.value, np)); delete x.einheiten; }
      else { const paare = $$('#kt-fenster .kt-preis').map(z => [preisForm($('[data-preis]', z).value, np), sauber($('[data-einheit]', z).value)]).filter(a => a[0]); x.preise = paare.map(a => a[0]); if (paare.some(a => a[1])) x.einheiten = paare.map(a => a[1]); else delete x.einheiten; }
      if ($('#f-allergene')) { const al = $$('#f-allergene [aria-pressed="true"]').map(b => b.dataset.al); if (al.length) x.allergene = al; else delete x.allergene; }
      if (!neu) { const deAnders = x.name !== u0.name || (x.zusatz || '') !== (u0.zusatz || '') || de.join('\n') !== (u0.zeilen || []).filter(z => !z.en && !(z.preise || []).length).map(z => z.text).join('\n'), enAnders = en.join('\n') !== (u0.zeilen || []).filter(z => z.en).map(z => z.text).join('\n');
        if (enAnders) delete x.uebersetzung; else if (deAnders && en.length) x.uebersetzung = 'offen'; else if (u0.uebersetzung) x.uebersetzung = u0.uebersetzung; else delete x.uebersetzung; }
      return x;
    }
    if (art === 'zeile') { x.name = sauber(v('f-name')); x.preis = preisForm(v('f-preis'), np); return x; }
    if (art === 'rubrik') { x.titel = sauber(v('f-titel')); x.en = sauber(v('f-en')); const zs = sauber(v('f-zusatz')); if (zs) x.zusatz = zs; else delete x.zusatz;
      if (!neu) { if (x.en !== (u0.en || '')) delete x.uebersetzung; else if (x.titel !== u0.titel && x.en) x.uebersetzung = 'offen'; } return x; }
    if (art === 'frei') { x.zeilen = zeilenAus('f-zeilen').map((text, n) => Object.assign({}, (u.zeilen || [])[n] || {}, { text })); return x; }
    if (art === 'notiz') { x.text = sauber(v('f-text')); const en = ($('#f-sprache [aria-pressed="true"]') || {}).dataset; if (en && en.sp === 'en') x.en = true; else delete x.en; return x; }
    x.text = sauber(v('f-text')); return x;
  };
  const zeichne = () => {
    fenster(`<h2>${neu ? 'Neu auf <em>die Karte.</em>' : `${ART[art]} <em>bearbeiten.</em>`}</h2>
      <p class="kt-satz">${rub ? `Rubrik «${h(rub.titel)}»` : 'Am Anfang der Karte'}. Rechts steht der Eintrag so, wie er in der PDF erscheint.</p>
      ${neu ? `<div class="feld"><span>Art</span><div class="kt-chips" id="f-art">${arten.map(a => `<button type="button" data-a="${a}" aria-pressed="${a === art}">${ART[a]}</button>`).join('')}</div></div>` : ''}
      <div class="kt-zwei"><div id="f-felder">${felder()}</div><div>${miniFeld()}
        ${neu || ['rubrik', 'zw', 'land', 'kopf'].includes(art) ? '' : `<button type="button" class="kt-schalter" id="f-aus" role="switch" aria-checked="${!u.aus}"><i>${SYM.haken}</i>Auf der Karte zeigen</button>`}</div></div>
      <p class="kt-fehler" id="f-fehler" role="alert"></p>
      <div class="kt-fenster__kn">${neu ? '' : '<button class="kt-link" type="button" id="f-weg">Von der Karte nehmen</button>'}${!neu && u.uebersetzung === 'offen' ? '<button class="kt-link" type="button" id="f-en-ok" style="margin-inline-end:0">Englisch stimmt so</button>' : ''}<button class="kn kn--klein kn--ohne" type="button" data-zu>Abbrechen</button><button class="kn kn--d" type="button" id="f-ok">${neu ? 'Auf die Karte setzen' : 'Speichern'}<i>${PF}</i></button></div>`);
    const f = $('#kt-fenster');
    const frisch = () => { const aus = $('#f-aus'); u = lese(); if (aus && aus.getAttribute('aria-checked') !== 'true') u.aus = true; else delete u.aus; mini(u); $('#f-fehler').textContent = ''; };
    f.oninput = frisch;
    mini(u);
    const schliessen = f.onclick;    // ein einziger Klick-Weg je Fenster (kein addEventListener: das Fenster wird öfter neu gezeichnet)
    f.onclick = ev => {
      schliessen(ev);
      const b = ev.target.closest('button'); if (!b || !f.contains(b) || f.hidden) return;
      if (b.dataset.a) { art = b.dataset.a; u = leer(art); mitAngabe = false; allergeneAuf = false; return zeichne(); }
      if (b.id === 'f-mit-angabe') { u = lese(); mitAngabe = true; return zeichne(); }
      if (b.id === 'f-al-auf') { u = lese(); allergeneAuf = true; return zeichne(); }
      if (b.id === 'f-preis-dazu') { u = lese(); u.preise = (u.preise || []).concat(['']); if (u.einheiten) u.einheiten.push(''); mitAngabe = true; zeichne(); const l = $$('#kt-fenster [data-einheit]').pop(); if (l) setTimeout(() => l.focus(), 40); return; }
      if (b.hasAttribute('data-preis-weg')) { const z = b.closest('.kt-preis'); if ($$('#f-preise .kt-preis').length > 1) z.remove(); else $$('input', z).forEach(i => { i.value = ''; }); return frisch(); }
      if (b.dataset.al) { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); return frisch(); }
      if (b.dataset.sp) { $$('#f-sprache button').forEach(x => x.setAttribute('aria-pressed', x === b)); return frisch(); }
      if (b.id === 'f-aus') { b.setAttribute('aria-checked', b.getAttribute('aria-checked') !== 'true'); return frisch(); }
      if (b.id === 'f-weg') return entfernen(ort.ti, ort.i);
      if (b.id === 'f-en-ok') { zu(); return tun(() => { delete p[ort.i].uebersetzung; }, 'Englisch bestätigt', `«${nameVon(u0)}»`, [ort.ti, ort.i]); }
      if (b.id !== 'f-ok') return;
      const x = lese(), aus = $('#f-aus'); if (aus && aus.getAttribute('aria-checked') !== 'true') x.aus = true; else delete x.aus;
      const fehlt = (art === 'gericht' || art === 'zeile') && !x.name ? 'Bitte einen Namen eintragen.' : art === 'rubrik' && !x.titel ? 'Bitte einen Titel eintragen.' : (['notiz', 'land', 'zw', 'kopf'].includes(art) && !x.text) ? 'Bitte einen Text eintragen.'
        : art === 'frei' && !x.zeilen.length ? 'Bitte einen Text eintragen.' : (u0 && (u0.koepfe || []).length && (x.koepfe || []).length !== u0.koepfe.length) ? `Es müssen ${u0.koepfe.length} Spaltenköpfe bleiben, je Zeile einer.` : '';
      if (fehlt) { $('#f-fehler').textContent = fehlt; return; }
      if (!neu && JSON.stringify(x) === JSON.stringify(p[ort.i])) { zu(); return sag('Nichts geändert, nichts gespeichert.'); }
      zu();
      const name = nameVon(x);
      if (neu) { x.s = (p[Math.max(ort.nach, 0)] || {}).s || 1; tun(() => { p.splice(ort.nach + 1, 0, x); }, `${ART[art]} auf der Karte`, `«${name}» steht jetzt im Entwurf.`, [ort.ti, ort.nach + 1]); }
      else { const pa = preisText(u0), pn = preisText(x); tun(() => { p[ort.i] = x; }, `${ART[art]} gespeichert`, pa !== pn ? `«${name}»: Preis ${pa || 'leer'} → ${pn || 'leer'}` : `«${name}»`, [ort.ti, ort.i]); }
    };
  };
  zeichne();
}
function leer(art) { return art === 'gericht' ? { t: 'gericht', name: '', zeilen: [], preise: [] } : art === 'zeile' ? { t: 'zeile', name: '', preis: '' } : art === 'rubrik' ? { t: 'rubrik', titel: '', en: '' } : art === 'frei' ? { t: 'frei', zeilen: [] } : art === 'notiz' ? { t: 'notiz', text: '' } : { t: art, text: '' }; }
function vermutlich(ti, nach) {   // was in diesem Abschnitt üblich ist: Zeilen in Tafeln, sonst Gerichte
  const p = teile()[ti].posten;
  for (let j = Math.max(nach, 0); j < p.length && j <= nach + 3; j++) if (p[j] && (p[j].t === 'zeile' || p[j].t === 'gericht')) return p[j].t;
  for (let j = Math.min(nach, p.length - 1); j >= 0; j--) if (p[j].t === 'zeile' || p[j].t === 'gericht') return p[j].t;
  return 'gericht';
}
function deckelFenster(ti) {
  const t = teile()[ti];
  fenster(`<h2>Deckblatt <em>ändern.</em></h2><p class="kt-satz">Titel und Zweitzeile auf dem dunklen Deckblatt. Weitere Zeilen stehen klein darunter.</p>
    ${feld('d-t', 'Titel', t.titel)}${feld('d-u', 'Zweitzeile', t.unter || '')}${feld('d-z', 'Weitere Zeilen', (t.zeilen || []).join('\n'), 'Eine Zeile je Absatz.', true)}
    <p class="kt-fehler" id="d-f" role="alert"></p><div class="kt-fenster__kn"><button class="kn kn--klein kn--ohne" type="button" data-zu>Abbrechen</button><button class="kn kn--d" type="button" id="d-ok">Speichern<i>${PF}</i></button></div>`, true);
  $('#d-ok').addEventListener('click', () => {
    const titel = sauber(v('d-t')), unter = sauber(v('d-u')), zl = zeilenAus('d-z'); if (!titel) { $('#d-f').textContent = 'Das Deckblatt braucht einen Titel.'; return; }
    zu(); tun(() => { t.titel = titel; t.unter = unter; t.zeilen = zl; }, 'Deckblatt gespeichert', titel);
  });
}
function karteFenster() {
  const e = eintrag(), k = e.karte;
  fenster(`<h2>Karte <em>einrichten.</em></h2><p class="kt-satz">Von wann bis wann diese Karte gilt, und was unten auf jeder Innenseite steht. Der Zeitraum steht nicht auf der gedruckten Karte.</p>
    <div class="kt-zw2">${feld('k-von', 'Gilt von', datumText(e.gilt.von), 'Tag.Monat.Jahr, z. B. 01.05.2027. Darf leer bleiben.')}${feld('k-bis', 'Gilt bis', datumText(e.gilt.bis), 'Darf leer bleiben.')}</div>
    ${feld('k-fuss', 'Fusszeile auf jeder Innenseite', k.fuss || '', 'Zum Beispiel der Hinweis zu Preisen und Mehrwertsteuer. Darf leer bleiben.', true)}
    <p class="kt-fehler" id="k-f" role="alert"></p><div class="kt-fenster__kn"><button class="kn kn--klein kn--ohne" type="button" data-zu>Abbrechen</button><button class="kn kn--d" type="button" id="k-ok">Speichern<i>${PF}</i></button></div>`, true);
  $('#k-ok').addEventListener('click', () => {
    const von = datumLesen(v('k-von')), bis = datumLesen(v('k-bis')), fuss = sauber(v('k-fuss'));
    if (von === null || bis === null) { $('#k-f').textContent = 'Bitte das Datum als Tag.Monat.Jahr schreiben, zum Beispiel 01.05.2027.'; return; }
    if (von && bis && von > bis) { $('#k-f').textContent = '«Gilt bis» liegt vor «Gilt von».'; return; }
    zu(); tun(() => { e.gilt = { von, bis }; k.fuss = fuss; }, 'Karte eingerichtet', kurzname(k.name));
  });
}
function rubrikNeu(ti, nach) {
  fenster(`<h2>Neue <em>Rubrik.</em></h2><p class="kt-satz">Zum Beispiel «Für Kinder» oder «Raritäten». Danach legen Sie die Einträge darunter an. Auf der gedruckten Karte erscheint die Rubrik, sobald ein Eintrag darin steht.</p>
    ${feld('r-t', 'Titel', '')}${feld('r-e', 'Englisch', '', 'Darf leer bleiben.')}
    <p class="kt-fehler" id="r-f" role="alert"></p><div class="kt-fenster__kn"><button class="kn kn--klein kn--ohne" type="button" data-zu>Abbrechen</button><button class="kn kn--d" type="button" id="r-ok">Anlegen<i>${PF}</i></button></div>`, true);
  $('#r-ok').addEventListener('click', () => {
    const titel = sauber(v('r-t')), en = sauber(v('r-e')); if (!titel) { $('#r-f').textContent = 'Bitte einen Titel eintragen.'; return; }
    const p = teile()[ti].posten, at = nach === undefined ? p.length : nach;
    zu(); tun(() => { p.splice(at, 0, { t: 'rubrik', titel, en, s: (p[at - 1] || p[0] || {}).s || 1 }); }, 'Rubrik angelegt', `«${titel}». Jetzt Einträge darunter hinzufügen.`, [ti, at]);
  });
}
function entfernen(ti, i) {   // wie im Original: mit Rückfrage; bis zum Veröffentlichen kommt alles mit «Rückgängig» zurück, danach über «Frühere Fassungen»
  const p = teile()[ti].posten, u = p[i];
  if (u.t === 'rubrik') {
    const b = bloecke(ti).find(x => x[0] === i), n = b ? b[1] - b[0] - 1 : 0;
    return frage('Rubrik <em>entfernen?</em>', n ? `«${u.titel}» und die ${n} Einträge darunter verschwinden aus der Karte. Bis zum Veröffentlichen holen Sie alles mit «Rückgängig» oder «Entwurf verwerfen» zurück.` : `«${u.titel}» verschwindet aus der Karte.`, 'Entfernen',
      () => tun(() => { p.splice(i, b ? b[1] - b[0] : 1); }, 'Rubrik entfernt', u.titel));
  }
  const name = nameVon(u) || 'Eintrag';
  frage('Von der Karte <em>nehmen?</em>', `«${name}» verschwindet aus der Karte. Wenn es nur vorübergehend ist, blenden Sie es lieber aus (Auge). Bis zum Veröffentlichen lässt es sich zurückholen.`, 'Von der Karte nehmen',
    () => tun(() => { p.splice(i, 1); }, 'Von der Karte genommen', name));
}
function blende(ti, i) {   // ausblenden statt löschen; eine Rubrik nimmt ihre Einträge mit
  const p = teile()[ti].posten, u = p[i], wird = !u.aus;
  const b = u.t === 'rubrik' ? bloecke(ti).find(x => x[0] === i) : null, bis = b ? b[1] : i + 1;
  tun(() => { for (let j = i; j < bis; j++) { if (wird) p[j].aus = true; else delete p[j].aus; } }, wird ? 'Ausgeblendet' : 'Wieder auf der Karte',
    u.t === 'rubrik' ? `Rubrik «${u.titel}» mit ihren ${bis - i - 1} Einträgen ${wird ? 'steht vorerst nicht in der PDF' : ''}`.trim() : wird ? `«${nameVon(u)}» steht vorerst nicht in der PDF.` : `«${nameVon(u)}»`, [ti, i]);
}
function schiebe(ti, i, r) {
  const p = teile()[ti].posten, u = p[i];
  if (u.t === 'rubrik') {   // ganze Rubrik mit ihren Einträgen gegen die Nachbar-Rubrik tauschen
    const b = bloecke(ti), k = b.findIndex(x => x[0] === i), n = b[k + r];
    if (!n) return sag('Weiter geht es nicht.', r < 0 ? 'Diese Rubrik steht schon ganz oben.' : 'Diese Rubrik steht schon ganz unten.');
    const [a, c] = r < 0 ? [n, b[k]] : [b[k], n];
    return tun(() => { const vorn = p.slice(a[0], a[1]), hinten = p.slice(c[0], c[1]); p.splice(a[0], c[1] - a[0], ...hinten, ...vorn); }, 'Reihenfolge gespeichert', `«${u.titel}» steht jetzt weiter ${r < 0 ? 'oben' : 'unten'}`, [ti, r < 0 ? a[0] : a[0] + (c[1] - c[0])]);
  }
  const j = i + r; if (j < 0 || j >= p.length) return sag('Weiter geht es nicht.', r < 0 ? 'Dieser Eintrag steht schon ganz oben.' : 'Dieser Eintrag steht schon ganz unten.');
  tun(() => { [p[i], p[j]] = [p[j], p[i]]; }, 'Reihenfolge gespeichert', `«${nameVon(u)}» steht jetzt weiter ${r < 0 ? 'oben' : 'unten'}`, [ti, j]);
}
function neuGlobal() {
  const opts = [];
  teile().forEach((t, ti) => { if (t.art !== 'inhalt') return; t.posten.forEach((u, i) => { if (u.t === 'rubrik') opts.push([ti, i, u.titel]); }); });
  if (!opts.length) { const ti = teile().findIndex(t => t.art === 'inhalt'); return eintragFenster({ ti, nach: teile()[ti].posten.length - 1 }); }
  fenster(`<h2>Neuer <em>Eintrag.</em></h2><p class="kt-satz">In welche Rubrik? Der Eintrag kommt an ihr Ende, verschieben lässt er sich danach mit den Pfeilen.</p>
    <div class="kt-chips" id="g-r" style="margin-bottom:6px">${opts.map(([ti, i, t], k) => `<button type="button" data-k="${k}" aria-pressed="false">${h(t)}</button>`).join('')}</div>`, false);
  $('#g-r').addEventListener('click', ev => { const b = ev.target.closest('[data-k]'); if (!b) return; const [ti, i] = opts[+b.dataset.k]; const bl = bloecke(ti).find(x => x[0] === i); eintragFenster({ ti, nach: (bl ? bl[1] : i + 1) - 1 }); });
}

// ---------------------------------------------------------------- Vorher / nachher, Verlauf, Daten
function text(u) {
  if (!u) return '';
  const chip = u.aus ? '<br><i class="kt-chip" style="margin:4px 0 0">Ausgeblendet</i>' : '';
  if (u.t === 'gericht' || u.t === 'frei') return `${u.name ? `<b>${h(u.name)}${u.zusatz ? ' <small>' + h(u.zusatz) + '</small>' : ''}</b>` : ''}${(u.zeilen || []).map(z => z.en ? `<em>${h(z.text)}</em>` : `<span>${h(z.text)}${(z.preise || []).length ? ' · ' + h(z.preise.join(' · ')) : ''}</span><br>`).join('')}${(u.preise || []).length ? `<span class="zahl">${h(preisText(u))}</span>` : ''}${(u.allergene || []).length ? `<em>Enthält: ${h(u.allergene.map(a => UEBER.allergene[a] || a).join(', '))}</em>` : ''}${u.uebersetzung === 'offen' ? '<em>Englisch noch nachzuziehen</em>' : ''}${chip}`;
  if (u.t === 'zeile') return `<b>${h(u.name)}</b><span class="zahl">${h(u.preis)}</span>${chip}`;
  if (u.t === 'rubrik') return `<b>${h(u.titel)}</b>${u.en ? `<em>${h(u.en)}</em>` : ''}${u.zusatz ? `<em>${h(u.zusatz)}</em>` : ''}${(u.koepfe || []).length ? `<span class="zahl">${h(u.koepfe.join(' · '))}</span>` : ''}${chip}`;
  if (u.t === 'deckel') return `<b>${h(u.titel)}</b><em>${h(u.unter || '')}</em>${(u.zeilen || []).map(x => `<span>${h(x)}</span>`).join('<br>')}`;
  return `<span>${h(u.text)}</span>${(u.koepfe || []).length ? `<br><span class="zahl">${h(u.koepfe.join(' · '))}</span>` : ''}${chip}`;
}
function markiere(a, b) {   // gleiche Wörter normal, andere hervorgehoben
  const wa = new Set(a.replace(/<[^>]+>/g, ' ').split(/\s+/));
  return b.replace(/>([^<]+)</g, (m, t) => '>' + t.split(/(\s+)/).map(w => w.trim() && !wa.has(w) ? `<mark>${w}</mark>` : w).join('') + '<');
}
function vglHTML(liste, links, rechts) {
  const W = { neu: 'Neu', weg: 'Entfernt', anders: 'Geändert', verschoben: 'Verschoben' };
  const mehrere = new Set(liste.map(x => x.kid)).size > 1 || DOC.karten.length > 1;
  return `<div class="kt-vgl__k"><span></span><span class="kt-mono">${links}</span><span class="kt-mono">${rechts}</span></div>
    <div class="kt-vgl">${liste.map(x => { const a = x.a ? text(x.a.u) : '', b = x.b ? text(x.b.u) : ''; return `<div class="kt-vgl__z"><span class="kt-mono">${W[x.art]}<small>${h([mehrere ? x.karte : '', (x.b || x.a).ort || ''].filter(Boolean).join(' · '))}</small></span><div class="${a ? '' : 'kt-leer'}">${a ? (x.art === 'weg' ? `<del>${a}</del>` : a) : 'stand noch nicht da'}</div><div class="${b ? '' : 'kt-leer'}">${b ? (x.art === 'anders' ? markiere('>' + a + '<', '>' + b + '<').slice(1, -1) : b) : 'nicht mehr auf der Karte'}</div></div>`; }).join('')}</div>`;
}
function vglFenster() {
  const l = vergleich(STAND.live, DOC);
  const offenEn = []; DOC.karten.forEach(e => e.karte.teile.forEach(t => (t.posten || []).forEach(u => { if (u.uebersetzung === 'offen' && !u.aus) offenEn.push(nameVon(u)); })));
  const fass = DOC.karten.flatMap(e => karteAnders(e.id) ? Object.keys(e.fassungen || {}).map(sp => kurzname(e.karte.name) + ' ' + sp.toUpperCase()) : []);
  fenster(`<h2>Vorher <em>und nachher.</em></h2><p class="kt-satz">${l.length ? `${l.length} ${l.length === 1 ? 'Stelle' : 'Stellen'} im Entwurf. Links steht, was heute in der PDF steht, rechts der Entwurf. Was neu ist, ist markiert.` : 'Der Entwurf ist gleich wie die PDF.'}</p>
    ${vglHTML(l, 'Heute in der PDF', 'Im Entwurf')}
    ${offenEn.length ? `<p class="kt-klein" id="v-en" style="margin-top:16px">Englisch ist bei ${offenEn.length} ${offenEn.length === 1 ? 'Eintrag' : 'Einträgen'} noch nicht nachgezogen: ${h(offenEn.slice(0, 6).join(', '))}${offenEn.length > 6 ? ' …' : ''}. Die Karte erscheint dort mit der bisherigen englischen Zeile.</p>` : ''}
    ${fass.length ? `<p class="kt-klein" id="v-fass" style="margin-top:16px">Sprachfassungen (${h(fass.join(', '))}) werden nicht mit geändert. Sie zeigen danach einen früheren Stand, bis sie nachgezogen sind.</p>` : ''}
    ${l.length ? `<div class="kt-zw2" style="margin-top:22px">${feld('v-wer', 'Ihr Name', wer(), 'Steht bei der Fassung im Verlauf. Darf leer bleiben.')}${feld('v-notiz', 'Notiz für den Verlauf', '', 'Zum Beispiel «Preise Herbst». Darf leer bleiben.')}</div>` : ''}
    <div class="kt-fenster__kn"><button class="kn kn--klein kn--ohne" type="button" data-zu>Schliessen</button>${l.length ? `<button class="kn kn--d" type="button" id="v-ok">Veröffentlichen<i>${PF}</i></button>` : ''}</div>`);
  const ok = $('#v-ok'); if (ok) ok.addEventListener('click', () => veroeffentlichen(sauber(v('v-wer')), sauber(v('v-notiz'))));
}
async function verlaufFenster() {
  let l = [], p = [];
  try { [l, p] = await Promise.all([ruf('GET', `/api/verlauf/${H()}/karten`), ruf('GET', `/api/protokoll/${H()}/karten`)]); } catch (e) { return sag('Verlauf nicht lesbar', e.message, [], true); }
  const was = { grundstand: 'Erster Stand eingelesen', entwurf: 'Entwurf gespeichert', verworfen: 'Entwurf verworfen', veroeffentlicht: 'Veröffentlicht', zurueckgeholt: 'Frühere Fassung in den Entwurf geholt', 'aus-sicherung': 'Aus der Sicherung wiederhergestellt' };
  fenster(`<h2>Frühere <em>Fassungen.</em></h2><p class="kt-satz">Jede veröffentlichte Fassung bleibt aufbewahrt. Eine Fassung zurückholen legt sie in den Entwurf; die PDF ändert sich erst beim Veröffentlichen. Die Fassungen gelten für alle Karten des Hauses zusammen.</p>
    <div class="kt-verlauf" id="vl">${l.length ? l.map(x => `<div class="kt-verlauf__z" data-fassung="${h(x.fassung)}"><div><b>Stand bis ${h(zeitText(x.abgeloest))}</b><p class="kt-mono">abgelöst${x.wer ? ' von ' + h(x.wer) : ''}${x.notiz ? ' · «' + h(x.notiz) + '»' : ''}</p></div><div class="kt-verlauf__kn"><button class="kt-link" type="button" data-sehen>Ansehen</button><button class="kn kn--klein kn--ohne" type="button" data-d>In den Entwurf holen</button></div></div>`).join('') : '<p>Noch keine früheren Fassungen. Die erste entsteht beim ersten Veröffentlichen.</p>'}</div>
    <p class="kt-mono" style="margin-top:24px">Was zuletzt geschah</p><div class="kt-verlauf">${p.slice(0, 8).map(z => `<div class="kt-verlauf__z"><div><b>${h(was[z.was] || z.was)}</b><p class="kt-mono">${h(zeitText(z.zeit))}${z.wer ? ' · ' + h(z.wer) : ''}${z.notiz ? ' · «' + h(z.notiz) + '»' : ''}</p></div></div>`).join('')}</div>
    <div class="kt-fenster__kn"><button class="kn kn--klein kn--ohne" type="button" data-zu>Schliessen</button></div>`);
  $('#vl').addEventListener('click', async ev => {
    const z = ev.target.closest('[data-fassung]'); if (!z) return;
    const id = z.dataset.fassung, zeit = $('b', z).textContent;
    if (ev.target.closest('[data-sehen]')) {
      try { const f = await ruf('GET', `/api/fassung/${H()}/karten/${id}`), unt = vergleich(f.daten, STAND.live);
        fenster(`<h2>${h(zeit)}</h2><p class="kt-satz">${unt.length ? 'Links die frühere Fassung, rechts die heute veröffentlichte Karte.' : 'Diese Fassung gleicht der heute veröffentlichten Karte.'}</p>${vglHTML(unt, 'Frühere Fassung', 'Heute veröffentlicht')}
          <div class="kt-fenster__kn"><button class="kt-link" type="button" id="vl-zurueck">Zurück zu den Fassungen</button><button class="kn kn--klein kn--ohne" type="button" data-zu>Schliessen</button></div>`);
        $('#vl-zurueck').addEventListener('click', verlaufFenster);
      } catch (e) { sag('Fassung nicht lesbar', e.message, [], true); }
      return;
    }
    if (!ev.target.closest('[data-d]')) return;
    const holen = async () => {
      try { STAND = await ruf('POST', `/api/zurueckholen/${H()}/karten`, { fassung: id, wer: wer() }); } catch (e) { return sag('Nicht geholt', e.message, [], true); }
      zu(); uebernimm();
      if (geaendert()) sag('Fassung im Entwurf', 'Prüfen Sie vorher und nachher, dann veröffentlichen.', [{ t: 'Vorher / nachher', f: vglFenster }]); else sag('Nichts zurückzuholen', 'Diese Fassung gleicht der veröffentlichten Karte.');
    };
    if (geaendert() || OFFEN) frage('Entwurf <em>ersetzen?</em>', `Die Fassung «${zeit}» kommt in den Entwurf. Der heutige Entwurf wird dabei ersetzt. Die PDF bleibt, bis Sie veröffentlichen.`, 'In den Entwurf holen', holen); else holen();
  });
}
function datenFenster() {
  const k = D();
  fenster(`<h2>Daten <em>der Karte.</em></h2><p class="kt-satz">Für Fortgeschrittene: die ganze Karte als Text. Jeder Eintrag hat eine Art (t): rubrik, gericht, zeile, land, zw, kopf, notiz, frei. «aus»: true blendet einen Eintrag aus. Nach «Übernehmen» steht die Karte unten, gespeichert wird mit dem Knopf in der Leiste.</p>
    <textarea class="kt-daten" id="j-t" spellcheck="false" aria-label="Daten der Karte">${h(JSON.stringify({ fuss: k.fuss, teile: k.teile }, null, 1))}</textarea><p class="kt-fehler" id="j-f" role="alert"></p>
    <div class="kt-fenster__kn"><button class="kn kn--klein kn--ohne" type="button" data-zu>Abbrechen</button><button class="kn kn--d" type="button" id="j-ok">Übernehmen<i>${PF}</i></button></div>`);
  $('#j-ok').addEventListener('click', () => {
    let x; try { x = JSON.parse($('#j-t').value); } catch (e) { $('#j-f').textContent = 'Der Text ist kein gültiges Format: ' + e.message; return; }
    if (!x || !Array.isArray(x.teile)) { $('#j-f').textContent = 'Es fehlen die Teile der Karte.'; return; }
    const ok = x.teile.every(t => t && (t.art === 'deckel' || (t.art === 'inhalt' && Array.isArray(t.posten) && t.posten.every(u => u && ART[u.t]))));
    if (!ok) { $('#j-f').textContent = 'Ein Teil oder Eintrag hat eine unbekannte Art.'; return; }
    k.teile = x.teile; k.fuss = typeof x.fuss === 'string' ? x.fuss : ''; OFFEN = JSON.stringify(DOC) !== BASIS; zu(); vorschau(); leiste();
    sag('Übernommen', 'Noch nicht gespeichert. Mit «Speichern» unten landet es im Entwurf.');
  });
}

// ---------------------------------------------------------------- Probe, PDF, Veröffentlichen, Verwerfen
function pdfLink(base64) { const roh = atob(base64), b = new Uint8Array(roh.length); for (let i = 0; i < roh.length; i++) b[i] = roh.charCodeAt(i); return URL.createObjectURL(new Blob([b], { type: 'application/pdf' })); }
async function probe() {
  if (OFFEN && !(await speichern('Im Entwurf gespeichert', 'Vor der Probe gespeichert.'))) return;
  const warte = sag('Probe-PDF wird gedruckt', 'Einen Moment.', [], false, 60000);
  try { const r = await ruf('POST', `/api/x/karten/probe/${H()}/${encodeURIComponent(Z)}`, {}); warte.remove();
    sag('Probe-PDF fertig', `${r.bericht.seiten} Seiten, ${r.aus === 'entwurf' ? 'aus dem Entwurf' : 'wie veröffentlicht'}. ${r.bericht.ok ? 'PDF und Daten stimmen überein.' : 'Achtung: PDF und Daten stimmen nicht überein.'} Die echte PDF bleibt unverändert.`, [{ t: 'Probe öffnen', href: pdfLink(r.pdf) }], !r.bericht.ok, 30000).dataset.pdf = 'probe'; }
  catch (e) { warte.remove(); sag('Keine Probe-PDF', e.message, [], true); }
}
async function pdfHolen() {
  const warte = sag('Die PDF wird geholt', 'Einen Moment.', [], false, 60000);
  try { const r = await ruf('GET', `/api/x/karten/pdf/${H()}/${encodeURIComponent(Z)}`); warte.remove();
    sag('PDF der veröffentlichten Karte', `«${kurzname(D().name)}», ${r.seiten} Seiten, gedruckt ${zeitText(r.erzeugt)}.${geaendert() ? ' Der Entwurf ist darin noch nicht enthalten.' : ''}`, [{ t: 'PDF öffnen', href: pdfLink(r.pdf) }], false, 30000).dataset.pdf = 'live'; }
  catch (e) { warte.remove(); sag('Keine PDF', e.message, [], true); }
}
async function veroeffentlichen(name, notiz) {
  if (OFFEN && !(await speichern('Im Entwurf gespeichert', 'Vor dem Veröffentlichen gespeichert.'))) return;
  if (!geaendert()) { zu(); return sag('Nichts geändert, nichts veröffentlicht.'); }
  try { localStorage.setItem('karten-wer', name || ''); } catch (e) { /* egal */ }
  const SCHRITTE = ['Jede geänderte Karte wird gesetzt', 'Die PDF wird gedruckt', 'PDF und Daten werden Wort für Wort verglichen', 'Die neue Fassung wird übernommen'];
  fenster(`<div class="kt-lade"><div class="kt-lade__r"></div><h2>Die PDF <em>entsteht.</em></h2><p class="kt-satz" style="margin:0">Alles wird zuerst gedruckt und geprüft. Erst wenn PDF und Daten übereinstimmen, wird umgeschaltet; sonst bleibt alles, wie es ist. Das dauert wenige Sekunden.</p><ol>${SCHRITTE.map(s => `<li>${h(s)}</li>`).join('')}</ol></div>`, true);
  $('#kt-fenster').onclick = null; $('#kt-fenster [data-zu]').hidden = true;
  let r;
  try { r = await ruf('POST', `/api/x/karten/veroeffentlichen/${H()}`, { erwartet: STAND.kennung_entwurf, wer: name || '', notiz: notiz || '' }); }
  catch (e) {
    zu();
    if (e.status === 409 && e.stichwort === 'konflikt') return konflikt('Veröffentlichen');
    return sag('Nicht veröffentlicht', 'Die PDF ist unverändert, Ihr Entwurf ist noch da. ' + e.message + (e.stichwort ? ' (Stichwort: ' + e.stichwort + ')' : ''), [], true, 20000);
  }
  STAND = r.stand; uebernimm();
  const neu = r.bericht.filter(b => b.neu_gedruckt);
  fenster(`<h2>Veröffentlicht. <em>Die PDF steht.</em></h2><p class="kt-satz" id="v-fertig">${neu.length ? neu.map(b => `«${h(kurzname(b.name))}»: ${b.seiten} Seiten neu gedruckt und gegen die Daten geprüft.`).join(' ') : 'Die PDF bleiben, wie sie sind.'} Die vorige Fassung liegt unter «Frühere Fassungen».</p>
    <div class="kt-fenster__kn"><button class="kn kn--klein kn--ohne" type="button" data-zu>Schliessen</button><button class="kn kn--d" type="button" id="v-pdf">PDF öffnen<i>${PF}</i></button></div>`, true);
  $('#v-pdf').addEventListener('click', () => { zu(); pdfHolen(); });
}
function verwerfen() {
  frage('Entwurf <em>verwerfen?</em>', 'Alle Änderungen seit der letzten PDF fallen weg, bei allen Karten des Hauses. Die veröffentlichte Karte bleibt, wie sie ist.', 'Verwerfen', async () => {
    try { STAND = await ruf('DELETE', `/api/entwurf/${H()}/karten`, { wer: wer() }); } catch (e) { return sag('Nicht verworfen', e.message, [], true); }
    uebernimm(); sag('Entwurf verworfen', 'Die Karte steht wieder wie in der PDF.');
  });
}

// ---------------------------------------------------------------- Laden
function uebernimm() {   // STAND ist neu vom Speicher: Arbeitsstand danach richten
  DOC = kopie(STAND.entwurf || STAND.live); if (!eintrag(Z)) Z = DOC.karten[0].id;
  BASIS = JSON.stringify(DOC); OFFEN = false; UNDO = []; GESCHRIEBEN.clear();
  alles();
  ruf('GET', `/api/x/karten/uebersicht/${H()}`).then(u => { UEBER = u; rand(); }).catch(() => {});
}
async function lade(z, still) {
  STAND = await ruf('GET', `/api/stand/${H()}/karten`);
  if (!STAND.live) throw Object.assign(new Error('Für dieses Haus sind noch keine Karten eingelesen.'), { stichwort: 'haus-ohne-karten' });
  UEBER = await ruf('GET', `/api/x/karten/uebersicht/${H()}`);
  ZSVG = '';
  if (kleid().zeichen) { try { const r = await fetch(kleidDatei(kleid().zeichen), { cache: 'no-store' }); if (r.ok) { const t = await r.text(); if (/^<svg[\s>]/.test(t) && !/<script|\son\w+=|javascript:/i.test(t)) ZSVG = t; } } catch (e) { /* ohne Zeichen: Anfangsbuchstaben */ } }
  DOC = kopie(STAND.entwurf || STAND.live);
  Z = eintrag(z) ? z : DOC.karten[0].id;
  BASIS = JSON.stringify(DOC); OFFEN = false; UNDO = []; GESCHRIEBEN.clear();
  try { localStorage.setItem('karten-karte-' + HAUS, Z); } catch (e) { /* egal */ }
  history.replaceState(null, '', '#' + Z);
  alles();
  if (!still && STAND.offen) sag('Entwurf geöffnet', 'Gespeichert, noch nicht in der PDF.');
}
async function wechsel(z) {
  if (z === Z) return;
  if (laufend) await laufend;
  const los = () => { if (OFFEN) { DOC = JSON.parse(BASIS); OFFEN = false; GESCHRIEBEN.clear(); } Z = z; try { localStorage.setItem('karten-karte-' + HAUS, Z); } catch (e) { /* egal */ } history.replaceState(null, '', '#' + Z); window.scrollTo(0, 0); $('#kt-seiten').scrollTop = 0; alles(); };
  if (OFFEN) return frage('Nicht <em>gespeichert.</em>', 'Sie haben in dieser Karte Änderungen, die noch nicht gespeichert sind.', 'Verwerfen und wechseln', los);
  los();
}
async function modus(m) {
  if (m === MODUS) return;
  if (laufend) await laufend;   // wird gerade gespeichert: erst das Ergebnis abwarten
  const los = () => { MODUS = m; try { localStorage.setItem('karten-modus', MODUS); } catch (e) { /* egal */ } alles(); };
  if (OFFEN && m === 'einfach') return frage('Nicht <em>gespeichert.</em>', 'Erst speichern, dann wechseln?', 'Speichern', async () => { if (await speichern('Im Entwurf gespeichert')) los(); });
  los();
}

// ---------------------------------------------------------------- Ereignisse
document.addEventListener('click', ev => {
  const b = ev.target.closest('[data-akt],[data-z],[data-m],[data-zoom]');
  if (!b || b.closest('#kt-fenster') || b.disabled) return;
  if (b.dataset.z) return wechsel(b.dataset.z);
  if (b.dataset.m) return modus(b.dataset.m);
  if (b.dataset.zoom) { ZM[MODUS] = Math.min(1.3, Math.max(0.35, +(ZM[MODUS] + (+b.dataset.zoom) * 0.1).toFixed(2))); try { localStorage.setItem('karten-zoom-' + MODUS, ZM[MODUS]); } catch (e) { /* egal */ } return neuPassen(); }
  const a = b.dataset.akt, r = b.closest('.kt-r'), ti = r ? +r.dataset.ti : +(b.dataset.ti == null ? -1 : b.dataset.ti), i = r && r.dataset.i !== undefined ? +r.dataset.i : -1;
  if (a === 'speichern') return OFFEN ? speichern('Im Entwurf gespeichert') : sag(GRUEN ? 'Gespeichert.' : 'Alles ist gespeichert.', 'Nichts geändert, nichts gespeichert. Offene Eingaben gibt es gerade nicht.');
  if (a === 'veroeffentlichen') return OFFEN || geaendert() ? (OFFEN ? speichern('Im Entwurf gespeichert').then(ok => ok && vglFenster()) : vglFenster()) : null;
  if (a === 'vgl') return vglFenster();
  if (a === 'probe') return probe();
  if (a === 'pdf') return pdfHolen();
  if (a === 'verwerfen') return verwerfen();
  if (a === 'verlauf') return verlaufFenster();
  if (a === 'karte') return karteFenster();
  if (a === 'daten') return datenFenster();
  if (a === 'neu') return neuGlobal();
  if (a === 'edit-deckel') return deckelFenster(ti);
  if (a === 'edit') return eintragFenster({ ti, i });
  if (a === 'neu-hier') { const bl = bloecke(ti).find(x => x[0] === i); return eintragFenster({ ti, nach: (bl ? bl[1] : i + 1) - 1 }); }
  if (a === 'neu-ende') return eintragFenster({ ti, nach: teile()[ti].posten.length - 1 });
  if (a === 'rubrik-neu') return rubrikNeu(ti);
  if (a === 'hoch') return schiebe(ti, i, -1);
  if (a === 'runter') return schiebe(ti, i, 1);
  if (a === 'aus') return blende(ti, i);
  if (a === 'weg') return entfernen(ti, i);
});
$('.kt-ansicht').addEventListener('click', ev => { const b = ev.target.closest('[data-ansicht]'); if (!b || b.dataset.ansicht === ANSICHT) return; ANSICHT = b.dataset.ansicht; ansicht(); });
document.addEventListener('keydown', ev => {
  if (ev.key === 'Escape' && !$('#kt-fenster').hidden && $('#kt-fenster [data-zu]:not([hidden])')) zu();
  if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 's') { ev.preventDefault(); if (OFFEN) speichern('Im Entwurf gespeichert'); }
});
window.addEventListener('beforeunload', ev => { if (OFFEN) { ev.preventDefault(); ev.returnValue = ''; } });
let warte; window.addEventListener('resize', () => { clearTimeout(warte); warte = setTimeout(() => { if (DOC) neuPassen(); }, 180); });
Welt.bei(() => { if (DOC) { kleide(); oben(); } });

// ---------------------------------------------------------------- Start
const w0 = $('#kt-vorschau').contentWindow; if (w0 && w0.KT_DRUCK) window.KT_VORSCHAU_BEREIT(w0);
(async () => {
  try {
    if (!HAUS) throw Object.assign(new Error('In der Adresse fehlt das Haus, zum Beispiel ?haus=gasterntal.'), { stichwort: 'haus-fehlt' });
    let z = location.hash.slice(1); if (!z) { try { z = localStorage.getItem('karten-karte-' + HAUS) || ''; } catch (e) { z = ''; } }
    await lade(z);
  } catch (e) {
    const kaputt = STAND && STAND.entwurf;
    document.body.innerHTML = `<div class="kt-tuer"><div><p class="t-ansicht" id="kt-tuer-titel">${h(Welt.name('karten'))} startet nicht.</p><p>${h(e.message)}</p>${e.stichwort ? `<p class="angabe">Stichwort: ${h(e.stichwort)}</p>` : ''}
      <div class="kt-kopf__kn"><button class="kn" type="button" id="kt-nochmal">Noch einmal versuchen<i>${PF}</i></button>${kaputt ? '<button class="kn kn--klein kn--ohne" type="button" id="kt-entwurf-weg">Entwurf verwerfen und neu laden</button>' : ''}</div>
      ${kaputt ? '<p>Liegt es am Entwurf, hilft «Entwurf verwerfen»: die veröffentlichte Karte bleibt, wie sie ist.</p>' : ''}</div></div>`;
    $('#kt-nochmal').onclick = () => location.reload();
    if (kaputt) $('#kt-entwurf-weg').onclick = () => ruf('DELETE', `/api/entwurf/${H()}/karten`, { wer: wer() }).then(() => location.reload(), f => { $('#kt-tuer-titel').textContent = 'Nicht verworfen: ' + f.message; });
  }
})();
window.KT = { preisForm, vergleich, stand: () => STAND, vorschau: () => LETZTE, bereit: () => !!DOC, modus: () => MODUS };
})();
