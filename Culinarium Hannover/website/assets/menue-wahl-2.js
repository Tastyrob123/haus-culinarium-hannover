/* Culinarium · «Was auf den Tisch kommt», zweite Runde: Säulen, Glocke, runder Tisch, Kino, gegenläufige Säulen, Laufband, Bogen,
   Kerze, lange Tafel, schwebendes Bild, Kamerafahrt, Umschlag und Lamellen. Nur transform und opacity, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var handy = matchMedia('(max-width:860px)');
  function sichtbar(sel) { return document.querySelectorAll('.wv:not([hidden]) ' + sel); }
  function klemm(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }

  /* Reiter: [data-q] zeigt [data-a] im selben [data-mx-tabs] */
  function reiter(box, i) {
    box.querySelectorAll('[data-q],[data-a]').forEach(function (x) {
      x.classList.toggle('an', (x.dataset.q !== undefined ? x.dataset.q : x.dataset.a) === String(i));
    });
    box.dataset.akt = i;
  }
  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-mx-tabs] [data-q]'); if (!q) return;
    var box = q.closest('[data-mx-tabs]'); box.dataset.halt = '1'; reiter(box, q.dataset.q);
  });
  /* 6 Untertitel: läuft von selbst weiter, solange niemand gewählt hat und es zu sehen ist */
  setInterval(function () {
    sichtbar('[data-mx-auto]').forEach(function (box) {
      if (box.dataset.halt || ruhig) return;
      var r = box.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
      var n = box.querySelectorAll('[data-q]').length;
      reiter(box, ((+box.dataset.akt || 0) + 1) % n);
    });
  }, 5600);

  /* 18 Kamera: Bildpunkt x,y mit Faktor s in die Mitte holen, ohne über den Rand zu fahren */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-mx-kamera] [data-z]'); if (!b) return;
    var box = b.closest('[data-mx-kamera]');
    box.querySelectorAll('[data-z]').forEach(function (x) { x.classList.toggle('an', x === b); });
    var z = b.dataset.z.split(',').map(Number), s = z[2];
    var tx = Math.min(0, Math.max(100 - 100 * s, 50 - z[0] * 100 * s)), ty = Math.min(0, Math.max(100 - 100 * s, 50 - z[1] * 100 * s));
    box.querySelector('.mx18-bild img').style.transform = 'translate(' + tx.toFixed(2) + '%,' + ty.toFixed(2) + '%) scale(' + s + ')';
  });

  /* 20 Lamellen: die verdeckte Seite bekommt das neue Bild, dann drehen sich alle Lamellen um 180 Grad */
  function lamellen(box, i) {
    var bilder = JSON.parse(box.dataset.bilder), grad = +(box.dataset.grad || 0);
    if (String(i) === (box.dataset.akt || '0')) return;
    var vorn = (grad / 180) % 2 === 0 ? 'v' : 'h', hinten = vorn === 'v' ? 'h' : 'v';
    grad += 180; box.dataset.grad = grad; box.dataset.akt = i;
    box.querySelectorAll('.mx20-s').forEach(function (s) {
      s.querySelector('i.' + hinten).style.backgroundImage = 'url(' + bilder[i] + ')';
      s.style.transform = 'rotateY(' + grad + 'deg)';
    });
    box.querySelectorAll('[data-l]').forEach(function (x) { x.classList.toggle('an', x.dataset.l === String(i)); });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-mx-lamellen] [data-l]'); if (!b) return;
    var box = b.closest('[data-mx-lamellen]'); box.dataset.halt = '1'; lamellen(box, b.dataset.l);
  });
  setInterval(function () {
    sichtbar('[data-mx-lamellen]').forEach(function (box) {
      if (box.dataset.halt || ruhig) return;
      var r = box.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
      lamellen(box, ((+box.dataset.akt || 0) + 1) % 4);
    });
  }, 4200);
  /* Bilder der Lamellen vorladen */
  document.querySelectorAll('[data-mx-lamellen]').forEach(function (box) { JSON.parse(box.dataset.bilder).forEach(function (u) { new Image().src = u; }); });

  if (ruhig) return;

  /* 12 Kerze: der Lichtkegel folgt dem Zeiger */
  document.querySelectorAll('[data-mx-kerze]').forEach(function (b) {
    var d = b.querySelector('.mx12-dunkel');
    b.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch') return;
      var r = b.getBoundingClientRect();
      b.classList.add('gefuehrt');
      d.style.transform = 'translate3d(' + (e.clientX - r.left - r.width / 2) + 'px,' + (e.clientY - r.top - r.height / 2) + 'px,0)';
    });
    b.addEventListener('pointerleave', function () { b.classList.remove('gefuehrt'); d.style.transform = ''; });
  });

  /* 16 Schwebendes Bild: folgt dem Zeiger über der Namensliste */
  document.querySelectorAll('[data-mx-folge]').forEach(function (box) {
    var s = box.querySelector('.mx16-schwebe'), liste = box.querySelector('.mx16-liste');
    box.querySelectorAll('.mx16-z').forEach(function (z) {
      z.addEventListener('pointerenter', function () {
        liste.classList.add('zeigt'); s.classList.add('an');
        box.querySelectorAll('.mx16-z').forEach(function (x) { x.classList.toggle('an', x === z); });
        s.querySelectorAll('figure').forEach(function (f) { f.classList.toggle('an', f.dataset.i === z.dataset.i); });
      });
    });
    liste.addEventListener('pointerleave', function () { liste.classList.remove('zeigt'); s.classList.remove('an'); });
    box.addEventListener('pointermove', function (e) {
      var r = box.getBoundingClientRect();
      s.style.transform = 'translate3d(' + (e.clientX - r.left + 36) + 'px,' + (e.clientY - r.top - s.offsetHeight * .5) + 'px,0) rotate(-2deg)';
    });
  });

  /* 15 Lange Tafel: Höhe der Strecke aus der Breite der Spur */
  function tafelHoehe() {
    sichtbar('[data-mx-quer]').forEach(function (q) {
      if (handy.matches) { q.style.height = ''; return; }
      var sp = q.querySelector('.mx15-spur');
      q.style.height = (sp.scrollWidth - innerWidth + innerHeight) + 'px';
    });
  }

  var lauf = false;
  function takt() {
    lauf = false;
    var h = innerHeight, w = innerWidth;
    /* 1 Säulen: jede Säule in eigenem Tempo */
    sichtbar('[data-mx-par]').forEach(function (s) {
      var r = s.parentNode.getBoundingClientRect(); if (r.bottom < -200 || r.top > h + 200) return;
      var p = (r.top + r.height / 2 - h / 2) / h;
      s.style.transform = 'translate3d(0,' + (p * +s.dataset.mxPar * h * -1.6).toFixed(1) + 'px,0)';
    });
    /* 2 Glocke: hebt sich, wenn der Teller in die Mitte kommt */
    sichtbar('[data-mx-glocke]').forEach(function (b) {
      var r = b.getBoundingClientRect(); if (r.bottom < -400 || r.top > h) return;
      var p = klemm((h * .78 - r.top) / (h * .5)), e = p * p * (3 - 2 * p);
      b.querySelector('.mx02-glocke').style.transform = 'translate3d(' + (e * 8) + '%,' + (e * -118) + '%,0) rotate(' + (e * -9) + 'deg)';
    });
    /* 5 Runder Tisch: dreht sich mit dem Scroll */
    sichtbar('[data-mx-dreh]').forEach(function (d) {
      var r = d.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var p = (r.top + r.height / 2 - h / 2) / h;
      d.style.setProperty('--d', (p * -70).toFixed(2) + 'deg');
    });
    /* 9 Gegenläufig: Küche hoch, Bar runter */
    sichtbar('[data-mx-gegen]').forEach(function (g) {
      var r = g.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var p = klemm((h - r.top) / (h + r.height));
      g.querySelectorAll('.mx09-sp').forEach(function (sp) {
        var l = sp.querySelector('.mx09-lauf'), weg = Math.max(0, l.offsetHeight - sp.clientHeight);
        var y = sp.classList.contains('l') ? -p * weg : -(1 - p) * weg;
        l.style.transform = 'translate3d(0,' + y.toFixed(1) + 'px,0)';
      });
    });
    /* 10 Laufband: Teller nach links, Drinks nach rechts */
    sichtbar('[data-mx-lauf]').forEach(function (b) {
      var r = b.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var p = klemm((h - r.top) / (h + r.height)), sp = b.firstElementChild, weg = Math.max(0, sp.scrollWidth - w);
      var x = +b.dataset.mxLauf < 0 ? -p * weg : -(1 - p) * weg;
      sp.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
    });
    /* 11 Bogen: öffnet sich, bis die Tafel den Schirm füllt */
    sichtbar('[data-mx-bogen]').forEach(function (b) {
      var r = b.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var p = klemm(-r.top / (r.height - h)), e = p * p;
      b.querySelector('.mx11-tor').style.transform = 'translate(-50%,-50%) scale(' + (1 + e * 5.5).toFixed(3) + ')';
    });
    /* 15 Lange Tafel: die Spur zieht seitwärts */
    if (!handy.matches) sichtbar('[data-mx-quer]').forEach(function (q) {
      var r = q.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var sp = q.querySelector('.mx15-spur'), p = klemm(-r.top / (r.height - h));
      sp.style.transform = 'translate3d(' + (-p * (sp.scrollWidth - w)).toFixed(1) + 'px,0,0)';
    });
    /* 8 Wand: das grosse Bild kommt langsam näher */
    sichtbar('[data-mx-zoom] img').forEach(function (im) {
      var r = im.parentNode.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var p = klemm((h - r.top) / (h + r.height));
      im.style.transform = 'scale(' + (1.02 + p * .16).toFixed(4) + ')';
    });
    /* 19 Einladung: die Karte zieht aus dem Umschlag */
    sichtbar('[data-mx-brief]').forEach(function (b) {
      var br = b.querySelector('.mx19-brief'), r = br.getBoundingClientRect(); if (r.bottom < -200 || r.top > h + 200) return;
      var p = klemm((h * .95 - r.top) / (h * .6)), e = 1 - Math.pow(1 - p, 3);
      var k = b.querySelector('.mx19-karte'), weg = k.offsetHeight - br.offsetHeight * .76;
      k.style.transform = 'translate3d(0,' + ((1 - e) * weg).toFixed(1) + 'px,0)';
    });
  }
  function an() { if (!lauf) { lauf = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', an, { passive: true });
  addEventListener('resize', function () { tafelHoehe(); an(); });
  document.addEventListener('click', function () { setTimeout(function () { tafelHoehe(); an(); }, 60); });
  addEventListener('load', function () { tafelHoehe(); an(); });
  tafelHoehe(); an();
})();
