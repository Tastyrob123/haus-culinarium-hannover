#!/usr/bin/env python3
"""Culinarium Hannover · «So läuft ein Abend» in 15 kompakten Fassungen, direkt in der echten Startseite, 26.10.2026.
Robert (nach der edlen Runde): «es muss zum stil der seite passen, es muss auf einen schnellen blick alles widerspiegeln,
ohne dass man grossartig scrollen muss, nichts unübersichtlich, und es soll nicht mehrere abschnitte einnehmen».
Also: jede Fassung passt in einen Bildschirm, alle vier Schritte sind auf einmal zu sehen, gebaut aus den Bausteinen der Seite
(Foto mit runder Ecke, Orange-Linie über dem Titel, Fraunces, Mono-Etikett, römische Ziffer, Menükarte, ×).
Baut ablauf-wahl-seite.html (Leiste unten, Pfeiltasten, ?ablauf=Nummer); Fassung 0 ist der heutige Stand.
Die edle Runde liegt in _alt/ablauf_wahl.edel-2026-10-26.py.
Aufruf: python3 website/bau.py && python3 website/ablauf_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, knopf

HIER = bau.HIER

# Nummer, Titel, Satz
S = [
    ('I', 'Ankommen', 'Zur Begrüssung ein Aperitif. Die Tafel ist gedeckt, die Kerzen brennen.'),
    ('II', 'Drei Gänge', 'Aus der Küche, Teller für Teller für die ganze Tafel. Das Menü wechselt jeden Abend.'),
    ('III', 'Fünf Drinks', 'Fünf Signature Drinks von Momo, gemacht für genau dieses Essen.'),
    ('IV', 'Tasting und Schulung', 'Momo erklärt jeden Drink am Tisch, damit man die Aromen auch versteht.'),
]
BILD = ['g2', 'r09', 'm7', 'kerze2']
POS = {'kerze2': '50% 35%'}
WORT = ['Aperitif', 'Drei Gänge', 'Fünf Drinks', 'Tasting']


def f(k, cls='', pos=None, w=1000):
    """Foto im Stil der Seite (runde Ecke, Schatten), sichtbar von Anfang an."""
    pos = pos or POS.get(k)
    return '<figure class="foto %s"><img src="assets/bild/%s-%d.webp?v=%s" alt="" loading="lazy" decoding="async"%s></figure>' % (
        cls, k, w, VERSION, ' style="object-position:%s"' % pos if pos else '')


def kopf(cls='', satz=True, extra=''):
    return ('<div class="kb-kopf %s"><p class="mono kb-kicker">Culinarium · Der Ablauf</p><h2 class="kb-h">So läuft ein Abend.</h2>%s%s</div>'
            % (cls, '<p class="kb-in">Wer zum ersten Mal kommt, weiss nicht, was ihn erwartet. Ungefähr so:</p>' if satz else '', extra))


def st(i, cls='', nr=True):
    n, t, s = S[i]
    return '<div class="kb-st %s">%s<h3 class="kb-t">%s</h3><p class="kb-s">%s</p></div>' % (
        cls, '<span class="kb-nr">%s</span>' % n if nr else '', E(t), E(s))


def alle(fn):
    return ''.join(fn(i) for i in range(4))


F = []  # (Name, Inhalt)

# 1 Kopf links, vier rechts: der Titel steht neben der Reihe, alles in einer Höhe
F.append(('Kopf links, vier rechts', '<div class="kb-01">%s<div class="kb-01-r">%s</div></div>' % (
    kopf(), alle(lambda i: '<div>%s%s</div>' % (f(BILD[i]), st(i))))))

# 2 Ein Bild, vier Spalten: die gedeckte Tafel quer, darunter die vier Schritte nebeneinander
F.append(('Ein Bild, vier Spalten', '%s%s<div class="kb-02-r">%s</div>' % (
    kopf('mitte'), f('tafelleer', 'kb-02-b', '50% 60%', 1600), alle(st))))

# 3 Wie «Das erste Glas»: grosses Bild mit Titel, daneben vier Zeilen mit runden Bildern
F.append(('Wie «Das erste Glas»', '<div class="kb-03"><div class="kb-03-l">%s<div class="kb-03-titel"><h2 class="kb-h">So läuft ein Abend.</h2><p class="kb-in">Wer zum ersten Mal kommt, weiss nicht, was ihn erwartet. Ungefähr so:</p></div></div><div class="kb-03-r">%s</div></div>' % (
    f('t02', '', '50% 40%'), alle(lambda i: '<div class="kb-03-z">%s%s</div>' % (f(BILD[i], 'rund'), st(i))))))

# 4 Zwei mal zwei: Titel links, vier Bilder rechts, der Schritt steht im Bild
F.append(('Zwei mal zwei', '<div class="kb-04">%s<div class="kb-04-r">%s</div></div>' % (
    kopf(extra='<div class="kb-knopf">%s</div>' % knopf('Der Abend', 'abend.html')),
    alle(lambda i: '<div class="kb-04-z">%s<div class="kb-04-t"><span class="kb-nr">%s</span><h3 class="kb-t">%s</h3></div></div>' % (f(BILD[i]), S[i][0], E(S[i][1]))))))

# 5 Die Menükarte: der Ablauf auf der Karte des Hauses, links und rechts je zwei Bilder
F.append(('Die Menükarte', '<div class="kb-05"><div class="kb-05-s">%s%s</div><div class="kb-05-k"><p class="kb-05-kopf">So läuft ein Abend</p>%s<p class="kb-05-fuss">A unique experience</p></div><div class="kb-05-s">%s%s</div></div>' % (
    f(BILD[0]), f(BILD[1]), alle(lambda i: '<div class="kb-05-g"><span class="kb-nr">%s</span><h3>%s</h3><p>%s</p></div>' % (S[i][0], E(S[i][1]), E(S[i][2]))), f(BILD[2]), f(BILD[3]))))

# 6 Die Zahlen: 1 · 3 · 5 · 1 wie die Zahlen im Teil darüber, je über einem Bild
ZAHL = [('1', 'Aperitif'), ('3', 'Gänge'), ('5', 'Drinks'), ('1', 'Tasting')]
F.append(('Die Zahlen', '%s<div class="kb-06">%s</div>' % (kopf('mitte', False), alle(
    lambda i: '<div>%s<div class="kb-06-z"><b>%s</b><span>%s</span></div><p class="kb-s">%s</p></div>' % (f(BILD[i]), ZAHL[i][0], ZAHL[i][1], E(S[i][2]))))))

# 7 Kante an Kante: vier Bilder ohne Fuge über die ganze Breite, der Text liegt auf einer dunklen Platte im Bild
F.append(('Kante an Kante', '%s<div class="kb-07">%s</div>' % (kopf('mitte', False), alle(
    lambda i: '<div class="kb-07-z">%s<div class="kb-07-p">%s</div></div>' % (f(BILD[i]), st(i))))))

# 8 Die Kerzenlinie: eine Linie durch den Abend, Bilder im Wechsel darüber und darunter
F.append(('Die Kerzenlinie', '%s<div class="kb-08"><div class="kb-08-l"></div>%s</div>' % (kopf('mitte', False), alle(
    lambda i: '<div class="kb-08-z %s">%s<span class="kb-08-nr">%s</span>%s</div>' % ('oben' if i % 2 == 0 else 'unten', f(BILD[i]), S[i][0], st(i, '', False))))))

# 9 Teller × Glas: das Paar in der Mitte stösst an, so wie Essen und Drink zusammengehören
F.append(('Teller × Glas', '%s<div class="kb-09 auf"><div class="kb-09-e">%s%s</div><div class="kb-09-paar"><div>%s%s</div><span class="kb-09-x">×</span><div>%s%s</div></div><div class="kb-09-e">%s%s</div></div>' % (
    kopf('mitte', False), f(BILD[0]), st(0), f(BILD[1]), st(1), f(BILD[2]), st(2), f(BILD[3]), st(3))))

# 10 Rudis Zeile: der Ablauf als eine Zeile in Versalien, wie Rudi seine Teller schreibt, unter jedem Wort sein Bild
F.append(('Rudis Zeile', '%s<div class="kb-10">%s</div>' % (kopf('mitte', False), ''.join(
    '<div><p class="kb-10-w">%s%s</p>%s<p class="kb-s">%s</p></div>' % (E(WORT[i]), '<i>/</i>' if i < 3 else '', f(BILD[i]), E(S[i][2])) for i in range(4)))))

# 11 Vier Karten auf dem Bild: ein breites Bild der Tafel, vier helle Karten liegen auf seiner Kante
F.append(('Vier Karten auf dem Bild', '%s<div class="kb-11">%s<div class="kb-11-r">%s</div></div>' % (
    kopf('mitte', False), f('tafelleer', 'kb-11-b', '50% 62%', 1600), alle(st))))

# 12 Um die Mitte: vier Bilder aussen, die Sätze innen jeweils an ihrem Bild
F.append(('Um die Mitte', '%s<div class="kb-12">%s%s%s%s%s%s%s%s</div>' % (
    kopf('mitte', False), f(BILD[0]), st(0, 'rechts'), st(1), f(BILD[1]), f(BILD[2]), st(2, 'rechts'), st(3), f(BILD[3]))))

# 13 Schachbrett-Streifen: Bild und helles Textfeld im Wechsel, zwei Reihen
F.append(('Schachbrett-Streifen', '%s<div class="kb-13">%s%s%s%s%s%s%s%s</div>' % (
    kopf('mitte', False), f(BILD[0]), st(0, 'hell'), f(BILD[1]), st(1, 'hell'), st(2, 'hell'), f(BILD[2]), st(3, 'hell'), f(BILD[3]))))

# 14 Bild wechselt, Text bleibt: alle vier Schritte stehen da, Zeigen holt das passende Bild
F.append(('Bild wechselt, Text bleibt', '<div class="kb-14" data-kb-wechsel><div class="kb-14-b">%s</div><div class="kb-14-r">%s<div class="kb-14-l">%s</div></div></div>' % (
    ''.join('<img%s src="assets/bild/%s-1000.webp?v=%s" alt="" loading="lazy"%s>' % (' class="an"' if i == 0 else '', k, VERSION, ' style="object-position:%s"' % POS[k] if k in POS else '') for i, k in enumerate(BILD)),
    kopf('', False), ''.join(st(i, 'an' if i == 0 else '').replace('<div class="kb-st', '<div data-i="%d" class="kb-st' % i, 1) for i in range(4)))))

# 15 Bild und Satz: vier Paare aus quadratischem Bild und Text, zwei mal zwei
F.append(('Bild und Satz', '%s<div class="kb-15">%s</div>' % (kopf('mitte', False), alle(
    lambda i: '<div class="kb-15-z">%s%s</div>' % (f(BILD[i]), st(i))))))


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    m = re.search(r'(<section class="vab v-ablauf[^"]*"[^>]*id="ablauf"[^>]*>)(<div class="vi h-ablauf">.*?)(<p class="ueber[^>]*>.*?</p></section>)', seite, re.S)
    assert m, 'Teil «So läuft ein Abend» in index.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab v-ablauf', 'class="vab v-ablauf wahl', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    # .auf: die Fotos steigen wie überall auf der Seite von unten in ihren Platz (Seiten-CSS .foto / .da)
    teile += ['<div class="wv kb kb-f%02d" data-n="%d" hidden><div class="auf">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>So läuft ein Abend</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Treppe aus vier Karten'] + [n for n, _x in F]
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["ablauf"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/ablauf-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, VERSION + 'k%d' % os.path.getmtime(os.path.join(HIER, 'assets', 'ablauf-wahl.css')))
    seite = seite.replace('<title>', '<title>Ablauf wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/ablauf-wahl.css?v=%s">\n</head>' % (VERSION, VERSION + 'k%d' % os.path.getmtime(os.path.join(HIER, 'assets', 'ablauf-wahl.css'))), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'ablauf-wahl-seite.html'), 'w').write(seite)
    print('Seite ablauf-wahl-seite.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
