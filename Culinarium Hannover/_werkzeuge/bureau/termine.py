"""Termine von Culinarium im Le Bureau (28.10.2026): die nächsten Abende als Daten, nie als Text.

Die Website zeichnet die Terminplakate auf «Der Abend» aus einer Liste in website/assets/buchen.js (BEISPIEL, gebaut von
website/buchen.py, Vorschau ohne echte Buchung). Diese Liste ist der Ursprung: sie wird gelesen, nie abgetippt und nie verändert.
Hier liegen dazu Entwurf, veröffentlichter Stand und Verlauf (Master Werkzeug-Bau 2.2), in einer Datei mit Sicherung der letzten
guten Fassung (.gut). Ausgeliefert wird der Stand, indem der Server des Bureau buchen.js der Probe-Kopie beim Ausliefern mit
dem Stand füllt (fuelle()); ohne Änderung bleibt die Datei Byte für Byte, wie die Website sie gebaut hat.

Jede Anfrage, die den Entwurf ersetzt, trägt dessen Fingerabdruck (erwartet); passt er nicht mehr: KONFLIKT (409, L13).
Meldungen in der Form STICHWORT · Text (Master 2.6), jedes Stichwort steht im Lexikon der Prüfseite (pruefung-haus.js)."""
import datetime
import hashlib
import json
import os
import re
import threading
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
QUELLE = HIER.parent.parent / 'website' / 'assets' / 'buchen.js'
DATEN = Path(os.environ['WERKZEUGE_DATEN']) / 'bureau-termine' if os.environ.get('WERKZEUGE_DATEN') else HIER / '_daten'
DATEI = DATEN / 'termine.json'
WER = 'Team Culinarium'
HOECHSTENS = 40
_SCHLOSS = threading.Lock()
MUSTER = re.compile(r'(var BEISPIEL = )(\[.*?\])(;)', re.S)
KEY = re.compile(r"(var KEY = ')([\w-]+)(';)")


class Fehler(Exception):
    def __init__(self, status, stichwort, text):
        super().__init__(text)
        self.status, self.stichwort, self.text = status, stichwort, text


def ursprung():
    """Die Termine, wie die Website sie gebaut hat: die Liste BEISPIEL aus buchen.js, als JSON gelesen (Schlüssel ohne Anführungszeichen)."""
    try:
        roh = QUELLE.read_text(encoding='utf-8')
    except OSError:
        raise Fehler(503, 'termine-quelle', 'TERMINE · website/assets/buchen.js ist nicht lesbar.')
    m = MUSTER.search(roh)
    if not m:
        raise Fehler(503, 'termine-quelle', 'TERMINE · In buchen.js steht keine Liste «BEISPIEL» mehr. Die Website wurde umgebaut; die Termine lassen sich erst wieder pflegen, wenn die Liste da ist.')
    js = re.sub(r"([{,]\s*)([a-z]+)\s*:", r'\1"\2":', m.group(2)).replace("'", '"')
    try:
        return [pruefe_einen(t, i) for i, t in enumerate(json.loads(js))]
    except (ValueError, Fehler) as e:
        raise Fehler(503, 'termine-quelle', f'TERMINE · Die Liste in buchen.js ist nicht lesbar ({e}).')


def fingerabdruck(liste):
    return hashlib.sha1(json.dumps(liste, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()[:12]


def pruefe_einen(t, i=0):
    """Ein Termin: Datum, Beginn, Preis, Plätze, vergebene Plätze. Alles andere wird abgelehnt (keine fremden Felder auf die Website)."""
    if not isinstance(t, dict):
        raise Fehler(400, 'termin-falsch', 'TERMIN · Ein Eintrag ist kein Termin.')
    nr = f'Termin {i + 1}: '
    tid = str(t.get('id') or '')
    if not re.fullmatch(r'[a-z0-9-]{1,24}', tid):
        raise Fehler(400, 'termin-falsch', 'TERMIN · ' + nr + 'Kennung fehlt.')
    d = str(t.get('datum') or '')
    try:
        datetime.date.fromisoformat(d)
    except ValueError:
        raise Fehler(400, 'termin-datum', 'DATUM · ' + nr + 'Das Datum fehlt oder gibt es nicht.')
    z = str(t.get('zeit') or '')
    if not re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d', z):
        raise Fehler(400, 'termin-zeit', 'BEGINN · ' + nr + 'Bitte die Uhrzeit als Stunden und Minuten, zum Beispiel 19:00.')
    try:
        preis = float(t.get('preis'))
        plaetze = int(t.get('plaetze'))
        gebucht = int(t.get('gebucht') or 0)
    except (TypeError, ValueError):
        raise Fehler(400, 'termin-zahl', 'ZAHL · ' + nr + 'Preis und Plätze brauchen eine Zahl.')
    if not (0 < preis <= 999) or round(preis * 100) != preis * 100:
        raise Fehler(400, 'termin-preis', 'PREIS · ' + nr + 'Der Preis liegt zwischen 1 und 999 Euro, höchstens mit Cent.')
    if not (1 <= plaetze <= 40):
        raise Fehler(400, 'termin-plaetze', 'PLÄTZE · ' + nr + 'Ein Abend hat zwischen 1 und 40 Plätze.')
    if not (0 <= gebucht <= plaetze):
        raise Fehler(400, 'termin-plaetze', 'PLÄTZE · ' + nr + 'Es sind mehr Plätze vergeben, als der Abend hat.')
    return {'id': tid, 'datum': d, 'zeit': z, 'preis': int(preis) if preis == int(preis) else preis, 'plaetze': plaetze, 'gebucht': gebucht}


def pruefe(liste):
    if not isinstance(liste, list):
        raise Fehler(400, 'termin-falsch', 'TERMIN · Die Anfrage enthält keine Liste von Terminen.')
    if len(liste) > HOECHSTENS:
        raise Fehler(400, 'termin-viele', f'TERMINE · Höchstens {HOECHSTENS} Termine stehen gleichzeitig auf der Website.')
    aus = [pruefe_einen(t, i) for i, t in enumerate(liste)]
    if len({t['id'] for t in aus}) != len(aus):
        raise Fehler(400, 'termin-falsch', 'TERMIN · Zwei Termine tragen dieselbe Kennung.')
    if len({(t['datum'], t['zeit']) for t in aus}) != len(aus):
        raise Fehler(400, 'termin-doppelt', 'DOPPELT · Zwei Termine stehen am selben Tag zur selben Zeit.')
    return sorted(aus, key=lambda t: (t['datum'], t['zeit']))


def _leer():
    return {'entwurf': None, 'stand': None, 'verlauf': [], 'protokoll': []}


def lade():
    """Datei lesen; ist sie beschädigt, die letzte gute Fassung, nie still leer (Master 5.1)."""
    for p in (DATEI, DATEI.with_suffix('.json.gut')):
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding='utf-8'))
                if isinstance(d, dict) and 'verlauf' in d:
                    return d
            except ValueError:
                continue
    if DATEI.is_file():
        raise Fehler(500, 'termine-speicher', 'SPEICHER · Die Datei der Termine und ihre Sicherung sind beide unlesbar. Prüfung öffnen.')
    return _leer()


def schreib(d):
    DATEN.mkdir(parents=True, exist_ok=True)
    if DATEI.is_file():
        try:
            json.loads(DATEI.read_text(encoding='utf-8'))
            DATEI.replace(DATEI.with_suffix('.json.gut'))
        except ValueError:
            pass
    tmp = DATEI.with_suffix('.tmp')
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp.replace(DATEI)


def jetzt():
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def lage(d=None):
    """Was die Ansicht braucht: Ursprung, Stand (veröffentlicht), Entwurf (falls einer wartet), Verlauf, Fingerabdruck des Entwurfs."""
    d = d or lade()
    u = ursprung()
    stand = d['stand'] if d['stand'] is not None else u
    entwurf = d['entwurf']
    return {'ursprung': u, 'stand': stand, 'entwurf': entwurf, 'wartet': entwurf is not None and entwurf != stand,
            'kennung': fingerabdruck(entwurf if entwurf is not None else stand),
            'zuletzt': next((v for v in reversed(d['verlauf']) if v.get('art') == 'veroeffentlicht'), None),
            'verlauf': [{'nr': i, 'zeit': v['zeit'], 'art': v['art'], 'notiz': v.get('notiz', ''), 'zahl': len(v['termine'])} for i, v in enumerate(d['verlauf'])][::-1],
            'quelle': 'website/assets/buchen.js › BEISPIEL'}


def wartend(l):
    """Wie viele Termine sich zwischen Stand und Entwurf unterscheiden (neu, geändert, entfällt), wie die Ansicht sie zählt."""
    if not l['wartet']:
        return 0
    alt, neu = {t['id']: t for t in l['stand']}, {t['id']: t for t in l['entwurf']}
    return sum(1 for k, t in neu.items() if alt.get(k) != t) + sum(1 for k in alt if k not in neu)


def _bewache(d, erwartet):
    l = lage(d)
    if erwartet != l['kennung']:
        raise Fehler(409, 'konflikt', 'KONFLIKT · In einem anderen Fenster wurden die Termine inzwischen geändert. Die Liste lädt neu, deine Eingaben bleiben stehen.')
    return l


def _protokoll(d, was):
    d['protokoll'] = (d['protokoll'] + [{'zeit': jetzt(), 'wer': WER, 'was': was}])[-400:]


def speichern(liste, erwartet):
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        neu = pruefe(liste)
        alt = l['entwurf'] if l['entwurf'] is not None else l['stand']
        if neu == alt:
            return {'nichts': True, 'meldung': 'Nichts geändert, nichts gespeichert.', **lage(d)}
        d['entwurf'] = None if neu == l['stand'] else neu
        _protokoll(d, 'Termine im Entwurf gespeichert')
        schreib(d)
        return {'vorher': alt, **lage(d)}


def veroeffentlichen(erwartet, notiz=''):
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        if not l['wartet']:
            return {'nichts': True, 'meldung': 'Nichts geändert, nichts veröffentlicht.', **l}
        d['stand'] = l['entwurf']
        d['entwurf'] = None
        d['verlauf'] = (d['verlauf'] + [{'zeit': jetzt(), 'art': 'veroeffentlicht', 'notiz': str(notiz or '')[:200], 'termine': d['stand']}])[-60:]
        _protokoll(d, 'Termine veröffentlicht')
        schreib(d)
        return lage(d)


def verwerfen(erwartet):
    with _SCHLOSS:
        d = lade()
        _bewache(d, erwartet)
        vorher = d['entwurf']
        d['entwurf'] = None
        _protokoll(d, 'Entwurf der Termine verworfen')
        schreib(d)
        return {'vorher': vorher, **lage(d)}


def zurueckholen(nr, erwartet):
    """Eine frühere Fassung (nr im Verlauf) oder den Ursprung («ursprung») in den Entwurf holen, nie direkt auf die Website (R14)."""
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        if nr == 'ursprung':
            t = l['ursprung']
        else:
            try:
                t = d['verlauf'][int(nr)]['termine']
            except (ValueError, IndexError, TypeError):
                raise Fehler(404, 'fassung-unbekannt', 'FASSUNG · Diese frühere Fassung gibt es nicht.')
        d['entwurf'] = None if t == l['stand'] else t
        _protokoll(d, 'Frühere Fassung der Termine in den Entwurf geholt')
        schreib(d)
        return lage(d)


def fuelle(roh, liste, u):
    """buchen.js mit einer Liste füllen. Gleich wie der Ursprung: unverändert zurück. Sonst die Liste und ein eigener Schlüssel für den
    Speicher des Browsers (sonst überdeckt eine alte Vorschau aus termine-pflege.html den veröffentlichten Stand)."""
    if liste == u:
        return roh
    js = '[\n' + ',\n'.join('    ' + json.dumps(t, ensure_ascii=False).replace('"id"', 'id').replace('"datum"', 'datum').replace('"zeit"', 'zeit')
                             .replace('"preis"', 'preis').replace('"plaetze"', 'plaetze').replace('"gebucht"', 'gebucht') for t in liste) + '\n  ]'
    roh = MUSTER.sub(lambda m: m.group(1) + js + m.group(3), roh, 1)
    return KEY.sub(lambda m: m.group(1) + m.group(2) + '-' + fingerabdruck(liste) + m.group(3), roh, 1)


def ausliefern(roh, welche='stand'):
    l = lage()
    liste = l['entwurf'] if welche == 'entwurf' and l['entwurf'] is not None else l['stand']
    return fuelle(roh, liste, l['ursprung'])


def pruefung():
    """Punkte für die Prüfseite: Quelle lesbar, Speicher lesbar, Sicherung da, Stand gültig."""
    p = []
    try:
        u = ursprung()
        p.append({'gut': True, 'titel': 'Termine der Website', 'text': f'{len(u)} Termine in website/assets/buchen.js gelesen.'})
    except Fehler as e:
        return [{'gut': False, 'titel': 'Termine der Website', 'text': e.text, 'stichwort': e.stichwort}]
    try:
        d = lade()
        for k in ('stand', 'entwurf'):
            if d[k] is not None:
                pruefe(d[k])
        p.append({'gut': True, 'titel': 'Speicher der Termine', 'text': 'lesbar' + (', Sicherung der letzten guten Fassung liegt daneben' if DATEI.with_suffix('.json.gut').is_file() else ', noch nichts gespeichert') + '.'})
    except Fehler as e:
        p.append({'gut': False, 'titel': 'Speicher der Termine', 'text': e.text, 'stichwort': e.stichwort})
    return p
