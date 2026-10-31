#!/usr/bin/env python3
"""Culinarium Hannover · Öffnungszeiten «Wann die Bar offen hat.» in 15 Fassungen, direkt in der echten Bar-Seite, 27.10.2026 (zweite Runde).
Robert zur ersten Runde: «die Vorschläge sind alles scheiße … wie ist der Designstil der Seite gebaut, wie sind wir konzeptionell aufgestellt».
Diese Runde baut nur aus der Sprache der Seite (CHARAKTER.md, Website-Briefing 6 und 10): Nacht und Kerzenlicht, echte Hochformate Kante an Kante,
Fraunces leicht und nie kursiv, Zeiten und Daten in DM Mono, die dunkle Tafel aus dem Kopf der Bar, und die Bausteine des Hauses
(Paar/Anstossen, Einkerbung, Fläche, Staffel, Über Eck, Laufband, Plakatwand, Band zum Blättern, Säulen). Keine Requisiten, kein Neon, keine Kicker-Zeilen.
Nur Fotos, die auf der Bar-Seite noch nicht stehen. Fakten: Do 19–1, Fr und Sa 19–2, So bis Mi zu; Konzerte am Donnerstag, SESSION an Samstagen (Plakate).
Baut zeiten-wahl.html (Leiste unten, Pfeiltasten, ?zeiten=Nummer); Fassung 0 ist der heutige Stand. Vorige Runde: *.vor-neu-2026-10-27.
Aufruf: python3 website/zeiten_wahl.py"""
import datetime, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets/bild/meta.json')))
SATZ = 'Reservieren geht per Nachricht oder Telefon.'
OFFEN = [('do', 'Donnerstag', 1, 'Konzerte in der Bar'), ('fr', 'Freitag', 2, 'Drinks nach deinem Geschmack'),
         ('sa', 'Samstag', 2, 'An manchen Abenden SESSION, DJs an den Decks')]
MONO = 'Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr'
ZU = 'Sonntag bis Mittwoch geschlossen'


def bild(k, sizes='50vw', pos=None):
    st = META[k]['stufen']
    p, alt = bau.BILD[k][1], bau.BILD[k][2]
    s = ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in st)
    return '<img src="assets/bild/%s-%d.webp?v=%s" srcset="%s" sizes="%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        k, st[min(1, len(st) - 1)], VERSION, s, sizes, E(alt), pos or p)


def foto(k, cls='', sizes='33vw', pos=None, extra=''):
    """Foto mit dem Verhalten der Seite: deckend von unten, Zoom in den Rahmen."""
    return '<figure class="foto %s">%s%s</figure>' % (cls, bild(k, sizes, pos), extra)


def kerbe(t):
    return '<p class="aw-kerbe">%s</p>' % t


def titel(groesse='mittel', zeilen=('Wann die', 'Bar offen hat.')):
    return bau.zl(list(zeilen), 'h2', groesse)


def satz(t=SATZ, i=1, cls=''):
    return bau.sw(E(t), 'p', 'zw-satz ' + cls, i)


def mono(t=MONO, i=2, cls=''):
    return '<p class="zw-mono sw auf %s" style="--i:%d">%s</p>' % (cls, i, E(t))


def kn(i=3, cls=''):
    return '<div class="knoepfe sw auf %s" style="--i:%d">%s%s</div>' % (
        cls, i, bau.knopf('Der Weg', 'weg.html'), bau.knopf('Instagram', 'https://www.instagram.com/walkonthewildside_hannover/', 'leise'))


def liste(i=2, was=False):
    z = ''.join('<div data-tag="%s"><dt>%s%s</dt><dd>19 bis %d Uhr</dd></div>' % (
        k, t, '<small>%s</small>' % E(w) if was else '', b) for k, t, b, w in OFFEN)
    return '<div class="sw auf" style="--i:%d"><dl class="vz zw-vz">%s<div class="zu"><dt>Sonntag bis Mittwoch</dt><dd>geschlossen</dd></div></dl></div>' % (i, z)


F = []

# 1 Die Antwort zuerst: die Überschrift ist schon die Antwort, daneben drei Hochformate Kante an Kante als Fläche
F.append(('Die Antwort zuerst', '<div class="zw-in zw01"><div class="zw01-text">%s%s%s%s</div><div class="zw01-wand flaeche auf">%s%s%s</div></div>' % (
    titel('mittel', ('Donnerstag bis Samstag,', 'ab 19 Uhr.')),
    '<p class="zw-mono sw auf" style="--i:1">Donnerstag bis 1 Uhr<br>Freitag und Samstag bis 2 Uhr<br>Sonntag bis Mittwoch geschlossen</p>',
    satz(SATZ, 2), kn(3),
    foto('ws03', '', '(max-width:860px) 50vw, 20vw'), foto('ws16', '', '(max-width:860px) 50vw, 20vw'), foto('glasnacht', '', '(max-width:860px) 50vw, 20vw', '50% 55%'))))

# 2 Drei Nächte: je offener Abend ein grosses Hochformat, Tag und Zeit in der Einkerbung, darunter, was an dem Abend los ist
NB = {'do': 'ws16', 'fr': 'bar', 'sa': 'ws03'}
F.append(('Drei Nächte', '<div class="zw-in zw02"><div class="zw-kopf mitte">%s%s</div><div class="zw02-reihe staffel auf">%s</div>'
          '<div class="zw-fuss mitte">%s%s</div></div>' % (
              titel(), satz(),
              ''.join('<div class="zw02-n" data-tag="%s" style="--i:%d">%s<p class="zw02-was">%s</p></div>' % (
                  k, n, foto(NB[k], '', '(max-width:860px) 100vw, 33vw', None, kerbe('%s<br>19 bis %d Uhr' % (t, b))), E(w))
                  for n, (k, t, b, w) in enumerate(OFFEN)),
              mono(ZU, 1), kn(2))))

# 3 Ankommen bei Nacht: links die Bar von draussen gross, rechts das Schild und darunter die Zeiten als geschlossener Block
F.append(('Ankommen bei Nacht', '<div class="zw-in zw03">%s<div class="zw03-r">%s<div class="zw03-block">%s%s%s%s</div></div></div>' % (
    foto('barlicht', 'zw03-gross auf', '(max-width:860px) 100vw, 58vw'),
    foto('schildnacht', 'zw03-schild auf', '(max-width:860px) 100vw, 40vw', '50% 42%'),
    titel(), satz(), liste(2), kn(3))))

# 4 Anstossen: zwei Hälften steigen getrennt herauf und stossen an der Naht an; links der Donnerstag, rechts Freitag und Samstag
F.append(('Anstossen', '<div class="zw-in zw04"><div class="zw-kopf mitte">%s%s</div><div class="paar auf zw04-paar">%s%s</div>'
          '<div class="zw04-unter"><div data-tag="do" class="sw auf" style="--i:1"><p class="zw-mono">Donnerstag</p><p class="zw04-zeit">19 bis 1 Uhr</p><p class="zw04-was">Konzerte in der Bar</p></div>'
          '<div data-tag="fr sa" class="sw auf" style="--i:2"><p class="zw-mono">Freitag und Samstag</p><p class="zw04-zeit">19 bis 2 Uhr</p><p class="zw04-was">Samstags manchmal SESSION mit DJs</p></div></div>'
          '<div class="zw-fuss mitte">%s%s</div></div>' % (
              titel(), satz(), foto('ws19', '', '(max-width:860px) 50vw, 36vw'), foto('ws07', '', '(max-width:860px) 50vw, 36vw', '50% 60%'), mono(ZU, 1), kn(2))))

# 5 Über Eck: zwei Bildgruppen, schräg geteilt mit der Naht in Kerzenfarbe; die Naht läuft unter den Bildern weiter und trennt die Zeiten
F.append(('Über Eck', '<div class="zw-in zw05"><div class="zw-kopf">%s%s</div><div class="zw05-band flaeche auf"><div class="zw05-g l">%s%s</div><div class="zw05-g r">%s%s</div>'
          '<svg class="zw05-naht" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><line x1="53" y1="0" x2="47" y2="100"/></svg></div>'
          '<div class="zw05-unter"><div data-tag="do" class="sw auf" style="--i:1"><p class="zw-mono">Donnerstag · Konzerte</p><p class="zw05-zeit">19 bis 1 Uhr</p></div><i class="zw05-strich"></i>'
          '<div data-tag="fr sa" class="sw auf" style="--i:2"><p class="zw-mono">Freitag und Samstag</p><p class="zw05-zeit">19 bis 2 Uhr</p></div></div>'
          '<div class="zw-fuss mitte">%s%s</div></div>' % (
              titel(), satz(), foto('ws16', '', '25vw'), foto('ws15', '', '25vw'), foto('bar', '', '25vw'), foto('ws29', '', '25vw'), mono(ZU, 1), kn(2))))

# 6 Wie eine Karte: die Bar hat keine Getränkekarte, also stehen die Abende wie Zeilen einer Karte in Versalien, im Zickzack mit ihrem Bild
F.append(('Wie eine Karte', '<div class="zw-in zw06"><div class="zw-kopf">%s%s%s</div>%s<div class="zw-fuss">%s</div></div>' % (
    titel(), satz(), kn(2), ''.join(
        '<div class="zw06-z%s" data-tag="%s">%s<div class="zw06-t">%s<p class="zw-mono sw auf" style="--i:1">19 bis %d Uhr</p><p class="zw06-was sw auf" style="--i:2">%s</p></div></div>' % (
            ' um' if n % 2 else '', k, foto(b, 'auf', '(max-width:860px) 100vw, 48vw', p), bau.zl([t.upper()], 'p', 'mittel zw06-name'), bb, E(w))
        for n, ((k, t, bb, w), (b, p)) in enumerate(zip(OFFEN, [('ws19', '50% 40%'), ('ws13', '50% 45%'), ('ws05', '50% 40%')]))),
    mono(ZU, 0))))

# 7 Heute: die Antwort auf die eigentliche Frage gross und live, darunter die Woche; daneben eine Bildgruppe aus einem grossen und zwei kleinen Bildern
F.append(('Heute', '<div class="zw-in zw07"><div class="zw07-text"><p class="zw07-heute mittel sw auf" data-heute>Donnerstag<br>ab 19 Uhr wieder offen.</p>'
          '<p class="zw-satz sw auf" style="--i:1" data-heute-unter>Heute ist geschlossen.</p>%s%s</div><div class="zw07-gruppe flaeche auf">%s%s%s</div></div>' % (
              liste(2), kn(3), foto('glasnacht', 'a', '(max-width:860px) 100vw, 36vw', '50% 58%'), foto('ws13', 'b', '(max-width:860px) 50vw, 18vw'), foto('ws29', 'c', '(max-width:860px) 50vw, 18vw'))))

# 8 Die Tafel im Bildband: über die volle Breite ein Band aus Hochformaten, eines der Felder ist die dunkle Tafel mit den Zeiten
F.append(('Die Tafel im Bildband', '<div class="zw08 staffel auf">%s<div class="zw08-tafel" style="--i:1">%s%s%s%s</div>%s%s%s</div>' % (
    foto('barnacht', 'z1', '(max-width:860px) 50vw, 17vw'), titel(), satz(), liste(2), kn(3),
    foto('ws16', 'z3', '(max-width:860px) 50vw, 17vw'), foto('glasnacht', 'z4', '(max-width:860px) 50vw, 17vw', '50% 55%'), foto('ws07', 'z5', '(max-width:860px) 50vw, 17vw'))))

# 9 Laufband an der Naht: zwei Reihen Hochformate Kante an Kante, dazwischen läuft die Woche als ein Satz durch
LAUF = ''.join('<span>%s</span><i class="sl">/</i>' % E(t) for t in [
    'Donnerstag 19 bis 1 Uhr', 'Freitag 19 bis 2 Uhr', 'Samstag 19 bis 2 Uhr', 'Sonntag bis Mittwoch geschlossen', 'Haasemannstraße 13, Linden'])
F.append(('Laufband an der Naht', '<div class="zw09"><div class="zw-in zw-kopf zw09-kopf">%s<div>%s%s</div></div><div class="zw09-reihe flaeche auf">%s</div>'
          '<div class="zw09-lauf" aria-label="%s"><div class="zw09-spur" aria-hidden="true"><div>%s</div><div>%s</div></div></div><div class="zw09-reihe flaeche auf">%s</div></div>' % (
              titel(), satz(), kn(2), ''.join(foto(k, '', '20vw') for k in ['barnacht', 'ws16', 'ws13', 'ws03', 'ws19']), E(MONO + ', ' + ZU), LAUF * 2, LAUF * 2,
              ''.join(foto(k, '', '20vw') for k in ['ws29', 'ws07', 'glasnacht', 'ws15', 'schildnacht']))))

# 10 Die Plakatwand der Bar: die Plakate ihrer Abende dicht an dicht, daneben die Zeiten als geschlossener Block; ein Glanzstreif zieht einmal darüber
PL = ['ws49', 'ws37', 'ws40', 'ws42', 'ws47', 'ws50', 'ws51', 'ws52', 'ws21', 'ws39', 'ws32', 'ws48']
F.append(('Die Plakatwand der Bar', '<div class="zw-in zw10"><div class="zw10-text">%s%s%s%s</div><div class="zw10-wand flaeche auf">%s</div></div>' % (
    titel(), satz('Donnerstags spielt Musik, an manchen Samstagen legen bei SESSION DJs auf. Reservieren geht per Nachricht oder Telefon.'), liste(2), kn(3),
    ''.join(foto(k, 'zw10-p', '(max-width:860px) 33vw, 11vw') for k in PL))))

# 11 Die nächsten Abende: ein Band zum Blättern mit den nächsten offenen Abenden und ihrem Datum in der Einkerbung; es rechnet sich selbst weiter
NBB = ['ws16', 'bar', 'ws03', 'ws19', 'ws13', 'glasnacht']


def naechste(n=6, ab=datetime.date(2026, 10, 28)):
    MON = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    aus, d = [], ab
    while len(aus) < n:
        if d.weekday() in (3, 4, 5):
            k, t, b = [('do', 'Donnerstag', 1), ('fr', 'Freitag', 2), ('sa', 'Samstag', 2)][d.weekday() - 3]
            aus.append((k, t, b, '%d. %s' % (d.day, MON[d.month - 1])))
        d += datetime.timedelta(days=1)
    return aus


F.append(('Die nächsten Abende', '<div class="zw11"><div class="zw-in zw11-kopf"><div class="zw-kopf">%s%s</div><div class="zw11-r">%s<div class="zw11-pfeile"><button type="button" data-zw11="-1" aria-label="Zurück">‹</button>'
          '<button type="button" data-zw11="1" aria-label="Weiter">›</button></div></div></div><div class="zw11-band staffel auf" data-naechste>%s</div><div class="zw-in zw11-fuss"><div class="zw11-balken"><i data-balken></i></div>%s</div></div>' % (
              titel(), satz(), kn(2), ''.join('<div class="zw11-k" style="--i:%d">%s</div>' % (
                  i, foto(NBB[i], '', '(max-width:860px) 78vw, 26vw', None, kerbe('<span data-k-tag>%s</span><br><span class="zw-mono" data-k-dat>%s · 19 bis %d Uhr</span>' % (t, dat, b))))
                  for i, (k, t, b, dat) in enumerate(naechste())), mono(ZU, 0))))

# 12 Lage: eine Wand aus vier Hochformaten über die volle Breite, die helle Tafel greift von unten hinein, die Angaben gross nebeneinander
F.append(('Lage mit heller Tafel', '<div class="zw12"><div class="zw12-wand flaeche auf">%s</div><div class="zw-in"><div class="zw12-tafel sw auf" data-ton="hell">'
          '<div class="zw12-kopf">%s%s</div><dl class="zw12-z">%s<div class="zu"><dt>Sonntag bis Mittwoch</dt><dd>geschlossen</dd></div></dl>%s</div></div></div>' % (
              ''.join(foto(k, '', '25vw', p) for k, p in [('schildnacht', '50% 40%'), ('ws05', None), ('ws29', None), ('barlicht', '50% 60%')]),
              titel(), satz(), ''.join('<div data-tag="%s"><dt>%s</dt><dd>19 bis %d Uhr</dd></div>' % (k, t, b) for k, t, b, _w in OFFEN), kn(3))))

# 13 Die Einkerbung: ein einziges grosses Bild, die Zeiten sitzen in der ausgeschnittenen Ecke
F.append(('Die Einkerbung', '<div class="zw-in zw13"><div class="zw-kopf zw13-kopf">%s<div>%s%s</div></div>%s</div>' % (
    titel(), satz(), kn(2), foto('g5', 'zw13-bild auf', '(max-width:860px) 100vw, 1360px', '50% 64%',
                                 '<div class="aw-kerbe zw13-kerbe">%s<p class="zw-mono">%s</p></div>' % (
                                     ''.join('<p data-tag="%s"><span>%s</span><b>19 bis %d Uhr</b></p>' % (k, t, b) for k, t, b, _w in OFFEN), ZU)))))

# 14 Zwei Säulen: links und rechts läuft je eine Säule aus Bildern gegeneinander, in der Mitte steht die Tafel mit den Zeiten
S1 = ['ws16', 'barnacht', 'ws29', 'ws03']
S2 = ['glasnacht', 'ws19', 'ws13', 'ws07']
F.append(('Zwei Säulen', '<div class="zw-in zw14 auf"><div class="zw14-s hoch"><div class="zw14-spur">%s%s</div></div><div class="zw14-tafel">%s%s%s%s</div>'
          '<div class="zw14-s runter"><div class="zw14-spur">%s%s</div></div></div>' % (
              ''.join(foto(k, '', '22vw') for k in S1), ''.join(foto(k, '', '22vw') for k in S1),
              titel(), satz(), liste(2), kn(3), ''.join(foto(k, '', '22vw') for k in S2), ''.join(foto(k, '', '22vw') for k in S2))))

# 15 Ziegelverband: vier Bilder im Verband als eine Gruppe, daneben die Zeiten als geschlossener Block an der Unterkante
F.append(('Ziegelverband', '<div class="zw-in zw15"><div class="zw15-gruppe flaeche auf">%s%s%s%s</div><div class="zw15-text">%s%s%s%s</div></div>' % (
    foto('barlicht', 'a', '(max-width:860px) 50vw, 24vw', '50% 55%'), foto('ws07', 'b', '(max-width:860px) 50vw, 24vw'),
    foto('ws15', 'c', '(max-width:860px) 50vw, 24vw'), foto('glasnacht', 'd', '(max-width:860px) 50vw, 24vw', '50% 55%'),
    titel(), satz(), liste(2, True), kn(3))))


def main():
    seite = open(os.path.join(HIER, 'bar.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="vab bar-ab v-bar-zeiten[^"]*"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, 'Öffnungszeiten in bar.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('<section class="vab', '<section id="zeiten" data-name="Öffnungszeiten" class="wahl vab', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv zw zw-f%02d" data-n="%d" hidden>%s</div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Öffnungszeiten</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Foto mit heller Karte'] + [n for n, _x in F]
    v = VERSION + 'z%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('zeiten-wahl.css', 'zeiten-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["zeiten"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/zeiten-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    seite = seite.replace('<title>', '<title>Öffnungszeiten wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/zeiten-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'zeiten-wahl.html'), 'w', encoding='utf-8').write(seite)
    print('Seite zeiten-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
