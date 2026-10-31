/* Wahlseite «So läuft ein Abend»: Momente der 15 Fassungen (Rivage-Machart). Nur transform und opacity, nativer Scroll; rechnet nur die sichtbare Fassung. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  function $$(s, c) { return [].slice.call((c || document).querySelectorAll(s)); }
  function sichtbar(el) { var v = el.closest('.wv'); return v && !v.hidden; }

  /* 3 3D-Kacheln: neigen sich ganz leicht zur Maus (höchstens ±1,6°, Briefing 6.2), beim Scrollen nicht */
  if (!ruhig && matchMedia('(hover:hover)').matches) $$('[data-kb-neigen] .kb-03-z').forEach(function (z) {
    z.addEventListener('pointermove', function (e) { var r = z.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; z.style.transform = 'rotateY(' + (x * 3.2).toFixed(2) + 'deg) rotateX(' + (-y * 3.2).toFixed(2) + 'deg)'; });
    z.addEventListener('pointerleave', function () { z.style.transform = ''; });
  });

  /* 5 Kino: Bild fährt langsam heran und geht ins nächste über, die Linie unter dem Schritt läuft mit */
  $$('[data-kb-kino]').forEach(function (k) {
    var imgs = $$('.kb-05-bild img', k), bt = $$('.kb-05-r button', k), lin = $$('.kb-05-l i', k), i = 0, t0 = performance.now(), D = 6000, sicht = false;
    function zeig(n) { i = (n + 4) % 4; t0 = performance.now(); imgs.forEach(function (m, j) { m.classList.toggle('an', j === i); }); bt.forEach(function (b, j) { b.classList.toggle('an', j === i); }); lin.forEach(function (l, j) { if (j !== i) l.style.transform = 'scaleX(0)'; }); }
    bt.forEach(function (b) { b.addEventListener('click', function () { zeig(+b.dataset.i); }); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { sicht = e[0].isIntersecting; t0 = performance.now(); }, { threshold: .3 }).observe(k);
    (function tick(now) { requestAnimationFrame(tick); if (!sicht || ruhig || !sichtbar(k)) return; var p = (now - t0) / D; if (p >= 1) { zeig(i + 1); p = 0; } lin[i].style.transform = 'scaleX(' + p.toFixed(4) + ')'; })(performance.now());
  });

  /* 12 Bildgruppe: das angetippte kleine Bild fährt an die Stelle des grossen (FLIP, nur transform, Briefing 6.5) */
  $$('[data-kb-gruppe]').forEach(function (g) {
    var ps = $$('.kb-12-p', g);
    ps.forEach(function (p) {
      p.addEventListener('click', function () {
        var platz = +p.dataset.platz; if (!platz) return;
        var gross = ps.filter(function (x) { return x.dataset.platz === '0'; })[0];
        var a = p.getBoundingClientRect(), b = gross.getBoundingClientRect();
        p.dataset.platz = '0'; gross.dataset.platz = String(platz);
        [[p, a], [gross, b]].forEach(function (o) {
          var el = o[0], alt = o[1], neu = el.getBoundingClientRect();
          if (ruhig) return;
          el.style.transition = 'none'; el.style.transformOrigin = '0 0';
          el.style.transform = 'translate(' + (alt.left - neu.left) + 'px,' + (alt.top - neu.top) + 'px) scale(' + (alt.width / neu.width) + ',' + (alt.height / neu.height) + ')';
          requestAnimationFrame(function () { requestAnimationFrame(function () { el.style.transition = 'transform 880ms cubic-bezier(.36,0,.1,1)'; el.style.transform = ''; }); });
        });
      });
    });
  });

  /* 15 Löcher in der Wand: die Bilder gleiten hinter den Öffnungen gegen die Scrollrichtung */
  var loecher = $$('.kb-15-loch img'), lt = false;
  function takt() {
    lt = false; var vh = innerHeight;
    loecher.forEach(function (im) { if (!sichtbar(im)) return; var r = im.parentNode.getBoundingClientRect(); if (r.bottom < 0 || r.top > vh) return; var p = (r.top + r.height / 2 - vh / 2) / vh; im.style.transform = 'translate3d(0,' + (p * -12).toFixed(2) + '%,0)'; });
  }
  function scroll() { if (!lt) { lt = true; requestAnimationFrame(takt); } }
  if (!ruhig) { addEventListener('scroll', scroll, { passive: true }); addEventListener('resize', scroll, { passive: true }); }
  if ('MutationObserver' in window) new MutationObserver(scroll).observe(document.getElementById('ablauf'), { attributes: true, subtree: true, attributeFilter: ['hidden'] });
  takt();

  /* Beim Laden mit ?ablauf=N ist die Fassung schon sichtbar, bevor die Seite ihre Auftritte beobachtet: einmal nachmelden */
  addEventListener('load', function () { var v = document.querySelector('#ablauf .wv.kb:not([hidden])'); if (v && window.culinariumNeu) window.culinariumNeu(v); });
})();
