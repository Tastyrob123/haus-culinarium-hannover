/* Culinarium · «Drei Leute, ein Haus.» zur Wahl, zweite Runde: Bühne, Band, stehende Bühne, Theke entlang, Rückwand, Drehbühne, Fenster, Takt.
   Nur transform und opacity, nativer Scroll. */
(function () {
  'use strict';
  var schmal = matchMedia('(max-width:860px)');
  function anteil(el, a, b) { var r = el.getBoundingClientRect(), h = innerHeight; return Math.max(0, Math.min(1, (h * a - r.top) / (h * b))); }
  function waehle(wurzel, i) { wurzel.querySelectorAll('[data-i]').forEach(function (x) { x.classList.toggle('an', +x.dataset.i === i); }); }
  var laeuft = false;
  function rechne() {
    laeuft = false;
    /* 6 Die Bühne bleibt stehen: wer der Mitte am nächsten ist, steht auf der Bühne */
    document.querySelectorAll('[data-t2-still]').forEach(function (w) {
      if (!w.offsetParent) return; var best = 0, min = 1e9;
      w.querySelectorAll('.t2-06-b').forEach(function (b) { var r = b.getBoundingClientRect(), d = Math.abs(r.top + r.height / 2 - innerHeight / 2); if (d < min) { min = d; best = +b.dataset.i; } });
      w.querySelectorAll('.t2-06-buehne figure').forEach(function (f) { f.classList.toggle('an', +f.dataset.i === best); });
    });
    /* 9 An der Theke entlang: der Zug fährt nach links, solange der Abschnitt durchs Bild geht */
    document.querySelectorAll('[data-t2-zug]').forEach(function (z) {
      if (!z.offsetParent) return; var s = z.firstElementChild;
      if (schmal.matches) { s.style.removeProperty('--x'); return; }
      s.style.setProperty('--x', (-(s.scrollWidth - z.clientWidth) * anteil(z, 1, 1.5)).toFixed(1) + 'px');
    });
    /* 16 Die Rückwand zieht auf: von 1.12 auf 1 */
    document.querySelectorAll('[data-t2-wand]').forEach(function (w) { if (w.offsetParent) w.firstElementChild.style.setProperty('--s', (1.12 - .12 * anteil(w, 1, 1.1)).toFixed(4)); });
    /* 18 Fensterwand: die Bilder ziehen in ihren Fenstern */
    document.querySelectorAll('[data-t2-fenster]').forEach(function (w) {
      if (!w.offsetParent) return; var r = w.getBoundingClientRect(), t = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
      w.querySelectorAll('.t2-18-f').forEach(function (f) { f.firstElementChild.style.setProperty('--y', (Math.max(-1, Math.min(1, t)) * f.clientHeight * .1).toFixed(1) + 'px'); });
    });
  }
  function bitte() { if (!laeuft) { laeuft = true; requestAnimationFrame(rechne); } }
  addEventListener('scroll', bitte, { passive: true }); addEventListener('resize', bitte);
  addEventListener('keydown', function () { setTimeout(bitte, 80); setTimeout(bitte, 400); });
  document.addEventListener('click', function () { setTimeout(bitte, 80); });

  /* 4 Namen holen auf die Bühne: überfahren oder antippen */
  document.querySelectorAll('[data-t2-buehne]').forEach(function (w) {
    w.querySelectorAll('.t2-04-n').forEach(function (n) {
      var los = function () { waehle(w, +n.dataset.i); };
      n.addEventListener('mouseenter', los); n.addEventListener('focus', los); n.addEventListener('click', los);
    });
  });

  /* 5 Band: Pfeile blättern um eine Bildbreite */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-t2-band]'); if (!b) return;
    var bahn = b.closest('.t2-05').querySelector('[data-t2-bahn]'); bahn.scrollBy({ left: +b.dataset.t2Band * bahn.clientWidth * .6, behavior: 'smooth' });
  });

  /* 17 Drehbühne: Pfeil, Name oder Bild dreht den Ring zur Person */
  document.querySelectorAll('[data-t2-ring]').forEach(function (w) {
    var ring = w.querySelector('.t2-17-ring'), stand = 0, schritt = 0;
    /* Falls ein Browser die Tiefe flach rechnet: das vordere Bild liegt auch in der Reihenfolge oben */
    function tiefe() { ring.querySelectorAll('figure').forEach(function (f) { var a = (((+f.style.getPropertyValue('--n') - 1) * 40 - 120 * stand) % 360 + 540) % 360 - 180; f.style.zIndex = 20 - Math.round(Math.abs(a) / 20); }); }
    tiefe();
    function dreh(i) {
      var ziel = ((i % 3) + 3) % 3, d = ziel - stand; if (d > 1) d -= 3; if (d < -1) d += 3;
      schritt += d; stand = ziel; ring.style.setProperty('--w', (-120 * schritt) + 'deg'); tiefe();
      w.querySelectorAll('.t2-17-namen [data-i], .t2-17-text').forEach(function (x) { x.classList.toggle('an', +x.dataset.i === ziel); });
    }
    w.addEventListener('click', function (e) {
      var p = e.target.closest('[data-t2-dreh]'); if (p) return dreh(stand + +p.dataset.t2Dreh);
      var n = e.target.closest('.t2-17-namen [data-i]'); if (n) return dreh(+n.dataset.i);
      var f = e.target.closest('.t2-17-ring figure'); if (f) dreh(+f.dataset.p);
    });
  });

  /* 20 Im Takt: reihum wechselt immer nur eine Karte ihr Bild */
  var takt = 0;
  setInterval(function () {
    document.querySelectorAll('[data-t2-takt]').forEach(function (w) {
      if (!w.offsetParent || matchMedia('(prefers-reduced-motion:reduce)').matches) return;
      var r = w.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
      var st = w.querySelectorAll('.t2-20-stapel')[takt % 3], fs = st.children, an = [].indexOf.call(fs, st.querySelector('.an'));
      fs[an].classList.remove('an'); fs[(an + 1) % fs.length].classList.add('an');
    });
    takt++;
  }, 1800);

  bitte(); addEventListener('load', bitte);
})();
