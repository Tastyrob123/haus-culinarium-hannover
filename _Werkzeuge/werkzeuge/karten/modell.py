"""modell.py · das Datenmodell der Karten, für jedes Haus dasselbe.

Ein Haus hat im Speicher unter dem Werkzeug «karten» EIN Dokument:

    { "schema": 1, "haus": "<kennung>",
      "karten": [ { "id": "karte-2026",
                    "gilt": { "von": "", "bis": "" },          Zeitraum der Karte (JJJJ-MM-TT), leer = nicht gesagt
                    "fassungen": { "en": { "stand_de": "<kennung>", "karte": {…} } },   Sprachfassungen, leer = keine
                    "herkunft": {…}, "offen": [ … ],           woher gelesen, was das Original nicht sagt
                    "karte": { "ziel", "name", "gruppe", "format": [b, h], "kl", "fuss", "teile": [ … ] } } ] }

Teile einer Karte: { "art": "deckel", "titel", "unter", "zeilen": [text] } und { "art": "inhalt", "posten": [ … ] }.
Posten (Feld «t»):
    rubrik   titel · en · zusatz · koepfe[]              Rubrik, wahlweise mit Spaltenköpfen einer Tafel
    land     text                                        grosser Zwischentitel (Land der Weinkarte)
    zw       text · koepfe[]                             kleiner Zwischentitel
    kopf     text                                        Spaltenkopf rechts
    zeile    name · preis                                Tafelzeile
    notiz    text · en                                   Erläuterung
    gericht  name · zusatz · zeilen[] · preise[] · einheiten[] · allergene[] · uebersetzung
    frei     zeilen[]                                    freier Block
    zeilen:  { text, en, fett, preise[] }
Jeder Posten kann «aus»: true tragen (ausgeblendet statt gelöscht) und «s» (Seite im Original).
«einheiten» läuft neben «preise»: die Angabe zum Preis («33cl», «Portion»). «allergene»: Schlüssel aus ALLERGENE.
«uebersetzung»: "offen", wenn die deutsche Zeile geändert wurde und die englische noch nicht.

Hier steht nichts über ein bestimmtes Haus. Ein drittes Haus ist ein weiteres Dokument derselben Form.
"""
import collections
import hashlib
import json
import re
import subprocess
import unicodedata

SCHEMA = 1
SATZ_VERSION = 5          # wie in satz.js: ändert sich der Satz, gelten gespeicherte PDF als veraltet
TYPEN = ('rubrik', 'land', 'zw', 'kopf', 'zeile', 'notiz', 'gericht', 'frei')
# Die 14 Zutaten, die nach Lebensmittelrecht (CH: LIV Anhang 6, EU: LMIV Anhang II) auf Verlangen zu nennen sind
ALLERGENE = collections.OrderedDict([
    ('gluten', 'Glutenhaltiges Getreide'), ('krebstiere', 'Krebstiere'), ('eier', 'Eier'), ('fisch', 'Fisch'), ('erdnuesse', 'Erdnüsse'),
    ('soja', 'Soja'), ('milch', 'Milch'), ('nuesse', 'Hartschalenobst (Nüsse)'), ('sellerie', 'Sellerie'), ('senf', 'Senf'), ('sesam', 'Sesam'),
    ('sulfite', 'Schwefeldioxid und Sulfite'), ('lupinen', 'Lupinen'), ('weichtiere', 'Weichtiere')])
_ID = re.compile(r'^[a-z0-9][a-z0-9-]{0,29}$')
_DATUM = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
_SPRACHE = re.compile(r'^[a-z]{2}$')
MAX_TEXT, MAX_POSTEN, MAX_KARTEN, MAX_LISTE = 600, 3000, 40, 60


def kennung(daten):
    roh = json.dumps(daten, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(roh.encode('utf-8')).hexdigest()[:16]


def druck_kennung(karte, welt, haus_name, kleid=''):
    """Wovon die PDF abhängt: Karte, Welt, Name und Kleid des Hauses (Zeichen, Tapete), Stand des Satzes."""
    return kennung({'karte': karte, 'welt': welt, 'haus': haus_name, 'kleid': kleid, 'satz': SATZ_VERSION})


def _text(x, was, pflicht=False):
    if not isinstance(x, str):
        return f'{was} ist kein Text.'
    if len(x) > MAX_TEXT:
        return f'{was} ist länger als {MAX_TEXT} Zeichen.'
    if pflicht and not x.strip():
        return f'{was} fehlt.'
    if any(ord(c) < 32 for c in x):
        return f'{was} enthält ein Steuerzeichen (Zeilenumbruch oder Tabulator).'
    return ''


def _texte(x, was):
    if not isinstance(x, list) or len(x) > MAX_LISTE:
        return f'{was} ist keine Liste (höchstens {MAX_LISTE}).'
    for t in x:
        f = _text(t, was)
        if f:
            return f
    return ''


def _datum(x, was):
    if x == '':
        return ''
    m = _DATUM.match(x) if isinstance(x, str) else None
    if not m or not (1 <= int(m.group(2)) <= 12 and 1 <= int(m.group(3)) <= 31):
        return f'{was} ist kein Datum (Tag.Monat.Jahr).'
    return ''


def pruefe_karte(k):
    """Erste Unstimmigkeit einer Karte in Alltagssprache, '' = in Ordnung."""
    if not isinstance(k, dict):
        return 'Die Karte ist kein Datensatz.'
    name = k.get('name') if isinstance(k.get('name'), str) else ''
    f = _text(k.get('name'), 'Der Name der Karte', True) or _text(k.get('fuss', ''), 'Die Fusszeile') or _text(k.get('kl', ''), 'Die Art des Satzes')
    if f:
        return f
    fo = k.get('format')
    if not (isinstance(fo, list) and len(fo) == 2 and all(isinstance(x, (int, float)) and not isinstance(x, bool) and 50 <= x <= 600 for x in fo)):
        return f'«{name}»: das Format fehlt (Breite und Höhe in Millimetern).'
    if not re.match(r'^[a-z ]{0,40}$', k.get('kl', '')):
        return f'«{name}»: die Art des Satzes ist unbekannt.'
    if not isinstance(k.get('teile'), list) or not k['teile']:
        return f'«{name}» hat keine Teile.'
    posten = sichtbar = 0
    for i, t in enumerate(k['teile']):
        if not isinstance(t, dict):
            return f'«{name}»: Teil {i + 1} ist kein Datensatz.'
        if t.get('art') == 'deckel':
            f = _text(t.get('titel'), 'Der Titel des Deckblatts', True) or _text(t.get('unter', ''), 'Die Zeile unter dem Titel') or _texte(t.get('zeilen', []), 'Eine Zeile des Deckblatts')
            if f:
                return f'«{name}»: {f}'
            continue
        if t.get('art') != 'inhalt' or not isinstance(t.get('posten'), list):
            return f'«{name}»: Teil {i + 1} ist weder Deckblatt noch Inhalt.'
        for u in t['posten']:
            posten += 1
            if posten > MAX_POSTEN:
                return f'«{name}» hat mehr als {MAX_POSTEN} Einträge.'
            f = pruefe_posten(u)
            if f:
                return f'«{name}»: {f}'
            sichtbar += 0 if u.get('aus') else 1
    if not sichtbar:
        return f'Auf «{name}» steht nichts mehr.'
    return ''


def pruefe_posten(u):
    if not isinstance(u, dict) or u.get('t') not in TYPEN:
        return 'Ein Eintrag hat eine unbekannte Art.'
    t = u['t']
    was = u.get('name') or u.get('titel') or u.get('text') or ''
    was = f'«{was}»' if isinstance(was, str) and was else 'Ein Eintrag'
    if 'aus' in u and not isinstance(u['aus'], bool):
        return f'{was}: «ausgeblendet» ist weder ja noch nein.'
    for feld in ('titel', 'en', 'zusatz', 'text', 'name', 'preis'):
        if feld in u and not (feld == 'en' and isinstance(u[feld], bool)):
            f = _text(u[feld], f'{was}: das Feld «{feld}»')
            if f:
                return f
    if t == 'rubrik' and not str(u.get('titel', '')).strip():
        return 'Eine Rubrik hat keinen Titel.'
    if t in ('gericht', 'zeile') and not str(u.get('name', '')).strip():
        return 'Ein Gericht hat keinen Namen.' if t == 'gericht' else 'Eine Zeile hat keinen Namen.'
    if t in ('land', 'zw', 'kopf', 'notiz') and not str(u.get('text', '')).strip():
        return 'Ein Zwischentitel oder eine Erläuterung ist leer.'
    for feld in ('koepfe', 'preise', 'einheiten'):
        if feld in u:
            f = _texte(u[feld], f'{was}: «{feld}»')
            if f:
                return f
    if 'einheiten' in u and len(u['einheiten']) != len(u.get('preise') or []):
        return f'{was}: zu jedem Preis gehört genau eine Angabe (sie darf leer sein).'
    if 'allergene' in u and not (isinstance(u['allergene'], list) and all(a in ALLERGENE for a in u['allergene'])):
        return f'{was}: ein Allergen ist unbekannt.'
    if 'uebersetzung' in u and u['uebersetzung'] != 'offen':
        return f'{was}: der Vermerk zur Übersetzung ist unbekannt.'
    if 'zeilen' in u:
        if not isinstance(u['zeilen'], list) or len(u['zeilen']) > MAX_LISTE:
            return f'{was}: die Zeilen sind keine Liste.'
        for z in u['zeilen']:
            if not isinstance(z, dict):
                return f'{was}: eine Zeile ist kein Datensatz.'
            f = _text(z.get('text'), f'{was}: eine Zeile') or ('preise' in z and _texte(z['preise'], f'{was}: Preise einer Zeile')) or ''
            if f:
                return f
    if t == 'frei' and not any(str(z.get('text', '')).strip() for z in u.get('zeilen') or []):
        return 'Ein freier Block ist leer.'
    return ''


def pruefe(d, haus=None):
    """Erste Unstimmigkeit des ganzen Dokuments, '' = in Ordnung."""
    if not isinstance(d, dict) or d.get('schema') != SCHEMA:
        return 'Die Daten haben nicht die Form dieses Werkzeugs.'
    if haus is not None and d.get('haus') != haus:
        return 'Die Daten gehören zu einem anderen Haus.'
    if not isinstance(d.get('karten'), list) or not d['karten'] or len(d['karten']) > MAX_KARTEN:
        return f'Ein Haus braucht mindestens eine Karte (höchstens {MAX_KARTEN}).'
    gesehen = set()
    for e in d['karten']:
        if not isinstance(e, dict) or not isinstance(e.get('id'), str) or not _ID.match(e['id']):
            return 'Eine Karte hat keine gültige Kennung.'
        if e['id'] in gesehen:
            return f'Die Kennung «{e["id"]}» kommt zweimal vor.'
        gesehen.add(e['id'])
        g = e.get('gilt')
        if not isinstance(g, dict) or set(g) != {'von', 'bis'}:
            return f'«{e["id"]}»: der Zeitraum fehlt (von, bis; beides darf leer sein).'
        f = _datum(g['von'], 'Gilt von') or _datum(g['bis'], 'Gilt bis')
        if f:
            return f'«{e["id"]}»: {f}'
        if g['von'] and g['bis'] and g['von'] > g['bis']:
            return f'«{e["id"]}»: «gilt bis» liegt vor «gilt von».'
        f = pruefe_karte(e.get('karte'))
        if f:
            return f
        fa = e.get('fassungen')
        if not isinstance(fa, dict):
            return f'«{e["id"]}»: die Sprachfassungen fehlen (dürfen leer sein).'
        for sp, x in fa.items():
            if not _SPRACHE.match(sp) or not isinstance(x, dict) or not isinstance(x.get('stand_de'), str):
                return f'«{e["id"]}»: die Sprachfassung «{sp}» ist unvollständig.'
            f = pruefe_karte(x.get('karte'))
            if f:
                return f'Sprachfassung «{sp}»: {f}'
    return ''


def sprachen_stand(d):
    """Je Karte und Sprachfassung: passt sie noch zum Deutschen? Dazu die Einträge, deren englische Zeile nachzuziehen ist."""
    aus = []
    for e in d['karten']:
        k = kennung(e['karte'])
        offen = [u.get('name') or u.get('titel') or '' for t in e['karte']['teile'] for u in t.get('posten', []) if u.get('uebersetzung') == 'offen' and not u.get('aus')]
        aus.append({'id': e['id'], 'name': e['karte']['name'], 'kennung_de': k, 'zeilen_offen': offen,
                    'fassungen': [{'sprache': sp, 'aktuell': x['stand_de'] == k, 'stand_de': x['stand_de']} for sp, x in sorted(e.get('fassungen', {}).items())]})
    return aus


# ---------- PDF gegen Daten ----------

def _norm(t):
    t = unicodedata.normalize('NFC', t).replace('\xa0', ' ').replace('\xad', '')
    for a, b in (('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬀ', 'ff'), ('ﬃ', 'ffi'), ('ﬄ', 'ffl'), ('ß', 'ss'), ('ẞ', 'ss')):
        t = t.replace(a, b)
    return t.lower()


def woerter(t):
    """Wörter aus Buchstaben und Ziffern, Gross/Klein egal (Versalzeilen der Karte stehen in der PDF gross)."""
    return collections.Counter(re.findall(r'[^\W_]+', _norm(t)))


def gedruckte_posten(posten):
    """Was der Satz von einem Teil druckt: nichts Ausgeblendetes, und keine Rubrik oder Erläuterung am Ende, auf die kein Eintrag
    mehr folgt (wie satz.js, setze)."""
    u = [x for x in posten if not x.get('aus')]

    def kopf(x):
        return x['t'] in ('rubrik', 'land', 'zw', 'kopf')

    def vorspann(i):
        if kopf(u[i]):
            return True
        if u[i]['t'] != 'notiz':
            return False
        j = i
        while j > 0 and u[j]['t'] == 'notiz':
            j -= 1
        return kopf(u[j])
    while u and vorspann(len(u) - 1):
        u.pop()
    return u


def karten_text(karte, haus_name, seiten):
    """Alles, was auf der gedruckten Karte stehen muss: die Daten, dazu der Name des Hauses (Deckblatt und Kopf jeder Innenseite)
    und die Fusszeile auf jeder Innenseite. Hat das Haus ein Zeichen, steht das statt des Namens da: haus_name ist dann leer."""
    s, deckel = [], 0
    for t in karte['teile']:
        if t['art'] == 'deckel':
            deckel += 1
            s += [t.get('titel', ''), t.get('unter', '')] + list(t.get('zeilen') or [])
            continue
        for u in gedruckte_posten(t['posten']):
            s += [u.get(k, '') for k in ('titel', 'zusatz', 'text', 'name', 'preis')]
            if isinstance(u.get('en'), str):
                s.append(u['en'])
            ein = u.get('einheiten') or []
            s += list(u.get('koepfe') or []) + list(u.get('preise') or []) + (list(ein) if any(ein) else [])
            for z in u.get('zeilen') or []:
                s += [z['text']] + list(z.get('preise') or [])
            if u.get('allergene'):
                s += ['Enthält'] + [ALLERGENE[a] for a in u['allergene']]
    innen = max(0, seiten - deckel)
    s += [karte.get('fuss', '')] * innen + [haus_name] * seiten
    return ' '.join(x for x in s if isinstance(x, str) and x)


def pdf_text(pdf):
    """(Seitenzahl, Text) einer PDF. Die PDF kommt über die Standardeingabe, es entsteht keine Datei."""
    try:
        info = subprocess.run(['pdfinfo', '-'], input=pdf, capture_output=True, timeout=60)
        text = subprocess.run(['pdftotext', '-layout', '-', '-'], input=pdf, capture_output=True, timeout=60)
    except FileNotFoundError:
        raise RuntimeError('pdftotext fehlt auf diesem Rechner (poppler). Ohne es lässt sich die PDF nicht gegen die Daten prüfen.')
    except subprocess.TimeoutExpired:
        raise RuntimeError('Das Lesen der PDF hat zu lange gedauert. Es wurde nichts veröffentlicht, bitte noch einmal versuchen.')
    m = re.search(r'Pages:\s+(\d+)', info.stdout.decode('utf-8', 'replace'))
    if info.returncode or text.returncode or not m:
        raise RuntimeError('Die PDF lässt sich nicht lesen.')
    return int(m.group(1)), text.stdout.decode('utf-8', 'replace')


def pdf_gegen_daten(pdf, karte, haus_name):
    """Steht in der PDF genau, was in den Daten steht? Rückgabe: dict(ok, seiten, fehlt, dazu)."""
    seiten, text = pdf_text(pdf)
    ist, soll = woerter(text), woerter(karten_text(karte, haus_name, seiten))
    fehlt, dazu = soll - ist, ist - soll
    # gleiche Zeichen, nur anders getrennt (Umbruch mitten im Wort): gilt als gleich
    if fehlt and collections.Counter(''.join(fehlt.elements())) == collections.Counter(''.join(dazu.elements())):
        fehlt = dazu = collections.Counter()
    return {'ok': not fehlt and not dazu, 'seiten': seiten, 'fehlt': dict(fehlt), 'dazu': dict(dazu), 'woerter': sum(soll.values())}
