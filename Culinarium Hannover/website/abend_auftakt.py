#!/usr/bin/env python3
"""Culinarium Hannover · Seite «Der Abend»: 15 Fassungen des Auftakts zum Durchklicken (Robert 26.10.2026 zum heutigen Auftakt: «der Hero Müll»).
Liest die fertige abend.html (nach bau.py / varianten.py), ersetzt den ersten Abschnitt durch einen Rahmen mit Fassung 0 (heutiger Stand)
und den Fassungen 1 bis 15, bindet assets/abend-auftakt.css und .js ein. Pfeiltasten ← →, schmale Leiste unten mit Nummer und Vorschaubild,
Stand in der Adresse (?f=N), beim Wechsel bleibt man oben.
Jede Fassung hat eine eigene Anordnung und genau einen eigenen bewegten Moment; nur transform und opacity, nativer Scroll.
Fakten nur aus dem Auftrag und den Quellen der Seite (Food-Pairing, lange Tafel, drei Gänge, fünf Signature Drinks, vierzehn Plätze,
freitags ab 19 Uhr, samstags ab 17 Uhr, zuletzt 25./26. September 2026 ausgebucht, nächster Termin offen). Kein Preis im Auftakt (Kern Abschnitt 4).
Aufruf: python3 website/abend_auftakt.py   (läuft auch am Ende von varianten.py)
Vorschaubilder: python3 website/abend_auftakt.py daumen   (nimmt jede Fassung unsichtbar in WebKit auf, Playwright aus ~/Aussen-Pruefung)"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, BILD, VERSION, knopf, marke

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))
bau.META.update(META)
ANF, END = '<!--abend-auftakt-->', '<!--/abend-auftakt-->'


def b(k, sizes, cls='', pos=None, attr=''):
    """Foto ohne die Auftritte der Seite: jede Fassung bewegt ihre Bilder selbst. Geladen wird erst beim Zeigen der Fassung."""
    m = META[k]
    _q, p, alt = BILD[k]
    srcset = ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in m['stufen'])
    return ('<figure class="aa-b%s" style="--lq:url(%s)"%s><img data-aa="%s" sizes="%s" alt="%s" decoding="async" style="object-position:%s"></figure>'
            % ((' ' + cls) if cls else '', m['lq'], attr, srcset, sizes, E(alt), pos or p))


def zl(zeilen, cls='aa-titel', tag='h1', i0=0):
    """Überschrift, zeilenweise aus dem Schlitz."""
    t = ' '.join(re.sub('<[^>]+>', '', z) for z in zeilen)
    inner = ''.join('<span class="aa-z"><span style="--i:%d">%s</span></span>' % (i0 + i, z) for i, z in enumerate(zeilen))
    return '<%s class="%s" aria-label="%s">%s</%s>' % (tag, cls, E(t), inner, tag)


def sw(text, i, cls='aa-satz', tag='p'):
    return '<%s class="aa-sw %s" style="--i:%d">%s</%s>' % (tag, cls, i, text, tag)


def kn(i, cls=''):
    return '<div class="aa-sw aa-kn" style="--i:%d">%s</div>' % (i, knopf('Auf die Warteliste', '#warteliste', cls))


def rudi(z):
    """Zeile in der Schreibweise von Rudis Karten, der Schrägstrich in Kerze."""
    return E(z).replace(' /', '&#160;<i>/</i>')


SATZ = 'Food-Pairing-Abende an der langen Tafel im Walk on the Wild Side, Hannover-Linden: drei Gänge, fünf Signature Drinks, vierzehn Plätze.'
KURZ = 'Food-Pairing-Abende an der langen Tafel im Walk on the Wild Side, Hannover-Linden.'
ZEIT = '<span>Freitag ab 19 Uhr</span><span>Samstag ab 17 Uhr</span>'
ZULETZT = 'Zuletzt am 25. und 26. September 2026, ausgebucht. Der nächste Termin steht noch nicht fest.'

WAHL = 5   # Robert 26.10.2026: «5» (Von oben); 0 = alle Fassungen zum Durchklicken
F = []   # (Name, Klasse, Inhalt)

# 1 Anstossen: Glas und Teller, gross Wand an Wand; zwei Bilder steigen getrennt herauf und kommen an der Naht zusammen (Bewegungsidee des Hauses)
F.append(('Anstoßen', 'aa1', '''<div class="aa1-paar"><div class="aa1-l">%s</div><div class="aa1-r">%s</div></div>
<div class="aa1-text">%s<div class="aa1-unten">%s%s%s</div></div>''' % (
    b('glas', '(max-width:860px) 100vw, 50vw', pos='50% 62%'), b('r07', '(max-width:860px) 100vw, 50vw', pos='50% 60%'),
    zl(['Culinarium.'], 'aa-titel aa-schatten aa1-t'), sw(SATZ, 2, 'aa-satz aa-schatten'), sw(ZEIT, 3, 'aa-info aa-schatten'), kn(4))))

# 2 Lichter an: der Abend liegt im Dunkeln, die Bilder gehen nacheinander an wie Kerzen
VIER = [('loch', '50% 50%'), ('schaumglas', '50% 40%'), ('kerze3', '50% 45%'), ('barlicht', '50% 55%')]
F.append(('Lichter an', 'aa2', '''<div class="aa2-gross">%s<i class="aa2-hof"></i><i class="aa2-s" style="--i:0"></i>
<div class="aa2-text">%s%s%s%s</div></div>
<div class="aa2-vier">%s</div>''' % (
    b('tafelleer', '(max-width:860px) 100vw, 46vw', pos='50% 46%'),
    zl(['Der Abend.'], 'aa-titel aa-schatten'), sw(SATZ, 2, 'aa-satz aa-schatten'), sw(ZEIT, 3, 'aa-info aa-schatten'), kn(4),
    ''.join('<div class="aa2-z">%s<i class="aa2-s" style="--i:%d"></i></div>' % (b(k, '(max-width:860px) 50vw, 28vw', pos=p), i + 1) for i, (k, p) in enumerate(VIER)))))

# 3 Vor dem Namen: der Name steht gross im Raum, das Foto steigt davor auf
F.append(('Vor dem Namen', 'aa3', '''<h1 class="aa3-wort" aria-label="Culinarium"><span class="aa-z"><span style="--i:0">Culinarium</span></span></h1>
<div class="aa3-bild">%s</div>
<div class="aa3-links">%s%s</div>
<dl class="aa3-rechts aa-sw" style="--i:3"><div><dt>Freitag</dt><dd>ab 19 Uhr</dd></div><div><dt>Samstag</dt><dd>ab 17 Uhr</dd></div><div><dt>Plätze</dt><dd>14 an einer Tafel</dd></div></dl>''' % (
    b('toast', '(max-width:860px) 70vw, 34vw', pos='50% 40%'), sw(SATZ, 2), kn(4))))

# 4 Drei, fünf, vierzehn: die drei Zahlen des Abends, jede mit ihrem Bild; die Zahlen zählen hoch
ZAHLEN = [('r09', '50% 50%', 3, 'Gänge', 'aus der Küche von Rudi Napieraj'), ('g1', '50% 42%', 5, 'Drinks', 'Signature Drinks von Momo'),
          ('tafelleer', '50% 50%', 14, 'Plätze', 'an einer langen Tafel')]
F.append(('Drei, fünf, vierzehn', 'aa4', '''<div class="aa4-kopf">%s%s</div>
<div class="aa4-reihe">%s</div>
<div class="aa4-fuss">%s%s</div>''' % (
    zl(['Der Abend.'], 'aa-titel aa4-t'), sw(KURZ, 1),
    ''.join('<div class="aa4-sp" style="--i:%d"><div class="aa4-rahmen">%s</div><p class="aa4-zahl"><b data-aa-zahl="%d">%d</b><span>%s</span></p><p class="aa4-wer">%s</p></div>'
            % (i, b(k, '(max-width:860px) 33vw, 24vw', pos=p), n, n, w, wer) for i, (k, p, n, w, wer) in enumerate(ZAHLEN)),
    sw(ZEIT, 5, 'aa-info'), kn(6))))

# 5 Von oben: der Tisch von oben, in der Mitte die Karte, rundherum die Teller; serviert wird reihum
TELLER = [('lauch', '50% 50%'), ('roq1', '50% 55%'), ('r05', '50% 50%'), ('r09', '50% 50%')]   # oben links, oben rechts, unten rechts, unten links
# Reihenfolge (Robert 28.10.2026): unten links, oben rechts, oben links, unten rechts. Stand davor *.vor-hero-reihenfolge-2026-10-28
F.append(('Von oben', 'aa5', '''<div class="aa5-z aa5-1" style="--i:2">%s</div><div class="aa5-z aa5-2" style="--i:1">%s</div>
<div class="aa5-karte"><div class="aa5-wm aa-sw" style="--i:0">%s</div>%s%s%s%s</div>
<div class="aa5-z aa5-3" style="--i:3">%s</div><div class="aa5-z aa5-4" style="--i:0">%s</div>''' % (
    b(TELLER[0][0], '(max-width:860px) 50vw, 34vw', pos=TELLER[0][1]), b(TELLER[1][0], '(max-width:860px) 50vw, 34vw', pos=TELLER[1][1]),
    marke('wm'), zl(['Drei Gänge,', 'fünf Drinks.'], 'aa-titel aa5-t', i0=1), sw(KURZ, 3), sw(ZEIT, 4, 'aa-info'), kn(5),
    b(TELLER[2][0], '(max-width:860px) 50vw, 34vw', pos=TELLER[2][1]), b(TELLER[3][0], '(max-width:860px) 50vw, 34vw', pos=TELLER[3][1]))))

# 6 Im Dunkeln: ein Glas in der Mitte, links und rechts die Speisefolge in der Schreibweise von Rudis Karten, Zeile für Zeile
F.append(('Im Dunkeln', 'aa6', '''<div class="aa6-glas">%s</div><div class="aa6-wm aa-sw" style="--i:0">%s</div>
<div class="aa6-l">%s%s</div><div class="aa6-r">%s%s</div>''' % (
    b('glas', '(max-width:860px) 100vw, 40vw', pos='50% 50%'), marke('wm'),
    zl([rudi('APERITIF /'), rudi('DREI GÄNGE /')], 'aa6-zeilen', i0=1), sw(SATZ, 6),
    zl([rudi('FÜNF DRINKS /'), rudi('VIERZEHN PLÄTZE')], 'aa6-zeilen', 'p', i0=3), '<div class="aa6-fuss">%s%s</div>' % (sw(ZEIT, 6, 'aa-info'), kn(7)))))

# 7 Band: oben der Name, darunter laufen Glas und Teller im Wechsel langsam vorbei
BAND = [('g1', '50% 42%'), ('r09', '50% 50%'), ('g3', '50% 50%'), ('roq1', '50% 55%'), ('g4', '50% 50%'), ('r01', '50% 50%'),
        ('d1', '50% 55%'), ('r07', '50% 50%'), ('coupe', '50% 50%'), ('r10', '50% 50%')]
band = ''.join(b(k, '(max-width:860px) 46vw, 24vw', pos=p) for k, p in BAND)
F.append(('Band', 'aa7', '''<div class="aa7-kopf">%s<div class="aa7-text">%s<div class="aa7-reihe">%s%s</div></div></div>
<div class="aa7-band"><div class="aa7-lauf">%s%s</div></div>''' % (
    zl(['Culinarium.'], 'aa-titel aa7-t'), sw(SATZ, 1), sw(ZEIT, 2, 'aa-info'), kn(3),
    band, band.replace('<img ', '<img aria-hidden="true" '))))

# 8 Halb und halb: links der Raum gross, er setzt sich langsam in seinen Rahmen; rechts die Karte des Abends über einem Teller
F.append(('Halb und halb', 'aa8', '''<div class="aa8-gross">%s</div>
<div class="aa8-rechts"><div class="aa8-text">%s%s%s%s</div><div class="aa8-klein">%s</div></div>''' % (
    b('t08', '(max-width:860px) 100vw, 58vw', pos='50% 52%'),
    zl(['Der Abend.'], 'aa-titel'), sw(SATZ, 1), sw(ZEIT, 2, 'aa-info'), kn(3),
    b('r06', '(max-width:860px) 100vw, 42vw', pos='50% 50%'))))

# 9 Zwei Abende: Freitag und Samstag, je eine Hälfte; die Uhrzeit rollt in ihre Stelle
def rolle(z, i):
    """Eine Ziffer, die von unten durch 0 bis z in ihre Stelle rollt; die Breite gibt die Ziffer selbst vor."""
    return '<span class="aa9-ziffer"><span class="aa9-mass">%s</span><span class="aa9-rolle" style="--n:%s;--i:%d">%s</span></span>' % (z, z, i, '<br>'.join(str(x) for x in range(10)))
F.append(('Zwei Abende', 'aa9', '''<div class="aa9-h aa9-fr">%s<i class="aa9-hof"></i><div class="aa9-zeit" aria-label="Freitag ab 19 Uhr"><span class="aa9-tag">Freitag ab</span><span class="aa9-uhr">%s%s<em>Uhr</em></span></div></div>
<div class="aa9-h aa9-sa">%s<i class="aa9-hof"></i><div class="aa9-zeit" aria-label="Samstag ab 17 Uhr"><span class="aa9-tag">Samstag ab</span><span class="aa9-uhr">%s%s<em>Uhr</em></span></div></div>
<div class="aa9-oben">%s%s%s</div>''' % (
    b('fassade', '(max-width:860px) 100vw, 50vw', pos='50% 46%'), rolle(1, 0), rolle(9, 1),
    b('kerze3', '(max-width:860px) 100vw, 50vw', pos='50% 50%'), rolle(1, 2), rolle(7, 3),
    zl(['Culinarium.'], 'aa-titel aa-schatten aa9-t'), sw(SATZ, 1, 'aa-satz aa-schatten'), kn(2))))

# 10 Unter Glas: der Abend als gerahmter Abzug in der Mitte; ein Glanz läuft einmal über das Glas
F.append(('Unter Glas', 'aa10', '''<div class="aa10-links">%s%s%s</div>
<div class="aa10-rahmen"><div class="aa10-bild">%s<i class="aa10-glanz"></i></div></div>
<dl class="aa10-rechts aa-sw" style="--i:3"><div><dt>Drei Gänge</dt><dd>aus der Küche</dd></div><div><dt>Fünf Drinks</dt><dd>Signature Drinks von Momo</dd></div><div><dt>Vierzehn Plätze</dt><dd>an einer langen Tafel</dd></div><div><dt>Freitag · Samstag</dt><dd>ab 19 Uhr · ab 17 Uhr</dd></div></dl>''' % (
    zl(['Der Abend.'], 'aa-titel'), sw(KURZ, 1), kn(2), b('anstossen', '(max-width:860px) 70vw, 30vw', pos='50% 40%'))))

# 11 Gedeck: Glas, Teller, Dessert in einer Reihe wie gedeckt; die Reihe kommt als Ganzes entgegen
F.append(('Gedeck', 'aa11', '''%s<div class="aa11-reihe"><div class="aa11-a">%s</div><div class="aa11-b">%s</div><div class="aa11-c">%s</div></div>
<div class="aa11-fuss">%s<div class="aa11-zeile">%s%s</div></div>''' % (
    zl(['Culinarium.'], 'aa-titel aa11-t'), b('d2', '(max-width:860px) 50vw, 22vw', pos='50% 50%'), b('pass4', '(max-width:860px) 100vw, 44vw', pos='50% 50%'),
    b('hok2', '(max-width:860px) 50vw, 22vw', pos='50% 50%'), sw(SATZ, 2), sw(ZEIT, 3, 'aa-info'), kn(4))))

# 12 Zwei Tempi: rechts zwei Bildsäulen, die beim Scrollen verschieden schnell wandern
F.append(('Zwei Tempi', 'aa12', '''<div class="aa12-text">%s%s%s%s%s</div>
<div class="aa12-saeulen"><div class="aa12-s aa12-a" data-tempo=".10">%s%s</div><div class="aa12-s aa12-b" data-tempo=".30">%s%s</div></div>''' % (
    zl(['Der', 'Abend.'], 'aa-titel'), sw(SATZ, 2), sw(ZEIT, 3, 'aa-info'), sw(ZULETZT, 4, 'aa-klein'), kn(5),
    b('momo', '(max-width:860px) 46vw, 28vw', pos='50% 30%'), b('g4', '(max-width:860px) 46vw, 28vw', pos='50% 50%'),
    b('r01', '(max-width:860px) 46vw, 28vw', pos='50% 50%'), b('t05', '(max-width:860px) 46vw, 28vw', pos='50% 35%'))))

# 13 Wand: ein dichtes Feld aus Raum, Pass und Glas, die Karte in einer eigenen Kachel; das Feld kommt als Fläche gemeinsam
F.append(('Wand', 'aa13', '''<div class="aa13-feld"><div class="aa13-gross">%s</div><div class="aa13-quer">%s</div><div class="aa13-glas">%s</div>
<div class="aa13-karte">%s%s%s</div></div>''' % (
    b('t09', '(max-width:860px) 100vw, 44vw', pos='50% 50%'), b('pass', '(max-width:860px) 100vw, 56vw', pos='50% 50%'),
    b('g5', '(max-width:860px) 50vw, 28vw', pos='50% 60%'), zl(['Der Abend.'], 'aa-titel aa13-t'), sw(SATZ, 1), kn(2))))

# 14 Von draussen: die Bar bei Nacht von der Strasse, der Blick folgt der Maus durchs Fenster
F.append(('Von draußen', 'aa14', '''<div class="aa14-rahmen"><div class="aa14-bild">%s</div></div>
<div class="aa14-text">%s%s%s%s%s</div>''' % (
    b('barnacht', '(max-width:860px) 140vw, 115vw', pos='50% 60%'),
    zl(['Culinarium.'], 'aa-titel aa14-t'), sw('im Walk on the Wild Side', 1, 'aa14-unter'),
    sw('Haasemannstraße 13, Hannover-Linden. Food-Pairing-Abende an der langen Tafel: drei Gänge, fünf Signature Drinks, vierzehn Plätze.', 2),
    sw(ZEIT, 3, 'aa-info'), kn(4))))

# 15 Der Teller: Rudis Teller von oben, er wird hingestellt und dreht sich ein letztes Stück an seinen Platz
F.append(('Der Teller', 'aa15', '''<div class="aa15-text">%s%s%s%s%s</div>
<div class="aa15-bild"><div class="aa15-dreh">%s</div></div>''' % (
    zl(['Culinarium.'], 'aa-titel'), '<p class="aa-sw aa15-zeile" style="--i:1">%s</p>' % rudi('LAUCH / BLUMENKOHL / CHIPOTLE'),
    sw(SATZ, 2), sw(ZEIT, 3, 'aa-info'), kn(4), b('lauch', '(max-width:860px) 160vw, 90vw', pos='50% 50%'))))


# ------------------------------------------------------------------ Rahmen
def rahmen(heute):
    teile = [] if WAHL else ['<div class="aa-f aa0" data-nr="0" data-name="Heute" hidden>%s</div>' % heute]
    for i, (name, cls, inner) in enumerate(F, 1):
        if WAHL and i != WAHL:   # versandfertig (Robert 28.10.2026): nur die gewählte Fassung, keine versteckten
            continue
        teile.append('<div class="aa-f %s" data-nr="%d" data-name="%s" hidden><div class="aa-buehne">%s</div></div>' % (cls, i, E(name), inner))
    # Fassung sofort beim Lesen der Seite zeigen und ihre Bilder anfordern, nicht erst nach dem Laden des Skripts
    sofort = ('<script>(function(){var s=document.getElementById("auftakt"),n=parseInt(new URLSearchParams(location.search).get("f"),10);'
              'if(%d)n=%d;if(!(n>=0&&n<=%d))n=1;var f=s.querySelector(\'.aa-f[data-nr="\'+n+\'"]\');f.hidden=false;s.dataset.an=n;s.classList.toggle("aa-null",n===0);'
              'if(n)f.querySelectorAll("img[data-aa]").forEach(function(i){i.srcset=i.dataset.aa;i.removeAttribute("data-aa");i.fetchPriority="high"});'
              # Handy (28.10.2026, LCP), seit 30.10.2026 auch am Rechner: nicht auf das Seitenskript warten, die Kacheln kommen, sobald die Bilder da sind, spätestens nach 600 ms
              'if(n&&document.documentElement.classList.contains("js")){var im=f.querySelectorAll(".aa-buehne img"),k=im.length;'
              'function go(){if(f.classList.contains("bereit"))return;f.classList.add("bereit");requestAnimationFrame(function(){requestAnimationFrame(function(){f.classList.add("los")})})}'
              'im.forEach(function(i){if(i.complete&&i.naturalWidth)k--;else i.addEventListener("load",function(){if(--k<=0)go()},{once:true})});if(k<=0)go();setTimeout(go,600)}})()</script>') % (WAHL, WAHL, len(F))
    leiste = ('<nav class="aa-leiste" id="aa-leiste" aria-label="Fassungen des Auftakts"' + (' hidden style="display:none"' if WAHL else '') + '>'
              '<button class="aa-pfeil" type="button" data-aa-schritt="-1" aria-label="Vorige Fassung">‹</button>'
              '<div class="aa-daumen">%s</div>'
              '<button class="aa-pfeil" type="button" data-aa-schritt="1" aria-label="Nächste Fassung">›</button>'
              '<p class="aa-name" aria-live="polite"></p></nav>') % ''.join(
        '<button type="button" data-aa-nr="%d" aria-label="Fassung %d: %s"><img src="assets/abend-auftakt/f%d.jpg?v=%s" alt="" loading="lazy" width="64" height="36"><b>%d</b></button>'
        % (i, i, E(n), i, VERSION, i) for i, n in enumerate(['Heute'] + [x[0] for x in F]))
    if WAHL:
        leiste = ''
    return ('%s<section class="aa" id="auftakt" data-ton="nacht" aria-label="Der Abend"' + (' data-fest="1"' if WAHL else '') + '>%s</section>%s%s%s%s') % (
        ANF, (re.sub(r'<img data-aa="', '<img fetchpriority="high" srcset="', ''.join(teile)) if WAHL else ''.join(teile)), sofort, leiste, fenster(), END)   # feste Fassung: Bilder direkt im HTML, nicht erst per Skript (Handy-LCP 28.10.2026)


def fenster():
    """Fenster zwischen Auftakt und Karte (Robert 26.10.2026 20:08: «kannst du da ein Fenster einbauen?»): das Bild steht, die Seite zieht darüber,
    der Satz mittig mit Schatten. Bauweise und Bewegung wie das Fenster der Startseite (culinarium.css/.js). Satz belegt durch die Karte der Seite
    («Momo stellt zu jedem einen eigenen Drink dazu»). Bild seit 27.10.2026: kartglas (Robert wählte Bild 4 der Fenster-Wahl)."""
    return ('<section class="fenster" id="fenster" aria-label="Erst anstoßen, dann essen"><div class="fenster-schicht">%s<div class="fenster-hof"></div>'
            '<p class="fenster-satz zl"><span class="z"><span style="--i:0">Erst anstoßen,</span></span><span class="z"><span style="--i:1">dann essen.</span></span></p></div></section>'
            % bau.foto('kartglas', '', '100vw', auf=False, pos='50% 35%'))


def main():
    pfad = os.path.join(HIER, 'abend.html')
    h = open(pfad, encoding='utf-8').read()
    if ANF in h:   # schon eingebaut: den heutigen Stand aus Fassung 0 zurückholen
        a, e = h.index(ANF), h.index(END) + len(END)
        alt = h[a:e]
        m0 = re.search(r'<div class="aa-f aa0"[^>]*>(.*?)</div><div class="aa-f ', alt, re.S)
        assert m0, 'abend.html trägt nur die feste Fassung: erst bau.py laufen lassen, dann neu bauen'
        h = h[:a] + m0.group(1) + h[e:]
    m = re.search(r'<section class="vab bar-ab v-kopf.*?</section>', h, re.S)
    assert m, 'Erster Abschnitt in abend.html nicht gefunden (erst bau.py laufen lassen)'
    h = h[:m.start()] + rahmen(m.group(0)) + h[m.end():]
    h = re.sub(r'\n?<link rel="stylesheet" href="assets/abend-auftakt\.css[^>]*>', '', h)
    h = re.sub(r'\n?<script src="assets/abend-auftakt\.js[^>]*></script>', '', h)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/abend-auftakt.css?v=%s">\n</head>' % VERSION, 1)
    h = h.replace('</body>', '<script src="assets/abend-auftakt.js?v=%s" defer></script>\n</body>' % VERSION, 1)
    open(pfad, 'w', encoding='utf-8').write(h)
    print('abend.html: Auftakt mit %d Fassungen,' % len(F), len(h) // 1024, 'KB')


def daumen():
    """Vorschaubilder der Leiste: jede Fassung bei 1440 × 900 in WebKit, ohne Leiste, als 160 × 90."""
    ziel = os.path.join(HIER, 'assets', 'abend-auftakt')
    os.makedirs(ziel, exist_ok=True)
    js = r'''
const path=require('path'),os=require('os');module.paths.push(path.join(os.homedir(),'Aussen-Pruefung','node_modules'));
const pw=require('playwright');
(async()=>{const [url,ziel,n]=process.argv.slice(2);const br=await pw.webkit.launch({headless:true});
const pg=await (await br.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1})).newPage();
for(let i=0;i<=+n;i++){await pg.goto(url+'?f='+i,{waitUntil:'load'});await pg.addStyleTag({content:'.aa-leiste{display:none!important}'});
await pg.waitForTimeout(i?4200:2600);await pg.screenshot({path:path.join(ziel,'f'+i+'.png'),clip:{x:0,y:0,width:1440,height:810}});}
await br.close();})().catch(e=>{console.error(e);process.exit(1)});'''
    skript = os.path.join(ziel, '_aufnahme.js')
    open(skript, 'w').write(js)
    url = 'http://127.0.0.1:8978/haus/Culinarium%20Hannover/website/abend.html'
    try:
        subprocess.run(['node', skript, url, ziel, str(len(F))], check=True)
    finally:
        os.remove(skript)
    from PIL import Image
    for i in range(len(F) + 1):
        p = os.path.join(ziel, 'f%d.png' % i)
        im = Image.open(p).convert('RGB').resize((160, 90), Image.LANCZOS)
        im.save(os.path.join(ziel, 'f%d.jpg' % i), 'JPEG', quality=82)
        os.remove(p)
    print('Vorschaubilder', len(F) + 1)


if __name__ == '__main__':
    daumen() if 'daumen' in sys.argv else main()
