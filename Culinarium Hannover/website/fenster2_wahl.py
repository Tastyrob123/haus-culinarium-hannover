#!/usr/bin/env python3
"""Culinarium Hannover · Bildwahl für das Fenster «Bis zum nächsten Abend an der Tafel.» (zwischen Warteliste und Fuss) auf abend.html, 27.10.2026.
Robert: «10 verschiedene Variationen … was man da als Hintergrundbild alternativ noch nehmen kann, was besser in den Kontext passt».
Abendbilder rund um die Tafel (Kerzen, Anstossen, Service, das Schild in der Nacht), kein Tageslicht. Bild 1 ist der heutige Stand (g2).
Baut fenster2-wahl.html aus abend.html: Leiste unten, Pfeiltasten ← →, ?fw2=Nummer.
Aufruf: python3 website/fenster2_wahl.py"""
import json, os

HIER = os.path.dirname(os.path.abspath(__file__))
META = json.load(open(os.path.join(HIER, 'assets/bild/meta.json')))
VERSION = '26131'

# Bild, Ausschnitt, Beschreibung, wie oft heute auf der Website
B = [
    ('g2', '50% 55%', 'Heute: Drink mit Kräutern', 'nur hier'),
    ('t01', '50% 42%', 'An der Tafel wird angestossen, Kerzen', 'Startseite'),
    ('t02', '50% 45%', 'Applaus an der Tafel', 'Startseite'),
    ('t03', '50% 58%', 'Kerze, Flasche, gedeckte Tafel', 'nirgends'),
    ('t04', '50% 50%', 'Kerze und Glas am Platz', 'nirgends'),
    ('t07', '50% 62%', 'Die Tafel im Raum unter den Lampen', 'nirgends'),
    ('t06', '50% 45%', 'Der Raum, Service an der Tafel', 'nirgends'),
    ('t12', '50% 45%', 'Am Tisch wird der Gang serviert', 'nirgends'),
    ('t11', '50% 42%', 'Service mit Tablett im Dunkeln', 'nirgends'),
    ('kerze2', '50% 45%', 'Kerzen vorn, die Tafel dahinter', 'Startseite'),
    ('schildnacht', '50% 38%', 'Das Schild in der Nacht', 'Startseite'),
]


def srcset(b):
    return ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (b, s, VERSION, s) for s in META[b]['stufen'])


L = [[b, srcset(b), pos, txt, wie, max(META[b]['stufen'])] for b, pos, txt, wie in B]

LEISTE = r'''<script type="application/json" id="fw2-wahl">%s</script>
<script>
/* Bildwahl im Fenster «Bis zum nächsten Abend an der Tafel.» (?fw2=N): ← → oder Klick wechseln */
(function () {
  var L = JSON.parse(document.getElementById('fw2-wahl').textContent), f = document.getElementById('fenster2'), img = f.querySelector('.fenster-schicht img');
  var n = parseInt(new URLSearchParams(location.search).get('fw2'), 10); if (!(n >= 1 && n <= L.length)) n = 1;
  var t = document.createElement('div');
  t.style.cssText = 'position:fixed;left:50%%;bottom:18px;transform:translateX(-50%%);z-index:300;background:#16151A;color:#FAF4F4;border:1px solid rgba(239,118,73,.6);border-radius:999px;padding:8px 10px;font:500 13px/1 Urbanist,sans-serif;letter-spacing:.06em;display:flex;gap:14px;align-items:center;white-space:nowrap;max-width:calc(100vw - 24px)';
  var k = 'background:none;border:0;color:#F5A689;font:400 22px/1 Urbanist,sans-serif;cursor:pointer;padding:2px 10px';
  t.innerHTML = '<button type="button" style="' + k + '" data-s="-1" aria-label="Voriges Bild">‹</button><span data-i></span><button type="button" style="' + k + '" data-s="1" aria-label="Nächstes Bild">›</button>';
  document.body.appendChild(t);
  function zeig(i) {
    n = (i + L.length - 1) %% L.length + 1; var e = L[n - 1];
    img.removeAttribute('data-srcset'); img.srcset = e[1]; img.sizes = '100vw'; img.style.objectPosition = e[2];
    t.querySelector('[data-i]').innerHTML = '<span style="color:#F5A689">Bild ' + n + ' / ' + L.length + '</span>&nbsp;&nbsp;' + e[3] + '&nbsp;&nbsp;<span style="opacity:.55">' + e[0] + ' · sonst ' + e[4] + (e[5] < 1600 ? ' · max ' + e[5] + ' px' : '') + '</span>';
    history.replaceState(null, '', '?fw2=' + n);
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

h = open(os.path.join(HIER, 'abend.html'), encoding='utf-8').read()
h = h.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
h = h.replace('</body>', LEISTE + '</body>', 1)
open(os.path.join(HIER, 'fenster2-wahl.html'), 'w', encoding='utf-8').write(h)
print('fenster2-wahl.html: %d Bilder' % len(L))
