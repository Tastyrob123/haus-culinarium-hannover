#!/usr/bin/env python3
"""Le Livre · Culinarium Hannover: das Markenbuch zum Arbeiten (buch.html und buch/), gebaut von bau.py.
Grundlage ist das Markenbuch der Station 05 (Farbwelt A «Plakat», Robert 26.10.2026: «a»), _kette/05-markenbauer/marke/markenbuch.html, genau dieses
(Fehlerbuch 10a, 20.10.2026), im Stand der Website (Fehlerbuch 10a, Demo-Check Schäfli: Schriftwerte gegen die Website):
  · Wortmarke und Zeile: Rudis Original (28.10.2026, _quelle/logo/original/), wie die Website es trägt, statt des Platzhalters vom Plakat;
  · Titelschrift: Fraunces mit weichen Enden wie auf der Website (wght 340, SOFT 100, opsz 144) statt 600 bis 900;
  · ohne Internes: Platzhalter-Hinweise, die nicht gewählte Farbwelt B mit Probe-Seiten, «Projekt Nummer 10» (Vergleich mit anderen Häusern),
    die Schriftwahl gegen den Platzhalter, den Vermerk zur Station.
«Als PDF sichern» öffnet das Druckfenster (A4 quer)."""
import hashlib, html, io, os, re, shutil

e = html.escape
HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))
LOGO = os.path.join(PROJEKT, '_quelle', 'logo', 'original', 'culinarium-logo-original.svg')


def _v(n):
    p = os.path.join(HIER, n)
    return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:10] if os.path.exists(p) else '1'


def original():
    s = open(LOGO, encoding='utf-8').read()
    d = {k: re.search(r'<path id="%s"[^>]* d="([^"]+)"' % k, s).group(1) for k in ('wm', 'zeile')}
    vb = {'marke': re.search(r'viewBox="([^"]+)"', s).group(1), 'wortmarke': re.search(r'data-wm="([^"]+)"', s).group(1),
          'zeile': re.search(r'data-zeile="([^"]+)"', s).group(1)}
    pf = {'marke': d['wm'] + d['zeile'], 'wortmarke': d['wm'], 'zeile': d['zeile']}
    return pf, vb


def ersetze(s, alt, neu, n=1):
    """Genau n Treffer, sonst Abbruch: Station 05 hat sich geändert, erst nachsehen."""
    k = s.count(alt)
    if k != n:
        raise SystemExit(f'Markenbuch: «{alt[:70]}» {k}× statt {n}×, erst klären')
    return s.replace(alt, neu)


def weg(s, muster, n=1):
    s2, k = re.subn(muster, '', s, flags=re.S)
    if k != n and not (n == 0 and k >= 1):                       # n=0: mindestens einmal, alle weg
        raise SystemExit(f'Markenbuch: Muster «{muster[:60]}» {k}× statt {n}×, erst klären')
    return s2


ALT_VB = {'wortmarke': '0 0 6072 620', 'zeile': '0 0 6388 268', 'marke': '0 0 6388 1484'}


def logo_tauschen(s, pf, vb):
    """Symbole #wortmarke, #zeile, #marke mit Rudis Pfaden; die viewBox jeder Verwendung mit."""
    for k in ('wortmarke', 'zeile', 'marke'):
        s, n = re.subn(r'<symbol id="%s" viewBox="[^"]+">.*?</symbol>' % k, f'<symbol id="{k}" viewBox="{vb[k]}"><path d="{pf[k]}"/></symbol>', s, flags=re.S)
        if n != 1:
            raise SystemExit(f'Markenbuch: Symbol {k} {n}×, erst klären')
        s = s.replace(f'viewBox="{ALT_VB[k]}"', f'viewBox="{vb[k]}"')
    return s.replace('aria-label="A unique experience by Momo x Rudi"', 'aria-label="A unique experience"').replace(
        'aria-label="Culinarium, a unique experience by Momo x Rudi"', 'aria-label="Culinarium, a unique experience"')


def zeichen_dateien(ziel, pf, vb):
    """buch/zeichen/: Wortmarke, Zeile und beides zusammen aus Rudis Original, gleiche Namen und Farben wie bei Station 05 (C und x bleiben)."""
    for n in os.listdir(ziel):
        m = re.match(r'(wortmarke-mit-zeile|wortmarke|zeile)(-[a-z]+)?\.svg$', n)
        if not m:
            continue
        alt = open(os.path.join(ziel, n), encoding='utf-8').read()
        f = re.search(r'fill="(#[0-9A-Fa-f]{3,6}|currentColor)"', alt)
        farbe = f.group(1) if f else 'currentColor'
        k = {'wortmarke-mit-zeile': 'marke', 'wortmarke': 'wortmarke', 'zeile': 'zeile'}[m.group(1)]
        titel = {'marke': 'Culinarium · A UNiQUE EXPERiENCE', 'wortmarke': 'Culinarium', 'zeile': 'A UNiQUE EXPERiENCE'}[k]
        open(os.path.join(ziel, n), 'w', encoding='utf-8').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[k]}"><title>{titel} · Original von Rudi</title><path fill="{farbe}" d="{pf[k]}"/></svg>\n')


def fraunces_wie_website(web, ziel):
    """Fraunces der Website (variabel) auf die Werte der Titel festgesetzt: wght 340, SOFT 100, opsz 144, WONK 1 (culinarium.css .gross).
    Als eine Schrift für alle Stärken eingetragen: jede Stelle des Buchs, die Fraunces setzt, steht wie die Titel der Website (nie fett)."""
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    f = TTFont(os.path.join(web, 'assets', 'schrift', 'fraunces-soft.woff2'))
    inst = instancer.instantiateVariableFont(f, {'wght': 340, 'SOFT': 100, 'opsz': 144, 'WONK': 1})
    inst.flavor = 'woff2'
    inst.save(os.path.join(ziel, 'schriften', 'Fraunces-340-wie-website.woff2'))


def ohne_internes(s, schrift='../../assets/schrift/'):
    # Titel: Platzhalter-Hinweis und Weg zur Probe
    s = weg(s, r'\s*<p class="titel__ph"[^>]*>.*?</p>')
    s = weg(s, r'<a class="kn kn--linie" href="probe\.html"[^>]*>.*?</a>', 1)
    s = s.replace('<a href="#welten" data-r style="--i:4"><span>Welten</span></a>', '<a href="#welten" data-r style="--i:4"><span>Farbwelt</span></a>')
    # Zeichen und Name: Rudis Original
    s = ersetze(s, '<span class="z"><span><em>vorerst ein Platzhalter.</em></span></span>', '<span class="z"><span><em>ein Original.</em></span></span>')
    s = re.sub(r'(<p class="mk__lead">)Rudi sagt am 26\. Oktober 2026:.*?neu geprüft\.(</p>)',
               r'\1Die Wortmarke ist Rudis Original: CULINARIUM in einer breiten Display-Schrift der 70er, dicke Stämme, dünne Diagonalen, Enden wie Tropfen, '
               r'darunter linksbündig die Zeile «A UNiQUE EXPERiENCE». Sie wird als Datei eingesetzt, nie nachgezeichnet. Auf den Plakaten steht darunter «BY MOMO X RUDI».\2', s, count=1, flags=re.S)
    s = weg(s, r'\s*<div class="band hinweis" data-r>.*?</div>')
    # Farbwelt: nur die gewählte, ohne Probe-Seiten
    s = re.sub(r'(<section class="[^"]*" id="welten">.*?<p class="mk__lead">).*?(</p>)',
               r'\1Die Website trägt das Plakat: Schiefer, abgedunkelt, als dunkle Fläche, Warmweiss als helle, betont wird mit der Farbe des Abends. '
               r'Solange der nächste Abend keine eigene Farbe hat, gilt Orange vom Februar 2025, nah am Licht im Flur der Bar.\2', s, count=1, flags=re.S)
    s = weg(s, r'\s*<div class="welt welt--nicht">.*?</div>\s*</div>(?=\s*</div>\s*</div>\s*</section>)')
    s = weg(s, r'\s*<div class="ger" data-r="feder" style="--i:0">.*?</div>\s*<img class="ger__tel"[^>]*>\s*</div>')
    s = weg(s, r'\s*<div class="knr"><a class="kn " href="probe\.html\?welt=a".*?</div>')
    s = s.replace('<span class="kw">HAASEMANNSTRASSE 13 · WELT A</span>', '<span class="kw">HAASEMANNSTRASSE 13</span>')
    s = s.replace('Ein Klick auf ein Plakat färbt dieses Markenbuch um, Welt A.', 'Ein Klick auf ein Plakat färbt die Hausregeln um.')
    # Schrift: Werte der Website, ohne die Schriftwahl gegen den Platzhalter
    s = ersetze(s, '<dd>600 bis 900, weich, gross und klein, Zutatenzeilen in Versalien</dd>',
                '<dd>leicht, 340 für Titel, 300 für Rudis Zeilen in Versalien, weiche Enden (SOFT 100); nie fett, nie kursiv</dd>')
    s = ersetze(s, '<dd>Titel, Zutatenzeilen, grosse Zahlen; aus der Wortmarke abgeleitet</dd>', '<dd>Titel, Rudis Zeilen, grosse Zahlen</dd>')
    s = ersetze(s, '<dd>800 und 900, Versalien, das i klein, gesperrt</dd>', '<dd>600 und 700, Versalien, 0,12 em gesperrt</dd>')
    s = ersetze(s, '<dd>Kapitelzeilen, Bildzeilen, Knöpfe, das Band; aus der Zeile der Plakate</dd>', '<dd>Kapitelzeilen, Bildzeilen, Knöpfe; aus der Zeile der Plakate</dd>')
    s = ersetze(s, '<dd>Regular 400 und Semibold 600</dd>', '<dd>400, 17 px, Zeilenabstand 1,62</dd>')
    s = s.replace('Die Etiketten nehmen die Zeile auf: Urbanist, kräftig, gesperrt,', 'Die Etiketten nehmen die Zeile auf: Urbanist, gesperrt,')
    s = weg(s, r'\s*<div class="rang">.*?(?=\s*</div>\s*</section>)')
    # Logo richtig und falsch: für das Original
    s = weg(s, r'Die Regeln gelten vorerst für den Platzhalter aus Profilbild und Plakaten; mit Rudis Original werden sie neu gezeichnet\.\s*')
    s = s.replace('Auf dunkler Fläche in Warmweiss, Form unverändert, aus dem Zug der Original-Pixel.', 'Auf dunkler Fläche in Warmweiss, Form unverändert.')
    # Farben und Herkunft: ohne die nicht gewählte Welt B
    for a, b in (('Daraus die Welt B und die Tiefe der dunklen Flächen.', 'Daraus die Tiefe der dunklen Flächen.'),
                 ('Das Licht der Abende. Daraus die Betonung der Welt B, auf dunkler Fläche hell und warm.', 'Das Licht der Abende, auf dunkler Fläche hell und warm.'),
                 ('Sirup in Glas, Zapfhähne aus Metall. Der Honig ist die Betonung der Welt B auf hellem Grund.', 'Sirup in Glas, Zapfhähne aus Metall.'),
                 ('Glas auf Tischplatte, dahinter Dunkel. Tischplatte und Dunkel sind die Flächen der Welt B.', 'Glas auf Tischplatte, dahinter Dunkel.')):
        s = ersetze(s, a, b)
    # Projekt Nummer 10: Vergleich mit anderen Häusern
    s = weg(s, r'\s*<section class="[^"]*" id="unterschied">.*?</section>')
    # Zum Mitnehmen
    s = s.replace('Wortmarke, Zeile und C als Vektor (Platzhalter, bis Rudis Original da ist),', 'Wortmarke, Zeile und C als Vektor,')
    s = s.replace('<small>Platzhalter · SVG, Schiefer-Violett</small>', '<small>Original von Rudi · SVG, Schiefer-Violett</small>')
    s = s.replace('<small>Platzhalter · SVG, Warmweiss</small>', '<small>Original von Rudi · SVG, Warmweiss</small>')
    s = s.replace('<small>Platzhalter · SVG, Zeichen</small>', '<small>SVG, Zeichen</small>')
    s = s.replace('<small>beide Welten und sechs Abende als CSS-Datei</small>', '<small>Farben und sechs Abende als CSS-Datei</small>')
    s = ersetze(s, '<small>600 bis 900, WOFF2, Lizenz OFL</small></span><a class="kn " href="schriften/Fraunces-Soft-600_900.woff2"',
                '<small>wie die Website, WOFF2, Lizenz OFL</small></span><a class="kn " href="' + schrift + 'fraunces-soft.woff2"')
    s = ersetze(s, '<a class="kn " href="schriften/Urbanist-400_900.woff2"', '<a class="kn " href="' + schrift + 'urbanist.woff2"')
    s = re.sub(r'<p class="ende__s">.*?</p>', '<p class="ende__s">Die Hausregeln · Culinarium Hannover · Stand {stand}. Abendfarbe Orange, bis der nächste Abend seine eigene Farbe hat.</p>', s, count=1, flags=re.S)
    s = weg(s, r'<a class="kn " href="probe\.html" target="_blank" rel="noopener">.*?</a>', 0)
    return s


def ohne_band(s, buch=True):
    """Oberchef 28.10.2026 (auf culinarium-livre, Robert hat das Band am 26.10. als Beschriftung abgelehnt): das warmweisse Band mit doppelter Linie bleibt
    nur als Merkmal der Plakate (belegt auf allen 12 Plakaten in _quelle/extern/ig/, pruefung/belege/band-auf-den-plakaten.png). Der Baustein «Das Band» für
    Website und Drucksachen und die Logo-Fassungen auf dem Band («Auf dem Band», «Unter dem Foto») kommen raus, ebenso jede Regel, die das Band als
    Beschriftung auf Website oder Drucksachen verlangt."""
    regel = lambda t: r'<div class="regel regel--r"[^>]*><div class="regel__f">(?:(?!<div class="regel ).)*?<h3>%s</h3><p>[^<]*</p></div>' % t
    s = weg(s, regel('Auf dem Band'))
    s = weg(s, regel('Unter dem Foto'))
    for a, b in ((' Die doppelte Linie des Bandes zählt nicht als Störung.', ''),
                 (' Die Wortmarke gehört auf das Band.', ''),
                 (' Das Band liegt unter dem Bild, über die ganze Breite.', '')):
        s = ersetze(s, a, b)
    s = s.replace('Acht Dinge, die gehen, und acht, die nicht gehen.', 'Sechs Dinge, die gehen, und acht, die nicht gehen.')   # nur im Markenbuch
    if not buch:
        return s
    # ohne die Band-Fassung bleiben drei Tafeln und drei Zeichen: in drei Spalten, keine allein am Rand (Fehlerbuch 10a, 20.10.2026)
    s = s.replace('</head>', '<style>@media (min-width:900px){.lockups{grid-template-columns:repeat(3,minmax(0,1fr))!important}.reihe5{grid-template-columns:repeat(3,minmax(0,1fr))!important}}</style>\n</head>', 1)
    s = weg(s, r'\s*<figure class="lock lock--papier"[^>]*>(?:(?!</figure>).)*AUF DEM BAND(?:(?!</figure>).)*</figure>')
    s = weg(s, r'\s*<div class="zei"[^>]*><span class="band"[^>]*></span><b>Das Band</b><small>[^<]*</small></div>')
    s = weg(s, r'\s*<div data-r style="--i:2"><h3>Das Band statt Schrift im Bild\.</h3><p>[^<]*</p></div>')
    s = weg(s, r'<div class="bau"[^>]*>(?:(?!<div class="bau").)*?<h3>Das Band</h3><p>[^<]*</p></div>')
    s = weg(s, r'\s*<div data-r style="--i:2"><h3>Die Probe\.</h3><p>.*?</p></div>')
    for a, b in (('Auf Fotos nie; dafür gibt es das Band.', 'Auf Fotos nie.'),
                 ('dunkle Flächen wie die Bar, warmweisse Bänder wie das Plakat, und eine Farbe', 'dunkle Flächen wie die Bar, Warmweiss wie das Plakat, und eine Farbe'),
                 ('<span class="z"><span>Knopf, Band,</span></span><span class="z"><span><em>Bon und Zeile.</em></span></span>', '<span class="z"><span>Knopf, Bon</span></span><span class="z"><span><em>und Zeile.</em></span></span>'),
                 (' Das Band trägt Namen und Daten.', ''),
                 ('Daraus kommt die Ordnung der Seite: das Bild wechselt, das Band bleibt, die Farbe gehört dem nächsten Abend.', 'Daraus kommt die Ordnung der Seite: das Bild wechselt, die Farbe gehört dem nächsten Abend.'),
                 ('Die Seite spielt beides: dunkle Flächen wie die Bar, warmweisse Bänder wie das Plakat, und Bilder', 'Die Seite spielt beides: dunkle Flächen wie die Bar, Warmweiss wie das Plakat, und Bilder'),
                 ('<p>Das Band unter dem Bild: wie auf jedem Plakat sitzt unter dem Foto ein warmweisses Band mit doppelter Linie, darin Name, Datum oder Zeile in der Etikettschrift. Keine Schrift auf dem Foto, kein Schild darüber. Dazu die Abendfarbe: die Betonung der ganzen Seite wechselt mit dem Plakat des nächsten Abends.</p>',
                  '<p>Die Abendfarbe: die Betonung der ganzen Seite wechselt mit dem Plakat des nächsten Abends. Keine Schrift auf dem Foto, kein Schild darüber.</p>')):
        s = ersetze(s, a, b)
    return s


STAND_MARKE = '<meta name="stand" content="website-2026-10-28">'   # Markenbuch der Station 05 steht schon auf dem Stand der Website


def website_stand(s, schrift='../../assets/schrift/'):
    """Markenbuch der Station 05 → Stand der Website: Rudis Original, ohne Internes, Band nur als Merkmal der Plakate. Steht es schon so, unverändert."""
    if STAND_MARKE in s:
        return s
    pf, vb = original()
    return ohne_band(ohne_internes(logo_tauschen(s, pf, vb), schrift))


def aus_station5(st5, web, daten):
    """st5 = Ordner marke/ der Station 05, web = website/. Schreibt buch.html und buch/."""
    ziel = os.path.join(HIER, 'buch')
    if os.path.isdir(ziel):
        shutil.rmtree(ziel)
    for d in ('bilder', 'zeichen', 'schriften'):
        shutil.copytree(os.path.join(st5, d), os.path.join(ziel, d))
    os.makedirs(os.path.join(ziel, 'logo-richtig-falsch'))
    for n in ('marke.css', 'marke.js', 'farben.css', 'farben.svg'):
        shutil.copyfile(os.path.join(st5, n), os.path.join(ziel, n))
    for n_ in os.listdir(os.path.join(ziel, 'zeichen')):   # Tor 3, 30.10.2026: Tapete ohne das x an den Kreuzungen, das Zeichen ist das C
        if n_.startswith('tapete'):
            q_ = os.path.join(ziel, 'zeichen', n_); t_ = open(q_, encoding='utf-8').read(); open(q_, 'w', encoding='utf-8').write(re.sub(r'<svg [^>]*viewBox="0 0 224 228"[^>]*>.*?</svg>', '', t_, flags=re.S))
    pf, vb = original()
    zeichen_dateien(os.path.join(ziel, 'zeichen'), pf, vb)
    fraunces_wie_website(web, ziel)
    css = open(os.path.join(ziel, 'marke.css'), encoding='utf-8').read()
    css = ersetze(css, "@font-face{font-family:'Fraunces Soft';font-style:normal;font-weight:400 900;font-display:swap;src:url('schriften/Fraunces-Soft-600_900.woff2') format('woff2')}",
                  "@font-face{font-family:'Fraunces Soft';font-style:normal;font-weight:1 1000;font-display:swap;src:url('schriften/Fraunces-340-wie-website.woff2') format('woff2')}")
    css = re.sub(r'^/\* Markenbuch Culinarium Hannover · Station 05[^*]*\*/', '/* Markenbuch Culinarium Hannover · Le Livre */', css, count=1)
    css += ('\n/* Robert 29.10.2026: Zeichen-Kacheln passen in jede Breite, letzter Baustein volle Breite, am Ende nur das C in Orange */\n'
            '.g1{width:min(118px,34%)}.g2{width:min(66px,19%)}.g3{width:min(38px,11%)}.g4{width:min(20px,6%)}\n'
            '.lock--groessen>div{gap:min(52px,6%)}\n'
            '.lock--quer .lock__z{width:min(80px,15%);flex:none}.lock--quer .lock__wq{width:min(300px,62%)}\n'
            '.baus>.bau:last-child:nth-child(odd){grid-column:1/-1}\n'
            '.ende__w{color:var(--papier)}\n'
            '@media (min-width:900px){html body .reihe5{grid-template-columns:repeat(2,minmax(0,1fr))!important}}\n'
            '.kn.kn--leiste{height:44px;padding-left:20px;font-size:10.5px;flex:none;border:0;cursor:pointer}\n'
            '@media (max-width:1365px){.kn.kn--leiste{margin-left:auto}}\n'
            '.mk__t{line-height:1.08}.mk__t .z+.z{margin-top:.04em}\n'
            '/* Robert 29.10.2026: Schrift in Knöpfen optisch mittig (Messlauf text-mitte) */\n.kn>.kw{text-box:trim-both cap alphabetic}\n'
            '/* Messlauf 29.10.2026 (Regel einzelwort): kein einzelnes Wort allein in der letzten Titelzeile */\nh1,h2,h3,h4,figcaption{text-wrap:balance}\n'
            '/* Messlauf 29.10.2026 (Regel beschnitten): Plakate der Herkunft ganz zeigen, Schrift und Wortmarke nicht abschneiden */\n.her__b img{object-fit:contain}\n'
            '/* Tor 3, 30.10.2026: Kapitel-Leiste am Handy nie unter dem Blatt, keine Raute am Zeilenanfang; Bildraster ohne Loch; 5 % auf derselben Grundlinie */\n'
            '.titel{padding-bottom:var(--rund)}@media (min-width:761px){.index::before{content:"";flex-basis:100%;order:1;height:0}.index a:nth-child(n+7){order:2}.index a:nth-child(7)::before{display:none}}@media (max-width:760px){.index a+a::before{display:none}.collage>.bi:nth-last-child(2):nth-child(even){grid-column:1/-1!important}.collage>.bi:nth-last-child(2):nth-child(even) .k3__b{aspect-ratio:4/3}}\n'
            '@media (min-width:621px){.anteil__b>span:last-child small{display:block;visibility:hidden;width:0;overflow:hidden;white-space:nowrap}}\n'
            '.wo{white-space:nowrap}\n'
            '.lf .mono{font-family:var(--mono)}\n'
            '/* Tor 2, 30.10.2026: eine Navigation (die Leiste oben nennt keine Kapitel mehr, die Inhaltsleiste nennt alle); 5 % nie abgeschnitten; Musterzeilen ausgewogen; Ortszeile am Handy ohne Raute am Zeilenende */\n'
            '@media (min-width:1001px){.regeln--4:has(>:nth-child(6):last-child){grid-template-columns:repeat(3,minmax(0,1fr))}}.laden li:last-child:nth-child(odd){grid-column:1/-1}'
            '@media (min-width:1001px){.regeln--4:has(>:nth-child(8)) .regel h3{min-height:calc(2.3em + clamp(24px,2.4vw,34px));display:flex;align-items:flex-start}}.drei .k3:nth-child(2),.hers .her{margin-top:0!important}.regeln--4 .regel h3{margin-top:0}.kn.kn--leiste{margin-left:auto}'
            '@media (max-width:600px){.sch__satz--ganz{white-space:nowrap!important;text-wrap:nowrap!important}.sch__satz--a{font-size:6.2vw!important}.sch__satz--b{font-size:4.7vw!important}}'
            '.leiste__k{display:none!important}.anteil__b>span{min-width:max-content}.sch__satz{text-wrap:balance}'
            '@media (max-width:760px){.titel__ort{display:flex;flex-direction:column;align-items:center;gap:6px}.titel__ort .raute{display:none}}\n'
            '/* Tor 3, 30.10.2026 (K37): bei «weniger Bewegung» kein Auftritt, keine Schleife, alles steht sofort */\n'
            '@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}.js [data-r],.z>span{opacity:1!important;transform:none!important;clip-path:none!important}.js [data-r="flug"]{transform:rotate(var(--rot,0deg))!important}}\n')
    # Robert 30.10.2026: kein gekreuztes Zeichen; «Falsch» zeigt der rote Kreis mit einem Querstrich
    css = ersetze(css, "<path d='M10 10l10 10M20 10L10 20' stroke='white' stroke-width='2.4' stroke-linecap='round'/>", "<path d='M9.5 15h11' stroke='white' stroke-width='2.4' stroke-linecap='round'/>")
    # Bewegungs-Tor 30.10.2026 (Regel 55): bewegt wird nur über transform und opacity; Farbe und Schatten stehen sofort
    css = css.replace('transition:color .4s', 'transition:none').replace('transition:transform .55s var(--e2),box-shadow .55s var(--e2)', 'transition:transform .55s var(--e2)')
    open(os.path.join(ziel, 'marke.css'), 'w', encoding='utf-8').write(css)

    s = open(os.path.join(st5, 'markenbuch.html'), encoding='utf-8').read()
    s = website_stand(s).replace('{stand}', e(daten['stand']['datum']))
    # Robert 29.10.2026 («und das braucht der Kunde doch nicht?»): Wahl der Farbwelt und offene Rechtefragen sind Arbeitsstand
    s = weg(s, r'\s*<section class="[^"]*" id="welten">.*?</section>')
    s = weg(s, r'<a href="#welten"[^>]*>.*?</a>', 0)
    s = re.sub(r'<p class="ende__s">.*?</p>', '<p class="ende__s">Die Hausregeln · Culinarium Hannover · Stand ' + e(daten['stand']['datum'])
               + '. Abendfarbe Orange, bis der nächste Abend seine eigene Farbe hat.</p>', s, count=1, flags=re.S)
    s = s.replace('Sie bleiben in jeder Farbwelt.', 'Sie bleiben an jedem Abend.')
    # Tor 3, 30.10.2026: das x ist kein Zeichen des Hauses; keine offene Rechtefrage beim Kunden; Titel ohne Einzelwort; Trenner nie am Zeilenanfang oder -ende
    s = ersetze(s, 'die Wortmarke, das C und das x, das Band', 'die Wortmarke und das C, das Band')
    s = ersetze(s, 'an jeder Kreuzung das x, in jedem Feld das C', 'in jedem Feld das C')
    s = ersetze(s, 'Wer sie gemacht hat und wer darauf zu sehen ist, ist noch nicht belegt; Namen stehen deshalb nirgends im Bild.', 'Namen von Fotografen und Gästen stehen nirgends im Bild.')
    s = ersetze(s, '<span class="z"><span>Woher die Farben</span></span><span class="z"><span><em>kommen.</em></span></span>', '<span class="z"><span>Woher die</span></span><span class="z"><span><em>Farben kommen.</em></span></span>')
    s = ersetze(s, '<span class="z"><span><span class="sl">/ </span>Limette', '<span class="z"><span>Limette')
    s = ersetze(s, 'in vier Wörtern: AUBERGINE / KOKOS / LIMETTE / SESAM.', 'in vier Wörtern: <span class="wo">AUBERGINE / KOKOS / LIMETTE / SESAM.</span>')
    s = re.sub(r'<p class="sch__satz[^"]*"[^>]*>.*?</p>', lambda m: re.sub(r'((?:<span class="ro"[^>]*>[^<]*</span>)+)', r'<span class="wo">\1</span>', m.group(0)), s, flags=re.S)   # Musterzeilen brechen nur zwischen Wörtern
    # Tor 3, 30.10.2026: Musterzeilen mit Trennern («/», «·») stehen am Handy einzeilig (kleiner gesetzt), «BY MOMO X RUDi» bricht nie; RGB-Werte der Farbkarten nie umbrochen; ein Knopf zur Seite «Logo richtig und falsch»
    s = re.sub(r'<p class="sch__satz([^"]*)" aria-label="([^"]*(?: / | · )[^"]*)"', lambda m: f'<p class="sch__satz{m.group(1)} sch__satz--ganz sch__satz--{"a" if "/" in m.group(2) else "b"}" aria-label="{m.group(2)}"', s)
    s = s.replace('Schrift, Wortmarke, dunkle Fläche in A<', 'Schrift, Wortmarke, dunkle Fläche<')   # Rolle in der Quelle mitten im Wort abgeschnitten
    WO = r'<span class="wo">(?:<span class="ro"[^>]*>[^<]*</span>)+</span>'
    s = re.sub(r'(<p class="sch__satz[^"]*" aria-label="[^"]*MOMO X RUD[^"]*">.*?)((?:' + WO + r'\s*){3}' + WO + r')(</p>)', lambda m: m.group(1) + '<span class="wo">' + m.group(2) + '</span>' + m.group(3), s, flags=re.S)
    s = re.sub(r'(<span>RGB</span>)([\d ·]+)', r'\1<span class="wo">\2</span>', s)
    s, n_ = re.subn(r'\s*<div class="knr knr--mitte"><a class="kn kn--linie" href="(?:\./)?(?:buch/)?logo-richtig-falsch/index\.html"[^>]*><span class="kw">LOGO R(?:<span class="ki">)?[iI](?:</span>)?CHT.*?</div>', '', s, count=1, flags=re.S)
    if not n_:
        raise SystemExit('Markenbuch: zweiter Knopf «Logo richtig und falsch» nicht gefunden')
    # Robert 29.10.2026: das Team wird geduzt, nicht gesiezt
    s = s.replace('Probieren Sie es gern aus.', 'Probier es gern aus.')
    # Robert 29.10.2026 («wieso ist … überall dieses x ???»): das Zeichen des Hauses ist das C; das x aus «Momo x Rudi» ist kein eigenes Zeichen
    s = weg(s, r'\s*<div class="zei"[^>]*><svg class="" viewBox="0 0 224 228"[^>]*><use href="#x"/></svg><b>Das x</b>.*?</div>')
    s = weg(s, r'\s*<li data-r style="--i:\d+"><span><b>Das x</b><small>SVG</small></span>.*?</li>')
    s = s.replace('<small>Farbwelt und sechs Abende als CSS-Datei</small>', '<small>Farben und sechs Abende als CSS-Datei</small>')
    # Wege der Dateien
    s = re.sub(r'(src|href)="(\./)?(bilder|zeichen|schriften|logo-richtig-falsch|marke\.css|marke\.js|farben\.css|farben\.svg)', r'\1="buch/\3', s)
    s = re.sub(r'url\((\./)?(zeichen|bilder)/', r'url(buch/\2/', s)
    s = s.replace("url('schriften/", "url('buch/schriften/")
    # Leiste des Buchs als Leiste des Werkzeugs: zurück ins Werkzeug, Blätter, «Als PDF sichern» statt «Die Probe» (Stil des Buchs bleibt)
    name = daten['namen']['marke']
    zu = re.sub(r'^Das |^Der ', 'zum ', re.sub(r'^Die ', 'zur ', name)) if re.match(r'^(Das|Der|Die) ', name) else 'zu ' + name   # «Zurück zum Markenbuch»
    s = ersetze(s, '<a class="leiste__m" href="#oben">', '<a class="leiste__m" href="./" title="Zurück ' + e(zu) + '">')
    s, n_ = re.subn(r'<small>(Station 05 · )?Culinarium Hannover</small>', '<small>Zurück ' + e(zu) + '</small>', s, count=1)
    s = s.replace('<a href="#welten"><span class="kw">WELTEN</span></a>', '<a href="#welten"><span class="kw">FARBWELT</span></a>')
    # Robert 29.10.2026 («was das für ein hässlicher button da oben?»): der Knopf des Hauses mit Knauf, wie «Platz anfragen», statt Glanzring
    knopf = ('<button class="kn kn--leiste" type="button" id="bu-pdf"><span class="kw">ALS PDF S<span class="ki">i</span>CHERN</span>'
             '<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v10M3.5 7.5 8 12l4.5-4.5M3 14h10"/></svg></i></button>')
    s, n_ = re.subn(r'<a class="glanz" href="probe\.html"[^>]*>.*?</a>', knopf, s, count=1, flags=re.S)
    if not n_:                                                   # Station 05 auf Website-Stand: der Weg zur Probe ist dort schon weg
        s = re.sub(r'(<nav class="leiste".*?)(</nav>)', lambda m: m.group(1) + knopf + m.group(2), s, count=1, flags=re.S)
    kap = [m.group(1) for m in re.finditer(r'<section class="[^"]*\bblatt\b[^"]*" id="([a-z]+)"', s)]
    style = ('<style>button.glanz{border:0;cursor:pointer;font:inherit;flex:none}.leiste{min-width:0}.leiste__k{min-width:0;flex-wrap:nowrap;justify-content:center;gap:clamp(8px,.85vw,18px);font-size:.58rem;letter-spacing:.13em;white-space:nowrap}'
             '@media (max-width:1365px){.leiste__k{display:none}.leiste{justify-content:space-between}}'
             '.welten{grid-template-columns:minmax(0,760px)!important;justify-content:center}'
             '@page{size:A4 landscape;margin:10mm}@media print{.leiste{display:none}[data-r],[data-g],.z>span{opacity:1!important;transform:none!important;clip-path:none!important}'
             '.ab,.titel{-webkit-print-color-adjust:exact;print-color-adjust:exact}.ab{break-before:page;padding-top:30px!important;padding-bottom:24px!important}'
             '.titel{min-height:0!important;padding:40px 0!important;break-after:page}.fenster{height:620px!important;break-before:page;break-inside:avoid}.fenster__f{position:absolute!important;inset:0!important}'
             '.fenster__b{position:absolute!important;inset:0!important;height:auto!important;margin:0!important;z-index:0!important}.fenster__t{position:absolute!important;left:0;right:0;top:50%;z-index:1!important}'
             '.mk{margin-bottom:22px!important}figure,.regel,.fz,.sch,.welt,.lock,.zei,.laden li{break-inside:avoid}'
             '.knr:has(.kn){display:none}.index,.titel__runter{display:none}}</style>')
    s = re.sub(r'<link rel="icon"[^>]*>', '', s)
    s = s.replace('</head>', style + '<link rel="icon" href="/assets/oberflaeche/kleid/culinarium-zeichen.svg" type="image/svg+xml"></head>', 1)
    s = re.sub(r'<title>[^<]*</title>', '<title>Die Hausregeln · Culinarium Hannover</title>', s, count=1)
    # Robert 29.10.2026: das Werkzeug heisst «Das Markenbuch», dieser Teil «Die Hausregeln»
    for a, b in (('<span class="kw">MARKENBUCH</span>', '<span class="kw">DIE HAUSREGELN</span>'), ('MARKENBUCH · OKTOBER 2026', 'DIE HAUSREGELN · OKTOBER 2026'),
                 ('aria-label="Markenbuch"', 'aria-label="Die Hausregeln"'), ('färbt dieses Markenbuch um', 'färbt die Hausregeln um')):
        s = s.replace(a, b)
    s = s.replace('</body>', f'<script src="buch.js?v={_v("buch.js")}"></script></body>', 1)
    sichtbar = re.sub(r'<(style|script)[^>]*>.*?</\1>|<[^>]+>', ' ', s, flags=re.S)
    for w in ('Platzhalter', 'Station 0', 'Tasty', 'probe.html', 'Welt B', 'PROBE', 'Projekt Nummer', 'Rivage', 'Carlton', 'Schäfli', 'Schlössli', 'Zurbriggen',
              'Seiler', 'Doldenhorn', 'Ruedihus', 'Salt & Silver', '_quelle/', '_kette/', 'Späher', 'nicht gewählt', 'Zug der Original-Pixel'):
        if w in (sichtbar if w not in ('probe.html',) else s):
            raise SystemExit(f'Markenbuch: «{w}» steht noch drin, erst klären')
    # Stempel der Stilblätter aus ihrem Inhalt, damit der Browser nach jeder Änderung neu lädt (30.10.2026)
    s = re.sub(r'(buch/(marke\.css|marke\.js|farben\.css))\?v=[^"\']*', lambda m: m.group(1) + '?v=' + hashlib.sha1(open(os.path.join(ziel, m.group(2)), 'rb').read()).hexdigest()[:10], s)
    open(os.path.join(HIER, 'buch.html'), 'w', encoding='utf-8').write(s)
    # Logo richtig und falsch als eigene Seite: dieselbe Seite der Station 05, mit Rudis Original, Weg zurück ins Markenbuch des Werkzeugs
    r = open(os.path.join(st5, 'logo-richtig-falsch', 'index.html'), encoding='utf-8').read()
    r = logo_tauschen(r, pf, vb)
    if '<h3>Auf dem Band</h3>' in r:                         # Station 05 vor dem Nachziehen; danach steht die Seite schon so
        r = ohne_band(r, buch=False)
    r = r.replace('../markenbuch.html', '../../buch.html')
    for x, y in (('aria-label="Markenbuch"', 'aria-label="Die Hausregeln"'), ('<span class="kw">MARKENBUCH</span>', '<span class="kw">DIE HAUSREGELN</span>'), ('ZUM MARKENBUCH', 'ZU DEN HAUSREGELN')):
        r = r.replace(x, y)
    r = re.sub(r'Vorerst für den Platzhalter:.*?Eine Datei des Gestalters fehlt noch\.', 'Wortmarke, Zeile und C sind Dateien. Sie werden eingesetzt, nie nachgezeichnet, nie verändert.', r, flags=re.S)
    r = r.replace('Auf dunkler Fläche in Warmweiss, Form unverändert, aus dem Zug der Original-Pixel.', 'Auf dunkler Fläche in Warmweiss, Form unverändert.')
    r = re.sub(r'<title>[^<]*</title>', '<title>Logo richtig und falsch · Culinarium Hannover</title>', r, count=1)
    if 'Platzhalter' in re.sub(r'<[^>]+>', ' ', r) or 'Station 05' in r:
        raise SystemExit('Logo richtig und falsch: Platzhalter oder Station steht noch drin, erst klären')
    open(os.path.join(ziel, 'logo-richtig-falsch', 'index.html'), 'w', encoding='utf-8').write(r)
    return kap
