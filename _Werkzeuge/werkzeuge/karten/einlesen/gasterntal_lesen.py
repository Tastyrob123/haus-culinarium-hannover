"""Liest die Karte des Berghotels Gasterntal aus dem Original des Hauses und schreibt sie als Daten.

    python3 werkzeuge/karten/einlesen/gasterntal_lesen.py            → grundstand/gasterntal.json
    python3 werkzeuge/karten/einlesen/gasterntal_lesen.py --zeige    → nur ausgeben, nichts schreiben

Original: <Projekt>/assets/pdf/Karte-2026.pdf (Word-PDF des Hauses, 2 Seiten, 9.5.2026; dieselbe Datei wie
_quelle/website/pdf/Neue_Karte_Gasterntal_2026.pdf). Das Projekt wird nur gelesen.

Hier steht kein einziges Wort der Karte. Jeder Text kommt aus der Textschicht der PDF (pdftohtml -xml: Textstücke
mit Lage und Schrift). Die Regeln unten sagen nur, WELCHES Stück in WELCHES Feld gehört (nach Seite, Spalte, Zeile,
Schrift), nie, was darin steht. Verändert wird allein der Leerraum (mehrere Leerzeichen → eines, Rand weg).
Was die Textschicht nicht hergibt, steht in «offen». Ob das Ergebnis stimmt, prüft getrennt einlesen/abgleich.py
(anderes Auslesewerkzeug, Zeile für Zeile).
"""
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
PROJEKT = Path.home() / 'Desktop/Website-Projekte/Berghotel Gasterntal'
ORIGINAL = PROJEKT / 'assets/pdf/Karte-2026.pdf'
ZIEL = HIER.parent / 'grundstand' / 'gasterntal.json'

PREIS = re.compile(r'(?<![\d.,%-])\d{1,3}\.\d{2}\.?(?![\d%])')   # 5.50 · 12.00 · «5.50.» (so im Original), nicht 37.5-43%


def stuecke():
    """Alle Textstücke der PDF: Seite, oben, links, breit, hoch, Schrift (Familie, Grösse), Text."""
    xml = subprocess.run(['pdftohtml', '-xml', '-i', '-stdout', str(ORIGINAL)], capture_output=True, text=True, check=True).stdout
    schrift, aus, seite = {}, [], 0
    for zeile in xml.splitlines():
        m = re.search(r'<page number="(\d+)"', zeile)
        if m:
            seite = int(m.group(1))
        m = re.search(r'<fontspec id="(\d+)" size="(\d+)" family="[A-Z]+\+([^"]+)"', zeile)
        if m:
            schrift[m.group(1)] = (m.group(3), int(m.group(2)))
        m = re.match(r'<text top="(\d+)" left="(\d+)" width="(\d+)" height="(\d+)" font="(\d+)">(.*)</text>', zeile)
        if m:
            text = html.unescape(re.sub(r'<[^>]+>', '', m.group(6)))
            if text.strip():
                o, l, b, h = (int(m.group(i)) for i in (1, 2, 3, 4))
                fam, gr = schrift[m.group(5)]
                # Beginnt ein Stück mit einer Reihe Leerzeichen (Word rückt so ein), zählt die Stelle, an der die Schrift beginnt
                leer = len(text) - len(text.lstrip())
                tinte = l + round(b * leer / len(text)) if leer >= 3 else l
                aus.append(dict(seite=seite, oben=o, links=tinte, rechts=l + b, unten=o + h, fam=fam, gr=gr, text=text))
    return aus


def rein(t):
    return re.sub(r'\s+', ' ', t).strip()


def verbinde(teile):
    """Stücke einer Zeile von links nach rechts. Ein Leerzeichen kommt nur dazu, wo im Original eine Lücke ist."""
    aus = ''
    letzter = None
    for s in sorted(teile, key=lambda s: s['links']):
        if letzter is not None and s['links'] - letzter['rechts'] > 2 and not aus.endswith(' ') and not s['text'].startswith(' '):
            aus += ' '
        aus += s['text']
        letzter = s
    return rein(aus)


def zeilen(st):
    """Stücke zu Zeilen: gleiche Unterkante (± 4 Punkte), von oben nach unten."""
    aus = []
    for s in sorted(st, key=lambda s: (s['unten'], s['links'])):
        if aus and abs(aus[-1][0]['unten'] - s['unten']) <= 4:
            aus[-1].append(s)
        else:
            aus.append([s])
    return aus


def ist_schmuck(s):
    return s['fam'] == 'BeyondTheMountains'


def preis_teile(text):
    """«Cüpli 10.00» → [('Cüpli', '10.00')] · «5.00  6.00  12.00» → [('', '5.00'), ('', '6.00'), ('', '12.00')]"""
    aus, rest = [], text
    while True:
        m = PREIS.search(rest)
        if not m:
            break
        aus.append((rein(rest[:m.start()]), m.group(0)))
        rest = rest[m.end():]
    return aus, rein(rest)


def lies_spalte(st, seite, links_kante, preis_ab, angabe_ab, raster=None):
    """Eine Spalte der Karte → Liste von Einträgen. links_kante: wo Namen beginnen. preis_ab: ab hier stehen Preise.
    angabe_ab: ab hier stehen Angaben zum Preis («33cl», «Portion»), links davon Zusätze zum Namen («du Valais»).
    raster: x-Lagen der Preisspalten einer Tafel (für Zeilen, die nicht jede Spalte füllen)."""
    aus = []
    letztes = None        # das Gericht, zu dem Folgezeilen gehören
    tafel = 0             # Zahl der Spaltenköpfe der laufenden Rubrik
    for z in zeilen(st):
        z.sort(key=lambda s: s['links'])
        am_rand = [s for s in z if s['links'] <= links_kante + 2]
        erste = z[0]
        # Rubrik: Schmuckschrift am Rand
        if am_rand and ist_schmuck(am_rand[0]):
            titel = [s for s in z if ist_schmuck(s) or (s['gr'] >= 17 and s['links'] < preis_ab - 60)]
            uebrig = [s for s in z if s not in titel]
            u = dict(t='rubrik', titel=verbinde(titel), en='')
            koepfe = [k for s in uebrig if s['links'] >= preis_ab - 10 for k in re.split(r'\s{2,}', s['text'].strip()) if k]
            zusatz = verbinde([s for s in uebrig if s['links'] < preis_ab - 10])
            if koepfe:
                u['koepfe'] = koepfe
            if zusatz:
                u['zusatz'] = zusatz
            tafel = len(koepfe)
            u['s'] = seite
            aus.append(u)
            letztes = None
            continue
        # Englische Zeile (kursiv gesetzt, Grösse 13) am Rand: gehört zum Gericht davor
        if am_rand and am_rand[0]['gr'] == 13 and letztes is not None:
            links_teil = [s for s in z if s['gr'] == 13]
            letztes['zeilen'].append(dict(text=verbinde(links_teil), en=True))
            _angaben(letztes, [s for s in z if s not in links_teil])
            continue
        # Zeile ohne Text am Rand: nur Angaben und Preise, gehört zum Gericht davor («Chlini Portion 13.00»)
        if not am_rand:
            if letztes is None:
                raise SystemExit(f'Zeile ohne Gericht davor: Seite {seite}, {verbinde(z)!r}')
            _angaben(letztes, z)
            continue
        hat_preis = any(PREIS.search(s['text']) for s in z)
        gross = am_rand[0]['gr'] >= 17                       # Name eines Gerichts auf der Speisenseite
        klein = am_rand[0]['gr'] <= 12 and not hat_preis     # Zwischentitel der Getränkeseite («Weisse», «Rosé»)
        # Zwischentitel: kleines Wort am Rand ohne Preis, oder ein Wort der Grundschrift ganz ohne Preis in einer Tafel («Rote»)
        allein = len(z) == 1 and not hat_preis and not gross
        if klein or (allein and tafel and am_rand[0]['gr'] == 15):
            u = dict(t='zw', text=verbinde(am_rand))
            koepfe = [rein(s['text']) for s in z if s not in am_rand]
            if koepfe:
                u['koepfe'] = koepfe
                tafel = len(koepfe)
            u['s'] = seite
            aus.append(u)
            letztes = None
            continue
        # Erläuterung in Lesegrösse am Rand ohne Preis (Grösse 14 oder 10), kein Gericht davor: Notiz
        if am_rand[0]['gr'] in (14, 10) and not hat_preis and (letztes is None or am_rand[0]['gr'] == 10):
            aus.append(dict(t='notiz', text=verbinde(z), s=seite))
            continue
        # Folgezeile eines Gerichts: Beschreibung in Lesegrösse, oder Zeile in Grundschrift mit dem Preis des Gerichts darüber
        if letztes is not None and not gross and (am_rand[0]['gr'] in (14, 12) or (am_rand[0]['gr'] == 15 and not letztes['preise'] and seite == 2)):
            text_teil = [s for s in z if s['links'] < angabe_ab or s in am_rand]
            letztes['zeilen'].append(dict(text=verbinde(text_teil)))
            _angaben(letztes, [s for s in z if s not in text_teil])
            continue
        # Fortsetzung des Namens: grosse Zeile ohne Preis direkt nach einem Gericht mit Preis und noch ohne Zeilen
        if gross and not hat_preis and letztes is not None and letztes['preise'] and not letztes['zeilen'] and len(z) == 1 \
                and erste['text'][:1].islower():
            letztes['name'] = rein(letztes['name'] + ' ' + verbinde(z))
            continue
        # Gericht
        name_gr = am_rand[0]['gr']
        name_teil = [s for s in z if s['gr'] == name_gr and s['links'] < preis_ab - 40 and not PREIS.search(s['text'])]
        # dazu Stücke gleicher Zeile in der zweiten Namensschrift («es het wes het”», «Maeder’s Ämber»)
        name_teil += [s for s in z if s not in name_teil and s['gr'] in (15, 18) and name_gr in (15, 18) and s['links'] < preis_ab - 40
                      and not PREIS.search(s['text'])]
        rest = [s for s in z if s not in name_teil]
        zusatz_teil = [s for s in rest if s['links'] < angabe_ab and not PREIS.search(s['text'])]
        u = dict(t='gericht', name=verbinde(name_teil))
        if zusatz_teil:
            u['zusatz'] = verbinde(zusatz_teil)
        u['zeilen'], u['preise'] = [], []
        u['s'] = seite
        _angaben(u, [s for s in rest if s not in zusatz_teil], raster if tafel >= 3 else None, tafel)
        aus.append(u)
        letztes = u
    return aus


def _angaben(u, st, raster=None, tafel=0):
    """Angaben und Preise rechts in der Zeile, von links nach rechts: «33cl» + «5.50», «Cüpli 10.00» + «Flasche» + «54.00»."""
    offen = ''
    funde = []
    for s in sorted(st, key=lambda s: s['links']):
        paare, rest = preis_teile(s['text'])
        if not paare:
            offen = rein(offen + ' ' + s['text'])
            continue
        for i, (angabe, preis) in enumerate(paare):
            funde.append((rein((offen + ' ' + angabe) if i == 0 else angabe), preis, s['links']))
        offen = rest
    if offen:
        raise SystemExit(f'Angabe ohne Preis bei {u.get("name")!r}: {offen!r}')
    if not funde:
        return
    if raster and tafel >= 3 and len(funde) < tafel and not any(a for a, _, _ in funde):
        # Tafel mit drei Preisspalten, Zeile füllt nicht jede: jeder Preis kommt in die Spalte, über der er im Original steht
        zellen = [''] * tafel
        for _, preis, x in funde:
            zellen[min(range(tafel), key=lambda i: abs(raster[i] - x))] = preis
        u['preise'] = zellen
        return
    for angabe, preis, _ in funde:
        u['preise'].append(preis)
        u.setdefault('einheiten', [''] * (len(u['preise']) - 1)).append(angabe)
    if not any(u['einheiten']):
        del u['einheiten']


def lies():
    st = stuecke()

    def wo(seite, links_von, links_bis, oben_von=0, oben_bis=9999):
        return [s for s in st if s['seite'] == seite and links_von <= s['links'] < links_bis and oben_von <= s['oben'] < oben_bis]

    # Seite 1 links: Getränke. Die drei Preisspalten stehen bei x 290, 333, 375 (Köpfe «1dl 2dl 5dl» der offenen Weine).
    getraenke = lies_spalte(wo(1, 0, 450), 1, 42, 290, 270, raster=[290, 333, 375])
    # Seite 1 rechts: Umschlag (Titel in Schmuckschrift 42, Zeilen darunter), dann die Devise
    rechts1 = wo(1, 450, 9999)
    titel = [s for s in rechts1 if ist_schmuck(s) and s['gr'] >= 30]
    kopf_zeilen = [z for z in zeilen([s for s in rechts1 if s not in titel and s['oben'] < 850])]
    devise = [z for z in zeilen([s for s in rechts1 if s['oben'] >= 850])]
    deckel = dict(art='deckel', s=1, titel=verbinde(titel), unter='', zeilen=[verbinde(z) for z in kopf_zeilen])
    block, hinweis = [], []
    for z in devise:
        ziel = hinweis if z[0]['oben'] > 1050 else block      # Leerzeile im Original trennt den Hinweis zu den Allergenen ab
        ziel.append(dict(text=verbinde(z), fett=True) if ist_schmuck(z[0]) else dict(text=verbinde(z)))
    frei = [dict(t='frei', zeilen=block, s=1), dict(t='frei', zeilen=hinweis, s=1)]
    # Seite 2: links Speisen, rechts Kaltes, Kinder, Dessert, Jugendschutz
    links2 = lies_spalte(wo(2, 0, 450), 2, 42, 378, 270)
    rechts2_st = wo(2, 450, 9999)
    schutz_ab = min(s['oben'] for s in rechts2_st if ist_schmuck(s) and s['oben'] > 900)
    rechts2 = lies_spalte([s for s in rechts2_st if s['oben'] < schutz_ab], 2, 473, 808, 600)
    schutz = [z for z in zeilen([s for s in rechts2_st if s['oben'] >= schutz_ab and s['fam'] != 'Wingdings'])]
    rechts2.append(dict(t='rubrik', titel=verbinde(schutz[0]), en='', s=2))
    rechts2.append(dict(t='frei', zeilen=[dict(text=verbinde(z)) for z in schutz[1:]], s=2))

    posten = getraenke + frei + links2 + rechts2
    karte = dict(ziel='karte-2026', name=deckel['titel'], gruppe='Karte', quelle='assets/pdf/Karte-2026.pdf', format=[210, 297], kl='', fuss='',
                 teile=[deckel, dict(art='inhalt', posten=posten)])
    sha = hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()
    return dict(
        schema=1, haus='gasterntal',
        karten=[dict(
            id='karte-2026',
            gilt=dict(von='', bis=''),
            fassungen={},
            herkunft=dict(original='Berghotel Gasterntal/assets/pdf/Karte-2026.pdf', sha256=sha, gelesen_mit='einlesen/gasterntal_lesen.py'),
            offen=[
                'Zeitraum der Karte: das Original nennt kein «gilt von» und kein «gilt bis» (der Dateiname des Hauses sagt nur «2026»).',
                'Allergene je Gericht: das Original nennt keine, nur den Satz, dass die Mitarbeiter Auskunft geben.',
                'Währung: auf der Karte steht bei keinem Preis eine Währung.',
                'Zeichen auf dem Umschlag (Bild mit Schriftzug): liegt im Original als Bild vor, nicht als Text, und ist nicht übernommen.',
                'Fettdruck einzelner Wörter (Jugendschutz, Namen der Getränke) und das Aufzählungszeichen vor zwei Zeilen des Jugendschutzes '
                'sind Gestaltung des Originals und stehen nicht in den Daten.',
            ],
            karte=karte)])


if __name__ == '__main__':
    d = lies()
    text = json.dumps(d, ensure_ascii=False, indent=1)
    if '--zeige' in sys.argv:
        print(text)
    else:
        ZIEL.parent.mkdir(parents=True, exist_ok=True)
        ZIEL.write_text(text + '\n', encoding='utf-8')
        k = d['karten'][0]['karte']
        n = sum(len(t.get('posten', [])) for t in k['teile'])
        print(f'geschrieben: {ZIEL.relative_to(HIER.parent.parent.parent)} · {n} Einträge · Original {d["karten"][0]["herkunft"]["sha256"][:12]}')
