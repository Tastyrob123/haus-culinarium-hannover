/* Culinarium · 15 Footer zur Wahl: Umschalter unten, Pfeiltasten, ?f=Nummer; dazu die Momente, die Rechnen brauchen.
   Nur transform und opacity, nativer Scroll; gerechnet wird nur für den sichtbaren Footer. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  var F = [].slice.call(document.querySelectorAll('footer.ff'));
  var fz = document.getElementById('fuss-fassungen');
  if (!F.length || !fz) return;
  function klemme(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function laden(f) { f.querySelectorAll('img[data-srcset]').forEach(function (i) { i.srcset = i.dataset.srcset; i.removeAttribute('data-srcset'); }); }
  function sicht(cls) { var f = document.querySelector('footer.' + cls); return f && !f.hidden ? f : null; }

  /* ---------- Umschalter */
  var liste = JSON.parse(fz.dataset.liste), name = fz.querySelector('.fz-name'), jetzt = 1, SPEICHER = fz.dataset.speicher || 'culinarium-fuss';
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) e.target.classList.add('offen'); });
  }, { threshold: .22 }) : null;
  /* Rückfall ohne Beobachter-Takt: sobald der Footer zu einem Fünftel im Bild ist, geht er auf */
  function pruefe() { var f = F[jetzt - 1]; if (f && !f.classList.contains('offen') && f.getBoundingClientRect().top < innerHeight * .8) f.classList.add('offen'); }
  addEventListener('scroll', pruefe, { passive: true });
  function hin(f) {
    if (f.classList.contains('fx-vorhang')) { scrollTo(0, document.documentElement.scrollHeight); return; }
    scrollTo(0, f.getBoundingClientRect().top + scrollY - Math.round(innerHeight * .18));
  }
  function zeige(n, ersteMal) {
    n = ((n - 1 + liste.length) % liste.length) + 1;
    jetzt = n;
    F.forEach(function (f) { var an = +f.dataset.nr === n; f.hidden = !an; if (!an) f.classList.remove('offen'); });
    var f = F[n - 1];
    document.documentElement.classList.toggle('vorhang', f.classList.contains('fx-vorhang'));
    name.innerHTML = '<b>' + n + '</b> · ' + liste[n - 1][1];
    laden(f);
    if (io) { io.unobserve(f); setTimeout(function () { io.observe(f); }, 60); } else f.classList.add('offen');
    if (!ersteMal) history.replaceState(null, '', '?f=' + n);
    try { localStorage.setItem(SPEICHER, n); } catch (e) {}
    hin(f);
    setTimeout(pruefe, 400);
    scroll();
  }
  fz.querySelector('.fz-zurueck').addEventListener('click', function () { zeige(jetzt - 1); });
  fz.querySelector('.fz-vor').addEventListener('click', function () { zeige(jetzt + 1); });
  addEventListener('keydown', function (e) {
    if (e.target.closest('input,textarea,select')) return;
    if (e.key === 'ArrowRight') zeige(jetzt + 1);
    else if (e.key === 'ArrowLeft') zeige(jetzt - 1);
  });

  /* ---------- 1 Letzter Gang: die Wortmarke steigt aus der Unterkante, je näher das Ende der Seite */
  function gang() {
    var f = sicht('fx-gang'); if (!f) return;
    var r = f.getBoundingClientRect(), p = klemme((innerHeight - r.top) / r.height, 0, 1);
    var e = 1 - Math.pow(1 - p, 2);
    f.querySelector('.fg-wort').style.setProperty('--hoch', (32 * (1 - e)).toFixed(2) + '%');
  }
  /* ---------- 9 Das Loch in der Wand: das Bild im Loch zieht langsamer als die Seite */
  function loch() {
    var f = sicht('fx-loch'); if (!f) return;
    var h = f.querySelector('.fh-loch'), r = h.getBoundingClientRect();
    var p = klemme((r.top + r.height / 2) / innerHeight, -.2, 1.2) - .5;
    f.querySelector('.fh-tiefe').style.setProperty('--tief', (p * r.height * .22).toFixed(1) + 'px');
  }
  var lt = false;
  function scroll() { if (lt || ruhig) return; lt = true; requestAnimationFrame(function () { lt = false; gang(); loch(); }); }
  addEventListener('scroll', scroll, { passive: true });
  addEventListener('resize', scroll, { passive: true });

  /* ---------- 7 Wann wieder?: Zeigen tauscht das Bild im selben Rahmen */
  var fw = document.querySelector('.fx-wann');
  if (fw) {
    var li = [].slice.call(fw.querySelectorAll('.fw-liste li')), bi = [].slice.call(fw.querySelectorAll('.fw-bild .fb')), an = 0;
    li.forEach(function (l, i) {
      l.addEventListener('pointerenter', function () {
        if (i === an) return;
        bi.forEach(function (b) { b.classList.remove('war'); });
        bi[an].classList.add('war'); li[an].classList.remove('an'); bi[an].classList.remove('an');
        an = i; li[i].classList.add('an'); bi[i].classList.add('an');
      });
    });
  }

  /* ---------- 10 Die Karte: der Strich in Kerze folgt der Zeile */
  var fk = document.querySelector('.fk-zeilen');
  if (fk) {
    var st = fk.querySelector('.fk-strich'), zl = [].slice.call(fk.querySelectorAll('li'));
    function setze(l) { st.style.setProperty('--h', l.offsetHeight + 'px'); st.style.setProperty('--y', l.offsetTop + 'px'); }
    zl.forEach(function (l) { l.addEventListener('pointerenter', function () { setze(l); }); l.addEventListener('focusin', function () { setze(l); }); });
    new MutationObserver(function () { if (!fk.closest('footer').hidden) setTimeout(function () { setze(zl[0]); }, 50); }).observe(fk.closest('footer'), { attributes: true, attributeFilter: ['hidden'] });
  }

  /* ---------- 11 Offen?: welcher Tag heute ist und ob die Bar gerade offen hat (Do 19–1, Fr + Sa 19–2) */
  var fq = document.querySelector('.fx-offen');
  if (fq) {
    var TAG = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
    var d = new Date(), wt = d.getDay(), h = d.getHours() + d.getMinutes() / 60;
    var heute = (wt + 6) % 7;   // 0 = Montag
    var satz;
    var ende = { 4: 1, 5: 2, 6: 2 };   // Wochentag des Abends → Schluss in der Nacht
    var gestern = (wt + 6) % 7;
    if (ende[gestern] && h < ende[gestern]) satz = 'Jetzt gerade <em>offen</em>, noch bis ' + ende[gestern] + ' Uhr.';
    else if (ende[wt] && h >= 19) satz = 'Jetzt gerade <em>offen</em>, heute bis ' + ende[wt] + ' Uhr.';
    else if (ende[wt]) satz = 'Heute ab <em>19 Uhr</em> offen. ' + TAG[wt] + ' bis ' + ende[wt] + ' Uhr.';
    else satz = 'Heute ist ' + TAG[wt] + '. Wieder offen am <em>Donnerstag</em> ab 19 Uhr.';
    fq.querySelector('[data-status]').innerHTML = satz;
    var t = fq.querySelector('.fq-tag[data-tag="' + heute + '"]'); if (t) t.classList.add('heute');
  }

  var start = parseInt(new URLSearchParams(location.search).get('f'), 10);
  if (!start) { try { start = parseInt(localStorage.getItem(SPEICHER), 10); } catch (e) {} }
  addEventListener('load', function () { zeige(start >= 1 && start <= liste.length ? start : 1, true); });
})();
