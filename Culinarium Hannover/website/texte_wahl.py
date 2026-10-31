#!/usr/bin/env python3
"""Culinarium Hannover · Texte unter «Über Eck» (Der Abend / Das Haus) in 15 Fassungen, direkt in der echten Startseite, 26.10.2026.
Robert (Bildschirmfoto 20:50): «gib mir 15 variationsmöglichkeiten wie wir mit diesen texten umgehen können».
Die Bildwand bleibt wie sie ist, die Texte stehen weiter darunter (Robert 26.10.2026: «NICHT in die Bildsektion einarbeiten»).
Anders ist je Fassung der Umgang mit dem Text: Wortlaut, Gewicht, Satz, Ordnung, Verhältnis zur Naht.
Fakten nur aus bau.py, varianten.py und bar.html (Bar ohne Karte, Zeiten, Empore, Derya Ivkin und Momo).
Bewegung nur transform und opacity, nichts startet unsichtbar.
Baut texte-wahl.html (Leiste unten, Pfeiltasten, ?ebenen=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/texte_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, knopf, sw

HIER = bau.HIER

A = dict(et='Der Abend', ti='Culinarium',
         satz='Ein Menü mit fünf passenden Drinks an einer langen Tafel für vierzehn Gäste, an einzelnen Wochenenden.',
         info='Freitag ab 19:00 · Samstag ab 17:00 · zuletzt 89,00 EUR', kn=('Der Abend', 'abend.html', ''))
H = dict(et='Das Haus', ti='Walk on the Wild Side',
         satz='Eine Mixology-Bar ohne Karte in Linden, Haasemannstraße 13. Hier findet Culinarium statt.',
         info='Bar: Donnerstag bis Samstag ab 19 Uhr', kn=('Das Haus', 'bar.html', 'leise'))

WEITER = '<svg class="ue-weiter" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><line x1="43" y1="0" x2="37.4" y2="100"/></svg>'
PFEIL = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" '
         'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def kn(d):
    return knopf(d['kn'][0], d['kn'][1], d['kn'][2])


def mono(t):
    return '<span class="mono">%s</span>' % E(t)


def block(d, i0, et=None, ti=None, satz=None, info=None, knopf_=True, cls=''):
    """Ein Textblock wie heute, jedes Teil austauschbar (None = wie heute, '' = weglassen)."""
    teile = []
    et = d['et'] if et is None else et
    ti = E(d['ti']) if ti is None else ti
    satz = E(d['satz']) if satz is None else satz
    info = d['info'] if info is None else info
    if et: teile.append(sw(et, 'p', 'mono ue-etikett', i0))
    if ti: teile.append(sw(ti, 'h3', 'ue-titel', i0 + 1))
    if satz: teile.append(sw(satz, 'div' if satz.startswith('<dl') else 'p', 'vtext', i0 + 2))
    if info: teile.append(sw(mono(info), 'p', 'vinfo', i0 + 3))
    if knopf_: teile.append('<div class="sw auf" style="--i:%d">%s</div>' % (i0 + 3, kn(d)))
    return ''.join(teile)


def unter(links, rechts, cls='', naht=True):
    return '<div class="ue-unter %s">%s<div class="ue-text ue-tl">%s</div><div class="ue-text ue-tr">%s</div></div>' % (
        cls, WEITER if naht else '', links, rechts)


def link(t, href):
    """Textlink statt Knopf: Linie in Kerzenfarbe, wächst beim Zeigen (transform)."""
    return '<a class="tw-link" href="%s"><span>%s</span>%s</a>' % (href, E(t), PFEIL)


F = []   # (Name, Satz für Robert, HTML von ue-unter)

# 1 Weniger Worte: Titel, ein kurzer Satz, ein Textlink. Kein Etikett, keine Zeile mit Zeiten.
F.append(('Weniger Worte', 'Titel, ein kurzer Satz, ein Textlink. Etikett und Zeiten fallen weg, die stehen eine Seite weiter.', unter(
    block(A, 1, et='', satz='Ein Menü, fünf Drinks, eine Tafel für vierzehn.', info='', knopf_=False) + sw(link('Zum Abend', 'abend.html'), 'p', '', 4),
    block(H, 5, et='', satz='Die Bar ohne Karte in Linden, in der das alles passiert.', info='', knopf_=False) + sw(link('Zum Haus', 'bar.html'), 'p', '', 8),
    'tw01')))

# 2 Du: gleicher Aufbau, aber vom Gast aus erzählt, wie der Rest der Seite («Und während du trinkst …»)
F.append(('Du', 'Gleicher Aufbau, aber vom Gast aus erzählt, so wie die Seite sonst spricht («Und während du trinkst …»).', unter(
    block(A, 1, ti='Du an der langen Tafel', satz='Du sitzt mit dreizehn anderen an einem Tisch. Drei Gänge aus der Küche, fünf Drinks dazu, und Momo erklärt dir jeden.'),
    block(H, 5, ti='Du an der Theke', satz='Eine Karte gibt es hier nicht. Du erzählst, was du magst, und bekommst deinen eigenen Drink.',
          info='Haasemannstraße 13 · Donnerstag bis Samstag ab 19 Uhr'),
    'tw02')))

# 3 Ein Satz für beide: beide Texte werden ein grosser Satz über die ganze Breite, die Namen sind die Links
SATZ3 = ('<a href="abend.html">Culinarium</a> ist ein Abend mit Menü und fünf passenden Drinks an einer langen Tafel für vierzehn Gäste. '
         'Er findet im <a href="bar.html">Walk on the Wild Side</a> statt, einer Mixology-Bar ohne Karte in Linden.')
F.append(('Ein Satz für beide', 'Beide Texte werden ein grosser Satz über die ganze Breite. Die zwei Namen leuchten in Kerzenfarbe und sind die Links.',
    '<div class="ue-unter tw03">%s<div class="tw03-fuss">%s%s<div class="tw03-kn sw auf" style="--i:4">%s%s</div></div></div>' % (
        sw(SATZ3, 'p', 'tw03-satz', 1), sw(mono('Culinarium · ' + A['info']), 'p', 'vinfo', 2), sw(mono(H['info']), 'p', 'vinfo', 3), kn(A), kn(H))))

# 4 Vierzehn und Dreizehn: je eine grosse Zahl vor dem Text, 14 Plätze an der Tafel, Hausnummer 13
F.append(('Vierzehn und Dreizehn', 'Über jedem Text eine grosse Zahl in Fraunces: 14 Plätze an der Tafel, 13 die Hausnummer. Man merkt sich beides.', unter(
    sw('<b>14</b><span>Plätze an einer Tafel</span>', 'p', 'tw04-z', 1) + block(A, 2, et=''),
    sw('<b>13</b><span>Haasemannstraße, Linden</span>', 'p', 'tw04-z', 5) + block(H, 6, et='', satz='Eine Mixology-Bar ohne Karte. Hier findet Culinarium statt.'),
    'tw04')))


# 5 Steckbrief: kein Fliesstext, nur Zeilen mit Haarlinie, wie die Öffnungszeiten auf der Hausseite
def steck(zeilen):
    return '<dl class="tw05-dl">%s</dl>' % ''.join('<div><dt class="mono">%s</dt><dd>%s</dd></div>' % (E(a), E(b)) for a, b in zeilen)


F.append(('Steckbrief', 'Kein Fliesstext mehr, nur Zeilen mit feiner Linie: was, wo, wann, wie viele. Liest sich auf einen Blick.', unter(
    block(A, 1, satz=steck([('Was', 'Menü und fünf passende Drinks'), ('Wo', 'An der langen Tafel auf der Empore'),
                            ('Wann', 'Freitag ab 19:00, Samstag ab 17:00'), ('Plätze', 'Vierzehn'), ('Zuletzt', '89,00 EUR')]), info=''),
    block(H, 5, satz=steck([('Was', 'Mixology-Bar ohne Karte'), ('Wo', 'Haasemannstraße 13, Linden'),
                            ('Offen', 'Donnerstag 19 bis 1, Freitag und Samstag 19 bis 2'), ('Theke', 'Derya Ivkin und Momo')]), info=''),
    'tw05')))


# 6 Rudis Zeile: Versalien mit Schrägstrichen, so wie Rudi seine Teller schreibt
def rz(t):
    return '<span class="tw06-z">%s</span>' % E(t).replace(' / ', ' <i>/</i> ')


F.append(('Rudis Zeile', 'Statt eines Satzes eine Zeile in Versalien mit Schrägstrichen, so wie Rudi seine Teller schreibt. Weiter unten auf der Seite taucht sie wieder auf.', unter(
    block(A, 1, satz=rz('MENÜ / FÜNF DRINKS / VIERZEHN PLÄTZE')),
    block(H, 5, satz=rz('MIXOLOGY / OHNE KARTE / LINDEN'), info='Haasemannstraße 13 · Donnerstag bis Samstag ab 19 Uhr'),
    'tw06')))

# 7 Zwei Zeichen: statt der Titel in Fraunces stehen die echten Zeichen, die Culinarium-Wortmarke und das Schild der Bar
F.append(('Zwei Zeichen', 'Statt der Titel in Schrift stehen die echten Zeichen da: links die Culinarium-Wortmarke, rechts das Schild der Bar wie an der Hausecke.', unter(
    block(A, 1, ti=bau.marke('wm', 'tw07-wm')),
    '<div class="tw07-r">%s<div>%s</div></div>' % (sw(bau.zeichen_haus('ws', 'tw07-ws'), 'div', 'tw07-schild', 5), block(H, 6, ti='')),
    'tw07')))

# 8 Am Strich entlang: die Zeilen folgen der Schräge, links endet jede Zeile ein Stück früher, rechts beginnt sie ein Stück früher
F.append(('Am Strich entlang', 'Die Zeilen folgen der Schräge: links endet jede Zeile ein wenig früher, rechts beginnt sie ein wenig weiter links. Die Texte rücken an die Naht.', unter(
    '<i class="tw08-keil"></i>' + block(A, 1),
    '<i class="tw08-keil"></i>' + block(H, 5),
    'tw08')))

# 9 Satz auf der Naht: ein kurzer Satz läuft auf der Linie zwischen den Texten, die beiden Blöcke werden knapper
F.append(('Satz auf der Naht', 'Auf der Linie zwischen den Texten steht klein «hier findet Culinarium statt». Sie verbindet Abend und Haus, die Blöcke selbst werden knapper.',
    '<div class="ue-unter tw09">%s<p class="tw09-naht mono" aria-hidden="true"><span>hier findet Culinarium statt</span></p><div class="ue-text ue-tl">%s</div><div class="ue-text ue-tr">%s</div></div>' % (
        WEITER, block(A, 1, et=''), block(H, 5, et='', satz='Eine Mixology-Bar ohne Karte in Linden, Haasemannstraße 13.'))))

# 10 Namen gross: die beiden Namen so gross wie ein Abschnittstitel, alles andere klein darunter
F.append(('Namen gross', 'Die beiden Namen werden so gross wie ein Abschnittstitel, alles andere tritt klein dahinter zurück. Zeiten und Knopf in einer Reihe.', unter(
    block(A, 1, info='', knopf_=False) + '<div class="tw10-reihe sw auf" style="--i:4">%s%s</div>' % (mono(A['info']), kn(A)),
    block(H, 5, info='', knopf_=False) + '<div class="tw10-reihe sw auf" style="--i:8">%s%s</div>' % (mono(H['info']), kn(H)),
    'tw10')))


# 11 Zwei Zeilen quer: Abend und Haus als zwei lange Zeilen übereinander, wie ein Aushang
def quer(d, i0):
    return '<div class="tw11-z sw auf" style="--i:%d"><p class="mono ue-etikett">%s</p><h3 class="ue-titel">%s</h3><p class="vtext">%s</p><p class="vinfo">%s</p>%s</div>' % (
        i0, E(d['et']), E(d['ti']), E(d['satz']), mono(d['info']), kn(d))


F.append(('Zwei Zeilen quer', 'Abend und Haus stehen als zwei lange Zeilen übereinander, getrennt durch eine feine Linie, wie ein Aushang. Alles liegt auf einer Höhe.',
    '<div class="ue-unter tw11">%s%s</div>' % (quer(A, 1), quer(H, 2))))

# 12 Feuilleton: der Text in Fraunces mit Initiale in Kerzenfarbe, die Titel klein darüber, etwas mehr zu lesen
F.append(('Feuilleton', 'Der Text selbst in Fraunces mit einer Initiale in Kerzenfarbe, etwas länger, die Titel klein darüber. Liest sich wie ein Stück aus der Zeitung.', unter(
    block(A, 1, et='', ti='<span class="mono">Der Abend · Culinarium</span>',
          satz='Ein Menü mit fünf passenden Drinks an einer langen Tafel für vierzehn Gäste. Die drei Gänge kommen Teller für Teller für die ganze Tafel, und Momo erklärt am Tisch, was im Glas ist.'),
    block(H, 5, et='', ti='<span class="mono">Das Haus · Walk on the Wild Side</span>',
          satz='Eine Getränkekarte gibt es hier nicht. Wer an die Theke kommt, erzählt, was er mag, und bekommt seinen eigenen Drink. In dieser Bar in Linden, Haasemannstraße 13, findet Culinarium statt.'),
    'tw12')))

# 13 Hell, wo du hinschaust: Zeigen auf eine Bildhälfte oder einen Text lässt den anderen Text zurücktreten (nur Deckkraft)
F.append(('Hell, wo du hinschaust', 'Fährt man über die linke Bildhälfte oder den Abend-Text, tritt das Haus zurück, und umgekehrt. Bild und Text gehören sichtbar zusammen. Am Handy bleibt beides hell.',
    unter(block(A, 1), block(H, 5), 'tw13')))

# 14 Frage und Antwort: das Etikett wird eine Frage, der Text die Antwort
F.append(('Frage und Antwort', 'Statt «Der Abend» und «Das Haus» steht je eine Frage da, der Text darunter beantwortet sie. Wer neu ist, wird an die Hand genommen.', unter(
    block(A, 1, et='', ti='Was ist Culinarium?', satz='Ein Abend mit Menü und fünf passenden Drinks, an einer langen Tafel für vierzehn Gäste.'),
    block(H, 5, et='', ti='Und wo?', satz='Im Walk on the Wild Side, einer Mixology-Bar ohne Karte in Linden, Haasemannstraße 13.'),
    'tw14')))


# 15 Titel ist der Link: keine Knöpfe, der Name selbst führt weiter, eine Linie in Kerzenfarbe wächst beim Zeigen
def titellink(d):
    return '<a class="tw15-a" href="%s"><span>%s</span>%s</a>' % (d['kn'][1], E(d['ti']), PFEIL)


F.append(('Titel ist der Link', 'Keine Knöpfe mehr: der Name selbst führt weiter, mit Pfeil, und darunter wächst beim Zeigen eine Linie in Kerzenfarbe.', unter(
    block(A, 1, ti=titellink(A), knopf_=False), block(H, 5, ti=titellink(H), knopf_=False), 'tw15')))


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    m = re.search(r'(<section class="vab v-ebenen[^"]*"[^>]*id="ebenen"[^>]*>)<div class="h-ebenen ue">(<div class="ue-rahmen">.*?</div>)(<div class="ue-unter">.*?)</div></section>', seite, re.S)
    assert m, 'Teil «Über Eck» in index.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab v-ebenen', 'class="vab v-ebenen wahl', 1).replace('data-lauf', 'data-name="Texte unter Über Eck" data-lauf', 1)
    teile = ['<div class="wv h-ebenen ue" data-n="0">%s</div>' % m.group(3)]
    teile += ['<div class="wv h-ebenen ue tw" data-n="%d" hidden>%s</div>' % (i, inner) for i, (_n, _s, inner) in enumerate(F, 1)]
    neu = (kopf_tag + '<div class="wahl-marke"><b>Texte</b><span data-nr></span></div><div class="h-ebenen ue">%s</div>' % m.group(2)
           + ''.join(teile) + '</section>')
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute'] + [n for n, _s, _x in F]
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<p class="tw-satz" data-tw-satz></p>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["ebenen"],daumen:false};window.TW_SAETZE=%s;</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/texte-wahl.js?v=%s" defer></script>''' % (
        json.dumps(namen, ensure_ascii=False), json.dumps(['So steht es heute auf der Seite.'] + [s for _n, s, _x in F], ensure_ascii=False),
        VERSION, VERSION + 't')
    seite = seite.replace('<title>', '<title>Texte wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/texte-wahl.css?v=%s">\n</head>' % (VERSION, VERSION + 't'), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'texte-wahl.html'), 'w').write(seite)
    print('Seite texte-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
