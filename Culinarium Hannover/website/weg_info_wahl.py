#!/usr/bin/env python3
"""Culinarium Hannover · Der Weg: der Info-Kopf von «So findest du hin.» in 10 Fassungen zur Wahl (28.10.2026).
Robert: «10 verschiedene Darstellungsmöglichkeiten für den Info-Kopf da.» Gemeint ist nur der Kopf des Abschnitts
(Titel, Satz, Adresse, Plus Code, Culinarium-Zeiten); die Bildwand mit der Bar-Karte darunter bleibt in jeder Fassung gleich.
Jede Fassung ein anderes Gerüst, gezogen und gegengeprüft mit der Entwurfs-Maschine (anreise), kein Nummern-Raster, keine Pillen,
ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Angaben nur aus varianten.py (WEG_DATEN); «Ecke Rampenstraße» steht auf dem Strassenschild im Foto ecke.
Baut weg-info-wahl.html aus der echten weg.html (Leiste unten, Pfeiltasten, ?info=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/weg_info_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, sw

HIER = bau.HIER
MAPS = 'https://www.google.com/maps/search/?api=1&query=Walk+on+the+Wild+Side+Haasemannstra%C3%9Fe+13+30449+Hannover'
TITEL = 'So findest du hin.'
SATZ = 'Die Bar liegt an der Hausecke, am Schild mit Walk on the Wild Side erkennst du sie.'
HAUS = 'Walk on the Wild Side'
STRASSE = 'Haasemannstraße 13'
ORT = '30449 Hannover'
PLUS = '9PC7+49 Hannover'
ZEITEN = [('Freitag', 'ab 19:00'), ('Samstag', 'ab 17:00')]


def titel(zeilen=(TITEL,), cls='', i0=0, tag='h2'):
    return zl(list(zeilen), tag, ('wi-t ' + cls).strip(), i0)


def satz(text=SATZ, i=1, cls=''):
    return sw(text, 'p', ('wi-s ' + cls).strip(), i)


def kick(text, i=0, cls=''):
    return sw(text, 'p', ('wi-k ' + cls).strip(), i)


def gruppe(label, zeilen, i=2, cls=''):
    """Mono-Etikett, darunter die Zeilen in der Titelschrift."""
    return '<div class="wi-g %s sw auf" style="--i:%d"><p class="mono">%s</p><p class="wi-w">%s</p></div>' % (cls, i, label, '<br>'.join(zeilen))


def zeiten_zeilen():
    return ['%s %s' % (t, z) for t, z in ZEITEN]


F = []

# 1 Die Hausecke: der Titel links, rechts die Ecke als zwei Linien in Kerze, Haasemannstraße und Rampenstraße daran, die Bar als Punkt an der Ecke
F.append(('Die Hausecke', 'Die Ecke, an der die Bar liegt, als zwei gezeichnete Linien: Haasemannstraße quer, Rampenstraße hinunter, die Bar als leuchtender Punkt an der Ecke; die Linien ziehen sich beim Ankommen.', '''<div class="wi01"><div class="wi01-l">%s%s</div>
<div class="wi01-ecke auf" aria-label="Die Hausecke Haasemannstraße, Ecke Rampenstraße"><span class="wi01-h"></span><span class="wi01-v"></span><span class="wi01-punkt"></span>
<p class="mono wi01-s1">Haasemannstraße</p><p class="mono wi01-s2">Rampenstraße</p>
<div class="wi01-adr"><p class="wi-w">%s<br>%s<br>%s</p></div>
<div class="wi01-unten"><p class="mono">Plus Code</p><p class="wi-w">%s</p><p class="mono wi01-m2">Culinarium</p><p class="wi-w">%s</p></div></div></div>''' % (
    titel(), satz(), HAUS, STRASSE, ORT, PLUS, '<br>'.join(zeiten_zeilen()))))

# 2 Die Adresse zuerst: die Strasse wird zum Titel, riesig über die ganze Breite; «So findest du hin» ist die Zeile darüber, darunter Satz, Plus Code und Zeiten in einer Reihe
# (vorher «Wo, wann, woran» mit drei Fragespalten: laut Entwurfs-Maschine zu 100 % die Anreise des Walk on the Wild Side, darum ersetzt)
F.append(('Die Adresse zuerst', 'Die Strasse ist der Titel: Haasemannstraße 13 riesig über die ganze Breite, «So findest du hin» als Zeile darüber; darunter in einer Reihe der Satz, der Plus Code und die Zeiten.', '''<div class="wi02">%s%s
<div class="wi02-reihe">%s%s%s</div></div>''' % (
    kick(TITEL), zl(['Haasemannstraße 13,', 'Linden.'], 'h2', 'wi-t wi02-t', 0), satz(i=2), gruppe('Plus Code', [PLUS], 3), gruppe('Culinarium', zeiten_zeilen(), 4))))

# 3 Die Einladung: alles auf der Mittelachse wie eine Einladungskarte, eine Kerzenlinie wächst zwischen Titel und Angaben
F.append(('Die Einladung', 'Alles auf der Mittelachse wie auf einer Einladungskarte: Titel, eine Kerzenlinie, die beim Ankommen wächst, die Adresse gross, darunter die Zeiten und der Satz.', '''<div class="wi03">%s%s<span class="wi03-linie auf" aria-hidden="true"></span>
<p class="wi-w wi03-adr sw auf" style="--i:1">%s<br>%s<br>%s</p><p class="mono sw auf" style="--i:2">Plus Code %s</p>
<div class="wi03-zeit sw auf" style="--i:3"><p><span class="mono">Freitag</span><b>ab 19:00</b></p><p><span class="mono">Samstag</span><b>ab 17:00</b></p></div>%s</div>''' % (
    kick('Culinarium im Walk on the Wild Side', 0, 'mitte'), titel(cls='mitte'), HAUS, STRASSE, ORT, PLUS, satz(i=4, cls='mitte'))))

# 4 Ab 19 Uhr: die beiden Uhrzeiten riesig, der Titel wird zur Zeile darüber, Adresse und Plus Code darunter
F.append(('Ab 19 Uhr', 'Die beiden Uhrzeiten stehen riesig wie eine Leuchtanzeige, Freitag und Samstag als Etikett darüber; der Titel wird zur Zeile, Adresse und Plus Code stehen darunter.', '''<div class="wi04"><div class="wi04-l">%s%s</div>
<div class="wi04-r"><div class="wi04-z"><p class="mono sw auf" style="--i:0">Freitag ab</p>%s</div><div class="wi04-z"><p class="mono sw auf" style="--i:1">Samstag ab</p>%s</div></div></div>
<div class="wi04-unten">%s%s%s</div>''' % (
    kick(TITEL), satz(), zl(['19:00'], 'p', 'wi04-n', 0), zl(['17:00'], 'p', 'wi04-n', 1),
    gruppe('Adresse', [HAUS, STRASSE, ORT], 2), gruppe('Plus Code', [PLUS], 3), gruppe('Ecke', ['Haasemannstraße,', 'Ecke Rampenstraße'], 4))))

# 5 Senkrecht: der Titel läuft senkrecht am linken Rand, rechts die Angaben gross untereinander
F.append(('Senkrecht', 'Der Titel steht senkrecht am linken Rand und fährt beim Ankommen an der Kante hoch; rechts davon die Angaben gross untereinander, dazwischen eine feine Linie.', '''<div class="wi05"><h2 class="wi05-t auf" aria-label="%s">%s</h2>
<div class="wi05-r">%s%s%s%s</div></div>''' % (
    E(TITEL), TITEL, gruppe('Adresse', [HAUS, STRASSE, ORT], 0, 'wi05-g'), gruppe('Plus Code', [PLUS], 1, 'wi05-g'),
    gruppe('Culinarium', zeiten_zeilen(), 2, 'wi05-g'), satz(i=3))))

# 6 Wie auf der Karte: die Angaben als Speisekarte, Etikett links, Punktlinie, Wert rechts
F.append(('Wie auf der Karte', 'Die Angaben gesetzt wie die Menükarte des Abends: Etikett links, eine Punktlinie, der Wert rechts in der Titelschrift; die Zeilen kommen eine nach der anderen.', '''<div class="wi06"><div class="wi06-l">%s%s</div>
<dl class="wi06-k">%s</dl></div>''' % (
    titel(), satz(), ''.join('<div class="sw auf" style="--i:%d"><dt class="mono">%s</dt><i aria-hidden="true"></i><dd>%s</dd></div>' % (i, a, b) for i, (a, b) in enumerate([
        ('Haus', HAUS), ('Adresse', STRASSE), ('Ort', ORT + ', Linden'), ('Plus Code', PLUS), ('Freitag', 'ab 19:00'), ('Samstag', 'ab 17:00')])))))

# 7 Der eine Satz: alle Angaben in einem grossen Satz über die ganze Breite, die Zahlen in Kerze
F.append(('Der eine Satz', 'Keine Felder: Adresse, Hausecke, Schild und Zeiten stehen in einem einzigen grossen Satz über die ganze Breite, die Zahlen in Kerzenfarbe; die Zeilen kommen aus dem Schlitz.', '''<div class="wi07"><div class="wi07-kopf sw auf" style="--i:0"><span class="mono">%s</span><span class="mono">Plus Code %s</span></div>
%s</div>''' % (
    TITEL, PLUS, zl(['<em>Haasemannstraße 13</em> in Linden,', 'die Bar an der Hausecke, am Schild', 'mit Walk on the Wild Side erkennst du sie.', '<em>Freitag ab 19</em>, <em>Samstag ab 17 Uhr</em>.'], 'p', 'wi07-satz', 0))))

# 8 Das Zeichen: das Zeichen der Bar gross links, rechts Titel, Satz und die drei Angaben in einer Reihe
F.append(('Das Zeichen', 'Das Zeichen der Bar steht gross links, wie das Schild an der Ecke; rechts Titel und Satz, darunter Adresse, Plus Code und Zeiten in einer Reihe.', '''<div class="wi08"><div class="wi08-z auf"><svg viewBox="0 0 1296 1600" role="img" aria-label="Walk on the Wild Side"><use href="assets/zeichen/haus.svg?v=%s#ws"/></svg></div>
<div class="wi08-r">%s%s<div class="wi08-d">%s%s%s</div></div></div>''' % (
    VERSION, titel(), satz(), gruppe('Adresse', [HAUS, STRASSE, ORT], 2), gruppe('Plus Code', [PLUS], 3), gruppe('Culinarium', zeiten_zeilen(), 4))))

# 9 Die Dachzeile: die Angaben als eine Mono-Zeile zwischen zwei Linien über dem Titel, der Titel darunter riesig, der Satz rechts
F.append(('Die Dachzeile', 'Dicht wie ein Zeitungskopf: oben eine Zeile mit allen Angaben zwischen zwei Linien, darunter der Titel über die ganze Breite riesig, der Satz rechts darunter.', '''<div class="wi09"><p class="wi09-dach sw auf" style="--i:0"><span>%s</span><span>%s</span><span>%s</span><span>%s</span><span>Freitag ab 19:00</span><span>Samstag ab 17:00</span></p>
%s<div class="wi09-s">%s</div></div>''' % (
    HAUS, STRASSE, ORT, PLUS, titel(cls='wi09-t', i0=1), satz(i=2))))

# 10 Anstossen: zwei gleich grosse Platten, dunkel und warmweiss, steigen getrennt herauf und treffen an der Kerzennaht
F.append(('Anstossen', 'Zwei gleich grosse Platten: links dunkel mit Titel und Satz, rechts warmweiss mit den Angaben; sie steigen getrennt herauf, die rechte einen Wimpernschlag später, und treffen an der Kerzennaht.', '''<div class="wi10"><div class="wi10-p l auf">%s%s</div><span class="wi10-naht" aria-hidden="true"></span>
<div class="wi10-p r auf">%s%s%s</div></div>''' % (
    titel(cls='wi10-t'), satz(), gruppe('Adresse', [HAUS, STRASSE, ORT], 0, 'wi10-g'), gruppe('Plus Code', [PLUS], 1, 'wi10-g'), gruppe('Culinarium', zeiten_zeilen(), 2, 'wi10-g'))))


def main():
    seite = open(os.path.join(HIER, 'weg.html'), encoding='utf-8').read()
    a = seite.find('<section class="vab bar-ab v-weg-abends')
    assert a >= 0, 'Abschnitt «So findest du hin» in weg.html nicht gefunden (erst bau.py und varianten.py laufen lassen)'
    e = seite.find('</section>', a) + len('</section>')
    m = re.match(r'<section class="([^"]+)"([^>]*)>(.*)</section>', seite[a:e], re.S)
    inner = m.group(3)
    g = inner.find('</dl></div>')          # Ende der Angaben (fwk-extra); danach kommt die Bildwand, wie auch immer sie gerade gebaut ist (28.10.: Aufkleber)
    assert g >= 0, 'Angaben (weg-daten) im Abschnitt nicht gefunden'
    wand = inner[g + len('</dl></div>'):]   # Bildwand mit der Bar-Karte: bleibt in jeder Fassung gleich
    attrs = m.group(2).replace(' data-lauf=""', '')
    teile = ['<div class="wv" data-n="0"><section class="%s"%s>%s</section></div>' % (m.group(1), attrs, inner)]
    for i, (_n, _s, kopf) in enumerate(F, 1):
        sec = '<section class="%s wi wis%02d"%s><div class="vi h-wand2"><div class="wi-kopf">%s</div>%s</section>' % (m.group(1), i, attrs, kopf, wand)
        # die Bildwand endet mit </div></div> (vi); der Kopf sitzt davor, also die schliessenden Tags der vi gehören zur Wand
        teile.append('<div class="wv" data-n="%d" hidden>%s</div>' % (i, sec))
    neu = '<section class="ww wahl" data-ton="nacht" id="info" data-name="Info-Kopf"><div class="wahl-marke"><b>Info-Kopf</b><span data-nr></span></div>' + ''.join(teile) + '</section>'
    seite = seite[:a] + neu + seite[e:]
    namen = ['Heute: Titel links, Satz rechts, Angaben in zwei Spalten'] + [n for n, _s, _k in F]
    v = VERSION + 'r%d' % os.path.getmtime(os.path.join(HIER, 'assets', 'weg-info-wahl.css'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["info"],daumen:%s};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script>
/* Beim Aufruf mit ?info=Nummer sieht der Beobachter die zuerst versteckte Fassung nicht immer: ihre Auftritte anstossen */
(function(){function wecke(){var f=document.querySelector('#info>.wv:not([hidden]) .wi');if(f)setTimeout(function(){f.querySelectorAll('.auf:not(.da)').forEach(function(x){var r=x.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0)x.classList.add('da');});},120);}
addEventListener('load',wecke);document.addEventListener('click',wecke);addEventListener('keydown',wecke);addEventListener('scroll',wecke,{passive:true});})();
</script>''' % (json.dumps(namen, ensure_ascii=False), 'true' if os.path.exists(os.path.join(HIER, 'assets/daumen/info-1.jpg')) else 'false', VERSION)
    seite = seite.replace('<title>', '<title>Info-Kopf wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/weg-info-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'weg-info-wahl.html'), 'w', encoding='utf-8').write(seite)
    os.makedirs(os.path.join(HIER, '_sicherung'), exist_ok=True)
    json.dump([{'nr': i, 'name': n, 'satz': s_} for i, (n, s_, _k) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'weg-info-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite weg-info-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
