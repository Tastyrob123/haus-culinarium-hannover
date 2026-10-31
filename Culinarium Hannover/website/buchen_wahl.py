#!/usr/bin/env python3
"""Culinarium Hannover · «Platz buchen» (Seite Der Abend) in 15 Fassungen, direkt in der echten Seite, 27.10.2026.
Robert: «Bitte gib mir 15 Visualisierungsmöglichkeiten, um das darzustellen.» Heute: vier helle Terminkarten mit Punktreihe.
Jede Fassung zeigt dieselben Termine aus der Vorschau (localStorage, wie buchen.js) und bucht über denselben Dialog.
Ideen aus der Welt des Hauses (Tafel, vierzehn Plätze, Kerzen, Gläser, Plakate, Rudis Zeilen, Bonschiene am Pass, Anstossen),
abgegrenzt gegen die 20 Fassungen von «Wann und wie viel» (termine_wahl.py). Ein bewegter Moment je Fassung, nur transform und opacity.
Baut buchen-wahl.html (Leiste unten, Pfeiltasten, ?buchen=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/buchen_wahl.py (nach bau.py / buchen.py)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import VERSION

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))

NAMEN = ['Sitzplan der Tafel', 'Vierzehn Kerzen', 'Plakate am Brett', 'Wie Rudis Zeilen', 'Der Ticketblock',
         'Vierzehn Gläser', 'Das Reservierungsbuch', 'Platzkarten auf der Tafel', 'Anstossen: Freitag und Samstag',
         'Abende im Band', 'Der nächste Abend gross', 'Die Strichliste', 'Die Einladung', 'An der Bonschiene', 'Die Gästewand']

BILDER = {'tafelleer': 1600, 'kerze2': 1900, 'kerze3': 1400, 'kerze1': 1000, 'anstossen': 1000, 'toast': 1000,
          'glaeser': 1000, 'tablett': 1000, 'service': 1000, 'kartglas': 1000, 'loch': 1000, 'g5': 1000}
BILDER.update({'t%02d' % n: 400 for n in range(1, 15)})


def src(k, w):
    st = [s for s in META[k]['stufen'] if s <= w] or META[k]['stufen'][:1]
    return 'assets/bild/%s-%d.webp?v=%s' % (k, st[-1], VERSION)


def main():
    seite = open(os.path.join(HIER, 'abend.html')).read()
    m = re.search(r'(<section class="tb"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Platz buchen» in abend.html nicht gefunden (erst buchen.py laufen lassen)'
    kopf_tag = m.group(1).replace('id="termine-buchen"', 'id="buchen" data-name="Platz buchen"', 1).replace('class="tb"', 'class="tb wahl"', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv bw bw-f%02d" data-n="%d" data-bw="%d" hidden></div>' % (i, i, i) for i in range(1, len(NAMEN) + 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Platz buchen</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: vier helle Karten mit Punktreihe'] + NAMEN
    daten = {'bild': {k: src(k, w) for k, w in BILDER.items()}, 'marke': bau.marke('wm')}
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('buchen-wahl.css', 'buchen-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["buchen"],daumen:false};window.BW=%s;</script>
<script src="assets/buchen-wahl.js?v=%s" defer></script>
<script src="assets/wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), json.dumps(daten, ensure_ascii=False), v, VERSION)
    seite = seite.replace('<title>', '<title>Platz buchen wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/buchen-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'buchen-wahl.html'), 'w').write(seite)
    print('Seite buchen-wahl.html', len(seite) // 1024, 'KB,', len(NAMEN), 'Fassungen + heute')


if __name__ == '__main__':
    main()
