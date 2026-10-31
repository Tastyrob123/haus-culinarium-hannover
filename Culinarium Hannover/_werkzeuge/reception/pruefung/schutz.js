// Schutz für jeden Prüflauf (Prüf-Chat 17.10.2026, nach Vorfall Doldenhorn und Ruedihus: Firefox headless öffnete über «mailto:» Apple Mail auf Roberts
// Bildschirm). Jedes Prüfskript startet Browser und Kontext nur hierüber:
//  · Firefox ohne externe Programme für mailto/tel/sms (Einstellungen), alle Browser headless.
//  · Im Kontext fängt ein Skript vor allen anderen jeden Klick auf mailto:/tel:/sms:-Links und auf Knöpfe ab, die das Mailprogramm öffnen
//    ([data-akt="mail"]), zählt ihn in window.__abgefangen (Liste in window.__abgefangenWas) und lässt ihn nie bis zur Seite durch.
//  · window.open mit mailto/tel wird ebenso geschluckt.
const PREFS = { 'network.protocol-handler.external.mailto': false, 'network.protocol-handler.external.tel': false, 'network.protocol-handler.external.sms': false,
  'network.protocol-handler.expose.mailto': true, 'network.protocol-handler.expose.tel': true, 'network.protocol-handler.expose.sms': true, 'network.protocol-handler.warn-external-default': true };
const SKRIPT = () => {
  window.__abgefangen = 0; window.__abgefangenWas = [];
  const fang = was => { window.__abgefangen++; window.__abgefangenWas.push(String(was).slice(0, 120)); };
  const pruef = e => { const el = e.target && e.target.closest ? e.target.closest('a[href^="mailto:"],a[href^="tel:"],a[href^="sms:"],[data-akt="mail"]') : null;
    if (el) { e.preventDefault(); e.stopImmediatePropagation(); fang(el.getAttribute('href') || el.getAttribute('data-akt')); } };
  for (const t of ['click', 'auxclick', 'pointerup', 'mouseup', 'keydown']) document.addEventListener(t, e => { if (t === 'keydown' && e.key !== 'Enter' && e.key !== ' ') return; if (t === 'click' || t === 'auxclick' || t === 'keydown') pruef(e); }, true);
  const wo = window.open; window.open = function (u, ...r) { if (/^(mailto|tel|sms):/i.test(String(u || ''))) { fang(u); return null; } return wo.call(this, u, ...r); };
};
module.exports = {
  start: (pw, motor, opt = {}) => pw[motor].launch({ headless: true, ...opt, ...(motor === 'firefox' ? { firefoxUserPrefs: { ...PREFS, ...(opt.firefoxUserPrefs || {}) } } : {}) }),
  kontext: async (br, opt) => { const c = await br.newContext(opt); await c.addInitScript(SKRIPT); return c; },
};
