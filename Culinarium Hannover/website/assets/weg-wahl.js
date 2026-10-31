/* Culinarium · Der Weg in 15 Fassungen (nur Wahlseite): Tag und Nacht, Stadtplan, Briefchen, Abzüge, Band; Licht, Zoom und Wandern am Scrollen. Nur transform und opacity. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');

  function druecke(knoepfe, an) { knoepfe.forEach(function (b) { b.setAttribute('aria-pressed', b === an ? 'true' : 'false'); }); }

  function stapel(r) {
    var k = [].slice.call(r.querySelectorAll('.wg12-a'));
    var oben = k.reduce(function (a, b) { return +a.style.zIndex > +b.style.zIndex ? a : b; });
    if (oben.classList.contains('weg')) return;
    oben.classList.add('weg');
    setTimeout(function () {
      k.forEach(function (x) { x.style.zIndex = +x.style.zIndex + 1; });
      oben.style.zIndex = 1;
      oben.classList.remove('weg');
    }, ruhig ? 0 : 520);
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-wg-zeit]');
    if (t) { var r4 = t.closest('.wg04'); r4.dataset.zeit = t.dataset.wgZeit; druecke([].slice.call(r4.querySelectorAll('[data-wg-zeit]')), t); return; }
    var p = e.target.closest('[data-wg-ort]');
    if (p) { var r8 = p.closest('.wg08'); r8.dataset.ort = p.dataset.wgOrt; druecke([].slice.call(r8.querySelectorAll('[data-wg-ort]')), p); return; }
    if (e.target.closest('[data-wg-klappe]')) { e.target.closest('.wg06').classList.toggle('zu'); return; }
    var s = e.target.closest('[data-wg-stapel]');
    if (s) { stapel(s.closest('.wg12')); return; }
    var b = e.target.closest('[data-wg-band]');
    if (b) { var band = b.closest('.wg10').querySelector('.wg10-band'); band.scrollBy({ left: +b.dataset.wgBand * band.clientWidth * .7, behavior: 'smooth' }); }
  });

  /* Am Scrollen: Licht geht an (opacity), Rahmen kommen näher (scale), Bilder wandern gegeneinander (translate) */
  if (ruhig) return;
  var els = [].slice.call(document.querySelectorAll('[data-wg-lauf]')), lt = false;
  function bild() {
    lt = false;
    var vh = innerHeight;
    els.forEach(function (el) {
      if (el.closest('[hidden]')) return;
      var r = el.getBoundingClientRect();
      if (r.bottom < -vh * .2 || r.top > vh * 1.2) return;
      var p = Math.max(0, Math.min(1, (vh - r.top) / (vh + r.height))), art = el.dataset.wgLauf, f = +el.dataset.f || 0;
      if (art === 'licht') el.style.opacity = (.15 + Math.min(1, p * 1.6) * .85).toFixed(3);
      else if (art === 'zoom') el.style.transform = 'scale(' + (1 + (p - .5) * f).toFixed(3) + ')';
      else if (art === 'drift') el.style.transform = 'translate3d(0,' + ((p - .5) * f).toFixed(1) + 'px,0)';
      else if (art === 'dreh') el.style.transform = 'rotate(' + ((p - .5) * f).toFixed(1) + 'deg)';
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(bild); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', takt, { passive: true });
  document.addEventListener('click', function () { setTimeout(takt, 60); });
  addEventListener('keydown', function () { setTimeout(takt, 60); });
  takt();
})();
