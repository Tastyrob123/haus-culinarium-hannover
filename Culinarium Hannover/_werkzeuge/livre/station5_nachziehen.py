#!/usr/bin/env python3
"""Station 05 (Markenbauer) auf den Stand der Website nachziehen · Auftrag des Oberchefs an culinarium-livre, 28.10.2026.
Werkbank (papier.py, marke_werkbank.py, sb_strom.js), Tresen und Schaufenster lesen aus _kette/05-markenbauer/; dort stand noch der Platzhalter vom 26.10.
Geschrieben werden nur: marke.json, marke/markenbuch.html, marke/logo-richtig-falsch/index.html, marke/bilder/ (zwei Plakate als Beleg für das Band, herkunft.json) und, neu daneben,
marke/schriften/Fraunces-340-wie-website.woff2 (die Titelschrift der Website auf ihre Werte festgesetzt; nichts überschrieben). Vorher je Datei eine
Sicherung *.vor-website-stand-2026-10-28 (nie überschrieben). Die Umstellungen am Markenbuch sind dieselben wie in Le Livre (buch.website_stand).

   python3 _werkzeuge/livre/station5_nachziehen.py"""
import html, json, os, re, shutil, sys
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))
ST5 = os.path.join(PROJEKT, '_kette', '05-markenbauer')
M = os.path.join(ST5, 'marke')
WEB = os.path.join(PROJEKT, 'website')
IG = os.path.join(PROJEKT, '_quelle', 'extern', 'ig')
SICH = '.vor-website-stand-2026-10-28'
sys.path.insert(0, HIER)
import buch  # noqa: E402

e = html.escape
# Beleg für das Band (Oberchef 28.10.2026: Robert zeigte vier echte Plakate, Varianten «BY MOMO X CHRISTOPH», «BY MOMO», «BY MOMO X RUDI»)
BELEG = [('plakat-2023-10', '2023-10-12_culinarium_hannover_CyT32RTMB4d-1.jpg', 'Plakat 21.10.2023, «BY MOMO X CHRISTOPH»'),
         ('plakat-2024-04', '2024-04-18_culinarium_hannover_C56bJeds8PF-1.jpg', 'Plakat 26./27.04.2024, «BY MOMO»'),
         ('plakat-2025-02', None, 'Plakat 21./22.02.2025, «BY MOMO X RUDI»'),
         ('plakat-2026-09', None, 'Plakat 25./26.09.2026, «BY MOMO X RUDI»')]


def sichern(p):
    z = p + SICH
    if not os.path.exists(z):
        (shutil.copytree if os.path.isdir(p) else shutil.copy2)(p, z)


def bilder():
    h = json.load(open(os.path.join(M, 'bilder', 'herkunft.json'), encoding='utf-8'))
    for k, q, was in BELEG:
        if not q:
            continue
        im = Image.open(os.path.join(IG, q)).convert('RGB')
        o = im.size
        if im.width > 1440:
            im = im.resize((1440, round(im.height * 1440 / im.width)), Image.LANCZOS)
        im.save(os.path.join(M, 'bilder', k + '.jpg'), 'JPEG', quality=88)
        h[k] = {'quelle': '_quelle/extern/ig/' + q, 'was': was + ' · Beleg für das Band der Plakate (28.10.2026)', 'original': list(o), 'hier': list(im.size)}
    json.dump(h, open(os.path.join(M, 'bilder', 'herkunft.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def beleg_html():
    fig = ''.join(f'<figure style="margin:0"><img src="bilder/{k}.jpg" alt="{e(t)}" loading="lazy" decoding="async" style="display:block;width:100%;aspect-ratio:1;object-fit:cover;object-position:50% 100%;border-radius:8px">'
                  f'<figcaption class="mono" style="margin-top:8px;font-size:10px;letter-spacing:.12em">{e(t)}</figcaption></figure>' for k, _, t in BELEG)
    return ('<div class="plakatband" data-r style="margin-top:clamp(36px,4vw,56px)"><p class="mk__kap"><b><span class="kw">AUF DEN PLAKATEN</span></b><i></i></p>'
            '<p style="max-width:62ch;margin:10px 0 18px">Auf jedem Plakat seit Oktober 2023 steht die Wortmarke in einem doppelt gerahmten warmweissen Feld, darunter die Zeile: '
            '«A UNiQUE EXPERiENCE BY MOMO X RUDI», früher «BY MOMO X CHRISTOPH» und «BY MOMO». Das Band gehört zu den Plakaten. Auf der Website und auf Drucksachen '
            'steht die Wortmarke ohne Band.</p>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px">{fig}</div></div>')


def markenbuch():
    p = os.path.join(M, 'markenbuch.html')
    s = open(p + SICH, encoding='utf-8').read()          # immer aus der Sicherung (Stand 26.10.), damit der Lauf wiederholbar ist
    s = buch.website_stand(s, schrift='../../../website/assets/schrift/')
    s = s.replace('{stand}', '28.10.2026')
    # Leiste der Station: ohne Weg zur Probe, ohne «Station 05»
    s = re.sub(r'\s*<a class="glanz" href="probe\.html"[^>]*>.*?</a>', '', s, count=1, flags=re.S)
    s = s.replace('<small>Station 05 · Culinarium Hannover</small>', '<small>Culinarium Hannover</small>')
    s = s.replace('<a href="#welten"><span class="kw">WELTEN</span></a>', '<a href="#welten"><span class="kw">FARBWELT</span></a>')
    # Beleg der Plakate im Blatt «Zeichen», nach der Reihe der Zeichen
    s, n = re.subn(r'(<section class="[^"]*" id="zeichen">.*?<div class="reihe5" data-g>.*?</div>\s*</div>)', lambda m: m.group(1) + '\n    ' + beleg_html(), s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('Blatt Zeichen: Reihe nicht gefunden, erst klären')
    # Titelschrift wie die Website (wght 340, SOFT 100): feste Schrift für alle Stärken, nach marke.css eingetragen
    s = s.replace('</head>', "<style>@font-face{font-family:'Fraunces Soft';font-style:normal;font-weight:1 1000;font-display:swap;src:url('schriften/Fraunces-340-wie-website.woff2') format('woff2')}</style>\n"
                  + buch.STAND_MARKE + '\n</head>', 1)
    sichtbar = re.sub(r'<(style|script)[^>]*>.*?</\1>|<[^>]+>', ' ', s, flags=re.S)
    for w in ('Platzhalter', 'Station 0', 'Tasty', 'Welt B', 'PROBE', 'Projekt Nummer', 'Rivage', 'Carlton', 'Schäfli', 'Schlössli', 'nicht gewählt', 'Zug der Original-Pixel'):
        if w in sichtbar:
            raise SystemExit(f'Markenbuch Station 05: «{w}» steht noch drin, erst klären')
    if 'probe.html' in s:
        raise SystemExit('Markenbuch Station 05: Weg zur Probe steht noch drin')
    open(p, 'w', encoding='utf-8').write(s)
    # Logo richtig und falsch (eigene Seite, aus dem Markenbuch verlinkt): Rudis Original, ohne Platzhalter-Satz, ohne Band-Fassungen
    q = os.path.join(M, 'logo-richtig-falsch', 'index.html')
    r = open(q + SICH, encoding='utf-8').read()
    r = buch.ohne_band(buch.logo_tauschen(r, *buch.original()), buch=False)
    r = re.sub(r'Vorerst für den Platzhalter:.*?Eine Datei des Gestalters fehlt noch\.', 'Wortmarke, Zeile und C sind Dateien. Sie werden eingesetzt, nie nachgezeichnet, nie verändert.', r, flags=re.S)
    r = r.replace('Auf dunkler Fläche in Warmweiss, Form unverändert, aus dem Zug der Original-Pixel.', 'Auf dunkler Fläche in Warmweiss, Form unverändert.')
    if 'Platzhalter' in re.sub(r'<[^>]+>', ' ', r):
        raise SystemExit('Logo richtig und falsch: Platzhalter steht noch drin')
    open(q, 'w', encoding='utf-8').write(r)
    print('Markenbuch und Logo richtig und falsch der Station 05 auf dem Stand der Website')


def marke_json():
    p = os.path.join(ST5, 'marke.json')
    m = json.load(open(p, encoding='utf-8'))
    m['wortmarke'] = {
        'status': 'original',
        'quelle': 'Rudis Original-Logo, als Vektor-PDF geschickt am 28.10.2026 (_quelle/logo/original/culinarium-logo-original-rudi-2026-10-28.pdf), Farbe #383944',
        'datei': '_quelle/logo/original/culinarium-logo-original.svg', 'art': 'svg',
        'auf_der_website': 'website/assets/zeichen/marke.svg (Symbole wm, wmz, zeile; gebaut von website/bau.py zeichen() aus dem Original)',
        'zeile': 'A UNiQUE EXPERiENCE (linksbündig unter der Wortmarke)',
        'auf_den_plakaten': 'darunter «BY MOMO X RUDI» (2023 «BY MOMO X CHRISTOPH», 2024 «BY MOMO»), im doppelt gerahmten warmweissen Feld',
        'farben': 'Schiefer #3A3845 auf Warmweiss, Warmweiss #FAF4F4 auf Dunkel; nie neu gesetzt, nie mit Schatten',
        'vorher': 'bis 28.10.2026 Platzhalter, aus dem Plakat nachgezogen (_quelle/logo/nachgezogen/), nach Rudi nicht sein Logo'}
    m['zeichen_satz'] = ('Das C ist der erste Buchstabe der Wortmarke (formgleich mit Rudis Original, Zeichen der Werkzeuge im Ring); das x kommt aus «MOMO X RUDI» '
                         'der Plakate. Auf der Website trägt die Tapete das C.')
    for s_ in m['schriften']:
        if s_['rolle'] == 'titel':
            s_.update(schnitt='leicht: 340 für Titel, 300 für Rudis Zeilen in Versalien, Weichheit 100 (SOFT 100), optische Grösse 144; nie fett, nie kursiv',
                      datei='website/assets/schrift/fraunces-soft.woff2', wofuer='Titel, Rudis Zeilen, grosse Zahlen (wie website/assets/culinarium.css .gross, .rudi)')
        elif s_['rolle'] == 'etikett':
            s_.update(schnitt='600 und 700, Versalien, 0,12 em gesperrt', datei='website/assets/schrift/urbanist.woff2', wofuer='Etiketten, Kapitelzeilen, Knöpfe')
        elif s_['rolle'] == 'lauf':
            s_.update(schnitt='400, 17 px, Zeilenabstand 1,62', datei='website/assets/schrift/instrument.woff2', wofuer='Lesetext der Website')
        elif s_['rolle'] == 'mono':
            s_.update(datei='website/assets/schrift/dmmono.woff2')
    m['schriftwahl']['titel'][0].update(name='Fraunces Soft', satz='Eine Antiqua der 70er mit weichen, tropfenförmigen Enden wie in der Wortmarke; auf der Website leicht gesetzt (340), nie fett. Liegt in der Website.')
    m['band'] = {'was': 'Merkmal der Plakate: auf jedem Plakat seit Oktober 2023 die Wortmarke im doppelt gerahmten warmweissen Feld, darunter die Zeile',
                 'beleg': [f'marke/bilder/{k}.jpg' for k, _, _ in BELEG], 'nur': 'auf den Plakaten',
                 'nie': 'kein Baustein für Website und Drucksachen (Robert 26.10.2026 abgelehnt als Beschriftung; Oberchef 28.10.2026), kein gerahmtes Schild auf einem Foto, keine Plakette, keine Einkerbung'}
    m['darstellungsidee'] = ('Die Abendfarbe: die Betonung der ganzen Seite wechselt mit dem Plakat des nächsten Abends. Dunkle Flächen wie die Bar, Warmweiss wie das Plakat. '
                             'Keine Schrift auf dem Foto, kein Schild darüber.')
    m['knopf']['form'] = 'Platte mit Radius 10 px, Etikettschrift Urbanist 700 in Versalien, rechts runder Knauf in Kerze mit dem Pfeil als Linie (wie website/assets/culinarium.css .knopf)'
    nicht = m.setdefault('merkmale_nicht', [])
    satz = 'das warmweisse Band mit doppelter Linie als Beschriftung auf Website und Drucksachen (Robert 26.10.2026 abgelehnt; bleibt Merkmal der Plakate)'
    if satz not in nicht:
        nicht.append(satz)
    m['website_stand'] = {'datum': '2026-10-28', 'farben': 'website/assets/culinarium.css: Nacht #16151A, Strasse #1C1B21, Bar #222028, Tafel #26252E, Schiefer #3A3845, Warmweiss #FAF4F4, '
                          'Tinte #2A2833, Kerze #EF7649 (hell #F5A689, tief #B15736), Dirty Chicken #8953A9; = Farbwelt A, Abendfarbe Orange',
                          'lesetext': 'Instrument Sans (body), Urbanist für Etiketten', 'von': 'culinarium-livre auf Auftrag des Oberchefs'}
    m['stand'] = '28.10.2026; auf dem Stand der Website: Rudis Original-Logo, Fraunces leicht, Farben und Lesetext der Website, Band nur auf den Plakaten (vorher 26.10.2026, Platzhalter)'
    json.dump(m, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('marke.json auf dem Stand der Website')


if __name__ == '__main__':
    for p in (os.path.join(ST5, 'marke.json'), os.path.join(M, 'markenbuch.html'), os.path.join(M, 'bilder'), os.path.join(M, 'logo-richtig-falsch', 'index.html')):
        sichern(p)
    f = os.path.join(M, 'schriften', 'Fraunces-340-wie-website.woff2')
    tmp = os.path.join(HIER, '_qa', 'fraunces-tmp')
    if os.path.exists(f):
        os.remove(f)                                      # selbst angelegt (neu am 28.10.), kein Original der Station
    os.makedirs(os.path.join(tmp, 'schriften'), exist_ok=True)
    buch.fraunces_wie_website(WEB, tmp)
    shutil.move(os.path.join(tmp, 'schriften', 'Fraunces-340-wie-website.woff2'), f)
    shutil.rmtree(tmp, ignore_errors=True)
    bilder()
    markenbuch()
    marke_json()
