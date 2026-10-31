#!/usr/bin/env python3
"""Culinarium Hannover · Hero von «Das Team» (leute.html): Gruppenbild und Schriftzug wählen, 27.10.2026.
Robert: «Teambereich als Hero kann man schon mal das ganze Team … Kannst du mir bitte alle verschiedenen Gruppenbilder geben, die wir haben,
damit ich auswählen kann, und dann noch ein bisschen mit dem Schriftzug arbeiten.»
Zwei Achsen: oben in der Leiste das Gruppenbild (alle Gruppenbilder im Bestand, ?bild=Nummer), unten die Fassung des Schriftzugs (?kopf=Nummer).
Fassung 0 ist der heutige Stand. Schrift nur Fraunces leicht, nie fett, nie kursiv; Kerze als einziger Akzent.
Baut leute-kopf-wahl.html. Aufruf: python3 website/bau.py && python3 website/varianten.py && python3 website/team_kopf_wahl.py"""
import json, os, re, sys
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, sw, knopf

HIER, PROJ = bau.HIER, bau.PROJ
DC = '_quelle/dirty-chicken/'

# Alle Gruppenbilder im Bestand (Bögen aller Quellordner durchgesehen 27.10.2026). Fremdkonten (Events, Bands, Gäste) zeigen nicht das Team.
# (Kürzel, Quelle, Zuschnitt links/rechts als Anteil oder None, object-position im Hero, Name in der Leiste, alt)
BILDER = [
    ('63875', '_quelle/vom-kunden/63875.jpg', None, '50% 30%', 'Zu dritt vor der Bar (heute)', 'Drei aus dem Team vor der Bar'),
    ('63873', '_quelle/vom-kunden/drive/63873.jpg', None, '50% 28%', 'Zu dritt, zweite Aufnahme', 'Drei aus dem Team vor der Bar'),
    ('dz1', DC + 'ig/2026-06-03_dirtychicken.hannover_DZIjZWNCGZT-1.jpg', None, '50% 44%', 'Alle hinter der Theke', 'Das ganze Team hinter der Theke'),
    ('dz2', DC + 'ig/2026-06-03_dirtychicken.hannover_DZIjZWNCGZT-2.jpg', None, '50% 44%', 'Alle, zweite Aufnahme', 'Das ganze Team hinter der Theke'),
    ('84558', DC + 'vom-kunden-2026-10-27/84558.jpg', (.16, .95), '50% 52%', 'Alle, weiter Blick', 'Das ganze Team hinter der Theke'),
    # D geschärft (Robert 27.10.2026: «so richtig geil high-end fotografmässig scharf»). KI: Higgsfield-Upscale auf 4096 px, sehr klar, verändert aber
    # Gesichter leicht (Mimik, Augen, ein Tattoo). Treu: Lanczos auf 2880 px und zweistufiges Nachschärfen, nichts dazuerfunden.
    ('dz2ki', DC + 'hochgerechnet/DZIjZWNCGZT-2-4k.png', None, '50% 44%', 'D scharf, KI 4K', 'Das ganze Team hinter der Theke'),
    ('dz2treu', DC + 'hochgerechnet/DZIjZWNCGZT-2-treu.jpg', None, '50% 44%', 'D geschärft, treu', 'Das ganze Team hinter der Theke'),
]
STUFEN = (800, 1400, 2200)
SATZ = 'Die Abende von Culinarium und ihr Haus, das Walk on the Wild Side: getragen von denselben Leuten.'
FAMILIE = 'Wenn aus Freunden und Kollegen Familie wird.'   # Beitrag DZIjZWNCGZT, aus dem die Gruppenbilder stammen


def bilder_machen():
    meta = {}
    for k, q, schnitt, _p, _n, _a in BILDER:
        qp = os.path.join(PROJ, q)
        im, st = None, []
        for b in STUFEN:
            z = os.path.join(HIER, 'assets/bild/tm_%s-%d.webp' % (k, b))
            if not (os.path.exists(z) and os.path.getmtime(z) > os.path.getmtime(qp)):
                if im is None:
                    im = ImageOps.exif_transpose(Image.open(qp)).convert('RGB')
                    if schnitt:
                        im = im.crop((round(im.width * schnitt[0]), 0, round(im.width * schnitt[1]), im.height))
                if im.width < b * .9 and b != STUFEN[0]:
                    continue
                x = im.resize((b, round(im.height * b / im.width)), Image.LANCZOS) if im.width > b else im
                x.save(z, 'WEBP', quality=82, method=6)
                print('Bild', k, b)
            st.append(b)
        meta[k] = st
    return meta


META = bilder_machen()


def srcset(k):
    return ', '.join('assets/bild/tm_%s-%d.webp?v=%s %dw' % (k, b, VERSION, b) for b in META[k])


def gb(sizes='100vw', cls=''):
    """Gruppenbild; das Skript der Seite tauscht es gegen das gewählte."""
    k, _q, _s, p, _n, alt = BILDER[2]
    return '<img class="tm-i%s" src="assets/bild/tm_%s-800.webp?v=%s" srcset="%s" sizes="%s" alt="%s" style="object-position:%s" decoding="async">' % (
        (' ' + cls) if cls else '', k, VERSION, srcset(k), sizes, E(alt), p)


def titel(cls='', zeilen=('Das Team.',)):
    return zl(list(zeilen), 'h1', 'tm-titel ' + cls)


def satz(i=2, cls=''):
    return sw(SATZ, i=i, cls='tm-satz ' + cls)


def knoepfe(i=3):
    return '<div class="knoepfe sw auf" style="--i:%d">%s</div>' % (i, knopf('Der Abend', 'abend.html'))


def held(cls, inner):
    return '<div class="tm %s">%s</div>' % (cls, inner)


F = []

# 1 Darunter: das Bild randlos oben, die Schrift steht darunter auf der Nacht und liegt nie auf einem Gesicht
F.append(('Darunter', held('tm01', '<figure class="tm-bild tm01-bild tm-setzt auf">%s</figure><div class="tm01-text">%s<div class="tm01-rechts">%s%s</div></div>' % (
    gb(), titel(), satz(), knoepfe()))))

# 2 Über den Köpfen: der Titel steht gross über der Gruppe, Satz und Knopf unten
F.append(('Über den Köpfen', held('tm02', '<figure class="tm-bild tm-setzt auf">%s</figure><div class="tm-grund oben-unten"></div>%s<div class="tm02-unten">%s%s</div>' % (
    gb(), titel('tm02-titel'), satz(), knoepfe()))))

# 3 Angeschnitten: der Titel läuft über die ganze Breite und wird vom unteren Rand angeschnitten
F.append(('Angeschnitten', held('tm03', '<figure class="tm-bild tm-setzt auf">%s</figure><div class="tm-grund oben-unten"></div><div class="tm03-oben">%s%s</div>%s' % (
    gb(), satz(1), knoepfe(2), titel('tm03-titel')))))

# 4 Die Zeilen: links auf der Nacht der Titel und darunter die Aufgaben in Rudis Versalien mit Kerzen-Strichen, rechts das Bild
F.append(('Die Zeilen', held('tm04', '<div class="tm04-text"><p class="tm-k mono sw auf">Culinarium · Walk on the Wild Side</p>%s%s%s%s</div><figure class="tm04-bild tm-setzt auf">%s</figure>' % (
    titel(), zl(['DAS HAUS /', 'DIE DRINKS /', 'DIE KÜCHE /', 'DIE TAFEL'], 'p', 'rudi tm04-zeilen', 1), satz(5), knoepfe(6), gb('(max-width:860px) 100vw, 62vw')))))

# 5 Der Abzug: das Gruppenbild als Abzug mit hellem Rand auf der Nacht, der Titel liegt halb auf dem Abzug, halb darunter
F.append(('Der Abzug', held('tm05', '<div class="tm05-abzug auf"><figure class="tm05-bild">%s</figure><p class="tm05-zeile mono"><span>Das Team</span><span>Linden, Haasemannstraße 13</span></p></div>%s<div class="tm05-unten">%s%s</div>' % (
    gb('(max-width:860px) 92vw, 70vw'), titel('tm05-titel'), satz(), knoepfe()))))

# 6 Das Kinobild: schwarz, in der Mitte ein Breitbild, der Titel im unteren Balken
F.append(('Das Kinobild', held('tm06', '<figure class="tm06-bild tm-setzt auf">%s</figure><div class="tm06-balken">%s<div class="tm06-r">%s%s</div></div>' % (
    gb(), titel(), satz(), knoepfe()))))

# 7 Senkrecht: der Titel läuft an der linken Kante hinauf, das Bild bleibt frei
F.append(('Senkrecht', held('tm07', '<figure class="tm-bild tm-setzt auf">%s</figure><div class="tm-grund links-schmal"></div>%s<div class="tm07-unten">%s%s</div>' % (
    gb(), titel('tm07-titel'), satz(), knoepfe()))))

# 8 Umriss: «Das» als feine Kontur über der Gruppe, «Team.» voll; das Bild bleibt durch die Kontur sichtbar
F.append(('Umriss', held('tm08', '<figure class="tm-bild tm-setzt auf">%s</figure><div class="tm-grund mitte"></div><h1 class="zl auf tm08-titel" aria-label="Das Team."><span class="z"><span class="kontur" style="--i:0">Das</span></span><span class="z"><span style="--i:1">Team.</span></span></h1><div class="tm08-unten">%s%s</div>' % (
    gb(), satz(), knoepfe()))))

# 9 Familie: Titel unten links, daneben der Satz aus dem Beitrag, aus dem die Gruppenbilder stammen
F.append(('Familie', held('tm09', '<figure class="tm-bild tm-setzt auf">%s</figure><div class="tm-grund unten"></div><div class="tm09-unten"><div>%s%s</div><blockquote class="zitat tm09-zitat sw auf" style="--i:2"><p>%s</p><footer class="mono">Dirty Chicken, Juni 2026</footer></blockquote></div>' % (
    gb(), titel(), knoepfe(3), E(FAMILIE)))))

# 10 Gestapelt: links eine Spalte Nacht mit «Das / Team.» riesig übereinander, der Punkt in Kerze; rechts das Bild bis an den Rand
F.append(('Gestapelt', held('tm10', '<div class="tm10-text">%s%s%s</div><figure class="tm10-bild tm-setzt auf">%s</figure>' % (
    titel('tm10-titel', ('Das', 'Team<b class="tm-punkt">.</b>')), satz(), knoepfe(), gb('(max-width:860px) 100vw, 60vw')))))

# 11 Der Rahmen: eine feine helle Linie rahmt das Bild wie ein Passepartout, der Titel unterbricht sie unten
F.append(('Der Rahmen', held('tm11', '<figure class="tm-bild tm-setzt auf">%s</figure><div class="tm-grund unten"></div><div class="tm11-rahmen auf" aria-hidden="true"></div><div class="tm11-unten">%s<div class="tm11-r">%s%s</div></div>' % (
    gb(), titel('tm11-titel'), satz(), knoepfe()))))

# 12 Titelblatt: wie ein Heft, in den vier Ecken die Angaben in Mono, der Titel unten mittig
F.append(('Titelblatt', held('tm12', '<figure class="tm-bild tm-setzt auf">%s</figure><div class="tm-grund rand"></div>'
                         '<p class="tm12-e o-l mono sw auf">Culinarium</p><p class="tm12-e o-r mono sw auf">Walk on the Wild Side</p>'
                         '<div class="tm12-mitte">%s<div class="tm12-reihe">%s%s</div></div><p class="tm12-e u-l mono sw auf">Linden · Haasemannstraße 13</p><p class="tm12-e u-r mono sw auf">Bar · Küche · Tafel</p>' % (
                             gb(), titel(), satz(), knoepfe()))))

# 13 Zurücktreten: das Bild beginnt nah an den Gesichtern und tritt langsam zurück, bis alle zu sehen sind; der Titel steigt mit
F.append(('Zurücktreten', held('tm13', '<figure class="tm-bild tm13-bild auf">%s</figure><div class="tm-grund unten"></div><div class="tm13-text">%s<div class="tm13-reihe">%s%s</div></div>' % (
    gb(), titel(), satz(), knoepfe()))))


def main():
    seite = open(os.path.join(HIER, 'leute.html')).read()
    m = re.search(r'<section class="vab bar-ab v-lt-kopf[^"]*"[^>]*>(.*?)</section>', seite, re.S)
    assert m, 'Kopf in leute.html nicht gefunden (erst bau.py und varianten.py laufen lassen)'
    teile = ['<div class="wv tm-heute" data-n="0">%s</div>' % m.group(1)]
    teile += ['<div class="wv tmv" data-n="%d" hidden>%s</div>' % (i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = '<section class="vab tw wahl" data-ton="nacht" id="kopf" data-name="Schriftzug"><div class="wahl-marke"><b>Team</b><span data-nr></span></div>%s</section>' % ''.join(teile)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Titel unten links auf dem Bild'] + [n for n, _x in F]
    bild = [dict(k=k, name=n, alt=a, pos=p, src='assets/bild/tm_%s-800.webp?v=%s' % (k, VERSION), srcset=srcset(k)) for k, _q, _s, p, n, a in BILDER]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('team-kopf-wahl.css', 'team-kopf-wahl.js'))
    knoepfe_bild = ''.join('<button type="button" data-b="%d"><img src="assets/bild/tm_%s-800.webp?v=%s" alt="" style="object-position:%s"><span><i>%s</i>%s</span></button>' % (
        i, b['k'], VERSION, b['pos'], 'ABCDEFG'[i], E(b['name'])) for i, b in enumerate(bild))
    leiste = '''<div id="wleiste"><div class="tm-bildwahl"><b>Gruppenbild</b><div class="tm-bildknoepfe" data-tm-bilder>%s</div></div><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["kopf"],daumen:false};window.TEAMBILD=%s;</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/team-kopf-wahl.js?v=%s" defer></script>''' % (knoepfe_bild, json.dumps(namen, ensure_ascii=False), json.dumps(bild, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Team-Hero wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/team-kopf-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'leute-kopf-wahl.html'), 'w').write(seite)
    print('Seite leute-kopf-wahl.html', len(seite) // 1024, 'KB,', len(BILDER), 'Gruppenbilder,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
