#!/usr/bin/env python3
"""Culinarium Hannover · Bildwahl für «Wann die Bar offen hat» auf bar.html, 27.10.2026.
Robert: «Können wir da bitte ein anderes Bild einfügen, was irgendwie besser passt? Das ist ja Bullshit mit irgendeinem Handy.»
Baut bar-zeiten-bildwahl.html aus bar.html: das Bild im Abschnitt wechselt mit ← →, ?b=Nummer, 0 ist der heutige Stand (t12).
Eingesetzt wird erst nach Roberts Nummer. Aufruf: python3 website/varianten.py && python3 website/bar_zeiten_bildwahl.py"""
import json, os
import bau

HIER = os.path.dirname(os.path.abspath(__file__))
bau.META.update(json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json'))))

B = [('t12', '50% 50%', 'Heute: Gäste an der Tafel, mit Handy'),
     ('barnacht', '50% 60%', 'Die Bar abends durchs Fenster, das Licht ist an'),
     ('barlicht', '50% 60%', 'Die Bar durchs Fenster, Gäste an der Theke'),
     ('anstossen', '50% 40%', 'Anstossen am Tisch mit Kerzen'),
     ('kerze2', '50% 40%', 'Ein Abend bei Kerzenlicht, Gast im Raum'),
     ('t03', '50% 50%', 'Die gedeckte Tafel mit Gästen'),
     ('toast', '50% 40%', 'Prost mit roten Drinks'),
     ('glas', '50% 50%', 'Ein Drink im Glas, dunkel'),
     ('d1', '50% 50%', 'Zwei Drinks auf dem Tresen'),
     ('tablett', '50% 40%', 'Drinks auf dem Tablett'),
     ('m1', '50% 40%', 'Momo giesst die Gläser'),
     ('g5', '50% 50%', 'Ein Drink auf dem Holztisch'),
     ('team_alle', '50% 45%', 'Das ganze Team an der Bar')]

L = [[k, bau.srcset(k), pos, bau.META[k]['lq'], name] for k, pos, name in B]

SKRIPT = r'''<script>
/* Bild wählen (?b=N): ← → oder Klick; 0 = heute */
(function () {
  var L = %s, s = document.querySelector('.v-bar-zeiten'), fig = s.querySelector('.bk-bild .foto'), im = fig.querySelector('img');
  var n = parseInt(new URLSearchParams(location.search).get('b'), 10); if (!(n >= 0 && n < L.length)) n = 1;
  var t = document.createElement('div');
  t.style.cssText = 'position:fixed;left:50%%;bottom:18px;transform:translateX(-50%%);z-index:300;background:#16151A;color:#FAF4F4;border:1px solid rgba(239,118,73,.6);border-radius:999px;padding:8px 10px;font:500 13px/1 Urbanist,sans-serif;letter-spacing:.06em;display:flex;gap:14px;align-items:center;white-space:nowrap;max-width:calc(100vw - 24px);overflow:hidden';
  var k = 'background:none;border:0;color:#F5A689;font:400 22px/1 Urbanist,sans-serif;cursor:pointer;padding:2px 10px';
  t.innerHTML = '<button type="button" style="' + k + '" data-s="-1" aria-label="Voriges Bild">‹</button><span data-i></span><button type="button" style="' + k + '" data-s="1" aria-label="Nächstes Bild">›</button>';
  document.body.appendChild(t);
  function zeig(i) {
    n = (i + L.length) %% L.length; var x = L[n];
    im.removeAttribute('data-srcset'); im.sizes = '(max-width:860px) 100vw, 84vw'; im.srcset = x[1]; im.src = 'assets/bild/' + x[0] + '-1000.webp'; im.style.objectPosition = x[2];
    fig.style.setProperty('--lq', 'url(' + x[3] + ')');
    t.querySelector('[data-i]').innerHTML = '<span style="color:#F5A689">Bild ' + n + ' / ' + (L.length - 1) + '</span>&nbsp;&nbsp;' + x[4];
    history.replaceState(null, '', '?b=' + n);
  }
  t.addEventListener('click', function (e) { var x = e.target.closest('[data-s]'); if (x) zeig(n + +x.dataset.s); });
  addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); zeig(n + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); zeig(n - 1); } });
  zeig(n);
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function hin() { scrollTo(0, s.getBoundingClientRect().top + scrollY - 40); }
  addEventListener('load', function () { setTimeout(hin, 150); setTimeout(hin, 900); });
})();
</script>
''' % json.dumps(L, ensure_ascii=False)

h = open(os.path.join(HIER, 'bar.html'), encoding='utf-8').read()
assert 'v-bar-zeiten' in h
h = h.replace('<title>', '<title>Bild wählen · ', 1).replace('</body>', SKRIPT + '</body>', 1)
open(os.path.join(HIER, 'bar-zeiten-bildwahl.html'), 'w', encoding='utf-8').write(h)
print('bar-zeiten-bildwahl.html: %d Bilder + heute' % (len(B) - 1))
