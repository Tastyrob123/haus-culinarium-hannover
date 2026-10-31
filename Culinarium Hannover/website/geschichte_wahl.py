#!/usr/bin/env python3
"""Culinarium Hannover · Bar-Seite, Teil «Seit 2017 in Linden.» · Fassungen, direkt in der echten bar.html, 27.10.2026 (dritte Runde).
Robert zur zweiten Runde: «die heutige Version, die schlägt trotzdem alles noch … Das ist ja nicht Sinn der Aufgabe gewesen.»
Lehre: Die heutige Fassung ist die Messlatte (Master 2.1 «Erlebnis» Nr. 1). Was sie stark macht: monumentale Schrift (Titel 104 px,
Zahlen 132 px in Kerze mit Linie darüber), ruhige helle Fläche, und die Bilder als eine geschlossene Wand mit Fugen und einem Schatten.
Die zweite Runde hat das durch Bühnen mit schwebenden Einzelbildern ersetzt: kleiner, unruhiger, schwächer.
Diese Runde behält alles davon und hebt es je Fassung an genau einer Stelle (Bewegung, Umfang, Schrift, Film). Gebaut aus denselben
Bausteinen wie heute (.fwk, .fwk-titel, .gz, .fw.flaeche, .foto), damit nichts unter das heutige Niveau fällt.
Runde 1 und 2 gesichert unter _sicherung/*.vor-neubau-2026-10-27 und *.vor-runde3-2026-10-27.
Baut geschichte-wahl.html (Leiste unten, Pfeiltasten, ?geschichte=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/geschichte_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION

HIER = bau.HIER
bau.META.update(json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json'))))
TEXT = 'Christoph Elbert und Verena Schindler eröffneten die Bar Ende Oktober 2017 in der ehemaligen Fußballkneipe Linden Journal, gegenüber dem 11A. Seit dem Reopening führt Derya Ivkin sie.'
ZAHLEN = [('2017', 'Eröffnung im alten Linden Journal'), ('2023', 'Reopening am 9. November'), ('91', 'Punkte im Falstaff Bar Guide 2027')]
HEUTE = ['fensterdraussen', 'kerze3', 'ws01', 'ws00']
RASTER = 'grid-template-columns:1fr 1.2fr .9fr 1.1fr;grid-template-rows:clamp(300px,34vw,500px)'


def foto(k, sizes='(max-width:860px) 50vw, 30vw'):
    return bau.foto(k, sizes=sizes, auf=False)


def kopf():
    """Titel links, Text rechts, wie heute."""
    return ('<div class="fwk"><div class="fwk-l">' + bau.zl(['Seit 2017', 'in Linden.'], cls='fwk-titel') + '</div>'
            '<div class="fwk-r"><div>' + bau.sw(E(TEXT), cls='fwk-text', i=1) + '</div></div></div>')


def gz(rollen=False):
    """Die drei Zahlen wie heute; mit rollen=True läuft jede Ziffer wie ein Zählwerk an ihren Platz."""
    def zahl(z):
        if not rollen:
            return '<b data-zahl="91">91</b>' if z == '91' else '<b>%s</b>' % z
        return '<b class="g3-rw" aria-label="%s">%s</b>' % (z, ''.join(
            '<span class="g3-rad" aria-hidden="true"><span style="--d:%s;--i:%d">%s</span></span>' % (d, i, ''.join('<i>%d</i>' % n for n in range(10)))
            for i, d in enumerate(z)))
    return '<div class="fwk-extra sw auf"><div class="gz">%s</div></div>' % ''.join(
        '<div>%s<span>%s</span></div>' % (zahl(z), E(t)) for z, t in ZAHLEN)


def wand(zellen, raster=RASTER, cls=''):
    """Die Bilderwand wie heute: eine geschlossene Fläche mit Fugen, die Fotos kommen gemeinsam herauf."""
    return '<div class="fw flaeche auf%s" style="%s">%s</div>' % ((' ' + cls) if cls else '', raster, ''.join(zellen))


def zelle(k, platz='', extra=''):
    return '<div style="%s"%s>%s</div>' % (platz, extra, foto(k))


def film():
    return ('<figure class="film" style="--lq:url(assets/film/familie.webp)"><video muted playsinline preload="none" poster="assets/film/familie.webp?v=%s" '
            'data-src="assets/film/familie.mp4?v=%s" aria-label="Die Mannschaft an der Theke"></video></figure>') % (VERSION, VERSION)


HEUTE_WAND = wand([zelle(k, 'grid-column:%d' % (i + 1)) for i, k in enumerate(HEUTE)])
F = []  # (Name, Inhalt)

# 1 Das Zählwerk: alles wie heute, aber jede Ziffer rollt wie in einem alten Zählwerk an ihren Platz, Stelle für Stelle
F.append(('Das Zählwerk', kopf() + gz(True) + HEUTE_WAND))

# 2 Die Wand läuft: dieselbe Wand, aber endlos seitwärts mit acht Bildern, langsam wie eine Diashow; Zeigen hält sie an
LAUF = ['fensterdraussen', 'kerze3', 'ws01', 'ws00', 'ecke', 'bar', 'barlicht', 'glasnacht']
F.append(('Die Wand läuft', kopf() + gz() + '<div class="fw flaeche auf g3-lauf"><div class="g3-lauf-band">%s</div></div>' % (
    ''.join('<div class="g3-lauf-z">%s</div>' % foto(k, '(max-width:860px) 60vw, 26vw') for k in LAUF + LAUF))))

# 3 Die Wand fächert auf: die vier Bilder liegen beim Hereinkommen übereinander in der Mitte und gleiten an ihren Platz
F.append(('Die Wand fächert auf', kopf() + gz() + wand([zelle(k, 'grid-column:%d;--f:%d' % (i + 1, i)) for i, k in enumerate(HEUTE)], cls='g3-facher')))

# 4 Der Titel über die volle Breite: «Seit 2017 in Linden.» in einer Zeile über die ganze Seite, darunter Text und Zahlen in einer Reihe
F.append(('Der Titel über die volle Breite', bau.zl(['Seit 2017 in Linden.'], cls='fwk-titel g3-breit') + '<div class="g3-reihe">%s%s</div>' % (
    bau.sw(E(TEXT), cls='fwk-text', i=1), gz().replace('fwk-extra sw auf', 'sw auf g3-reihe-z')) + HEUTE_WAND))

# 5 Die Wand randlos: über die volle Breite des Bildschirms und höher, die Fotos zoomen beim Scrollen langsam in ihren Rahmen
F.append(('Die Wand randlos', kopf() + gz() + wand([zelle(k, 'grid-column:%d' % (i + 1)) for i, k in enumerate(HEUTE)],
                                                   'grid-template-columns:1fr 1.2fr .9fr 1.1fr;grid-template-rows:clamp(420px,46vw,700px)', 'g3-randlos')))


# 6 Die Zahlen in der Wand: Zahlen und Fotos teilen sich eine Wand, im Wechsel wie ein Schachbrett
def kachel(z, t, platz):
    b = '<b data-zahl="91">91</b>' if z == '91' else '<b>%s</b>' % z
    return '<div class="g3-kachel" style="%s">%s<span>%s</span></div>' % (platz, b, E(t))


F.append(('Die Zahlen in der Wand', kopf() + wand([
    zelle('fensterdraussen', 'grid-column:1;grid-row:1/3'), kachel('2017', ZAHLEN[0][1], 'grid-column:2;grid-row:1'), zelle('ws01', 'grid-column:2;grid-row:2'),
    zelle('kerze3', 'grid-column:3;grid-row:1/3'), zelle('ws00', 'grid-column:4;grid-row:1'), kachel('2023', ZAHLEN[1][1], 'grid-column:4;grid-row:2'),
    kachel('91', ZAHLEN[2][1], 'grid-column:5;grid-row:1'), zelle('glasnacht', 'grid-column:5;grid-row:2')],
    'grid-template-columns:1.1fr .85fr 1.15fr .85fr .85fr;grid-template-rows:repeat(2,clamp(220px,19vw,300px))', 'g3-schach')))

# 7 Der Film in der Wand: wie heute, aber im dritten Feld läuft der Film der Mannschaft an der Theke
F.append(('Der Film in der Wand', kopf() + gz() + wand([zelle('fensterdraussen', 'grid-column:1'), zelle('kerze3', 'grid-column:2'),
                                                       '<div style="grid-column:3">%s</div>' % film(), zelle('ws00', 'grid-column:4')],
                                                      'grid-template-columns:1fr 1.1fr 1.1fr 1fr;grid-template-rows:clamp(300px,34vw,500px)')))

# 8 Die Wand atmet: wie heute, aber jedes Foto gleitet in seinem Feld mit eigener Geschwindigkeit, die Wand bewegt sich beim Scrollen leise in sich
F.append(('Die Wand atmet', kopf() + gz() + wand([zelle(k, 'grid-column:%d' % (i + 1), ' data-g3-gleit="%s"' % v)
                                                 for i, (k, v) in enumerate(zip(HEUTE, ['.5', '-.35', '.7', '-.55']))], cls='g3-atmet')))

# 9 Sechs Bilder in zwei Reihen: dieselbe Wand mit mehr Welt, hohe und flache Felder im Wechsel
F.append(('Sechs Bilder in zwei Reihen', kopf() + gz() + wand([
    zelle('fensterdraussen', 'grid-column:1;grid-row:1/3'), zelle('kerze3', 'grid-column:2;grid-row:1'), zelle('ecke', 'grid-column:2;grid-row:2'),
    zelle('ws00', 'grid-column:3;grid-row:1/3'), zelle('ws01', 'grid-column:4;grid-row:1'), zelle('glasnacht', 'grid-column:4;grid-row:2')],
    'grid-template-columns:1fr 1.15fr 1.25fr .95fr;grid-template-rows:clamp(240px,21vw,330px) clamp(200px,17vw,270px)')))

# 10 Die Wand zieht vorbei: sieben Bilder, breiter als die Seite; beim Scrollen zieht die Wand seitwärts weiter
ZUG = ['ecke', 'fensterdraussen', 'kerze3', 'ws01', 'ws00', 'bar', 'glasnacht']
F.append(('Die Wand zieht vorbei', kopf() + gz() + '<div class="fw flaeche auf g3-zug" data-g3-zug><div class="g3-zug-band">%s</div></div>' % (
    ''.join('<div class="g3-zug-z">%s</div>' % foto(k, '(max-width:860px) 60vw, 28vw') for k in ZUG))))


def main():
    seite = open(os.path.join(HIER, 'bar.html')).read()
    m = re.search(r'(<section class="vab bar-ab v-bar-geschichte[^"]*"[^>]*>)(<div class="vi h-wand2">.*?</div>)(</section>)', seite, re.S)
    assert m, 'Teil «Seit 2017» in bar.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab bar-ab v-bar-geschichte', 'id="geschichte" data-name="Seit 2017" class="vab bar-ab v-bar-geschichte wahl', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv g3 g3-f%02d" data-n="%d" hidden><div class="vi h-wand2">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Seit 2017</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: drei Zahlen, vier Bilder'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('geschichte-wahl.css', 'geschichte-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["geschichte"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/geschichte-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Seit 2017 wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/geschichte-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'geschichte-wahl.html'), 'w').write(seite)
    print('Seite geschichte-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
