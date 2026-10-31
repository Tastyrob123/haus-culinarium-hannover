#!/usr/bin/env python3
"""Culinarium Hannover · Bildwahl für das Fenster «Zu jedem Gang ein eigener Drink.» auf abend.html, 27.10.2026.
Robert: «was haben wir für alternative bilder zu diesem Fenster? die noch nicht so häufig verwendung finden auf der website».
Zweite Runde 27.10.2026 17:07: «15 alternative Bilder … die wir noch nicht so oft benutzt haben».
Nur Bilder mit Drink-Bezug, die auf den sichtbaren Seiten höchstens einmal vorkommen. Bild 1 ist der heutige Stand (tablett).
Baut fenster-wahl.html aus abend.html: Leiste unten, Pfeiltasten ← →, ?fw=Nummer.
Aufruf: python3 website/fenster_wahl.py"""
import json, os

HIER = os.path.dirname(os.path.abspath(__file__))
META = json.load(open(os.path.join(HIER, 'assets/bild/meta.json')))
VERSION = '26131'

# Bild, Ausschnitt, Beschreibung, wie oft heute auf der Website
B = [
    ('tablett', '50% 46%', 'Heute: Tablett mit Gläsern', 'nur hier'),
    ('glas', '50% 36%', 'Ein Glas im Dunkeln', 'nirgends'),
    ('g5', '50% 48%', 'Coupe auf dem Holztisch', 'nirgends'),
    ('kartglas', '50% 35%', 'Roter Drink wird zum Gedeck gereicht', 'nirgends'),
    ('schaumglas', '50% 46%', 'Schaumdrink bei Kerzenlicht', 'nirgends'),
    ('coupe', '50% 46%', 'Coupe und Dessert, Drink zum Gang', 'nirgends'),
    ('hok2', '50% 38%', 'Drink und Dessert im Dunkeln', 'nirgends'),
    ('beeteglas', '50% 30%', 'Drink wird durch die Wand gereicht', 'nirgends'),
    ('g3', '50% 22%', 'Longdrink mit Erdbeere', 'nirgends'),
    ('m3', '50% 40%', 'Gläser mit Goldrand, bereitgestellt', 'nirgends'),
    ('d2', '50% 32%', 'Grüner Drink mit Minze', 'nirgends'),
    ('roq2', '50% 10%', 'Teller, Glas im Vordergrund', 'nirgends'),
    ('t03', '50% 55%', 'Gin-Flasche und Kerze am Tisch', 'nirgends'),
    ('flaschen', '50% 55%', 'Flaschenreihe an der Bar', 'nirgends'),
    ('barneg', '50% 45%', 'Die Bar mit Negroni-Schild', 'nirgends'),
    ('m1', '50% 58%', 'Coupes werden an der Bar gefüllt', 'einmal (Bar)'),
]


def srcset(b):
    return ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (b, s, VERSION, s) for s in META[b]['stufen'])


L = [[b, srcset(b), pos, txt, wie, max(META[b]['stufen'])] for b, pos, txt, wie in B]

LEISTE = r'''<script type="application/json" id="fw-wahl">%s</script>
<script>
/* Bildwahl im Fenster «Zu jedem Gang ein eigener Drink.» (?fw=N): ← → oder Klick wechseln */
(function () {
  var L = JSON.parse(document.getElementById('fw-wahl').textContent), f = document.getElementById('fenster'), img = f.querySelector('.fenster-schicht img');
  var n = parseInt(new URLSearchParams(location.search).get('fw'), 10); if (!(n >= 1 && n <= L.length)) n = 1;
  var t = document.createElement('div');
  t.style.cssText = 'position:fixed;left:50%%;bottom:18px;transform:translateX(-50%%);z-index:300;background:#16151A;color:#FAF4F4;border:1px solid rgba(239,118,73,.6);border-radius:999px;padding:8px 10px;font:500 13px/1 Urbanist,sans-serif;letter-spacing:.06em;display:flex;gap:14px;align-items:center;white-space:nowrap;max-width:calc(100vw - 24px)';
  var k = 'background:none;border:0;color:#F5A689;font:400 22px/1 Urbanist,sans-serif;cursor:pointer;padding:2px 10px';
  t.innerHTML = '<button type="button" style="' + k + '" data-s="-1" aria-label="Voriges Bild">‹</button><span data-i></span><button type="button" style="' + k + '" data-s="1" aria-label="Nächstes Bild">›</button>';
  document.body.appendChild(t);
  function zeig(i) {
    n = (i + L.length - 1) %% L.length + 1; var e = L[n - 1];
    img.removeAttribute('data-srcset'); img.srcset = e[1]; img.sizes = '100vw'; img.style.objectPosition = e[2];
    t.querySelector('[data-i]').innerHTML = '<span style="color:#F5A689">Bild ' + n + ' / ' + L.length + '</span>&nbsp;&nbsp;' + e[3] + '&nbsp;&nbsp;<span style="opacity:.55">' + e[0] + ' · sonst ' + e[4] + (e[5] < 1600 ? ' · max ' + e[5] + ' px' : '') + '</span>';
    history.replaceState(null, '', '?fw=' + n);
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
open(os.path.join(HIER, 'fenster-wahl.html'), 'w', encoding='utf-8').write(h)
print('fenster-wahl.html: %d Bilder' % len(L))
