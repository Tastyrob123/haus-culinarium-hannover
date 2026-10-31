/* Startseite · Wahlseite Bildwand Dirty Chicken: Taschenlampe (8), Diaprojektor (11), Band (12), Wand gleitet (13), Filme nur in der gezeigten Fassung. Nur transform, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  function drin(el) { if (el.closest('[hidden]')) return false; var r = el.getBoundingClientRect(); return r.bottom > -300 && r.top < innerHeight + 300; }

  /* 8 Taschenlampe: der Lichtkegel folgt der Maus (nur Transform); ohne Maus wandert er per CSS */
  document.querySelectorAll('.sdc8-wand').forEach(function (w) {
    var licht = w.querySelector('.sdc8-licht'), zx = 0, zy = 0, ax = 0, ay = 0, lauf = false, an = false;
    function schritt() { ax += (zx - ax) * .12; ay += (zy - ay) * .12; licht.style.transform = 'translate3d(' + ax.toFixed(1) + 'px,' + ay.toFixed(1) + 'px,0)'; if (an && (Math.abs(zx - ax) > .3 || Math.abs(zy - ay) > .3)) requestAnimationFrame(schritt); else lauf = false; }
    w.addEventListener('pointermove', function (e) { if (e.pointerType !== 'mouse') return; var r = w.getBoundingClientRect(); zx = e.clientX - r.left - r.width / 2; zy = e.clientY - r.top - r.height / 2; w.classList.add('maus'); an = true; if (!lauf) { lauf = true; requestAnimationFrame(schritt); } });
    w.addEventListener('pointerleave', function () { an = false; w.classList.remove('maus'); });
  });

  /* 11 Diaprojektor: alle 3,5 s das nächste Dia, Antippen der kleinen Bilder wählt; nur solange zu sehen */
  document.querySelectorAll('.sdc11').forEach(function (p) {
    var n = p.querySelectorAll('.sdc11-d').length, t = null, sicht = false;
    function zeige(i) { p.dataset.akt = i; p.querySelectorAll('.sdc11-k').forEach(function (k) { k.classList.toggle('an', +k.dataset.s === i); }); }
    function weiter() { zeige((+p.dataset.akt + 1) % n); }
    function start() { if (ruhig || t) return; t = setInterval(weiter, 3500); }
    function stopp() { clearInterval(t); t = null; }
    p.addEventListener('click', function (e) { var k = e.target.closest('.sdc11-k'); if (!k) return; zeige(+k.dataset.s); stopp(); start(); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { sicht = es[0].isIntersecting && !p.closest('[hidden]'); if (sicht) start(); else stopp(); }, { threshold: .3 }).observe(p);
  });

  /* 12 Band: Laufbalken und Pfeile */
  document.querySelectorAll('.sdc12').forEach(function (b) {
    var band = b.querySelector('.sdc12-band'), lauf = b.querySelector('.sdc12-lauf i');
    function stand() { var m = band.scrollWidth - band.clientWidth; var q = m > 0 ? band.scrollLeft / m : 0; lauf.style.transform = 'scaleX(' + (0.12 + .88 * q).toFixed(4) + ')'; }
    band.addEventListener('scroll', stand, { passive: true }); stand();
    b.addEventListener('click', function (e) { var k = e.target.closest('[data-sdc12]'); if (!k) return; band.scrollBy({ left: +k.dataset.sdc12 * band.clientWidth * .7, behavior: 'smooth' }); });
  });

  /* 13 Die Wand gleitet: jedes Feld bekommt seinen Versatz aus der Scroll-Lage */
  var G = [].slice.call(document.querySelectorAll('.sdc13-f')), lt = false;
  function rechnen() {
    lt = false; if (ruhig) return; var vh = innerHeight;
    G.forEach(function (z) { if (!drin(z)) return; var r = z.getBoundingClientRect(), p = Math.max(-1, Math.min(1, (r.top + r.height / 2 - vh / 2) / vh)); var f = parseFloat(z.style.getPropertyValue('--g0')) || 0; z.style.setProperty('--g', (p * f * Math.min(46, r.height * .1)).toFixed(1) + 'px'); });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true }); addEventListener('resize', takt, { passive: true }); rechnen();

  /* Filme der Wahlseite: nur die gezeigte Fassung bekommt ihre Quelle und spielt, solange sie zu sehen ist */
  var fio = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { var v = e.target.querySelector('video'); if (!v) return; if (e.isIntersecting) { if (!v.src) v.src = v.dataset.film; var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } else if (v.src) v.pause(); });
  }, { threshold: .3 }) : null;
  function filme(root) {
    (root || document).querySelectorAll('.filmw').forEach(function (f) { if (f.closest('[hidden]')) return; if (fio) fio.observe(f); else { var v = f.querySelector('video'); v.src = v.dataset.film; v.play(); } });
  }
  filme();
  var alt = window.culinariumNeu;
  window.culinariumNeu = function (root) { if (alt) alt(root); filme(root); setTimeout(takt, 50); };
})();

/* ---------- Zweite Runde: Daumenkino (22), Tausch (24), Lupe (25), Zug (27), Näher ran (29) */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  function drin(el) { if (el.closest('[hidden]')) return false; var r = el.getBoundingClientRect(); return r.bottom > -300 && r.top < innerHeight + 300; }
  function p(el) { var r = el.getBoundingClientRect(), vh = innerHeight; return Math.max(-1, Math.min(1, (r.top + r.height / 2 - vh / 2) / vh)); }
  /* 22 Daumenkino: blättert, solange es zu sehen ist */
  document.querySelectorAll('.sdc22-kino').forEach(function (k) {
    var n = k.querySelectorAll('.sdc22-bl').length, t = null;
    function start() { if (t || ruhig) return; t = setInterval(function () { k.dataset.s = (+k.dataset.s + 1) % n; }, 120); }
    function stopp() { clearInterval(t); t = null; }
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { if (es[0].isIntersecting && !k.closest('[hidden]')) start(); else stopp(); }, { threshold: .3 }).observe(k);
  });
  /* 24 Tausch: alle drei Sekunden tauschen zwei Kacheln den Platz (nur transform) */
  document.querySelectorAll('.sdc24-raster').forEach(function (r) {
    var K = [].slice.call(r.querySelectorAll('.sdc24-k')), n = K.length, platz = K.map(function (_k, i) { return i; }), t = null;
    function stellen() {
      var home = K.map(function (k) { k.style.transform = 'none'; return k.getBoundingClientRect(); });
      K.forEach(function (k, i) { var z = home[platz[i]], h = home[i]; k.style.transform = 'translate(' + (z.left - h.left).toFixed(1) + 'px,' + (z.top - h.top).toFixed(1) + 'px)'; });
    }
    function tausch() {
      var a = Math.floor(Math.random() * n), b = (a + 1 + Math.floor(Math.random() * (n - 1))) % n;
      var pa = platz[a]; platz[a] = platz[b]; platz[b] = pa; stellen();
    }
    function start() { if (t || ruhig) return; t = setInterval(tausch, 3000); }
    function stopp() { clearInterval(t); t = null; }
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { if (es[0].isIntersecting && !r.closest('[hidden]')) start(); else stopp(); }, { threshold: .3 }).observe(r);
    addEventListener('resize', function () { if (!r.closest('[hidden]')) stellen(); }, { passive: true });
  });
  /* 25 Lupe: der Kreis folgt der Maus */
  document.querySelectorAll('.sdc25-buehne').forEach(function (b) {
    var l = b.querySelector('.sdc25-b');
    b.addEventListener('pointermove', function (e) { if (e.pointerType !== 'mouse') return; var r = b.getBoundingClientRect(); b.classList.add('maus'); l.style.setProperty('--x', ((e.clientX - r.left) / r.width * 100).toFixed(2) + '%'); l.style.setProperty('--y', ((e.clientY - r.top) / r.height * 100).toFixed(2) + '%'); });
    b.addEventListener('pointerleave', function () { b.classList.remove('maus'); l.style.removeProperty('--x'); l.style.removeProperty('--y'); });
  });
  /* 27 Zug und 29 Näher ran: aus der Scroll-Lage */
  var Z = [].slice.call(document.querySelectorAll('.sdc27-zug')), N = [].slice.call(document.querySelectorAll('.sdc29-zoom')), lt = false;
  function rechnen() {
    lt = false; if (ruhig) return;
    Z.forEach(function (z) { if (!drin(z)) return; var q = Math.max(0, Math.min(1, (1 - p(z)) / 2)); z.style.transform = 'translate3d(' + (-(z.scrollWidth - z.parentNode.clientWidth) * q).toFixed(1) + 'px,0,0)'; });
    N.forEach(function (z) { if (!drin(z)) return; z.style.setProperty('--z', (1.02 + (1 - p(z)) * .07).toFixed(4)); });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true }); addEventListener('resize', takt, { passive: true }); rechnen();
  var alt = window.culinariumNeu;
  window.culinariumNeu = function (root) { if (alt) alt(root); setTimeout(takt, 50); };
})();
