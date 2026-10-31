// Abnahme-Tor · Funktionen, die im Browser laufen (page.evaluate). Jede Funktion steht für sich (keine Bezüge nach aussen).
// kandidaten  – alle bedienbaren Stellen des Zustands (für das Inventar), mit Wiederfinde-Angaben
// finde       – markiert eine Stelle für den Klick (data-tor="ziel")
// signatur    – Kennung des Zustands (Weg, aktive Navigation, offene Fenster, Titel, Dokumente) und Inhalt (für «zwei Wege zum selben Ziel»)
// verdeckte   – blendet Ebenen aus der Messung aus, die ganz von einer anderen Ebene überdeckt sind
// ergaenzung  – Kriterien, die der Messlauf nicht misst (Platzhalter, Einzelwort, Kante, leere Kachel, Stil, doppelte Marke, Substanz)

exports.kandidaten = function kandidaten(opt) {
  const GEFAHR = new RegExp(opt.gefahr, 'i');
  const LAUFZUSTAND = /^(an|aktiv|da|gespielt|offen|sicht|auf|zu|hover|fokus|gewaehlt|gewählt|wahl|ist-.*|js-.*|an-.*|is-.*|selected|active|current|wo-an|kw-an)$/;
  const sicht = e => { const r = e.getBoundingClientRect(); if (r.width < 4 || r.height < 4) return false;
    for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const c = getComputedStyle(x); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false; if (x.hidden || x.inert) return false; } return true; };
  const klassen = e => (typeof e.className === 'string' ? e.className : (e.className && e.className.baseVal) || '').trim().split(/\s+/).filter(k => k && !LAUFZUSTAND.test(k));
  const glied = e => e.tagName.toLowerCase() + klassen(e).slice(0, 3).map(k => '.' + CSS.escape(k)).join('');
  const ankerVon = e => { for (let x = e.parentElement; x && x !== document.body; x = x.parentElement) if (x.id && !/^\d/.test(x.id)) return x; return null; };
  const kette = e => { const a = ankerVon(e), teile = []; for (let x = e; x && x !== a && x !== document.body && teile.length < 4; x = x.parentElement) teile.unshift(glied(x)); return { anker: a ? '#' + CSS.escape(a.id) : '', kette: teile.join(' > ') }; };
  const text = e => (e.getAttribute('aria-label') || e.innerText || e.title || e.getAttribute('data-tip') || '').trim().replace(/\s+/g, ' ').slice(0, 70);
  const wo = e => { const z = e.closest('nav,aside,header,footer,[role=tablist],dialog,[role=dialog],.reiter,[class*="leiste"],[class*="rand"]'); return z ? z.tagName.toLowerCase() + (z.getAttribute('role') ? '[' + z.getAttribute('role') + ']' : '') + (klassen(z)[0] ? '.' + klassen(z)[0] : '') : 'haupt'; };
  const basis = new URL(opt.bereich, location.href);
  const sel = 'button,a[href],[role=tab],[role=button],[role=menuitem],summary,[data-ansicht],[data-gehe],[data-zeige],[data-oeffne],[data-art],[data-vorlage],[onclick]';
  const frei = e => { const r = e.getBoundingClientRect(); const x = r.left + r.width / 2, y = r.top + r.height / 2; if (x < 0 || y < 0 || x > innerWidth || y > innerHeight) return true; const h = document.elementFromPoint(x, y); return !h || e.contains(h) || h.contains(e) || h.closest('label') === e.closest('label'); };
  const alle = [...new Set([...document.querySelectorAll(sel)])].filter(e => !e.closest('[data-messlauf-aus],[data-tor-aus]') && !e.disabled && e.getAttribute('aria-disabled') !== 'true' && sicht(e) && frei(e));
  const aus = [];
  for (const e of alle) {
    const t = text(e); if (GEFAHR.test(t) || GEFAHR.test(e.id || '')) continue;
    if (e.closest('a[href]') && e.closest('a[href]') !== e && !e.matches('button,[role=button]')) continue;    // Inhalt eines Links zählt als der Link
    let ziel = 'klick';
    if (e.matches('a[href]')) { const h = e.getAttribute('href') || '';
      if (/^(mailto|tel|javascript|data|blob):/i.test(h) || e.target === '_blank' || e.hasAttribute('download')) continue;
      let u; try { u = new URL(e.href); } catch (x) { continue; }
      const gleich = u.origin === location.origin && u.pathname === location.pathname && u.search === location.search;
      if (!gleich) { if (u.origin !== basis.origin || !u.pathname.startsWith(basis.pathname)) continue;   // anderes Werkzeug / Website: nicht dieses Werkzeug
        if (opt.ohne && new RegExp(opt.ohne).test(u.pathname)) continue;   // ausgenommene Bereiche (z. B. /wildside/, /en/ für die deutsche Website)
        if (/\.(pdf|zip|png|jpe?g|webp|svg|json|csv|ase|ttf|woff2?)$/i.test(u.pathname)) continue;
        ziel = 'seite'; }
    }
    const k = kette(e);
    aus.push({ text: t, anker: k.anker, kette: k.kette, gruppe: k.anker + ' ' + k.kette, wo: wo(e), ziel, href: e.href || '', rolle: e.getAttribute('role') || e.tagName.toLowerCase(), r: (r => [Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)])(e.getBoundingClientRect()) });
  }
  // laufende Nummer unter gleichen (Gruppe + Text), damit gleichnamige Stellen wiedergefunden werden
  const z = {}; for (const a of aus) { const s = a.gruppe + '|' + a.text; a.nr = z[s] = (z[s] ?? -1) + 1; }
  const gr = {}; for (const a of aus) gr[a.gruppe] = (gr[a.gruppe] || 0) + 1; for (const a of aus) a.gruppenZahl = gr[a.gruppe];
  return aus;
};

exports.finde = function finde(k) {
  document.querySelectorAll('[data-tor="ziel"]').forEach(e => e.removeAttribute('data-tor'));
  const sicht = e => { const r = e.getBoundingClientRect(); if (r.width < 4 || r.height < 4) return false; for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const c = getComputedStyle(x); if (c.display === 'none' || c.visibility === 'hidden') return false; } return true; };
  const text = e => (e.getAttribute('aria-label') || e.innerText || e.title || e.getAttribute('data-tip') || '').trim().replace(/\s+/g, ' ').slice(0, 70);
  let kand = []; try { kand = [...document.querySelectorAll((k.anker ? k.anker + ' ' : '') + k.kette)]; } catch (x) { }
  let gleich = kand.filter(e => text(e) === k.text);
  if (!gleich.length && k.text) { // Umbau der Klassen: nach Text suchen
    gleich = [...document.querySelectorAll('button,a[href],[role=tab],[role=button],summary,[data-ansicht],[data-art],[data-vorlage]')].filter(e => text(e) === k.text); }
  if (!gleich.length && k.text && /\d/.test(k.text)) { // Zahlen im Namen ändern sich im Lauf des Tages (Besucherliste «Besuche 1» → «Besuche 4», Tor 6 30.10.): ohne Zahlen vergleichen
    const oz = v => v.replace(/[\d.,:%]+/g, '#').replace(/\s+/g, ' ').trim();
    gleich = kand.filter(e => oz(text(e)) === oz(k.text));
    if (!gleich.length) gleich = [...document.querySelectorAll('button,a[href],[role=tab],[role=button],summary,[data-ansicht],[data-art],[data-vorlage]')].filter(e => oz(text(e)) === oz(k.text)); }
  const sichtbar = gleich.filter(sicht);
  const e = sichtbar[k.nr] || sichtbar[0] || gleich[k.nr] || gleich[0];
  if (!e) return false;
  e.setAttribute('data-tor', 'ziel'); return true;
};

exports.signatur = function signatur(opt) {
  const sicht = e => { const r = e.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return false; for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const c = getComputedStyle(x); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false; if (x.hidden) return false; } return true; };
  const t = e => (e.innerText || e.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 50);
  const aktiv = [...document.querySelectorAll('nav [aria-current],nav .an,nav .aktiv,aside .an,aside .aktiv,aside .wo-an,[role=tab][aria-selected="true"],.reiter .an,[aria-pressed="true"],header .an')].filter(sicht).map(t).filter(Boolean).sort();
  const fenster = [...document.querySelectorAll('dialog[open],[role=dialog],[aria-modal="true"],[class*="fenster"],[class*="dialog"],[class*="modal"],[class*="schublade"],[class*="lightbox"],[class*="popover"],[class*="leiste--offen"],[class*="rechts"]:not(.rechts-zu),.rdg-karte')]
    .filter(e => { if (!sicht(e)) return false; const r = e.getBoundingClientRect(); if (r.width < 60 || r.height < 60) return false; const p = getComputedStyle(e).position; return p === 'fixed' || p === 'absolute' || e.matches('dialog,[role=dialog],[aria-modal="true"]') || /rechts/.test(e.className); })
    .map(e => (e.className && typeof e.className === 'string' ? e.className.split(/\s+/)[0] : e.tagName) + ':' + t(e.querySelector('h1,h2,h3,h4,legend,strong') || e).slice(0, 30));
  const titel = [...document.querySelectorAll('h1,h2,h3')].filter(sicht).map(t).filter(Boolean).slice(0, 8);
  const DOK = new RegExp(opt.dokument), NDOK = opt.dokumentNicht ? new RegExp(opt.dokumentNicht) : null;
  const doks = [...document.querySelectorAll('*')].filter(e => { const k = typeof e.className === 'string' ? e.className : ''; return k && DOK.test(' ' + k + ' ') && !(NDOK && NDOK.test(' ' + k + ' ')) && !/(^|\s)papier--leer(\s|$)/.test(k) && sicht(e) && e.getBoundingClientRect().height > 60; })
    .filter((e, i, a) => !a.some(o => o !== e && o.contains(e)));
  const gross = doks.filter(e => e.getBoundingClientRect().height >= 300);
  const lage = gross.map(e => { const r = e.getBoundingClientRect(); return r.width > r.height * 1.05 ? 'quer' : 'hoch'; });
  const weg = location.pathname + location.search;
  const roh = [weg, aktiv.join(','), fenster.join(','), titel.join('|'), (gross.length ? 'dok:' + lage.join(',') : '')].join('¶');
  let h = 0; for (let i = 0; i < roh.length; i++) h = (h * 31 + roh.charCodeAt(i)) | 0;
  // Inhalt für «zwei Wege zum selben Ziel»: sichtbarer Text und Bilder ausserhalb von Navigation/Kopf
  const haupt = [...document.querySelectorAll('body *')].filter(e => !e.closest('nav,aside,header,[role=tablist],[class*="leiste"],[class*="kopf"]'));
  const bilder = [...new Set(haupt.filter(e => e.tagName === 'IMG' && sicht(e)).map(e => (e.currentSrc || e.src).split('/').pop().split('?')[0]))].slice(0, 200);
  const woerter = [...new Set(haupt.filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && sicht(e)).map(e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ')).join(' ').toLowerCase().match(/[a-zäöüß]{3,}/g) || [])].slice(0, 600);
  return { sig: String(h >>> 0), weg, aktiv, fenster, titel, dok: { n: doks.length, gross: gross.length, lage }, inhalt: { bilder, woerter }, hoehe: document.documentElement.scrollHeight };
};

exports.verdeckte = function verdeckte() {
  const VW = innerWidth, VH = innerHeight; let n = 0;
  const pruef = [...document.body.children]; for (const c of [...pruef]) pruef.push(...c.children); for (const c of [...pruef]) pruef.push(...c.children);
  for (const e of pruef) {
    if (e.closest('[data-messlauf-aus]')) continue;
    const r = e.getBoundingClientRect(); const l = Math.max(0, r.left), o = Math.max(0, r.top), re = Math.min(VW, r.right), u = Math.min(VH, r.bottom);
    if (re - l < VW * 0.3 || u - o < VH * 0.3) continue;
    let treffer = 0, punkte = 0;
    for (const fx of [.2, .5, .8]) for (const fy of [.2, .5, .8]) { const x = l + (re - l) * fx, y = o + (u - o) * fy; const h = document.elementFromPoint(x, y); punkte++; if (h && (e.contains(h) || h.contains(e))) treffer++; }
    if (punkte && !treffer) { e.setAttribute('data-messlauf-aus', 'verdeckt'); n++; }
  }
  return n;
};

exports.ergaenzung = function ergaenzung(opt) {
  const F = [], VW = innerWidth;
  const cs = e => getComputedStyle(e);
  const sicht = e => { if (e.closest('[data-messlauf-aus]')) return false; const r = e.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return false; for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const c = cs(x); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false; } return true; };
  const pfad = e => { const p = []; for (let x = e; x && x !== document.body && p.length < 4; x = x.parentElement) { let t = x.tagName.toLowerCase(); if (x.id) { p.unshift(t + '#' + x.id); break; } const k = typeof x.className === 'string' ? x.className.trim().split(/\s+/).slice(0, 2) : []; if (k.length && k[0]) t += '.' + k.join('.'); p.unshift(t); } return p.join(' > '); };
  const rect = e => { const r = e.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height) }; };
  const txt = e => (e.innerText || e.placeholder || e.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 60);
  const fund = (k, art, e, info) => F.push({ k, art, sel: pfad(e), text: txt(e), info, r: rect(e) });
  const DOK = new RegExp(opt.dokument), NDOK = opt.dokumentNicht ? new RegExp(opt.dokumentNicht) : null;
  const istDok = e => { const k = typeof e.className === 'string' ? e.className : ''; return k && DOK.test(' ' + k + ' ') && !(NDOK && NDOK.test(' ' + k + ' ')) && !/(^|\s)papier--leer(\s|$)/.test(k); };
  const alle = [...document.body.querySelectorAll('*')].filter(e => !/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|OPTION|BR)$/.test(e.tagName));
  const sichtbar = alle.filter(sicht);
  const leuchte = c => { const m = c.match(/[\d.]+/g); if (!m) return null; const [r, g, b] = m.slice(0, 3).map(v => { v = +v / 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }); return { L: .2126 * r + .7152 * g + .0722 * b, a: m[3] === undefined ? 1 : +m[3] }; };
  const grund = e => { for (let x = e; x; x = x.parentElement) { const c = cs(x).backgroundColor; const l = leuchte(c); if (l && l.a > .5) return l.L; } return 1; };
  const kontrast = (a, b) => (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
  const breite = (s, font) => { const c = ergaenzung.c || (ergaenzung.c = document.createElement('canvas').getContext('2d')); c.font = font; return c.measureText(s).width; };

  // K2 Platzhalter: passt der Platzhalter in sein Feld?  K8 Platzhalter nicht zu blass
  for (const e of sichtbar.filter(e => e.matches('input[placeholder],textarea[placeholder]') && !e.value)) {
    const c = cs(e), ph = e.placeholder; if (!ph) continue;
    const pc = cs(e, '::placeholder');
    const font = `${pc.fontStyle} ${pc.fontWeight} ${pc.fontSize} ${pc.fontFamily}`;
    const innen = e.clientWidth - parseFloat(c.paddingLeft) - parseFloat(c.paddingRight);
    const w = breite(ph, font);
    if (e.tagName === 'INPUT') { if (w > innen + 1) fund(2, 'platzhalter', e, `Platzhalter ${Math.round(w)} px breit, Feld innen ${Math.round(innen)} px: «${ph.slice(0, 40)}» abgeschnitten`); }
    else { const lh = parseFloat(pc.lineHeight) || parseFloat(pc.fontSize) * 1.3; const zeilen = Math.ceil(w / Math.max(innen, 1) + 0.15); const hoch = e.clientHeight - parseFloat(c.paddingTop) - parseFloat(c.paddingBottom);
      if (zeilen * lh > hoch + 2) fund(2, 'platzhalter', e, `Platzhalter braucht ${zeilen} Zeilen (${Math.round(zeilen * lh)} px), Feld ${Math.round(hoch)} px hoch: «${ph.slice(0, 40)}» abgeschnitten`); }
    const lp = leuchte(pc.color); if (lp) { const k = kontrast(lp.L * lp.a + grund(e) * (1 - lp.a), grund(e)); if (k < 2.6) fund(8, 'blass', e, `Platzhalter Kontrast ${k.toFixed(2)}:1 (zu blass)`); }
  }

  // K1 Rundknopf ohne eigene Fläche (Ring aus ::before, Rahmen am Kind): Symbolknopf mit runder Form, der nicht kreisrund ist
  for (const e of sichtbar.filter(e => e.matches('a,button,[role=button]') && !(e.innerText || '').trim() && e.querySelector('svg,img'))) {
    const r = e.getBoundingClientRect(), w = r.width, h = r.height; if (Math.max(w, h) > 96 || Math.min(w, h) < 12) continue;
    const rad = cs(e).borderTopLeftRadius, radPx = rad.endsWith('%') ? parseFloat(rad) / 100 * Math.min(w, h) : parseFloat(rad);
    const rund = (rad.endsWith('%') && parseFloat(rad) >= 50) || radPx >= Math.min(w, h) / 2 - .5 || /(^|[\s-])(rund|round|kreis)/i.test(typeof e.className === 'string' ? e.className : '');
    if (rund && Math.abs(w - h) > 1 && Math.max(w, h) / Math.min(w, h) <= 2) fund(1, 'oval', e, `Rundknopf ${w.toFixed(1)} × ${h.toFixed(1)} px (${e.getAttribute('aria-label') || e.title || 'ohne Namen'})`);
  }

  // K2 Beschriftung ohne Luft im Knopf/Kachel (auch ohne eigene Fläche): Text näher als 3 px am Rand oder breiter als der Knopf
  for (const e of sichtbar.filter(e => e.matches('button,[role=button],[role=tab],a[class*="kn"],a[class*="kachel"]'))) {
    const r = e.getBoundingClientRect(); if (r.height < 26 || r.width > VW * .6) continue;
    const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n, l = 1e9, re = -1e9;
    while ((n = w.nextNode())) { if (!n.textContent.trim()) continue; const g = document.createRange(); g.selectNodeContents(n); for (const q of g.getClientRects()) if (q.width > .5) { l = Math.min(l, q.left); re = Math.max(re, q.right); } }
    if (l > 1e8) continue;
    const lr = l - r.left, rr = r.right - re;
    const kc = cs(e), kasten = (kc.backgroundColor !== 'rgba(0, 0, 0, 0)' && kc.backgroundColor !== 'transparent') || kc.backgroundImage !== 'none' || parseFloat(kc.borderLeftWidth) > 0 || kc.boxShadow !== 'none';
    if (Math.min(lr, rr) < 3 && (kasten || Math.min(lr, rr) < -.5 || re - l >= r.width - 4)) fund(2, 'randlos', e, `Beschriftung «${(e.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 30)}» ${Math.round(lr)} px vom linken, ${Math.round(rr)} px vom rechten Rand des Knopfs (${Math.round(r.width)} px)`);
  }

  // K7 Einzelwort allein in der letzten Zeile von Titeln und Unterschriften
  const TITEL = 'h1,h2,h3,h4,h5,h6,figcaption,caption,legend,dt,[class*="titel"],[class*="title"],[class*="unterschrift"],[class*="__t"],[class*="__n"] b,[class*="name"],.stueck b,.stueck strong,button b,button strong';
  const gesehen = new Set();
  for (const e of sichtbar) {
    if (!e.matches(TITEL)) continue; if (gesehen.has(e)) continue; gesehen.add(e);
    if (e.closest('input,textarea,select,[contenteditable]')) continue;
    if (cs(e).whiteSpace === 'nowrap') continue;
    if ([...e.querySelectorAll('div,p,section,article,h1,h2,h3,h4,h5,h6,ul,ol,li,figure,button')].some(x => sicht(x))) continue;
    const tn = []; const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.textContent.trim()) tn.push(n);
    const worte = []; for (const t of tn) { const re = /\S+/g; let m; while ((m = re.exec(t.textContent))) { const r = document.createRange(); r.setStart(t, m.index); r.setEnd(t, m.index + m[0].length); const q = [...r.getClientRects()].filter(q => q.width > .5); if (q.length) worte.push({ w: m[0], top: q[q.length - 1].top, h: q[0].height }); } }
    if (worte.length < 3) continue;
    const zeilen = []; for (const x of worte) { const z = zeilen.find(z => Math.abs(z.top - x.top) < x.h * .5); if (z) z.w.push(x.w); else zeilen.push({ top: x.top, w: [x.w] }); }
    if (zeilen.length < 2) continue; zeilen.sort((a, b) => a.top - b.top);
    const letzte = zeilen[zeilen.length - 1].w; if (letzte.length === 1 && !/^[–—·|/&+-]$/.test(letzte[0])) fund(7, 'einzelwort', e, `«${letzte[0]}» allein in der letzten Zeile (${zeilen.length} Zeilen)`);
  }

  // K6 gemeinsame linke Kante: Textanfänge übereinanderstehender Geschwister in Leisten, Füssen und Kacheln
  const BLOCK = 'aside,nav,footer,[class*="leiste"],[class*="rand"],[class*="fuss"],[class*="foot"],[class*="kachel"],[class*="karte"],[class*="panel"]';
  const kanteGesehen = new Set();
  const textAnfang = e => { const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT); let n, links = 1e9; while ((n = w.nextNode())) { if (n.nodeType === 1) { if (n.matches && n.matches('svg,img,i') && sicht(n)) { links = Math.min(links, n.getBoundingClientRect().left); } continue; } if (!n.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(n); const q = [...r.getClientRects()].filter(q => q.width > .5); if (q.length) links = Math.min(links, ...q.map(q => q.left)); } return links; };
  for (const blk of sichtbar.filter(e => e.matches(BLOCK) && !istDok(e) && !e.closest('[class*="papier"],[class*="blatt"]'))) {
    const kinder = [...blk.children].filter(c => sicht(c) && (c.innerText || '').trim() && cs(c).position !== 'absolute' && cs(c).position !== 'fixed');
    if (kinder.length < 2) continue;
    // nur Geschwister, die untereinander stehen und nicht über die ganze Breite laufen
    const st = kinder.map(c => ({ c, r: c.getBoundingClientRect(), l: textAnfang(c), ta: cs(c).textAlign })).filter(x => x.l < 1e8);
    for (let i = 1; i < st.length; i++) {
      const a = st[i - 1], b = st[i];
      if (b.r.top < a.r.bottom - 2) continue;                    // nebeneinander
      if (/center/.test(a.ta) || /center/.test(b.ta)) { if (Math.abs((a.r.left + a.r.right) / 2 - (b.r.left + b.r.right) / 2) <= 2) continue; }
      const d = Math.abs(a.l - b.l);
      if (d > 2.5 && d < 40) { const key = pfad(blk); if (kanteGesehen.has(key + i)) continue; kanteGesehen.add(key + i);
        fund(6, 'kante', blk, `Zeilen stehen nicht auf einer Kante: «${(a.c.innerText || '').trim().split('\n')[0].slice(0, 24)}» beginnt bei ${Math.round(a.l)} px, «${(b.c.innerText || '').trim().split('\n')[0].slice(0, 24)}» bei ${Math.round(b.l)} px`); }
    }
  }

  // K4 leere Kachel: Kachel/Knopf ohne Text und ohne sichtbares Bild; Bilder, die nicht laden; Flächen nur mit Hintergrund → Bildprüfung
  const KACHEL = /k[aä]chel|karte|tile|card|stueck|\bwo\b|wo__|feld|tafel|kasten|swatch|muster|tapete|vorschau|bild|foto|thumb|mini/i;
  const pruefBild = [];
  for (const e of sichtbar) {
    const k = typeof e.className === 'string' ? e.className : ''; const r = e.getBoundingClientRect();
    if (r.width < 40 || r.height < 40 || r.width > VW * 0.9) continue;
    if (e.tagName === 'IMG') { if (e.complete && e.naturalWidth === 0 && e.getAttribute('src')) fund(4, 'bild-fehlt', e, `Bild lädt nicht: ${(e.getAttribute('src') || '').split('/').pop()}`); continue; }
    // Fläche, die nur aus einem Hintergrundbild besteht (Muster, Tapete, Farbfeld): ins Bild schauen, ob etwas zu sehen ist
    if (cs(e).backgroundImage.startsWith('url(') && !(e.innerText || '').trim() && !e.children.length && pruefBild.length < 14 && !e.closest('[class*="papier"],[class*="blatt"]')) { pruefBild.push({ sel: pfad(e) + ' [' + (cs(e).backgroundImage.match(/([^/]+?)["')]*$/) || ['', ''])[1] + ']', r: rect(e) }); continue; }
    if (!KACHEL.test(k) && !e.matches('button,a[href],figure,li')) continue;
    if (e.closest('[class*="papier"],[class*="blatt"]') && !istDok(e)) continue;
    const hatText = (e.innerText || '').trim().length > 0;
    const medien = [...e.querySelectorAll('img,svg,canvas,video,picture')].filter(m => sicht(m) && m.getBoundingClientRect().width > 8);
    const bg = cs(e).backgroundImage !== 'none' || [...e.querySelectorAll('*')].some(x => sicht(x) && cs(x).backgroundImage !== 'none' && x.getBoundingClientRect().width > r.width * .5);
    if (!hatText && !medien.length && !bg && !e.matches('input,textarea,select') && (e.children.length === 0 || KACHEL.test(k))) {
      if (cs(e).backgroundColor !== 'rgba(0, 0, 0, 0)' || parseFloat(cs(e).borderTopWidth) > 0) fund(4, 'leer', e, `Kachel ohne Inhalt (${Math.round(r.width)}×${Math.round(r.height)} px)`); }
    else if (!hatText && (bg || medien.length) && KACHEL.test(k) && pruefBild.length < 14) pruefBild.push({ sel: pfad(e), r: rect(e) });
  }

  // Dokumente: Lage für die Bildprüfung (Löcher, Mitte); K12 Stil; K14 doppelte Marke
  const stil = opt.stil || {};
  const doks = sichtbar.filter(istDok).filter((e, i, a) => !a.some(o => o !== e && o.contains(e)) && e.getBoundingClientRect().height > 60);
  const dokListe = [];
  for (const d of doks) {
    dokListe.push({ sel: pfad(d), r: rect(d) });
    const innen = [...d.querySelectorAll('*')].filter(sicht);
    // K12 Versalien in Lesezeilen (nicht Mono-Etiketten), Trennzeichen
    if (stil.versalienNur) { const erlaubt = new RegExp(stil.versalienErlaubt || stil.versalienNur, 'i');
      for (const e of innen) { const own = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').trim(); if (own.split(/\s+/).length < 2 || own.length < 10) continue;
        const c = cs(e); const gross = c.textTransform === 'uppercase' || (own === own.toUpperCase() && /[A-ZÄÖÜ]{3}/.test(own));
        const rudiZeile = stil.rudi && own.includes(' ' + stil.rudi + ' ') && own.split(' ' + stil.rudi + ' ').every(g => g.trim().split(/\s+/).length <= 3); // Hausregel: Rudis Zeilen in Versalien mit «/»
        if (gross && !rudiZeile && !erlaubt.test(c.fontFamily)) { fund(12, 'stil', e, `Versalien in ${c.fontFamily.split(',')[0]} (Haus: Versalien nur ${stil.versalienNur}): «${own.slice(0, 40)}»`); break; } } }
    if (stil.trenner) { const falsch = new RegExp(stil.trennerFalsch || '\\S\\s+/\\s+\\S');
      for (const e of innen) { const own = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' '); const gemischt = /[a-zäöüß]/.test(own) && /[A-ZÄÖÜ]/.test(own); if (stil.rudi && !gemischt) continue; /* Versalien = Rudis Zeile (Hausregel), klein = Pfad */ if (falsch.test(own)) { fund(12, 'stil', e, `Trennzeichen «/» statt «${stil.trenner}»: «${own.trim().slice(0, 40)}»`); break; } } }
    // K14 Marke doppelt
    const marken = innen.filter(e => e.matches('img,svg,[class*="marke"],[class*="logo"],[class*="wortmarke"]') && /marke|logo|wortmarke|zeichen/i.test((e.getAttribute('alt') || '') + ' ' + (e.getAttribute('aria-label') || '') + ' ' + (typeof e.className === 'string' ? e.className : (e.className.baseVal || '')) + ' ' + (e.getAttribute('src') || '')))
      .filter((e, i, a) => !a.some(o => o !== e && o.contains(e)));
    if (marken.length > 1) fund(14, 'marke-doppelt', d, `${marken.length} Marken/Logos in einem Dokument`);
  }

  // K2/K4 zerfallene Spalte (Werkbank-Feed 30.10.): Lesetext oder Knopf mit vielen Wörtern, fast ein Wort pro Zeile
  for (const e of sichtbar) { const direkt = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').trim(); if (!e.matches('p,li,h1,h2,h3,h4,a,button,dd,figcaption') && direkt.split(/\s+/).length < 8) continue; if (e.matches('p,li,dd,figcaption,div') && [...e.children].some(k => k.matches('p,li,div'))) continue; const own = (e.innerText || '').trim(); const n = own.split(/\s+/).length; if (n < 3) continue;
    if (own.length > 600 || e.getElementsByTagName('*').length > 40) continue;   // Kacheln mit ganzem Dokument darin (Vorlagen-Knöpfe) sind kein Lesetext; die Zählung wäre dort quadratisch und hängt (30.10.)
    const r = e.getBoundingClientRect(); const rg = document.createRange(); rg.selectNodeContents(e); const tt = [...rg.getClientRects()].filter(q => q.width > 1).map(q => q.top).sort((x, y) => x - y); let zeilen = 0, vor = -1e9; for (const v of tt) { if (v - vor >= 4) zeilen++; vor = v; }   // Häufung der Oberkanten wie vorher (Abstand unter 4 px = dieselbe Zeile), nur sortiert statt quadratisch   // Zeilen aus der Lage des Textes, nicht aus der Höhe (Knöpfe haben Innenabstand)
    if ((n >= 8 && zeilen >= n * .6) || (e.matches('a,button') && zeilen >= 3 && r.width < 160)) { fund(2, 'spalte', e, `Text zerfällt: ${n} Wörter auf ${zeilen} Zeilen, Breite ${Math.round(r.width)} px`); } }

  // K18 Substanz: «n Vorlagen» mit n < 4
  for (const e of sichtbar) { const own = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' '); const m = own.match(/\b(\d+)\s+(Vorlagen|VORLAGEN|Vorlage|VORLAGE)\b/);
    if (m && +m[1] > 0 && +m[1] < 4) { const kachel = e.closest('[class*="wo"],[class*="kachel"],[class*="karte"],button,a') || e; fund(18, 'substanz', kachel, `nur ${m[1]} ${m[2]}: «${(kachel.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 40)}»`); } }

  return { funde: F, doks: dokListe.slice(0, 12), bilder: pruefBild };
};
