// Abnahme-Tor (schnell) · Funktionen im Browser, ergänzend zu seite.js.
// skelett – Gerüst des Zustands: sichtbare Elemente mit Tag, Klassen (ohne Laufzustände), Lage und Grösse auf 8 px gerundet, ohne Text.
//           Zwei Zustände mit gleichem Gerüst zeigen dasselbe Layout (anderer Inhalt), z. B. 296 Fotos derselben Sammlung im Editor.
exports.skelett = function skelett() {
  const LAUF = /^(an|aktiv|da|gespielt|offen|sicht|auf|zu|hover|fokus|gewaehlt|gewählt|wahl|ist-.*|js-.*|an-.*|is-.*|selected|active|current|wo-an|kw-an)$/;
  const teile = [];
  const sicht = e => { const r = e.getBoundingClientRect(); return r.width >= 2 && r.height >= 2; };
  for (const e of document.body.querySelectorAll('*')) {
    if (/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|OPTION|BR|PATH|G|USE|DEFS)$/.test(e.tagName)) continue;
    if (!sicht(e)) continue;
    const c = getComputedStyle(e); if (c.display === 'none' || c.visibility === 'hidden') continue;
    const kl = (typeof e.className === 'string' ? e.className : (e.className && e.className.baseVal) || '').trim().split(/\s+/).filter(k => k && !LAUF.test(k)).slice(0, 3).join('.');
    const r = e.getBoundingClientRect();
    const q = v => Math.round(v / 8);
    teile.push(e.tagName + (kl ? '.' + kl : '') + '@' + q(r.left) + ',' + q(r.top + scrollY) + ',' + q(r.width) + ',' + q(r.height));
  }
  const roh = teile.join(';'); let h = 0; for (let i = 0; i < roh.length; i++) h = (h * 31 + roh.charCodeAt(i)) | 0;
  return String(h >>> 0) + ':' + teile.length;
};
