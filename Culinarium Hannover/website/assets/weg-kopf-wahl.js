/* Culinarium · Hero von «Der Weg» in 15 Fassungen (nur Wahlseite): Scroll-Züge, Naht Tag und Nacht, Taschenlampe; nur transform und opacity. */
(function () {
  var ruhig = document.documentElement.classList.contains('ruhig');
  var kopf = document.getElementById('kopf');
  function sichtbar(el) { var v = el.closest('.wv'); if (v.hidden) return false; var r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }

  /* 3 Tag und Nacht: Naht ziehen (geht auch bei «ruhig», es ist eine Bedienung) */
  var f3 = kopf.querySelector('[data-naht]');
  if (f3) {
    var nacht = f3.querySelector('.wh03-nacht'), innen = f3.querySelector('.wh03-innen'), naht = f3.querySelector('.wh03-naht'), zieht = false;
    var setze = function (x) {
      var w = f3.clientWidth || innerWidth; x = Math.max(0, Math.min(w, x));
      nacht.style.transform = 'translate3d(' + x + 'px,0,0)'; innen.style.transform = 'translate3d(' + -x + 'px,0,0)'; naht.style.transform = 'translate3d(' + x + 'px,0,0)';
    };
    var von = function (e) { return e.clientX - f3.getBoundingClientRect().left; };
    f3.addEventListener('pointerdown', function (e) { if (e.target.closest('a')) return; zieht = true; setze(von(e)); });
    f3.addEventListener('pointermove', function (e) { if (zieht || e.pointerType === 'mouse' && e.buttons) setze(von(e)); });
    addEventListener('pointerup', function () { zieht = false; });
    addEventListener('pointercancel', function () { zieht = false; });
    addEventListener('resize', function () { nacht.style.transform = innen.style.transform = naht.style.transform = ''; });   // zurück zur Mitte aus dem CSS
  }

  /* Beim Aufruf mit ?kopf=Nummer sieht der Beobachter die zuerst versteckte Fassung nicht: ihre Auftritte hier anstossen */
  function wecke() { var f = kopf.querySelector('.whv:not([hidden])'); if (f) setTimeout(function () { f.querySelectorAll('.auf:not(.da)').forEach(function (x) { x.classList.add('da'); }); f.firstElementChild.classList.add('an'); }, 80); }
  wecke(); document.addEventListener('click', wecke); addEventListener('keydown', wecke);

  /* 25 Jetzt offen: Zeiten der Bar (fakten.json) gegen die Uhr in Hannover; Feiertage und Sonderschliessungen kennt sie nicht */
  var offen = kopf.querySelector('[data-offen]');
  if (offen) {
    var TAGE = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
    var AUF = { 4: [19, 25], 5: [19, 26], 6: [19, 26] };   // Wochentag: [ab, bis] in Stunden, über Mitternacht weitergezählt
    var jetzt = function () {
      var t = {}; new Intl.DateTimeFormat('de-DE', { timeZone: 'Europe/Berlin', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' })
        .formatToParts(new Date()).forEach(function (p) { t[p.type] = p.value; });
      var wt = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'].indexOf(t.weekday.replace('.', ''));
      return { tag: wt, h: +t.hour + t.minute / 60 };
    };
    var status = function () {
      var n = jetzt(), gestern = (n.tag + 6) % 7, a;
      if ((a = AUF[gestern]) && n.h + 24 < a[1]) return 'Jetzt offen, bis ' + (a[1] - 24) + ' Uhr.';
      if ((a = AUF[n.tag]) && n.h >= a[0]) return 'Jetzt offen, bis ' + (a[1] - 24) + ' Uhr.';
      if ((a = AUF[n.tag])) return 'Heute ab ' + a[0] + ' Uhr offen.';
      for (var d = 1; d < 7; d++) { var w = (n.tag + d) % 7; if (AUF[w]) return (d === 1 ? 'Morgen' : TAGE[w]) + ' ab ' + AUF[w][0] + ' Uhr wieder offen.'; }
    };
    offen.textContent = status();
  }

  /* 26 Der Rundgang: mit der Maus ziehen (Finger und Trackpad scrollen von selbst) */
  var zug = kopf.querySelector('.wh26-zug');
  if (zug) {
    var x0 = 0, s0 = 0, an = false;
    zug.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse' || e.target.closest('a')) return; an = true; x0 = e.clientX; s0 = zug.scrollLeft; zug.classList.add('zieht'); });
    addEventListener('pointermove', function (e) { if (an) zug.scrollLeft = s0 - (e.clientX - x0); });
    addEventListener('pointerup', function () { if (!an) return; an = false; zug.classList.remove('zieht'); });
  }

  if (ruhig) return;

  /* 15 Taschenlampe: folgt Maus oder Finger; ohne Zeiger wandert sie langsam um das Schild */
  var f15 = kopf.querySelector('[data-lampe]');
  if (f15) {
    var dunkel = f15.querySelector('.wh15-dunkel'), zuletzt = 0, t0 = performance.now();
    var lampe = function (x, y) { dunkel.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)'; };
    f15.addEventListener('pointermove', function (e) { var r = f15.getBoundingClientRect(); zuletzt = performance.now(); lampe(e.clientX - r.left, e.clientY - r.top); });
    (function wandern(t) {
      if (t - zuletzt > 2500 && sichtbar(f15)) {
        var w = f15.clientWidth, h = f15.clientHeight, s = (t - t0) / 1000;
        lampe(w * (.5 + .16 * Math.sin(s * .45)), h * (.48 + .12 * Math.sin(s * .7 + 1)));
      }
      requestAnimationFrame(wandern);
    })(t0);
  }

  var tick = false;
  function rechnen() {
    tick = false;
    var f = kopf.querySelector('.whv:not([hidden])'); if (!f) return;
    var r = f.getBoundingClientRect(), h = innerHeight;
    if (r.bottom < 0 || r.top > h) return;
    var s = Math.max(0, -r.top), p = Math.min(1, s / (h * .85));
    f.querySelectorAll('[data-zieh]').forEach(function (el) {
      var art = el.dataset.zieh;
      if (art === 'nah') el.style.transform = 'scale(' + (1 + p * .9) + ')';
      else if (art === 'tiefe') el.style.transform = 'translate3d(0,' + (-s * .22) + 'px,0)';
      else if (art === 'spion') el.style.transform = 'scale(' + (1 + p * 1.4) + ')';
    });
  }
  function anstoss() { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', anstoss, { passive: true });
  addEventListener('resize', anstoss);
  document.addEventListener('click', function () { setTimeout(anstoss, 30); });
  addEventListener('keydown', function () { setTimeout(anstoss, 30); });
  anstoss();
})();
