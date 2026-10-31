/* Culinarium · Hero «Das Team» wählen (nur Wahlseite): Gruppenbild umschalten (?bild=Nummer), gilt für alle Fassungen des Schriftzugs */
(function () {
  var B = window.TEAMBILD, kopf = document.getElementById('kopf');
  var knoepfe = document.querySelector('[data-tm-bilder]');
  var n = +(new URLSearchParams(location.search).get('bild'));
  if (!(n >= 0 && n < B.length)) n = 2;
  function zeige(i) {
    n = i; var b = B[i];
    kopf.querySelectorAll('.tm-i, .tm-heute .foto img').forEach(function (img) {
      img.removeAttribute('data-srcset');
      img.srcset = b.srcset; img.src = b.src; img.alt = b.alt; img.style.objectPosition = b.pos;
    });
    [].forEach.call(knoepfe.children, function (c) { c.classList.toggle('an', +c.dataset.b === i); });
    var u = new URL(location.href); u.searchParams.set('bild', i); history.replaceState(null, '', u);
  }
  knoepfe.addEventListener('click', function (e) { var c = e.target.closest('button'); if (c) zeige(+c.dataset.b); });
  addEventListener('keydown', function (e) {
    if (e.target.closest('input,textarea')) return;
    var t = +e.key; if (t >= 1 && t <= B.length) zeige(t - 1);   /* Zifferntasten wählen das Bild */
  });
  zeige(n);
})();
