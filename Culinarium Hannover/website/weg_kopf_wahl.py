#!/usr/bin/env python3
"""Culinarium Hannover · Hero von «Der Weg» (weg.html) in 15 Fassungen, 27.10.2026.
Robert: «Gib mir 15 verschiedene visuelle Darstellungsmöglichkeiten für diesen Hero.» Zweite Runde 16 bis 30: «Bitte 15 weitere Vorschläge.» (Stand davor *.vor-runde2-2026-10-27)
Jede Fassung ist ein Hero über den ganzen ersten Bildschirm (wie die dritte Runde von «Alle Abende»), nur Rudis Fotos von draussen und vom Weg hinein.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut weg-kopf-wahl.html (Leiste unten, Pfeiltasten, ?kopf=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/varianten.py && python3 website/weg_kopf_wahl.py"""
import json, math, os, re, sys
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, sw, knopf

HIER, PROJ = bau.HIER, bau.PROJ
MAPS = 'https://www.google.com/maps/search/?api=1&query=Walk+on+the+Wild+Side+Haasemannstra%C3%9Fe+13+30449+Hannover'
TITEL = ['Haasemann-', 'straße 13.']
SATZ = 'Linden-Mitte. Am Schild über der Hausecke erkennst du die Bar schon von weitem.'

# Fotos von draussen in grösseren Stufen (die Website hat sie nur bis 1000 px), Quelle und Beschreibung aus bau.BILD
SCHLUESSEL = ['schildnacht', 'barnacht', 'schildtag', 'ecke', 'barlicht', 'schildnah', 'fassade', 'flur', 'fensterdraussen']
STUFEN = (800, 1400, 2200)


def fotos_machen():
    for k in SCHLUESSEL:
        qp = os.path.join(PROJ, bau.BILD[k][0])
        im = None
        for b in STUFEN:
            z = os.path.join(HIER, 'assets/bild/wg_%s-%d.webp' % (k, b))
            if os.path.exists(z) and os.path.getmtime(z) > os.path.getmtime(qp):
                continue
            if im is None:
                im = ImageOps.exif_transpose(Image.open(qp)).convert('RGB')
            if im.width < b * .9 and b != STUFEN[0]:
                continue
            x = im.resize((b, round(im.height * b / im.width)), Image.LANCZOS) if im.width > b else im
            x.save(z, 'WEBP', quality=80, method=6)
            print('Foto', k, b)


def foto(k, sizes='100vw', pos='50% 50%', cls='', eager=False):   # lazy: versteckte Fassungen laden erst beim Zeigen
    if k.startswith('kf_'):    # Fotos der Abende aus kopf_wahl.py
        st, alt = [b for b in (800, 1400) if os.path.exists(os.path.join(HIER, 'assets/bild/%s-%d.webp' % (k, b)))], 'Abend in der Bar unter der bemalten Decke'
        pfad = lambda b: 'assets/bild/%s-%d.webp?v=%s' % (k, b, VERSION)
    else:
        st, alt = [b for b in STUFEN if os.path.exists(os.path.join(HIER, 'assets/bild/wg_%s-%d.webp' % (k, b)))], bau.BILD[k][2]
        pfad = lambda b: 'assets/bild/wg_%s-%d.webp?v=%s' % (k, b, VERSION)
    return '<img class="%s" src="%s" srcset="%s" sizes="%s" alt="%s" style="object-position:%s"%s decoding="async">' % (
        cls, pfad(st[0]), ', '.join('%s %dw' % (pfad(b), b) for b in st), sizes, E(alt), pos,
        ' fetchpriority="high"' if eager else ' loading="lazy"')


def titel(zeilen=TITEL, cls='gross'):
    return zl(zeilen, 'h1', cls)


def unten(i=1):
    """Satz und Knopf, wie im heutigen Kopf."""
    return '%s<div class="sw auf wh-knopf" style="--i:%d">%s</div>' % (sw(SATZ, 'p', '', i), i + 1, knopf('In Google Maps öffnen', MAPS))


def text(cls='', zeilen=TITEL):
    return '<div class="wh-text %s">%s%s</div>' % (cls, titel(zeilen), unten())


def held(cls, inner, extra=''):
    return '<div class="wh %s"%s>%s</div>' % (cls, extra, inner)


fotos_machen()   # vor dem Zusammensetzen, foto() liest die vorhandenen Stufen
F = []  # (Name, Inhalt)

# 1 Das Schild geht an: die Hausecke bei Nacht rechts von der dunklen Wand, erst dunkel; nach dem Laden flackert das Schild an wie eine Leuchtreklame
F.append(('Das Schild geht an', held('wh01', '<figure class="wh-bild wh01-bild auf"><span class="wh01-aus">%s</span><span class="wh01-an">%s</span></figure><div class="wh-grund links"></div>%s' % (
    foto('schildnacht', '(max-width:860px) 100vw, 72vw', pos='50% 40%'), foto('schildnacht', '(max-width:860px) 100vw, 72vw', pos='50% 40%'), text('links')))))

# 2 Von weitem: die Strassenecke mit dem Schild Rampenstrasse; beim Scrollen geht man auf das Schild zu
F.append(('Von weitem', held('wh02', '<figure class="wh-bild wh02-bild" data-zieh="nah">%s</figure><div class="wh-grund unten"></div>%s' % (
    foto('ecke', pos='50% 30%'), text('unten-links')))))

# 3 Tag und Nacht: dieselbe Ecke am Tag und in der Nacht, die Naht lässt sich mit Finger oder Maus verschieben
F.append(('Tag und Nacht', held('wh03', '<figure class="wh-bild wh03-tag">%s</figure><div class="wh03-nacht"><figure class="wh-bild wh03-innen">%s</figure></div>'
                               '<div class="wh03-naht" aria-hidden="true"><i>‹ ›</i></div><span class="wh03-w l mono">Am Tag</span><span class="wh03-w r mono">In der Nacht</span>'
                               '<div class="wh-grund unten"></div>%s' % (foto('schildtag', pos='50% 38%'), foto('schildnacht', pos='50% 40%'), text('unten-mitte')),
                  ' data-naht')))

# 4 Das Strassenschild: der Titel als emailliertes Strassenschild mit Hausnummer, es hängt sich beim Laden gerade
F.append(('Das Strassenschild', held('wh04', '<figure class="wh-bild">%s</figure><div class="wh-grund voll"></div>'
                                     '<div class="wh04-mitte"><h1 class="wh04-schild auf" aria-label="Haasemannstraße 13."><span class="wh04-str">Haasemannstraße</span><span class="wh04-nr">13</span></h1>%s</div>' % (
                                         foto('barnacht', pos='50% 55%'), unten()))))

# 5 Die Dreizehn: die Hausnummer riesig, in den Ziffern die Hausecke am Tag; daneben Strasse, Satz und Knopf
F.append(('Die Dreizehn', held('wh05', '<p class="wh05-zahl zl auf" aria-hidden="true"><span class="z"><span style="background-image:url(assets/bild/wg_schildtag-1400.webp?v=%s)">13</span></span></p>'
                               '<div class="wh05-text"><h1 class="zl auf gross" aria-label="Haasemannstraße 13."><span class="z"><span style="--i:1">Haasemann-</span></span><span class="z"><span style="--i:2">straße.</span></span></h1>%s</div>' % (VERSION, unten(3)))))

# 6 Das Fenster: die Wand der Bar bei Nacht, darin ein grosses Sprossenfenster; drinnen die Bar, die beim Scrollen langsamer zieht
F.append(('Das Fenster', held('wh06', '<div class="wh06-fenster"><figure class="wh06-drinnen" data-zieh="tiefe">%s</figure><span class="wh06-s v"></span><span class="wh06-s h"></span></div>%s' % (
    foto('kf_3986', '(max-width:860px) 100vw, 55vw', pos='50% 45%'), text('links')))))

# 7 Über Eck: zwei Wände treffen sich in der Mitte wie die Hausecke; links das Schild am Tag, rechts die Fenster bei Nacht; sie klappen beim Laden auf
F.append(('Über Eck', held('wh07', '<h1 class="vh">Haasemannstraße 13.</h1><div class="wh07-ecke auf">'
                          '<figure class="wh07-f l">%s<p class="wh07-w gross" aria-hidden="true">Haasemann-</p></figure>'
                          '<figure class="wh07-f r">%s<p class="wh07-w gross" aria-hidden="true">straße 13.</p></figure></div><div class="wh07-unten">%s</div>' % (
                              foto('schildtag', '(max-width:860px) 50vw, 46vw', pos='50% 36%'), foto('barnacht', '(max-width:860px) 50vw, 46vw', pos='50% 60%'), unten()))))

# 8 Die Tür: der orange Flur zur Bar über den ganzen Schirm, der Titel dunkel an der hellen Wand über der Tür
F.append(('Die Tür', held('wh08', '<figure class="wh-bild wh-setzt auf">%s</figure><div class="wh-grund fuss"></div>'
                         '<div class="wh08-oben">%s</div><div class="wh08-unten">%s</div>' % (foto('flur', pos='50% 46%'), titel(), unten()))))

# 9 Drei Schritte: die Ecke, das Schild, das Fenster als drei hohe Bilder, versetzt gehängt wie Orgelpfeifen
DREI = [('ecke', '50% 30%', 'Die Ecke'), ('schildnah', '50% 50%', 'Das Schild'), ('barlicht', '50% 50%', 'Das Fenster')]
F.append(('Drei Schritte', held('wh09', '%s<div class="wh09-saeulen">%s</div>' % (
    text('wh09-text'), ''.join('<figure class="wh09-s auf" style="--i:%d">%s<figcaption class="mono">%s</figcaption></figure>' % (i, foto(k, '(max-width:860px) 34vw, 20vw', pos=p), w)
                               for i, (k, p, w) in enumerate(DREI))))))

# 10 Die Kreuzung: Haasemannstrasse und Rampenstrasse als Plan, an der Ecke die Bar im Foto, die Hausnummer pulst
F.append(('Die Kreuzung', held('wh10', '<div class="wh10-strasse h" aria-hidden="true"><span>Haasemannstraße</span><span>Haasemannstraße</span><span>Haasemannstraße</span></div>'
                               '<div class="wh10-strasse v" aria-hidden="true"><span>Rampenstraße</span><span>Rampenstraße</span></div>'
                               '<figure class="wh10-haus auf">%s</figure><span class="wh10-ort" aria-hidden="true"><b>13</b></span>'
                               '<span class="wh10-viertel mono" aria-hidden="true">Linden-Mitte</span>%s' % (
                                   foto('ecke', '(max-width:860px) 50vw, 30vw', pos='50% 40%'), text('wh10-text')))))

# 11 Das Laufband: über den Fenstern bei Nacht laufen Adresse, Viertel und Bar in drei Zeilen gegeneinander
ZEILEN = ['Haasemannstraße 13', 'Linden-Mitte', 'Walk on the Wild Side']
F.append(('Das Laufband', held('wh11', '<figure class="wh-bild">%s</figure><div class="wh-grund voll stark"></div><h1 class="vh">Haasemannstraße 13.</h1>'
                               '<div class="wh11-baender" aria-hidden="true">%s</div><div class="wh11-unten">%s</div>' % (
                                   foto('barlicht', pos='50% 45%'),
                                   ''.join('<div class="wh11-z z%d"><span>%s</span><span>%s</span></div>' % (i, (w + ' <i>/</i> ') * 3, (w + ' <i>/</i> ') * 3) for i, w in enumerate(ZEILEN)),
                                   unten()))))

# 12 Das Schild schwingt: das Schild hängt am Ausleger auf dem dunklen Mauerwerk und pendelt sich beim Laden aus
F.append(('Das Schild schwingt', held('wh12', '%s<div class="wh12-ausleger" aria-hidden="true"><span class="wh12-arm"></span></div>'
                                      '<figure class="wh12-schild auf"><span class="wh12-k l"></span><span class="wh12-k r"></span>%s</figure>' % (
                                          text('wh12-text'), foto('schildnah', '(max-width:860px) 70vw, 30vw', pos='50% 50%')))))

# 13 Die Abzüge: fünf Abzüge vom Weg liegen verstreut auf dem dunklen Tisch und fächern beim Laden aus einem Stapel auf
ABZ = [('ecke', 55, 9, 17, -7), ('schildtag', 74, 4, 15, 6), ('barnacht', 63, 46, 17, 4), ('flur', 82, 44, 14, -5), ('fensterdraussen', 44, 58, 13, 9)]
F.append(('Die Abzüge', held('wh13', '%s%s' % (
    ''.join('<figure class="wh13-a auf" style="--l:%dvw;--t:%dvh;width:%dvw;--r:%ddeg;--dx:calc(50vw - %dvw);--dy:calc(50vh - %dvh - %.1fvw);--i:%d">%s</figure>' % (
        l, t, w, r, l + w / 2, t, w * .68, i, foto(k, '(max-width:860px) 40vw, 18vw', pos='50% 45%')) for i, (k, l, t, w, r) in enumerate(ABZ)),
    text('wh13-text')))))

# 14 Die Visitenkarte: die Fenster bei Nacht, darauf schräg die Karte der Bar mit Adresse, Zeiten und Plus Code
KARTE = ('<div class="wh14-karte auf"><p class="wh14-name">Walk on the Wild Side</p><p class="wh14-adr">Haasemannstraße 13<br>30449 Hannover-Linden</p>'
         '<dl><div><dt class="mono">Die Bar</dt><dd>Do 19 bis 1 Uhr<br>Fr und Sa 19 bis 2 Uhr</dd></div><div><dt class="mono">Culinarium</dt><dd>Fr ab 19 Uhr<br>Sa ab 17 Uhr</dd></div></dl>'
         '<p class="wh14-fuss mono">9PC7+49 Hannover</p></div>')
F.append(('Die Visitenkarte', held('wh14', '<figure class="wh-bild wh-setzt auf">%s</figure><div class="wh-grund links"></div>%s%s' % (
    foto('barnacht', pos='50% 58%'), text('links'), KARTE))))

# 15 Die Taschenlampe: die Ecke liegt im Dunkeln, ein Lichtkegel folgt Maus oder Finger und sucht das Schild; ohne Maus wandert er von selbst
F.append(('Die Taschenlampe', held('wh15', '<figure class="wh-bild">%s</figure><div class="wh15-dunkel" aria-hidden="true"></div>%s' % (
    foto('schildnacht', pos='50% 40%'), text('unten-links')), ' data-lampe')))


# ---------------------------------------------------------------- Zweite Runde, 16 bis 30 (Robert 27.10.2026: «Bitte 15 weitere Vorschläge.»)

# 16 Die Koordinate: der Plus Code der Bar riesig über den Fenstern am Abend, Zeichen für Zeichen; darunter Titel, Satz und Knopf
F.append(('Die Koordinate', held('wh16', '<figure class="wh-bild">%s</figure><div class="wh-grund voll stark"></div>'
                                 '<div class="wh16-code"><p class="mono wh16-wort">Plus Code für Google Maps</p><p class="wh16-zeichen zl auf" aria-label="9PC7+49">%s</p></div>%s' % (
                                     foto('fassade', pos='50% 50%'),
                                     ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i, c) for i, c in enumerate('9PC7+49')),
                                     text('unten-links')))))

# 17 Die Abfahrtstafel: die Zeiten von Bar und Culinarium als Fallblatt-Tafel, die Blätter klappen beim Laden um
TAFEL = [('Donnerstag', 'Die Bar', '19:00', '01:00'), ('Freitag', 'Die Bar', '19:00', '02:00'), ('Freitag', 'Culinarium', '19:00', ''),
         ('Samstag', 'Die Bar', '19:00', '02:00'), ('Samstag', 'Culinarium', '17:00', '')]
F.append(('Die Abfahrtstafel', held('wh17', '<figure class="wh-bild">%s</figure><div class="wh-grund voll stark"></div><div class="wh17-mitte"><div class="wh17-links">%s%s</div>'
                                    '<div class="wh17-tafel auf" role="table" aria-label="Öffnungszeiten"><div class="wh17-r kopf" role="row"><span>Tag</span><span>Was</span><span>Ab</span><span>Bis</span></div>%s</div></div>' % (
                                        foto('barlicht', pos='50% 50%'), titel(), unten(),
                                        ''.join('<div class="wh17-r" role="row">%s</div>' % ''.join('<span class="wh17-b" style="--i:%d">%s</span>' % (r * 4 + j, E(w) or '&#160;') for j, w in enumerate(z)) for r, z in enumerate(TAFEL))))))

# 18 Der Türspion: alles schwarz, in einem runden Messingring die Fenster der Bar; beim Scrollen kommt man ans Guckloch heran
F.append(('Der Türspion', held('wh18', '<div class="wh18-ring" data-zieh="spion"><figure class="wh18-loch">%s</figure></div>%s' % (
    foto('barnacht', '(max-width:860px) 80vw, 46vw', pos='50% 55%'), text('links')))))

# 19 Die Faltkarte: die Hausecke am Tag als gefalteter Plan in fünf Feldern, der sich beim Laden glatt auffaltet
F.append(('Die Faltkarte', held('wh19', '<div class="wh19-karte auf" role="img" aria-label="%s">%s</div><div class="wh-grund unten"></div>%s' % (
    E(bau.BILD['schildtag'][2]),
    ''.join('<span class="wh19-f" style="--i:%d;--r:%ddeg">%s<i></i></span>' % (i, 26 if i % 2 else -26, foto('schildtag', pos='50% 38%')) for i in range(5)),
    text('unten-links')))))

# 20 Der Kreis: das Schild als Quadrat in der Mitte, darum dreht sich langsam ein Ring aus Adresse, Viertel und Bar
RING = 'Haasemannstraße 13 · Linden-Mitte · Walk on the Wild Side · '.replace(' · ', ' — ')
F.append(('Der Kreis', held('wh20', '%s<div class="wh20-mitte"><svg class="wh20-ring" viewBox="0 0 500 500" aria-hidden="true"><defs><path id="wh20-p" d="M250,250 m-212,0 a212,212 0 1,1 424,0 a212,212 0 1,1 -424,0"/></defs>'
                            '<text><textPath href="#wh20-p" textLength="1325">%s</textPath></text></svg><figure class="wh20-schild auf">%s</figure></div>' % (
                                text('wh20-text'), E(RING * 2), foto('schildnah', '(max-width:860px) 50vw, 26vw', pos='50% 50%')))))

# 21 Der Blick nach oben: man steht auf dem Gehweg; beim Laden wandert der Blick die Hauswand hinauf bis zu Strassenschild und Bar-Schild
F.append(('Der Blick nach oben', held('wh21', '<figure class="wh21-wand auf">%s</figure><div class="wh-grund unten"></div>%s' % (
    foto('ecke', pos='50% 50%'), text('unten-links')))))

# 22 Der Satz zuerst: der Satz, an dem man die Bar erkennt, steht gross; die Adresse ist klein darüber
F.append(('Der Satz zuerst', held('wh22', '<figure class="wh-bild">%s</figure><div class="wh-grund voll stark"></div><div class="wh22-text">'
                                  '<h1 class="mono wh22-adr sw auf">Haasemannstraße 13 <i>/</i> Linden-Mitte</h1>%s'
                                  '<div class="sw auf wh-knopf" style="--i:6">%s</div></div>' % (
                                      foto('schildtag', pos='50% 38%'),
                                      zl(['Am Schild über', 'der Hausecke erkennst du', 'die Bar schon von weitem.'], 'p', 'gross', 1),
                                      knopf('In Google Maps öffnen', MAPS)))))

# 23 Der Titel leuchtet: die Adresse selbst ist die Leuchtschrift an der dunklen Wand und flackert beim Laden an
F.append(('Der Titel leuchtet', held('wh23', '<figure class="wh-bild">%s</figure><div class="wh-grund voll stark"></div><div class="wh23-mitte">'
                                     '<p class="mono wh23-ueber">Walk on the Wild Side</p><div class="wh23-neon auf"><h1 class="wh23-t">Haasemannstraße 13.</h1>'
                                     '<p class="wh23-t wh23-glut" aria-hidden="true">Haasemannstraße 13.</p></div>%s</div>' % (foto('schildnacht', pos='50% 40%'), unten()))))

# 24 Die Strasse dazwischen: oben die Ecke am Tag, unten die Fenster bei Nacht; dazwischen die Strasse mit dem Titel, beim Laden rücken beide Hälften heran
F.append(('Die Strasse dazwischen', held('wh24', '<figure class="wh24-h o">%s</figure><figure class="wh24-h u">%s</figure>'
                                         '<div class="wh24-band auf"><div>%s%s</div><div class="sw auf wh-knopf" style="--i:2">%s</div></div>' % (
                                             foto('ecke', pos='50% 26%'), foto('barnacht', pos='50% 52%'), titel(['Haasemannstraße 13.']),
                                             sw(SATZ, 'p', '', 1), knopf('In Google Maps öffnen', MAPS)))))

# 25 Jetzt offen: über dem Titel steht, ob die Bar gerade offen hat oder wann sie wieder öffnet (Zeiten aus fakten.json, Feiertage kennt sie nicht)
F.append(('Jetzt offen', held('wh25', '<figure class="wh-bild wh-setzt auf">%s</figure><div class="wh-grund links"></div>'
                              '<div class="wh-text links"><p class="mono wh25-wer sw auf">Die Bar</p><p class="wh25-status sw auf" data-offen style="--i:1">Donnerstag bis Samstag ab 19 Uhr.</p>%s%s</div>' % (
                                  foto('barlicht', pos='50% 50%'), titel(), unten(2)))))

# 26 Der Rundgang: sechs Bilder vom Weg in einer Reihe über die ganze Höhe, mit Finger oder Maus seitwärts zu ziehen; der Titel ist das erste Feld
RUND = [('ecke', '50% 30%', 'Die Ecke'), ('schildtag', '50% 38%', 'Das Schild am Tag'), ('schildnacht', '50% 40%', 'Das Schild bei Nacht'),
        ('fassade', '50% 50%', 'Die Fenster'), ('flur', '50% 46%', 'Der Flur'), ('kf_3986', '50% 45%', 'Die Bar')]
F.append(('Der Rundgang', held('wh26', '<div class="wh26-zug" tabindex="0" aria-label="Bilder vom Weg, seitwärts ziehen"><div class="wh26-k wh26-anfang">%s%s<p class="mono wh26-hin">Seitwärts ziehen</p></div>%s</div>' % (
    titel(), unten(), ''.join('<figure class="wh26-k">%s<figcaption class="mono">%s</figcaption></figure>' % (foto(k, '(max-width:860px) 80vw, 36vw', pos=p), w) for k, p, w in RUND)),
    ' data-ziehen')))

# 27 Das Zusammensetzen: die Hausecke am Tag in zwölf Teilen, die beim Laden aus allen Richtungen zusammenrücken
TEILE = [(-9, -14, -6), (6, -18, 5), (-4, -12, 3), (12, -9, -7), (-14, 4, 4), (-3, 9, -3), (8, 6, 6), (15, 3, -4), (-10, 15, -5), (4, 17, 4), (-6, 13, 7), (11, 16, -6)]
F.append(('Das Zusammensetzen', held('wh27', '<div class="wh27-bild" role="img" aria-label="%s">%s</div><div class="wh-grund unten"></div>%s' % (
    E(bau.BILD['schildtag'][2]),
    ''.join('<span class="wh27-t auf" style="--c:%d;--z:%d;--dx:%dvw;--dy:%dvh;--r:%ddeg;--i:%d">%s</span>' % (i % 4, i // 4, dx, dy, r, i, foto('schildtag', pos='50% 38%'))
            for i, (dx, dy, r) in enumerate(TEILE)),
    text('unten-links')))))

# 28 Zurücktreten: zuerst ganz nah am Schild, beim Laden tritt man zurück, bis die ganze Hausecke im Bild ist
F.append(('Zurücktreten', held('wh28', '<figure class="wh-bild wh28-bild auf">%s</figure><div class="wh-grund rechts"></div>%s' % (
    foto('schildtag', pos='50% 38%'), text('rechts')))))

# 29 Der Weg als Linie: eine gestrichelte Linie führt vom Knopf über die Strasse bis zum Schild an der Ecke, Strich für Strich
def linie(p0, p1, p2, n=26, aspekt=1.6):
    out = []
    for k in range(n):
        t = (k + .5) / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
        dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
        w = math.degrees(math.atan2(dy, dx * aspekt))
        out.append('<i style="left:%.2f%%;top:%.2f%%;--w:%.1fdeg;--i:%d"></i>' % (x, y, w, k))
    return ''.join(out)


F.append(('Der Weg als Linie', held('wh29', '<figure class="wh-bild">%s</figure><div class="wh-grund unten"></div><div class="wh29-linie auf" aria-hidden="true">%s<b></b></div>%s' % (
    foto('ecke', pos='50% 30%'), linie((36, 84), (54, 98), (60, 66)), text('unten-links')))))

# 30 Die Scheibe: die Fenster der Bar bei Nacht, auf dem Glas die Adresse im Bogen in Blattgold; ein Lichtschein streicht darüber
F.append(('Die Scheibe', held('wh30', '<figure class="wh-bild">%s</figure><div class="wh-grund fuss"></div><h1 class="vh">Haasemannstraße 13.</h1>'
                              '<div class="wh30-glas auf" aria-hidden="true"><svg viewBox="0 0 1000 330"><defs><path id="wh30-b" d="M70,300 Q500,10 930,300"/>'
                              '<linearGradient id="wh30-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7E2A6"/><stop offset=".48" stop-color="#D9A94E"/><stop offset=".52" stop-color="#B8832F"/><stop offset="1" stop-color="#F0CF7E"/></linearGradient></defs>'
                              '<text class="wh30-bogen"><textPath href="#wh30-b" startOffset="50%%" text-anchor="middle">Haasemannstraße 13</textPath></text>'
                              '<text class="wh30-klein" x="500" y="318" text-anchor="middle">WALK ON THE WILD SIDE</text></svg><span class="wh30-schein"></span></div>'
                              '<div class="wh30-unten">%s</div>' % (foto('barlicht', pos='50% 45%'), unten()))))


def main():
    seite = open(os.path.join(HIER, 'weg.html')).read()
    a = seite.find('<section class="vab bar-ab v-weg-kopf')
    assert a >= 0, 'Kopf in weg.html nicht gefunden (erst bau.py und varianten.py laufen lassen)'
    e = seite.find('</section>', a) + len('</section>')
    m = re.match(r'<section class="([^"]+)"([^>]*)>(.*)</section>', seite[a:e], re.S)
    teile = ['<div class="wv %s" data-n="0"%s>%s</div>' % (m.group(1), m.group(2).replace(' data-lauf=""', ''), m.group(3))]
    teile += ['<div class="wv whv" data-n="%d" hidden>%s</div>' % (i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = '<section class="ww wahl" data-ton="strasse" id="kopf" data-name="Kopf">' + '<div class="wahl-marke"><b>Kopf</b><span data-nr></span></div>' + ''.join(teile) + '</section>'
    seite = seite[:a] + neu + seite[e:]
    namen = ['Heute: Titel zwischen zwei Bildern'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('weg-kopf-wahl.css', 'weg-kopf-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["kopf"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/weg-kopf-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Kopf «Der Weg» wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/weg-kopf-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'weg-kopf-wahl.html'), 'w').write(seite)
    print('Seite weg-kopf-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
