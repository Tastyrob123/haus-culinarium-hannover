/* Culinarium · Öffnungszeiten in 15 Fassungen (nur Wahlseite). «Heute» nach Berliner Zeit; eine Nacht bis 3 Uhr zählt zum Vortag.
   Bewegung nur über transform, ein Takt für alle Scroll-Momente, nur die sichtbare Fassung. */
(function () {
  'use strict';
  var BIS = { do: 1, fr: 2, sa: 2 }, KEY = ['so', 'mo', 'di', 'mi', 'do', 'fr', 'sa'];
  var NAME = { do: 'Donnerstag', fr: 'Freitag', sa: 'Samstag' };
  var MON = ['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sep.', 'Okt.', 'Nov.', 'Dez.'];
  var ruhig = document.documentElement.classList.contains('ruhig') || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);

  /* Berliner Zeit */
  var t = new Date(new Date().toLocaleString('en-US', { timeZone: 'Europe/Berlin' }));
  var std = t.getHours(), nacht = new Date(t);
  if (std < 3) nacht.setDate(nacht.getDate() - 1);
  var heute = KEY[nacht.getDay()];
  var offenJetzt = !!BIS[heute] && (std >= 19 || std < BIS[heute]);
  var heuteSpaeter = !!BIS[heute] && std >= 3 && std < 19;
  /* der Abend, um den es geht: heute, sonst der nächste offene */
  var d = new Date(nacht), dran = heute;
  if (!offenJetzt && !heuteSpaeter) { do { d.setDate(d.getDate() + 1); } while (!BIS[KEY[d.getDay()]]); dran = KEY[d.getDay()]; }

  function an(sel) { document.querySelectorAll(sel).forEach(function (e) { e.classList.add('an'); }); }
  an('.zw01-neon [data-tag="' + dran + '"], .zw04-z [data-tag="' + dran + '"], .zw07-woche [data-tag="' + dran + '"], .zw08-z[data-tag="' + dran + '"], .zw11-zeilen [data-tag="' + dran + '"]');
  document.querySelectorAll('.zw10-satz em[data-tag]').forEach(function (e) { if (e.dataset.tag.split(' ').indexOf(dran) >= 0) e.classList.add('an'); });
  document.querySelectorAll('.zw02-t[data-tag="' + heute + '"]').forEach(function (e) { e.classList.add('heute'); });
  var rows = { do: 0, fr: 1, sa: 2 };
  document.querySelectorAll('.zw06-bon .z').forEach(function (e, i) { if (i === rows[dran]) e.classList.add('an'); });
  document.querySelectorAll('.zw14-fest .vz div').forEach(function (e, i) { if (i === rows[dran]) e.classList.add('an'); });

  /* Heute Abend */
  var tagWort = dran === heute ? 'Heute' : (function () { var m = new Date(nacht); m.setDate(m.getDate() + 1); return KEY[m.getDay()] === dran ? 'Morgen' : NAME[dran]; })();
  var gross, klein;
  if (offenJetzt) { gross = 'Gerade offen, bis <b>' + BIS[heute] + ' Uhr</b>.'; klein = 'Komm vorbei, Haasemannstraße 13.'; }
  else if (heuteSpaeter) { gross = 'Heute ab <b>19 Uhr</b> offen.'; klein = 'Bis ' + BIS[heute] + ' Uhr in der Nacht.'; }
  else { gross = tagWort + ' ab <b>19 Uhr</b> wieder offen.'; klein = (BIS[heute] ? 'Für heute ist Schluss.' : 'Heute ist geschlossen.') + ' ' + NAME[dran] + ' bis ' + BIS[dran] + ' Uhr.'; }
  document.querySelectorAll('[data-heute]').forEach(function (e) { e.innerHTML = gross; });
  document.querySelectorAll('[data-heute-unter]').forEach(function (e) { e.textContent = klein; });
  document.querySelectorAll('[data-bon-gruss]').forEach(function (e) { e.textContent = offenJetzt || heuteSpaeter ? 'BIS HEUTE ABEND!' : 'BIS ' + (tagWort === 'Morgen' ? 'MORGEN' : NAME[dran].toUpperCase()) + '!'; });

  /* Die nächsten Abende: Datum live */
  document.querySelectorAll('[data-naechste]').forEach(function (band) {
    var k = band.querySelectorAll('.zw12-k'), x = new Date(nacht), n = 0;
    if (BIS[heute] && !offenJetzt && !heuteSpaeter) x.setDate(x.getDate() + 1);
    while (n < k.length) {
      var key = KEY[x.getDay()];
      if (BIS[key]) {
        var c = k[n]; c.querySelector('.zw12-d b').textContent = NAME[key]; c.querySelector('.zw12-d span').textContent = x.getDate() + '. ' + MON[x.getMonth()];
        c.querySelector('.zw12-z').textContent = '19 bis ' + BIS[key] + ' Uhr';
        c.classList.toggle('heute', n === 0 && key === heute && (offenJetzt || heuteSpaeter)); n++;
      }
      x.setDate(x.getDate() + 1);
    }
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-zw12]'); if (b) { var band = b.closest('.zw12').querySelector('.zw12-band'); band.scrollBy({ left: +b.dataset.zw12 * band.clientWidth * .6, behavior: 'smooth' }); }
    var h = e.target.closest('[data-heft-auf]'); if (h) h.closest('[data-heft]').classList.toggle('auf-geklappt');
  });

  /* Streichholzheft klappt einmal auf, sobald es zu sehen ist */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { var h = e.target; setTimeout(function () { h.classList.add('auf-geklappt'); }, ruhig ? 0 : 900); io.unobserve(h); } }); }, { threshold: .6 });
    document.querySelectorAll('[data-heft]').forEach(function (h) { io.observe(h); });
    /* Von 19 bis 2: die Uhrzeit links geht mit */
    var uio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { var u = e.target.closest('.zw14').querySelector('[data-uhr]'); if (u) u.textContent = e.target.dataset.st; } }); }, { rootMargin: '-45% 0px -45% 0px' });
    document.querySelectorAll('.zw14-st').forEach(function (s) { uio.observe(s); });
  }

  /* Scroll-Momente: Untersetzer dreht, Foto zieht langsamer, Plakat richtet sich auf */
  if (ruhig) return;
  var vh = innerHeight, laeuft = false;
  function wert(el) { var r = el.getBoundingClientRect(); return r.bottom < -200 || r.top > vh + 200 || !r.height ? null : (r.top + r.height / 2 - vh / 2) / vh; }
  function takt() {
    laeuft = false;
    document.querySelectorAll('.wv:not([hidden]) [data-dreh]').forEach(function (e) { var p = wert(e.parentNode); if (p !== null) e.style.transform = 'rotate(' + (p * -40).toFixed(2) + 'deg)'; });
    document.querySelectorAll('.wv:not([hidden]) [data-zieh]').forEach(function (e) { var p = wert(e.parentNode); if (p !== null) e.style.transform = 'translate3d(0,' + (p * 9).toFixed(2) + '%,0)'; });
    document.querySelectorAll('.wv:not([hidden]) [data-plakat]').forEach(function (e) { var p = wert(e); if (p !== null) { var q = Math.max(0, Math.min(1, p + .1)); e.style.transform = 'rotate(' + (q * 6).toFixed(2) + 'deg) translate3d(0,' + (q * 40).toFixed(1) + 'px,0)'; } });
  }
  function los() { if (!laeuft) { laeuft = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', los, { passive: true });
  addEventListener('resize', function () { vh = innerHeight; los(); });
  document.addEventListener('click', function (e) { if (e.target.closest('#wleiste')) setTimeout(los, 60); });
  addEventListener('keydown', function () { setTimeout(los, 60); });
  los();
})();
