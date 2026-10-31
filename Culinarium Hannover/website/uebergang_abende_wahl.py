#!/usr/bin/env python3
"""Culinarium Hannover · Übergang zwischen Kopf («Geteilt») und Fenster («Jeder Abend hatte sein Plakat.») auf abende.html, 27.10.2026.
Robert: «zwischen dem Hero und dem ersten Fenster irgendwie noch was überlegen? der übergang ist sonst zu hart».
Fassungen als Klasse am body (ue-1 … ue-8), nur Verläufe, Linien und Lagen; Bewegung nur transform und opacity.
Baut abende-uebergang-wahl.html aus abende.html: Leiste unten, Pfeiltasten ← →, ?ue=Nummer; 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/uebergang_abende_wahl.py"""
import json, os

HIER = os.path.dirname(os.path.abspath(__file__))

N = [
    'Heute: harte Kante',
    'Verlauf: der Kopf läuft in die Nacht aus, das Fenster kommt aus ihr',
    'Nachtband: dazwischen ein schmales Band Nacht mit einer Zeile',
    'Kerzenfaden: eine feine Linie in Kerze führt vom Titel ins Fenster',
    'Darübergeschoben: das Fenster schiebt sich mit runden Ecken über den Kopf',
    'Lichtkante: an der Naht ein warmer Lichtstreif, beide Seiten verlaufen',
    'Abdunkeln: beim Scrollen wird der Kopf dunkel, bevor das Fenster kommt',
    'Der Bogen: das Fenster öffnet sich oben als flacher Bogen',
    'Verlauf und Abdunkeln zusammen',
]

CSS = '''
/* Übergang Kopf → Fenster (nur Wahlseite) */
.kopf-geteilt::after,.kopf-geteilt::before,#fenster-abende::before,#fenster-abende::after{content:none;position:absolute;left:0;right:0;pointer-events:none}
.ue-band{display:none}
/* Verlauf: unten am Kopf und oben am Fenster dieselbe Nacht */
body:is(.ue-1,.ue-2,.ue-3,.ue-5,.ue-8) .kopf-geteilt::after{content:"";bottom:0;height:34%;z-index:1;background:linear-gradient(to bottom,rgba(15,14,19,0),#0F0E13 92%)}
body:is(.ue-1,.ue-2,.ue-3,.ue-5,.ue-6,.ue-8) #fenster-abende::before{content:"";top:0;height:36%;z-index:1;background:linear-gradient(to bottom,#0F0E13,rgba(15,14,19,0))}
/* Nachtband */
body.ue-2 .ue-band{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;height:30vh;min-height:200px;background:#0F0E13;color:rgba(250,244,244,.7);margin:0}
.ue-band p{font:400 12px/1 var(--mono);letter-spacing:.28em;text-transform:uppercase}
.ue-band .ue-linie{width:1px;height:64px;background:linear-gradient(var(--kerze),rgba(239,118,73,0));transform-origin:50% 0}
html.js:not(.ruhig) body.ue-2 .ue-band .ue-linie{transform:scaleY(.15);transition:transform 1.8s var(--k)}
html.js body.ue-2 .ue-band.da .ue-linie{transform:none}
/* Kerzenfaden: unten aus dem Kopf, oben ins Fenster */
body.ue-3 .kopf-geteilt::before{content:"";left:50%;right:auto;bottom:0;width:1px;height:20vh;z-index:2;background:linear-gradient(rgba(239,118,73,0),var(--kerze))}
body.ue-3 #fenster-abende::after{content:"";left:50%;right:auto;top:0;width:1px;height:22vh;z-index:2;background:linear-gradient(var(--kerze),rgba(239,118,73,0))}
/* Darübergeschoben */
body.ue-4 #fenster-abende{z-index:2;margin-top:-9vh;clip-path:inset(0 round 30px 30px 0 0);-webkit-clip-path:inset(0 round 30px 30px 0 0)}
body.ue-4 .kopf-geteilt{z-index:1}
body.ue-4 #fenster-abende::before{content:"";top:0;height:18%;z-index:1;background:linear-gradient(to bottom,rgba(15,14,19,.55),rgba(15,14,19,0))}
/* Lichtkante */
body.ue-5 #fenster-abende::after{content:"";top:0;height:1px;z-index:2;background:linear-gradient(to right,rgba(239,118,73,0),rgba(245,166,137,.9) 50%,rgba(239,118,73,0));box-shadow:0 0 28px 6px rgba(239,118,73,.28)}
/* Abdunkeln beim Scrollen (Deckkraft der Schicht folgt dem Scroll) */
.ue-dunkel{position:absolute;inset:0;z-index:1;background:#0F0E13;opacity:0;pointer-events:none;display:none}
body:is(.ue-6,.ue-8) .ue-dunkel{display:block}
/* Der Bogen */
body.ue-7 #fenster-abende{z-index:2;margin-top:-12vh;clip-path:inset(0 round 50% 50% 0 0 / 12vh 12vh 0 0);-webkit-clip-path:inset(0 round 50% 50% 0 0 / 12vh 12vh 0 0)}
body.ue-7 .kopf-geteilt{z-index:1}
@media (max-width:860px){body.ue-4 #fenster-abende{margin-top:-6svh}body.ue-7 #fenster-abende{margin-top:-7svh;clip-path:inset(0 round 50% 50% 0 0 / 7svh 7svh 0 0);-webkit-clip-path:inset(0 round 50% 50% 0 0 / 7svh 7svh 0 0)}}
'''

LEISTE = r'''<script>
/* Übergang wählen (?ue=N): ← → oder Klick wechseln */
(function () {
  var N = %s, b = document.body, kopf = document.querySelector('.kopf-geteilt'), dunkel = kopf.querySelector('.ue-dunkel'), f = document.getElementById('fenster-abende');
  var n = parseInt(new URLSearchParams(location.search).get('ue'), 10); if (!(n >= 0 && n < N.length)) n = 1;
  var t = document.createElement('div');
  t.style.cssText = 'position:fixed;left:50%%;bottom:18px;transform:translateX(-50%%);z-index:300;background:#16151A;color:#FAF4F4;border:1px solid rgba(239,118,73,.6);border-radius:999px;padding:8px 10px;font:500 13px/1 Urbanist,sans-serif;letter-spacing:.06em;display:flex;gap:14px;align-items:center;white-space:nowrap;max-width:calc(100vw - 24px);overflow:hidden';
  var k = 'background:none;border:0;color:#F5A689;font:400 22px/1 Urbanist,sans-serif;cursor:pointer;padding:2px 10px';
  t.innerHTML = '<button type="button" style="' + k + '" data-s="-1" aria-label="Voriger Übergang">‹</button><span data-i style="overflow:hidden;text-overflow:ellipsis"></span><button type="button" style="' + k + '" data-s="1" aria-label="Nächster Übergang">›</button>';
  b.appendChild(t);
  function zeig(i) {
    n = (i + N.length) %% N.length;
    for (var j = 1; j < N.length; j++) b.classList.toggle('ue-' + j, j === n);
    t.querySelector('[data-i]').innerHTML = '<span style="color:#F5A689">Übergang ' + n + ' / ' + (N.length - 1) + '</span>&nbsp;&nbsp;' + N[n];
    history.replaceState(null, '', '?ue=' + n); rechnen();
  }
  function rechnen() {
    var r = kopf.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / (r.height * .7)));
    dunkel.style.opacity = (p * .82).toFixed(3);
  }
  addEventListener('scroll', function () { requestAnimationFrame(rechnen); }, { passive: true });
  t.addEventListener('click', function (e) { var x = e.target.closest('[data-s]'); if (x) zeig(n + +x.dataset.s); });
  addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); zeig(n + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); zeig(n - 1); } });
  zeig(n);
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function hin() { scrollTo(0, f.getBoundingClientRect().top + scrollY - innerHeight * .5); }
  addEventListener('load', function () { setTimeout(hin, 150); setTimeout(hin, 900); });
})();
</script>
''' % json.dumps(N, ensure_ascii=False)

h = open(os.path.join(HIER, 'abende.html'), encoding='utf-8').read()
assert '<section class="kopf-geteilt"' in h and 'id="fenster-abende"' in h, 'Kopf oder Fenster fehlt in abende.html (erst bau.py laufen lassen)'
h = h.replace('<title>', '<title>Übergang wählen · ', 1)
h = h.replace('</head>', '<style>%s</style>\n</head>' % CSS, 1)
h = h.replace('<div class="kg-grund" aria-hidden="true"></div>', '<div class="kg-grund" aria-hidden="true"></div><div class="ue-dunkel" aria-hidden="true"></div>', 1)
h = h.replace('<section class="fenster" id="fenster-abende"', '<section class="ue-band auf" aria-hidden="true"><span class="ue-linie"></span><p>Linden · seit Mai 2023</p></section>\n<section class="fenster" id="fenster-abende"', 1)
h = h.replace('</body>', LEISTE + '</body>', 1)
open(os.path.join(HIER, 'abende-uebergang-wahl.html'), 'w', encoding='utf-8').write(h)
print('abende-uebergang-wahl.html: %d Übergänge + heute' % (len(N) - 1))
