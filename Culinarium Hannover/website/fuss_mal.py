#!/usr/bin/env python3
"""Culinarium Hannover · 15 Fassungen von Footer 6 «Das ×», 26.10.2026.
Robert: «bau 15 Variationen aus 6». Kern von 6: drei Zeichen nach Gewicht (Culinarium gross, Wild-Side-Schild, D von Dirty Chicken),
verbunden durch das x der Plakate; aus dem + wird beim Hinscrollen ein ×.
Baut fuss-mal-wahl.html: die echte Startseite, unten die 15 Fassungen zum Durchklicken (Pfeile, Pfeiltasten, ?f=Nummer).
Jede Fassung ein bewegter Moment; nur transform und opacity, nativer Scroll. Bausteine aus fuss_wahl.py.
Aufruf: python3 website/bau.py && python3 website/fuss_mal.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, knopf, marke, VERSION
from fuss_wahl import b, zeichen, zeichen_bauen, nav, insta, recht, spalte, TEL, ADR, CUL, BAR, WARTE

HIER = bau.HIER
X = '<span class="xt-x" aria-hidden="true">+</span>'


def trio(cls='', wm='wmz'):
    """Die drei Zeichen nach Gewicht, verbunden durch das x."""
    return '<div class="xt %s"><div class="xt-cul">%s</div>%s<div class="xt-ws">%s</div>%s<div class="xt-dc">%s</div></div>' % (
        cls, marke(wm), X, zeichen('ws'), X, zeichen('dc'))


def spalten(cls='', satz='Ein Menü, fünf passende Drinks, eine lange Tafel.', k=WARTE):
    """Je Zeichen seine Spalte, genau darunter."""
    return ('<div class="xs %s"><div class="xs-1"><p class="xs-gross">%s</p><p>%s</p>%s</div>'
            '<div class="xs-2"><p class="ff-k">Das Haus</p><p>Walk on the Wild Side<br>%s<br>%s<br>%s</p></div>'
            '<div class="xs-3"><p class="ff-k">Das Pop-up</p><p>Dirty Chicken<br>Termine auf Instagram</p></div></div>') % (cls, satz, CUL, k, ADR, BAR, TEL)


def unten(cls=''):
    return '<div class="xu %s">%s%s%s</div>' % (cls, nav(), insta(), recht())


F = []   # (Name, Hinweis, Klasse, Inhalt)

# 1 Grundlinie: wie 6, die Zeichen stehen auf einer Linie in Kerze, die sich beim Hinscrollen zieht
F.append(('Grundlinie', 'hinscrollen', 'xm-linie', '%s<div class="x1-linie"></div>%s%s' % (trio(), spalten(), unten())))

# 2 Riesen-×: hinter allem steht ein × über die ganze Höhe, das sich aus dem + dreht
F.append(('Riesen-×', 'hinscrollen', 'xm-riese', '<span class="x2-riese" aria-hidden="true">+</span><div class="x2-innen">%s%s%s</div>' % (trio(), spalten(), unten())))

# 3 Kerzenfeld: die ganze Fläche in Kerze, die Zeichen in Nacht, das × in Weiss
F.append(('Kerzenfeld', 'hinscrollen', 'xm-kerze', '%s%s%s' % (trio(), spalten(k=knopf('Auf die Warteliste', 'abend.html#warteliste', 'hell')), unten())))

# 4 Gestapelt: Culinarium über die ganze Breite, darunter ein grosses ×, darunter das Haus und das Pop-up
F.append(('Gestapelt', 'hinscrollen', 'xm-stapel', '''<div class="x4-cul">%s</div><span class="xt-x x4-gross" aria-hidden="true">+</span>
<div class="x4-paar"><div class="x4-ws">%s<p><b>Walk on the Wild Side</b><br>%s<br>%s<br>%s</p></div>%s<div class="x4-dc">%s<p><b>Dirty Chicken</b><br>Das Pop-up aus der Familie<br>Termine auf Instagram</p></div></div>
<div class="x4-cul2"><p>%s</p>%s</div>%s''' % (marke('wmz'), zeichen('ws'), ADR, BAR, TEL, X, zeichen('dc'), CUL.replace('<br>', ' · '), WARTE, unten())))

# 5 Die Kreuzung: zwei Linien in Kerze kreuzen den ganzen Footer; oben Culinarium, links das Haus, rechts das Pop-up, unten der Rest
F.append(('Die Kreuzung', 'hinscrollen', 'xm-kreuz', '''<svg class="x5-linien" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0L100 100M100 0L0 100" stroke="currentColor" stroke-width="1.5" vector-effect="non-scaling-stroke" fill="none"/></svg>
<div class="x5-oben"><div class="x5-wm">%s</div><p>%s</p>%s</div>
<div class="x5-links">%s<p class="ff-k">Das Haus</p><p>Walk on the Wild Side<br>%s<br>%s<br>%s</p></div>
<div class="x5-rechts">%s<p class="ff-k">Das Pop-up</p><p>Dirty Chicken<br>Sandwiches &amp; More<br>Termine auf Instagram</p></div>
%s''' % (marke('wmz'), CUL.replace('<br>', ' · '), WARTE, zeichen('ws'), ADR, BAR, TEL, zeichen('dc'), unten('x5-unten'))))

# 6 Abspann: wie der Abspann eines Films, mittig, mit dem × zwischen den Häusern und den Angaben als Zeilen
ABSPANN = [('Abende', 'an einzelnen Wochenenden'), ('Freitag', 'ab 19:00'), ('Samstag', 'ab 17:00'), ('Plätze', 'vierzehn an einer Tafel'),
           ('Bar', 'Donnerstag 19 bis 1 Uhr'), ('', 'Freitag und Samstag 19 bis 2 Uhr'), ('Wo', 'Haasemannstraße 13, 30449 Hannover-Linden'),
           ('Telefon', TEL), ('Pop-up', 'Dirty Chicken, Termine auf Instagram')]
F.append(('Abspann', 'hinscrollen', 'xm-abspann', '''<div class="x6-wm">%s</div>%s<div class="x6-haus">%s<p>im Walk on the Wild Side</p></div>%s<div class="x6-haus">%s<p>mit Dirty Chicken</p></div>
<dl class="x6-zeilen">%s</dl><div class="x6-k">%s</div>%s''' % (
    marke('wmz'), X, zeichen('ws'), X, zeichen('dc'), ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in ABSPANN), WARTE, unten('mitte'))))

# 7 Ein Satz: die Zeichen stehen mitten im Satz, so hoch wie die Schrift
F.append(('Ein Satz', 'hinscrollen', 'xm-satz', '''<p class="x7-satz"><span class="x7-g">Ein Abend <span class="x7-wm">%s</span></span> %s <span class="x7-g">ein Haus <span class="x7-ws">%s</span></span> %s <span class="x7-g">ein Pop-up <span class="x7-dc">%s</span></span></p>%s%s''' % (
    marke('wm'), X, zeichen('ws'), X, zeichen('dc'), spalten('x7-sp'), unten())))

# 8 Drei Farben: drei Felder in der Breite ihres Gewichts, das × sitzt rund auf den Nähten
F.append(('Drei Farben', 'hinscrollen', 'xm-farben', '''<div class="x8-felder">
  <div class="x8-cul">%s<p class="xs-gross">Ein Menü, fünf passende Drinks, eine lange Tafel.</p><p>%s</p>%s</div>
  <span class="x8-naht x8-n1" aria-hidden="true"><span class="xt-x">+</span></span>
  <div class="x8-ws">%s<p>Walk on the Wild Side<br>%s<br>%s<br>%s</p></div>
  <span class="x8-naht x8-n2" aria-hidden="true"><span class="xt-x">+</span></span>
  <div class="x8-dc">%s<p>Dirty Chicken<br>Das Pop-up<br>Termine auf Instagram</p></div>
</div>%s''' % (marke('wmz'), CUL, WARTE, zeichen('ws'), ADR, BAR, TEL, zeichen('dc'), unten())))

# 9 Hell: dieselbe Ordnung auf Warmweiss, nach der dunklen Seite ein Schnitt ins Helle
F.append(('Hell', 'hinscrollen', 'xm-hell', '%s%s%s' % (trio(), spalten(k=knopf('Auf die Warteliste', 'abend.html#warteliste', 'hell')), unten())))

def spalten_edel():
    """Fassung 10 (Robert 26.10.: «edler, besser lesbar», dann «noch random angeordnet»): alle drei Spalten gleich gebaut,
    Etikett, Name mit Satz, zwei Zeilen mit Haarlinie, Handlung; ein gemeinsames Zeilenraster, damit jede Linie quer durchläuft."""
    def spalte_e(n, etikett, name, satz, zeilen, tat, ncls='xe-name'):
        dl = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % z for z in zeilen)
        return ('<div class="xs-%d"><p class="ff-k">%s</p><div class="xe-kopf"><p class="%s">%s</p><p class="xe-text">%s</p></div><dl class="xe-zeiten">%s</dl><div class="xe-tat">%s</div></div>'
                % (n, etikett, ncls, name, satz, dl, tat))
    return '<div class="xs xe">%s%s%s</div>' % (
        spalte_e(1, 'Culinarium', 'Ein Menü, fünf passende Drinks, eine lange Tafel.', 'An einzelnen Wochenenden, vierzehn Plätze pro Abend.',
                 [('Freitag', 'ab 19:00 Uhr'), ('Samstag', 'ab 17:00 Uhr')], WARTE, 'xe-name xe-gross'),
        spalte_e(2, 'Das Haus', 'Walk on the Wild Side', 'Haasemannstraße 13<br>30449 Hannover-Linden',
                 [('Do', '19 bis 1 Uhr'), ('Fr und Sa', '19 bis 2 Uhr')], '<a class="xe-link" href="tel:+491633909578">+49 163 3909578</a>'),
        spalte_e(3, 'Das Pop-up', 'Dirty Chicken', 'Aus der Familie<br>der Bar',
                 [('Küche', 'Sandwiches &amp; More'), ('Termine', 'auf Instagram')],
                 '<a class="xe-link" href="https://www.instagram.com/dirtychicken.hannover/" rel="noopener" target="_blank">@dirtychicken.hannover</a>'))


# 10 Mit Fotos: unter jedem Zeichen sein Bild, so breit wie das Zeichen
F.append(('Mit Fotos', 'hinscrollen', 'xm-fotos', '%s<div class="x10-bilder">%s<span></span>%s<span></span>%s</div>%s%s' % (
    trio(), b('tafelleer', '', '(max-width:860px) 60vw, 56vw', '50% 58%'), b('theke', '', '(max-width:860px) 20vw, 14vw', '50% 40%'),
    b('dc_tisch', '', '(max-width:860px) 20vw, 12vw', '50% 50%'), spalten_edel(), unten())))

# 11 Langsame Drehung: die Zeichen mittig mit Luft, das × dreht sich ruhig weiter wie ein Ventilator unter der Decke
F.append(('Langsame Drehung', 'ansehen', 'xm-dreh', '%s%s%s' % (trio('', 'wm'), spalten(), unten())))

# 12 Schilder: an einer Stange hängen drei Schilder, dazwischen das ×; beim Hinscrollen schwingen sie aus
F.append(('Schilder', 'hinscrollen', 'xm-schild', '''<div class="x12-links"><p class="xs-gross">Drei Schilder, ein Haus in Linden.</p>
  <div class="x12-sp">%s%s%s</div>%s</div>
<div class="x12-stange"><span class="x12-rohr"></span>
  <div class="x12-s x12-cul" style="--i:0"><span class="x12-kette"></span><div class="x12-tafel">%s</div></div>%s
  <div class="x12-s x12-ws" style="--i:1"><span class="x12-kette"></span>%s</div>%s
  <div class="x12-s x12-dc" style="--i:2"><span class="x12-kette"></span><div class="x12-rund">%s</div></div>
</div>%s''' % (
    spalte('Culinarium', '<p>%s</p>' % CUL), spalte('Das Haus', '<p>Walk on the Wild Side<br>%s<br>%s<br>%s</p>' % (ADR, BAR, TEL)),
    spalte('Das Pop-up', '<p>Dirty Chicken<br>Termine auf Instagram</p>'), WARTE, marke('wmz'), X, zeichen('ws'), X, zeichen('dc'), unten())))

# 13 Fünf mal drei mal vierzehn: das × als Rechenzeichen des Abends, darunter die drei Zeichen
F.append(('5 × 3 × 14', 'hinscrollen', 'xm-rechnung', '''<div class="x13-rechnung"><div><b>5</b><span>Drinks von Momo</span></div>%s<div><b>3</b><span>Gänge aus der Küche</span></div>%s<div><b>14</b><span>Plätze an der Tafel</span></div></div>
%s%s%s''' % (X, X, trio('x13-trio'), spalten(), unten())))

# 14 Kompakt: dieselbe Idee als schmales Band, für Unterseiten
F.append(('Kompakt', 'hinscrollen', 'xm-kompakt', '''<div class="x14-reihe">%s<div class="x14-info"><p><b>Culinarium</b> an einzelnen Wochenenden · Fr ab 19:00 · Sa ab 17:00</p>
<p><b>Walk on the Wild Side</b> Haasemannstraße 13 · Do 19–1 · Fr + Sa 19–2 · %s</p><p><b>Dirty Chicken</b> Pop-up · Termine auf Instagram</p></div></div>%s''' % (trio('', 'wm'), TEL, unten())))

# 15 Schräges Band: die drei Zeichen auf einem Band in Kerze, quer über die Breite, das beim Hinscrollen hereinzieht
F.append(('Schräges Band', 'hinscrollen', 'xm-band', '<div class="x15-band"><div class="x15-zug">%s</div></div>%s%s' % (trio('', 'wm'), spalten(), unten())))


def footer():
    return ''.join('<footer class="ff xm %s" data-nr="%d"%s>%s</footer>' % (cls, i, '' if i == 1 else ' hidden', inner)
                   for i, (_n, _h, cls, inner) in enumerate(F, 1))


def main():
    zeichen_bauen()
    seite = open(os.path.join(HIER, 'index.html')).read()
    seite, n = re.subn(r'<footer class="fuss">.*?</footer>', lambda _m: footer(), seite, count=1, flags=re.S)
    assert n == 1, 'Footer in index.html nicht gefunden (erst bau.py laufen lassen)'
    liste = json.dumps([[i, '%s <em>%s</em>' % (E(nm), E(h))] for i, (nm, h, _c, _x) in enumerate(F, 1)], ensure_ascii=False)
    leiste = ('<div class="fassungen" id="fuss-fassungen" data-speicher="culinarium-fuss-mal" data-liste="%s"><button class="fz-zurueck" type="button" aria-label="Vorige Fassung">‹</button>'
              '<span class="fz-name"></span><button class="fz-vor" type="button" aria-label="Nächste Fassung">›</button></div>') % E(liste)
    stand = lambda d: '%s-%d' % (VERSION, os.path.getmtime(os.path.join(HIER, 'assets', d)))
    seite = seite.replace('<title>', '<title>Footer × wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/fuss-wahl.css?v=%s">\n<link rel="stylesheet" href="assets/fuss-mal.css?v=%s">\n</head>'
                          % (stand('fuss-wahl.css'), stand('fuss-mal.css')), 1)
    seite = seite.replace('</body>', '%s\n<script src="assets/fuss-wahl.js?v=%s" defer></script>\n</body>' % (leiste, stand('fuss-wahl.js')), 1)
    open(os.path.join(HIER, 'fuss-mal-wahl.html'), 'w').write(seite)
    print('Seite fuss-mal-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen')


if __name__ == '__main__':
    main()
