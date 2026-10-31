/* Culinarium · Team-Seite «Wie es kam.» zur Wahl: Schalter, Tresen, Mittellinie, Karte, Postkarten, Wörter, Kerzen, Fassade.
   Nur Klassen und transform, nativer Scroll. */
(function () {
  'use strict';
  var teil = document.getElementById('kam');
  function sichtbar(x) { return !x.closest('[hidden]'); }
  function grenze(v) { return Math.min(1, Math.max(0, v)); }

  /* Ton des Abschnitts folgt der gezeigten Fassung (hell oder Nacht) */
  function ton() { var v = teil.querySelector(':scope>.wv:not([hidden])'); if (v) teil.dataset.ton = v.dataset.ton; }
  new MutationObserver(ton).observe(teil, { subtree: true, attributes: true, attributeFilter: ['hidden'] });
  ton();

  /* Schalter: data-q zeigt alles mit demselben data-a im selben [data-kw] */
  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-q]'); if (!q) return;
    var box = q.closest('[data-kw]'); if (!box) return;
    var i = q.dataset.q;
    box.querySelectorAll('[data-q],[data-a]').forEach(function (x) {
      x.classList.toggle('an', (x.dataset.q !== undefined ? x.dataset.q : x.dataset.a) === i);
    });
  });

  /* 8 Postkarten: antippen dreht um */
  document.addEventListener('click', function (e) { var k = e.target.closest('[data-kw-dreh]'); if (k) k.classList.toggle('um'); });

  /* 5 Die Karte: der Gang in der Mitte (oder unter der Maus) zeigt sein Foto */
  document.querySelectorAll('[data-kw-karte]').forEach(function (box) {
    function setze(m) { box.querySelectorAll('[data-m]').forEach(function (x) { x.classList.toggle('an', x.dataset.m === m); }); }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) setze(e.target.dataset.m); }); }, { rootMargin: '-46% 0px -46% 0px' });
    box.querySelectorAll('.kw-05-gang').forEach(function (g) { io.observe(g); g.addEventListener('mouseenter', function () { setze(g.dataset.m); }); });
  });

  /* 12 Die grossen Wörter: das Foto folgt der Maus */
  document.querySelectorAll('[data-kw-woerter]').forEach(function (box) {
    var f = box.querySelector('.kw-12-folger'), x = 0, y = 0, fx = 0, fy = 0, laeuft = false;
    function schritt() {
      fx += (x - fx) * .16; fy += (y - fy) * .16;
      f.style.transform = 'translate(' + (fx - f.offsetWidth / 2) + 'px,' + (fy - f.offsetHeight * .6) + 'px) rotate(' + ((x - fx) * .03).toFixed(2) + 'deg)';
      if (Math.abs(x - fx) + Math.abs(y - fy) > .5) requestAnimationFrame(schritt); else laeuft = false;
    }
    box.addEventListener('mousemove', function (e) { x = e.clientX; y = e.clientY; if (!laeuft) { laeuft = true; requestAnimationFrame(schritt); } });
    box.querySelectorAll('.kw-12-z').forEach(function (z) {
      z.addEventListener('mouseenter', function (e) {
        if (!f.classList.contains('an')) { fx = x = e.clientX; fy = y = e.clientY; }
        f.classList.add('an');
        f.querySelectorAll('figure').forEach(function (b) { b.classList.toggle('an', b.dataset.m === z.dataset.m); });
      });
    });
    box.querySelector('.kw-12-liste').addEventListener('mouseleave', function () { f.classList.remove('an'); });
  });

  /* Scrollgesteuert: --p, Tresen, Kerzen, Fassade */
  function lauf() {
    var h = innerHeight;
    document.querySelectorAll('.kw [data-kw-p]').forEach(function (el) {
      if (!sichtbar(el)) return;
      var r = el.getBoundingClientRect(), p;
      if (r.bottom < -200 || r.top > h + 200) return;
      p = el.dataset.kwP === 'linie' ? (h * .62 - r.top) / r.height : (h - r.top) / (h + r.height);
      el.style.setProperty('--p', grenze(p).toFixed(4));
    });
    document.querySelectorAll('[data-kw-tresen]').forEach(function (box) {
      if (!sichtbar(box) || innerWidth <= 860) return;
      var r = box.getBoundingClientRect(), spur = box.querySelector('.kw-03-spur');
      var q = grenze(-r.top / (r.height - h));
      spur.style.transform = 'translateX(' + (-(spur.scrollWidth - innerWidth) * q).toFixed(1) + 'px)';
    });
    document.querySelectorAll('[data-kw-kerzen]').forEach(function (box) {
      if (!sichtbar(box)) return;
      var n = -1;
      box.querySelectorAll('.kw-14-m').forEach(function (m) { if (m.getBoundingClientRect().top < h * .62) n = Math.max(n, +m.dataset.m); });
      box.querySelectorAll('.kw-14-k').forEach(function (k) { k.classList.toggle('an', +k.dataset.m <= n); });
    });
    document.querySelectorAll('.kw-15-f').forEach(function (f) {
      if (!sichtbar(f)) return;
      f.classList.toggle('an', f.getBoundingClientRect().top < h * .62);
    });
  }
  var warten = false;
  addEventListener('scroll', function () { if (!warten) { warten = true; requestAnimationFrame(function () { warten = false; lauf(); }); } }, { passive: true });
  addEventListener('resize', lauf);
  new MutationObserver(function () { requestAnimationFrame(lauf); }).observe(teil, { subtree: true, attributes: true, attributeFilter: ['hidden'] });
  lauf();
})();
