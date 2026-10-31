/* Auswahl-Seite: jeder Abschnitt an seinem Platz umschaltbar, Stand in der Adresse */
(function () {
  var W = window.WAHL, NAMEN = W.namen, IDS = W.ids;
  var q = new URLSearchParams(location.search), stand = {}, akt = IDS[0], blocks = {};
  IDS.forEach(function (k) { var v = q.get(k); stand[k] = v === null ? 0 : (+v || 0); blocks[k] = document.getElementById(k); });
  function zeige(k, n, springen) {
    var b = blocks[k]; n = (n + NAMEN.length) % NAMEN.length; stand[k] = n;
    var neu = null;
    [].forEach.call(b.querySelectorAll(':scope>.wv'), function (v) { var an = +v.dataset.n === n; if (an && v.hidden) neu = v; v.hidden = !an; });
    b.querySelector('[data-nr]').textContent = 'Fassung ' + n + ' · ' + NAMEN[n];
    var u = new URL(location.href); IDS.forEach(function (x) { u.searchParams.set(x, stand[x]); }); history.replaceState(null, '', u);
    if (neu && window.culinariumNeu) window.culinariumNeu(neu);
    if (springen) { var y = b.getBoundingClientRect().top + scrollY - 70; scrollTo(0, y); }
    leiste();
  }
  function leiste() {
    var n = stand[akt];
    document.querySelector('[data-wl-ab]').textContent = blocks[akt].dataset.name;
    document.querySelector('[data-wl-nr]').textContent = n + ' / ' + (NAMEN.length - 1);
    document.querySelector('[data-wl-name]').textContent = NAMEN[n];
    document.querySelector('[data-wl-wahl]').innerHTML = IDS.map(function (k) { return '<a href="#' + k + '" data-k="' + k + '"' + (k === akt ? ' class="an"' : '') + '>' + blocks[k].dataset.name + ' <b>' + stand[k] + '</b></a>'; }).join('');
    var d = document.querySelector('[data-wl-daumen]');
    if (d.dataset.ab !== akt) {
      d.dataset.ab = akt;
      d.innerHTML = NAMEN.map(function (x, i) { return '<button type="button" data-i="' + i + '">' + (W.daumen ? '<img src="assets/daumen/' + akt + '-' + i + '.jpg" alt="" loading="lazy">' : '') + '<span><i>' + i + '</i>' + x + '</span></button>'; }).join('');
    }
    [].forEach.call(d.children, function (c) { c.classList.toggle('an', +c.dataset.i === n); });
    var an = d.querySelector('.an'); if (an) d.scrollTo({ left: an.offsetLeft - d.clientWidth / 2 + an.clientWidth / 2, behavior: 'smooth' });
  }
  document.querySelector('[data-wl-daumen]').addEventListener('click', function (e) { var c = e.target.closest('button'); if (c) zeige(akt, +c.dataset.i, true); });
  document.querySelector('[data-wl-zur]').addEventListener('click', function () { zeige(akt, stand[akt] - 1, true); });
  document.querySelector('[data-wl-vor]').addEventListener('click', function () { zeige(akt, stand[akt] + 1, true); });
  document.querySelector('[data-wl-wahl]').addEventListener('click', function (e) { var a = e.target.closest('a'); if (!a) return; e.preventDefault(); akt = a.dataset.k; scrollTo(0, blocks[akt].getBoundingClientRect().top + scrollY - 70); leiste(); });
  addEventListener('keydown', function (e) { if (e.target.closest('input,textarea')) return; if (e.key === 'ArrowRight') zeige(akt, stand[akt] + 1, true); if (e.key === 'ArrowLeft') zeige(akt, stand[akt] - 1, true); });
  function welcher() { var m = innerHeight * .45, best = IDS[0]; IDS.forEach(function (k) { if (blocks[k].getBoundingClientRect().top < m) best = k; }); if (best !== akt) { akt = best; leiste(); } }
  addEventListener('scroll', welcher, { passive: true });
  /* Band: Pfeile blättern um eine Bildbreite */
  document.addEventListener('click', function (e) { var b = e.target.closest('[data-band]'); if (!b) return; var band = b.closest('.vi').querySelector('.vband'); band.scrollBy({ left: +b.dataset.band * band.clientWidth * .7, behavior: 'smooth' }); });
  IDS.forEach(function (k) { zeige(k, stand[k], false); }); welcher(); leiste();
})();
