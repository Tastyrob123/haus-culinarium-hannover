/* Culinarium · Hero der Seite Dirty Chicken in 15 Fassungen (nur Wahlseite). Filme, Scroll-Züge und Bildspur; nur transform und opacity. */
(function () {
  var ruhig = document.documentElement.classList.contains('ruhig');
  var kopf = document.getElementById('kopf');

  function sichtbar() { return kopf.querySelector('.wv:not([hidden])'); }

  /* Filme: nur der Film der sichtbaren Fassung spielt, und nur solange er im Bild ist */
  function filme() {
    var f = sichtbar();
    kopf.querySelectorAll('video.film-hier').forEach(function (v) {
      var r = v.getBoundingClientRect(), an = f && f.contains(v) && r.bottom > 0 && r.top < innerHeight;
      if (an) {
        if (!v.src) { v.src = v.dataset.src; }
        if (v.paused && !ruhig) v.play().catch(function () {});
      } else if (!v.paused) v.pause();
    });
  }
  setInterval(filme, 400);

  /* 13 Stories: Laufbalken folgt dem Film */
  var sv = kopf.querySelector('.d13 video'), sb = kopf.querySelector('.d13-balken i');
  (function balken() {
    if (sv && sb && !sv.paused && sv.duration) sb.style.transform = 'scaleX(' + (sv.currentTime / sv.duration) + ')';
    requestAnimationFrame(balken);
  })();

  if (ruhig) return;

  /* 5 Bildspur: wo die Maus fährt, landet das nächste Foto */
  var spur = kopf.querySelector('.d05');
  if (spur) {
    var vorrat = [].slice.call(spur.querySelectorAll('.d05-vorrat img')), n = 0, lx = -999, ly = -999;
    function lege(x, y) {
      var r = spur.getBoundingClientRect(), fig = document.createElement('figure'), im = vorrat[n++ % vorrat.length].cloneNode();
      im.loading = 'eager';
      fig.className = 'd05-k neu';
      fig.style.left = (x - r.left) + 'px'; fig.style.top = (y - r.top) + 'px';
      fig.style.setProperty('--d', (Math.random() * 24 - 12).toFixed(1) + 'deg');
      fig.appendChild(im);
      var ort = spur.querySelector('.d05-spur');
      ort.appendChild(fig);
      requestAnimationFrame(function () { requestAnimationFrame(function () { fig.classList.add('da'); }); });
      var alle = ort.querySelectorAll('.d05-k');
      if (alle.length > 18) alle[0].remove();
    }
    spur.addEventListener('pointermove', function (e) {
      if (Math.hypot(e.clientX - lx, e.clientY - ly) < 120) return;
      lx = e.clientX; ly = e.clientY; lege(e.clientX, e.clientY);
    });
  }

  /* Scroll-Züge: 4 in das D hinein, 8 auf die Mannschaft zu */
  var tick = false;
  function rechnen() {
    tick = false;
    var f = sichtbar(); if (!f) return;
    var h = innerHeight;
    var d = f.querySelector('[data-zieh="d"]');
    if (d) {
      var k = f.querySelector('.d04'), r = k.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, -r.top / (r.height - h)));
      d.style.transform = 'scale(' + (1 + Math.pow(p, 2.4) * 34) + ')';
    }
    var hi = f.querySelector('[data-zieh="hinein"]');
    if (hi) {
      var r2 = f.getBoundingClientRect(), s = Math.max(0, -r2.top);
      hi.style.transform = 'scale(' + (1 + Math.min(1, s / (h * .8)) * .35) + ')';
    }
  }
  function anstoss() { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', anstoss, { passive: true });
  addEventListener('resize', anstoss);
  document.addEventListener('click', function () { setTimeout(anstoss, 30); setTimeout(filme, 60); });
  addEventListener('keydown', function () { setTimeout(anstoss, 30); setTimeout(filme, 60); });
  anstoss();
})();
