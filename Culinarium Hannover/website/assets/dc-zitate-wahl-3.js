/* Dirty Chicken · Wahlseite Zitate, Runde 3: Gesprächsfetzen (2), Wendetafel (4), Litfasssäule (5), Filmplakat (10), Scheinwerfer (11),
   Glocke (12), Typoplakat (14), Schreibmaschine (15). Nur transform und opacity, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  var IO = 'IntersectionObserver' in window;
  function sichtbar(el) { return !el.closest('[hidden]'); }
  function drin(el) { if (!sichtbar(el)) return false; var r = el.getBoundingClientRect(); return r.bottom > -300 && r.top < innerHeight + 300; }
  function p(el) { var r = el.getBoundingClientRect(); return Math.max(-1, Math.min(1, (r.top + r.height / 2 - innerHeight / 2) / innerHeight)); }
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }

  /* 4 Wendetafel: jede Lamelle klappt nacheinander schmal, wechselt den Inhalt und klappt wieder auf (nur scaleX) */
  function tafel(t) {
    if (t.__ok) return; t.__ok = true;
    var daten = JSON.parse(t.parentNode.querySelector('.zv4-daten').textContent), n = 0;
    var lam = $$('.zv4-f', t), nr = t.parentNode.querySelector('.zv4-nr');
    t.weiter = function () {
      n = (n + 1) % daten.length;
      if (nr) nr.textContent = (n + 1) + ' / ' + daten.length;
      lam.forEach(function (f, j) {
        setTimeout(function () {
          if (ruhig) { f.firstChild.innerHTML = daten[n]; return; }
          f.classList.add('zu');
          setTimeout(function () { f.firstChild.innerHTML = daten[n]; f.classList.remove('zu'); }, 370);
        }, ruhig ? 0 : j * 55);
      });
    };
    t.addEventListener('click', function () { t.weiter(); zeit(t); });
    t.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t.weiter(); zeit(t); } });
  }
  function zeit(t) { clearInterval(t.__z); if (!ruhig && t.__an) t.__z = setInterval(function () { if (sichtbar(t)) t.weiter(); }, 3600); }
  var tio = IO ? new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.__an = e.isIntersecting; tafel(e.target); zeit(e.target); }); }, { threshold: .35 }) : null;
  $$('.zv4').forEach(function (t) { tafel(t); if (tio) tio.observe(t); });

  /* 12 Unter der Glocke: hebt sich beim Ankommen, antippen deckt ab und serviert den nächsten Satz */
  var gio = IO ? new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting && sichtbar(e.target)) setTimeout(function () { e.target.classList.add('offen'); }, 500); }); }, { threshold: .45 }) : null;
  $$('.zv12-tisch').forEach(function (t) { if (gio) gio.observe(t); else t.classList.add('offen'); });
  document.addEventListener('click', function (e) {
    var k = e.target.closest('.zv12-knopf'); if (!k) return;
    var w = k.closest('.zv12'), t = w.querySelector('.zv12-tisch'), n = (+t.dataset.akt + 1) % 5, nr = w.querySelector('.zv12-nr');
    t.classList.remove('offen');
    setTimeout(function () { t.dataset.akt = n; if (nr) nr.textContent = (n + 1) + ' / 5'; }, ruhig ? 0 : 750);
    setTimeout(function () { t.classList.add('offen'); }, ruhig ? 0 : 1050);
  });

  /* 14 Typoplakat: jede Zeile so gross, dass sie die Breite füllt */
  function passen(root) {
    $$('.zv14', root).forEach(function (b) {
      if (!sichtbar(b)) return;
      var cs = getComputedStyle(b), w = b.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      $$('.zv14-t', b).forEach(function (t) { t.style.setProperty('--fs', '100px'); var tw = t.offsetWidth || 1; t.style.setProperty('--fs', Math.min(240, 100 * w / tw * .985).toFixed(1) + 'px'); });
    });
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { passen(); }); else passen();

  /* Scroll-getrieben */
  var FE = $$('.zv2-s[data-tiefe]'), LS = $$('.zv5-saeule'), PL = $$('.zv10-bild img'), SW = $$('.zv11'), SM = $$('.zv15-papier');
  var lt = false;
  function rechnen() {
    lt = false;
    FE.forEach(function (f) { var r = f.closest('.zv2-raum'); if (!drin(r) || ruhig) return; f.style.transform = 'translate3d(0,' + (p(r) * parseFloat(f.dataset.tiefe) * innerHeight).toFixed(1) + 'px,0)'; });
    LS.forEach(function (s) {
      if (!drin(s)) return;
      var ps = $$('.zv5-p', s), k = s.querySelector('.zv5-koerper'), R = k.clientWidth / 2, n = ps.length;
      var basis = ruhig ? 0 : (-p(s) * 160);   /* Grad: die Säule dreht sich mit dem Scrollen */
      ps.forEach(function (el, i) {
        var a = ((basis + i * 360 / n) % 360 + 540) % 360 - 180, rad = a * Math.PI / 180, c = Math.cos(rad);
        if (c <= 0.02) { el.style.opacity = '0'; el.style.transform = 'translate3d(0,0,0) scaleX(.02)'; return; }
        el.style.opacity = (0.35 + 0.65 * c).toFixed(3);
        el.style.transform = 'translate3d(' + (R * Math.sin(rad)).toFixed(1) + 'px,0,0) scaleX(' + c.toFixed(3) + ')';
        el.style.zIndex = String(Math.round(c * 100));
      });
    });
    PL.forEach(function (im) { var b = im.parentNode; if (!drin(b) || ruhig) return; im.style.transform = 'scale(' + (1 + Math.max(0, p(b) + .2) * .18).toFixed(4) + ')'; });
    SW.forEach(function (w) {
      if (!drin(w)) return;
      var ss = $$('.zv11-s', w), best = null, bd = 1e9, mitte = innerHeight * .5;
      ss.forEach(function (s) { var r = s.getBoundingClientRect(), d = Math.abs(r.top + r.height / 2 - mitte); if (d < bd) { bd = d; best = s; } });
      ss.forEach(function (s) { s.classList.toggle('an', s === best); });
      var l = w.querySelector('.zv11-licht'); if (!best || !l) return;
      var wr = w.getBoundingClientRect(), br = best.getBoundingClientRect();
      var x = br.left - wr.left + br.width * (best.classList.contains('r') ? .62 : .38) - l.offsetWidth / 2, y = br.top - wr.top + br.height / 2 - l.offsetHeight / 2;
      l.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)';
    });
    SM.forEach(function (pa) {
      if (!drin(pa)) return;
      var r = pa.getBoundingClientRect(), t = ruhig ? 1 : Math.max(0, Math.min(1, (innerHeight * .85 - r.top) / (r.height * .9)));
      var z = pa.__z || (pa.__z = $$('.zv15-s span', pa)), n = Math.round(t * z.length);
      if (pa.__n === n) return; pa.__n = n;
      z.forEach(function (s, i) { s.classList.toggle('an', i < n); });
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', function () { passen(); takt(); }, { passive: true });
  rechnen();
  var alt = window.culinariumNeu;
  window.culinariumNeu = function (root) {
    if (alt) alt(root);
    $$('.zv12-tisch', root).forEach(function (t) { t.classList.remove('offen'); if (gio) { gio.unobserve(t); gio.observe(t); } });
    $$('.zv15-papier', root).forEach(function (pa) { pa.__n = -1; });
    passen(root); setTimeout(takt, 50);
  };
})();
