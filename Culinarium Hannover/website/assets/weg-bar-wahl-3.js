/* Culinarium · Der Weg, «Die Bar» in 15 Fassungen, Runde 3 (nur Wahlseite).
   Heute in der Woche markieren, Abende antippen, Linie füllt sich, Wand geht auf, Bühne wechselt beim Scrollen. Nur transform und opacity.
   Wandern (drift, quer) macht weg-bar-wahl.js, das Bild an der Maus hr.js. */
(function () {
  'use strict';
  var handy = matchMedia('(max-width:860px)'), ruhig = document.documentElement.classList.contains('ruhig');
  /* Die Woche: heute markieren */
  document.querySelectorAll('[data-zd-woche]').forEach(function (w) {
    var d = new Date().getDay(); d = d === 0 ? 7 : d;
    var t = w.querySelector('.zd01-t[data-tag="' + d + '"]'); if (t) t.classList.add('heute');
  });
  /* Drei Abende: antippen tauscht die Wand an derselben Stelle */
  document.querySelectorAll('[data-zd-tap]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      var k = e.target.closest('.zd03-k'); if (!k) return;
      var i = k.dataset.i;
      b.querySelectorAll('.zd03-k').forEach(function (x) { var an = x.dataset.i === i; x.classList.toggle('an', an); x.setAttribute('aria-pressed', an ? 'true' : 'false'); });
      b.querySelectorAll('.zd03-wand').forEach(function (x) { var an = x.dataset.i === i; x.classList.toggle('an', an); if (an) x.removeAttribute('aria-hidden'); else x.setAttribute('aria-hidden', 'true'); });
    });
  });
  if (ruhig) return;
  var els = [].slice.call(document.querySelectorAll('[data-zd]')), lt = false;
  var kl = function (x) { return Math.max(0, Math.min(1, x)); };
  function sichtbar(el, r, vh) { return !el.closest('[hidden]') && r.bottom > -vh * .2 && r.top < vh * 1.2; }
  function bild() {
    lt = false;
    var vh = innerHeight;
    /* Das Fenster: der Satz kommt, sobald das Fenster im oberen Drittel steht (auf der Wahlseite greift der Beobachter der Seite nicht zuverlässig) */
    document.querySelectorAll('.zd13').forEach(function (f) {
      if (f.closest('[hidden]')) return;
      var fr = f.getBoundingClientRect();
      if (fr.top < vh * .45 && fr.bottom > 0) f.querySelector('.fenster-satz').classList.add('da');
    });
    els.forEach(function (el) {
      var art = el.dataset.zd, host = art === 'fuell' ? el.closest('.zd02') : el;
      var r = host.getBoundingClientRect();
      if (!sichtbar(host, r, vh)) return;
      if (art === 'fuell') {
        /* die Linie füllt sich, bis der Strahl in der Bildschirmmitte steht */
        var p = kl((vh - r.top) / (vh * .5 + r.height * .5));
        el.style.transform = 'scaleX(' + p.toFixed(3) + ')';
      } else if (art === 'wand') {
        /* obere und untere Reihe rücken auseinander, bis die Wand in der Mitte steht */
        var wand = el.querySelector('.zd04-wand'), reihen = el.querySelectorAll('.zd04-reihe');
        var g = parseFloat(getComputedStyle(wand).rowGap) - 10, q = kl((vh - r.top) / (vh * .55 + r.height * .5));
        var w = ((1 - q) * g).toFixed(1);
        reihen[0].style.transform = 'translate3d(0,' + w + 'px,0)';
        reihen[2].style.transform = 'translate3d(0,-' + w + 'px,0)';
      } else if (art === 'buehne') {
        if (handy.matches) return;
        var p2 = kl(-r.top / Math.max(1, r.height - vh)), i = Math.min(2, Math.floor(p2 * 3));
        if (el.__i === i) return;
        el.__i = i;
        el.querySelectorAll('.zd15-tag').forEach(function (t) { t.classList.toggle('an', +t.dataset.i === i); });
        el.querySelectorAll('.zd15-wand').forEach(function (t) { t.classList.toggle('an', +t.dataset.i === i); });
      }
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(bild); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', takt, { passive: true });
  document.addEventListener('click', function () { setTimeout(takt, 60); });
  addEventListener('keydown', function () { setTimeout(takt, 60); });
  takt();
})();
