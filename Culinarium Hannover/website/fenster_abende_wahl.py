#!/usr/bin/env python3
"""Culinarium Hannover · Bildwahl für das Fenster «Jeder Abend hatte sein Plakat.» zwischen Kopf und Vitrinen auf abende.html, 27.10.2026.
Robert: «gib mir bitte 15 verschiedene Variationen, aus denen ich auswählen kann». Auftrag des Fensters: neutraler Übergang vom dunklen, warmen Kopf
ins Warmweiss der Vitrinen, also helle, ruhige Bilder mit wenig Farbe (Beton, Holz, weisse Teller, Tageslicht), keine Kerzen, keine Plakate.
Bild 0 ist der heutige Stand (g5, 63741). Baut abende-fenster-wahl.html aus abende.html: Leiste unten, Pfeiltasten ← →, ?fa=Nummer.
Aufruf: python3 website/bau.py && python3 website/fenster_abende_wahl.py"""
import json, os
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HIER)
D = '_quelle/vom-kunden/drive/'
STUFEN = (800, 1400, 2200)

# Datei, Ausschnitt, Beschreibung
B = [
    ('63741', '50% 55%', 'Heute: Glas auf dem Holztisch vor der Betonwand'),
    ('63740', '50% 52%', 'Es wird durchs Sieb ins Glas gegossen, Betonwand'),
    ('5289', '50% 48%', 'Heller Drink mit Kräutern vor beiger Wand'),
    ('4921', '50% 45%', 'Ein helles Glas vor grauem Grund'),
    ('4582', '50% 50%', 'Ein Teller von oben auf hellem Beton, daneben die Karte'),
    ('5345', '50% 45%', 'Tarte und Eis auf weissem Teller'),
    ('4843', '50% 58%', 'Zwei Drinks vor der hellen Wand'),
    ('4075', '50% 58%', 'Der gedeckte Platz mit Karte bei Tageslicht'),
    ('3967', '50% 42%', 'Die Hausecke an der Rampenstrasse bei Tag'),
    ('5541', '50% 28%', 'Die Schilder an der Hausecke bei Tag'),
    ('4032', '50% 62%', 'Von draussen durchs Fenster der Bar, Tageslicht'),
    ('36611', '50% 50%', 'Mit dem Spritzbeutel am hellen Fenster'),
    ('4238', '50% 50%', 'Blumenkohl auf weissem Teller'),
    ('63963', '50% 50%', 'Schaum aus dem Siphon, helle Wand'),
    ('4834', '50% 50%', 'Leere Gläser mit Goldrand'),
    ('36738', '50% 45%', 'Der Koch richtet am hellen Pass an'),
]


def quelle(n):
    return next(p for p in (D + n + '.jpg', '_quelle/vom-kunden/%s.jpg' % n, '_quelle/vom-kunden/%s.png' % n) if os.path.exists(os.path.join(PROJ, p)))


def machen(n):
    q = os.path.join(PROJ, quelle(n))
    im, st = None, []
    for b in STUFEN:
        z = os.path.join(HIER, 'assets/bild/fa_%s-%d.webp' % (n, b))
        if not (os.path.exists(z) and os.path.getmtime(z) > os.path.getmtime(q)):
            if im is None:
                im = ImageOps.exif_transpose(Image.open(q)).convert('RGB')
            if im.width < b * .9 and b != STUFEN[0]:
                continue
            x = im.resize((b, round(im.height * b / im.width)), Image.LANCZOS) if im.width > b else im
            x.save(z, 'WEBP', quality=80, method=6)
        st.append(b)
    return st, Image.open(q).size[0]


L = []
for n, pos, txt in B:
    st, breite = machen(n)
    L.append([n, ', '.join('assets/bild/fa_%s-%d.webp %dw' % (n, b, b) for b in st), pos, txt, breite])

LEISTE = r'''<script type="application/json" id="fa-wahl">%s</script>
<script>
/* Bildwahl im Fenster «Jeder Abend hatte sein Plakat.» (?fa=N): ← → oder Klick wechseln */
(function () {
  var L = JSON.parse(document.getElementById('fa-wahl').textContent), f = document.getElementById('fenster-abende'), img = f.querySelector('.fenster-schicht img');
  var n = parseInt(new URLSearchParams(location.search).get('fa'), 10); if (!(n >= 0 && n < L.length)) n = 1;
  var t = document.createElement('div');
  t.style.cssText = 'position:fixed;left:50%%;bottom:18px;transform:translateX(-50%%);z-index:300;background:#16151A;color:#FAF4F4;border:1px solid rgba(239,118,73,.6);border-radius:999px;padding:8px 10px;font:500 13px/1 Urbanist,sans-serif;letter-spacing:.06em;display:flex;gap:14px;align-items:center;white-space:nowrap;max-width:calc(100vw - 24px);overflow:hidden';
  var k = 'background:none;border:0;color:#F5A689;font:400 22px/1 Urbanist,sans-serif;cursor:pointer;padding:2px 10px';
  t.innerHTML = '<button type="button" style="' + k + '" data-s="-1" aria-label="Voriges Bild">‹</button><span data-i style="overflow:hidden;text-overflow:ellipsis"></span><button type="button" style="' + k + '" data-s="1" aria-label="Nächstes Bild">›</button>';
  document.body.appendChild(t);
  function zeig(i) {
    n = (i + L.length) %% L.length; var e = L[n];
    img.removeAttribute('data-srcset'); img.srcset = e[1]; img.sizes = '100vw'; img.style.objectPosition = e[2];
    img.closest('figure').style.setProperty('--lq', 'none');
    t.querySelector('[data-i]').innerHTML = '<span style="color:#F5A689">Bild ' + n + ' / ' + (L.length - 1) + '</span>&nbsp;&nbsp;' + e[3] + (e[4] < 1440 ? '&nbsp;&nbsp;<span style="opacity:.55">nur ' + e[4] + ' px breit</span>' : '');
    history.replaceState(null, '', '?fa=' + n);
  }
  t.addEventListener('click', function (e) { var b = e.target.closest('[data-s]'); if (b) zeig(n + +b.dataset.s); });
  addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); zeig(n + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); zeig(n - 1); } });
  zeig(n);
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function hin() { scrollTo(0, f.getBoundingClientRect().top + scrollY - (innerHeight - f.offsetHeight) / 2); }
  addEventListener('load', function () { setTimeout(hin, 150); setTimeout(hin, 900); });
})();
</script>
''' % json.dumps(L, ensure_ascii=False)

h = open(os.path.join(HIER, 'abende.html'), encoding='utf-8').read()
assert 'id="fenster-abende"' in h, 'Fenster fehlt in abende.html (erst bau.py laufen lassen)'
h = h.replace('<title>', '<title>Fensterbild wählen · ', 1)
h = h.replace('</body>', LEISTE + '</body>', 1)
open(os.path.join(HIER, 'abende-fenster-wahl.html'), 'w', encoding='utf-8').write(h)
print('abende-fenster-wahl.html: %d Bilder + heute' % (len(L) - 1))
