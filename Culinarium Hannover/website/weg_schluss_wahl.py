#!/usr/bin/env python3
"""Culinarium Hannover · Bildwahl für den Schluss «Bis zum nächsten Abend.» auf weg.html, 27.10.2026.
Robert: «10 verschiedene Bilder, die man da im Hintergrund einsetzen kann, statt dem aktuellen».
Abendbilder rund um die Tafel, warm und dunkel genug für die Schrift; keins, das weiter oben auf weg.html steht. Bild 1 ist der heutige Stand (barlicht).
Baut weg-schluss-wahl.html aus weg.html: Leiste unten, Pfeiltasten ← →, ?ws=Nummer.
Aufruf: python3 website/weg_schluss_wahl.py"""
import json, os

HIER = os.path.dirname(os.path.abspath(__file__))
META = json.load(open(os.path.join(HIER, 'assets/bild/meta.json')))
VERSION = '26147'

# Bild, Ausschnitt, Beschreibung, wo es sonst auf der Website steht
B = [
    ('barlicht', '50% 50%', 'Heute: die Bar bei Nacht von draussen', 'nur hier'),
    ('tafelleer', '50% 50%', 'Die gedeckte Tafel, die Plätze warten noch', 'Bar, Abende'),
    ('t01', '50% 42%', 'Anstossen bei Kerzenlicht', 'Startseite'),
    ('anstossen', '50% 40%', 'Anstossen mit dem Aperitif', 'Startseite, Abend'),
    ('t03', '50% 58%', 'Kerze, Flasche, die Tafel im Dunkeln', 'nirgends'),
    ('loch', '50% 60%', 'Kerzen und Trockenblumen an der warmen Wand', 'Startseite, Abend'),
    ('kerze2', '50% 45%', 'Kerzen vorn, Service dahinter', 'Startseite'),
    ('t09', '50% 50%', 'Der Raum mit der Tafel, Gastgeber am Tisch', 'Startseite, Abend'),
    ('t02', '50% 45%', 'Applaus an der Tafel', 'Startseite'),
    ('kartglas', '50% 50%', 'Menükarte und Gläser am Platz', 'Startseite, Abend'),
    ('t08', '50% 50%', 'Die Tafel vor der Negroni-Bar', 'Startseite, Abend, Abende'),
]


def srcset(b):
    return ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (b, s, VERSION, s) for s in META[b]['stufen'])


L = [[b, srcset(b), pos, txt, wo, max(META[b]['stufen']), META[b]['lq']] for b, pos, txt, wo in B]

LEISTE = r'''<script type="application/json" id="ws-wahl">%s</script>
<script>
/* Bildwahl im Schluss «Bis zum nächsten Abend.» (?ws=N): ← → oder Klick wechseln */
(function () {
  var L = JSON.parse(document.getElementById('ws-wahl').textContent), f = document.querySelector('.v-schluss'), fig = f.querySelector('.fenster-schicht figure'), img = fig.querySelector('img');
  var n = parseInt(new URLSearchParams(location.search).get('ws'), 10); if (!(n >= 1 && n <= L.length)) n = 1;
  var t = document.createElement('div');
  t.style.cssText = 'position:fixed;left:50%%;bottom:18px;transform:translateX(-50%%);z-index:300;background:#16151A;color:#FAF4F4;border:1px solid rgba(239,118,73,.6);border-radius:999px;padding:8px 10px;font:500 13px/1 Urbanist,sans-serif;letter-spacing:.06em;display:flex;gap:14px;align-items:center;white-space:nowrap;max-width:calc(100vw - 24px);overflow:hidden';
  var k = 'background:none;border:0;color:#F5A689;font:400 22px/1 Urbanist,sans-serif;cursor:pointer;padding:2px 10px';
  t.innerHTML = '<button type="button" style="' + k + '" data-s="-1" aria-label="Voriges Bild">‹</button><span data-i style="overflow:hidden;text-overflow:ellipsis"></span><button type="button" style="' + k + '" data-s="1" aria-label="Nächstes Bild">›</button>';
  document.body.appendChild(t);
  function zeig(i) {
    n = (i + L.length - 1) %% L.length + 1; var e = L[n - 1];
    fig.style.setProperty('--lq', 'url(' + e[6] + ')');
    img.removeAttribute('data-srcset'); img.srcset = e[1]; img.sizes = '100vw'; img.style.objectPosition = e[2];
    t.querySelector('[data-i]').innerHTML = '<span style="color:#F5A689">Bild ' + n + ' / ' + L.length + '</span>&nbsp;&nbsp;' + e[3] + '&nbsp;&nbsp;<span style="opacity:.55">' + e[0] + ' · sonst ' + e[4] + (e[5] < 1600 ? ' · max ' + e[5] + ' px' : '') + '</span>';
    history.replaceState(null, '', '?ws=' + n);
  }
  t.addEventListener('click', function (e) { var b = e.target.closest('[data-s]'); if (b) zeig(n + +b.dataset.s); });
  addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); zeig(n + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); zeig(n - 1); } });
  zeig(n);
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function hin() { f.scrollIntoView({ block: 'center' }); }
  addEventListener('load', function () { setTimeout(hin, 150); setTimeout(hin, 900); });
})();
</script>
''' % json.dumps(L, ensure_ascii=False)

h = open(os.path.join(HIER, 'weg.html'), encoding='utf-8').read()
h = h.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
h = h.replace('</body>', LEISTE + '</body>', 1)
open(os.path.join(HIER, 'weg-schluss-wahl.html'), 'w', encoding='utf-8').write(h)
print('weg-schluss-wahl.html: %d Bilder' % len(L))
