#!/usr/bin/env python3
"""Rahmen der Wahlseiten «Wie Dirty Chicken von sich spricht» (Robert 28.10.2026: «benutze bitte auch die aktuellen Formate der Website, wie sie jetzt gebaut ist»).
Statt die Nachbarn aus alten Bausteinen nachzubauen, nimmt jede Wahlseite die echte dirty-chicken.html, so wie sie gerade gebaut ist,
und setzt nur an die Stelle des Zitat-Abschnitts den umschaltbaren Block (Nummer 0 = genau der Abschnitt der echten Seite).
So stehen Hero, Fenster, Essen, Nacht, zweites Fenster, Pop-up, Opening und «Aus demselben Haus» immer im heutigen Stand drumherum."""
import json, os, re
import bau

HIER = bau.HIER
LIVE = os.path.join(HIER, 'dirty-chicken.html')
ANFANG = '<section class="vab dc-ab bar-ab v-dc-zitate'


def seite(datei, sid, name, fassungen, css, js, titel, extra_head='', extra_body=''):
    """fassungen: Liste (Name, Satz, HTML). css/js: Dateinamen in assets/. Schreibt datei und gibt die Grösse zurück."""
    h = open(LIVE, encoding='utf-8').read()
    a = h.index(ANFANG)
    e = h.index('<section', a + 20)
    heute = h[a:e]
    teile = ['<div class="wv" data-n="0">%s</div>' % heute]
    teile += ['<div class="wv" data-n="%d" hidden>%s</div>' % (i, x) for i, (_n, _s, x) in enumerate(fassungen, 1)]
    block = '<section class="dw wahl" data-ton="warm" id="%s" data-name="%s"><div class="wahl-marke"><b>%s</b><span data-nr></span></div>%s</section>' % (
        sid, name, name, ''.join(teile))
    h = h[:a] + block + h[e:]
    h = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % titel, h, count=1)
    v = bau.VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in (css, js))
    namen = ['Heute: so steht es auf der Seite'] + [re.sub('&amp;', '&', n) for n, _s, _x in fassungen]
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["%s"],daumen:%s};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/%s?v=%s" defer></script>%s''' % (
        json.dumps(namen, ensure_ascii=False), sid, 'true' if os.path.exists(os.path.join(HIER, 'assets/daumen/%s-1.jpg' % sid)) else 'false',
        bau.VERSION, js, v, extra_body)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/%s?v=%s">\n%s</head>' % (bau.VERSION, css, v, extra_head), 1)
    h = h.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, datei), 'w', encoding='utf-8').write(h)
    return len(h) // 1024
