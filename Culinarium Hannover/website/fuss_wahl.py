#!/usr/bin/env python3
"""Culinarium Hannover · 15 Footer zur Wahl, 26.10.2026.
Robert: «15 Variationsmöglichkeiten für einen geilen Footer, der Main-Energy-Vibes dem Culinarium gibt und Wild Side und Dirty Chicken trotzdem aufgreift».
Baut fuss-wahl.html: die echte Startseite, unten die 15 Footer zum Durchklicken (Pfeile unten, Pfeiltasten, ?f=Nummer).
Rangfolge in jeder Fassung: Culinarium gross, Walk on the Wild Side als das Haus, Dirty Chicken als Pop-up aus derselben Familie.
Jede Fassung hat ein eigenes Gerüst und genau einen bewegten Moment; nur transform und opacity, nativer Scroll.
Fakten nur aus dem heutigen Footer in bau.py und CHARAKTER.md.
Aufruf: python3 website/bau.py && python3 website/fuss_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, knopf, marke, BILD, VERSION, NAV

HIER = bau.HIER
PROJ = bau.PROJ
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))


# ------------------------------------------------------------------ Zeichen der beiden anderen Häuser
def symbol(datei, sid, viewbox):
    s = open(os.path.join(PROJ, datei)).read()
    g = re.search(r'<g transform="([^"]+)"', s).group(1)
    pfade = ''.join('<path d="%s"/>' % ' '.join(d.split()) for d in re.findall(r'<path d="([^"]+)"', s))
    return '<symbol id="%s" viewBox="%s"><g transform="%s">%s</g></symbol>' % (sid, viewbox, g, pfade)


def zeichen_bauen():
    """Wild-Side-Schild (nachgezogen, Station 03) und das D mit Hühnerfuss (aus dem Profilbild nachgezogen) als ein Sprite."""
    dc = '_quelle/dirty-chicken/logo/dirtychicken-zeichen-nachgezogen.svg'
    svg = ('<svg xmlns="http://www.w3.org/2000/svg">%s%s</svg>'
           % (symbol('_quelle/walk-on-the-wild-side/logo/wildside-logo-nachgezogen.svg', 'ws', '0 0 1296 1600'),
              symbol(dc, 'dc', '214 197 652 712')))   # genau die Kante des D (gemessen am Profilbild)
    open(os.path.join(HIER, 'assets', 'zeichen', 'haus.svg'), 'w').write(svg)


def zeichen(sid, cls=''):
    vb = {'ws': '0 0 1296 1600', 'dc': '0 0 652 712'}[sid]   # Ausschnitt steckt im Symbol, aussen nie verschieben (Safari verschiebt sonst doppelt)
    name = {'ws': 'Walk on the Wild Side', 'dc': 'Dirty Chicken'}[sid]
    return '<svg class="zn zn-%s %s" viewBox="%s" role="img" aria-label="%s"><use href="assets/zeichen/haus.svg?v=%s#%s"/></svg>' % (sid, cls, vb, name, VERSION, sid)


# ------------------------------------------------------------------ Bausteine
def b(k, cls='', sizes='50vw', pos=None, i=None):
    """Foto, geladen erst, wenn seine Fassung gezeigt wird; Abbild als Grund."""
    m = META[k]
    _q, p, alt = BILD[k]
    srcset = ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in m['stufen'])
    return ('<figure class="fb %s" style="--lq:url(%s)%s"><img data-srcset="%s" sizes="%s" alt="%s" decoding="async" style="object-position:%s"></figure>'
            % (cls, m['lq'], '' if i is None else ';--i:%d' % i, srcset, sizes, E(alt), pos or p))


def nav(cls='ff-nav'):
    return '<nav class="%s" aria-label="Seiten">%s</nav>' % (cls, ''.join('<a href="%s">%s</a>' % (h, E(t)) for h, t in NAV))


IG = [('culinarium_hannover', '@culinarium_hannover'), ('walkonthewildside_hannover', '@walkonthewildside_hannover'), ('dirtychicken.hannover', '@dirtychicken.hannover')]


def insta(cls='ff-ig', nur=None):
    return '<p class="%s">%s</p>' % (cls, ''.join('<a href="https://www.instagram.com/%s/" rel="noopener" target="_blank">%s</a>' % (h, t)
                                                 for h, t in IG if nur is None or h in nur))


TEL = '<a href="tel:+491633909578">+49 163 3909578</a>'
ADR = 'Haasemannstraße 13<br>30449 Hannover-Linden'
CUL = 'an einzelnen Wochenenden<br>Freitag ab 19:00<br>Samstag ab 17:00'
BAR = 'Donnerstag 19 bis 1 Uhr<br>Freitag und Samstag 19 bis 2 Uhr'
DCT = 'Pop-up mit Sandwiches &amp; More<br>aus der Familie der Bar<br>Termine auf Instagram'
WARTE = knopf('Auf die Warteliste', 'abend.html#warteliste')


def recht():
    return ('<div class="ff-recht"><span>Culinarium im Walk on the Wild Side</span>'
            '<a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div>')


def spalte(k, inhalt, cls=''):
    return '<div class="ff-sp %s"><p class="ff-k">%s</p>%s</div>' % (cls, k, inhalt)


# ------------------------------------------------------------------ die 15 Fassungen
F = []   # (Name, Hinweis, Klasse, Inhalt)

# 1 Letzter Gang: die Wortmarke über die ganze Breite steigt beim Hinunterscrollen aus der Unterkante; Haus und Pop-up als kleine Zeichen darüber
F.append(('Letzter Gang', 'bis ganz unten scrollen', 'fx-gang', '''%s<div class="fg-hof"></div>
<div class="fg-oben">
  <div class="fg-cul"><p class="fg-satz">Ein Menü, fünf passende Drinks, eine lange Tafel für vierzehn Gäste.</p><p class="ff-zeit">%s</p>%s</div>
  %s
  %s
  %s
</div>
<div class="fg-mitte">%s%s</div>
<div class="fg-wort">%s</div>''' % (
    b('tafelleer', 'fg-foto', '100vw', '50% 58%'), CUL.replace('<br>', ' · ', 1), WARTE,
    spalte('Im Haus', '%s<p><b>Walk on the Wild Side</b><br>%s</p>' % (zeichen('ws'), BAR), 'fg-ws'),
    spalte('Aus der Familie', '%s<p><b>Dirty Chicken</b><br>%s</p>' % (zeichen('dc'), DCT), 'fg-dc'),
    spalte('Wo', '<p>%s<br>%s</p>%s' % (ADR, TEL, insta()), 'fg-wo'),
    nav(), recht(), marke('wm'))))

# 2 Das Plakat: der Footer ist das Plakat des nächsten Abends, mit der Akzentlinie unter dem Datum
F.append(('Das Plakat', 'ansehen', 'fx-plakat', '''<div class="fp-blatt">
  <div class="fp-kopf">%s<span>Walk on the Wild Side präsentiert</span><span class="fp-ort">Haasemannstraße 13 · Hannover-Linden</span></div>
  <div class="fp-marke">%s</div>
  <div class="fp-mitte">
    <div class="fp-datum"><p class="ff-k">Nächster Abend</p><p class="fp-gross">Termin folgt</p><span class="fp-linie"></span><p class="fp-klein">Zuletzt: 25. + 26.09.2026, ausgebucht</p></div>
    <dl class="fp-daten"><div><dt>Menü</dt><dd>3 Gänge</dd></div><div><dt>Drinks</dt><dd>5</dd></div><div><dt>Plätze</dt><dd>14</dd></div><div><dt>Beginn</dt><dd>Fr 19:00 · Sa 17:00</dd></div></dl>
    <div class="fp-knopf">%s</div>
  </div>
  <div class="fp-band"><div>%s<p><b>Die Bar</b> Do 19 bis 1 Uhr · Fr + Sa 19 bis 2 Uhr · %s</p></div><div>%s<p><b>Im selben Haus zu Gast:</b> Dirty Chicken, das Pop-up. Termine auf Instagram.</p></div></div>
</div>
<div class="fp-unten">%s%s%s</div>''' % (
    zeichen('ws'), marke('wmz'), knopf('Auf die Warteliste', 'abend.html#warteliste', 'hell'), zeichen('ws'), TEL, zeichen('dc'), nav(), insta(), recht())))

# 3 Laufband: Culinarium gross, dazwischen das Schild der Bar und das D, ohne Ende
def band():
    eins = '<span class="fl-glied">%s<i>×</i>%s<i>×</i>%s<i>×</i>%s<i>×</i></span>' % (marke('wm'), zeichen('ws'), marke('wm'), zeichen('dc'))
    return eins * 2 + eins.replace('<svg ', '<svg aria-hidden="true" ') * 2
F.append(('Laufband', 'ansehen', 'fx-lauf', '''<div class="fl-band" aria-label="Culinarium im Walk on the Wild Side, mit Dirty Chicken"><div class="fl-lauf">%s</div></div>
<div class="fl-raster">
  <div class="fl-cul"><p class="fl-satz">Food-Pairing-Abende im Walk on the Wild Side in Linden.</p>%s</div>
  %s%s%s%s
</div>%s''' % (
    band(), WARTE, spalte('Culinarium', '<p>%s</p>' % CUL), spalte('Die Bar', '<p>%s<br>%s</p>' % (BAR, TEL)),
    spalte('Dirty Chicken', '<p>%s</p>' % DCT), spalte('Seiten', nav()), '<div class="fl-fuss">%s%s</div>' % (insta(), recht()))))

# 4 Licht an: unter dem Schild der Bar geht die Wortmarke an wie Leuchtschrift
F.append(('Licht an', 'hinscrollen', 'fx-licht', '''%s<div class="fn-hof"></div>
<div class="fn-innen">
  <p class="fn-ueber">Unter dem Schild in Linden</p>
  <div class="fn-wort">%s</div>
  <div class="fn-zeile">%s</div>
  <div class="fn-spalten">%s%s%s%s</div>
  <div class="fn-fuss">%s%s</div>
</div>''' % (
    b('schildnacht', 'fn-foto', '100vw', '50% 30%'), marke('wm'), marke('zeile'),
    spalte('Culinarium', '<p>%s</p>%s' % (CUL, WARTE)),
    spalte('Walk on the Wild Side', '<p>%s<br>%s<br>%s</p>' % (ADR, BAR, TEL)),
    spalte('Pop-up', '<div class="fn-dc">%s<p>Dirty Chicken<br>Termine auf Instagram</p></div>' % zeichen('dc')),
    spalte('Seiten', nav()), insta(), recht())))

# 5 Der Bon: der Abend als Rechnung; der Zettel kommt beim Hinscrollen aus dem Schlitz
F.append(('Der Bon', 'hinscrollen', 'fx-bon', '''<div class="fo-links">
  <div class="fo-wort">%s</div>
  <p class="fo-satz">Danke für den Abend. Der nächste ist schon in Arbeit.</p>%s
  <div class="fo-unten">%s%s</div>
</div>
<div class="fo-kasse"><div class="fo-schlitz"></div><div class="fo-fenster"><div class="fo-zettel">
  <div class="fo-ws">%s</div>
  <p class="fo-m">WALK ON THE WILD SIDE<br>Haasemannstraße 13<br>30449 Hannover-Linden<br>Tel. +49 163 3909578</p>
  <p class="fo-t">CULINARIUM</p>
  <p class="fo-z"><span>Menü</span><span>3 Gänge</span></p><p class="fo-z"><span>Drinks von Momo</span><span>5</span></p><p class="fo-z"><span>Plätze an der Tafel</span><span>14</span></p>
  <p class="fo-m">Fr ab 19:00 · Sa ab 17:00<br>an einzelnen Wochenenden</p>
  <p class="fo-t">BAR</p>
  <p class="fo-z"><span>Donnerstag</span><span>19–1 Uhr</span></p><p class="fo-z"><span>Freitag, Samstag</span><span>19–2 Uhr</span></p>
  <p class="fo-t">NACHSCHLAG</p>
  <p class="fo-z fo-dc"><span>%s Dirty Chicken</span><span>Pop-up</span></p><p class="fo-m">Termine auf Instagram</p>
  <p class="fo-dank">Dann haste allet<br>richtig jemacht!</p>
</div></div></div>''' % (
    marke('wmz'), WARTE, nav(), insta() + recht(), zeichen('ws'), zeichen('dc'))))

# 6 Das ×: drei Zeichen, so gross wie ihr Gewicht, verbunden durch das x der Plakate; jede Spalte steht unter ihrem Zeichen
F.append(('Das ×', 'hinscrollen', 'fx-mal', '''<div class="fm-reihe">
  <div class="fm-cul">%s</div><span class="fm-x" aria-hidden="true">+</span><div class="fm-ws">%s</div><span class="fm-x" aria-hidden="true">+</span><div class="fm-dc">%s</div>
</div>
<div class="fm-spalten">
  <div class="fm-s1"><p class="fm-gross">Ein Menü, fünf passende Drinks, eine lange Tafel.</p><p>%s</p>%s</div>
  <div class="fm-s2"><p class="ff-k">Das Haus</p><p>Walk on the Wild Side<br>%s<br>%s<br>%s</p></div>
  <div class="fm-s3"><p class="ff-k">Das Pop-up</p><p>Dirty Chicken<br>Termine auf Instagram</p></div>
</div>
<div class="fm-fuss">%s%s%s</div>''' % (
    marke('wmz'), zeichen('ws'), zeichen('dc'), CUL, WARTE, ADR, BAR, TEL, nav(), insta(), recht())))

# 7 Wann wieder?: die Frage vom Ende der Geschichte, drei Antworten nach Gewicht; Zeigen tauscht das Bild im selben Rahmen
WANN = [('Zum nächsten Culinarium', 'Fr ab 19:00 · Sa ab 17:00 · 14 Plätze', 'abend.html#warteliste', 'kerze2', 'w1'),
        ('An einem Barabend im Wild Side', 'Do 19 bis 1 Uhr · Fr + Sa 19 bis 2 Uhr', 'bar.html', 'theke', 'w2'),
        ('Zum nächsten Pop-up von Dirty Chicken', 'Termine auf Instagram', 'dirty-chicken.html', 'dc_tisch', 'w3')]
F.append(('Wann wieder?', 'Zeilen zeigen', 'fx-wann', '''<div class="fw-links">
  <p class="fw-frage">Und wann sehen wir uns wieder?</p>
  <ul class="fw-liste">%s</ul>
</div>
<div class="fw-bild">%s</div>
<div class="fw-fuss">%s%s%s%s</div>''' % (
    ''.join('<li class="%s%s" data-n="%d"><a href="%s"><span class="fw-t">%s</span><span class="fw-m">%s</span></a></li>' % (c, ' an' if i == 0 else '', i, h, t, m)
            for i, (t, m, h, _k, c) in enumerate(WANN)),
    ''.join(b(k, 'an' if i == 0 else '', '(max-width:860px) 100vw, 42vw') for i, (_t, _m, _h, k, _c) in enumerate(WANN)),
    '<div class="fw-marke">%s</div>' % marke('wm'), spalte('Wo', '<p>Walk on the Wild Side<br>%s<br>%s</p>' % (ADR, TEL)), nav(), '<div class="fw-recht">%s%s</div>' % (insta(), recht()))))

# 8 Plakatwand: oben die Culinarium-Plakate, unten die Abende der Bar und das Pop-up, beide Reihen ziehen langsam gegeneinander
PL1 = ['p_DbYnkdkjrNy', 'p_DVjkofijp6R', 'p_DPwlqcfiKcA', 'p_DJw8OqGMY1G', 'p_DFqbLG2s_dc', 'p_DCCf-ikoaGs', 'p_C8cgYVSouVT', 'p_C56bJeds8PF', 'p_C17kqAXLfs_', 'p_C0w6iuCMcnF', 'p_CzMcqNcMCqG', 'p_CyT32RTMB4d', 'p_CxNkFWTIvL2']
PL2 = ['ws52', 'dc_plakat', 'ws51', 'ws39', 'ws50', 'ws21', 'ws49', 'ws48', 'pop23', 'ws47', 'ws42', 'ws32', 'ws40', 'pl23']
def reihe(ks):
    s = ''.join(b(k, '', '160px') for k in ks)
    return s + s.replace('<img ', '<img aria-hidden="true" ')
F.append(('Plakatwand', 'ansehen', 'fx-wand', '''<div class="fa-reihe fa-r1"><div class="fa-lauf">%s</div></div>
<div class="fa-band">
  <div class="fa-marke">%s<p>Jeder Abend hat sein Plakat. Der nächste auch.</p>%s</div>
  <div class="fa-spalten">%s%s%s</div>
</div>
<div class="fa-reihe fa-r2"><div class="fa-lauf">%s</div></div>
<div class="fa-fuss">%s%s%s</div>''' % (
    reihe(PL1), marke('wmz'), WARTE,
    spalte('Culinarium', '<p>%s</p>' % CUL), spalte('Im Walk on the Wild Side', '<p>%s<br>%s<br>%s</p>' % (ADR, BAR, TEL)),
    spalte('Und Dirty Chicken', '<p>Das Pop-up aus der Familie<br>Termine auf Instagram</p>'),
    reihe(PL2), nav(), insta(), recht())))

# 9 Das Loch in der Wand: der Blick durch die Wand auf die Tafel; das Bild im Loch zieht langsamer als die Seite
F.append(('Das Loch in der Wand', 'scrollen', 'fx-loch', '''<div class="fh-wand">
  <div class="fh-links">
    <div class="fh-wort">%s</div>
    <p class="fh-satz">Hinter dieser Wand steht an einzelnen Wochenenden die lange Tafel.</p>
    <div class="fh-spalten">%s%s</div>%s
  </div>
  <div class="fh-loch"><div class="fh-tiefe">%s</div></div>
  <div class="fh-schild" title="Walk on the Wild Side">%s</div>
  <div class="fh-aufkleber">%s<span>Pop-up</span></div>
</div>
<div class="fh-fuss">%s%s<p class="fh-dc">Dirty Chicken: Termine auf Instagram</p>%s</div>''' % (
    marke('wm'), spalte('Culinarium', '<p>%s</p>' % CUL), spalte('Walk on the Wild Side', '<p>%s<br>%s<br>%s</p>' % (ADR, BAR, TEL)), WARTE,
    b('loch', 'fh-foto', '(max-width:860px) 90vw, 40vw', '50% 50%'), zeichen('ws'), zeichen('dc'), nav(), insta(), recht())))

# 10 Die Karte: der Footer in der Schreibweise der Speisekarte, Versalien mit Schrägstrich; ein Strich in Kerze folgt der Zeile
KARTE = [('Wo', 'HAASEMANNSTRASSE 13 / LINDEN', 'Walk on the Wild Side · 30449 Hannover', 'weg.html', ''),
         ('Culinarium', 'FREITAG AB 19 / SAMSTAG AB 17', 'an einzelnen Wochenenden · 14 Plätze · Warteliste', 'abend.html#warteliste', ''),
         ('Die Bar', 'DONNERSTAG BIS SAMSTAG / AB 19', 'Do bis 1 Uhr · Fr + Sa bis 2 Uhr · +49 163 3909578', 'bar.html', 'ws'),
         ('Ab und zu', 'DIRTY CHICKEN / POP-UP', 'Sandwiches & More · Termine auf Instagram', 'dirty-chicken.html', 'dc')]
F.append(('Die Karte', 'Zeilen zeigen', 'fx-karte', '''<div class="fk-karte">
  <div class="fk-kopf">%s</div>
  <ul class="fk-zeilen"><span class="fk-strich" aria-hidden="true"></span>%s</ul>
  <div class="fk-fuss">%s%s</div>
</div>%s''' % (
    marke('wmz'),
    ''.join('<li><a href="%s"><span class="fk-k">%s%s</span><span class="fk-z">%s</span><span class="fk-u">%s</span></a></li>' % (
        h, zeichen(z) if z else '', k, E(t).replace(' / ', '&#160;<i>/</i> '), E(u)) for k, t, u, h, z in KARTE),
    nav(), insta(), recht())))

# 11 Offen?: der Footer weiss, welcher Tag ist; die drei Fenster der Barabende gehen an
TAGE = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
F.append(('Offen?', 'ansehen', 'fx-offen', '''<div class="fq-oben">
  <div class="fq-links"><p class="ff-k">Walk on the Wild Side · Haasemannstraße 13</p><p class="fq-satz" data-status>Die Bar hat donnerstags bis samstags ab 19 Uhr offen.</p></div>
  <div class="fq-woche">%s</div>
</div>
<div class="fq-mitte">
  <div class="fq-cul"><div class="fq-wort">%s</div><p>Culinarium, die Abende an der langen Tafel: %s. Nächster Abend: Termin folgt.</p>%s</div>
  <div class="fq-dc">%s<p><b>Dirty Chicken</b><br>Nächstes Pop-up: Termine auf Instagram</p></div>
</div>
<div class="fq-fuss">%s%s%s%s</div>''' % (
    ''.join('<div class="fq-tag%s" data-tag="%d" style="--i:%d">%s<span>%s</span></div>' % (
        ' auf' if i in (3, 4, 5) else '', i, i, b(('barlicht', 'fassade', 'barnacht')[i - 3], '', '120px') if i in (3, 4, 5) else '', t) for i, t in enumerate(TAGE)),
    marke('wm'), CUL.replace('<br>', ', ').replace('an einzelnen Wochenenden, ', 'an einzelnen Wochenenden, '), WARTE, zeichen('dc'),
    spalte('Kontakt', '<p>%s<br>%s</p>' % (ADR, TEL)), nav(), insta(), recht())))

# 12 Bierdeckel: drei Deckel auf dem Tresen, gross, eckig, klein; Zeigen dreht sie
F.append(('Bierdeckel', 'Deckel zeigen', 'fx-deckel', '''<div class="fd-tresen">
  <div class="fd-d fd-cul"><div class="fd-wort">%s</div><p class="fd-zeile">%s</p><p class="fd-t">Freitag ab 19:00<br>Samstag ab 17:00</p><p class="fd-k">an einzelnen Wochenenden</p></div>
  <div class="fd-d fd-ws">%s<p class="fd-t">Do 19–1 · Fr + Sa 19–2</p></div>
  <div class="fd-d fd-dc">%s<p class="fd-t">Pop-up<br><span>Termine auf Instagram</span></p></div>
  <div class="fd-text"><p class="fd-satz">Leg einen Deckel auf dein Glas. Wir halten dir den Platz an der Tafel frei.</p>%s</div>
</div>
<div class="fd-fuss">%s%s%s%s</div>''' % (
    marke('wm'), marke('zeile'), zeichen('ws'), zeichen('dc'), WARTE,
    spalte('Wo', '<p>Walk on the Wild Side<br>%s<br>%s</p>' % (ADR, TEL)), nav(), insta(), recht())))

# 13 Der Vorhang: die Seite hebt sich vom Footer ab wie ein Vorhang; darunter liegt eine Fläche in Kerze
F.append(('Der Vorhang', 'bis ganz unten scrollen', 'fx-vorhang', '''<div class="fv-feld">
  <div class="fv-oben"><p class="fv-satz">Der nächste Abend kommt bestimmt.</p>%s</div>
  <div class="fv-wort">%s</div>
  <div class="fv-spalten">%s%s%s</div>
</div>
<div class="fv-band">
  <div class="fv-haus">%s<p>Im Walk on the Wild Side<br><span>%s</span></p></div>
  <div class="fv-haus">%s<p>Mit Dirty Chicken<br><span>Termine auf Instagram</span></p></div>
  %s
</div>''' % (
    knopf('Auf die Warteliste', 'abend.html#warteliste', 'hell'), marke('wm'),
    spalte('Culinarium', '<p>%s</p>' % CUL), spalte('Die Bar', '<p>%s<br>%s</p>' % (BAR, TEL)), spalte('Seiten', nav()),
    zeichen('ws'), 'Haasemannstraße 13 · Linden', zeichen('dc'), '<div class="fv-recht">%s%s</div>' % (insta(), recht()))))

# 14 Haus im Schnitt: oben an der Tafel, unten an der Theke, draussen die Strasse, nebenan das Pop-up; die Stockwerke setzen sich
F.append(('Haus im Schnitt', 'hinscrollen', 'fx-schnitt', '''<div class="fs-haus">
  <svg class="fs-dach" viewBox="0 0 1000 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 80 L500 2 L1000 80" fill="none" stroke="currentColor" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg>
  <div class="fs-stock fs-oben" style="--i:0">%s<div class="fs-text"><p class="ff-k">Oben, an der Tafel</p><div class="fs-wort">%s</div><p>%s</p>%s</div></div>
  <div class="fs-stock fs-mitte" style="--i:1">%s<div class="fs-text"><p class="ff-k">Unten, an der Theke</p><p class="fs-name">Walk on the Wild Side</p><p>%s · Mixology ohne Karte</p></div>%s</div>
  <div class="fs-stock fs-strasse" style="--i:2"><p class="ff-k">Draussen</p><p class="fs-adr">Haasemannstraße 13 · 30449 Hannover-Linden</p><p>%s · <a href="weg.html">Der Weg</a></p></div>
  <div class="fs-anbau" style="--i:3">%s<p class="ff-k">Nebenan</p><p>Dirty Chicken<br>Das Pop-up aus der Familie</p></div>
</div>
<div class="fs-fuss">%s%s%s</div>''' % (
    b('tafelleer', 'fs-foto', '(max-width:860px) 100vw, 44vw', '50% 55%'), marke('wm'), CUL.replace('<br>', ' · '), WARTE,
    zeichen('ws'), BAR.replace('<br>', ' · '), b('theke', 'fs-foto2', '(max-width:860px) 100vw, 30vw', '50% 40%'),
    TEL, zeichen('dc'), nav(), insta(), recht())))

# 15 Die Tafel von oben: vierzehn Plätze um einen Tisch, auf dem Tisch Culinarium; die Plätze setzen sich
STUEHLE = ['t%02d' % n for n in range(1, 15)]
F.append(('Die Tafel von oben', 'hinscrollen', 'fx-tafel', '''<p class="ft-ueber">Vierzehn Plätze. Einer davon ist deiner.</p>
<div class="ft-raum">
  <div class="ft-reihe">%s</div>
  <div class="ft-tisch"><div class="ft-wort">%s</div><p>%s</p>%s</div>
  <div class="ft-reihe">%s</div>
</div>
<div class="ft-spalten">%s%s%s%s</div>
<div class="ft-fuss">%s%s</div>''' % (
    ''.join(b(k, 'ft-platz', '90px', '50% 40%', i) for i, k in enumerate(STUEHLE[:7])), marke('wmz'),
    'Die Tafel steht im Walk on the Wild Side · ' + CUL.replace('<br>', ' · '), WARTE,
    ''.join(b(k, 'ft-platz', '90px', '50% 40%', i + 7) for i, k in enumerate(STUEHLE[7:])),
    spalte('Das Haus', '<div class="ft-zn">%s<p>Walk on the Wild Side<br>%s<br>%s</p></div>' % (zeichen('ws'), BAR, TEL)),
    spalte('Das Pop-up', '<div class="ft-zn">%s<p>Dirty Chicken<br>Termine auf Instagram</p></div>' % zeichen('dc')),
    spalte('Wo', '<p>%s</p>' % ADR), spalte('Seiten', nav()), insta(), recht())))


def footer():
    return ''.join('<footer class="ff %s" data-nr="%d"%s>%s</footer>' % (cls, i, '' if i == 1 else ' hidden', inner)
                   for i, (_n, _h, cls, inner) in enumerate(F, 1))


def main():
    zeichen_bauen()
    seite = open(os.path.join(HIER, 'index.html')).read()
    seite, n = re.subn(r'<footer class="fuss">.*?</footer>', lambda _m: footer(), seite, count=1, flags=re.S)
    assert n == 1, 'Footer in index.html nicht gefunden (erst bau.py laufen lassen)'
    liste = json.dumps([[i, '%s <em>%s</em>' % (E(nm), E(h))] for i, (nm, h, _c, _x) in enumerate(F, 1)], ensure_ascii=False)
    leiste = ('<div class="fassungen" id="fuss-fassungen" data-liste="%s"><button class="fz-zurueck" type="button" aria-label="Voriger Footer">‹</button>'
              '<span class="fz-name"></span><button class="fz-vor" type="button" aria-label="Nächster Footer">›</button></div>') % E(liste)
    seite = seite.replace('<title>', '<title>Footer wählen · ', 1)
    stand = lambda d: '%s-%d' % (VERSION, os.path.getmtime(os.path.join(HIER, 'assets', d)))
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/fuss-wahl.css?v=%s">\n</head>' % stand('fuss-wahl.css'), 1)
    seite = seite.replace('</body>', '%s\n<script src="assets/fuss-wahl.js?v=%s" defer></script>\n</body>' % (leiste, stand('fuss-wahl.js')), 1)
    open(os.path.join(HIER, 'fuss-wahl.html'), 'w').write(seite)
    print('Seite fuss-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen')


if __name__ == '__main__':
    main()
