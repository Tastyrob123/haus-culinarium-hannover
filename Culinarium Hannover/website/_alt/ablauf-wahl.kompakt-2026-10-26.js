/* Wahlseite «So läuft ein Abend»: Fassung 14 «Bild wechselt, Text bleibt». Zeigen auf einen Schritt holt sein Bild (nur opacity). */
(function () {
  'use strict';
  [].forEach.call(document.querySelectorAll('[data-kb-wechsel]'), function (w) {
    var imgs = [].slice.call(w.querySelectorAll('.kb-14-b img')), st = [].slice.call(w.querySelectorAll('.kb-14-l [data-i]'));
    st.forEach(function (s) {
      function setz() { var i = +s.dataset.i; st.forEach(function (x, j) { x.classList.toggle('an', j === i); }); imgs.forEach(function (m, j) { m.classList.toggle('an', j === i); }); }
      s.addEventListener('mouseenter', setz); s.addEventListener('click', setz);
    });
  });
})();
