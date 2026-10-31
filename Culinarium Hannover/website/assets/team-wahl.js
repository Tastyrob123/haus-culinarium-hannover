/* Culinarium · «Drei Leute, ein Haus.» zur Wahl: Zoom zurück, Filmstreifen, Umdrehen, Ringe. Nur transform, nativer Scroll. */
(function () {
  'use strict';
  function anteil(el, a, b) { var r = el.getBoundingClientRect(), h = innerHeight; return Math.max(0, Math.min(1, (h * a - r.top) / (h * b))); }
  var laeuft = false;
  function rechne() {
    laeuft = false;
    /* 3 Zoom zurück: von 2.2 auf 1, solange das Bild durch das untere Drittel nach oben wandert */
    document.querySelectorAll('[data-tw-zoom]').forEach(function (f) { if (f.offsetParent) f.style.setProperty('--s', (2.2 - 1.2 * anteil(f, .95, .85)).toFixed(3)); });
    /* 6 Filmstreifen: läuft beim Scrollen nach links */
    document.querySelectorAll('[data-tw-lauf]').forEach(function (s) {
      if (!s.offsetParent) return; var b = s.firstElementChild, weg = Math.max(0, b.scrollWidth - s.clientWidth + 40);
      b.style.setProperty('--x', (-weg * anteil(s, .7, 1.4)).toFixed(1) + 'px');
    });
  }
  function bitte() { if (!laeuft) { laeuft = true; requestAnimationFrame(rechne); } }
  addEventListener('scroll', bitte, { passive: true }); addEventListener('resize', bitte);
  document.addEventListener('click', function (e) { bitte(); var k = e.target.closest('[data-tw-um]'); if (k) k.classList.toggle('um'); });
  addEventListener('keydown', function () { setTimeout(bitte, 60); });
  /* 15 Markiert: Name überfahren oder antippen zeigt den Ring */
  document.querySelectorAll('[data-tw-ringe]').forEach(function (box) {
    function an(i) {
      box.classList.toggle('wahl-r', i !== null);
      box.querySelectorAll('[data-r]').forEach(function (x) { x.classList.toggle('an', x.dataset.r === i); });
    }
    box.querySelectorAll('.tw-15-name').forEach(function (n) {
      n.addEventListener('mouseenter', function () { an(n.dataset.r); });
      n.addEventListener('mouseleave', function () { an(null); });
      n.addEventListener('click', function () { an(n.classList.contains('an') ? null : n.dataset.r); });
    });
  });
  rechne();
})();
