#!/usr/bin/env python3
"""Culinarium Hannover · «Drei Leute, ein Haus.» in 20 Fassungen, direkt in der echten Teamseite, 27.10.2026 (zweite Runde).
Robert schickte den heutigen Stand (drei helle Karten mit runden Köpfen) und will «20 visuelle Alternativen, um diesen Abschnitt darzustellen».
Die erste Runde (team_wahl.py, die Mannschaft im Bild) ist abgelehnt; es bleiben die drei. Jede Fassung zeigt Derya, Momo und Rudi mit
den Texten von heute, gross im Hochformat (w3, momo_hoch, w4; CHARAKTER.md 5), dazu Fotos aus ihrem Teil des Hauses: Bar und Haus, Glas, Teller.
Gesichter werden nie gerahmt, eingekreist oder heller gesetzt. Ein eigener Moment je Fassung, nur transform und opacity, nativer Scroll.
Keine Bilder, die auf leute.html sonst schon stehen (Hero, Arbeit, Chronik, Schluss).
Baut team-wahl-2.html (Pfeiltasten, ?team=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/team_wahl2.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets/bild/meta.json')))

TITEL = ('Drei Leute,', 'ein Haus.')
SATZ = 'Wer an einem Abend hinter der Theke, in der Küche und an der Tafel steht.'

# Texte wörtlich wie heute (varianten.py, personen); Bild: Hochformat, Ausschnitt, Kopf; A: Fotos aus ihrem Teil des Hauses, ohne Gesichter
P = [dict(h='w3', hp='40% 30%', kopf='kopf_derya', was='Führt die Bar', name='Derya Ivkin', vor='Derya', tut='führt die Bar', wort='BAR', ig='derrisch__',
          text='Führt das Walk on the Wild Side, das Haus von Culinarium, seit dem Reopening im November 2023. Wer an die Theke kommt, bekommt einen Drink nach seinem Geschmack.',
          seit='November 2023', seit_was='Das Reopening',
          A=['barneg', 'fassade', 'ecke', 'barlicht', 'ws13', 'flaschen', 'kanister']),
     dict(h='momo_hoch', hp='50% 22%', kopf='kopf_momo', was='Mixt die Drinks', name='Momo', vor='Momo', tut='mixt die Drinks', wort='DRINKS', ig='momo012027',
          text='Steht hinter der Bar und mixt die Signature Drinks, auch die fünf eines Culinarium-Abends, und erklärt jeden selbst. Das erste Pop-up gab es am 20. Mai 2023.',
          seit='20. Mai 2023', seit_was='Das erste Pop-up',
          A=['glasnacht', 'g1', 'schaum', 'd3', 'ws29', 'g5', 'schaumglas']),
     dict(h='w4', hp='74% 30%', kopf='kopf_rudi', was='Kocht die Gänge', name='Rudi Napieraj', vor='Rudi', tut='kocht die Gänge', wort='GÄNGE', ig='rudi__san',
          text='Kocht seit 2024 bei Culinarium, drei Gänge an der langen Tafel, und steht beim Pop-up Dirty Chicken in der Küche.',
          seit='2024', seit_was='Bei Culinarium',
          A=['roq1', 'hok1', 'beete', 'pass3', 'm8', 'r01', 'm2'])]


def srcset(k):
    return ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in META[k]['stufen'])


def img(k, sizes='33vw', pos=None, cls=''):
    st = META[k]['stufen']
    p = pos or next((x['hp'] for x in P if x['h'] == k), None) or bau.BILD[k][1]
    return '<img%s src="assets/bild/%s-%d.webp?v=%s" srcset="%s" sizes="%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        ' class="%s"' % cls if cls else '', k, st[min(1, len(st) - 1)], VERSION, srcset(k), sizes, E(bau.BILD[k][2]), p)


def foto(k, cls='', sizes='33vw', pos=None, extra=''):
    """Foto mit dem Verhalten der Seite: deckend, kommt von unten, zoomt in den Rahmen."""
    return '<figure class="foto%s" style="--lq:url(%s)">%s%s</figure>' % ((' ' + cls) if cls else '', META[k]['lq'], img(k, sizes, pos), extra)


def kopf(cls='mitte', satz=SATZ, titel=TITEL):
    return '<div class="vk %s">%s%s</div>' % (cls, bau.zl(list(titel), 'h2', 'titel'), bau.sw(E(satz), 'p', 'vtext', 1) if satz else '')


def kopf_z():
    """Kopf als Zeile wie auf den anderen Seiten: Titel links, Satz rechts unten."""
    return '<div class="t2-kopfz">%s%s</div>' % (bau.zl(list(TITEL), 'h2', 'titel'), bau.sw(E(SATZ), 'p', 'vtext', 1))


def ig(p, cls=''):
    return '<a class="t2-ig %s" href="https://www.instagram.com/%s/" target="_blank" rel="noopener">@%s</a>' % (cls, p['ig'], E(p['ig']))


def text(i, cls='', name=True, was=True, tag='div'):
    p = P[i]
    return '<%s class="t2-p %s sw auf" style="--i:%d">%s%s<p class="t2-text">%s</p>%s</%s>' % (
        tag, cls, i, '<p class="mono t2-was">%s</p>' % E(p['was']) if was else '', '<h3 class="t2-name">%s</h3>' % E(p['name']) if name else '',
        E(p['text']), ig(p), tag)


def drei(f):
    return ''.join(f(i, p) for i, p in enumerate(P))


F = []  # (Name, Inhalt)

# 1 Randlos: die drei Hochformate über die ganze Breite Kante an Kante, Rolle und Name stehen im Bild; darunter ein Streifen aus ihrem Teil des Hauses
F.append(('Randlos, Name im Bild', '<div class="t2-01"><div class="vi">%s</div><div class="t2-01-drei flaeche auf">%s</div><div class="t2-01-streifen flaeche auf">%s</div>'
          '<div class="vi"><div class="t2-01-texte">%s</div></div></div>' % (
              kopf(),
              drei(lambda i, p: foto(p['h'], '', '(max-width:860px) 100vw, 34vw', None,
                                     '<figcaption class="t2-01-im"><span class="mono">%s</span><b>%s</b></figcaption>' % (E(p['was']), E(p['name'])))),
              ''.join(foto(P[i]['A'][j], '', '(max-width:860px) 33vw, 17vw') for i in range(3) for j in (0, 1)),
              drei(lambda i, p: text(i, name=False, was=False)))))

# 2 Drei Paare: sechs Hochformate in einer Reihe, je Person ihr Bild und ihr Gegenstand; die beiden Hälften stossen an der Naht an
GEG = ['barneg', 'glasnacht', 'roq1']
F.append(('Drei Paare, die anstossen', '<div class="t2-02">%s<div class="t2-02-reihe">%s</div></div>' % (
    kopf(), drei(lambda i, p: '<div class="t2-02-platz"><div class="t2-02-paar auf"><div class="t2-02-h">%s</div><div class="t2-02-h">%s</div></div>%s</div>' % (
        foto(p['h'], '', '(max-width:860px) 50vw, 16vw'), foto(GEG[i], '', '(max-width:860px) 50vw, 16vw'), text(i, 't2-02-t'))))))

# 3 Zickzack: je Person eine Zeile, Bildgruppe aus Hochformat und zwei Fotos, die Seite wechselt; die Bildgruppe schiebt sich von ihrer Seite herein
F.append(('Zickzack', '<div class="t2-03">%s%s</div>' % (
    kopf_z(), drei(lambda i, p: '<div class="t2-03-z%s"><div class="t2-03-bilder auf">%s<div class="t2-03-zwei">%s%s</div></div>%s</div>' % (
        ' um' if i % 2 else '', foto(p['h'], 't2-03-gross', '(max-width:860px) 60vw, 34vw'),
        foto(p['A'][2], '', '(max-width:860px) 40vw, 20vw'), foto(p['A'][3], '', '(max-width:860px) 40vw, 20vw'), text(i, 't2-03-t'))))))

# 4 Die Bühne: links die drei Namen gross untereinander, rechts die Bühne; wer über einen Namen fährt oder ihn antippt, holt ihn auf die Bühne
F.append(('Namen holen auf die Bühne', '<div class="t2-04" data-t2-buehne>%s<div class="t2-04-raster"><div class="t2-04-l">%s<div class="t2-04-texte">%s</div></div>'
          '<div class="t2-04-buehne flaeche auf"><div class="t2-04-stapel gross">%s</div><div class="t2-04-zwei"><div class="t2-04-stapel">%s</div><div class="t2-04-stapel">%s</div></div></div></div></div>' % (
              kopf_z(),
              drei(lambda i, p: '<button type="button" class="t2-04-n%s" data-i="%d"><span class="mono">%s</span><span class="t2-04-name">%s</span></button>' % (
                  ' an' if i == 0 else '', i, E(p['was']), E(p['name']))),
              drei(lambda i, p: '<div class="t2-04-text%s" data-i="%d"><p class="t2-text">%s</p>%s</div>' % (' an' if i == 0 else '', i, E(p['text']), ig(p))),
              drei(lambda i, p: '<figure class="%s" data-i="%d">%s</figure>' % ('an' if i == 0 else '', i, img(p['h'], '(max-width:860px) 60vw, 32vw'))),
              drei(lambda i, p: '<figure class="%s" data-i="%d">%s</figure>' % ('an' if i == 0 else '', i, img(p['A'][0], '(max-width:860px) 40vw, 20vw'))),
              drei(lambda i, p: '<figure class="%s" data-i="%d">%s</figure>' % ('an' if i == 0 else '', i, img(p['A'][5], '(max-width:860px) 40vw, 20vw'))))))

# 5 Band zum Blättern: ein Band aus Hochformaten, je Person ihr Bild, eine dunkle Tafel mit dem Text und zwei Fotos; Wischen oder Pfeile
F.append(('Band zum Blättern', '<div class="t2-05"><div class="t2-05-kopf">%s<div class="t2-05-pfeile"><button type="button" data-t2-band="-1" aria-label="Zurück">‹</button>'
          '<button type="button" data-t2-band="1" aria-label="Weiter">›</button></div></div><div class="t2-05-band staffel auf" data-t2-bahn>%s</div></div>' % (
              kopf(''), drei(lambda i, p: '%s<div class="t2-05-tafel" data-ton="nacht">%s</div>%s%s' % (
                  foto(p['h'], 't2-05-k', '(max-width:860px) 70vw, 30vw'), text(i, ''),
                  foto(p['A'][1], 't2-05-k', '(max-width:860px) 70vw, 30vw'), foto(p['A'][5], 't2-05-k', '(max-width:860px) 70vw, 30vw'))))))

# 6 Die Bühne bleibt stehen: links steht das Hochformat still, rechts scrollen die drei vorbei; wer gerade dran ist, steht auf der Bühne
F.append(('Bühne beim Scrollen', '<div class="t2-06" data-t2-still>%s<div class="t2-06-raster"><div class="t2-06-buehne">%s</div><div class="t2-06-r">%s</div></div></div>' % (
    kopf(),
    drei(lambda i, p: '<figure class="%s" data-i="%d">%s</figure>' % ('an' if i == 0 else '', i, img(p['h'], '(max-width:860px) 100vw, 46vw'))),
    drei(lambda i, p: '<div class="t2-06-b" data-i="%d">%s%s<div class="t2-06-zwei flaeche auf">%s%s</div></div>' % (
        i, foto(p['h'], 't2-06-mobil', '100vw'), text(i, 't2-06-t'),
        foto(p['A'][2], '', '(max-width:860px) 50vw, 22vw'), foto(p['A'][6], '', '(max-width:860px) 50vw, 22vw'))))))


# 7 Über Eck: die drei in einem Band, schräg geteilt, die Nähte in Kerze; darunter ein zweites Band aus ihrem Teil des Hauses, die Nähte laufen weiter
def eck(ks, cls, sizes):
    return ('<div class="t2-07-band %s">%s<svg class="t2-07-naht" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
            '<line x1="36" y1="0" x2="30" y2="100"/><line x1="69" y1="0" x2="63" y2="100"/></svg></div>') % (
        cls, ''.join('<div class="t2-07-s s%d">%s</div>' % (n, foto(k, '', sizes)) for n, k in enumerate(ks)))


F.append(('Über Eck', '<div class="t2-07">%s<div class="t2-07-ganz auf">%s%s</div><div class="t2-07-texte">%s</div></div>' % (
    kopf(), eck([p['h'] for p in P], 'hoch', '(max-width:860px) 100vw, 40vw'), eck([p['A'][3] for p in P], 'flach', '40vw'),
    drei(lambda i, p: text(i)))))

# 8 Die dunkle Tafel: die drei Hochformate stehen auf der Kante der dunklen Tafel, darin die Texte und ein Bildstreifen; die Tafel kommt von unten herauf
F.append(('Die dunkle Tafel', '<div class="t2-08 auf">%s<div class="t2-08-koepfe staffel">%s</div><div class="t2-08-tafel" data-ton="nacht"><div class="t2-08-texte">%s</div>'
          '<div class="t2-08-streifen">%s</div></div></div>' % (
              kopf(), drei(lambda i, p: '<div style="--i:%d">%s</div>' % (i, foto(p['h'], '', '(max-width:860px) 100vw, 30vw'))),
              drei(lambda i, p: text(i)), ''.join(foto(P[i]['A'][j], '', '(max-width:860px) 33vw, 15vw') for i in range(3) for j in (1, 4)))))

# 9 An der Theke entlang: ein langer Zug aus Bildern, jede Person zwischen zwei Fotos aus ihrem Teil; beim Scrollen geht man die Theke entlang
F.append(('An der Theke entlang', '<div class="t2-09"><div class="vi">%s</div><div class="t2-09-fenster" data-t2-zug><div class="t2-09-spur flaeche auf">%s</div></div></div>' % (
    kopf_z(), drei(lambda i, p: '%s%s%s<div class="t2-09-t" style="grid-column:%d / span 3">%s</div>' % (
        foto(p['A'][0], 't2-09-a', '(max-width:860px) 40vw, 14vw'), foto(p['h'], 't2-09-p', '(max-width:860px) 60vw, 22vw'),
        foto(p['A'][2], 't2-09-a', '(max-width:860px) 40vw, 14vw'), 3 * i + 1, text(i))))))

# 10 Ein Satz: der Abschnitt als ein grosser Satz, die Bilder stehen mitten in der Zeile, wer und was er tut; darunter die drei Texte
IN = ['barneg', 'glasnacht', 'roq1']
F.append(('Ein Satz mit Bildern', '<div class="t2-10"><h2 class="t2-10-satz auf" aria-label="%s">%s</h2>%s<div class="t2-10-texte">%s</div></div>' % (
    E(', '.join('%s %s' % (p['vor'], p['tut']) for p in P) + '.'),
    ', '.join('%s <span class="t2-10-b k" style="--i:%d">%s</span> %s <span class="t2-10-b g" style="--i:%d">%s</span>' % (
        E(p['vor']), 2 * i, img(p['h'], '120px'), E(p['tut']), 2 * i + 1, img(IN[i], '160px')) for i, p in enumerate(P)) + '.',
    bau.sw(E(SATZ), 'p', 'vtext t2-10-unter', 1), drei(lambda i, p: text(i)))))

# 11 BAR / DRINKS / GÄNGE: die Überschrift in Rudis Zeilen, darunter steht unter jedem Wort seine Person mit zwei Fotos aus ihrem Teil
F.append(('BAR / DRINKS / GÄNGE', '<div class="t2-11"><div class="t2-11-kopf">%s%s</div><div class="t2-11-reihe staffel auf">%s</div></div>' % (
    bau.zl([' / '.join(p['wort'] for p in P)], 'h2', 'rudi t2-11-h'), bau.sw(E('Drei Leute, ein Haus. ' + SATZ), 'p', 'vtext', 1),
    drei(lambda i, p: '<div class="t2-11-s" style="--i:%d">%s<div class="t2-11-zwei">%s%s</div>%s</div>' % (
        i, foto(p['h'], 't2-11-gross', '(max-width:860px) 100vw, 30vw'),
        foto(p['A'][1], '', '(max-width:860px) 50vw, 15vw'), foto(p['A'][3], '', '(max-width:860px) 50vw, 15vw'), text(i))))))

# 12 Was sie tun, gross: je Person ihr Gegenstand im grossen Hochformat, sie selbst sitzt in der ausgeschnittenen Ecke; die Ecke steigt aus der Kante
WERK = ['barlicht', 'schaum', 'hok1']
F.append(('Was sie tun, in der Einkerbung', '<div class="t2-12">%s<div class="t2-12-reihe staffel auf">%s</div><div class="t2-12-texte">%s</div></div>' % (
    kopf(), drei(lambda i, p: '<div style="--i:%d">%s</div>' % (i, foto(WERK[i], 't2-12-bild', '(max-width:860px) 100vw, 32vw', None,
                                                                   '<div class="aw-kerbe t2-12-kerbe"><span class="t2-12-kopf">%s</span><span><span class="mono">%s</span><b>%s</b></span></div>' % (
                                                                       img(p['kopf'], '96px', '50% 40%'), E(p['was']), E(p['name']))))),
    drei(lambda i, p: text(i, name=False, was=False)))))

# 13 Seit wann: eine Zeitleiste über die Breite, die Kerzenlinie zieht von Mai 2023 bis 2024; an jedem Datum steht, wer seitdem dabei ist
ORD = [1, 0, 2]
F.append(('Seit wann', '<div class="t2-13">%s<div class="t2-13-leiste auf"><i class="t2-13-linie"></i><div class="t2-13-reihe">%s</div></div></div>' % (
    kopf(), ''.join('<div class="t2-13-s"><p class="t2-13-dat">%s</p><p class="mono t2-13-was">%s</p><div class="t2-13-paar flaeche">%s%s</div>%s</div>' % (
        E(P[i]['seit']), E(P[i]['seit_was']), foto(P[i]['h'], '', '(max-width:860px) 60vw, 20vw'), foto(P[i]['A'][5], '', '(max-width:860px) 40vw, 12vw'), text(i))
        for i in ORD))))

# 14 Drei Plakate: wie die Plakate der Abende, je Person ein dunkles Plakat mit Name, Bild und zwei Fotos; ein Glanzstreif zieht einmal darüber
F.append(('Drei Plakate', '<div class="t2-14">%s<div class="t2-14-reihe staffel auf">%s</div></div>' % (
    kopf(), drei(lambda i, p: '<div class="t2-14-s" style="--i:%d"><div class="t2-14-plakat" data-ton="nacht"><p class="mono">%s</p><h3>%s</h3>%s<div class="t2-14-zwei">%s%s</div>'
                 '<p class="mono t2-14-fuss">@%s</p></div><p class="t2-text">%s</p></div>' % (
                     i, E(p['was']), E(p['name']), foto(p['h'], 't2-14-bild', '(max-width:860px) 100vw, 28vw'),
                     foto(p['A'][0], '', '(max-width:860px) 50vw, 14vw'), foto(p['A'][6], '', '(max-width:860px) 50vw, 14vw'), E(p['ig']), E(p['text']))))))

# 15 Laufband an der Naht: oben die drei Kante an Kante mit ihren Texten, dazwischen laufen Namen und Rollen durch, unten sechs Fotos aus ihrem Teil
LAUF = ''.join('<span>%s</span><i class="sl">/</i><span class="mono">%s</span><i class="sl">/</i>' % (E(p['name']), E(p['was'])) for p in P)
F.append(('Laufband an der Naht', '<div class="t2-15">%s<div class="t2-15-oben flaeche auf">%s</div><div class="t2-15-texte">%s</div>'
          '<div class="t2-15-lauf" aria-hidden="true"><div class="t2-15-spur"><div>%s</div><div>%s</div></div></div><div class="t2-15-unten flaeche auf">%s</div></div>' % (
              kopf(), drei(lambda i, p: foto(p['h'], '', '(max-width:860px) 100vw, 33vw')), drei(lambda i, p: text(i)), LAUF * 2, LAUF * 2,
              ''.join(foto(P[i]['A'][j], '', '(max-width:860px) 33vw, 17vw') for i in range(3) for j in (4, 6)))))

# 16 Vor der Rückwand: eine Wand aus Bildern der Bar über die Breite, davor stehen die drei hellen Karten; die Wand zieht beim Scrollen langsam auf
RUECK = ['ws13', 'flaschen', 'kanister', 'ws33']
F.append(('Vor der Rückwand der Bar', '<div class="t2-16">%s<div class="t2-16-wand" data-t2-wand><div class="t2-16-zoom">%s</div></div><div class="t2-16-karten staffel auf">%s</div></div>' % (
    kopf(), ''.join('<figure>%s</figure>' % img(k, '(max-width:860px) 50vw, 25vw') for k in RUECK),
    drei(lambda i, p: '<article class="t2-16-k" style="--i:%d">%s%s</article>' % (i, foto(p['h'], '', '(max-width:860px) 100vw, 30vw'), text(i, '', tag='div'))))))

# 17 Drehbühne: ein Ring aus Bildern im Raum, je Person ihr Bild und zwei Fotos; Name oder Pfeil drehen den Ring, der Text darunter wechselt mit
RING = [(i, k) for i, p in enumerate(P) for k in (p['A'][1], p['h'], p['A'][3])]
F.append(('Drehbühne', '<div class="t2-17" data-t2-ring>%s<div class="t2-17-buehne auf"><div class="t2-17-ring">%s</div></div>'
          '<div class="t2-17-steuer"><button type="button" data-t2-dreh="-1" aria-label="Zurück">‹</button><div class="t2-17-namen">%s</div>'
          '<button type="button" data-t2-dreh="1" aria-label="Weiter">›</button></div><div class="t2-17-texte">%s</div></div>' % (
              kopf(), ''.join('<figure style="--n:%d" data-p="%d">%s</figure>' % (n, i, img(k, '(max-width:860px) 60vw, 24vw')) for n, (i, k) in enumerate(RING)),
              drei(lambda i, p: '<button type="button" class="%s" data-i="%d"><span class="mono">%s</span>%s</button>' % ('an' if i == 0 else '', i, E(p['was']), E(p['name']))),
              drei(lambda i, p: '<div class="t2-17-text%s" data-i="%d"><p class="t2-text">%s</p>%s</div>' % (' an' if i == 0 else '', i, E(p['text']), ig(p))))))

# 18 Fensterwand: eine dunkle Wand mit Fenstern wie die Fassade der Bar, drei grosse mit den Leuten, sechs kleine mit ihrem Teil; die Bilder ziehen in den Fenstern
F.append(('Fensterwand', '<div class="t2-18 auf" data-ton="nacht" data-t2-fenster><div class="t2-18-kopf">%s</div><div class="t2-18-gross">%s</div><div class="t2-18-klein">%s</div></div>' % (
    kopf(''), drei(lambda i, p: '<div class="t2-18-s"><div class="t2-18-f">%s</div>%s</div>' % (img(p['h'], '(max-width:860px) 100vw, 30vw'), text(i))),
    ''.join('<div class="t2-18-f">%s</div>' % img(P[i]['A'][j], '(max-width:860px) 33vw, 15vw') for i in range(3) for j in (2, 5)))))

# 19 Gegenüber: wie an der langen Tafel, oben die drei, unten was sie auf den Tisch bringen, dazwischen die Platte mit den Texten; beide Reihen rücken an die Platte
GEGEN = ['fassade', 'g1', 'beete']
F.append(('Gegenüber an der Tafel', '<div class="t2-19 auf">%s<div class="t2-19-oben">%s</div><div class="t2-19-platte">%s</div><div class="t2-19-unten">%s</div></div>' % (
    kopf(), drei(lambda i, p: foto(p['h'], '', '(max-width:860px) 100vw, 33vw')), drei(lambda i, p: text(i)),
    drei(lambda i, p: foto(GEGEN[i], '', '(max-width:860px) 100vw, 33vw')))))

# 20 Im Takt: drei Karten mit grossem Hochformat; nacheinander, immer nur eine, zeigt jede Karte ihr Bild, dann zwei Fotos aus ihrem Teil, dann wieder das Bild
F.append(('Im Takt', '<div class="t2-20" data-t2-takt>%s<div class="t2-20-reihe staffel auf">%s</div></div>' % (
    kopf(), drei(lambda i, p: '<article class="t2-20-k" style="--i:%d"><div class="t2-20-stapel">%s</div>%s</article>' % (
        i, ''.join('<figure class="%s">%s</figure>' % ('an' if n == 0 else '', img(k, '(max-width:860px) 100vw, 30vw')) for n, k in enumerate([p['h'], p['A'][4], p['A'][6]])),
        text(i, '', tag='div'))))))


def main():
    seite = open(os.path.join(HIER, 'leute.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="vab[^"]*v-lt-koepfe[^"]*"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Die Leute» in leute.html nicht gefunden (erst varianten.py laufen lassen)'
    kopf_tag = m.group(1).replace('<section class="', '<section id="team" data-name="Drei Leute" class="wahl ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv t2 t2-f%02d" data-n="%d" hidden>%s</div>' % (i, i, inner if inner.startswith('<div class="t2-01') or inner.startswith('<div class="t2-09') else '<div class="vi">%s</div>' % inner)
              for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Drei Leute</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: drei Karten'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('team-wahl-2.css', 'team-wahl-2.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["team"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/team-wahl-2.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    seite = seite.replace('<title>', '<title>Drei Leute wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/team-wahl-2.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'team-wahl-2.html'), 'w', encoding='utf-8').write(seite)
    print('Seite team-wahl-2.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
