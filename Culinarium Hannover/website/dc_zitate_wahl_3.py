#!/usr/bin/env python3
"""Dirty Chicken · «Wie Dirty Chicken von sich spricht», dritte Runde: 15 weitere Fassungen (Robert 28.10.2026: «nochmal 15 weitere Versionen
und benutze bitte auch die aktuellen Formate der Website, wie sie jetzt gebaut ist»).
Rahmen: die echte dirty-chicken.html im heutigen Stand (zitate_rahmen.py); davor steht das Pop-up «Senkrecht» mit Burger, Zeichen und Sauce,
danach Opening mit der Mannschaft. Deshalb hier vor allem die anderen Bilder: Karte, Drink, Mannschaft am Tresen (DZIjZWNCGZT-2), Plakat, Tisch,
Glas, Drinks, Theke und Standbilder aus dem Opening-Film.
Nichts aus Runde 1 oder 2 noch einmal (und nichts aus Essen-, Nacht- und Pop-up-Wahl). Nur transform und opacity, nichts überlappt Fotos,
Gesichter unberührt. Baut dirty-chicken-zitate-wahl-3.html (?zitate3=Nummer, 0 = heute).
Aufruf: python3 website/dc_zitate_wahl_3.py"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, foto, zl, sw
from dc_zitate_wahl import Z, q, ek, et, ex, kopf, datum, d_zeichen, zeilenbrechen

HIER = bau.HIER
B = ['dn_karte', 'dc_drink', 'dc_team2', 'dc_plakat', 'dc_tisch']


def sec(n, ton, inner, cls=''):
    return '<section class="vab dc-ab ess zws%02d %s" data-ton="%s">%s</section>' % (n, cls, ton, inner)


def roh(s):
    return re.sub('&amp;', '&', s)


def bild(k, w=1600):
    st = max(x for x in bau.META[k]['stufen'] if x <= w)
    return 'assets/bild/%s-%d.webp?v=%s' % (k, st, VERSION)


def still(n):
    return 'assets/film/opening-still-%d.webp?v=%s' % (n, VERSION)


F = []

# 1 Das Interview: wir fragen, Dirty Chicken antwortet mit seinen Sätzen; zu jeder Antwort das Bild
FR = ['Was ist dit hier eigentlich?', 'Und was trinkt man dazu?', 'Wer steht hinter Dirty Chicken?', 'Wie war das Opening im Tiedthof?', 'Und wenn man es in einem Satz sagen müsste?']
def interview(i, f, s, d, k):
    return '''<div class="zv1-e %s"><div class="zv1-qa"><p class="zv1-f sw auf" style="--i:0"><b>Wir</b>%s</p>
<div class="zv1-a"><b class="zv1-wer">Dirty Chicken</b>%s%s</div></div><div class="zv1-bild auf">%s</div></div>''' % (
        'r' if i % 2 else 'l', f, zl(zeilenbrechen(q(s), 30), 'p', 'zv1-satz', 1), datum(d), foto(k, '', '(max-width:860px) 60vw, 24vw', auf=False, pos='50% 40%'))
F.append(('Das Interview', 'Ein kurzes Interview: Wir fragen, Dirty Chicken antwortet, und jede Antwort ist einer seiner Sätze von Instagram. Zu jeder Antwort das Bild des Beitrags, abwechselnd links und rechts.', sec(1, 'hell', '<div class="vi">%s<div class="zv1">%s</div></div>' % (
    kopf(kick='Fünf Fragen', titel=('Fünf Fragen,', 'fünf Ansagen.'), text='Die Fragen sind von uns. Die Antworten hat Dirty Chicken im Juni 2026 selbst geschrieben.'),
    ''.join(interview(i, f, s, d, k) for i, (f, (s, _h, d, _k, _p), k) in enumerate(zip(FR, Z, B)))))))

# 2 Gesprächsfetzen: die Theke am Abend gross über die ganze Breite, darin hängen die Sätze wie Gesprächsfetzen im Raum und wandern beim Scrollen verschieden schnell
FETZ = [(0, 5, 44, 'g', .05), (1, 58, 30, 'm', -.04), (2, 5, 66, 'm', .03), (3, 64, 56, 'k', -.05), (4, 40, 80, 'g', .04)]
F.append(('Gesprächsfetzen', 'Die Theke am Abend steht gross über die ganze Breite, und darin hängen die Sätze wie Gesprächsfetzen im Raum, verschieden gross. Beim Scrollen wandern sie verschieden schnell, als käme jeder aus einer anderen Ecke.', sec(2, 'nacht', '''<div class="vi">%s</div><div class="zv2-raum auf">%s<div class="zv2-dunkel"></div>%s</div>''' % (
    kopf(cls='mitte', text='Man hört es, bevor man es liest. So klingt es am Tresen.'), foto('dn_bar', 'zv2-f', '100vw', auf=False, pos='50% 22%', extra='style="--weg:0px"'),
    ''.join('<div class="zv2-s %s" style="left:%d%%;top:%d%%" data-tiefe="%.2f"><p>%s</p>%s</div>' % (g, x, y, t, q(Z[i][0]), datum(Z[i][2])) for i, x, y, g, t in FETZ)))))

# 3 Bilder im Satz: die Sätze gross gesetzt, kleine Bilder sitzen mitten zwischen den Wörtern
IM = [
    [('Dit is keen Burger.', 'dn_tisch'), ('Dit Ding is ’ne Ansage.', 'dn_karte')],
    [('Dirty Food', 'dc_drink'), ('&amp; Dirty Drinks.', 'dn_glas'), ('Jenau meen Ding wa.', None)],
    [('Wenn aus Freunden', 'dc_team2'), ('und Kollegen Familie wird. Dann haste allet richtig jemacht!', None)],
    [('Opening 2026!', 'dc_plakat'), ('Wat ne Sause.', None)],
    [('Dit ist wahre Liebe!', 'dc_tisch')],
]
def satz_mit_bildern(i, teile, d):
    out, j = [], 0
    for t, k in teile:
        out.append('<span class="zv3-t">%s</span>' % t)
        if k:
            out.append(' <span class="zv3-b" style="--j:%d">%s</span> ' % (j, foto(k, '', '22vw', auf=False, pos='50% 45%', extra='style="--weg:0px"')))
            j += 1
        else:
            out.append(' ')
    return '<div class="zv3-e auf"><div class="zv3-s">„%s“</div>%s</div>' % (''.join(out).strip(), datum(d))
F.append(('Bilder im Satz', 'Die fünf Sätze gross gesetzt auf hellem Grund, und mitten zwischen den Wörtern sitzen kleine Bilder: der Drink nach «Dirty Drinks», das Plakat nach «Opening». Die Bilder drehen sich beim Ankommen in die Zeile.', sec(3, 'hell', '<div class="vi">%s<div class="zv3">%s</div></div>' % (
    kopf(text='Fünf Sätze, so wie sie auf Instagram standen, mit den Bildern dazu mitten im Satz.'), ''.join(satz_mit_bildern(i, t, Z[i][2]) for i, t in enumerate(IM))))))

# 4 Die Wendetafel: wie eine Werbetafel mit drehenden Lamellen; Bild und Satz wechseln sich ab, die Lamellen drehen nacheinander
N4 = 12
ITEMS = []
for i, (s, _h, d, _k, _p) in enumerate(Z):
    ITEMS.append('<img class="zv4-img" src="%s" alt="" style="object-position:50%% 40%%">' % bild(B[i]))
    ITEMS.append('<div class="zv4-tafel %s"><p>%s</p>%s</div>' % ('t%d' % (i % 3), q(s), datum(d)))
def lamelle(j):
    return '<div class="zv4-s" style="--j:%d"><div class="zv4-f"><div class="zv4-voll" style="left:%d%%">%s</div></div></div>' % (j, -100 * j, ITEMS[0])
F.append(('Die Wendetafel', 'Wie eine Werbetafel mit drehenden Lamellen an der Strasse: Bild und Satz wechseln sich ab, alle paar Sekunden drehen die Lamellen nacheinander um. Antippen dreht sofort weiter.', sec(4, 'nacht', '''<div class="vi">%s<div class="zv4 auf" role="button" tabindex="0" aria-label="Weiterdrehen" data-n="%d">%s</div>
<script type="application/json" class="zv4-daten">%s</script><div class="zv4-unten"><p class="mono zv4-nr">1 / 10</p></div></div>''' % (
    kopf(text='Bild, Satz, Bild, Satz. Die Tafel dreht von selbst weiter.'), N4, ''.join(lamelle(j) for j in range(N4)), json.dumps(ITEMS)))))

# 5 Die Litfasssäule: die Sätze als Plakate auf einer Litfasssäule, die sich beim Scrollen dreht; daneben der Titel
def plakat5(i, s, d, k):
    return '<div class="zv5-p %s" data-i="%d"><div class="zv5-bild"><img src="%s" alt="" loading="lazy" style="object-position:50%% 40%%"></div><div class="zv5-text"><p>%s</p>%s</div></div>' % (
        'p%d' % (i % 3), i, bild(k, 1000), q(s), datum(d))
F.append(('Die Litfasssäule', 'Die Sätze als Plakate auf einer Litfasssäule: oben das Bild des Beitrags, darunter der Satz. Beim Scrollen dreht sich die Säule, die Plakate laufen um sie herum und werden an den Rändern schmaler, wie auf einer echten Säule.', sec(5, 'warm', '''<div class="vi zv5"><div class="zv5-links">%s</div>
<div class="zv5-saeule auf"><div class="zv5-dach"></div><div class="zv5-koerper">%s</div><div class="zv5-sockel"></div></div></div>''' % (
    kopf(kick='An der Ecke', titel=('Rundherum', 'plakatiert.'), text='Fünf Sätze, fünf Plakate. Scrollen dreht die Säule.'),
    ''.join(plakat5(i, s, d, k) for i, ((s, _h, d, _k, _p), k) in enumerate(zip(Z, B)))))))

# 6 Das Schaufenster: ein Ladenfenster mit Schild über der Tür; in jeder Scheibe ein Bild, unten auf dem Glas der Satz in Schildermalerei; ein Lichtstreif zieht über das Glas
F.append(('Das Schaufenster', 'Ein Ladenfenster mit violettem Schild darüber: in jeder der fünf Scheiben ein Bild, unten auf dem Glas der Satz, wie von Hand aufs Fenster gemalt. Beim Ankommen zieht einmal ein Lichtstreif über die Scheiben.', sec(6, 'nacht', '''<div class="vi">%s<div class="zv6 auf"><div class="zv6-schild"><b>Dirty Chicken</b><span>Sandwiches &amp; More · Dirty Drinks · Hannover</span></div>
<div class="zv6-rahmen">%s</div><div class="zv6-sims"></div></div></div>''' % (
    kopf(cls='mitte', text='So würde es auf dem Fenster stehen. Fünf Scheiben, fünf Sätze.'),
    ''.join('<div class="zv6-scheibe">%s<div class="zv6-glas"><p>%s</p>%s</div><i class="zv6-licht" style="--j:%d"></i></div>' % (
        foto(k, '', '(max-width:860px) 50vw, 20vw', auf=False, pos='50% 40%', extra='style="--weg:0px"'), roh(s), datum(d), i) for i, ((s, _h, d, _k, _p), k) in enumerate(zip(Z, B)))))))

# 7 Das Prägeband: die Sätze geprägt auf Etikettenband wie aus dem Beschriftungsgerät, Streifen für Streifen; daneben das Bild vom Tisch
PB = [['Dit is keen Burger.', 'Dit Ding is ’ne Ansage.'], ['Dirty Food &amp; Dirty Drinks.', 'Jenau meen Ding wa.'],
      ['Wenn aus Freunden', 'und Kollegen Familie wird.', 'Dann haste allet richtig jemacht!'], ['Opening 2026!', 'Wat ne Sause.'], ['Dit ist wahre Liebe!']]
FARBE7 = ['b-lila', 'b-schwarz', 'b-lila', 'b-kerze', 'b-schwarz']
ROT7 = [-1.6, .8, -.6, 1.4, -1.0, .5, -1.8, 1.1, -.4, .9, -1.3]
def praege():
    out, n = [], 0
    for i, (teile, (s, _h, d, _k, _p)) in enumerate(zip(PB, Z)):
        st = ''
        for t in teile:
            st += '<span class="zv7-band %s" style="--n:%d;--r:%.1fdeg">%s</span>' % (FARBE7[i], n, ROT7[n % len(ROT7)], E(roh(t).upper()))
            n += 1
        out.append('<div class="zv7-g" aria-label="%s">%s%s</div>' % (E(roh(s)), st, datum(d)))
    return ''.join(out)
F.append(('Das Prägeband', 'Die Sätze geprägt auf Etikettenband, wie aus dem Beschriftungsgerät: weisse Versalien auf violettem, schwarzem und orangem Band, jeder Satz in Streifen. Die Streifen werden beim Ankommen einer nach dem anderen aufgedrückt. Daneben gross der Tisch mit den Drinks.', sec(7, 'warm', '''<div class="vi">%s<div class="zv7"><div class="zv7-baender auf">%s</div><div class="zv7-bild auf">%s</div></div></div>''' % (
    kopf(kick='Beschriftet', titel=('Kurz und', 'jeprägt.'), text=''), praege(), foto('dn_drinks', '', '(max-width:860px) 100vw, 40vw', auf=False, pos='50% 45%')))))

# 8 Die Schablone: jeder Satz ist mit Schablone auf die Wand gesprüht; beim Ankommen hebt sich die Schablone ab und der Satz steht da
def schablone(i, s, d):
    zeilen = zeilenbrechen(roh(s).upper(), 22)
    fs, lh, w = 84, 92, 1200
    h = lh * len(zeilen) + 30
    t = ''.join('<text x="0" y="%d">%s</text>' % (lh * (j + 1) - 10, E(z)) for j, z in enumerate(zeilen))
    return '''<div class="zv8-e %s"><div class="zv8-feld"><svg class="zv8-farbe" viewBox="0 0 %d %d" aria-label="%s"><g class="zv8-spray">%s</g></svg>
<svg class="zv8-blatt" viewBox="0 0 %d %d" aria-hidden="true"><defs><mask id="zv8m%d"><rect x="-40" y="-30" width="%d" height="%d" fill="#fff"/><g fill="#000" class="zv8-loch">%s</g></mask></defs>
<rect x="-40" y="-30" width="%d" height="%d" fill="#C9B79C" mask="url(#zv8m%d)"/></svg></div>%s</div>''' % (
        'r' if i % 2 else 'l', w, h, E(roh(s)), t, w, h, i, w + 80, h + 60, t, w + 80, h + 60, i, datum(d))
F.append(('Die Schablone', 'Jeder Satz ist mit Schablone auf eine helle Betonwand gesprüht, in violetten Versalien mit ein wenig Sprühnebel. Beim Ankommen hebt sich die Pappschablone ab, eine nach der anderen, und der Satz steht auf der Wand.', sec(8, 'hell', '<div class="vi">%s<div class="zv8 auf">%s</div></div>' % (
    kopf(kick='An der Wand', titel=('Jesprüht,', 'nicht jesagt.'), text='Fünf Sätze, mit Schablone auf die Wand. So spricht Dirty Chicken.'), ''.join(schablone(i, s, d) for i, (s, _h, d, _k, _p) in enumerate(Z))))))

# 9 Der Wegweiser: an einem Pfahl zeigen fünf Schilder in verschiedene Richtungen, auf jedem ein Satz; oben das Zeichen
F.append(('Der Wegweiser', 'Ein Wegweiser wie an einer Strassenecke: An einem Pfahl zeigen fünf Schilder abwechselnd nach links und rechts, auf jedem ein Satz und sein Datum, oben das Zeichen. Beim Ankommen schwingen die Schilder in ihre Lage.', sec(9, 'dc', '''<div class="vi zv9"><div class="zv9-links">%s</div><div class="zv9-pfahl auf"><div class="zv9-kopf">%s</div><i class="zv9-stange"></i>%s</div></div>''' % (
    kopf(kick='Hier lang', titel=('Immer', 'der Nase nach.'), text='Fünf Schilder, fünf Sätze. Jeder zeigt woanders hin, alle führen zum selben Pop-up.'), d_zeichen('zv9-z'),
    ''.join('<div class="zv9-schild %s s%d" style="--j:%d"><p>%s</p>%s</div>' % ('l' if i % 2 else 'r', i % 3, i, roh(s), datum(d)) for i, (s, _h, d, _k, _p) in enumerate(Z))))))

# 10 Das Filmplakat: wie ein Kinoplakat, die Sätze stehen oben als Stimmen, darunter das Standbild aus dem Opening-Film, der Titel und der Abspann mit den echten Partnern
F.append(('Das Filmplakat', 'Ein Kinoplakat: oben stehen vier Sätze wie Stimmen der Kritik, darunter ein Standbild aus dem Opening-Film, gross der Titel und «Dit ist wahre Liebe!» als Untertitel. Unten der Abspann mit den echten Namen vom Plakat. Das Bild zoomt beim Scrollen langsam zurück.', sec(10, 'nacht', '''<div class="vi zv10"><div class="zv10-links">%s</div>
<div class="zv10-plakat auf"><div class="zv10-stimmen">%s</div><div class="zv10-bild"><img src="%s" alt="Ein Tablett mit Chicken, Pommes und Krautsalat beim Opening" loading="lazy"></div>
<p class="zv10-titel">Dirty Chicken</p><p class="zv10-unter">„Dit ist wahre Liebe!“</p>
<p class="zv10-abspann">Opening 30. Mai 2026 · AM:PM Café im Tiedthof<br>AM:PM · Walk on the Wild Side · Beluga · NATE · Gastschicht Martin Bauermann · Mit Rudi und Momo</p></div></div>''' % (
    kopf(kick='Jetzt im Tiedthof', titel=('Die Kritik', 'ist sich einig.'), text='Wer die Kritiken geschrieben hat? Dirty Chicken selbst, im Juni 2026 auf Instagram.'),
    ''.join('<div class="zv10-st sw auf" style="--i:%d"><p>%s</p><span>Dirty Chicken · %s</span></div>' % (j, q(Z[i][0]), Z[i][2].replace(' 2026', '')) for j, i in enumerate((0, 1, 3, 2))),
    still(17)))))

# 11 Der Scheinwerfer: dunkle Bühne, ein Lichtkegel wandert beim Scrollen von Satz zu Satz; der Satz im Licht ist hell, die anderen warten im Dunkeln
F.append(('Der Scheinwerfer', 'Eine dunkle Bühne: ein warmer Lichtkreis wandert beim Scrollen von Satz zu Satz. Der Satz im Licht steht hell, die anderen warten im Halbdunkel, bis sie dran sind.', sec(11, 'nacht', '''<div class="vi">%s<div class="zv11 auf"><i class="zv11-licht"></i>%s</div></div>''' % (
    kopf(cls='mitte', kick='Bühne frei', text='Live-Musik gehört zu Dirty Chicken. Die Sätze bekommen hier ihren Auftritt.'),
    ''.join('<div class="zv11-s %s"><p>%s</p>%s</div>' % ('l' if i % 2 == 0 else 'r', q(s), datum(d)) for i, (s, _h, d, _k, _p) in enumerate(Z))))))

# 12 Unter der Glocke: ein Teller mit silberner Glocke; die Glocke hebt sich und darunter liegt der Satz; antippen serviert den nächsten
F.append(('Unter der Glocke', 'Serviert wie im Restaurant: ein Teller unter einer silbernen Glocke. Die Glocke hebt sich, und auf dem Teller liegt der Satz. Antippen deckt ab und serviert den nächsten, das Bild daneben wechselt mit.', sec(12, 'warm', '''<div class="vi zv12"><div class="zv12-links">%s<button type="button" class="zv12-knopf">Nächster Satz <i>%s</i></button><p class="mono zv12-nr">1 / 5</p></div>
<div class="zv12-tisch auf" data-akt="0"><div class="zv12-teller"><div class="zv12-saetze">%s</div></div><svg class="zv12-glocke" viewBox="0 0 400 260" aria-hidden="true"><defs><linearGradient id="zv12g" x1="0" x2="1"><stop offset="0" stop-color="#7C7A86"/><stop offset=".35" stop-color="#E9E7EE"/><stop offset=".55" stop-color="#B8B5C2"/><stop offset="1" stop-color="#5E5C68"/></linearGradient></defs>
<path d="M30 236 C30 120 110 48 200 48 C290 48 370 120 370 236 Z" fill="url(#zv12g)"/><rect x="14" y="230" width="372" height="16" rx="8" fill="#8F8C99"/><circle cx="200" cy="36" r="16" fill="#C9C6D1"/><rect x="194" y="40" width="12" height="14" fill="#A7A4B0"/></svg>
<div class="zv12-bild">%s</div></div></div>''' % (
    kopf(kick='Serviert', titel=('Unter', 'der Glocke.'), text='Jeder Satz wird einzeln serviert. Antippen bringt den nächsten.'), bau.PFEIL,
    ''.join('<div class="zv12-s" data-s="%d"><p>%s</p>%s</div>' % (i, q(s), datum(d)) for i, (s, _h, d, _k, _p) in enumerate(Z)),
    ''.join('<div class="zv12-b" data-s="%d">%s</div>' % (i, foto(k, '', '(max-width:860px) 40vw, 16vw', auf=False, pos='50% 40%', extra='style="--weg:0px"')) for i, k in enumerate(B))))))

# 13 Der Flash-Bogen: wie ein Bogen mit Tattoo-Motiven, jeder Satz auf geschwungenen Bändern, dazu Zeichen, Stern und Herz in feiner Linie
def band(t, fs=34, h=58):
    w = int(len(roh(t)) * fs * .64) + 90
    mid = 14 + h // 2
    return ('<svg class="zv13-band" viewBox="0 0 %d %d" style="--w:%d">' % (w, h + 16, w) +
            '<path class="zv13-ende" d="M0 14 H44 V%d H0 L16 %d Z"/>' % (h + 14, mid) +
            '<path class="zv13-ende" d="M%d 14 H%d L%d %d L%d %d H%d Z"/>' % (w - 44, w, w - 16, mid, w, h + 14, w - 44) +
            '<path class="zv13-form" d="M22 2 H%d V%d H22 Z"/>' % (w - 22, h) +
            '<text x="%d" y="%d" text-anchor="middle" textLength="%d" lengthAdjust="spacingAndGlyphs">%s</text></svg>' % (w // 2, h // 2 + fs // 3 + 1, w - 84, E(roh(t).upper())))
MOTIV = ['<svg class="zv13-motiv" viewBox="0 0 100 100"><polygon points="50,4 61,38 96,38 68,59 79,93 50,72 21,93 32,59 4,38 39,38"/></svg>',
         None,
         '<svg class="zv13-motiv" viewBox="0 0 100 100"><path d="M50 88 C20 66 6 50 6 32 C6 18 17 8 30 8 C40 8 47 14 50 22 C53 14 60 8 70 8 C83 8 94 18 94 32 C94 50 80 66 50 88 Z"/></svg>',
         '<svg class="zv13-motiv" viewBox="0 0 100 100"><polygon points="50,2 58,30 88,12 70,40 98,50 70,60 88,88 58,70 50,98 42,70 12,88 30,60 2,50 30,40 12,12 42,30"/></svg>',
         None]
F.append(('Der Flash-Bogen', 'Wie ein Bogen mit Tattoo-Motiven an der Wand eines Studios: Jeder Satz steht auf geschwungenen Bändern, dazu Stern, Herz und das Zeichen in Violett und Orange mit schwarzer Linie. Die Motive werden beim Ankommen nacheinander aufgedrückt.', sec(13, 'hell', '''<div class="vi">%s<div class="zv13-bogen auf"><p class="zv13-kopf mono">Flash · Dirty Chicken · Juni 2026</p><div class="zv13-feld">%s</div></div></div>''' % (
    kopf(kick='Für die Ewigkeit', titel=('Gestochen', 'scharf.'), text='Was Dirty Chicken sagt, würde man sich stechen lassen. Fünf Sätze als Motive.'),
    ''.join('<div class="zv13-m m%d" style="--i:%d">%s%s%s</div>' % (i, i, MOTIV[i] or d_zeichen('zv13-motiv zv13-d'), ''.join(band(t) for t in PB[i]), datum(Z[i][2])) for i in range(5))))))

# 14 Das Typoplakat: alle Sätze als ein Plakat aus Schrift, jede Zeile so gross, dass sie die ganze Breite füllt; Titelschrift und Versalien im Wechsel
ZL = [('Dit is keen Burger.', 'a'), ('Dit Ding is ’ne Ansage.', 'b'), ('Dirty Food &amp; Dirty Drinks.', 'a'), ('Jenau meen Ding wa.', 'c'),
      ('Wenn aus Freunden und Kollegen', 'a'), ('Familie wird.', 'b'), ('Dann haste allet richtig jemacht!', 'a'), ('Opening 2026!', 'c'), ('Wat ne Sause.', 'b'), ('Dit ist wahre Liebe!', 'a')]
DAT14 = {1: Z[0][2], 3: Z[1][2], 6: Z[2][2], 8: Z[3][2], 9: Z[4][2]}
F.append(('Das Typoplakat', 'Alle fünf Sätze als ein Plakat aus Schrift: jede Zeile genau so gross, dass sie die ganze Breite füllt, Titelschrift, violette Versalien und Umrisslinie im Wechsel, das Datum klein am Rand. Die Zeilen schieben sich abwechselnd von links und rechts in die Breite.', sec(14, 'nacht', '<div class="vi">%s</div><div class="vi zv14 auf">%s</div>' % (
    kopf(text=''), ''.join('<div class="zv14-z %s %s" style="--j:%d"><span class="zv14-t">%s</span>%s</div>' % (art, 'l' if j % 2 == 0 else 'r', j, t, datum(DAT14[j], 'zv14-d') if j in DAT14 else '') for j, (t, art) in enumerate(ZL))))))

# 15 Die Schreibmaschine: ein Brief auf Papier mit dem Kopf von Dirty Chicken; beim Scrollen tippt die Maschine die Sätze Buchstabe für Buchstabe
def getippt(s):
    return ''.join('<span>%s</span>' % (E(c) if c != ' ' else ' ') for c in roh(s))
F.append(('Die Schreibmaschine', 'Ein Brief auf hellem Papier mit dem Kopf von Dirty Chicken: Beim Scrollen tippt die Schreibmaschine die fünf Sätze Buchstabe für Buchstabe, die noch nicht getippten stehen blass vorgezeichnet. Unten die Unterschrift.', sec(15, 'warm', '''<div class="vi zv15"><div class="zv15-links">%s</div><div class="zv15-papier auf"><div class="zv15-kopf">%s<div><b>Dirty Chicken</b><span>Sandwiches &amp; More · Hannover</span></div></div>
<p class="zv15-ort mono">Hannover, im Juni 2026</p><div class="zv15-text">%s</div><p class="zv15-gruss">Euer Dirty Chicken</p></div></div>''' % (
    kopf(kick='Schwarz auf weiss', titel=('Getippt,', 'wie jesagt.'), text='Scrollen tippt weiter. Jeder Satz so, wie er auf Instagram stand.'), d_zeichen('zv15-z'),
    ''.join('<p class="zv15-s" aria-label="%s">%s</p>' % (E(roh(s)), getippt(s)) for s, _h, d, _k, _p in Z)))))


def main():
    import zitate_rahmen
    kb = zitate_rahmen.seite('dirty-chicken-zitate-wahl-3.html', 'zitate3', 'Zitate 3', F, 'dc-zitate-wahl-3.css', 'dc-zitate-wahl-3.js', 'Zitate wählen, Runde 3 · Dirty Chicken')
    json.dump([{'nr': i, 'name': n, 'satz': s_} for i, (n, s_, _h) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'zitate3-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite dirty-chicken-zitate-wahl-3.html', kb, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
