#!/usr/bin/env python3
"""Beschreibung von Culinarium für den Schreibtisch des Stamms (Le Bureau · Website pflegen), 28.10.2026.
   python3 _werkzeuge/bureau/beschreibung.py          schreibt beide Dateien neu und legt die Probe-Kopie an, falls sie fehlt
   python3 _werkzeuge/bureau/beschreibung.py --pruef  zeigt nur, was geschrieben würde

Schreibt (Muster Schäfli 21.10.2026, Master Werkzeug-Bau 4.2 L17/L18):
  ~/Desktop/Website-Projekte/_Werkzeuge/haeuser/culinarium/haus.json                 Kennung, Name, Welt, Quelle
  ~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/haeuser/culinarium.json    Seiten, Bereiche, Angaben, Abende
Nichts wird abgetippt: Seiten aus dem Menü der gebauten Website, Telefon, Adresse und Links aus dem Fuss von index.html,
die Welt aus _kette/05-markenbauer/marke.json. Die Website selbst (website/) wird nur gelesen."""
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parent.parent
WEB = PROJEKT / 'website'
STAMM = Path.home() / 'Desktop/Website-Projekte/_Werkzeuge'
HAUS = 'culinarium'
FOTO_SEITE = {'impressum.html': 'kanister', 'datenschutz.html': 'schildnah'}   # Seiten ohne eigenes Foto: Bild für Google-Texte und Listen (Fotos der Website)
# Zeiten und Preise: Muster des Stamms (api.py › ZAHL) mit «EUR», denn die Website schreibt Preise als «89,00 EUR» (Stamm kennt CHF, Fr., €)
ZAHL_EUR = (r'(CHF|Fr\.|€|\bEUR\b|\bUhr\b|\d+\s?(Minuten|Min\.|m²|m2|Personen|Pers\.|Nächte?|Nacht|Betten|Plätze|Gänge|Drinks|km|m ü\. M\.)'
            r'|\d{1,2}[.:]\d{2}\s?(?:[–-]|bis)\s?\d{1,2}[.:]\d{2}|\d{1,2}[.:]\d{2}\s?Uhr)')


def lies(name):
    return (WEB / name).read_text(encoding='utf-8')


def seiten():
    """Jede Seite, die das Menü der Website nennt, dazu Impressum und Datenschutz aus dem Fuss. Wahlseiten und termine-pflege.html
    (Vorschau-Werkzeug der Website) gehören nicht dazu."""
    start = lies('index.html')
    menue = re.search(r'<div class="menue" id="menue".*?</nav>', start, re.S).group(0)
    namen = ['index.html'] + [d for d in re.findall(r'href="([a-z-]+\.html)"', menue) if d != 'index.html']
    namen += [d for d in re.findall(r'href="((?:impressum|datenschutz)\.html)"', start) if d not in namen]
    for d in namen:
        if not (WEB / d).is_file():
            sys.exit(f'{d} steht im Menü, liegt aber nicht in website/.')
    return list(dict.fromkeys(namen))


def angaben():
    h = lies('index.html')
    tel = re.search(r'href="tel:(\+\d+)">([^<]+)</a>', h)
    ort = re.search(r'<p class="menue-ort">Walk on the Wild Side · ([^·<]+?) · ([^<]+?)</p>', h)
    ig = re.findall(r'href="(https://www\.instagram\.com/[^"/]+/)"', h)
    if not (tel and ort and ig):
        sys.exit('Telefon, Adresse oder Instagram stehen nicht mehr im Fuss/Menü von index.html: Beschreibung nicht geschrieben.')
    q = 'website/index.html (gebaut aus website/bau.py › fuss(), kopf())'
    aus = [{'key': 'telefon', 'label': 'Telefon der Bar', 'art': 'telefon', 'wert': tel.group(2).strip(), 'link': 'tel:' + tel.group(1), 'quelle': q},
           {'key': 'strasse', 'label': 'Strasse', 'art': 'text', 'wert': ort.group(1).strip(), 'quelle': q},
           {'key': 'ort', 'label': 'PLZ und Ort', 'art': 'text', 'wert': ort.group(2).strip(), 'quelle': q}]
    namen = {'culinarium_hannover': 'Instagram Culinarium', 'walkonthewildside_hannover': 'Instagram der Bar', 'dirtychicken.hannover': 'Instagram Dirty Chicken'}
    reihe = list(namen)
    for u in sorted(dict.fromkeys(ig), key=lambda u: reihe.index(u.rstrip('/').rsplit('/', 1)[1]) if u.rstrip('/').rsplit('/', 1)[1] in reihe else 9):
        k = u.rstrip('/').rsplit('/', 1)[1]
        aus.append({'key': 'ig-' + re.sub(r'[^a-z]', '', k)[:20], 'label': namen.get(k, 'Instagram ' + k), 'art': 'link', 'wert': u, 'quelle': q})
    return aus


def beschreibung():
    s = seiten()
    rechts = [d for d in s if d in ('impressum.html', 'datenschutz.html')]
    website = [
        ('start', 'Startseite', 'Der erste Eindruck: was Culinarium ist, das Haus in Linden, das erste Glas, die Gänge, die Plakate und die Leute.', ['index.html'], 'tafelleer'),
        ('abend', 'Der Abend', 'Wie ein Abend abläuft, was auf den Tisch kommt, wann und wie viel, die nächsten Termine und die Warteliste. Die Termine selbst pflegst du unter «Termine».', ['abend.html'], 'beete'),
        ('abende', 'Alle Abende', 'Jeder Abend seit 2023 mit Plakat, Datum und Preis, in Vitrinen nach Jahr.', ['abende.html'], 'p_DbYnkdkjrNy'),
        ('haus', 'Das Haus', 'Das Walk on the Wild Side: die Bar, ihre Geschichte und ihre Zeiten.', ['bar.html'], 'theke'),
        ('leute', 'Team', 'Die Menschen hinter Culinarium und der Bar, mit ihren Aufgaben.', ['leute.html'], 'team_alle'),
        ('weg', 'Der Weg', 'Adresse, Anfahrt und wann die Bar offen hat.', ['weg.html'], 'wg_schildnacht'),
        ('dirty-chicken', 'Dirty Chicken', 'Das Pop-up aus der Familie der Bar: Essen, Nacht, das erste Pop-up.', ['dirty-chicken.html'], 'dc_tisch'),
        ('recht', 'Rechtliches', 'Impressum und Datenschutz im Wortlaut des Hauses.', rechts, 'barneg'),
    ]
    fehlt = set(s) - {d for w in website for d in w[3]}
    if fehlt:
        sys.exit('Seiten ohne Bereich: ' + ', '.join(sorted(fehlt)))
    return {
        '_lies_mich': 'Beschreibung des Hauses für das Werkzeug «website» (Le Bureau · Website pflegen). Culinarium Hannover: Food-Pairing-Abende im Walk on the Wild Side, '
                      'nur Deutsch. Jeder Text, jede Zahl, jedes Foto wird aus den gebauten Seiten gelesen (website/ des Projekts). Läuft im Rahmen des Hauses: '
                      'http://127.0.0.1:9082/_werkzeuge/bureau/ (Culinarium Hannover/_werkzeuge/bureau/). Geschrieben von _werkzeuge/bureau/beschreibung.py, nie von Hand ändern.',
        'seiten': [dict({'datei': d}, **({'foto': FOTO_SEITE[d]} if d in FOTO_SEITE else {})) for d in s],
        'sprachen': [],
        'kopie': {'unter': 'website', 'ordner': ['assets']},
        'gesperrt': [],
        'auslassen': ['[data-termine]', '.tb-dialog', 'img[src^="assets/ueberleitung/"]', 'img[src^="assets/abend-auftakt/"]', 'img[src*="team_alle_vorn"]'],   # Termine: eigene Ansicht; Einzelbilder der Scroll-Filme und die freigestellten Leute im Team-Kopf (Ebene über dem Foto) sind keine tauschbaren Fotos
        'vorschau': {'ohne_skripte': [], 'zusatz_css': '.fenster{overflow:clip}@media (hover:none){[data-ws-e],img[data-ws-b]{cursor:pointer}}'},
        'bereiche': {
            **{k: {'an': False} for k in ('zimmer', 'preisstufen', 'packages', 'saele', 'unterlagen', 'stellen')},
            'abende': {
                'name': 'Archiv der Abende',
                'satz': 'Jeder Abend seit 2023 mit Datum, Preis und Plakat, so wie er auf der Seite «Alle Abende» steht. Was nicht mehr gezeigt werden soll, blendest du aus.',
                'quellen': [{'seite': 'abende.html', 'jedes': '.vitrinen figure.vit-p', 'felder': [
                    {'key': 'datum', 'label': 'Datum', 'art': 'text', 'wo': '.vit-datum', 'titel': True},
                    {'key': 'preis', 'label': 'Preis und Zusatz', 'art': 'zahl', 'wo': '.vit-mono'},
                    {'key': 'mit', 'label': 'Zeile auf dem Plakat', 'art': 'text', 'wo': '.vit-mit'},
                    {'key': 'bild', 'label': 'Plakat', 'art': 'bild', 'wo': '.vit-rahmen img', 'kann_fehlen': True}]}]},
        },
        'zahlen': {'muster': ZAHL_EUR},
        'kleid': {'foto': 'fassade'},
        'website': [{'key': k, 'name': n, 'satz': t, 'seiten': sei, 'foto': f} for k, n, t, sei, f in website],
        'angaben': angaben(),
        'google': {'an': True},
        'hochladen': {'an': True, 'ordner': 'assets/bild'},
        'funktionen': ['leiste_klar', 'team_wer'],
        'anleitung': '/_werkzeuge/bureau/anleitung.html',
    }


def haus():
    try:
        welt = json.loads((PROJEKT / '_kette/05-markenbauer/marke.json').read_text(encoding='utf-8')).get('welt') or 'grand'
    except (OSError, ValueError):
        welt = 'grand'
    return {'kennung': HAUS, 'name': 'Culinarium', 'welt': welt, 'quelle': '~/Desktop/Website-Projekte/Culinarium Hannover',
            'hinweis': 'Food-Pairing-Abende «Momo x Rudi» im Walk on the Wild Side, Hannover-Linden. Nur Deutsch. Welt aus _kette/05-markenbauer/marke.json. '
                       'Angelegt 28.10.2026 vom Bau-Chat Le Bureau (culinarium-bureau) mit _werkzeuge/bureau/beschreibung.py. Die Quelle wird nur gelesen, nie beschrieben.'}


def schreib(p, d):
    neu = json.dumps(d, ensure_ascii=False, indent=1) + '\n'
    if p.is_file() and p.read_text(encoding='utf-8') == neu:
        return f'{p.name}: unverändert'
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix('.tmp')
    tmp.write_text(neu, encoding='utf-8')
    tmp.replace(p)
    return f'{p.name}: geschrieben'


if __name__ == '__main__':
    b, h = beschreibung(), haus()
    if '--pruef' in sys.argv:
        print(json.dumps({'haus': h, 'beschreibung': b}, ensure_ascii=False, indent=1))
        sys.exit()
    print(schreib(STAMM / 'haeuser' / HAUS / 'haus.json', h))
    print(schreib(STAMM / 'werkzeuge/website/haeuser' / f'{HAUS}.json', b))
    print(subprocess.run([sys.executable, str(STAMM / 'werkzeuge/website/probe.py'), HAUS], capture_output=True, text=True).stdout.strip())
