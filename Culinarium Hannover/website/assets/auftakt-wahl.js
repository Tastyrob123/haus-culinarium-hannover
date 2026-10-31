/* Culinarium · Momente der 15 Auftakte auf der Wahlseite. Nur transform und opacity, nativer Scroll; rechnet nur die sichtbare Fassung. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  function sicht(cls) { var f = document.querySelector('.vx .' + cls); return f && !f.hidden ? f : null; }
  function klemme(v, a, b) { return Math.max(a, Math.min(b, v)); }
  var maus = { x: innerWidth * .5, y: innerHeight * .55, da: false };
  addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') { maus.x = e.clientX; maus.y = e.clientY; maus.da = true; } }, { passive: true });

  /* ---------- 1 Durchs Wort: der Deckel wächst um einen Punkt im I, bis der Raum frei ist */
  var deckel = document.querySelector('.vw-deckel');
  function wort() {
    var f = sicht('v-wort'); if (!f) return;
    var r = f.getBoundingClientRect(), weg = r.height - innerHeight;
    var p = klemme(-r.top / weg, 0, 1), e = p * p * (3 - 2 * p);
    var breit = deckel.clientWidth;
    var gross = Math.max(innerWidth, innerHeight) * .72 / (breit * .0191);   // halbe Strichbreite des I = 1,91 % der Wortmarke (gemessen)
    var s = Math.pow(gross, e);
    deckel.style.transform = 'translate(-50%,-50%) scale(' + s.toFixed(4) + ')';
  }

  /* ---------- 14 Randlos: das Bild zoomt beim Hinausscrollen langsam heran */
  function randlos() {
    var f = sicht('v-randlos'); if (!f) return;
    var r = f.getBoundingClientRect(), p = klemme(-r.top / r.height, 0, 1);
    f.querySelector('.vr-foto').style.transform = 'scale(' + (1 + .16 * p).toFixed(4) + ')';
  }
  var lt = false;
  function scroll() { if (lt) return; lt = true; requestAnimationFrame(function () { lt = false; wort(); randlos(); }); }
  if (!ruhig) { addEventListener('scroll', scroll, { passive: true }); addEventListener('resize', scroll, { passive: true }); }

  /* ---------- 5 Kerzenlicht, 8 Ebenen, 11 Draussen/drinnen: ein Takt, weich nachgezogen */
  var licht = { x: 0, y: 0, start: false }, eb = { x: 0, y: 0 }, tuer = { p: 50, ziel: 50, griff: false };
  function takt(t) {
    requestAnimationFrame(takt);
    var f, r;
    if ((f = sicht('v-licht'))) {
      r = f.getBoundingClientRect();
      if (r.bottom > 0 && r.top < innerHeight) {
        var L = f.querySelector('.vk-licht'), I = f.querySelector('.vk-innen'), R = L.offsetWidth / 2;
        if (I.__w !== r.width || I.__h !== r.height) { I.style.width = r.width + 'px'; I.style.height = r.height + 'px'; I.__w = r.width; I.__h = r.height; }
        var zx, zy;
        if (maus.da) { zx = maus.x - r.left; zy = maus.y - r.top; }
        else { zx = r.width * (.5 + .3 * Math.sin(t / 3100)); zy = r.height * (.56 + .14 * Math.sin(t / 2300)); }
        if (!licht.start) { licht.x = r.width * .32; licht.y = r.height * .6; licht.start = true; }
        licht.x += (zx - licht.x) * .09; licht.y += (zy - licht.y) * .09;
        var dx = (licht.x - R).toFixed(1), dy = (licht.y - R).toFixed(1);
        L.style.transform = 'translate3d(' + dx + 'px,' + dy + 'px,0)';
        I.style.transform = 'translate3d(' + (-dx) + 'px,' + (-dy) + 'px,0)';
      }
    }
    if ((f = sicht('v-ebenen'))) {
      var ax = maus.da ? (maus.x / innerWidth - .5) * 2 : Math.sin(t / 2600) * .5, ay = maus.da ? (maus.y / innerHeight - .5) * 2 : Math.cos(t / 3300) * .4;
      eb.x += (ax - eb.x) * .06; eb.y += (ay - eb.y) * .06;
      f.querySelectorAll('.ve-e').forEach(function (e) {
        var k = parseFloat(e.dataset.t);
        e.style.transform = 'translate3d(' + (eb.x * k * 34).toFixed(1) + 'px,' + (eb.y * k * 22).toFixed(1) + 'px,0)';
      });
    }
    if ((f = sicht('v-tuer'))) {
      tuer.p += (tuer.ziel - tuer.p) * (tuer.griff ? .35 : .08);
      f.style.setProperty('--p', tuer.p.toFixed(2) + '%');
    }
  }
  if (!ruhig) requestAnimationFrame(takt);

  /* 11: Maus führt die Naht, am Handy wird sie gezogen; beim Zeigen einmal ein kleiner Stups */
  var vt = document.querySelector('.v-tuer');
  if (vt) {
    function setze(x) { var r = vt.getBoundingClientRect(); tuer.ziel = klemme((x - r.left) / r.width * 100, 3, 97); }
    vt.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse' || tuer.griff) setze(e.clientX); });
    vt.addEventListener('pointerdown', function (e) { if (e.target.closest('a,button')) return; tuer.griff = true; setze(e.clientX); });
    addEventListener('pointerup', function () { tuer.griff = false; });
    new MutationObserver(function () { if (vt.classList.contains('offen')) { tuer.p = 74; tuer.ziel = 50; } }).observe(vt, { attributes: true, attributeFilter: ['class'] });
    if (ruhig) vt.style.setProperty('--p', '50%');
  }

  /* ---------- 3 Was zum Abend gehört: Zeigen tauscht das Bild; ohne Hand wechselt es von selbst */
  var vl = document.querySelector('.v-liste');
  if (vl) {
    var li = [].slice.call(vl.querySelectorAll('.vl-zeilen li')), bi = [].slice.call(vl.querySelectorAll('.vl-bild .vb')), jetzt = 0, selbst = true;
    function zeige(n) {
      if (n === jetzt) return;
      bi.forEach(function (b) { b.classList.remove('war'); });
      bi[jetzt].classList.add('war');
      li[jetzt].classList.remove('an'); bi[jetzt].classList.remove('an');
      jetzt = n; li[n].classList.add('an'); bi[n].classList.add('an');
    }
    li.forEach(function (l, i) {
      l.addEventListener('pointerenter', function () { selbst = false; zeige(i); });
      l.addEventListener('click', function () { selbst = false; zeige(i); });
    });
    setInterval(function () { if (selbst && !vl.hidden && !ruhig) zeige((jetzt + 1) % li.length); }, 3600);
  }

  /* ---------- 9 Der Stapel: der unterste Abzug fliegt ein und landet oben */
  var st = document.querySelector('.vs-stapel');
  if (st) {
    [].forEach.call(st.children, function (c) { c.style.setProperty('--rot', getComputedStyle(c).getPropertyValue('--rot')); });
    st.addEventListener('click', function () {
      var v = st.closest('.fassung'); v.classList.add('gespielt');
      var unten = st.firstElementChild; unten.classList.add('weg'); st.appendChild(unten);
      unten.offsetWidth;   // Ausgangslage festhalten, dann landen
      unten.classList.remove('weg');
    });
  }
})();
