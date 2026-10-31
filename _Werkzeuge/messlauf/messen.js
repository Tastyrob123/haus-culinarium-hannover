// Messlauf · Messfunktion, läuft im Browser (page.evaluate). Findet in einem Zustand:
//  ueberlauf  – Text breiter/höher als sein Kasten oder ausserhalb des Kastens
//  rand       – Text näher als 6 px am linken/rechten Rand von Knopf oder Kachel
//  wort       – Wort abgeschnitten (Kasten schneidet ab) oder ohne Trennstrich mitten im Wort umgebrochen
//  oval       – Symbol-Knopf / Knauf / runder Knopf nicht kreisrund (Breite ≠ Höhe um mehr als 1 px)
//  reihe      – Kacheln einer Reihe: Oberkante, Höhe oder Titel (Lage, Grösse) ungleich
//  ueberlappt – zwei Text- oder Knopf-Elemente überdecken sich
//  anschnitt  – Element vom Bildschirmrand angeschnitten, Seite verrutscht seitlich
//  beschnitten – Plakat/Motiv/Wortmarke im Bild mit object-fit:cover in einem Kasten anderer Form (Abweichung > 2 %): die Schrift im Bild wird abgeschnitten
//  einzelwort – Titel, dessen letzte Zeile nur ein Wort ist (z. B. «2026» allein in der zweiten Zeile)
//  text-mitte – Schrift (bzw. Symbol) in Knopf, Pille, Etikett, Rundknopf sitzt nicht optisch mittig: Mitte der Glyphen (canvas measureText,
//               actualBoundingBox) weicht senkrecht mehr als 0,5 px von der Mitte des Kastens ab, bei zentrierten Knöpfen auch waagrecht
//  zier-x     – «x» oder «×» als Zier- oder Trennzeichen (Pseudo-Element, allein stehend, zwischen Wörtern); erlaubt nur in Namen («Momo x Rudi») und als Schliessen-Knopf
module.exports = function messen() {
  const VW = innerWidth, VH = innerHeight, F = [];
  document.querySelectorAll('[data-ml-f]').forEach(e => e.removeAttribute('data-ml-f'));
  // Abschnitte mit content-visibility:auto für die Messung ganz auslegen (so stehen sie, sobald man hinrollt)
  let cvStil = document.getElementById('ml-cv'); if (!cvStil) { cvStil = document.createElement('style'); cvStil.id = 'ml-cv'; cvStil.setAttribute('data-messlauf-aus', ''); cvStil.textContent = '*{content-visibility:visible!important}'; document.head.appendChild(cvStil); }
  // Ein Stil-Objekt je Element (live, zeigt also immer den aktuellen Stand): sonst legt WebKit bei jedem Aufruf ein neues an,
  // auf der Werkbank (3000 Elemente, Abschnitt 4 paarweise) 800 MB mehr und der Tab stürzt ab (cu-werkbank, 30.10.2026)
  const CS = new Map(); const cs = e => { let c = CS.get(e); if (!c) { c = getComputedStyle(e); CS.set(e, c); } return c; };
  const sicht = e => {
    if (!e.isConnected) return false;
    if (e.checkVisibility) { if (!e.checkVisibility({ contentVisibilityAuto: true, opacityProperty: true, visibilityProperty: true })) return false; if (e.closest('details:not([open])') && !e.closest('summary')) return false; return true; }
    if (e.closest('details:not([open])') && !e.closest('summary')) return false;
    const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false;
    for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const c = cs(x); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false; }
    return true;
  };
  const pfad = e => { const p = []; for (let x = e; x && x !== document.body && p.length < 4; x = x.parentElement) {
      let t = x.tagName.toLowerCase(); if (x.id) { p.unshift(t + '#' + x.id); break; }
      const k = typeof x.className === 'string' ? x.className.trim().split(/\s+/).filter(c => c && !/^(an|ist-|da|sicht|js-|offen|aktiv|auf)$/.test(c)).slice(0, 2) : [];
      if (k.length) t += '.' + k.join('.'); p.unshift(t); } return p.join(' > '); };
  const ebene = e => { for (let x = e; x && x !== document.body; x = x.parentElement) { const p = cs(x).position; if (p === 'fixed' || p === 'sticky') return x; } return null; };
  const kastenSichtbar = e => { const c = cs(e); return (c.backgroundColor !== 'rgba(0, 0, 0, 0)' && c.backgroundColor !== 'transparent') || c.backgroundImage !== 'none' || (parseFloat(c.borderLeftWidth) > 0 && parseFloat(c.borderRightWidth) > 0); };
  const ausschnitt = (e, r) => { r = r || e.getBoundingClientRect(); let l = r.left, t = r.top, rr = r.right, b = r.bottom;
    for (let x = e.parentElement; x && x !== document.documentElement; x = x.parentElement) { const c = cs(x);
      if (c.overflowX !== 'visible' || c.overflowY !== 'visible' || c.clipPath !== 'none') { const q = x.getBoundingClientRect();
        if (c.overflowX !== 'visible') { l = Math.max(l, q.left); rr = Math.min(rr, q.right); } if (c.overflowY !== 'visible') { t = Math.max(t, q.top); b = Math.min(b, q.bottom); } }
      if (c.position === 'fixed') break; }
    return { left: l, top: t, right: rr, bottom: b, width: Math.max(0, rr - l), height: Math.max(0, b - t) }; };
  const text = e => (e.innerText || e.getAttribute('aria-label') || e.title || '').trim().replace(/\s+/g, ' ').slice(0, 60);
  const rect = e => { const r = e.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const mark = (e, i) => { if (e && e.setAttribute) e.setAttribute('data-ml-f', ((e.getAttribute('data-ml-f') || '') + ' f' + i).trim()); };
  const fund = (art, e, info, extra) => mark(e, F.length) || F.push({ art, sel: pfad(e), text: text(e), info, r: rect(e), fest: !!ebene(e) && cs(ebene(e)).position === 'fixed', ...(extra || {}) });
  const istKnopf = e => e.matches('button,a[class*="kn"],a[class*="knopf"],[role=button],[role=tab],.wo-kn,.knopf,input[type=submit],input[type=button]');
  const hatFlaeche = e => { const c = cs(e); return (c.backgroundColor !== 'rgba(0, 0, 0, 0)' && c.backgroundColor !== 'transparent') || c.backgroundImage !== 'none' || parseFloat(c.borderLeftWidth) > 0 || parseFloat(c.borderTopWidth) > 0 || c.boxShadow !== 'none'; };
  const istKachel = e => /k[aä]chel|karte|kart\b|tile|card|wo-bk|wo-ag|wo-kc|tafel|kasten/i.test(typeof e.className === 'string' ? e.className : '') && hatFlaeche(e) && !e.querySelector('input,textarea,select');
  const scroller = e => { for (let x = e.parentElement; x && x !== document.body; x = x.parentElement) { const c = cs(x); if (/(auto|scroll)/.test(c.overflowX) && x.scrollWidth > x.clientWidth + 1) return x; } return null; };
  const alle = [...document.body.querySelectorAll('*')].filter(e => !/^(SCRIPT|STYLE|SVG|PATH|NOSCRIPT|IFRAME|CANVAS|VIDEO|OPTION|BR|HTML|HEAD|META|LINK|TEMPLATE|G|USE|CIRCLE|RECT|LINE|POLYLINE|POLYGON|ELLIPSE|DEFS|SYMBOL|TEXT|TSPAN)$/i.test(e.tagName) && !e.closest('[data-messlauf-aus],.ml-rahmen'));
  const sichtbar = alle.filter(sicht);
  const S = new Set(sichtbar);

  // Kasten eines Textes: nächster Knopf oder Kachel (Fläche), sonst das Element selbst
  const kastenVon = e => { for (let x = e; x && x !== document.body; x = x.parentElement) { if (istKnopf(x) || istKachel(x) || (x.tagName === 'LABEL' && hatFlaeche(x))) return x; } return null; };

  const gesehenUe = new Set();
  for (const e of sichtbar) {
    const c = cs(e);
    const tn = [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim().length > 0);
    // 1 eigener Text, Kasten schneidet ab (overflow hidden/clip/auto und Inhalt grösser)
    if (tn.length || (e.matches('input,textarea,select') && (e.value || e.placeholder))) {
      const zu = /(hidden|clip)/.test(c.overflowX) || /(hidden|clip)/.test(c.overflowY) || e.matches('input,select');
      const er = e.getBoundingClientRect();
      if (zu && er.width > 4 && er.height > 4) {
        if (e.matches('input,select')) { if (e.scrollWidth > e.clientWidth + 1) { fund('gekuerzt', e, `Eingabe ${e.scrollWidth} px in Feld ${e.clientWidth} px`); gesehenUe.add(e); } }
        else { const pl = er.left + e.clientLeft, pr = pl + e.clientWidth, po = er.top + e.clientTop, pu = po + e.clientHeight; let breit = 0, aus = 0;
          for (const n of tn) { const rg = document.createRange(); rg.selectNodeContents(n); for (const q of rg.getClientRects()) { if (q.width < 1) continue; breit = Math.max(breit, q.right - pl);
            const innen = q.right > pl && q.left < pr && q.bottom > po && q.top < pu; if (innen && (q.right > pr + 1 || q.left < pl - 1 || q.bottom > pu + 2)) aus++; } }
          if (aus && tn.map(n => n.textContent.trim()).join('').length <= 2) aus = 0;
          if (aus) { fund(c.textOverflow === 'ellipsis' ? 'gekuerzt' : 'ueberlauf', e, `Text ${Math.round(breit)} px breit in Kasten ${e.clientWidth}×${e.clientHeight}, abgeschnitten` + (c.textOverflow === 'ellipsis' ? ' (mit …)' : '')); gesehenUe.add(e); } }
      }
    }
    if (!tn.length) continue;
    const kasten = kastenVon(e); if (!kasten || !S.has(kasten)) continue;
    const kr = kasten.getBoundingClientRect(); if (kr.width > VW * 0.92) continue;
    const kc = cs(kasten);
    const innen = { l: kr.left + parseFloat(kc.borderLeftWidth), r: kr.right - parseFloat(kc.borderRightWidth), o: kr.top + parseFloat(kc.borderTopWidth), u: kr.bottom - parseFloat(kc.borderBottomWidth) };
    let minL = 1e9, minR = 1e9, raus = null, brueche = [];
    // versteckter Text für Vorleser (clip-Muster, Fläche unter 2 px) zählt weder für «rand» noch für «ueberlauf» (30.10.2026, «Website ansehen» bei 1000 px)
    const vorleser = pe => { for (let x = pe; x && x !== kasten.parentElement; x = x.parentElement) { const c = cs(x), r = x.getBoundingClientRect(); if (x !== kasten && (r.width < 2 || r.height < 2)) return true; if (/absolute|fixed/.test(c.position) && c.clip && c.clip !== 'auto') return true; if (/^inset\((50|100)%/.test(c.clipPath)) return true; } return false; };
    for (const n of tn) {
      if (vorleser(n.parentElement)) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const q0 of rg.getClientRects()) { if (q0.width < 1) continue;
        let q1 = q0; { const pe = n.parentElement, pc = cs(pe); if (/(hidden|clip)/.test(pc.overflowX)) { const pr = pe.getBoundingClientRect(); const l = pr.left + parseFloat(pc.borderLeftWidth) + parseFloat(pc.paddingLeft), r = pr.right - parseFloat(pc.borderRightWidth) - parseFloat(pc.paddingRight); q1 = { left: Math.max(q0.left, l), right: Math.min(q0.right, r), top: q0.top, bottom: q0.bottom, width: Math.max(0, Math.min(q0.right, r) - Math.max(q0.left, l)), height: q0.height }; } }   // Text hinter «…» ist nicht sichtbar
        const q = ausschnitt(n.parentElement, q1); if (q.width < 1 || q.height < 1) continue;   // versteckt (z. B. Bildzeile, die erst beim Überfahren kommt)
        minL = Math.min(minL, q.left - innen.l); minR = Math.min(minR, innen.r - q.right);
        if (q.right > innen.r + 0.5 || q.left < innen.l - 0.5 || q.bottom > innen.u + 1.5 || q.top < innen.o - 1.5) raus = q; }
      // Wort ohne Trennstrich über zwei Zeilen
      if (cs(n.parentElement).hyphens !== 'auto') { const t = n.textContent; const re = /[A-Za-zÄÖÜäöüß]{4,}/g; let m;
        while ((m = re.exec(t))) { const w = document.createRange(); w.setStart(n, m.index); w.setEnd(n, m.index + m[0].length);
          const zs = [...w.getClientRects()].filter(q => q.width > 0.5); if (!(zs.length > 1 && Math.abs(zs[0].top - zs[zs.length - 1].top) > 2)) continue;
          // genau prüfen: bricht die Zeile zwischen zwei Buchstaben dieses Wortes? (30.10.2026: «3-Gänge-/Menü» bricht am Bindestrich, das ist erlaubt)
          let oben = null, mitten = false; for (let i = 0; i < m[0].length; i++) { const z = document.createRange(); z.setStart(n, m.index + i); z.setEnd(n, m.index + i + 1); const q = [...z.getClientRects()].filter(x => x.width > 0.2)[0]; if (!q) continue; if (oben !== null && Math.abs(q.top - oben) > 2) { mitten = true; break; } oben = q.top; }
          if (mitten) brueche.push(m[0]); } }
    }
    if (raus && /(hidden|clip)/.test(kc.overflowX + kc.overflowY) && (raus.left >= innen.r || raus.right <= innen.l || raus.top >= innen.u || raus.bottom <= innen.o)) raus = null;
    const kurzZeichen = tn.map(n => n.textContent.trim()).join('').length <= 2;
    if (raus && kurzZeichen) raus = null;
    if (raus && [e, ...e.querySelectorAll('*')].concat([kasten]).some(x => cs(x).webkitLineClamp && cs(x).webkitLineClamp !== 'none')) { if (!gesehenUe.has(kasten)) { gesehenUe.add(kasten); fund('gekuerzt', kasten, 'Text mit … gekürzt (Zeilenbegrenzung)'); } raus = null; }
    if (raus && !gesehenUe.has(kasten)) { gesehenUe.add(kasten); fund('ueberlauf', kasten, `Text ragt aus dem Kasten (${Math.round(raus.left - innen.l)}…${Math.round(raus.right - innen.l)} px bei Breite ${Math.round(innen.r - innen.l)})`); }
    else if ((istKnopf(kasten) || (istKachel(kasten) && kr.width <= 420 && kr.height <= 320)) && kastenSichtbar(kasten) && Math.min(minL, minR) < 6 && Math.min(minL, minR) > -0.5) {
      // Knopf/Kachel: Text näher als 6 px am Rand (nur seitlich, Text sitzt nicht absichtlich bündig: Kasten hat Polster > 0 oder ist zentriert)
      const kn = kastenVon(e); const key = 'rand' + pfad(kn);
      if (!gesehenUe.has(key)) { gesehenUe.add(key); fund('rand', kn, `Text ${Math.round(minL)} px vom linken, ${Math.round(minR)} px vom rechten Rand`); }
    }
    if (brueche.length) fund('wort', e, 'Wort ohne Trennstrich umgebrochen: ' + [...new Set(brueche)].slice(0, 3).join(', '));
  }

  // 2 runde Knöpfe und Knäufe
  for (const e of sichtbar) {
    const r = e.getBoundingClientRect(), c = cs(e); const w = r.width, h = r.height;
    if (Math.max(w, h) > 96 || Math.min(w, h) < 8) continue;
    const rad = c.borderTopLeftRadius; const radPx = rad.endsWith('%') ? parseFloat(rad) / 100 * Math.min(w, h) : parseFloat(rad);
    const prozent = rad.endsWith('%') && parseFloat(rad) >= 50;
    const ohneText = !(e.innerText || '').trim();
    const nurSymbol = (istKnopf(e) || e.matches('a[href],[class*="rund"]')) && ohneText && e.querySelector('svg,i') && !e.querySelector('img,picture,video');
    const rund = prozent || radPx >= Math.min(w, h) / 2 - 0.5;
    const flaeche = hatFlaeche(e);
    const knauf = !istKnopf(e) && ohneText && e.parentElement && e.parentElement.closest('button,a,[role=button]') && e.querySelector('svg');
    if (((nurSymbol && (rund || flaeche)) || (knauf && rund && flaeche)) && Math.abs(w - h) > 1) {
      if (e.closest('label:has(input[type=checkbox]),[role=switch],[class*="schalter"],[class*="switch"],[class*="toggle"]') || e.querySelector('button,a,[role=button]')) continue;
      if (e.matches('input[type=range]') || /(linie|strich|balken|bar|track|regler|schieber|punkt-leiste)/i.test(e.className)) continue;
      fund('oval', e, `${w.toFixed(1)} × ${h.toFixed(1)} px, Radius ${rad}`);
    }
  }

  // 3 Kacheln einer Reihe
  const gruppen = new Map();
  for (const e of sichtbar) { if (!e.parentElement || !(istKachel(e) || (istKnopf(e) && e.offsetWidth > 120 && e.offsetHeight > 70))) continue;
    const key = e.parentElement; if (!gruppen.has(key)) gruppen.set(key, []); gruppen.get(key).push(e); }
  for (const [eltern, ks] of gruppen) {
    const zeilen = []; for (const e of ks) { const r = e.getBoundingClientRect(); let z = zeilen.find(z => Math.abs(z.top - r.top) < 24); if (!z) zeilen.push(z = { top: r.top, bottom: r.bottom, el: [] }); z.el.push(e); }
    for (const z of zeilen) { if (z.el.length < 2) continue;
      const klassen = new Set(z.el.map(e => e.className)); if (klassen.size > 1) continue;
      const rs = z.el.map(e => e.getBoundingClientRect());
      if (Math.max(...rs.map(r => r.width)) - Math.min(...rs.map(r => r.width)) > 2) continue;
      const lage = e => { let t = 0; for (let x = e; x && x !== eltern; x = x.offsetParent) t += x.offsetTop; return t; };
      const oben = z.el.map(lage), hoch = z.el.map(e => e.offsetHeight);
      const sp = a => Math.max(...a) - Math.min(...a);
      const tit = z.el.map(e => { const t = e.querySelector('h1,h2,h3,h4,h5,[class*="titel"],[class*="__t"]:not([class*="__tx"])'); if (!t || !sicht(t)) return null;
        const rg = document.createRange(); rg.selectNodeContents(t); const qs = [...rg.getClientRects()].filter(q => q.width > 0); if (!qs.length) return null; const top = e.getBoundingClientRect().top;
        return { dy: qs[0].bottom - top, dl: qs[qs.length - 1].bottom - top, fs: parseFloat(cs(t).fontSize) }; });
      const tt = tit.filter(Boolean); const probleme = [];
      if (sp(oben) > 1) probleme.push(`Oberkante ±${sp(oben).toFixed(1)} px`);
      if (sp(hoch) > 1) probleme.push(`Höhe ${Math.round(Math.min(...hoch))}–${Math.round(Math.max(...hoch))} px`);
      if (tt.length === z.el.length && sp(tt.map(t => t.dy)) > 1.5 && sp(tt.map(t => t.dl)) > 1.5) probleme.push(`Titel-Grundlinie ±${Math.min(sp(tt.map(t => t.dy)), sp(tt.map(t => t.dl))).toFixed(1)} px`);
      if (tt.length === z.el.length && sp(tt.map(t => t.fs)) > 0.5) probleme.push(`Titelgrösse ${Math.min(...tt.map(t => t.fs))}–${Math.max(...tt.map(t => t.fs))} px`);
      if (probleme.length) { const e = z.el[0]; z.el.forEach(x => mark(x, F.length)); const r0 = rs.reduce((a, r) => ({ l: Math.min(a.l, r.left), t: Math.min(a.t, r.top), r: Math.max(a.r, r.right), b: Math.max(a.b, r.bottom) }), { l: 1e9, t: 1e9, r: -1e9, b: -1e9 });
        F.push({ art: 'reihe', sel: pfad(e), text: z.el.map(text).map(t => t.slice(0, 18)).join(' | '), info: probleme.join(', ') + ` (${z.el.length} Kacheln)`, r: { x: Math.round(r0.l), y: Math.round(r0.t), w: Math.round(r0.r - r0.l), h: Math.round(r0.b - r0.t) } }); }
    }
  }

  // 4 Überschneidungen: Text- und Knopf-Elemente
  const blatt = sichtbar.filter(e => (istKnopf(e) || [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1)) && cs(e).position !== 'fixed' && !e.closest('[aria-hidden="true"]'));
  const kaesten = [];
  for (const e of blatt) { const eig = e.getBoundingClientRect(); const ce = cs(e); const schneidet = /(hidden|clip)/.test(ce.overflowX + ce.overflowY);
    if (istKnopf(e)) { const r = ausschnitt(e, eig); if (r.width > 2 && r.height > 2) kaesten.push({ e, r, knopf: true }); continue; }
    for (const n of [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim())) { const rg = document.createRange(); rg.selectNodeContents(n);
      for (let q of rg.getClientRects()) { if (schneidet) q = { left: Math.max(q.left, eig.left), right: Math.min(q.right, eig.right), top: Math.max(q.top, eig.top), bottom: Math.min(q.bottom, eig.bottom) };
        const r = ausschnitt(e, { left: q.left, top: q.top, right: q.right, bottom: q.bottom, width: q.right - q.left, height: q.bottom - q.top }); if (r.width > 2 && r.height > 2) kaesten.push({ e, r }); } } }
  // 4b Zeichen aus ::before/::after (Anführungszeichen, Zier) als eigene Kästen (Oberchef 30.10.2026: im Gästebuch lag ein «
  //    unbemerkt über dem Titel). Nur Zeichen mit sichtbarem Text und absolut gesetzt (im Textfluss kann nichts überdecken);
  //    gemessen wird die Tinte der Zeichen (canvas measureText), nicht der Zeilenkasten. Kommt auch in die Randprüfung.
  const zeichen = [];
  { const cv = document.createElement('canvas').getContext('2d');
    for (const e of sichtbar) { if (cs(e).position === 'fixed' || e.closest('[aria-hidden="true"]') || /^(INPUT|TEXTAREA|SELECT|IMG)$/.test(e.tagName)) continue;
      for (const ps of ['::before', '::after']) { const pc = getComputedStyle(e, ps); const roh = pc.content;
        if (!roh || roh === 'none' || roh === 'normal' || !/^["']/.test(roh)) continue;
        // nur die Zeichenketten vor einem Alternativtext (content: "x" / "")
        let t = '', rest = roh.trim(); for (let m; (m = rest.match(/^("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')\s*/)); rest = rest.slice(m[0].length)) t += m[1].slice(1, -1).replace(/\\(.)/g, '$1');
        // Kopie des eigenen Wortes als Leuchten oder Schatten (Neon auf der Bar-Seite): gewollt deckungsgleich, kein Fund
        if (t.trim().toLowerCase() === (e.textContent || '').trim().replace(/\s+/g, ' ').toLowerCase()) continue;
        if (!t.trim() || pc.display === 'none' || pc.visibility === 'hidden' || +pc.opacity < 0.05 || !/^(absolute)$/.test(pc.position)) continue;
        // Bezugskasten: nächster positionierter Vorfahr ab dem Element selbst (Polsterkante)
        let cb = e; while (cb && cb !== document.body && cs(cb).position === 'static' && !(cs(cb).transform && cs(cb).transform !== 'none')) cb = cb.parentElement;
        if (!cb) continue; const cr = cb.getBoundingClientRect(), cc = cs(cb);
        const ox = cr.left + parseFloat(cc.borderLeftWidth), oy = cr.top + parseFloat(cc.borderTopWidth);
        const w = parseFloat(pc.width), h = parseFloat(pc.height); if (!(w > 0) || !(h > 0)) continue;
        let x = parseFloat(pc.left), y = parseFloat(pc.top);
        if (isNaN(x)) { const rr = parseFloat(pc.right); if (isNaN(rr)) continue; x = cr.width - parseFloat(cc.borderLeftWidth) - parseFloat(cc.borderRightWidth) - rr - w - parseFloat(pc.marginLeft) - parseFloat(pc.marginRight); }
        if (isNaN(y)) { const bb = parseFloat(pc.bottom); if (isNaN(bb)) continue; y = cr.height - parseFloat(cc.borderTopWidth) - parseFloat(cc.borderBottomWidth) - bb - h - parseFloat(pc.marginTop) - parseFloat(pc.marginBottom); }
        x += parseFloat(pc.marginLeft) || 0; y += parseFloat(pc.marginTop) || 0;
        const m = (pc.transform || '').match(/matrix\(([^)]+)\)/); if (m) { const v = m[1].split(',').map(parseFloat); if (Math.abs(v[1]) > 0.01) continue; x += v[4]; y += v[5]; }
        const tr = (pc.translate || 'none'); if (tr !== 'none') { const v = tr.split(/\s+/).map(parseFloat); if (!isNaN(v[0]) && !/%/.test(tr)) { x += v[0]; y += v[1] || 0; } }
        // Tinte: Zeilenkasten → Grundlinie, dann Glyphen
        const tt = pc.textTransform === 'uppercase' ? t.toUpperCase() : t;
        cv.font = `${pc.fontStyle} ${pc.fontWeight} ${pc.fontSize} ${pc.fontFamily}`; try { cv.letterSpacing = pc.letterSpacing === 'normal' ? '0px' : pc.letterSpacing; } catch (q) {}
        const g = cv.measureText(tt); const fs = parseFloat(pc.fontSize); const lh = pc.lineHeight === 'normal' ? (g.fontBoundingBoxAscent + g.fontBoundingBoxDescent) : parseFloat(pc.lineHeight);
        const pl = parseFloat(pc.paddingLeft) + parseFloat(pc.borderLeftWidth), pt = parseFloat(pc.paddingTop) + parseFloat(pc.borderTopWidth);
        const ib = w - pl - parseFloat(pc.paddingRight) - parseFloat(pc.borderRightWidth);
        const ausr = pc.textAlign === 'center' ? (ib - g.width) / 2 : /right|end/.test(pc.textAlign) ? ib - g.width : 0;
        const asc = g.fontBoundingBoxAscent, des = g.fontBoundingBoxDescent; const grund = oy + y + pt + (lh - (asc + des)) / 2 + asc;
        const l0 = ox + x + pl + ausr;
        const r = { left: l0 - g.actualBoundingBoxLeft, right: l0 + g.actualBoundingBoxRight, top: grund - g.actualBoundingBoxAscent, bottom: grund + g.actualBoundingBoxDescent };
        r.width = r.right - r.left; r.height = r.bottom - r.top; if (r.width < 1 || r.height < 1 || fs < 6) continue;
        const q = ausschnitt(e, r); const ec = cs(e); let z = q;
        if (/(hidden|clip)/.test(ec.overflowX + ec.overflowY)) { const er = e.getBoundingClientRect(); z = { left: Math.max(q.left, er.left), right: Math.min(q.right, er.right), top: Math.max(q.top, er.top), bottom: Math.min(q.bottom, er.bottom) }; z.width = z.right - z.left; z.height = z.bottom - z.top; }
        if (z.width > 1 && z.height > 1) { const k = { e, r: z, ps, t }; zeichen.push(k); kaesten.push(k); } } }
  }
  // Zeichen in Knopf oder Kachel: dieselbe Randregel wie für Text (näher als 6 px am linken/rechten Rand)
  for (const k of zeichen) { const kasten = kastenVon(k.e); if (!kasten || !S.has(kasten) || !kastenSichtbar(kasten)) continue;
    const kr = kasten.getBoundingClientRect(); if (kr.width > VW * 0.92 || !(istKnopf(kasten) || (istKachel(kasten) && kr.width <= 420 && kr.height <= 320))) continue;
    const kc = cs(kasten); const il = kr.left + parseFloat(kc.borderLeftWidth), ir = kr.right - parseFloat(kc.borderRightWidth);
    const mi = Math.min(k.r.left - il, ir - k.r.right); const key = 'rand' + pfad(kasten);
    if (mi < 6 && mi > -0.5 && !gesehenUe.has(key)) { gesehenUe.add(key); fund('rand', kasten, `Zeichen «${k.t}» (${k.ps}) ${Math.round(k.r.left - il)} px vom linken, ${Math.round(ir - k.r.right)} px vom rechten Rand`); } }
  const zweimal = new Set();
  // Nur Paare, die sich überhaupt schneiden: nach Oberkante sortiert, je Kasten nur die, die oben vor seiner Unterkante beginnen
  // (vorher jedes Paar mit Elternkette, 30.10.2026); geprüft wird danach in derselben Reihenfolge wie zuvor (i < j)
  const nachOben = kaesten.map((k, i) => i).sort((x, y) => kaesten[x].r.top - kaesten[y].r.top), paare = [];
  for (let p = 0; p < nachOben.length; p++) { const A = kaesten[nachOben[p]].r;
    for (let q = p + 1; q < nachOben.length; q++) { const B = kaesten[nachOben[q]].r; if (B.top >= A.bottom - 3) break;
      if (Math.min(A.right, B.right) - Math.max(A.left, B.left) > 3) paare.push(nachOben[p] < nachOben[q] ? [nachOben[p], nachOben[q]] : [nachOben[q], nachOben[p]]); } }
  paare.sort((x, y) => x[0] - y[0] || x[1] - y[1]);
  const merke = f => { const m = new Map(); return x => { if (!m.has(x)) m.set(x, f(x)); return m.get(x); }; };
  const ebeneM = merke(ebene);
  for (const [i, j] of paare) {
    const a = kaesten[i], b = kaesten[j];
    // Zeichen gegen Text: auch der eigene Text des Elements zählt (das « im Gästebuch lag über seinem eigenen Titel); nur Knopfkästen, in denen das Zeichen steht, nicht
    if (a.ps || b.ps) { if (a.ps && b.ps && a.e === b.e && a.ps === b.ps) continue; const o = a.ps ? b : a, z = a.ps ? a : b; if (!o.ps && o.knopf && (o.e.contains(z.e) || z.e.contains(o.e))) continue; }
    else if (a.e.contains(b.e) || b.e.contains(a.e)) continue;
    if (ebeneM(a.e) !== ebeneM(b.e)) continue;
    const overlay = x => { for (let y = x; y && y !== document.body; y = y.parentElement) { const c = cs(y); if ((c.position === 'absolute' || c.position === 'fixed') && (parseInt(c.zIndex) || 0) >= 5) { const r = y.getBoundingClientRect(); if (r.width * r.height >= 0.25 * VW * VH) return y; } } return null; };
    if (overlay(a.e) !== overlay(b.e)) continue;
    const gedreht = x => { for (let y = x, n = 0; y && n < 4; y = y.parentElement, n++) { const m = cs(y).transform; if (m && m !== 'none') { const v = m.match(/matrix\(([^)]+)\)/); if (v && Math.abs(parseFloat(v[1].split(',')[1])) > 0.01) return true; } } return false; };
    if (gedreht(a.e) || gedreht(b.e)) continue;
    const ix = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left), iy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
    if (ix > 3 && iy > 3 && ix * iy > 24 && iy > 0.3 * Math.min(a.r.height, b.r.height)) { const pa = pfad(a.e) + (a.ps || ''), pb = pfad(b.e) + (b.ps || ''); const k = pa + '|' + pb; if (zweimal.has(k)) continue; zweimal.add(k); mark(a.e, F.length); mark(b.e, F.length);
      F.push({ art: 'ueberlappt', sel: pa, text: (a.ps ? a.ps + ' ' + a.t : text(a.e).slice(0, 30)) + ' ⟷ ' + (b.ps ? b.ps + ' ' + b.t : text(b.e).slice(0, 30)), info: `überdeckt ${pb} (${Math.round(ix)}×${Math.round(iy)} px)`, r: { x: Math.round(Math.min(a.r.left, b.r.left)), y: Math.round(Math.min(a.r.top, b.r.top)), w: Math.round(Math.max(a.r.right, b.r.right) - Math.min(a.r.left, b.r.left)), h: Math.round(Math.max(a.r.bottom, b.r.bottom) - Math.min(a.r.top, b.r.top)) } }); }
  }

  // 6 Plakate und Motive mit Schrift: Seitenverhältnis Bild gegen Kasten
  const PLAKAT_DATEI = /^(pl_|plakat|poster|motiv|vorlage|wortmarke|logo|flyer|einladung)|[_-](plakat|poster|motiv|wortmarke|logo)[_.-]/i, PLAKAT_ALT = /^(das |ein |the |a )?([\w-]*-)?(plakat|poster|wortmarke)\b/i;
  for (const e of sichtbar) { if (e.tagName !== 'IMG' || !e.naturalWidth || !e.naturalHeight) continue;
    const datei = decodeURIComponent((e.currentSrc || e.src || '').split('?')[0].split('/').pop());
    const quelle = datei + ' ' + (e.alt || '');
    if (!(PLAKAT_DATEI.test(datei) || PLAKAT_ALT.test(e.alt || '') || e.closest('[data-plakat],[class*="plakat"]'))) continue;
    if (/plakatwand|plakate|wand mit|an der wand/i.test(e.alt || '') || /wand|plakate/i.test(datei)) continue;   // Foto einer Plakatwand: ein Foto, kein einzelnes Plakat
    const c = cs(e); if (c.objectFit !== 'cover' && c.objectFit !== 'fill') continue;
    const r = e.getBoundingClientRect(); if (r.width < 24 || r.height < 24) continue;
    const bild = e.naturalWidth / e.naturalHeight, kasten = r.width / r.height, ab = Math.abs(bild / kasten - 1);
    if (ab > 0.02) fund('beschnitten', e, `Bild ${e.naturalWidth}×${e.naturalHeight} (${bild.toFixed(3)}) in Kasten ${Math.round(r.width)}×${Math.round(r.height)} (${kasten.toFixed(3)}), object-fit ${c.objectFit}: ${Math.round(ab * 100)} % ${c.objectFit === 'cover' ? 'abgeschnitten' : 'verzerrt'}`, { quelle }); }
  // 7 Titel mit einem einzelnen Wort in der letzten Zeile
  for (const e of sichtbar) { if (!e.matches('h1,h2,h3,h4,h5,[class*="titel"],[class*="__t"],figcaption,.wo-sb__h,.wo-zw') || e.closest('nav,aside') || e.querySelector('p,small + span,br + span')) continue;
    const t = (e.innerText || '').trim(); const woerter = t.split(/\s+/).filter(Boolean); if (woerter.length < 3 || t.length > 90) continue;
    const rg = document.createRange(); rg.selectNodeContents(e); const zeilen = [...new Set([...rg.getClientRects()].filter(q => q.width > 1).map(q => Math.round(q.bottom)))].sort((a, b) => a - b);
    if (zeilen.length < 2 || zeilen.length > 3) continue;
    // Wörter der letzten Zeile zählen
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n, letzte = [];
    while ((n = tw.nextNode())) { const re = /\S+/g; let m; while ((m = re.exec(n.textContent))) { const w = document.createRange(); w.setStart(n, m.index); w.setEnd(n, m.index + m[0].length); const q = [...w.getClientRects()].pop(); if (q && Math.abs(Math.round(q.bottom) - zeilen[zeilen.length - 1]) <= 2) letzte.push(m[0]); } }
    // ausgewogen umbrochen (letzte Zeile mindestens 60 % der längsten, z. B. «In den Hausregeln / nachschlagen.») ist kein Einzelwort (30.10.2026)
    const sp = {}; for (const q of rg.getClientRects()) if (q.width > 1) { const z = Math.round(q.bottom); sp[z] = sp[z] ? [Math.min(sp[z][0], q.left), Math.max(sp[z][1], q.right)] : [q.left, q.right]; }
    const breite = z => sp[z] ? sp[z][1] - sp[z][0] : 0; const quote = breite(zeilen[zeilen.length - 1]) / Math.max(...zeilen.map(breite));
    if (letzte.length === 1 && letzte[0].length < 14 && quote < 0.6) fund('einzelwort', e, `«${letzte[0]}» steht allein in der letzten Zeile (${zeilen.length} Zeilen)`); }

  // 8 «x» als Zier- oder Trennzeichen (Kriterium 24, Robert 29.10.2026)
  const NAMEN = /^(momo|rudi|christoph|derya|nate|culinarium)$/i, X = /^[x×✕✖]$/;
  const schliessen = e => !!e.closest('button,[role=button],a') && /schlie|close|zu\b|weg/i.test((e.closest('button,[role=button],a').getAttribute('aria-label') || '') + ' ' + (e.closest('button,[role=button],a').className || ''));
  for (const e of sichtbar) {
    for (const ps of ['::before', '::after']) { const c = getComputedStyle(e, ps).content; if (c && /^["'][\s]*[x×✕✖][\s]*["']$/.test(c) && !schliessen(e)) fund('zier-x', e, `«${c.replace(/["']/g, '').trim()}» als Zierzeichen in ${ps}`); }
    for (const n of [...e.childNodes].filter(n => n.nodeType === 3)) { const t = n.textContent; const w = t.split(/\s+/).filter(Boolean);
      if (w.length === 1 && X.test(w[0]) && !schliessen(e)) { fund('zier-x', e, `«${w[0]}» steht allein als Zeichen`); continue; }
      for (let i = 1; i < w.length - 1; i++) if (X.test(w[i]) && !(NAMEN.test(w[i - 1].replace(/\W+$/, '')) || NAMEN.test(w[i + 1].replace(/^\W+/, ''))) && !(/\d\W*$/.test(w[i - 1]) && /^\W*\d/.test(w[i + 1]))) { fund('zier-x', e, `«${w[i - 1]} ${w[i]} ${w[i + 1]}»: x als Trenner`); break; } }
  }

  // 8b gedrehte Kreuze (30.10.2026, Robert: «das X hat auf der ganzen Seite nichts zu suchen»; das Fuss-× war ein um 45° gedrehtes «+»)
  { const winkel = tf => { if (!tf || tf === 'none') return 0; const m = tf.match(/matrix\(([^)]+)\)/); if (!m) return 0; const [a, b] = m[1].split(',').map(parseFloat); return Math.atan2(b, a) * 180 / Math.PI; };
    const schraeg = w => { const r = ((Math.abs(w) % 90) + 90) % 90; return r > 30 && r < 60; };
    const drehung = (e, ps) => { const c = getComputedStyle(e, ps); let w = winkel(c.transform); if (c.rotate && c.rotate !== 'none') w += parseFloat(c.rotate) || 0; return w; };
    const vorfahrDreh = e => { let w = 0; for (let x = e; x && x !== document.body; x = x.parentElement) w += drehung(x); return w; };
    for (const e of sichtbar) { if (schliessen(e)) continue;
      // «+» als eigener Text, gedreht
      const eigen = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
      if (/^[+✚✛＋﹢]$/.test(eigen) && schraeg(vorfahrDreh(e))) fund('zier-x', e, `«${eigen}» um ${Math.round(vorfahrDreh(e))}° gedreht: sieht aus wie ein «×»`);
      for (const ps of ['::before', '::after']) { const c = getComputedStyle(e, ps); if (!c.content || c.content === 'none') continue;
        if (/^["'][+✚✛＋﹢]["']$/.test(c.content) && schraeg(drehung(e, ps) + vorfahrDreh(e))) fund('zier-x', e, `«+» in ${ps} gedreht: sieht aus wie ein «×»`); }
      // zwei schmale Balken in ::before und ::after, schräg gekreuzt
      const b = getComputedStyle(e, '::before'), a = getComputedStyle(e, '::after');
      if (b.content !== 'none' && a.content !== 'none' && /^["']["']$/.test(b.content) && /^["']["']$/.test(a.content)) { const wb = drehung(e, '::before') + vorfahrDreh(e), wa = drehung(e, '::after') + vorfahrDreh(e);
        const balken = c => { const w = parseFloat(c.width), h = parseFloat(c.height); return w > 0 && h > 0 && Math.max(w, h) / Math.min(w, h) >= 4; };
        if (balken(b) && balken(a) && schraeg(wb) && schraeg(wa) && Math.abs(Math.abs(wb - wa) - 90) < 15) fund('zier-x', e, 'Zwei gekreuzte Balken (::before/::after) bilden ein «×»'); }
      // SVG mit zwei gekreuzten Diagonalen

    } 
    for (const e of document.querySelectorAll('svg')) { const r0 = e.getBoundingClientRect(); if (r0.width < 4 || r0.height < 4 || r0.width > 96 || r0.height > 96 || getComputedStyle(e).visibility === 'hidden') continue;   /* nur Zeichen, keine Karten oder Bilder */
      let unsichtbar = false; for (let x = e; x && x !== document.body; x = x.parentElement) if (+getComputedStyle(x).opacity < 0.05) { unsichtbar = true; break; } if (unsichtbar) continue;
      if (e.closest('[aria-expanded]')) continue;   /* Auf/Zu-Knopf: das × ist sein Schliessen-Zustand (Chat-Knopf der Website) */ {
        const strecken = []; for (const l of e.querySelectorAll('line')) strecken.push([+l.getAttribute('x1'), +l.getAttribute('y1'), +l.getAttribute('x2'), +l.getAttribute('y2')]);
        for (const pa of e.querySelectorAll('path')) { const d = pa.getAttribute('d') || ''; const t = d.match(/[MmLl][^MmLl]*/g) || []; let x = 0, y = 0, sx = 0, sy = 0;
          for (const k of t) { const z = (k.slice(1).match(/-?\d*\.?\d+/g) || []).map(Number); if (z.length < 2) { strecken.length = strecken.length; continue; } const rel = k[0] === 'm' || k[0] === 'l';
            for (let i = 0; i + 1 < z.length; i += 2) { const nx = rel ? x + z[i] : z[i], ny = rel ? y + z[i + 1] : z[i + 1]; if ((k[0] === 'L' || k[0] === 'l') || i > 0) strecken.push([x, y, nx, ny]); x = nx; y = ny; } } }
        if (strecken.length > 8) continue;   /* ein × hat zwei Striche, kein ganzes Bild */
        const diag = strecken.filter(([a1, b1, a2, b2]) => { const dx = a2 - a1, dy = b2 - b1; return Math.abs(dx) > 1 && Math.abs(Math.abs(dy / dx) - 1) < 0.35; });
        const steigt = diag.filter(([a1, b1, a2, b2]) => (b2 - b1) / (a2 - a1) > 0), faellt = diag.filter(([a1, b1, a2, b2]) => (b2 - b1) / (a2 - a1) < 0);
        const kreuzt = (p, q) => { const [x1, y1, x2, y2] = p, [x3, y3, x4, y4] = q; const n = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4); if (Math.abs(n) < 1e-6) return false;
          const t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / n, u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / n; return t > 0.2 && t < 0.8 && u > 0.2 && u < 0.8; };   // mitten gekreuzt, nicht nur an einem Ende (Pfeil, Haken, Winkel)
        if (steigt.some(p => faellt.some(q => kreuzt(p, q))) && !schliessen(e) && !(e.closest('button,[role=button],a') && schliessen(e.closest('button,[role=button],a')))) fund('zier-x', e, 'Gezeichnetes «×» (zwei gekreuzte Diagonalen im SVG)'); } }
  }

  // 9 Schrift optisch mittig in Knöpfen, Pillen, Etiketten, Rundknöpfen (Robert 29.10.2026: «Die Schriften in deinen Buttons sitzen IMMER falsch»)
  { const cv = document.createElement('canvas').getContext('2d');
    const mitteKasten = e => { const r = e.getBoundingClientRect(), c = cs(e); return { x: r.left + parseFloat(c.borderLeftWidth) + (r.width - parseFloat(c.borderLeftWidth) - parseFloat(c.borderRightWidth)) / 2, y: r.top + parseFloat(c.borderTopWidth) + (r.height - parseFloat(c.borderTopWidth) - parseFloat(c.borderBottomWidth)) / 2, r }; };
    const gezeichnet = sv => { try { const bb = sv.getBBox(); const vb = sv.viewBox && sv.viewBox.baseVal; const r = sv.getBoundingClientRect(); if (!vb || !vb.width || !bb.width) return null; const sx = r.width / vb.width, sy = r.height / vb.height;
      return { l: r.left + (bb.x - vb.x) * sx, r: r.left + (bb.x - vb.x + bb.width) * sx, o: r.top + (bb.y - vb.y) * sy, u: r.top + (bb.y - vb.y + bb.height) * sy }; } catch (x) { return null; } };
    const pille = e => (istKnopf(e) || /pill|chip|etik|label|marke|tag\b|badge|zahl|mk\b|kn\b/i.test(typeof e.className === 'string' ? e.className : '')) && kastenSichtbar(e) && e.getBoundingClientRect().height <= 80 && e.getBoundingClientRect().width <= 420;
    for (const e of sichtbar) { if (!pille(e)) continue;
      const k = mitteKasten(e);
      // Textknoten direkt im Kasten oder in einem Kind ohne eigene Fläche; nur einzeilig
      // versteckter Text (clip-Muster für Vorleser, Fläche unter 2 px) zählt nicht (30.10.2026, «Neu» am Handy)
      const versteckt = pe => { for (let x = pe; x && x !== e.parentElement; x = x.parentElement) { const c = cs(x), r = x.getBoundingClientRect(); if (x !== e && (r.width < 2 || r.height < 2)) return true; if (/absolute|fixed/.test(c.position) && c.clip && c.clip !== 'auto') return true; if (/^inset\((50|100)%/.test(c.clipPath)) return true; } return false; };
      const tn = []; const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n; while ((n = tw.nextNode())) { if (!n.textContent.trim()) continue; const pe = n.parentElement; if (pe !== e && pille(pe)) continue; if (!S.has(pe) && pe !== e) continue; if (versteckt(pe)) continue; tn.push(n); }
      const symbole = [...e.querySelectorAll('svg')].filter(x => S.has(x) || x.getBoundingClientRect().width > 0);
      if (tn.length) { let oben = 1e9, unten = -1e9, links = 1e9, rechts = -1e9, zeilen = new Set();
        for (const n of tn) { const pe = n.parentElement, c = cs(pe); let t = n.textContent.replace(/\s+/g, ' ').trim(); if (c.textTransform === 'uppercase') t = t.toUpperCase(); else if (c.textTransform === 'lowercase') t = t.toLowerCase();
          cv.font = `${c.fontStyle} ${c.fontWeight} ${c.fontSize} ${c.fontFamily}`; try { cv.letterSpacing = c.letterSpacing === 'normal' ? '0px' : c.letterSpacing; } catch (x) {}
          const m = cv.measureText(t); const rg = document.createRange(); rg.selectNodeContents(n); const qs = [...rg.getClientRects()].filter(q => q.width > 0.5); if (!qs.length) continue;
          qs.forEach(q => zeilen.add(Math.round(q.top)));
          const q = qs[0]; const grund = q.top + (q.height - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2 + m.fontBoundingBoxAscent;
          // optische Mitte: Versalhöhe (Text mit Grossbuchstaben oder Ziffern) bzw. x-Höhe (reine Kleinschrift), ab der Grundlinie; Unterlängen und Akzente zählen nicht
          const roh = t.normalize('NFD').replace(/[\u0300-\u036f]/g, ''); const hoehe = /[A-ZÄÖÜ0-9]/.test(roh) ? cv.measureText('H').actualBoundingBoxAscent : cv.measureText('x').actualBoundingBoxAscent;
          const nurZeichen = !/[A-Za-z0-9]/.test(roh);   // z. B. «×» oder «+»: dann die echten Glyphen
          oben = Math.min(oben, grund - (nurZeichen ? m.actualBoundingBoxAscent : hoehe)); unten = Math.max(unten, grund + (nurZeichen ? m.actualBoundingBoxDescent : 0));
          links = Math.min(links, q.left - m.actualBoundingBoxLeft); rechts = Math.max(rechts, q.left + m.actualBoundingBoxRight); }
        // Zeichen über der Beschriftung (flex-direction column): die Gruppe aus Zeichen und Text messen (30.10.2026, Mail-Kacheln)
        const ce = cs(e), kol = symbole.length > 0 && /flex/.test(ce.display) && /column/.test(ce.flexDirection);
        if (kol) for (const sv of symbole) { const g = gezeichnet(sv); if (g) { oben = Math.min(oben, g.o); unten = Math.max(unten, g.u); links = Math.min(links, g.l); rechts = Math.max(rechts, g.r); } }
        if (zeilen.size === 1 && oben < 1e8) {
          const dy = (oben + unten) / 2 - k.y; const zentriert = kol ? ce.alignItems === 'center' : !symbole.length && !e.querySelector('i,img') && (/flex/.test(ce.display) ? ce.justifyContent === 'center' : /grid/.test(ce.display) ? (ce.justifyContent === 'center' || ce.justifyItems === 'center') : ce.textAlign === 'center');
          const dx = zentriert ? (links + rechts) / 2 - k.x : 0;
          if (Math.abs(dy) > 0.5 || Math.abs(dx) > 0.5) fund('text-mitte', e, `Schrift ${Math.abs(dy) > 0.5 ? (dy < 0 ? Math.abs(dy).toFixed(1) + ' px zu hoch' : dy.toFixed(1) + ' px zu tief') : ''}${Math.abs(dy) > 0.5 && Math.abs(dx) > 0.5 ? ', ' : ''}${Math.abs(dx) > 0.5 ? (dx < 0 ? Math.abs(dx).toFixed(1) + ' px zu weit links' : dx.toFixed(1) + ' px zu weit rechts') : ''} (Glyphen ${Math.round(unten - oben)} px hoch in Kasten ${Math.round(k.r.height)} px)`);
        } }
      else if (symbole.length === 1) { // Symbol allein im (Rund-)Knopf: Mitte der gezeichneten Form
        const sv = symbole[0]; try { const bb = sv.getBBox(); const vb = sv.viewBox && sv.viewBox.baseVal; const r = sv.getBoundingClientRect();
          if (vb && vb.width && bb.width) { const sx = r.width / vb.width, sy = r.height / vb.height; const mx = r.left + (bb.x - vb.x + bb.width / 2) * sx, my = r.top + (bb.y - vb.y + bb.height / 2) * sy;
            const dx = mx - k.x, dy = my - k.y; if (Math.abs(dx) > 0.5 || Math.abs(dy) > 0.5) fund('text-mitte', e, `Symbol ${dx.toFixed(1)} px waagrecht, ${dy.toFixed(1)} px senkrecht neben der Mitte`); } } catch (x) {} }
    } }

  // 5 Anschnitt am Bildschirmrand, seitliches Verrutschen
  const sw = document.documentElement.scrollWidth; if (sw > VW + 1) F.push({ art: 'anschnitt', sel: 'html', text: '', info: `Seite ${sw} px breit bei ${VW} px Fenster (verrutscht seitlich)`, r: { x: 0, y: 0, w: VW, h: 60 } });
  for (const e of blatt) { const r = e.getBoundingClientRect(); if (r.width < 4) continue;
    if ((r.left < -1 && r.right > 0) || (r.right > VW + 1 && r.left < VW)) { if (scroller(e)) continue; fund('anschnitt', e, `${Math.round(r.left)}…${Math.round(r.right)} px bei Fensterbreite ${VW}`); } }
  return F;
};
