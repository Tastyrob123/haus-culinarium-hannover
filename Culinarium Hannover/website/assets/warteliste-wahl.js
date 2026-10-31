/* Culinarium · Warteliste in 15 Fassungen (nur Wahlseite). Jede Fassung hat ihr eigenes Formular, alles darin schreibt mit; verschickt wird nichts.
   Nur Klassen und transform, nativer Scroll. */
(function () {
  'use strict';
  var TAGE = { fr: ['Freitag', 'ab 19:00'], sa: ['Samstag', 'ab 17:00'], egal: ['Freitag oder Samstag', 'beides geht'] };
  var REIHE = ['fr', 'sa', 'egal'];
  function anzahl(n) { return n + (n === 1 ? ' Person' : ' Personen'); }
  function rein(s) { return s.replace(/[<>&"]/g, ''); }

  document.querySelectorAll('.ww form[data-ww]').forEach(function (f) {
    var box = f.closest('.wv'), st = { tag: 'fr', n: 2 };
    var fName = f.elements.namedItem('name'), fMail = f.elements.namedItem('mail');
    function setze(k, w) { box.querySelectorAll('[data-feld="' + k + '"]').forEach(function (e) { e.textContent = w; }); }
    function name() { return fName && fName.value.trim(); }
    function male(neu) {
      var t = TAGE[st.tag];
      setze('name', name() || 'Dein Name'); setze('n', st.n); setze('anzahl', anzahl(st.n)); setze('tag', t[0]); setze('zeit', t[1]);
      box.dataset.tag = st.tag; box.style.setProperty('--n', st.n);
      box.querySelectorAll('[data-platz]').forEach(function (e) {
        var p = +e.dataset.platz; e.classList.toggle('an', e.hasAttribute('data-genau') ? p === st.n : p <= st.n);
      });
      box.querySelectorAll('input[name=tag]').forEach(function (r) { r.checked = r.value === st.tag; });
      if (neu) box.querySelectorAll('[data-neu]').forEach(function (e) { e.classList.remove('neu'); void e.offsetWidth; e.classList.add('neu'); });
    }
    /* Abreisskalender: das alte Blatt geht nach oben weg */
    function tag(k) {
      if (k === st.tag) return;
      var alt = box.querySelector('[data-blatt="' + st.tag + '"]');
      if (alt) { box.querySelectorAll('[data-blatt]').forEach(function (e) { e.classList.remove('weg'); }); void alt.offsetWidth; alt.classList.add('weg'); setTimeout(function () { alt.classList.remove('weg'); }, 900); }
      st.tag = k; male(true);
    }
    box.addEventListener('click', function (e) {
      var s = e.target.closest('[data-schritt]');
      if (s) { st.n = Math.max(1, Math.min(6, st.n + +s.dataset.schritt)); male(true); return; }
      var p = e.target.closest('[data-platz]');
      if (p) { if (+p.dataset.platz <= 6) { st.n = +p.dataset.platz; male(true); } return; }
      var r = e.target.closest('[data-reihum]');
      if (r) { if (r.dataset.reihum === 'tag') tag(REIHE[(REIHE.indexOf(st.tag) + 1) % 3]); else { st.n = st.n % 6 + 1; male(true); } }
    });
    box.addEventListener('change', function (e) { if (e.target.name === 'tag') tag(e.target.value); });
    f.addEventListener('input', function (e) { if (e.target.name === 'name') male(false); });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      [fName, fMail].forEach(function (i) { var g = i.checkValidity() && i.value.trim(); i.setAttribute('aria-invalid', g ? 'false' : 'true'); if (!g) ok = false; });
      var m = box.querySelector('[data-meldung]');
      if (!ok) { box.classList.remove('fertig'); m.innerHTML = 'Bitte Name und E-Mail eintragen.'; return; }
      m.innerHTML = 'Danke, ' + rein(name()) + '. Du stehst auf der Liste: ' + TAGE[st.tag][0] + ', ' + anzahl(st.n) + '.<small>Diese Vorschau verschickt noch nichts.</small>';
      box.classList.add('fertig');
    });
    male(false);
  });

  /* beim Öffnen gleich zur Warteliste */
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function hin() { var s = document.getElementById('warteliste'); if (s) scrollTo(0, s.getBoundingClientRect().top + scrollY - 70); }
  addEventListener('load', function () { setTimeout(hin, 120); setTimeout(hin, 900); });
})();
