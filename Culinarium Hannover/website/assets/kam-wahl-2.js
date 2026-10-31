/* Culinarium · Team-Seite «Wie es kam.» Runde 2 zur Wahl: Scrollfortschritt --p für Wechsel, Gegenläufig, Leporello, Bildstreifen, Spalten.
   Nur transform und opacity über CSS, nativer Scroll. */
(function () {
  'use strict';
  var teil = document.getElementById('kam');
  function grenze(v) { return Math.min(1, Math.max(0, v)); }

  /* Ton des Abschnitts folgt der gezeigten Fassung */
  function ton() { var v = teil.querySelector(':scope>.wv:not([hidden])'); if (v) teil.dataset.ton = v.dataset.ton; }
  new MutationObserver(ton).observe(teil, { subtree: true, attributes: true, attributeFilter: ['hidden'] });
  ton();

  /* --p: 0, wenn das Element unten hereinkommt, 1, wenn es oben hinausgeht */
  function lauf() {
    if (innerWidth <= 860) return;
    var h = innerHeight;
    teil.querySelectorAll('.wv:not([hidden]) [data-k2-p]').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > h + 200) return;
      el.style.setProperty('--p', grenze((h - r.top) / (h + r.height)).toFixed(4));
    });
  }
  var warten = false;
  addEventListener('scroll', function () { if (!warten) { warten = true; requestAnimationFrame(function () { warten = false; lauf(); }); } }, { passive: true });
  addEventListener('resize', lauf);
  new MutationObserver(function () { requestAnimationFrame(lauf); }).observe(teil, { subtree: true, attributes: true, attributeFilter: ['hidden'] });
  lauf();
})();
