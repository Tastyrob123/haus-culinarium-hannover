/* Dirty Chicken · Wahlseite «Das erste Pop-up»: Datum driftet (3), Marke wandert (8), Namen tauschen das Bild (10), Leiste zum Aufklappen (13). Nur transform, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  function p(el) { var r = el.getBoundingClientRect(), vh = innerHeight; return Math.max(-1, Math.min(1, (r.top + r.height / 2 - vh / 2) / vh)); }
  function drin(el) { if (el.closest('[hidden]')) return false; var r = el.getBoundingClientRect(); return r.bottom > -300 && r.top < innerHeight + 300; }

  /* 10 Vier Namen: Zeigen oder Tippen tauscht das Bild an derselben Stelle */
  function name(n) {
    var l = n.closest('.pp10'), w = l && l.querySelector('.pp10-wahl'); if (!w) return;
    w.dataset.wahl = n.dataset.s;
    l.querySelectorAll('.pp10-n').forEach(function (x) { x.classList.toggle('an', x === n); });
  }
  document.addEventListener('click', function (e) { var n = e.target.closest('.pp10-n'); if (n) name(n); });
  if (matchMedia('(hover:hover)').matches) document.addEventListener('mouseover', function (e) { var n = e.target.closest('.pp10-n'); if (n) name(n); });

  /* 13 Die Leiste: Antippen holt die Antwort auf die Bühne */
  document.addEventListener('click', function (e) {
    var k = e.target.closest('.pp13-k'); if (!k) return;
    var s = k.closest('section'), b = s.querySelector('.pp13-buehne');
    b.dataset.wahl = k.dataset.s;
    s.querySelectorAll('.pp13-k').forEach(function (x) { var an = x === k; x.classList.toggle('an', an); x.setAttribute('aria-selected', an ? 'true' : 'false'); });
  });

  /* Scroll-getrieben: das Datum driftet, die Marke wandert über die Stunden */
  var DA = [].slice.call(document.querySelectorAll('.pp3-datum')), PL = [].slice.call(document.querySelectorAll('.pp8-plan'));
  var lt = false;
  function rechnen() {
    lt = false;
    if (ruhig) return;
    DA.forEach(function (d) { if (!drin(d)) return; d.style.transform = 'translate3d(0,' + (p(d) * -60).toFixed(1) + 'px,0)'; });
    PL.forEach(function (pl) {
      if (!drin(pl)) return;
      var st = pl.querySelector('.pp8-stunden'), m = pl.querySelector('.pp8-marke'), r = pl.getBoundingClientRect();
      var q = Math.max(0, Math.min(1, (innerHeight * .85 - r.top) / (innerHeight * .9)));   /* 0 = unten am Rand, 1 = oben angekommen */
      m.style.transform = 'translate3d(' + (q * (st.clientWidth - 2)).toFixed(1) + 'px,0,0)';
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', takt, { passive: true });
  rechnen();
  /* Wahlseite: beim Umschalten neu stellen */
  var alt = window.culinariumNeu;
  window.culinariumNeu = function (root) { if (alt) alt(root); setTimeout(takt, 50); };
})();
