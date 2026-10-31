#!/usr/bin/env python3
"""Markenbuch des Grand Beau-Rivage Interlaken, Fassung 2 (Robert 12.10.2026: «komplett überarbeiten … richtig luxuriös und elegant und edel …
federnde, pulsierende reinfliegende Kacheln … geile Animationen … auf dem Niveau der Website»).

   PYTHONPATH=~/Desktop/Website-Projekte/_Werkbank-Kit python3 _werkbank/markenbuch.py      → marke/buch/index.html (+ zeichen.svg, farben.css)

Seit 12.10.2026 ein Kapitel von Le Livre (marke/). marke/buch/marke.css und marke/buch/marke.js sind von Hand. Bausteine aus dem UI-Fundus und der Website des Hauses (Eröffnungs-Vorhang seit 12.10.2026 raus, Robert: nie wieder): Zeilen-Maske,
Kapitelzeile mit Linie, Kachel schwebt mit Überschwung (federnd, Fotos von Anfang an sichtbar), Kachel-Neigung zur Maus (.k3), Bild-Vorhang,
Flug (Lockups, Drucksachen), Fenster (sticky), Gleiten (Scroll-Zeitachse), Grosse Zahlen, Lichtstreif, Einkerbung mit runden Ecken, Glanzkante,
Knopf mit Tiefe und Puls, Strich mit Zeichen. Farben, Herkunft und Messung: marke_daten.py. Jedes Foto nur einmal auf der Seite.
Fassung 1: _qa/sicherung/2026-10-12-markenbuch-v1/."""
import html, os, shutil, sys

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
sys.path.insert(0, W)
import haus as H  # noqa: E402
from marke_daten import GRUPPEN, F, HERKUNFT, GLANZ, GLANZ_SATZ, glanz_stopps, foto, streifen, rgb, lum, kontrast  # noqa: E402

e = html.escape
ZIEL = os.path.join(ROOT, 'marke')
BUCH = os.path.join(ZIEL, 'buch')   # seit 12.10.2026 ein Kapitel von Le Livre (marke/ ist das Werkzeug, _werkbank/livre_bau.py)
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
PU = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v10M3.5 7.5 8 12l4.5-4.5M3 14h10"/></svg>'

KAPITEL = [('haltung', 'Haltung'), ('zeichen', 'Zeichen'), ('farben', 'Farben'), ('herkunft', 'Herkunft'), ('schrift', 'Schrift'),
           ('tapete', 'Tapete'), ('bilder', 'Bilder'), ('bausteine', 'Bausteine'), ('anwendung', 'Anwendung'), ('mitnehmen', 'Mitnehmen')]


# Titel in dem Gold der Leiste oben links (Robert 13.10.2026): derselbe Verlauf wie «Markenbuch» in der Leiste. Das Zeichen liegt in einer
# gespiegelten Gruppe, deshalb läuft sein Verlauf von unten nach oben. Ohne Filter, weil sich Zeichen und Schriftzug bewegen.
_STOPS = '<stop offset="0" stop-color="#fbf0cf"/><stop offset=".34" stop-color="#ead39c"/><stop offset=".52" stop-color="#c9a764"/><stop offset=".62" stop-color="#9c7b43"/><stop offset=".8" stop-color="#dcc189"/><stop offset="1" stop-color="#f3e3b6"/>'
TGOLD = f'<linearGradient id="tgold" x1="0" y1="0" x2="0" y2="1">{_STOPS}</linearGradient><linearGradient id="tgold-z" x1="0" y1="1" x2="0" y2="0">{_STOPS}</linearGradient>'


def zeichen(kl='', titel=''):
    lab = f' role="img" aria-label="{e(titel)}"' if titel else ' aria-hidden="true"'
    return f'<svg class="{kl}" viewBox="{H.ZEICHEN[0]}" fill="currentColor"{lab}><use href="#br"/></svg>'


def wort(kl=''):
    return f'<svg class="{kl}" viewBox="{H.WORT[0]}" fill="currentColor" role="img" aria-label="Grand Beau-Rivage"><use href="#wort"/></svg>'


def kn(text, href, kl='', neu=False, laden=False):
    zus = (' target="_blank" rel="noopener"' if neu else '') + (' download' if laden else '')
    return f'<a class="kn {kl}" href="{href}"{zus}>{text}<i>{PU if laden else PF}</i></a>'


def zeilen(liste):
    return ''.join(f'<span class="z"><span>{"<em>" + x + "</em>" if i == len(liste) - 1 and len(liste) > 1 else x}</span></span>' for i, x in enumerate(liste))


def kopf(kap, titel, lead):
    return f'''<header class="mk" data-r="kopf">
      <div><p class="mk__kap"><b>{e(kap)}</b><i></i></p>
      <h2 class="mk__t">{zeilen(titel)}</h2></div>
      <p class="mk__lead">{lead}</p>
    </header>'''


def kachel(key, name, label, text, i, lage='50% 50%'):
    """Kachel wie die Zimmer der Startseite: Foto rund mit tiefem Schatten, federt herein, neigt sich zur Maus; Name, Goldlinie mit Raute, Versalzeile."""
    return f'''<article class="k3 k3--karte" data-r="feder" style="--i:{i}">
        <div class="k3__b"><img src="{foto(key, 'm')}" alt="{e(name)}" loading="lazy" decoding="async" style="object-position:{lage}"></div>
        <div class="k3__n"><small>{e(label)}</small><b>{e(name)}</b><p>{text}</p></div>
      </article>'''


def chip(k):
    n, h = F[k]
    return f'<span class="mini"><i style="background:{h}"></i>{e(n)}</span>'


def baue():
    os.makedirs(BUCH, exist_ok=True)
    shutil.copy(os.path.join(ROOT, 'assets', 'logo', 'emblem.svg'), os.path.join(BUCH, 'zeichen.svg'))
    open(os.path.join(BUCH, 'farben.css'), 'w', encoding='utf-8').write(
        '/* Grand Beau-Rivage Interlaken · Farben der neuen Website · Markenbuch, Oktober 2026 */\n:root{\n'
        + ''.join(f'  --{k}:{h};   /* {n} */\n' for k, (n, h) in F.items())
        + ''.join(f'  --{k}:{v};   /* {n}: {r} */\n' for k, n, v, r, _ in GLANZ) + '}\n')
    alle = [(k, n, h, r) for _, _, _, l in GRUPPEN for k, n, h, r in l]

    # ---------- Fächer: alle zwölf Töne öffnen sich wie ein Farbfächer
    n_f = len(alle)
    faecher = ''.join(f'''<button class="fa" type="button" data-hex="{h}" style="--c:{h};--t:{'#1a1d28' if lum(h) > .35 else '#fdf9f1'};--j:{j};--w:{(j - (n_f - 1) / 2) * 7.4:.1f}deg" aria-label="{e(n)} {h.upper()} kopieren">
          <span class="fa__n"><b>{e(n)}</b><small>{h.upper()}</small></span><span class="fa__ok">kopiert</span>
        </button>''' for j, (k, n, h, r) in enumerate(alle))

    # ---------- Farbkarten je Gruppe
    gruppen_html = ''
    for gk, gname, gsatz, liste in GRUPPEN:
        karten = ''.join(f'''<button class="fk" type="button" data-r="feder" data-hex="{h}" style="--i:{i};--c:{h};--t:{'#1a1d28' if lum(h) > .35 else '#fdf9f1'}" aria-label="{e(n)} {h.upper()} kopieren">
            <span class="fk__f"><span class="fk__hex">{h.upper()}</span><span class="fk__ok">kopiert</span></span>
            <span class="fk__n">{e(n)}</span>
            <span class="fk__r">{e(r)}</span>
            <span class="fk__w"><span>HEX</span>{h.upper()}<span>RGB</span>{' · '.join(map(str, rgb(h)))}</span>
          </button>''' for i, (k, n, h, r) in enumerate(liste))
        gruppen_html += f'''<div class="gr gr--{gk}" data-g>
        <div class="gr__k" data-r style="--i:0"><p class="mk__kap"><b>{e(gname)}</b><i></i></p><p class="gr__s">{e(gsatz)}</p></div>
        <div class="gr__l gr__l--{len(liste)}">{karten}</div>
      </div>'''

    # Glanzgold: zwei Verläufe statt eines Tons (14.10.2026), dieselbe Karte, ein Klick kopiert den Verlauf
    glanz = ''.join(f'''<button class="fk fk--glanz" type="button" data-r="feder" data-hex="{v}" style="--i:{i};--c:{v};--t:{t}" aria-label="{e(n)} kopieren">
            <span class="fk__f"><span class="fk__hex">Verlauf</span><span class="fk__ok">kopiert</span></span>
            <span class="fk__n">{e(n)}</span>
            <span class="fk__r">{e(r)}</span>
            <span class="fk__w"><span>VON</span>{glanz_stopps(v)[0].upper()}<span>MITTE</span>{min(glanz_stopps(v), key=lum).upper()}<span>BIS</span>{glanz_stopps(v)[-1].upper()}</span>
          </button>''' for i, (k, n, v, r, t) in enumerate(GLANZ))
    gruppen_html += f'''<div class="gr gr--glanz" data-g>
        <div class="gr__k" data-r style="--i:0"><p class="mk__kap"><b>Glanzgold</b><i></i></p><p class="gr__s">{e(GLANZ_SATZ)}</p></div>
        <div class="gr__l gr__l--2">{glanz}</div>
      </div>'''

    anteile = [('Helle Flächen', 60, '#f7f0e3', '#1a1d28'), ('Marine', 28, '#1b2033', '#e6d2a2'), ('Gold', 9, '#b0934f', '#fdf9f1'), ('Tinte', 3, '#1a1d28', '#fdf9f1')]
    anteil_html = ''.join(f'<span style="--p:{p};--j:{j};background:{c};color:{t}"><b><span data-zahl="{p}">0</span> %</b><small>{e(n)}</small></span>' for j, (n, p, c, t) in enumerate(anteile))

    paare = [('Tinte auf Papierton', 'tinte', 'papier', 'Lesetext'), ('Gold auf Marine', 'gold', 'marine', 'Titel und Zeichen auf Dunkel'),
             ('Weiss auf Blau', 'weiss', 'blau', 'Schrift im Knopf'), ('Taupe tief auf Papierton', 'taupe-tief', 'papier', 'kleine Goldschrift'),
             ('Akzent auf Papierton', 'akzent', 'papier', 'zweite Titelzeile'), ('Gold auf Papierton', 'gold', 'papier', 'nie als Schrift')]

    def urteil(r):
        if r >= 7: return 'Sehr gut, auch für langen Text'
        if r >= 4.5: return 'Gut für Lesetext'
        if r >= 3: return 'Nur für grosse Zeilen'
        return 'Nur Schmuck, nie Schrift'
    kontrast_html = ''
    for i, (t, a, b, w) in enumerate(paare):
        r = kontrast(F[a][1], F[b][1])
        kontrast_html += f'''<li class="ko" data-r="feder" style="--i:{i % 3};--g:{F[b][1]};--s:{F[a][1]}">
          <span class="ko__p"><span>Aa</span><small>Das Haus am Fluss</small></span>
          <span class="ko__n"><b>{e(t)}</b><small>{e(w)}</small></span>
          <span class="ko__z"><b><span data-zahl="{r:.1f}" data-komma>0</span></b><small>zu 1</small></span>
          <em class="ko__u">{urteil(r)}</em>
        </li>'''

    # ---------- Herkunft: Fotos als Kacheln, darunter der gemessene Streifen, der sich nach dem Landen füllt
    herkunft_html = ''
    for i, (key, t, x, toene, lage) in enumerate(HERKUNFT):
        st = streifen(key)
        st_html = ''.join(f'<i style="flex:{max(a, .06):.3f};background:{h};--j:{j}"></i>' for j, (a, h) in enumerate(st))
        werte = ' · '.join(h.upper() for _, h in st)
        wird = (f'<p class="her__wird"><span>Daraus</span>{"".join(chip(k) for k in toene)}</p>' if toene
                else '<p class="her__wird her__wird--nein"><span>Bleibt im Bild</span></p>')
        herkunft_html += f'''<article class="her k3" data-r="feder" style="--i:{i % 3}">
        <div class="k3__b her__b"><img src="{foto(key, 'm')}" alt="{e(t)}" loading="lazy" decoding="async" style="object-position:{lage}"><span class="kerbe kerbe--d">{e(t)}</span></div>
        <div class="her__st" aria-label="Gemessene Töne: {werte}">{st_html}</div>
        <p class="her__m">aus dem Foto gemessen · {werte}</p>
        <p class="her__x">{e(x)}</p>
        {wird}
      </article>'''

    # ---------- Schrift
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyzäöü<br>0123456789 · CHF 18.– · 1874'
    schriften = [
        ('a', 'Grosse Zeilen', 'Cormorant Garamond', 'Medium 500, nie fett', 'Titel, Namen, Preise auf Karten', 'Aa', 'Das Haus am Fluss', ALPHA),
        ('c', 'Kapitelzeilen', 'Cinzel', 'Regular 400, Versalien, gesperrt', 'die Schrift Ihrer Wortmarke: Kapitel, Ortszeilen, Schilder', 'AA', 'Interlaken · seit 1874', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>0123456789 · ÄÖÜ'),
        ('s', 'Lesetext', 'Instrument Sans', 'Regular 400 bis Semibold 600', 'alles, was gelesen wird', 'Aa', 'Zimmer mit Blick auf die Aare', ALPHA),
        ('m', 'Kleine Angaben', 'DM Mono', 'Regular 400', 'Zeiten, Preise, Adressen, Knöpfe', 'Aa', 'Höheweg 211 · 3800 Interlaken', ALPHA),
    ]

    def rollen(text):   # Buchstaben-Rollen beim Überfahren (Baustein «rollen»)
        return ''.join(f'<span class="ro" style="--k:{i}" data-c="{e(c)}">{e(c)}</span>' if c != ' ' else ' ' for i, c in enumerate(text))
    schrift_html = ''.join(f'''<article class="sch" data-g>
        <div class="sch__k" data-r style="--i:0"><p class="mk__kap"><b>{e(r)}</b><i></i></p><h3 class="sch__n f-{c}">{e(n)}</h3><dl><dt>Schnitt</dt><dd>{e(s)}</dd><dt>Wofür</dt><dd>{e(w)}</dd></dl></div>
        <div class="sch__aa f-{c}" data-r="maske" aria-hidden="true"><span class="z"><span>{aa}</span></span></div>
        <div class="sch__r" data-r style="--i:2"><p class="sch__satz f-{c}" aria-label="{e(probe)}">{rollen(probe)}</p><p class="sch__abc f-{c}">{abc}</p></div>
      </article>''' for c, r, n, s, w, aa, probe, abc in schriften)
    rang = [('Titel gross', 'Cormorant 500 · 98 px', 'r1', 'Das Haus am Fluss'), ('Titel', 'Cormorant 500 · 66 px', 'r2', 'Zimmer und Suiten'),
            ('Zwischentitel', 'Cormorant 500 · 36 px', 'r3', 'Junior Suite mit Flussblick'), ('Kleiner Titel', 'Cormorant 500 · 22 px', 'r4', 'Frühstück auf der Terrasse'),
            ('Kapitelzeile', 'Cinzel · 12 px · gesperrt', 'r5', 'La Vallée Spa'), ('Lesetext', 'Instrument Sans · 18 px · Zeilenabstand 1,66', 'r6', 'Das Haus steht seit 1874 direkt an der Aare, zwischen Thunersee und Brienzersee, mit der Jungfrau im Rücken.'),
            ('Kleine Angabe', 'DM Mono · 12,5 px · gesperrt', 'r7', 'Check-in · Höheweg 211 · 3800 Interlaken')]
    rang_html = ''.join(f'<li data-r="maske"><span class="rang__m"><b>{e(a)}</b>{e(b)}</span><span class="{c}"><span class="z"><span>{e(s)}</span></span></span></li>' for a, b, c, s in rang)

    # ---------- Bilder (jedes Foto nur einmal auf der Seite)
    bilder = [('halle', 'Die Halle', 'b1', '50% 50%'), ('terrasse-aare', 'Terrasse an der Aare', 'b2', '50% 50%'), ('balkon-aare', 'Balkon über der Aare', 'b3', '50% 60%'),
              ('hist-stich', 'Lithografie, Archiv', 'b4', '50% 50%'), ('saal', 'Ballsaal', 'b5', '50% 50%'), ('haus-winter', 'Das Haus im Winter', 'b6', '50% 50%'),
              ('rest-ambiance', 'Restaurant «L’Ambiance»', 'b7', '50% 50%')]
    bilder_html = ''.join(f'<figure class="bi {c} k3" data-r="feder" style="--i:{i % 3}"><div class="k3__b"><img src="{foto(k, "m")}" alt="{e(t)}" loading="lazy" decoding="async" style="object-position:{l}"><figcaption class="kerbe">{e(t)}</figcaption></div></figure>' for i, (k, t, c, l) in enumerate(bilder))

    # ---------- Anwendung: Drucksachen als freie Papierobjekte, fliegen aus ihrer Richtung herein und landen leicht gedreht
    anw = [('../drucksachen/img/briefbogen.webp', 'Briefbogen', -2.2, '-16vw', '34vh', '-11deg'), ('../drucksachen/img/ansichtskarte-1.webp', 'Ansichtskarte', 1.6, '0', '44vh', '7deg'),
           ('../drucksachen/img/nachttisch.webp', 'Nachttischkarte', -1.2, '16vw', '34vh', '12deg'), ('../drucksachen/img/m-menue1937-1.webp', 'Menükarte 1937, Nachdruck', 1.8, '-14vw', '40vh', '-8deg'),
           ('../drucksachen/img/gutschein.webp', 'Gutschein', -1.4, '0', '50vh', '6deg'), ('../kofferetiketten/img/e01.webp', 'Kofferaufkleber', 2.6, '14vw', '40vh', '14deg')]
    anw = [x for x in anw if os.path.exists(os.path.join(ZIEL, x[0]))]
    import markenbuch_schatten as SCH   # Schatten der Papiere als fertiges Bild (13.10.2026), Regeln je Papier in marke.css
    for x in anw:
        SCH.fuer(os.path.join(ZIEL, x[0]))
    anw_html = ''.join(f'''<figure class="pa pa--{SCH.name(p)}" data-r="flug" style="--i:{i % 3};--rot:{r}deg;--fx:{fx};--fy:{fy};--fw:{fw}">
        <div class="pa__o"><img src="{p}" alt="{e(t)}" loading="lazy" decoding="async"></div><figcaption>{e(t)}</figcaption>
      </figure>''' for i, (p, t, r, fx, fy, fw) in enumerate(anw))

    nein = [('zerr', 'Nicht verzerren'), ('dreh', 'Nicht drehen'), ('farbe', 'Nicht umfärben'), ('schatten', 'Keine Schatten')]
    nein_html = ''.join(f'<figure class="nein nein--{c}"><div>{zeichen()}<i></i></div><figcaption>{e(t)}</figcaption></figure>' for c, t in nein)

    index_html = ''.join(f'<a href="#{k}" data-r style="--i:{i}"><span>{e(n)}</span></a>' for i, (k, n) in enumerate(KAPITEL))
    nav_html = ''.join(f'<a href="#{k}">{e(n)}</a>' for k, n in KAPITEL[:9])
    v_css = int(os.path.getmtime(os.path.join(BUCH, 'marke.css')))
    v_js = int(os.path.getmtime(os.path.join(BUCH, 'marke.js'))) if os.path.exists(os.path.join(BUCH, 'marke.js')) else 1

    seite = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Markenbuch · Grand Beau-Rivage Interlaken</title>
<meta name="description" content="Zeichen, Farben und ihre Herkunft, Schriften, Tapete, Bilder und Bausteine der neuen Website des Grand Beau-Rivage Interlaken. Entwurf von Tasty Studios, Oktober 2026.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1b2033">
<link rel="icon" href="../assets/logo/favicon.svg" type="image/svg+xml">
<link rel="preload" href="../assets/fonts/cormorant-garamond-500-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/Cinzel-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/img/tapete-dunkel.webp" as="image">
<link rel="stylesheet" href="marke.css?v={v_css}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="br">{H.ZEICHEN[1]}</g><g id="wort">{H.WORT[1]}</g>{TGOLD}</defs></svg>

<nav class="leiste" aria-label="Markenbuch">
  <a class="leiste__m" href="#oben">{zeichen()}<span><b>Markenbuch</b><small>Le Livre · Grand Beau-Rivage</small></span></a>
  <div class="leiste__k">{nav_html}</div>
  <a class="glanz" href="../">Le Livre{PF}</a>
</nav>

<main>
<section class="titel tapete" id="oben">
  <div class="titel__in">
    <p class="titel__kap" data-r="hero" style="--i:0"><i></i><b>Markenbuch · Oktober 2026</b><i></i></p>
    <div class="titel__z" data-r="zeichen">{zeichen('', 'Medaillon BR').replace('fill="currentColor"', 'fill="url(#tgold-z) #cdaa5c"')}</div>
    <h1 class="titel__w" data-r="maske"><span class="z"><span>{wort().replace('fill="currentColor"', 'fill="url(#tgold) #cdaa5c"')}</span></span></h1>
    <p class="titel__ort" data-r="hero" style="--i:2">Interlaken <span class="raute"></span> seit 1874</p>
    <p class="titel__lead" data-r="hero" style="--i:3">Alles, was Ihr Haus erkennbar macht, an einem Ort: Zeichen und Name, die Farben und woher sie kommen, die Schriften, die Tapete, die Bilder und die Bausteine der neuen Website. Damit jedes neue Stück, ob Karte, Seite oder Schild, aussieht wie aus einem Guss.</p>
    <div class="knr knr--mitte" data-r="hero" style="--i:4">{kn('Lesen', '#haltung')}{kn('Website ansehen', '../index.html', 'kn--linie', neu=True)}</div>
  </div>
  <nav class="index" aria-label="Inhalt" data-g>{index_html}</nav>
  <span class="titel__runter" aria-hidden="true"><i></i></span>
</section>

<section class="ab blatt papier" id="haltung">
  <div class="in">
    {kopf('Haltung', ['Ein Grandhotel', 'an der Aare.'], 'Das Haus steht seit 1874 zwischen Thunersee und Brienzersee, direkt an der Aare, mit der Jungfrau im Rücken. Diese Lage ist das Produkt. Die Gestaltung zeigt sie, bevor ein Wort gelesen wird.')}
    <div class="drei" data-g>
      {kachel('salon', 'Viel Raum, wenige grosse Bilder.', 'Ruhe', 'Die Ruhe eines Grandhotels, nicht die Betriebsamkeit einer Buchungsseite. In jedem Abschnitt ein klarer nächster Schritt.', 0)}
      {kachel('hk-uhren', 'Gold zeigt, was zählt.', 'Gold', 'Gold steht nie im Lesetext. Es zeichnet das Medaillon, die Linien, die Zahlen und den Weg zur Buchung. Im Kopf der Startseite und in den Goldbändern glänzt es wie das Logo des Hauses.', 1)}
      {kachel('hist-plakat', 'Was echt ist, bleibt echt.', 'Herkunft', 'Fotos aus dem Haus, Stücke aus dem Archiv, der Wortlaut Ihrer Karten. Nichts aus einer Bilddatenbank, nichts dazuerfunden.', 2)}
    </div>
  </div>
</section>

<section class="fenster" aria-label="Das Haus am Fluss">
  <div class="fenster__f">
    <div class="fenster__b"><img src="{foto('haus-fluss-berge', 'l')}" alt="Das Grand Beau-Rivage an der Aare, dahinter die Berge" decoding="async"></div>
    <div class="fenster__t"><p class="fenster__s"><span class="z"><span>Zwischen zwei Seen,</span></span><span class="z"><span><em>an der Aare.</em></span></span></p><p class="fenster__u">Das Grand Beau-Rivage seit 1874, mit der Jungfrau im Rücken.</p></div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="zeichen">
  <div class="in">
    {kopf('Zeichen und Name', ['Das Medaillon', 'und Ihr Name.'], 'Das Medaillon mit dem BR ist aus Ihrem Logo nachgezeichnet und als Vektor angelegt, es bleibt in jeder Grösse scharf. Der Name steht in Cinzel, der Schrift Ihrer Wortmarke.')}
    <div class="lockups" data-g>
      <figure class="lock lock--marine tapete" data-r="flug" style="--i:0;--fx:-14vw;--fy:22vh;--fw:-6deg"><div>{zeichen('lock__z')}{wort('lock__w')}<p class="lock__o">Interlaken</p></div><figcaption class="kerbe kerbe--c">Hauptform auf Marine</figcaption></figure>
      <figure class="lock lock--papier" data-r="flug" style="--i:1;--fx:14vw;--fy:22vh;--fw:6deg"><div>{zeichen('lock__z')}{wort('lock__w')}<p class="lock__o">Interlaken</p></div><figcaption class="kerbe kerbe--c">Hauptform auf Papierton</figcaption></figure>
      <figure class="lock lock--quer" data-r="flug" style="--i:2;--fx:-12vw;--fy:30vh;--fw:5deg"><div>{zeichen('lock__z')}<span class="lock__strich"></span>{wort('lock__w')}</div><figcaption class="kerbe kerbe--c">Querform für Leisten und Briefköpfe</figcaption></figure>
      <figure class="lock lock--groessen tapete" data-r="flug" style="--i:3;--fx:12vw;--fy:30vh;--fw:-5deg"><div>{zeichen('g1')}{zeichen('g2')}{zeichen('g3')}{zeichen('g4')}</div><figcaption class="kerbe kerbe--c">Das Zeichen allein: Siegel, Stempel, Reiter im Browser</figcaption></figure>
    </div>
    <div class="regeln" data-g>
      <div class="regel" data-r="feder" style="--i:0">
        <div class="regel__f"><svg class="schutz" viewBox="-430 -480 2324 2362" aria-hidden="true">
          <rect class="schutz__r" x="-366" y="-363" width="2196" height="2178" rx="40" fill="none" stroke="currentColor" stroke-width="9" stroke-dasharray="36 28"/>
          <g fill="currentColor"><use href="#br"/></g>
          <path d="M0 -430 V-390 M0 -410 H-366 M-366 -430 V-390" stroke="currentColor" stroke-width="8" fill="none"/>
          <text x="-183" y="-440" text-anchor="middle" font-size="110" fill="currentColor" font-family="DM Mono, monospace">x</text>
        </svg></div>
        <h3>Schutzraum</h3><p>Rund um das Zeichen bleibt ein Viertel seiner Höhe frei. Kein Text, kein Bildrand, keine Linie ragt hinein.</p>
      </div>
      <div class="regel" data-r="feder" style="--i:1">
        <div class="regel__f klein"><span>{zeichen()}<small>16 px</small></span><span>{zeichen()}<small>24 px</small></span><span>{zeichen()}<small>8 mm</small></span></div>
        <h3>Kleinste Grösse</h3><p>Das Medaillon allein am Bildschirm nicht unter 16 Pixel, im Druck nicht unter 8 Millimeter. Mit dem Namen daneben mindestens 140 Pixel oder 40 Millimeter breit.</p>
      </div>
      <div class="regel regel--breit" data-r="feder" style="--i:2">
        <div class="regel__f neine">{nein_html}</div>
        <h3>Was das Zeichen nicht darf</h3><p>Es steht gerade, in Gold, Taupe, Tinte oder Weiss, ohne Schatten und ohne Rahmen. Auf Fotos nur dort, wo die Fläche ruhig ist.</p>
      </div>
    </div>
  </div>
</section>

<section class="ab blatt papier" id="farben">
  <div class="in">
    {kopf('Farben', ['Elf Töne, ein Rot', 'und Glanzgold.'], 'Hell ist der Normalzustand: Papierton und Creme tragen den Lesetext. Marine ist die eine dunkle Fläche, immer mit der Tapete. Gold zeichnet und schreibt nie den Lesetext. Im Kopf der Startseite und in den Goldbändern glänzt es als Verlauf, wie das Gold im Logo des Hauses. Das Rot gehört allein der Bar. Ein Klick auf eine Farbe kopiert ihren Wert.')}
    <div class="faecher" data-r="faecher"><div class="faecher__in">{faecher}</div><p class="faecher__h">Über den Fächer fahren, ein Klick kopiert den Farbwert.</p></div>
    <div class="anteil" data-r="anteil"><p class="mk__kap"><b>Mengenverhältnis</b><i></i><span>Richtwert für eine Seite oder ein Stück Papier</span></p><div class="anteil__b">{anteil_html}</div></div>
    {gruppen_html}
    <div class="kontrast">
      <div class="kontrast__k" data-r><p class="mk__kap"><b>Lesbarkeit</b><i></i></p><h3>Welche Farbe auf welcher stehen darf.</h3><p>Gerechnet nach dem internationalen Standard für Lesbarkeit im Netz (WCAG 2.1). Ab 4,5 zu 1 ist Lesetext gut lesbar, ab 3 zu 1 grosse Zeilen.</p></div>
      <ul class="kontrast__l" data-g>{kontrast_html}</ul>
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="herkunft">
  <div class="in">
    {kopf('Herkunft', ['Woher die Farben', 'kommen.'], 'Die Farben kommen nicht aus einem Fächer, sondern aus Ihrem Haus. Unter jedem Foto steht der Streifen, der beim Bau dieser Seite aus dem Bild selbst gemessen wurde, darunter die Töne, die daraus geworden sind.')}
    <div class="hers" data-g>{herkunft_html}</div>
  </div>
</section>

<section class="ab blatt papier" id="schrift">
  <div class="in">
    {kopf('Schrift', ['Vier Schriften,', 'jede mit ihrer Rolle.'], 'Cinzel kommt aus Ihrer Wortmarke. Cormorant Garamond gibt den Titeln die Ruhe einer klassischen Antiqua, Instrument Sans hält lange Texte lesbar, DM Mono steht bei Zeiten, Preisen und Adressen. Alle vier sind frei lizenziert und liegen als Dateien bei der Website, nichts wird von fremden Servern geladen.')}
    <div class="schs">{schrift_html}</div>
    <div class="rang">
      <div class="rang__k" data-r><p class="mk__kap"><b>Rangordnung</b><i></i></p><h3>Sieben Stufen, mehr braucht die Seite nicht.</h3><p>Grössen der neuen Website auf einem Rechner mit 1440 Pixel Breite. Auf dem Handy werden die Titel kleiner, der Lesetext bleibt.</p></div>
      <ul class="rang__l">{rang_html}</ul>
    </div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="tapete">
  <div class="in">
    {kopf('Tapete', ['Ihr Medaillon', 'als Tapete.'], 'Das Muster ist das Medaillon aus dem Ornament Ihres Zeichens, glatt und zart, Ton in Ton. Es liegt auf der Website, in den Karten und auf den Drucksachen, immer im Wechsel: ein Abschnitt mit Tapete, der nächste ohne.')}
    <div class="tap" data-g>
      <figure class="tap__f tap__f--dunkel" data-r="feder" style="--i:0"><span class="streif"></span><figcaption class="kerbe kerbe--c">Auf Marine</figcaption></figure>
      <figure class="tap__f tap__f--hell" data-r="feder" style="--i:1"><span class="streif"></span><figcaption class="kerbe kerbe--c">Auf Papierton und Creme</figcaption></figure>
    </div>
    <div class="prunk" data-r="prunk">
      <div class="prunk__z" style="--i:0"><b><span data-zahl="340">0</span></b><i></i><small>Pixel Rapport am Bildschirm</small></div>
      <div class="prunk__z" style="--i:1"><b><span data-zahl="36">0</span></b><i></i><small>Millimeter Rapport im Druck</small></div>
      <div class="prunk__z" style="--i:2"><b><span>1 : 1</span></b><i></i><small>im Wechsel mit glatten Flächen</small></div>
    </div>
  </div>
</section>

<section class="ab blatt papier" id="bilder">
  <div class="in">
    {kopf('Bilder', ['Ihr Haus,', 'in echtem Licht.'], 'Gezeigt wird, was der Gast vorfindet: die Halle, die Aare, der Saal, das Haus im Winter. Das Archiv bleibt eine eigene Bildwelt. Stiche und Schwarzweissfotos werden nicht eingefärbt.')}
    <div class="collage" data-g>{bilder_html}</div>
    <div class="satz3" data-g>
      <div data-r style="--i:0"><h3>Fotos aus dem Haus.</h3><p>Jedes Bild zeigt einen echten Raum des Grand Beau-Rivage. Überarbeitet werden nur Schärfe und Licht, nie der Inhalt.</p></div>
      <div data-r style="--i:1"><h3>Das Archiv bleibt Archiv.</h3><p>Lithografie, Plakat und Menükarte von 1937 stehen so, wie sie überliefert sind, mit Papierton und Gebrauchsspuren.</p></div>
      <div data-r style="--i:2"><h3>Der Name in der Einkerbung.</h3><p>Unten links, in Cormorant, in einer ausgeschnittenen Bildecke mit runden Kanten. So steht jeder Name an derselben Stelle.</p></div>
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="bausteine">
  <div class="in">
    {kopf('Bausteine', ['Knöpfe, Linien', 'und Einkerbungen.'], 'Die kleinen Teile, die überall wiederkehren. Jeder Knopf hat Tiefe und einen runden Knauf mit Pfeil und gibt nach, wenn man ihn drückt. Probieren Sie es gern aus.')}
    <div class="baus" data-g>
      <div class="bau" data-r="feder" style="--i:0"><div class="bau__f knr knr--mitte">{kn('Zimmer buchen', '#bausteine')}{kn('Mehr erfahren', '#bausteine', 'kn--linie')}</div><h3>Knöpfe</h3><p>Creme auf Marine, Blau auf Papierton. Schrift in DM Mono, gesperrt, in Versalien.</p></div>
      <div class="bau" data-r="feder" style="--i:1"><div class="bau__f"><span class="strich">{zeichen()}</span></div><h3>Der Strich</h3><p>Eine feine Goldlinie über die ganze Breite, in der Mitte das Medaillon. Sie steht genau auf der Naht zwischen zwei Abschnitten.</p></div>
      <div class="bau" data-r="feder" style="--i:0"><div class="bau__f"><figure class="kerbbild"><img src="{foto('terrasse-abend', 's')}" alt="" loading="lazy" decoding="async"><figcaption class="kerbe kerbe--d">Terrasse «La Belle Rivière»</figcaption></figure></div><h3>Die Einkerbung</h3><p>Der Name eines Bildes in einer ausgeschnittenen Ecke mit runden Kanten, immer unten links.</p></div>
      <div class="bau" data-r="feder" style="--i:1"><div class="bau__f bau__f--titel" data-r="maske"><p class="mk__kap"><b>Interlaken · seit 1874</b><i></i></p><p class="bau__t"><span class="z"><span>Das Haus</span></span><span class="z"><span><em>am Fluss.</em></span></span></p></div><h3>Kapitelzeile und Titel</h3><p>Über jedem Titel eine Zeile in Cinzel mit wachsender Linie. Der Titel steigt Zeile für Zeile aus dem Schlitz, der zweite Teil in Gold.</p></div>
    </div>
  </div>
</section>

<section class="ab blatt creme" id="anwendung">
  <div class="in">
    {kopf('Anwendung', ['Am Bildschirm', 'und auf Papier.'], 'Dieselben Farben, Schriften und Zeichen auf der Website, auf den Karten, den Drucksachen und den Kofferaufklebern. Alles davon liegt fertig in der Werkbank.')}
    <figure class="schirm" data-r="feder"><div class="schirm__k"><i></i><i></i><i></i><span>grandbeaurivage.ch</span></div><div class="schirm__b"><img src="../werkbank/img/auftakt.webp" alt="Startseite der neuen Website" loading="lazy" decoding="async"></div></figure>
    <div class="papiere" data-g>{anw_html}</div>
    <div class="knr knr--mitte" data-r>{kn('Drucksachen ansehen', '../drucksachen/index.html', neu=True)}{kn('Kofferaufkleber', '../kofferetiketten/index.html', 'kn--linie', neu=True)}</div>
  </div>
</section>

<section class="ab blatt marine tapete schluss" id="mitnehmen">
  <div class="in">
    {kopf('Zum Mitnehmen', ['Alles für das', 'nächste Stück.'], 'Das Zeichen als Vektor, die Farben als fertige Datei für die Website und die vier Schriften. Wer eine neue Karte, ein Schild oder eine Seite gestaltet, findet hier alles dafür.')}
    <ul class="laden" data-g>
      <li data-r style="--i:0"><span><b>Medaillon</b><small>Vektor, SVG, in jeder Grösse scharf</small></span>{kn('Laden', 'zeichen.svg', laden=True)}</li>
      <li data-r style="--i:1"><span><b>Farben</b><small>alle zwölf Töne als CSS-Datei</small></span>{kn('Laden', 'farben.css', laden=True)}</li>
      <li data-r style="--i:2"><span><b>Cormorant Garamond</b><small>Medium 500, WOFF2</small></span>{kn('Laden', '../assets/fonts/cormorant-garamond-500-latin.woff2', laden=True)}</li>
      <li data-r style="--i:3"><span><b>Cinzel</b><small>WOFF2</small></span>{kn('Laden', '../assets/fonts/Cinzel-latin.woff2', laden=True)}</li>
      <li data-r style="--i:4"><span><b>Instrument Sans</b><small>400 bis 600, WOFF2</small></span>{kn('Laden', '../assets/fonts/InstrumentSans-normal-400_600.woff2', laden=True)}</li>
      <li data-r style="--i:5"><span><b>DM Mono</b><small>Regular 400, WOFF2</small></span>{kn('Laden', '../assets/fonts/DMMono-normal-400.woff2', laden=True)}</li>
    </ul>
    <div class="ende" data-r="ende">
      <span class="strich strich--gross">{zeichen()}</span>
      <p class="ende__w">{wort()}</p>
      <p class="ende__s">Markenbuch Grand Beau-Rivage Interlaken · Entwurf von Tasty Studios, Oktober 2026.</p>
      <div class="knr knr--mitte">{kn('Zur Werkbank', '../werkbank/#handschrift')}{kn('Website ansehen', '../index.html', 'kn--linie', neu=True)}</div>
    </div>
  </div>
</section>
</main>
<script src="marke.js?v={v_js}" defer></script>
</body>
</html>
'''
    import re
    seite = re.sub(r'((?:href|src)=")\.\./(?!")', r'\1../../', seite)   # eine Ebene tiefer als vorher (marke/buch/)
    seite = seite.replace('href="../../">Le Livre', 'href="../">Le Livre')
    open(os.path.join(BUCH, 'index.html'), 'w', encoding='utf-8').write(seite)
    print('marke/buch/index.html', len(seite) // 1024, 'kB')
    __import__('subprocess').run([__import__('sys').executable, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'zur_werkbank.py')], check=False)   # «Zur Werkbank»: Knopf unten links wieder eintragen (12.10.2026)


if __name__ == '__main__':
    baue()
