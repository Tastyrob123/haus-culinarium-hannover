/* Culinarium · Öffnungszeiten in 15 Fassungen, zweite Runde (nur Wahlseite). «Heute» nach Berliner Zeit; eine Nacht bis 3 Uhr zählt zum Vortag.
   Markiert den Abend, um den es geht, schreibt «Heute» und die Daten der nächsten Abende, blättert das Band. Bewegung macht culinarium.js. */
(function () {
  'use strict';
  var BIS = { do: 1, fr: 2, sa: 2 }, KEY = ['so', 'mo', 'di', 'mi', 'do', 'fr', 'sa'];
  var NAME = { do: 'Donnerstag', fr: 'Freitag', sa: 'Samstag' };
  var MON = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];

  var t = new Date(new Date().toLocaleString('en-US', { timeZone: 'Europe/Berlin' }));
  var std = t.getHours(), nacht = new Date(t);
  if (std < 3) nacht.setDate(nacht.getDate() - 1);
  var heute = KEY[nacht.getDay()];
  var offenJetzt = !!BIS[heute] && (std >= 19 || std < BIS[heute]);
  var heuteSpaeter = !!BIS[heute] && std >= 3 && std < 19;
  var d = new Date(nacht), dran = heute;
  if (!offenJetzt && !heuteSpaeter) { do { d.setDate(d.getDate() + 1); } while (!BIS[KEY[d.getDay()]]); dran = KEY[d.getDay()]; }

  /* der Abend, um den es geht, bekommt die Kerzenfarbe */
  document.querySelectorAll('.zw [data-tag]').forEach(function (e) { if (e.dataset.tag.split(' ').indexOf(dran) >= 0) e.classList.add('an'); });

  /* Heute */
  var morgen = new Date(nacht); morgen.setDate(morgen.getDate() + 1);
  var wann = KEY[morgen.getDay()] === dran ? 'Morgen' : NAME[dran];
  var gross, klein;
  if (offenJetzt) { gross = 'Gerade offen, bis <b>' + BIS[heute] + ' Uhr</b>.'; klein = 'Komm vorbei, Haasemannstraße 13 in Linden.'; }
  else if (heuteSpaeter) { gross = 'Heute<br>ab <b>19 Uhr</b> offen.'; klein = 'Bis ' + BIS[heute] + ' Uhr in der Nacht. Reservieren geht per Nachricht oder Telefon.'; }
  else { gross = wann + '<br>ab <b>19 Uhr</b> wieder offen.'; klein = (BIS[heute] ? 'Für heute ist Schluss.' : 'Heute ist geschlossen.') + ' Reservieren geht per Nachricht oder Telefon.'; }
  document.querySelectorAll('[data-heute]').forEach(function (e) { e.innerHTML = gross; });
  document.querySelectorAll('[data-heute-unter]').forEach(function (e) { e.textContent = klein; });

  /* Die nächsten Abende: Datum live */
  document.querySelectorAll('[data-naechste]').forEach(function (band) {
    var k = band.querySelectorAll('.zw11-k'), x = new Date(nacht), n = 0;
    if (!offenJetzt && !heuteSpaeter) x.setDate(x.getDate() + 1);
    while (n < k.length) {
      var key = KEY[x.getDay()];
      if (BIS[key]) {
        k[n].querySelector('[data-k-tag]').textContent = (n === 0 && key === heute) ? 'Heute, ' + NAME[key] : NAME[key];
        k[n].querySelector('[data-k-dat]').textContent = x.getDate() + '. ' + MON[x.getMonth()] + ' · 19 bis ' + BIS[key] + ' Uhr';
        k[n].classList.toggle('heute', n === 0 && key === heute); n++;
      }
      x.setDate(x.getDate() + 1);
    }
    var balken = band.parentNode.querySelector('[data-balken]');
    function stand() { var max = band.scrollWidth - band.clientWidth; var q = max > 0 ? band.scrollLeft / max : 1; balken.style.transform = 'scaleX(' + (0.3 + q * 0.7).toFixed(3) + ')'; }
    band.addEventListener('scroll', stand, { passive: true }); stand();
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-zw11]'); if (!b) return;
    var band = b.closest('.zw11').querySelector('.zw11-band'), k = band.querySelector('.zw11-k');
    band.scrollBy({ left: +b.dataset.zw11 * (k.offsetWidth + 4), behavior: 'smooth' });
  });
})();
