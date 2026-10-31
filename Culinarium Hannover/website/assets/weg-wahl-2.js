/* Culinarium · Der Weg, 20 weitere Fassungen (nur Wahlseite): Tür auf und zu, Klingelleiste. Nur transform und opacity. */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-wh-tuer]')) { e.target.closest('.wh04').classList.toggle('zu'); return; }
    var k = e.target.closest('[data-wh-klingel]');
    if (k) {
      var r = k.closest('.wh17');
      r.dataset.klingel = k.dataset.whKlingel;
      r.querySelectorAll('[data-wh-klingel]').forEach(function (b) { b.setAttribute('aria-pressed', b === k ? 'true' : 'false'); });
    }
  });
})();
