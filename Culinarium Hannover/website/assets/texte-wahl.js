/* Wahlseite «Texte unter Über Eck»: Satz zur Fassung in der Leiste, Schräge der Naht für alle Fassungen, Fassung 13 (Deckkraft je Seite) */
(function () {
  'use strict';
  var sek = document.getElementById('ebenen'), rahmen = sek.querySelector('.ue-rahmen');
  var satz = document.querySelector('[data-tw-satz]'), name = document.querySelector('[data-wl-name]');

  /* Schräge der Naht in Pixel je Pixel Höhe (14 % der Breite auf die Höhe der Bildwand), wie culinarium.js */
  function schraege() {
    var r = rahmen.getBoundingClientRect(), s = .14 * r.width / Math.max(1, r.height);
    sek.style.setProperty('--schraege', s.toFixed(4));
    sek.style.setProperty('--tw09-w', (-(90 - Math.atan(s) * 180 / Math.PI)).toFixed(2) + 'deg');
    [].forEach.call(sek.querySelectorAll('.wv:not([hidden]) .ue-weiter line'), function (l) {
      var h = l.ownerSVGElement.getBoundingClientRect().height;
      l.setAttribute('x2', (43 - 14 * h / Math.max(1, r.height)).toFixed(2));
    });
  }
  function text() {
    var n = +(new URLSearchParams(location.search).get('ebenen') || 0);
    if (satz && window.TW_SAETZE) satz.textContent = window.TW_SAETZE[n] || '';
    schraege();
  }
  if (name) new MutationObserver(text).observe(name, { childList: true, characterData: true, subtree: true });
  addEventListener('resize', schraege, { passive: true });
  text();

  /* Fassung 13: wo der Zeiger ist (links oder rechts der Naht), bleibt der Text hell */
  if (!(window.matchMedia && matchMedia('(hover:hover)').matches)) return;
  sek.addEventListener('mousemove', function (e) {
    var t = sek.querySelector('.wv:not([hidden]) .tw13'); if (!t) return;
    var r = rahmen.getBoundingClientRect(), naht = r.left + r.width * (.57 - .14 * (e.clientY - r.top) / r.height);
    t.dataset.blick = e.clientX < naht ? 'l' : 'r';
  });
  sek.addEventListener('mouseleave', function () { var t = sek.querySelector('.tw13'); if (t) delete t.dataset.blick; });
})();
