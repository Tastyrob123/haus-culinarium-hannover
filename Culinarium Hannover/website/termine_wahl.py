#!/usr/bin/env python3
"""Culinarium Hannover · «Wann und wie viel» (Seite Der Abend) in 35 Fassungen, direkt in der echten Seite, 27.10.2026 (Runde 2: Fassungen 21 bis 35, «Irgendwie gefällt mir das nicht»).
Robert: «20 alternative visualisierungsmöglichkeiten für den abschnitt». Heute: randloses Tafelfoto, darauf Titel, vier grosse Zahlen in einer Reihe, Satz.
Ideen aus der Welt des Hauses (Ticket, Plakat, Tafel, Kerze, Negroni-Schriftzug, Tür), Rohwerte aus der Entwurfs-Maschine (angebote).
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Nur belegte Fakten: freitags ab 19:00, samstags ab 17:00, 14 Plätze, zuletzt 89 € am 25. und 26.09.2026 ausgebucht, Storno wörtlich (DbYnkdkjrNy, DVjkofijp6R).
Baut termine-wahl.html (Leiste unten, Pfeiltasten, ?termine=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/termine_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, marke

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))

TITEL = ['Wann und', 'wie viel.']
STORNO = '„Da die Plätze begrenzt sind, bitten wir um Verständnis, dass Tickets nicht rückerstattet werden können.“'
SATZ = ('Culinarium findet an einzelnen Wochenenden statt, der Preis gilt für den ganzen Abend, Essen und Drinks. '
        'Der nächste Termin steht noch nicht fest. Tickets gibt es bisher nur im Vorverkauf. ' + STORNO)
ZUL = 'zuletzt, 25. und 26. September 2026, ausgebucht'
ORT = 'Walk on the Wild Side · Haasemannstraße 13 · Linden'
MIT = 'A UNiQUE EXPERiENCE BY MOMO X RUDI'
EUR = '89&#160;€'
X = '<i class="tw-x" aria-hidden="true">×</i>'


def bild(k, w=1000, cls='', pos='50% 50%', alt=None):
    st = [s for s in META[k]['stufen'] if s <= w] or META[k]['stufen'][:1]
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        cls, k, st[-1], VERSION, E(alt if alt is not None else bau.BILD[k][2]), pos)


def src(k, w=1000):
    st = [s for s in META[k]['stufen'] if s <= w] or META[k]['stufen'][:1]
    return 'assets/bild/%s-%d.webp?v=%s' % (k, st[-1], VERSION)


def satz(cls='', i=2):
    return '<p class="sw auf tw-satz %s" style="--i:%d">%s</p>' % (cls, i, SATZ)


def titel(cls='', mit_satz=True):
    return '<div class="tw-tk %s">%s%s</div>' % (cls, zl(TITEL, 'h2', 'tw-h'), satz() if mit_satz else '')


F = []  # (Name, Inhalt)

# 1 Das Ticket: ein Billett mit Abriss liegt schräg auf dem Foto der Tafel; beim Ankommen löst sich der Abriss ein Stück
F.append(('Das Ticket', '<div class="tw01">%s<div class="tw01-buehne"><figure class="tw01-f auf">%s</figure>'
          '<div class="tw01-ticket auf eigen" style="--i:2"><div class="tw01-haupt"><div class="tw01-marke">%s</div><p class="tw-mit">%s</p>'
          '<div class="tw01-tage"><p><span>Freitag</span><b>ab 19:00</b></p><p><span>Samstag</span><b>ab 17:00</b></p></div>'
          '<p class="tw01-preis"><b>%s</b><span>der ganze Abend, Essen und Drinks</span></p><p class="tw01-ort">%s</p></div>'
          '<div class="tw01-abriss"><b>14</b><span>Plätze an einer Tafel</span><em>25. + 26.09.2026<br>ausgebucht</em></div></div></div></div>' % (
              titel(), bild('kartglas', 1600), marke('wm'), MIT, EUR, ORT)))

# 2 Das Plakat des Abends: wie die echten Culinarium-Plakate; daneben schiebt sich ein leeres Plakat für den nächsten Termin herein
F.append(('Plakat des Abends', '<div class="tw02">%s<div class="tw02-wand"><div class="tw02-plakat"><p class="tw-mit">%s</p><div class="tw02-marke">%s</div>'
          '<p class="tw02-datum">25. + 26.09.2026</p><div class="tw02-zeilen"><p><span>Freitag</span><b>ab 19:00</b></p><p><span>Samstag</span><b>ab 17:00</b></p>'
          '<p><span>Plätze</span><b>14</b></p><p><span>Preis</span><b>%s</b></p></div><p class="tw02-ort">Walk on the Wild Side · Haasemannstraße 13</p>'
          '<span class="tw02-quer">Ausgebucht</span></div>'
          '<div class="tw02-leer auf eigen"><p class="tw-mit">%s</p><div class="tw02-marke">%s</div><p class="tw02-frage">Der nächste Abend</p><p class="tw02-folgt">Datum folgt</p></div></div></div>' % (
              titel(), MIT, marke('wm'), EUR, MIT, marke('wm'))))

# 3 Die Tafel von oben: vierzehn Gedecke, die Kerzen in der Mitte; die Gedecke werden nacheinander aufgelegt
TELLER = []
for seite, y in ((0, 92), (1, 328)):
    for n in range(7):
        x = 205 + n * 131.6
        TELLER.append('<g class="tw03-g" style="--i:%d"><circle cx="%.1f" cy="%d" r="38" class="tw03-t"/><circle cx="%.1f" cy="%d" r="26" class="tw03-ti"/>'
                      '<circle cx="%.1f" cy="%d" r="9" class="tw03-gl"/><line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="tw03-b"/><line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="tw03-b"/></g>' % (
                          seite * 7 + n, x, y, x, y, x + 44, y + (34 if seite == 0 else -34), x - 52, y - 22, x - 52, y + 22, x + 52, y - 22, x + 52, y + 22))
KERZEN = ''.join('<circle cx="%d" cy="210" r="34" class="tw03-schein"/><circle cx="%d" cy="210" r="7" class="tw03-k"/>' % (x, x) for x in (330, 600, 870))
F.append(('Die Tafel von oben', '<div class="tw03">%s<div class="tw03-tisch"><p class="tw03-kopf l"><span>Freitag</span><b>ab 19:00</b></p>'
          '<svg class="tw03-svg auf eigen" viewBox="0 0 1200 420" aria-hidden="true"><rect x="120" y="150" width="960" height="120" rx="6" class="tw03-holz"/>%s%s</svg>'
          '<p class="tw03-kopf r"><span>Samstag</span><b>ab 17:00</b></p></div>'
          '<div class="tw03-unten"><p class="tw03-zahl"><b data-zahl="14">14</b><span>Plätze an einer Tafel</span></p><p class="tw03-zahl"><b>%s</b><span>%s</span></p>%s</div></div>' % (
              zl(TITEL, 'h2', 'tw-h tw-mi'), ''.join(TELLER), KERZEN, EUR, ZUL, satz('tw03-s'))))

# 4 Freitag und Samstag: zwei Hochformate an der Naht, sie steigen getrennt herauf und stossen an wie zwei Gläser
F.append(('Freitag und Samstag', '<div class="tw04"><div class="tw04-kopf">%s%s</div><div class="tw04-paar">'
          '<figure class="tw04-f a auf eigen">%s<figcaption><span>Freitags ab</span><b>19:00</b></figcaption></figure>'
          '<figure class="tw04-f b auf eigen">%s<figcaption><span>Samstags ab</span><b>17:00</b></figcaption></figure></div>'
          '<div class="tw04-fuss"><p><b>14</b> Plätze an einer Tafel</p><p><b>%s</b> %s</p></div></div>' % (
              zl(TITEL, 'h2', 'tw-h'), satz('tw04-s'), bild('kerze2', 1600, pos='50% 60%'), bild('anstossen', 1600, pos='50% 45%'), EUR, ZUL)))

# 5 Das Zifferblatt: der Abend als Bogen auf der Uhr, samstags ab fünf, freitags ab sieben; der Zeiger läuft auf siebzehn Uhr
STRICHE = ''.join('<line x1="200" y1="%d" x2="200" y2="%d" transform="rotate(%d 200 200)" class="tw05-s%s"/>' % (
    14 if h % 3 == 0 else 18, 30 if h % 3 == 0 else 26, h * 30, ' dick' if h % 3 == 0 else '') for h in range(12))
F.append(('Das Zifferblatt', '<div class="tw05"><div class="tw05-uhr auf eigen"><svg viewBox="0 0 400 400" aria-hidden="true">'
          '<circle cx="200" cy="200" r="196" class="tw05-rand"/>%s'
          '<path d="M284.0 345.5 A168 168 0 1 1 200.0 32.0" class="tw05-bogen t-sa"/><path d="M131.0 319.5 A138 138 0 0 1 200.0 62.0" class="tw05-bogen t-fr"/>'
          '<text x="292" y="372" class="tw05-z">17</text><text x="104" y="346" class="tw05-z">19</text>'
          '<g class="tw05-zeiger"><line x1="200" y1="200" x2="200" y2="70" /><circle cx="200" cy="200" r="7"/></g></svg></div>'
          '<div class="tw05-r">%s<div class="tw05-legende"><p class="t-sa"><i></i><span>Samstags ab</span><b>17:00</b></p><p class="t-fr"><i></i><span>Freitags ab</span><b>19:00</b></p></div>'
          '<p class="tw05-mehr"><b>14</b> Plätze an einer Tafel%s<b>%s</b> %s</p>%s</div></div>' % (
              STRICHE, zl(TITEL, 'h2', 'tw-h'), X, EUR, ZUL, satz())))

# 6 Das Kalenderblatt: September 2026, der 25. und 26. angestrichen; das Blatt hebt sich und zeigt das nächste, noch leere
TAGE = ['<span class="tw06-leer"></span>'] + ['<span class="%s">%s</span>' % (
    'an' if d in (25, 26) else ('we' if d % 7 in (4, 5) else ''),
    ('%d<em>%s</em>' % (d, '19:00' if d == 25 else '17:00')) if d in (25, 26) else d) for d in range(1, 31)]
F.append(('Das Kalenderblatt', '<div class="tw06"><div class="tw06-block auf eigen"><div class="tw06-unter"><p class="tw06-monat">Nächster Termin</p><p class="tw06-folgt">steht noch nicht fest</p></div>'
          '<div class="tw06-blatt"><div class="tw06-loch"><i></i><i></i></div><p class="tw06-monat">September <span>2026</span></p>'
          '<div class="tw06-wt"><span>Mo</span><span>Di</span><span>Mi</span><span>Do</span><span>Fr</span><span>Sa</span><span>So</span></div>'
          '<div class="tw06-tage">%s</div><p class="tw06-stempel">Ausgebucht</p></div></div>'
          '<div class="tw06-r">%s<p class="tw06-zahlen"><span><b>Freitags</b> ab 19:00</span><span><b>Samstags</b> ab 17:00</span><span><b>14</b> Plätze an einer Tafel</span><span><b>%s</b> zuletzt, Essen und Drinks</span></p>%s</div></div>' % (
              ''.join(TAGE), zl(TITEL, 'h2', 'tw-h'), EUR, satz())))

# 7 Unter dem Negroni: neben dem Schriftzug der Bar leuchten die vier Angaben als Leuchtschrift auf, Zeile für Zeile
F.append(('Unter dem Negroni', '<div class="tw07"><figure class="tw07-f">%s</figure><div class="tw07-wand">%s'
          '<div class="tw07-neon auf eigen"><p style="--i:0"><span>Freitags ab</span>19:00</p><p style="--i:1"><span>Samstags ab</span>17:00</p>'
          '<p style="--i:2"><span>Plätze an einer Tafel</span>14</p><p style="--i:3"><span>zuletzt, ausgebucht</span>%s</p></div>%s</div></div>' % (
              bild('barneg', 1600, pos='50% 40%'), zl(TITEL, 'h2', 'tw-h'), EUR, satz())))

# 8 Die Anzeigetafel: Fallblätter wie an einem Bahnsteig; beim Ankommen klappen die Blätter in die Zeile
def klapp(t, w):
    t = t.ljust(w)
    return ''.join('<span style="--i:%d">%s</span>' % (n, E(c) if c != ' ' else '&#160;') for n, c in enumerate(t))


ZEILEN8 = [('FREITAG', 'AB 19:00', 'CULINARIUM'), ('SAMSTAG', 'AB 17:00', 'CULINARIUM'), ('PLÄTZE', '14', 'EINE TAFEL'),
           ('PREIS', '89 EUR', 'ESSEN+DRINKS'), ('ZULETZT', '25+26.09.', 'AUSGEBUCHT'), ('NÄCHSTER', '--.--.', 'FOLGT')]
F.append(('Die Anzeigetafel', '<div class="tw08">%s<div class="tw08-tafel auf eigen"><div class="tw08-kopf"><span>Abend</span><span>Zeit</span><span>Hinweis</span></div>%s</div>%s</div>' % (
    zl(TITEL, 'h2', 'tw-h'),
    ''.join('<div class="tw08-z%s"><p>%s</p><p>%s</p><p>%s</p></div>' % (' warm' if r >= 4 else '', klapp(a, 8), klapp(b, 9), klapp(c, 12)) for r, (a, b, c) in enumerate(ZEILEN8)),
    satz('tw08-s'))))

# 9 Die Kerze brennt herunter: eine Kerze misst den Abend, oben samstags ab 17:00, zwei Stunden tiefer freitags ab 19:00; sie brennt mit dem Scrollen ab
F.append(('Die Kerze', '<div class="tw09"><figure class="tw09-f">%s</figure><div class="tw09-mitte" data-tw-kerze><div class="tw09-kerze"><span class="tw09-flamme"><i></i></span><span class="tw09-wachs"></span></div>'
          '<p class="tw09-mark t-sa"><b>17:00</b><span>samstags ab</span></p><p class="tw09-mark t-fr"><b>19:00</b><span>freitags ab</span></p></div>'
          '<div class="tw09-r">%s<p class="tw09-zahl"><b>14</b><span>Plätze an einer Tafel</span></p><p class="tw09-zahl"><b>%s</b><span>%s</span></p>%s</div></div>' % (
              bild('kerze2', 1000, pos='50% 50%'), zl(TITEL, 'h2', 'tw-h'), EUR, ZUL, satz())))

# 10 Der Stempel: der Preis riesig, darüber landet der Stempel «Ausgebucht»; links die Angaben wie auf einer Bestellliste
F.append(('Der Stempel', '<div class="tw10"><div class="tw10-l">%s<div class="tw10-liste"><p><span>Freitags</span><b>ab 19:00</b></p><p><span>Samstags</span><b>ab 17:00</b></p>'
          '<p><span>An einer Tafel</span><b>14 Plätze</b></p><p><span>Im Preis</span><b>Essen und Drinks</b></p></div>%s</div>'
          '<div class="tw10-r"><figure class="tw10-f">%s</figure><div class="tw10-mitte"><p class="tw10-preis">%s</p><p class="tw10-stempel auf eigen"><span>Ausgebucht</span><em>25. + 26. September 2026</em></p></div></div></div>' % (
              zl(TITEL, 'h2', 'tw-h'), satz(), bild('karte', 1000, pos='50% 50%'), EUR)))

# 11 Was drin ist: der Abend als Rechnung, Aperitif plus drei Gänge plus fünf Drinks plus Tasting ergibt 89 €; die Teile rücken zusammen
TEILE11 = [('Aperitif', 'glaeser'), ('Drei Gänge', 'roq1'), ('Fünf Drinks', 'g1'), ('Tasting', 'klaeren')]
F.append(('Was drin ist', '<div class="tw11"><div class="tw11-kopf">%s<p class="tw11-zeit"><span><b>Freitags</b> ab 19:00</span><span><b>Samstags</b> ab 17:00</span><span><b>14</b> Plätze an einer Tafel</span></p></div>'
          '<div class="tw11-rechnung auf eigen">%s<span class="tw11-op gleich" style="--i:4">=</span><p class="tw11-summe" style="--i:4"><b>%s</b><span>%s</span></p></div>%s</div>' % (
              zl(TITEL, 'h2', 'tw-h'),
              '<span class="tw11-op">+</span>'.join('<figure class="tw11-t" style="--i:%d">%s<figcaption>%s</figcaption></figure>' % (n, bild(k, 640), E(t)) for n, (t, k) in enumerate(TEILE11)),
              EUR, ZUL, satz('tw11-s'))))

# 12 Zahlen im Bild: die Angaben stehen dort im Foto, wo sie hingehören, die Zeiten bei den Kerzen, die 14 an der Tafel, der Preis auf der Karte
F.append(('Zahlen im Bild', '<div class="tw12"><div class="tw12-l">%s</div><div class="tw12-bild"><figure class="tw12-f" data-tw-zoom>%s</figure>'
          '<p class="tw12-in kerzen auf" style="--i:1"><span>Freitags ab</span><b>19:00</b><span>Samstags ab</span><b>17:00</b></p>'
          '<p class="tw12-in tafel auf" style="--i:2"><b>14</b><span>Plätze an einer Tafel</span></p>'
          '<p class="tw12-in karte auf" style="--i:3"><b>%s</b><span>zuletzt, ausgebucht</span></p></div></div>' % (
              titel(), bild('tafelleer', 1600, pos='50% 50%'), EUR)))

# 13 Das Türschild: an der Tür zur Tafel hängt ein Schild mit den Zeiten; beim Ankommen pendelt es aus
F.append(('Das Türschild', '<div class="tw13"><figure class="tw13-f">%s</figure><div class="tw13-r"><div class="tw13-haken auf eigen"><svg class="tw13-schnur" viewBox="0 0 200 70" aria-hidden="true"><path d="M30 70 L100 6 L170 70"/><circle cx="100" cy="6" r="5"/></svg>'
          '<div class="tw13-schild"><div class="tw13-marke">%s</div><p class="tw13-z"><span>Freitags ab</span><b>19:00</b></p><p class="tw13-z"><span>Samstags ab</span><b>17:00</b></p>'
          '<p class="tw13-unten">14 Plätze an einer Tafel</p><span class="tw13-zettel">25./26.09. ausgebucht</span></div></div>%s<p class="tw13-preis"><b>%s</b> %s, der ganze Abend mit Essen und Drinks</p>%s</div></div>' % (
              bild('kerze3', 1600, pos='40% 50%'), marke('wm'), zl(TITEL, 'h2', 'tw-h'), EUR, ZUL, satz())))

# 14 Freitag oder Samstag? Zwei grosse Wörter, antippen tauscht Foto und Uhrzeit an derselben Stelle
TAG14 = [('Freitag', '19:00', 'kerze2'), ('Samstag', '17:00', 'toast')]
F.append(('Freitag oder Samstag?', '<div class="tw14" data-tw><div class="tw14-l"><p class="tw14-frage zl auf" aria-label="Freitag oder Samstag?"><span class="z"><span style="--i:0">Freitag oder</span></span><span class="z"><span style="--i:1">Samstag?</span></span></p>'
          '<div class="tw14-wahl">%s</div><div class="tw14-zeiten">%s</div><p class="tw14-mehr"><b>14</b> Plätze an einer Tafel%s<b>%s</b> %s</p>%s</div>'
          '<div class="tw14-bild auf">%s</div></div>' % (
              ''.join('<button type="button" class="%s" data-q="%d">%s</button>' % ('an' if i == 0 else '', i, t) for i, (t, _z, _k) in enumerate(TAG14)),
              ''.join('<p class="tw14-zeit%s" data-a="%d"><span>%ss ab</span><b>%s</b></p>' % (' an' if i == 0 else '', i, t.lower().capitalize(), z) for i, (t, z, _k) in enumerate(TAG14)),
              X, EUR, ZUL, satz(),
              ''.join('<figure class="tw14-f%s" data-a="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(k, 1600)) for i, (_t, _z, k) in enumerate(TAG14)))))

# 15 Vierzehn: die Zahl so gross wie der Bildschirm, durch sie hindurch die Tafel; das Foto wandert in der Zahl gegenläufig
F.append(('Vierzehn', '<div class="tw15"><div class="tw15-zahl auf"><svg viewBox="0 0 1000 620" role="img" aria-label="14 Plätze">'
          '<defs><clipPath id="tw15-clip"><text x="500" y="560" text-anchor="middle" class="tw15-t">14</text></clipPath></defs>'
          '<g clip-path="url(#tw15-clip)"><rect width="1000" height="620" fill="#2A2228"/><image href="%s" x="0" y="-180" width="1000" height="1250" preserveAspectRatio="xMidYMid slice" data-tw-drift/></g></svg></div>'
          '<div class="tw15-unten"><p class="tw15-was">Plätze an einer Tafel</p><div class="tw15-rest">%s<p class="tw15-zeile"><span><b>Freitags</b> ab 19:00</span><span><b>Samstags</b> ab 17:00</span><span><b>%s</b> %s</span></p>%s</div></div></div>' % (
              src('t03', 1600), zl(TITEL, 'h2', 'tw-h'), EUR, ZUL, satz())))

# 16 Der Untersetzer: vorne die Marke, hinten die Angaben; er dreht sich beim Ankommen um, antippen wendet ihn zurück
F.append(('Der Untersetzer', '<div class="tw16"><div class="tw16-l">%s</div><div class="tw16-buehne"><figure class="tw16-f">%s</figure>'
          '<button type="button" class="tw16-deckel auf eigen" data-tw-wende aria-label="Untersetzer wenden"><span class="tw16-dreh">'
          '<span class="tw16-s vorn"><span class="tw16-marke">%s</span><span class="tw16-mit">%s</span></span>'
          '<span class="tw16-s hinten"><span class="tw16-k">Culinarium</span><span class="tw16-z"><em>Freitags ab</em>19:00</span><span class="tw16-z"><em>Samstags ab</em>17:00</span>'
          '<span class="tw16-kl">14 Plätze · %s</span><span class="tw16-k">zuletzt ausgebucht</span></span></span></button></div></div>' % (
              titel(), bild('g5', 1600), marke('wm'), MIT, EUR)))

# 17 Ein Satz: alles in einem grossen Satz, die Zahlen in Kerze; er fährt zeilenweise aus dem Schlitz
F.append(('Ein Satz', '<div class="tw17"><p class="tw-kick">Wann und wie viel</p><p class="tw17-satz zl auf" aria-label="Freitags ab 19:00, samstags ab 17:00. 14 Plätze an einer Tafel. Zuletzt 89 Euro für den ganzen Abend, Essen und Drinks.">'
          '<span class="z"><span style="--i:0">Freitags ab <b>19:00</b>,</span></span><span class="z"><span style="--i:1">samstags ab <b>17:00</b>.</span></span>'
          '<span class="z"><span style="--i:2"><b>14</b> Plätze an einer Tafel.</span></span><span class="z"><span style="--i:3">Zuletzt <b>%s</b> für den ganzen</span></span>'
          '<span class="z"><span style="--i:4">Abend, Essen und Drinks.</span></span></p>'
          '<div class="tw17-unten"><figure class="tw17-f">%s</figure><div><p class="tw17-zul">25. und 26. September 2026, ausgebucht.</p>%s</div></div></div>' % (
              EUR, bild('loch', 1000, pos='50% 60%'), satz())))

# 18 Vierzehn Streifen: ein Streifen je Platz, die Hälfte kommt von oben, die andere von unten, wie zwei Reihen an der Tafel
F.append(('Vierzehn Streifen', '<div class="tw18"><div class="tw18-kopf">%s<p class="tw18-zeile"><span><b>Freitags</b> ab 19:00</span><span><b>Samstags</b> ab 17:00</span><span><b>%s</b> %s</span></p></div>'
          '<div class="tw18-streifen auf eigen">%s</div><div class="tw18-fuss"><p class="tw18-14"><b>14</b> Plätze an einer Tafel, jeder Streifen ein Platz</p>%s</div></div>' % (
              zl(TITEL, 'h2', 'tw-h'), EUR, ZUL,
              ''.join('<figure class="tw18-s %s" style="--i:%d">%s</figure>' % ('o' if n % 2 == 0 else 'u', n, bild('t%02d' % (n + 1), 640)) for n in range(14)),
              satz())))

# 19 Der Zeitstrahl: das Wochenende als zwei Bahnen von 16 bis 24 Uhr, die Abende beginnen um 19 und 17 Uhr und laufen offen aus
STUNDEN = ''.join('<span style="--h:%d">%02d</span>' % (h - 16, h) for h in range(16, 25))
F.append(('Der Zeitstrahl', '<div class="tw19"><div class="tw19-kopf">%s%s</div><div class="tw19-strahl auf eigen"><div class="tw19-stunden">%s</div>'
          '<div class="tw19-bahn"><p class="tw19-tag"><b>Freitag</b><span>ab 19:00</span></p><div class="tw19-spur"><div class="tw19-abend" style="--ab:3">%s</div></div></div>'
          '<div class="tw19-bahn"><p class="tw19-tag"><b>Samstag</b><span>ab 17:00</span></p><div class="tw19-spur"><div class="tw19-abend" style="--ab:1">%s</div></div></div></div>'
          '<div class="tw19-fuss"><p><b>14</b> Plätze an einer Tafel</p><p><b>%s</b> %s</p></div></div>' % (
              zl(TITEL, 'h2', 'tw-h'), satz('tw19-s'), STUNDEN, bild('kerze2', 1600, pos='50% 55%'), bild('anstossen', 1600, pos='50% 40%'), EUR, ZUL)))

# 20 Laufband: zwei Zeilen aus den Angaben laufen gegenläufig über das Foto der Tafel
LAUF1 = ('Freitags ab 19:00' + X + 'Samstags ab 17:00' + X) * 3
LAUF2 = ('14 Plätze an einer Tafel' + X + EUR + ' für den ganzen Abend' + X) * 3
F.append(('Laufband', '<div class="tw20"><div class="tw20-buehne"><figure class="tw20-f">%s</figure><div class="tw20-baender" aria-hidden="true">'
          '<p class="tw20-band"><span>%s</span><span>%s</span></p><p class="tw20-band zur"><span>%s</span><span>%s</span></p></div></div>'
          '<div class="tw20-unten">%s<div><p class="tw20-zul">Freitags ab 19:00, samstags ab 17:00, 14 Plätze, %s %s.</p>%s</div></div></div>' % (
              bild('tafelleer', 1600, pos='50% 60%'), LAUF1, LAUF1, LAUF2, LAUF2, zl(TITEL, 'h2', 'tw-h'), EUR, ZUL, satz())))


# ---------------------------------------------------------------- Runde 2 (27.10.2026): ruhiger, Foto und Schrift statt Gegenstände
FAKTEN = [('Freitags ab', '19:00'), ('Samstags ab', '17:00'), ('Plätze an einer Tafel', '14'), ('Zuletzt, 25. und 26. September 2026, ausgebucht', EUR)]

# 21 Vier Ecken: das Foto wächst mit dem Scrollen aus der Mitte zum Vollbild, die vier Angaben stehen in den Ecken
F.append(('Vier Ecken', '<div class="tw21" data-tw-ecken><div class="tw21-buehne"><figure class="tw21-f">%s</figure>%s<div class="tw21-titel">%s</div></div><div class="tw21-weg"></div><div class="tw21-unten">%s</div></div>' % (
    bild('tafelleer', 1600, pos='50% 55%'),
    ''.join('<p class="tw21-e e%d"><b>%s</b><span>%s</span></p>' % (n, z, k) for n, (k, z) in enumerate(FAKTEN)),
    zl(TITEL, 'h2', 'tw-h tw-mi'), satz())))

# 22 Vier Hochformate: Kante an Kante, jedes trägt eine Angabe, sie steigen nacheinander
F.append(('Vier Hochformate', '<div class="tw22"><div class="tw22-kopf">%s%s</div><div class="tw22-reihe">%s</div></div>' % (
    zl(TITEL, 'h2', 'tw-h'), satz('tw22-s'),
    ''.join('<figure class="tw22-f auf" style="--i:%d">%s<figcaption><b>%s</b><span>%s</span></figcaption></figure>' % (
        n, bild(b, 1000), z, k) for n, ((k, z), b) in enumerate(zip(FAKTEN, ['kerze2', 'toast', 't05', 'kartglas']))))))

# 23 Ein Bild, vier Bahnen: das Tafelfoto in vier Bahnen geschnitten, in jeder Bahn eine Angabe; die Bahnen gleiten versetzt an ihren Platz
F.append(('Ein Bild in vier Bahnen', '<div class="tw23">%s<div class="tw23-bahnen">%s</div>%s</div>' % (
    zl(TITEL, 'h2', 'tw-h'),
    ''.join('<div class="tw23-b auf eigen" style="--n:%d;--i:%d"><div class="tw23-bild" style="background-image:url(%s)"></div><p><b>%s</b><span>%s</span></p></div>' % (
        n, n, src('tafelleer', 1600), z, k) for n, (k, z) in enumerate(FAKTEN)),
    satz('tw23-s'))))

# 24 Bühne mit Tausch: die Fläche bleibt stehen, beim Scrollen tauscht sie Foto und Angabe, vier Schritte
BUEHNE = [('Freitags ab', '19:00', 'kerze2'), ('Samstags ab', '17:00', 'anstossen'), ('Plätze an einer Tafel', '14', 'tafelleer'), ('zuletzt, 25. und 26. September 2026, ausgebucht', EUR, 'kartglas')]
F.append(('Bühne mit Tausch', '<div class="tw24" data-tw-buehne><div class="tw24-steh"><div class="tw24-bilder">%s</div><div class="tw24-text">%s<div class="tw24-zahlen">%s</div><div class="tw24-zaehler">%s</div>%s</div></div><div class="tw24-schritte">%s</div></div>' % (
    ''.join('<figure class="tw24-f%s" data-a="%d">%s</figure>' % (' an' if n == 0 else '', n, bild(b, 1600)) for n, (_k, _z, b) in enumerate(BUEHNE)),
    zl(TITEL, 'h2', 'tw-h'),
    ''.join('<p class="tw24-z%s" data-a="%d"><b>%s</b><span>%s</span></p>' % (' an' if n == 0 else '', n, z, k) for n, (k, z, _b) in enumerate(BUEHNE)),
    ''.join('<i class="%s" data-a="%d"></i>' % ('an' if n == 0 else '', n) for n in range(4)), satz(),
    ''.join('<div class="tw24-schritt" data-s="%d"></div>' % n for n in range(4)))))

# 25 Über die Kante: zwei Paare im Zickzack, die grosse Zahl liegt halb auf dem Foto, halb daneben
F.append(('Über die Kante', '<div class="tw25">%s<div class="tw25-paar l"><figure class="tw25-f auf">%s</figure><div class="tw25-t"><p class="tw25-zahl">19:00</p><p class="tw25-k">freitags ab, samstags schon ab <b>17:00</b></p></div></div>'
          '<div class="tw25-paar r"><figure class="tw25-f auf">%s</figure><div class="tw25-t"><p class="tw25-zahl">14</p><p class="tw25-k">Plätze an einer Tafel, zuletzt <b>%s</b> für den ganzen Abend, am 25. und 26. September 2026 ausgebucht</p></div></div>%s</div>' % (
              zl(TITEL, 'h2', 'tw-h'), bild('kerze1', 1600), bild('t09', 1600), EUR, satz('tw25-s'))))

# 26 Die Preisliste: heller Grund, gesetzt wie eine gedruckte Karte, ein Foto im Rahmen daneben
F.append(('Die Preisliste, hell', '<div class="tw26"><figure class="tw26-f auf">%s</figure><div class="tw26-liste"><p class="tw-kick">Culinarium · Walk on the Wild Side</p>%s'
          '<div class="tw26-zeilen"><p><span>Freitags</span><i></i><b>ab 19:00</b></p><p><span>Samstags</span><i></i><b>ab 17:00</b></p><p><span>An einer Tafel</span><i></i><b>14 Plätze</b></p>'
          '<p><span>Der ganze Abend, Essen und Drinks</span><i></i><b>%s</b></p></div><p class="tw26-zul">Zuletzt am 25. und 26. September 2026, ausgebucht.</p>%s</div></div>' % (
              bild('karte', 1600, pos='50% 50%'), zl(TITEL, 'h2', 'tw-h'), EUR, satz())))

# 27 Wie im Kino: ein breites Bild wie eine Leinwand, darunter die Angaben als Abspann in einer Zeile; das Bild fährt im Rahmen zurück
F.append(('Wie im Kino', '<div class="tw27"><div class="tw27-kopf">%s</div><figure class="tw27-f auf eigen">%s</figure><div class="tw27-abspann">%s</div>%s</div>' % (
    zl(TITEL, 'h2', 'tw-h'), bild('kerze2', 1600, pos='50% 62%'),
    ''.join('<p><span>%s</span><b>%s</b></p>' % (k, z) for k, z in [('Freitags ab', '19:00'), ('Samstags ab', '17:00'), ('Plätze an einer Tafel', '14'), ('Zuletzt, ausgebucht', EUR)]),
    satz('tw27-s'))))

# 28 Das Band: Fotos des Abends seitwärts, dazwischen die Angaben als eigene Felder; mit Pfeilen oder Wischen
BAND = [('b', 'schildnacht'), ('t', 0), ('b', 'kerze1'), ('t', 1), ('b', 'anstossen'), ('t', 2), ('b', 't07'), ('t', 3), ('b', 'kerze2')]
F.append(('Das Band', '<div class="tw28"><div class="tw28-kopf">%s<div class="tw28-pfeile"><button type="button" data-tw-band="-1" aria-label="Zurück">‹</button><button type="button" data-tw-band="1" aria-label="Weiter">›</button></div></div>'
          '<div class="tw28-band">%s</div>%s</div>' % (
              zl(TITEL, 'h2', 'tw-h'),
              ''.join(('<figure class="tw28-f">%s</figure>' % bild(v, 1000)) if a == 'b' else
                      '<p class="tw28-t"><b>%s</b><span>%s</span></p>' % (FAKTEN[v][1], FAKTEN[v][0]) for a, v in BAND),
              satz('tw28-s'))))

# 29 Fenster: das Foto steht, eine dunkle Tafel mit den Angaben zieht darüber
F.append(('Fenster mit Tafel', '<div class="tw29"><figure class="tw29-f">%s</figure><div class="tw29-tafel">%s<div class="tw29-zeilen">%s</div>%s</div></div>' % (
    bild('tafelleer', 1600, pos='50% 50%'), zl(TITEL, 'h2', 'tw-h'),
    ''.join('<p><span>%s</span><b>%s</b></p>' % (k, z) for k, z in FAKTEN), satz())))

# 30 Schachbrett: Bildfeld und Angabe wechseln wie auf einem Schachbrett, gleich gross
BRETT = [('t', 0), ('b', 'kerze2'), ('t', 1), ('b', 'toast'), ('b', 'tafelleer'), ('t', 2), ('b', 'kartglas'), ('t', 3)]
F.append(('Schachbrett', '<div class="tw30"><div class="tw30-kopf">%s%s</div><div class="tw30-brett">%s</div></div>' % (
    zl(TITEL, 'h2', 'tw-h'), satz('tw30-s'),
    ''.join(('<figure class="tw30-f"><div class="tw30-in auf" style="--i:%d">%s</div></figure>' % (n % 4, bild(v, 1000))) if a == 'b' else
            '<p class="tw30-t"><b>%s</b><span>%s</span></p>' % (FAKTEN[v][1], FAKTEN[v][0]) for n, (a, v) in enumerate(BRETT)))))

# 31 Verstreut: Abzüge des Abends frei um den Text, ungleich gross, ohne Raster; sie wandern leicht gegeneinander
STREU = [('kerze1', 2, 4, 15, .18), ('glaeser', 79, 0, 13, -.12), ('t02', 84, 52, 12, .22), ('anstossen', 0, 56, 16, -.2), ('schaumglas', 66, 80, 10, .14), ('t11', 22, 84, 9, -.16)]
F.append(('Verstreut', '<div class="tw31">%s<div class="tw31-mitte">%s<div class="tw31-zahlen">%s</div>%s</div></div>' % (
    ''.join('<figure class="tw31-f" data-tw-drift-h="%s" style="left:%d%%;top:%d%%;width:%dvw">%s</figure>' % (d, x, y, w, bild(k, 640)) for k, x, y, w, d in STREU),
    zl(TITEL, 'h2', 'tw-h tw-mi'),
    ''.join('<p><b>%s</b><span>%s</span></p>' % (z, k) for k, z in FAKTEN[:3]) + '<p><b>%s</b><span>zuletzt, ausgebucht</span></p>' % EUR, satz())))

# 32 Flankiert: zwei hohe Bilder rahmen die Mitte und laufen an den Rand, in der Mitte die Angaben untereinander
F.append(('Flankiert', '<div class="tw32"><figure class="tw32-f l auf">%s</figure><div class="tw32-mitte">%s<div class="tw32-zeilen">%s</div>%s</div><figure class="tw32-f r auf" style="--i:2">%s</figure></div>' % (
    bild('kerze3', 1000), zl(TITEL, 'h2', 'tw-h tw-mi'),
    ''.join('<p><span>%s</span><b>%s</b></p>' % (k, z) for k, z in FAKTEN), satz(), bild('toast', 1000))))

# 33 Gross und schmal: ein grosses Foto, daneben eine schmale Spalte mit den Angaben untereinander und einem kleinen Bild am Fuss
F.append(('Gross und schmal', '<div class="tw33"><figure class="tw33-f auf eigen">%s</figure><div class="tw33-spalte">%s<div class="tw33-zeilen">%s</div><figure class="tw33-klein auf">%s</figure></div><div class="tw33-satz">%s</div></div>' % (
    bild('anstossen', 1600, pos='50% 45%'), zl(TITEL, 'h2', 'tw-h'),
    ''.join('<p class="auf" style="--i:%d"><b>%s</b><span>%s</span></p>' % (n, z, k) for n, (k, z) in enumerate(FAKTEN)), bild('kartglas', 640), satz())))

# 34 Dichtes Mosaik: Fotos des Abends dicht in ungleichen Grössen, die Angaben sitzen als Textfelder darin
MOS = [('b', 'kerze2', 'a'), ('t', 0, 'b'), ('b', 'glaeser', 'c'), ('b', 'tafelleer', 'd'), ('t', 1, 'e'), ('b', 'toast', 'f'), ('t', 2, 'g'), ('b', 'kartglas', 'h'), ('b', 't06', 'i'), ('t', 3, 'j')]
F.append(('Dichtes Mosaik', '<div class="tw34"><div class="tw34-kopf">%s%s</div><div class="tw34-feld">%s</div></div>' % (
    zl(TITEL, 'h2', 'tw-h'), satz('tw34-s'),
    ''.join(('<figure class="tw34-f auf" style="grid-area:%s;--i:%d">%s</figure>' % (g, n % 5, bild(v, 1000))) if a == 'b' else
            '<p class="tw34-t" style="grid-area:%s"><b>%s</b><span>%s</span></p>' % (g, FAKTEN[v][1], FAKTEN[v][0]) for n, (a, v, g) in enumerate(MOS)))))

# 35 Ein Satz, dann Ruhe: ein Satz gross auf dem randlosen Bild, danach eine stille Strecke mit den Angaben
F.append(('Ein Satz, dann Ruhe', '<div class="tw35"><div class="tw35-buehne"><figure class="tw35-f auf eigen">%s</figure>'
          '<p class="tw35-satz zl auf" aria-label="Vierzehn Plätze. Eine Tafel. Ein Wochenende."><span class="z"><span style="--i:0">Vierzehn Plätze.</span></span><span class="z"><span style="--i:1">Eine Tafel.</span></span><span class="z"><span style="--i:2">Ein Wochenende.</span></span></p></div>'
          '<div class="tw35-ruhe"><div>%s</div><div class="tw35-zeilen">%s%s</div></div></div>' % (
              bild('kerze2', 1600, pos='50% 55%'), zl(TITEL, 'h2', 'tw-h'),
              ''.join('<p><span>%s</span><b>%s</b></p>' % (k, z) for k, z in FAKTEN), satz())))


def main():
    seite = open(os.path.join(HIER, 'abend.html')).read()
    m = re.search(r'(<section class="termine"[^>]*>)(\s*<div class="te-buehne">.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Wann und wie viel» in abend.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="termine"', 'id="termine" data-name="Wann und wie viel" class="termine wahl"', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv tew tw-f%02d" data-n="%d" hidden><div class="tw-in">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Wann und wie viel</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Tafelfoto, vier Zahlen in einer Reihe'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('termine-wahl.css', 'termine-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["termine"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/termine-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Wann und wie viel wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/termine-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'termine-wahl.html'), 'w').write(seite)
    print('Seite termine-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
