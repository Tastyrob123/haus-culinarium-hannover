#!/usr/bin/env python3
"""Culinarium Hannover · Warteliste «Dein Platz an der Tafel.» in 15 Fassungen, direkt in der echten Abend-Seite, 27.10.2026.
Robert: «Gib mir bitte 15 Visualisierungsmöglichkeiten, um das alternativ darzustellen.» Heute: drei Fotos mit Tischkarte links, rechts das Formular auf weissem Blatt.
Jede Fassung eine eigene Anordnung aus der Welt des Abends (Sitzplan, Ticket, Plakat, Bon am Pass, Kerzen, Gläser, Postkarte, Kalender, Umschlag …),
ohne Nummern-Liste und ohne Pillen. Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Alle Fassungen fragen dasselbe: Tag (Freitag ab 19, Samstag ab 17, egal), Plätze (1 bis 6), Name, E-Mail. Verschickt wird nichts.
Baut warteliste-wahl.html (Leiste unten, Pfeiltasten, ?warteliste=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/warteliste_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, PFEIL

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets/bild/meta.json')))
SATZ = 'Vierzehn Plätze an einer Tafel, und der letzte Abend war ausgebucht. Trag dich ein: Sobald der nächste Termin feststeht, erfährst du es vor allen anderen.'
TAGE = [('fr', 'Freitag', 'ab 19:00'), ('sa', 'Samstag', 'ab 17:00'), ('egal', 'Egal', 'beides geht')]
ZAHL = ['', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs']


def bild(k, sizes='50vw', pos=None):
    st = META[k]['stufen']
    p, alt = bau.BILD[k][1], bau.BILD[k][2]
    s = ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in st)
    return '<img src="assets/bild/%s-%d.webp?v=%s" srcset="%s" sizes="%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        k, st[min(1, len(st) - 1)], VERSION, s, sizes, E(alt), pos or p)


def fig(k, cls='', sizes='50vw', i=0, pos=None):
    return '<figure class="%s auf" style="--i:%d">%s</figure>' % (cls, i, bild(k, sizes, pos))


def kopf(cls='', groesse='gross', satz=SATZ):
    return '<div class="ww-kopf %s">%s%s</div>' % (cls, bau.zl(['Dein Platz', 'an der Tafel.'], 'h2', groesse),
                                                  bau.sw(E(satz), 'p', 'ww-satz', 1) if satz else '')


def tage(cls='', kurz=False):
    return '<div class="ww-tage %s" role="radiogroup" aria-label="Welcher Tag passt dir?">%s</div>' % (cls, ''.join(
        '<label><input type="radio" name="tag" value="%s"%s><span><b>%s</b><em>%s</em></span></label>' % (
            k, ' checked' if k == 'fr' else '', t, z) for k, t, z in TAGE))


def zaehler(cls=''):
    return ('<div class="ww-z %s"><button type="button" data-schritt="-1" aria-label="Weniger">−</button>'
            '<output data-feld="n" aria-live="polite">2</output><button type="button" data-schritt="1" aria-label="Mehr">+</button></div>' % cls)


def feld(n, label, cls='', ph=''):
    typ, ac = ('email', 'email') if n == 'mail' else ('text', 'name')
    return '<label class="ww-feld %s"><span>%s</span><input name="%s" type="%s" autocomplete="%s" required%s></label>' % (
        cls, label, n, typ, ac, ' placeholder="%s"' % E(ph) if ph else '')


def felder(cls='ww-zwei'):
    return '<div class="%s">%s%s</div>' % (cls, feld('name', 'Name'), feld('mail', 'E-Mail'))


def senden(t='Auf die Warteliste', cls=''):
    return '<button class="knopf %s" type="submit"><span>%s</span><i>%s</i></button>' % (cls, E(t).replace('i', '<em class="ki">i</em>'), PFEIL)


def leg(t):
    return '<p class="ww-leg">%s</p>' % t


MELD = '<p class="ww-meldung" data-meldung role="status" aria-live="polite"></p>'


def form(inner, cls='', tag='form'):
    return '<%s class="ww-form %s" data-ww novalidate>%s</%s>' % (tag, cls, inner, tag)


F = []

# 1 Der Sitzplan: die Tafel von oben, sieben Stühle je Seite; antippen, wie viele ihr seid, die Stühle rücken heran
STUEHLE = lambda reihe: ''.join(
    ('<button type="button" class="ww01-s" data-platz="%d" aria-label="%d %s"></button>' % (k, k, 'Platz' if k == 1 else 'Plätze'))
    if k <= 6 else '<span class="ww01-s frei"></span>' for k in reihe)
F.append(('Der Sitzplan', '<div class="ww-in ww01"><div class="ww01-l">%s%s</div><div class="ww01-r">%s<div class="ww01-plan auf" style="--i:1">'
          '<p class="ww01-k"><span data-feld="anzahl">2 Personen</span>, tipp an, wie viele ihr seid</p>'
          '<div class="ww01-reihe o">%s</div><div class="ww01-platte">%s</div><div class="ww01-reihe u">%s</div></div></div></div>' % (
              kopf('', 'mittel'), form(leg('Welcher Tag passt dir?') + tage() + felder() + '<div class="ww-tat">%s</div>%s' % (senden(), MELD)),
              fig('tafelleer', 'ww01-bild', '(max-width:860px) 100vw, 52vw', pos='50% 62%'),
              STUEHLE([1, 3, 5, 7, 9, 11, 13]), '<i></i>' * 7, STUEHLE([2, 4, 6, 8, 10, 12, 14]))))

# 2 Das Ticket: ein breites Ticket mit Abriss, die Felder stehen direkt darauf; beim Absenden löst sich der Abriss
F.append(('Das Ticket', '<div class="ww-in ww02">%s%s</div>' % (kopf('mitte', 'mittel'), form(
    '<figure class="ww02-bild">%s</figure><div class="ww02-mitte ww-hell"><div class="ww02-kopf">%s<span>A UNiQUE EXPERiENCE BY MOMO X RUDI</span></div>'
    '<div class="ww02-reihe"><div><p class="ww02-k">Tag</p>%s</div><div><p class="ww02-k">Plätze</p>%s</div></div>%s<div class="ww-tat">%s%s</div></div>'
    '<div class="ww02-abriss" aria-hidden="true"><p class="ww02-k">Warteliste</p><b data-feld="n">2</b><span class="ww02-pl">Plätze</span>'
    '<p class="ww02-t" data-feld="tag">Freitag</p><p class="ww02-z" data-feld="zeit">ab 19:00</p><p class="ww02-name" data-feld="name">Dein Name</p><p class="ww02-ok">Vorgemerkt</p></div>' % (
        bild('anstossen', '(max-width:860px) 100vw, 30vw'), bau.marke('wm'), tage(), zaehler(), felder(), senden(), MELD), 'ww02-ticket auf'))))

# 3 Der Satz: das ganze Formular ist ein Satz; Tag und Plätze antippen wechselt das Wort, Name und E-Mail schreibt man in die Lücke
F.append(('Der Satz', '<div class="ww-in ww03"><div class="ww03-bilder">%s%s</div>%s</div>' % (
    fig('kerze2', 'a', '(max-width:860px) 70vw, 30vw'), fig('kartglas', 'b', '(max-width:860px) 45vw, 18vw', 2),
    form('<p class="ww03-k sw auf">Warteliste · vierzehn Plätze, der letzte Abend war ausgebucht</p>'
         '<p class="ww03-satz sw auf" style="--i:1">Haltet mir einen Platz frei, am <button type="button" class="ww03-l" data-reihum="tag" aria-label="Tag wechseln">'
         '<span data-feld="tag">Freitag</span></button> für <button type="button" class="ww03-l" data-reihum="n" aria-label="Anzahl wechseln"><span data-feld="anzahl">2 Personen</span></button>. '
         'Ich heiße <label class="ww03-l"><span class="vh">Name</span><input name="name" autocomplete="name" required placeholder="Vor- und Nachname"></label>, '
         'schreibt mir an <label class="ww03-l"><span class="vh">E-Mail</span><input name="mail" type="email" autocomplete="email" required placeholder="deine@mail.de"></label>.</p>'
         '<p class="ww03-hin sw auf" style="--i:2">Die farbigen Wörter antippen, um sie zu ändern.</p><div class="ww-tat sw auf" style="--i:3">%s%s</div>' % (senden('Abschicken'), MELD), 'ww03-f'))))

# 4 Das Plakat: man trägt sich direkt auf dem Plakat des nächsten Abends ein; der Tag färbt die Linie des Abends
F.append(('Das Plakat', '<div class="ww-in ww04"><div class="ww04-l">%s<p class="ww04-hin sw auf" style="--i:2">Jeder Abend hat sein Plakat. Auf dem nächsten steht schon dein Name.</p></div>%s</div>' % (
    kopf('', 'mittel', SATZ), form(
        '<div class="ww04-blatt"><figure class="ww04-bild">%s</figure><div class="ww04-marke">%s</div><p class="ww04-zeile">A UNiQUE EXPERiENCE BY MOMO X RUDI</p>'
        '<div class="ww04-tage">%s</div><i class="ww04-linie" data-neu></i>'
        '<label class="ww04-name"><span class="vh">Name</span><input name="name" autocomplete="name" required placeholder="Dein Name"></label>'
        '<div class="ww04-unten"><div class="ww04-pl"><span>Plätze</span>%s</div><label class="ww04-mail"><span>E-Mail</span><input name="mail" type="email" autocomplete="email" required></label></div>'
        '<p class="ww04-ort">Walk on the Wild Side · Haasemannstraße 13 · Linden</p></div><div class="ww-tat">%s%s</div>' % (
            bild('t03', '(max-width:860px) 90vw, 34vw', '50% 45%'), bau.marke('wm'),
            ''.join('<label><input type="radio" name="tag" value="%s"%s><span>%s</span></label>' % (k, ' checked' if k == 'fr' else '', t)
                    for k, t in [('fr', 'Fr · 19:00'), ('sa', 'Sa · 17:00'), ('egal', 'Fr oder Sa')]),
            zaehler(), senden(), MELD), 'ww04-plakat auf'))))

# 5 Die Karte: geschrieben wie Rudis Zeilen in Versalien, der gewählte Tag und die Zahl leuchten, der Rest tritt zurück
F.append(('Die Karte', '<div class="ww-in ww05">%s</div>' % form(
    '<div class="ww05-text"><p class="ww05-k sw auf">Warteliste für den nächsten Abend</p>%s'
    '<div class="ww05-gang sw auf" style="--i:2"><p class="ww05-n">Der Tag</p><div class="ww05-zeile">%s</div><p class="ww05-unter"><span data-feld="zeit">ab 19:00</span></p></div>'
    '<div class="ww05-gang sw auf" style="--i:3"><p class="ww05-n">Die Plätze</p><div class="ww05-zeile">%s</div></div>'
    '<label class="ww05-gang sw auf" style="--i:4"><span class="ww05-n">Dein Name</span><input class="ww05-in" name="name" autocomplete="name" required placeholder="DEIN NAME"></label>'
    '<label class="ww05-gang sw auf" style="--i:5"><span class="ww05-n">E-Mail</span><input class="ww05-in" name="mail" type="email" autocomplete="email" required placeholder="DEINE@MAIL.DE"></label>'
    '<div class="ww-tat sw auf" style="--i:6">%s%s</div></div><figure class="ww05-bild auf">%s</figure>' % (
        bau.zl(['Dein Platz', 'an der Tafel.'], 'h2', 'mittel'),
        '<i class="sl">/</i>'.join('<label><input type="radio" name="tag" value="%s"%s><span>%s</span></label>' % (k, ' checked' if k == 'fr' else '', t.upper())
                                   for k, t, _z in TAGE),
        '<i class="sl">/</i>'.join('<button type="button" data-platz="%d" data-genau aria-label="%d">%s</button>' % (k, k, ZAHL[k].upper()) for k in range(1, 7)),
        senden(), MELD, bild('r09', '(max-width:860px) 100vw, 36vw')), 'ww05-karte')))

# 6 Der Bon am Pass: über dem Pass hängt an der Schiene der Bon, der beim Ausfüllen mitschreibt und bei jeder Änderung leicht schwingt
F.append(('Der Bon am Pass', '<div class="ww06"><div class="ww06-band">%s<i class="ww06-schiene"></i></div><div class="ww-in ww06-unten">'
          '<div class="ww06-bonplatz"><div class="ww06-bon" data-neu aria-hidden="true"><i class="ww06-klemme"></i>'
          '<p class="c">Culinarium</p><p class="c">Warteliste</p><p class="ww06-st">- - - - - - - - - - - - - -</p>'
          '<p><b data-feld="n">2</b> × Platz an der Tafel</p><p data-feld="tag">Freitag</p><p data-feld="zeit">ab 19:00</p><p class="ww06-st">- - - - - - - - - - - - - -</p>'
          '<p class="k">Für</p><p class="ww06-name" data-feld="name">Dein Name</p><p class="ww06-st">- - - - - - - - - - - - - -</p><p class="c ww06-ok">Vorgemerkt</p><p class="c ww06-wart">Haasemannstraße 13</p></div></div>'
          '<div class="ww06-r">%s%s</div></div></div>' % (
              fig('pass', 'ww06-bild', '100vw', pos='50% 46%'), kopf('', 'mittel'),
              form('<div class="ww06-reihe"><div>%s%s</div><div>%s%s</div></div>%s<div class="ww-tat">%s%s</div>' % (
                  leg('Welcher Tag?'), tage(), leg('Wie viele?'), zaehler(), felder(), senden(), MELD)))))

# 7 Anstossen: links und rechts ein Glas, dazwischen das Formular; ist man eingetragen, kommen die Gläser in der Mitte zusammen
F.append(('Anstossen', '<div class="ww-in ww07"><div class="ww07-reihe">%s<div class="ww07-m">%s%s</div>%s</div><div class="ww07-dank">%s</div></div>' % (
    fig('g1', 'ww07-g l', '(max-width:860px) 46vw, 24vw', pos='50% 40%'), kopf('mitte', 'mittel', 'Vierzehn Plätze, und der letzte Abend war ausgebucht. Trag dich ein, dann erfährst du den nächsten Termin zuerst.'),
    form(tage() + '<div class="ww07-pl"><span>Plätze</span>%s</div>%s<div class="ww-tat">%s</div>' % (zaehler(), felder('ww-eins'), senden('Anstossen'))),
    fig('g5', 'ww07-g r', '(max-width:860px) 46vw, 24vw', 1, '50% 52%'), MELD)))

# 8 Die Kerzen: für jeden Gast eine Kerze; antippen zündet so viele an, wie ihr seid
F.append(('Die Kerzen', '<div class="ww-in ww08">%s<div class="ww08-r">%s%s</div></div>' % (
    fig('kerze1', 'ww08-bild', '(max-width:860px) 100vw, 46vw'), kopf('', 'mittel'),
    form('<div class="ww08-box"><p class="ww-leg">Für jeden eine Kerze.</p><div class="ww08-kerzen">%s</div><p class="ww08-n"><span data-feld="anzahl">2 Personen</span></p></div>%s%s%s<div class="ww-tat">%s%s</div>' % (
        ''.join('<button type="button" class="ww08-k" data-platz="%d" aria-label="%d %s" style="--h:%dpx"><i class="fl"></i><b></b></button>' % (
            k, k, 'Person' if k == 1 else 'Personen', h) for k, h in zip(range(1, 7), [92, 70, 110, 80, 100, 64])),
        leg('Welcher Tag passt dir?'), tage(), felder(), senden(), MELD)))))

# 9 Die Gläser: sechs Gläser stehen in einer Reihe; so viele, wie ihr seid, rücken nach vorn
GL = ['g1', 'g2', 'g5', 'glas', 'coupe', 'd2']
F.append(('Die Gläser', '<div class="ww09"><div class="ww-in">%s</div><div class="ww09-reihe">%s</div><p class="ww-in ww09-n"><span data-feld="anzahl">2 Personen</span> · ein Glas für jeden, antippen zum Ändern</p>'
          '<div class="ww-in">%s</div></div>' % (
              kopf('mitte', 'mittel'),
              ''.join('<button type="button" class="ww09-g auf" data-platz="%d" style="--i:%d" aria-label="%d %s"><span class="ww09-f">%s</span></button>' % (
                  k, k - 1, k, 'Person' if k == 1 else 'Personen', bild(g, '(max-width:860px) 17vw, 15vw')) for k, g in enumerate(GL, 1)),
              form('<div class="ww09-zeile">%s%s%s%s</div>%s' % (tage(), feld('name', 'Name'), feld('mail', 'E-Mail'), senden('Eintragen'), MELD), 'ww09-form'))))

# 10 Freitag oder Samstag: zwei grosse Bilder, man wählt den Abend mit dem Bild; der andere tritt zurück
F.append(('Freitag oder Samstag', form(
    '<div class="ww-in">%s</div><div class="ww10-paar">'
    '<label class="ww10-h ww10-fr"><input type="radio" name="tag" value="fr" checked><span class="ww10-f auf">%s</span><span class="ww10-t"><b>Freitag</b><em>ab 19:00 Uhr</em></span></label>'
    '<label class="ww10-egal"><input type="radio" name="tag" value="egal"><span>Beides <br>geht</span></label>'
    '<label class="ww10-h ww10-sa"><input type="radio" name="tag" value="sa"><span class="ww10-f auf" style="--i:1">%s</span><span class="ww10-t"><b>Samstag</b><em>ab 17:00 Uhr</em></span></label></div>'
    '<div class="ww-in ww10-zeile"><div class="ww10-pl"><span>Plätze</span>%s</div>%s%s%s</div><div class="ww-in">%s</div>' % (
        kopf('mitte', 'mittel', 'Vierzehn Plätze, der letzte Abend war ausgebucht. Such dir deinen Abend aus, wir melden uns, sobald der Termin steht.'),
        bild('t03', '(max-width:860px) 50vw, 44vw'), bild('t05', '(max-width:860px) 50vw, 44vw'), zaehler(), feld('name', 'Name'), feld('mail', 'E-Mail'), senden('Eintragen'), MELD),
    'ww10')))

# 11 Am Tresen: ein kurzes Gespräch über die Theke; jede Frage steht da, die Antworten erscheinen als eigene Zeilen rechts
F.append(('Am Tresen', '<div class="ww-in ww11">%s%s</div>' % (
    fig('theke', 'ww11-bild', '(max-width:860px) 100vw, 40vw'), form(
        '<div class="ww11-kopf">%s<div><b>Culinarium</b><span>Warteliste · Walk on the Wild Side</span></div></div>'
        '<p class="ww11-q">Der letzte Abend war ausgebucht. Sollen wir dir Bescheid geben, sobald der nächste feststeht?</p>'
        '<p class="ww11-q">Welcher Tag passt dir besser?</p><div class="ww11-a">%s</div>'
        '<p class="ww11-q">Wie viele seid ihr?</p><div class="ww11-a ww11-pl"><span data-feld="anzahl">2 Personen</span>%s</div>'
        '<p class="ww11-q">Und wie heisst du, wohin schreiben wir dir?</p><div class="ww11-a ww11-felder">%s%s</div>'
        '<div class="ww11-a ww11-los">%s</div>%s' % (
            '<span class="ww11-av">%s</span>' % bild('barnacht', '52px'),
            '<i class="sl">/</i>'.join('<label><input type="radio" name="tag" value="%s"%s><span>%s</span></label>' % (k, ' checked' if k == 'fr' else '', t)
                                       for k, t in [('fr', 'Freitag, ab 19 Uhr'), ('sa', 'Samstag, ab 17 Uhr'), ('egal', 'Egal')]),
            zaehler(), feld('name', 'Name'), feld('mail', 'E-Mail'), senden('Abschicken'), MELD.replace('ww-meldung', 'ww-meldung ww11-q')), 'ww11-f'))))

# 12 Die Postkarte: man füllt die Rückseite einer Postkarte aus; abgeschickt, dreht sie sich auf das Bild
F.append(('Die Postkarte', '<div class="ww-in ww12">%s<div class="ww12-karte auf">%s</div>%s</div>' % (
    kopf('mitte', 'mittel', 'Vierzehn Plätze, der letzte Abend war ausgebucht. Schreib uns eine Karte, wir melden uns, sobald der Termin steht.'),
    form('<div class="ww12-dreh"><div class="ww12-rueck ww-hell"><div class="ww12-l"><p class="ww12-gruss">Liebe Tafel,<br>haltet mir einen Platz frei.</p>'
         '<div class="ww12-tage">%s</div><div class="ww12-pl"><span>Plätze</span>%s</div></div><i class="ww12-strich"></i>'
         '<div class="ww12-r"><div class="ww12-oben"><span class="ww12-stempel">Linden<br><b>Warteliste</b></span><span class="ww12-marke">%s</span></div>'
         '<label class="ww12-zeile"><span>Name</span><input name="name" autocomplete="name" required></label>'
         '<label class="ww12-zeile"><span>E-Mail</span><input name="mail" type="email" autocomplete="email" required></label><div class="ww-tat">%s</div></div></div>'
         '<div class="ww12-vorn" aria-hidden="true">%s</div></div>' % (
             ''.join('<label><input type="radio" name="tag" value="%s"%s><i></i><span>%s</span></label>' % (k, ' checked' if k == 'fr' else '', t)
                     for k, t in [('fr', 'Freitag, ab 19 Uhr'), ('sa', 'Samstag, ab 17 Uhr'), ('egal', 'Egal, beides geht')]),
             zaehler(), bild('glaeser', '120px'), senden('Abschicken'), bild('anstossen', '(max-width:860px) 100vw, 60vw')), 'ww12-f'), MELD)))

# 13 Die Tischkante: drei Bilder der Tafel Kante an Kante, darunter wie die Tischkante eine einzige Zeile zum Eintragen
F.append(('Die Tischkante', '<div class="ww13"><div class="ww-in">%s</div><div class="ww13-band">%s%s%s</div>%s</div>' % (
    kopf('mitte', 'mittel'),
    fig('kerze2', 'ww13-b', '(max-width:860px) 34vw, 34vw'), fig('tafelleer', 'ww13-b', '(max-width:860px) 34vw, 34vw', 1, '50% 60%'), fig('t05', 'ww13-b', '(max-width:860px) 34vw, 34vw', 2),
    form('<div class="ww-in ww13-zeile">%s<div class="ww13-pl"><span>Plätze</span>%s</div>%s%s%s</div><div class="ww-in">%s</div>' % (
        tage(), zaehler(), feld('name', 'Name'), feld('mail', 'E-Mail'), senden('Eintragen'), MELD), 'ww13-kante'))))

# 14 Der Abreisskalender: ein Kalenderblock zeigt den Tag; antippen reisst das Blatt ab und der nächste Tag erscheint
F.append(('Der Abreisskalender', form(
    '<div class="ww14-l">%s%s%s<div class="ww-tat">%s%s</div></div><div class="ww14-r"><div class="ww14-block auf"><i class="ww14-ring"></i>'
    '<button type="button" class="ww14-blaetter" data-reihum="tag" aria-label="Nächster Tag">%s</button></div><div class="ww14-wahl">%s</div></div>' % (
        kopf('', 'mittel'), '<div class="ww14-pl">%s%s</div>' % (leg('Wie viele Plätze?'), zaehler()), felder(), senden(), MELD,
        ''.join('<span class="ww14-blatt" data-blatt="%s"><span class="ww14-kopf">Warteliste · Culinarium</span><b>%s</b><em>%s</em>'
                '<span class="ww14-fuss"><span data-feld="anzahl">2 Personen</span> · vierzehn Plätze</span></span>' % (k, t, z)
                for k, t, z in [('fr', 'Freitag', 'ab 19:00 Uhr'), ('sa', 'Samstag', 'ab 17:00 Uhr'), ('egal', 'Fr oder Sa', 'beides geht')]),
        ''.join('<label><input type="radio" name="tag" value="%s"%s><span>%s</span></label>' % (k, ' checked' if k == 'fr' else '', t)
                for k, t, _z in TAGE)),
    'ww-in ww14')))

# 15 Der Umschlag: man schreibt auf einen Briefbogen; abgeschickt, gleitet der Brief in den Umschlag und das Siegel schliesst
F.append(('Der Umschlag', '<div class="ww-in ww15"><div class="ww15-l">%s<p class="ww15-hin sw auf" style="--i:2">Die Einladung kommt per Mail, sobald der nächste Termin steht.</p>%s</div>'
          '<div class="ww15-r auf">%s<div class="ww15-umschlag" aria-hidden="true"><i class="ww15-klappe"></i><span class="ww15-siegel">×</span></div></div></div>' % (
              kopf('', 'mittel'), MELD, form(
                  '<p class="ww15-an">An Culinarium<br>Haasemannstraße 13, Linden</p><p class="ww15-text">Bitte schickt mir die Einladung zum nächsten Abend.</p>'
                  '<div class="ww15-reihe"><div>%s%s</div><div>%s%s</div></div>%s<div class="ww-tat">%s</div>' % (
                      leg('Am liebsten'), tage(), leg('Wir sind'), zaehler(), felder(), senden('Abschicken')), 'ww15-brief ww-hell'))))


def main():
    seite = open(os.path.join(HIER, 'abend.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="warteliste"[^>]*id="warteliste"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, 'Warteliste in abend.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="warteliste"', 'data-name="Warteliste" class="warteliste wahl"', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv ww ww-f%02d" data-n="%d" hidden>%s</div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Warteliste</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Tischkarte und Formular'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('warteliste-wahl.css', 'warteliste-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["warteliste"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/warteliste-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    seite = seite.replace('<title>', '<title>Warteliste wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/warteliste-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'warteliste-wahl.html'), 'w', encoding='utf-8').write(seite)
    print('Seite warteliste-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
