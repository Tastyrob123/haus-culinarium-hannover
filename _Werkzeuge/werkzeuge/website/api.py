"""Eigene Wege des Werkzeugs «website» (Le Bureau · Der Schreibtisch), erreichbar unter /api/x/website/<weg>.

Das Werkzeug kennt kein Haus. Was ein Haus hat (Seiten, Sprachen, Bereiche, Felder, gesperrte Abschnitte), steht in
haeuser/<haus>.json. Die Änderungen des Hauses liegen als Schicht im gemeinsamen Speicher (Werkzeug «website») und werden
für Vorschau und Veröffentlichen über die Kopie der gebauten Seiten gelegt (_probe/<haus>/grundlage → _probe/<haus>/online).

  GET  haus/<haus>                         Name, Sprachen, Seiten, Bereiche
  GET  stand/<haus>                        Stand aus dem Speicher, dazu jede offene Änderung mit vorher und nachher
  GET  seite/<haus>/<datei>                Verzeichnis einer Seite: Abschnitte, Texte, Fotos
  GET  stelle/<haus>/<datei>/<h>/<n>       eine Textstelle ganz: Original, Entwurf, Sprachen, gleiche Stellen
  GET  foto/<haus>/<datei>/<b>/<n>         ein Foto ganz
  GET  fotos/<haus>                        alle Fotos der Website (zum Tauschen)
  GET  vorschau/<haus>/<zustand>/<sprache>/<datei>   {html}: die Seite mit Entwurf (entwurf), veröffentlicht (stand), oder für «Vorher, nachher»
  GET  zahlen/<haus>                       Zeiten und Preise: jede Zahl der Website
  GET  bereich/<haus>/<schluessel>         ein Bereich des Hauses (Zimmer, Säle …) mit Einträgen und Feldern
  GET  sprachen/<haus>                     jede offene Änderung und ihre Übersetzungen
  GET  verlauf/<haus> · fassung/<haus>/<fassung>
  GET  pruefung/<haus>                     die Prüfung des Werkzeugs von der Seite des Servers
  GET  ueberblick/<haus>                   Stand-Weg für La Maison: {aenderungen, zuletzt:{zeit}, bereiche, seiten}
  POST aendern/<haus>          {ops, erwartet, wer}      speichert in den Entwurf, antwortet mit Quittung
  POST veroeffentlichen/<haus> {erwartet, wer, notiz}    prüft, veröffentlicht, schreibt die Seiten
  POST reparieren/<haus>       {was, wer}

Jede Fehlermeldung trägt ein Stichwort, das im Lexikon der Prüfung steht (pruefung.js). Neue Meldung → Stichwort und Eintrag in derselben Änderung."""
import fcntl
import html as _h
import importlib
import json
import os
import posixpath
import re
import sys
import time
import types
from pathlib import Path

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parent.parent
WERKZEUG = 'website'
VERSION = '2026-10-21.1'
if str(HIER) not in sys.path:
    sys.path.insert(0, str(HIER))

ZW = sys.modules.setdefault('ws_zwischen', types.ModuleType('ws_zwischen')).__dict__   # Zwischenspeicher über Aufrufe hinweg (api.py wird je Aufruf frisch geladen)


def _modul(name):
    """Nachbar-Modul laden; hat sich die Datei geändert, frisch (damit Änderungen ohne Neustart des Servers greifen)."""
    p = HIER / f'{name}.py'
    zeit = p.stat().st_mtime
    m = sys.modules.get(name)
    if m is None or ZW.get(('modul', name)) != zeit:
        m = importlib.reload(m) if m is not None else importlib.import_module(name)
        ZW[('modul', name)] = zeit
        for k in [k for k in ZW if isinstance(k, tuple) and k[0] in ('zer', 'spender', 'namen', 'css')]:
            del ZW[k]
    return m


S = _modul('schicht')
A = _modul('ausgabe')
if ZW.get('api_zeit') != Path(__file__).stat().st_mtime:   # diese Datei selbst hat sich geändert: was sie errechnet hat, gilt nicht mehr
    for _k in [k for k in ZW if isinstance(k, tuple) and k[0] in ('zer', 'spender', 'namen', 'css', 'besch')]:
        del ZW[_k]
    ZW['api_zeit'] = Path(__file__).stat().st_mtime

BEREICHE = {   # die Hotel-Bereiche, die das Werkzeug kennt. Ein Haus schaltet sie in seiner Beschreibung ein und sagt, wo sie stehen
    'zimmer': ('Zimmer', 'Jede Kategorie mit Name, Angaben, Text und Fotos.'),
    'preisstufen': ('Preisstufen', 'Preise je Saison oder Stufe.'),
    'packages': ('Packages', 'Angebote und Pauschalen. Was abgelaufen ist, blenden Sie aus.'),
    'saele': ('Säle', 'Räume mit Fläche, Personenzahl und Miete.'),
    'unterlagen': ('Unterlagen', 'Dokumente zum Herunterladen und wohin sie führen.'),
    'stellen': ('Stellen', 'Offene Stellen. Was besetzt ist, blenden Sie aus.'),
}
OBER = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong', 'dt', 'th', 'summary', 'legend'}
FEST_NAME = {'header': 'Kopf und Menü', 'nav': 'Menü', 'footer': 'Fuss der Seite'}
ZAHL = r'(CHF|Fr\.|€|\bUhr\b|\d+\s?(Minuten|Min\.|m²|m2|Personen|Pers\.|Nächte?|Nacht|Betten|Plätze|km|m ü\. M\.)|\d{1,2}[.:]\d{2}\s?(?:[–-]|bis)\s?\d{1,2}[.:]\d{2}|\d{1,2}[.:]\d{2}\s?Uhr)'


class Fehler(Exception):
    def __init__(self, status, stichwort, text, **mehr):
        super().__init__(text)
        self.status, self.stichwort, self.text, self.mehr = status, stichwort, text, mehr


# ------------------------------------------------------------------ Haus, Beschreibung, Probe-Kopie
def beschreibung(haus):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,40}', haus or ''):
        raise Fehler(404, 'haus-unbekannt', 'Dieses Haus gibt es nicht.')
    p, q = HIER / 'haeuser' / f'{haus}.json', WURZEL / 'haeuser' / haus / 'haus.json'
    if not p.exists() or not q.exists():
        raise Fehler(404, 'haus-unbekannt', f'Für «{haus}» liegt keine Beschreibung vor.')
    key = ('besch', haus)
    zeit = (p.stat().st_mtime, q.stat().st_mtime)
    if ZW.get(key, (None,))[0] != zeit:
        try:
            b = json.loads(p.read_text(encoding='utf-8'))
            b['stamm'] = json.loads(q.read_text(encoding='utf-8'))
        except ValueError as e:
            raise Fehler(500, 'beschreibung', f'Die Beschreibung des Hauses ist nicht lesbar: {e}')
        b['regeln'] = {'gesperrt': b.get('gesperrt') or [], 'auslassen': b.get('auslassen') or [], 'bild_groessen': b.get('bild_groessen')}
        ZW[key] = (zeit, b)
        for k in [k for k in ZW if isinstance(k, tuple) and k[0] in ('zer', 'spender', 'namen') and k[1] == haus]:
            del ZW[k]
    return ZW[key][1]


def probe(haus):
    o = A.probe_ordner() / haus
    if not (o / 'grundlage').is_dir() or not (o / 'online').is_dir():
        raise Fehler(503, 'probe-fehlt', f'Die Kopie der Seiten von «{haus}» fehlt. Anlegen: python3 werkzeuge/website/probe.py {haus}')
    return o


def probe_adresse(haus, teil):
    return '/' + (A.probe_ordner() / haus / teil).resolve().relative_to(WURZEL).as_posix() + '/'


def seiten(haus):
    return [s['datei'] for s in beschreibung(haus)['seiten']]


def sprachen(haus):
    return beschreibung(haus).get('sprachen') or []


def _rel(haus, datei, sp=''):
    if datei not in seiten(haus):
        raise Fehler(404, 'seite-unbekannt', f'«{datei}» ist keine Seite dieser Website.')
    if sp:
        o = next((x['ordner'] for x in sprachen(haus) if x['code'] == sp), None)
        if o is None:
            raise Fehler(404, 'sprache-unbekannt', f'Die Sprache «{sp}» hat dieses Haus nicht.')
        return f'{o}/{datei}'
    return datei


def grundlage(haus, datei, sp=''):
    """Eine Seite, wie das Haus sie gebaut hat. None: diese Seite gibt es in dieser Sprache nicht."""
    p = probe(haus) / 'grundlage' / _rel(haus, datei, sp)
    if not p.exists():
        if sp:
            return None
        raise Fehler(500, 'seite-fehlt', f'Die Seite «{datei}» fehlt in der Kopie.')
    key = ('src', str(p))
    zeit = p.stat().st_mtime
    if ZW.get(key, (None,))[0] != zeit:
        ZW[key] = (zeit, p.read_bytes().decode('utf-8'))
    return ZW[key][1]


def zer(haus, datei, sp=''):
    src = grundlage(haus, datei, sp)
    if src is None:
        return None
    key = ('zer', haus, datei, sp)
    if ZW.get(key, (None,))[0] is not src:
        ZW[key] = (src, S.zerlege(src, beschreibung(haus)['regeln']))
    return ZW[key][1]


def spender(haus):
    """Jedes Foto der Website: Schlüssel → Quelltext eines <img>, das es zeigt (das grösste Vorkommen gewinnt)."""
    key = ('spender', haus)
    if key not in ZW:
        aus, gross = {}, {}
        for n in seiten(haus):
            z = zer(haus, n)
            for f in z['fotos']:
                if f.get('zu'):
                    continue
                w = int(f['attrs'].get('width') or 0) if str(f['attrs'].get('width') or '').isdigit() else 0
                if f['b'] not in aus or w > gross[f['b']]:
                    aus[f['b']], gross[f['b']] = grundlage(haus, n)[f['s']:f['se']], w
        aus.update(_spender_eigene(haus))   # eigene Fotos des Hauses (hochgeladen), wenn das Haus Hochladen eingeschaltet hat
        ZW[key] = aus
    return ZW[key]


def seitenname(haus, datei):
    """Der Name einer Seite, gelesen aus dem Menü der Website (sonst aus ihrer Überschrift, sonst aus dem Titel)."""
    key = ('namen', haus)
    if key not in ZW:
        namen = {}
        for n in seiten(haus):
            for ln in zer(haus, n)['links']:
                ziel = ln['href'].split('#')[0].split('?')[0]
                if ziel in seiten(haus) and ziel not in namen and ln['t'] and len(ln['t']) < 40 and ln['blk'] and _oben(ln['blk'])['tag'] in ('nav', 'header'):
                    namen[ziel] = ln['t']
        for n in seiten(haus):
            if n not in namen:
                z = zer(haus, n)
                h1 = next((t['t'] for t in z['texte'] if t['tag'] == 'h1'), '')
                titel = re.search(r'<title>(.*?)</title>', grundlage(haus, n), re.S)
                kurz = re.split(r'\s[·|–—]\s', S.klar(titel.group(1)))[0] if titel else ''
                namen[n] = (kurz or h1 or n)[:60]
        start = next((s['datei'] for s in beschreibung(haus)['seiten'] if s.get('start')), 'index.html')
        if start in namen:
            namen[start] = 'Startseite'
        ZW[key] = namen
    return ZW[key].get(datei, datei)


def _oben(blk):
    while blk.get('eltern'):
        blk = blk['eltern']
    return blk


def website_bereiche(haus):
    """Die Website, Bereich für Bereich (wie im ersten Le Bureau, siehe STAND.md): je Bereich Name, Satz, Seiten, ein Foto.
    Steht in der Beschreibung nichts dazu, ist jede Hauptseite ein Bereich mit ihren Unterseiten; Name aus dem Menü,
    Satz aus den Überschriften der Seite, Foto das erste grosse der Seite."""
    b = beschreibung(haus)
    alle = seiten(haus)
    liste = b.get('website')
    if not liste:
        liste = [{'key': s['datei'].rsplit('.', 1)[0], 'seiten': [s['datei']] + [x['datei'] for x in b['seiten'] if x.get('unter') == s['datei']]} for s in b['seiten'] if not s.get('unter')]
    aus = []
    for w in liste:
        dateien = []
        for m in w['seiten']:
            dateien += [n for n in _seiten_von(haus, m) if n not in dateien]
        if not dateien:
            continue
        erste = dateien[0]
        satz = w.get('satz')
        if not satz:
            titel = [g['titel'] for g in verzeichnis_roh(haus, erste)['gruppen'] if g['h'] and not g['fest'] and g['titel'] and len(g['titel']) < 48][:5]
            satz = ('Auf dieser Seite: ' + ', '.join(t.rstrip('.') for t in titel) + '.') if titel else ''
        foto = w.get('foto')
        if not foto or foto not in spender(haus):
            foto = next((f['b'] for f in zer(haus, erste)['fotos'] if not f.get('zu') and str(f['attrs'].get('width') or '').isdigit() and int(f['attrs']['width']) >= 800), '')
        aus.append({'key': w['key'], 'name': w.get('name') or seitenname(haus, erste), 'satz': satz, 'foto': kurz_bild(haus, foto) if foto else '', 'foto_gross': gross_bild(haus, foto) if foto else '',
                    'seiten': [{'datei': n, 'name': seitenname(haus, n)} for n in dateien]})
    return aus


def haus_info(haus):
    b = beschreibung(haus)
    probe(haus)
    fotos_verteilen(haus)
    kleid = {}
    for k in ('zeichen', 'tapete'):   # Zeichen und Tapete gehören dem Haus: sie kommen aus seinen eigenen Dateien, nie aus dem Werkzeug
        rel = (b.get('kleid') or {}).get(k)
        if rel and not rel.startswith(('/', '.')) and (A.probe_ordner() / haus / 'grundlage' / rel).is_file():
            kleid[k] = probe_adresse(haus, 'grundlage') + rel
    kleid['zeichen_art'] = (b.get('kleid') or {}).get('zeichen_art') or 'bild'
    kleid['tapete_breite'] = int((b.get('kleid') or {}).get('tapete_breite') or 340)
    foto = (b.get('kleid') or {}).get('foto')   # Aussenfoto des Hauses für das Startbild der Übersicht (Name eines Fotos der Website)
    if foto and foto in spender(haus):
        kleid['foto'] = gross_bild(haus, foto)
    kleid['stil'] = []   # Kleid des Hauses: Farben und Schriften (haeuser/<haus>/kleid.css im Stamm, für alle Werkzeuge) und die Anordnung dieses Werkzeugs (haeuser/<haus>.css hier)
    for p, adr in ((WURZEL / 'haeuser' / haus / 'kleid.css', f'/haeuser/{haus}/kleid.css'), (HIER / 'haeuser' / f'{haus}.css', f'/werkzeuge/{WERKZEUG}/haeuser/{haus}.css')):
        if p.is_file():
            kleid['stil'].append(f'{adr}?v={int(p.stat().st_mtime)}')
    bereiche = []
    for k, d in (b.get('bereiche') or {}).items():
        if d.get('an') is False:
            continue
        std = BEREICHE.get(k, (k, ''))
        bereiche.append({'key': k, 'name': d.get('name') or std[0], 'satz': d.get('satz') or std[1]})
    return {'haus': haus, 'name': b['stamm'].get('name') or haus, 'welt': b['stamm'].get('welt'), 'version': VERSION,
            'sprachen': [{'code': x['code'], 'name': x.get('name') or x['code']} for x in sprachen(haus)],
            'seiten': [{'datei': s['datei'], 'name': seitenname(haus, s['datei']), 'unter': s.get('unter') or ''} for s in b['seiten']],
            'bereiche': bereiche, 'website': website_bereiche(haus), 'kleid': kleid, 'zahlen': (b.get('zahlen') or {}).get('an', True), 'hinweis': (b.get('hinweis') or {}).get('an', True),
            'karten': any(g.get('werkzeug') == 'karten' for g in b.get('gesperrt') or []),
            'angaben': bool(b.get('angaben')), 'google': bool((b.get('google') or {}).get('an')), 'hochladen': bool((b.get('hochladen') or {}).get('an')),
            'anleitung': b.get('anleitung') or '', 'funktionen': b.get('funktionen') or [],
            'online': probe_adresse(haus, 'online')}


# ------------------------------------------------------------------ Stand und Schicht
def schicht(d):
    c = S.leer()
    if isinstance(d, dict):
        for k in c:
            if type(d.get(k)) is type(c[k]):
                c[k] = d[k]
    return c


def stand_roh(haus, speicher):
    beschreibung(haus)
    s = speicher.lesen(haus, WERKZEUG)
    if s['live'] is None:   # erster Besuch: die Website gilt, wie das Haus sie gebaut hat
        s = speicher.grundstand_setzen(haus, WERKZEUG, S.leer(), 'werkzeug')
    return s


def arbeits(s):
    return schicht(s['entwurf'] if s['entwurf'] is not None else s['live'])


def _stelle(z, h, n):
    return next((t for t in z['texte'] if t['h'] == h and t['n'] == n), None)


def _html(src, st):
    return src[st['s']:st['e']]


def _kontext(haus, datei, st):
    """Wo eine Stelle steht: Abschnitt, Überschrift darüber, Wort davor, und das wievielte Mal der Text dort vorkommt.
    Zwei Stellen mit gleichem Text sind nur dann «dieselbe Angabe», wenn all das gleich ist
    (18.00 – 21.30 im einen Restaurant ist nicht 18.00 – 21.30 im anderen, CHF 20 fürs Parken nicht CHF 20 für den Hund)."""
    v = verzeichnis_roh(haus, datei)
    return v['kontext'].get((st['h'], st['n']), ('', '', '', 0))


def verzeichnis_roh(haus, datei):
    key = ('zer', haus, datei, '#verz')
    src = grundlage(haus, datei)
    if ZW.get(key, (None,))[0] is src:
        return ZW[key][1]
    z = zer(haus, datei)
    gruppen, wo, kontext = [], {}, {}

    def kopf(blk):
        if blk.get('fest'):
            return FEST_NAME[blk['tag']]
        innen = src[blk['se']:blk['es']]
        m = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', innen, re.S)
        gesagt = re.search(r'<h[1-4][^>]*\saria-label="([^"]+)"', innen)   # Überschriften aus einzelnen Buchstaben nennen ihren Text hier
        return (_unesc(gesagt.group(1)) if gesagt else S.klar(m.group(1)) if m else blk['t'])[:80]

    def gruppe(blk):
        oben = _oben(blk) if blk else None
        k = (oben['h'], oben['n']) if oben else ('', 0)
        if k not in wo:
            wo[k] = len(gruppen)
            gruppen.append({'h': k[0], 'n': k[1], 'titel': kopf(oben) if oben else 'Weitere Texte', 'tag': oben['tag'] if oben else '', 'fest': bool(oben and oben.get('fest')),
                            'zu': (oben or {}).get('zu') or '', 'stellen': [], 'fotos': []})
        return gruppen[wo[k]]
    mal = {}
    for t in z['texte']:
        g = gruppe(t['blk'])
        ruhig = [x for x in reversed(g['stellen']) if not re.search(ZAHL, x['t']) and len(x['t']) < 90]
        vor = ruhig[0]['t'] if ruhig else ''
        ober = next((x['t'] for x in ruhig if x['tag'] in OBER), '')   # die Überschrift darüber: «La Petite Suisse» über «Abend»
        k = mal[(id(g), t['h'])] = mal.get((id(g), t['h']), -1) + 1     # das wievielte Mal dieser Text in diesem Abschnitt steht
        kontext[(t['h'], t['n'])] = (g['titel'] if not g['fest'] else g['tag'], ober, vor, k)
        g['stellen'].append({'h': t['h'], 'n': t['n'], 'tag': t['tag'], 't': t['t'], 'zu': t.get('zu') or '', 'vor': vor[:70], 'ober': ober[:70] if ober != vor else ''})
    for f in z['fotos']:
        gruppe(f['blk'])['fotos'].append({'b': f['b'], 'n': f['n'], 'alt': f['alt'], 'zu': f.get('zu') or ''})
    gruppen = [g for g in gruppen if g['stellen'] or g['fotos']]
    gruppen.sort(key=lambda g: not g['h'])   # Texte ohne eigenen Abschnitt ans Ende
    haeufig = {}
    for t in z['texte']:
        haeufig[t['h']] = haeufig.get(t['h'], 0) + 1
    v = {'gruppen': gruppen, 'kontext': kontext, 'mal': haeufig}
    ZW[key] = (src, v)
    return v


def gleiche(haus, datei, st):
    """Alle Stellen der Website mit demselben Text unter derselben Überschrift und nach demselben Wort (zum Beispiel im Fuss jeder Seite)."""
    kx = _kontext(haus, datei, st)
    aus = []
    for n in seiten(haus):
        v = verzeichnis_roh(haus, n)
        for (h, nr), k in v['kontext'].items():
            if h == st['h'] and k == kx and not (_stelle(zer(haus, n), h, nr) or {}).get('zu'):
                aus.append({'seite': n, 'n': nr})
    return aus


def _regel(c, art, seite, a, n):
    feld = {'texte': 'h', 'bilder': 'b', 'links': 'h', 'aus': 'h', 'seo': 'h'}[art]
    return next((x for x in c.get(art) or [] if x.get('seite') == seite and x.get(feld) == a and int(x.get('n') or 0) == n), None)


def gross_bild(haus, b, breite=1200):
    """Adresse der Fassung eines Fotos, die der Breite am nächsten kommt (aus dem srcset), sonst die Quelle."""
    tag = spender(haus).get(b)
    if not tag:
        return ''
    fass = [x.strip().split(' ') for x in (S._roh_attr(tag, 'data-srcset') or S._roh_attr(tag, 'srcset') or '').split(',') if x.strip()]
    fass = [(int(x[1].rstrip('w')), x[0]) for x in fass if len(x) > 1 and x[1].rstrip('w').isdigit()]
    return min(fass, key=lambda x: abs(x[0] - breite))[1] if fass else (S._roh_attr(tag, 'data-src') or S._roh_attr(tag, 'src') or '')


def _klein_hier(haus, datei, b, n):
    """Kleinste Fassung eines Fotos, gelesen aus seinem <img> auf dieser Seite: für Fotos, die nicht zur Wahl stehen (gesperrte Karten), damit die Liste
    nie ein leeres Bild mit der Adresse des Ordners anfragt (22.10.2026, Demo-Check: 813 leere Vorschaubilder in «Wein & Bar»)."""
    x = next((f for f in zer(haus, datei)['fotos'] if f['b'] == b and f['n'] == n), None)
    if not x:
        return ''
    a = x['attrs']
    satz = a.get('data-srcset') or a.get('srcset') or ''
    return (satz.split(',')[0].strip().split(' ')[0] if satz else (a.get('data-src') or a.get('src') or '')).strip()


def kurz_bild(haus, b):
    """Adresse eines kleinen Abbilds eines Fotos, gelesen aus seinem <img> (kleinste Fassung im srcset, sonst die Quelle)."""
    tag = spender(haus).get(b)
    if not tag:
        return ''
    for name in ('data-srcset', 'srcset'):
        roh = S._roh_attr(tag, name)
        if roh:
            return roh.split(',')[0].strip().split(' ')[0]
    return S._roh_attr(tag, 'data-src') or S._roh_attr(tag, 'src') or ''


# ------------------------------------------------------------------ Was offen ist: jede Änderung mit vorher und nachher
def aenderungen(haus, c, s):
    """Was in c anders ist als in s. Jede Änderung hat einen Schlüssel, der in Vorschau, Liste und Sprachen derselbe ist."""
    aus = []
    codes = [x['code'] for x in sprachen(haus)]

    def paar(art, feld):
        a = {(x['seite'], x[feld], int(x.get('n') or 0)): x for x in s[art]}
        b = {(x['seite'], x[feld], int(x.get('n') or 0)): x for x in c[art]}
        return [(k, a.get(k), b.get(k)) for k in dict.fromkeys(list(a) + list(b)) if a.get(k) != b.get(k)]
    for k, a, b in paar('texte', 'h'):
        x = b or a
        e = {'key': S.schluessel('text', *k), 'art': 'text', 'seite': k[0], 'h': k[1], 'n': k[2], 'wo': seitenname(haus, k[0]), 'was': 'Text',
             'vorher': S.klar(a['neu']) if a else x.get('alt', ''), 'nachher': S.klar(b['neu']) if b else x.get('alt', ''), 'zurueck': not b}
        nur = bool(b and b.get('nur_sprachen'))
        if nur:
            e['was'], e['nur'] = 'Übersetzung', True
            e['nachher'] = ' · '.join(f'{sp}: {S.klar(w)}' for sp, w in (b.get('sprachen') or {}).items())
        if b and codes:   # «fehlt» zählt nur, wo es auf der Seite der Sprache ein Gegenstück gibt und sich das Deutsche geändert hat
            st = _stelle(zer(haus, k[0]), k[1], k[2])
            e['sprachen'] = {sp: nur or bool(str((b.get('sprachen') or {}).get(sp) or '').strip()) for sp in codes if st and _gegenstueck(haus, k[0], sp, 'texte', st)}
        aus.append(e)
    for k, a, b in paar('bilder', 'b'):
        x = b or a
        aus.append({'key': S.schluessel('bild', *k), 'art': 'bild', 'seite': k[0], 'b': k[1], 'n': k[2], 'wo': seitenname(haus, k[0]), 'was': 'Foto',
                    'vorher': (a or {}).get('neu') or k[1], 'nachher': (b or {}).get('neu') or k[1], 'vorher_bild': kurz_bild(haus, (a or {}).get('neu') or k[1]),
                    'nachher_bild': kurz_bild(haus, (b or {}).get('neu') or k[1]), 'alt': (b or {}).get('alt') or x.get('alt_alt', ''), 'zurueck': not b})
    for k, a, b in paar('links', 'h'):
        x = b or a
        aus.append({'key': S.schluessel('link', *k), 'art': 'link', 'seite': k[0], 'h': k[1], 'n': k[2], 'wo': seitenname(haus, k[0]), 'was': 'Link «' + x.get('t', '') + '»',
                    'vorher': a['neu'] if a else x.get('alt', ''), 'nachher': b['neu'] if b else x.get('alt', ''), 'zurueck': not b})
    for k, a, b in paar('aus', 'h'):
        x = b or a
        aus.append({'key': S.schluessel('aus', *k), 'art': 'aus', 'seite': k[0], 'h': k[1], 'n': k[2], 'wo': seitenname(haus, k[0]),
                    'was': 'Abschnitt ausgeblendet' if b else 'Abschnitt wieder gezeigt', 'vorher': x.get('t', '') if b else '', 'nachher': '' if b else x.get('t', ''), 'zurueck': not b})
    a_seo = {x['seite']: x for x in s.get('seo') or []}
    b_seo = {x['seite']: x for x in c.get('seo') or []}
    for seite in dict.fromkeys(list(a_seo) + list(b_seo)):
        a, b = a_seo.get(seite), b_seo.get(seite)
        if a == b:
            continue
        x = b or a
        alt = ' · '.join(t for t in (x.get('alt_titel', ''), x.get('alt_beschreibung', '')) if t)
        aus.append({'key': S.schluessel('seo', seite, 'kopf', 0), 'art': 'seo', 'seite': seite, 'h': 'kopf', 'n': 0, 'wo': seitenname(haus, seite), 'was': 'Google-Texte',
                    'vorher': ' · '.join(t for t in ((a or {}).get('titel', ''), (a or {}).get('beschreibung', '')) if t) or alt,
                    'nachher': ' · '.join(t for t in ((b or {}).get('titel', ''), (b or {}).get('beschreibung', '')) if t) or alt, 'zurueck': not b})
    if (s.get('hinweis') or {}) != (c.get('hinweis') or {}):
        a, b = s.get('hinweis') or {}, c.get('hinweis') or {}
        e = {'key': 'hinweis', 'art': 'hinweis', 'seite': '', 'wo': 'Alle Seiten', 'was': 'Hinweis für Gäste', 'vorher': a.get('text', '') if a.get('an') else '',
             'nachher': b.get('text', '') if b.get('an') else '', 'zurueck': False}
        if b.get('an') and codes:
            e['sprachen'] = {sp: bool(str(((b.get('sprachen') or {}).get(sp) or {}).get('text') or '').strip()) for sp in codes}
        aus.append(e)
    return aus


def stand(haus, speicher):
    s = stand_roh(haus, speicher)
    live, c = schicht(s['live']), arbeits(s)
    ae = aenderungen(haus, c, live) if s['offen'] else []
    zuletzt = next((z for z in speicher.protokoll(haus, WERKZEUG, 200) if z.get('was') == 'veroeffentlicht'), None)
    return {'kennung': s['kennung_entwurf'] or s['kennung_live'], 'kennung_live': s['kennung_live'], 'offen': s['offen'], 'aenderungen': ae, 'zuletzt': zuletzt,
            'fehlt': sum(1 for a in ae for ok in (a.get('sprachen') or {}).values() if not ok), 'daten': c}


# ------------------------------------------------------------------ Verzeichnis, Stelle, Foto
def verzeichnis(haus, datei, c):
    v = verzeichnis_roh(haus, datei)
    gruppen = []
    for g in v['gruppen']:
        ng = {k: g[k] for k in ('h', 'n', 'titel', 'tag', 'fest', 'zu')}
        ng['aus'] = bool(_regel(c, 'aus', datei, g['h'], g['n'])) if g['h'] else False
        ng['stellen'] = []
        for st in g['stellen']:
            r = _regel(c, 'texte', datei, st['h'], st['n'])
            st = dict(st, gleich=v['mal'].get(st['h'], 1))
            ng['stellen'].append(dict(st, neu=S.klar(r['neu']), nur=bool(r.get('nur_sprachen'))) if r else st)
        ng['fotos'] = []
        for f in g['fotos']:
            r = _regel(c, 'bilder', datei, f['b'], f['n'])
            ng['fotos'].append(dict(f, klein=kurz_bild(haus, (r or {}).get('neu') or f['b']) or _klein_hier(haus, datei, f['b'], f['n']), neu=bool(r)))
        gruppen.append(ng)
    return {'seite': datei, 'name': seitenname(haus, datei), 'gruppen': gruppen,
            'ausgeblendet': [{'h': a['h'], 'n': int(a.get('n') or 0), 't': a.get('t', '')} for a in c['aus'] if a.get('seite') == datei]}


def _gegenstueck(haus, datei, sp, art, d):
    zs = zer(haus, datei, sp)
    if zs is None:
        return None
    x = next((t for t in zs[art] if t['pfad'] == d['pfad']), None)
    return x if x and x.get('tag') == d.get('tag') else None


def stelle(haus, datei, h, n, c, live):
    z = zer(haus, datei)
    st = _stelle(z, h, n)
    if st is None:
        raise Fehler(404, 'stelle-fehlt', 'Diese Stelle gibt es auf der Seite nicht mehr.')
    src = grundlage(haus, datei)
    r, rl = _regel(c, 'texte', datei, h, n), _regel(live, 'texte', datei, h, n)
    original = _html(src, st)
    kx = _kontext(haus, datei, st)
    sp_aus = []
    for x in sprachen(haus):
        g = _gegenstueck(haus, datei, x['code'], 'texte', st)
        quelle = grundlage(haus, datei, x['code'])
        sp_aus.append({'code': x['code'], 'name': x.get('name') or x['code'], 'bisher': S.klar(_html(quelle, g)) if g else '', 'bisher_html': _html(quelle, g) if g else '',
                       'wert': ((r or {}).get('sprachen') or {}).get(x['code'], ''), 'da': g is not None, 'seite_da': quelle is not None})
    return {'seite': datei, 'seite_name': seitenname(haus, datei), 'h': h, 'n': n, 'tag': st['tag'], 'art': st['art'], 'zu': st.get('zu') or '',
            'original': original, 'original_text': st['t'], 'wert': r['neu'] if r else original, 'stand': rl['neu'] if rl else original,
            'geaendert': bool(r), 'nur': bool(r and r.get('nur_sprachen')), 'abschnitt': FEST_NAME.get(kx[0], kx[0]), 'ober': kx[1] if kx[1] != kx[2] else '', 'vor': kx[2], 'zahl': bool(re.search(ZAHL, st['t'])), 'gleiche': gleiche(haus, datei, st), 'sprachen': sp_aus,
            'bloecke': _ahnen(st['blk'], c, datei)}


def _ahnen(blk, c, datei):
    aus = []
    while blk:
        if not blk.get('fest') and not blk.get('zu'):
            aus.append({'h': blk['h'], 'n': blk['n'], 'tag': blk['tag'], 't': blk['t'][:90], 'aus': bool(_regel(c, 'aus', datei, blk['h'], blk['n']))})
        blk = blk.get('eltern')
    return aus


def foto(haus, datei, b, n, c):
    z = zer(haus, datei)
    f = next((x for x in z['fotos'] if x['b'] == b and x['n'] == n), None)
    if f is None:
        raise Fehler(404, 'stelle-fehlt', 'Dieses Foto gibt es auf der Seite nicht mehr.')
    r = _regel(c, 'bilder', datei, b, n)
    sp_aus = []
    for x in sprachen(haus):
        zs = zer(haus, datei, x['code'])
        g = next((t for t in zs['fotos'] if t['pfad'] == f['pfad']), None) if zs else None
        sp_aus.append({'code': x['code'], 'name': x.get('name') or x['code'], 'bisher': g['alt'] if g else '', 'wert': ((r or {}).get('alt_sprachen') or {}).get(x['code'], ''), 'da': g is not None})
    jetzt = (r or {}).get('neu') or b
    return {'seite': datei, 'seite_name': seitenname(haus, datei), 'b': b, 'n': n, 'zu': f.get('zu') or '', 'original': b, 'wert': jetzt, 'klein': kurz_bild(haus, jetzt),
            'klein_original': kurz_bild(haus, b), 'alt_original': f['alt'], 'alt': (r or {}).get('alt') or f['alt'], 'geaendert': bool(r), 'sprachen': sp_aus,
            'bloecke': _ahnen(f['blk'], c, datei)}


def fotos(haus):
    aus = []
    eigen = set(_spender_eigene(haus))
    for b, tag in sorted(spender(haus).items(), key=lambda x: x[0] not in eigen):   # eigene Fotos zuerst
        w, h = S._roh_attr(tag, 'width'), S._roh_attr(tag, 'height')
        aus.append({'b': b, 'klein': kurz_bild(haus, b), 'alt': _unesc(S._roh_attr(tag, 'alt') or ''), 'w': int(w) if (w or '').isdigit() else 0, 'h': int(h) if (h or '').isdigit() else 0,
                    'eigen': b in eigen})
    return {'basis': probe_adresse(haus, 'grundlage'), 'fotos': aus}


def _unesc(s):
    import html
    return html.unescape(s)


# ------------------------------------------------------------------ Vorschau einer Seite
VORSCHAU = r'''<style>
[data-ws-e]{cursor:text}
.ws-an [data-ws-e]:hover{outline:1px dashed var(--ws-a,currentColor)!important;outline-offset:3px}
.ws-an img[data-ws-b]:hover{outline:2px dashed var(--ws-a,currentColor)!important;outline-offset:-2px;cursor:pointer}
.ws-an [data-ws-zu]:hover{outline-style:dotted!important;cursor:not-allowed}
[data-ws-e].ws-wahl,[data-ws-b].ws-wahl{outline:2px solid var(--ws-a,currentColor)!important;outline-offset:3px}
.ws-vgl [data-ws-neu]{outline:3px solid var(--ws-p,currentColor)!important;outline-offset:3px}
[data-ws-blk].ws-blk{outline:2px dashed var(--ws-p,currentColor)!important;outline-offset:4px}
</style>
<script>
(function(){var P=window.parent;if(P===window)return;var M=document.currentScript.getAttribute('data-modus');
document.documentElement.classList.add(M==='vgl'?'ws-vgl':'ws-an');
function nah(e,s){while(e&&e.nodeType===1){if(e.matches(s))return e;e=e.parentElement}return null}
document.addEventListener('click',function(ev){var z=ev.target.nodeType===1?ev.target:ev.target.parentElement;
 var a=nah(z,'a[href]'),b=nah(z,'img[data-ws-b]'),t=nah(z,'[data-ws-e]'),zu=nah(z,'[data-ws-zu]');
 ev.preventDefault();ev.stopPropagation();
 if(M==='vgl')return;
 if(zu&&(t||b)){P.postMessage({ws:'zu',werkzeug:zu.getAttribute('data-ws-zu')},'*');return}
 if(t){P.postMessage({ws:'text',h:t.getAttribute('data-ws-e'),n:+t.getAttribute('data-ws-n')},'*');return}
 if(b){P.postMessage({ws:'bild',b:b.getAttribute('data-ws-b'),n:+b.getAttribute('data-ws-bn')},'*');return}
 if(a){var h=a.getAttribute('href')||'';if(/^[\w\-]+\.html(#.*)?$/.test(h))P.postMessage({ws:'gehe',seite:h.split('#')[0]},'*')}
},true);
document.addEventListener('submit',function(ev){ev.preventDefault()},true);
function finde(d){return document.querySelector(d.b?'[data-ws-b="'+d.b+'"][data-ws-bn="'+d.n+'"]':d.blk?'[data-ws-blk="'+d.blk+'"][data-ws-bln="'+d.n+'"]':'[data-ws-e="'+d.h+'"][data-ws-n="'+d.n+'"]')}
window.addEventListener('message',function(ev){var d=ev.data||{};
 if(d.ws==='farben'){document.documentElement.style.setProperty('--ws-a',d.a);document.documentElement.style.setProperty('--ws-p',d.p)}
 if(d.ws==='zeige'){[].forEach.call(document.querySelectorAll('.ws-wahl,.ws-blk'),function(x){x.classList.remove('ws-wahl','ws-blk')});
  var el=finde(d);if(el){el.classList.add(d.blk?'ws-blk':'ws-wahl');if(!d.still){var r=el.getBoundingClientRect();window.scrollTo(0,Math.max(0,r.top+window.scrollY-(window.innerHeight-Math.min(r.height,window.innerHeight))/2))}}
  P.postMessage({ws:'gezeigt',da:!!el,key:d.key||''},'*')}
 if(d.ws==='tippe'){var e2=finde(d);if(e2)e2.innerHTML=d.html}
 if(d.ws==='oben'){window.scrollTo(0,d.y||0)}
});
function fertig(){P.postMessage({ws:'geladen',titel:document.title,neu:document.querySelectorAll('[data-ws-neu]').length},'*')}
if(document.readyState!=='loading')fertig();else document.addEventListener('DOMContentLoaded',fertig);
})();
</script>'''
RUHIG_JS = ('<script>(function(){var m=window.matchMedia;window.matchMedia=function(q){if(/prefers-reduced-motion:\\s*reduce/.test(q))'
            'return{matches:true,media:q,onchange:null,addListener:function(){},removeListener:function(){},addEventListener:function(){},removeEventListener:function(){}};'
            'return m.call(window,q)}})()</script>')
_RUHIG_AN = re.compile(r'\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)')
_RUHIG_AUS = re.compile(r'\(\s*prefers-reduced-motion\s*:\s*no-preference\s*\)')


def _ruhig(css):
    """«Weniger Bewegung» gilt in der Vorschau immer: die Bedingung dafür wird zu «immer», ihr Gegenteil zu «nie»."""
    return _RUHIG_AUS.sub('(max-width:0)', _RUHIG_AN.sub('(min-width:0)', css))


def _ruhiges_css(haus, href, sp_ordner):
    """Ein Stylesheet der Seite für die Vorschau: die Regeln des Hauses für «weniger Bewegung» gelten immer, damit jede Stelle sofort dasteht.
    Die Website selbst bleibt unverändert; nichts wird geschrieben, das Stylesheet steht in der Vorschau direkt in der Seite."""
    rel = posixpath.normpath(posixpath.join(sp_ordner, href.split('?')[0])) if sp_ordner else href.split('?')[0]
    p = probe(haus) / 'grundlage' / rel
    if rel.startswith('..') or not p.is_file():
        return None
    key = ('css', str(p))
    zeit = p.stat().st_mtime
    if ZW.get(key, (None,))[0] != zeit:
        t = _ruhig(p.read_text(encoding='utf-8'))
        ordner = posixpath.dirname(rel)

        def adresse(m):
            u = m.group(2)
            if re.match(r'(data:|https?:|/|#)', u):
                return m.group(0)
            return f'url({m.group(1)}{probe_adresse(haus, "grundlage")}{posixpath.normpath(posixpath.join(ordner, u))}{m.group(1)})'
        ZW[key] = (zeit, re.sub(r'url\((["\']?)([^)"\']+)\1\)', adresse, t).replace('</style', '<\\/style'))
    return ZW[key][1]


_REL = r'(?!https?:|//|/|#|data:|blob:|mailto:|tel:|javascript:|about:)'
_ADR = re.compile(r'(<(?:img|script|source|video|audio|iframe|embed|track|input)\b[^>]*?\s(?:src|poster)=")' + _REL + r'([^"]+)"')
_ADR_LINK = re.compile(r'(<link\b[^>]*?\shref=")' + _REL + r'([^"]+)"')
_SATZ = re.compile(r'(<(?:img|source|link)\b[^>]*?\s(?:srcset|imagesrcset)=")([^"]+)"')


def _feste_adressen(html, basis):
    """Adressen, die der Browser schon beim Lesen der Seite vorab lädt (Bilder, Skripte, Stylesheets), bekommen in der Vorschau ihren ganzen Pfad.
    Sonst holt er sie einmal von der Adresse des Werkzeugs (404) und erst dann von der richtigen. Alles andere löst <base> auf."""
    def fest(u):
        return u if re.match(r'(https?:|//|/|#|data:|blob:)', u) else posixpath.normpath(posixpath.join(basis, u.split('?')[0])) + ('?' + u.split('?', 1)[1] if '?' in u else '')

    def satz(m):
        teile = []
        for t in m.group(2).split(','):
            w = t.strip().split(' ', 1)
            teile.append(' '.join([fest(w[0])] + w[1:]))
        return f'{m.group(1)}{", ".join(teile)}"'
    html = _ADR.sub(lambda m: f'{m.group(1)}{fest(m.group(2))}"', html)
    html = _ADR_LINK.sub(lambda m: f'{m.group(1)}{fest(m.group(2))}"', html)
    return _SATZ.sub(satz, html)


def vorschau(haus, zustand, sp, datei, s):
    if zustand not in ('entwurf', 'stand', 'vorher', 'nachher'):
        raise Fehler(404, 'weg-unbekannt', 'Diese Vorschau gibt es nicht.')
    sp = '' if sp in ('de', '') else sp
    b = beschreibung(haus)
    live, c = schicht(s['live']), arbeits(s)
    nur = {a['key'] for a in aenderungen(haus, c, live)} if zustand in ('vorher', 'nachher') else None
    wahl = live if zustand in ('stand', 'vorher') else c
    src = grundlage(haus, datei, sp)
    if src is None:
        raise Fehler(404, 'seite-fehlt', 'Diese Seite gibt es in dieser Sprache nicht.')
    if sp:
        html = S.anwenden_sprache(datei, src, grundlage(haus, datei), wahl, sp, marken=True, regeln=b['regeln'], spender=spender(haus), nur_neu=nur)
    else:
        html = S.anwenden(datei, src, wahl, marken=True, regeln=b['regeln'], spender=spender(haus), nur_neu=nur)
    ordner = _rel(haus, datei, sp).rpartition('/')[0]
    v = b.get('vorschau') or {}

    def stil(m):
        css = _ruhiges_css(haus, m.group(1), ordner)
        return m.group(0) if css is None else f'<style data-ws-von="{m.group(1).split("?")[0]}">{css}</style>'
    html = re.sub(r'<link\b[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>', stil, html)
    html = _ruhig(html)
    ohne = v.get('ohne_skripte') or []
    if ohne:
        html = re.sub(r'<script\b[^>]*\bsrc="([^"]+)"[^>]*></script>', lambda m: '' if any(o in m.group(1) for o in ohne) else m.group(0), html)
    basis = probe_adresse(haus, 'grundlage') + (ordner + '/' if ordner else '')
    html = _feste_adressen(html, basis)
    kopf = f'<base href="{basis}">{RUHIG_JS}' + (f'<style>{v["zusatz_css"]}</style>' if v.get('zusatz_css') else '')
    html = re.sub(r'<head\b[^>]*>', lambda m: m.group(0) + kopf, html, 1)
    skript = VORSCHAU.replace('<script>', f'<script data-modus="{"vgl" if nur is not None else "an"}">', 1)
    return {'html': html.replace('</body>', skript + '</body>', 1) if '</body>' in html else html + skript, 'seite': datei, 'sprache': sp or 'de', 'zustand': zustand,
            'marken': len(nur) if nur is not None else None}


# ------------------------------------------------------------------ Zeiten und Preise
def zahlen(haus, c):
    """Jede Textstelle mit einer Zeit, einem Preis oder einem Mass. Gleicher Text unter gleicher Überschrift und nach gleichem Wort
    (der Fuss jeder Seite) ist eine Zeile mit allen ihren Orten."""
    b = beschreibung(haus)
    muster = re.compile((b.get('zahlen') or {}).get('muster') or ZAHL)
    zeilen, wo = [], {}
    for n in seiten(haus):
        v = verzeichnis_roh(haus, n)
        for g in v['gruppen']:
            if g['zu']:
                continue
            for st in g['stellen']:
                if st['zu'] or not muster.search(st['t']) or len(st['t']) > 320:
                    continue
                kx = v['kontext'][(st['h'], st['n'])]
                k = (st['h'], kx)
                if k not in wo:
                    wo[k] = len(zeilen)
                    zeilen.append({'h': st['h'], 'abschnitt': g['titel'], 'fest': g['fest'], 'vor': st['vor'], 'ober': st['ober'], 't': st['t'], 'tag': st['tag'], 'orte': [],
                                   'seite': n, 'seite_name': seitenname(haus, n)})
                zeilen[wo[k]]['orte'].append({'seite': n, 'n': st['n']})
    for z in zeilen:
        werte = {S.klar(r['neu']) for o in z['orte'] for r in [_regel(c, 'texte', o['seite'], z['h'], o['n'])] if r}
        z['neu'] = next(iter(werte)) if len(werte) == 1 and all(_regel(c, 'texte', o['seite'], z['h'], o['n']) for o in z['orte']) else ''
        z['teils'] = bool(werte) and not z['neu']
    gruppen, gw = [], {}
    for z in zeilen:
        k = 'Auf jeder Seite' if (z['fest'] and len(z['orte']) > 1) else z['seite_name']
        if k not in gw:
            gw[k] = len(gruppen)
            gruppen.append({'name': k, 'zeilen': []})
        gruppen[gw[k]]['zeilen'].append(z)
    gruppen.sort(key=lambda g: g['name'] != 'Auf jeder Seite')
    return {'gruppen': gruppen, 'zahl': len(zeilen)}


# ------------------------------------------------------------------ Bereiche des Hauses (Zimmer, Säle, Packages …): Felder aus der Beschreibung
def _seiten_von(haus, muster):
    alle = seiten(haus)
    if muster.endswith('*'):
        return [n for n in alle if n.startswith(muster[:-1])]
    return [n for n in alle if n == muster]


def bereich(haus, key, c):
    b = beschreibung(haus)
    d = (b.get('bereiche') or {}).get(key)
    if not d or d.get('an') is False:
        raise Fehler(404, 'bereich-aus', 'Diesen Bereich hat das Haus nicht.')
    std = BEREICHE.get(key, (key, ''))
    eintraege, fehlt = [], []
    for q in d.get('quellen') or []:
        for n in _seiten_von(haus, q['seite']):
            z = zer(haus, n)
            src = grundlage(haus, n)
            knoten = S.waehle(z['baum'].wurzel, q['jedes'])
            if not knoten:
                fehlt.append(f'{n}: «{q["jedes"]}» trifft nichts')
            for k in knoten:
                e = {'seite': n, 'seite_name': seitenname(haus, n), 'felder': [], 'titel': '', 'aus': False, 'blk': None}
                blk = next((x for x in z['bloecke'] if x['k'] is k), None)
                if blk and not blk.get('fest') and not blk.get('zu'):
                    e['blk'] = {'h': blk['h'], 'n': blk['n']}
                    e['aus'] = bool(_regel(c, 'aus', n, blk['h'], blk['n']))
                for f in q['felder']:
                    ziel = [k] if not f.get('wo') else S.waehle(z['baum'].wurzel, f['wo'], k)
                    feld = {'key': f['key'], 'label': f['label'], 'art': f['art'], 'teile': []}
                    for el in ziel[:(60 if f['art'] in ('liste', 'bilder') else 1)]:
                        if f['art'] in ('bild', 'bilder'):
                            for x in [x for x in z['fotos'] if x['k'] is el or el['s'] <= x['s'] < (el.get('ee') or el['se'])][:(40 if f['art'] == 'bilder' else 1)]:
                                r = _regel(c, 'bilder', n, x['b'], x['n'])
                                feld['teile'].append({'b': x['b'], 'n': x['n'], 'klein': kurz_bild(haus, (r or {}).get('neu') or x['b']), 'alt': (r or {}).get('alt') or x['alt'], 'neu': bool(r), 'zu': x.get('zu') or ''})
                        elif f['art'] == 'link':
                            for x in [x for x in z['links'] if x['k'] is el or el['s'] <= x['s'] < (el.get('ee') or el['se'])][:1]:
                                r = _regel(c, 'links', n, x['h'], x['n'])
                                feld['teile'].append({'h': x['h'], 'n': x['n'], 't': x['t'], 'wert': r['neu'] if r else x['href'], 'original': x['href'], 'neu': bool(r), 'zu': x.get('zu') or ''})
                        else:
                            for x in S.stellen_in(z, el)[:(60 if f['art'] == 'liste' else 6)]:
                                r = _regel(c, 'texte', n, x['h'], x['n'])
                                feld['teile'].append({'h': x['h'], 'n': x['n'], 't': S.klar(r['neu']) if r else x['t'], 'original': x['t'], 'neu': bool(r), 'zu': x.get('zu') or ''})
                    if feld['teile']:
                        e['felder'].append(feld)
                        if 't' in feld['teile'][0] and (f.get('titel') or (not e['titel'] and f['art'] == 'text')):
                            e['titel'] = ' '.join(x['t'] for x in feld['teile'])[:120]
                    elif not f.get('kann_fehlen'):
                        fehlt.append(f'{n}: Feld «{f["label"]}» ({f.get("wo") or "Eintrag"}) nicht gefunden')
                if not e['felder']:
                    continue
                ersatz = (q.get('bild_ersatz') or {}).get(e['titel'])   # Foto derselben Person von einer anderen Seite, wenn hier keins steht (21.10.2026: Team ohne Fotos)
                if ersatz and not any(f['art'] in ('bild', 'bilder') and f['teile'] for f in e['felder']) and ersatz in spender(haus):
                    e['bild_ersatz'] = kurz_bild(haus, ersatz)
                if q.get('dazu'):   # dieselbe Sache an zweiter Stelle der Seite (z. B. grosse Ankündigung): ein Eintrag, Felder mit Vorsatz dazu
                    def _gl(a, b):   # dazu_gleich «anfang»: kurzer Titel im Kalender = langer Titel der Ankündigung (21.10.2026)
                        if q.get('dazu_gleich') != 'anfang':
                            return a == b
                        a, b = a.rstrip('. ').lower(), b.rstrip('. ').lower()
                        return bool(a and b) and (a.startswith(b) or b.startswith(a))
                    gleich = next((x for x in eintraege if x['seite'] == e['seite'] and x['titel'] and _gl(x['titel'], e['titel'])), None)
                    if gleich:
                        for feld in e['felder']:
                            feld['label'] = q['dazu'] + ' · ' + feld['label']
                        gleich['felder'] += e['felder']
                        continue
                eintraege.append(e)
    return {'key': key, 'name': d.get('name') or std[0], 'satz': d.get('satz') or std[1], 'eintraege': eintraege, 'fehlt': fehlt[:20]}


# ------------------------------------------------------------------ Sprachen: jede offene Änderung und ihre Übersetzungen
def sprachen_liste(haus, c, live):
    codes = sprachen(haus)
    aus = []
    for a in aenderungen(haus, c, live):
        if a['art'] == 'text' and not a['zurueck']:
            r = _regel(c, 'texte', a['seite'], a['h'], a['n'])
            st = _stelle(zer(haus, a['seite']), a['h'], a['n'])
            if not st:
                continue
            e = {'key': a['key'], 'art': 'text', 'wo': a['wo'], 'seite': a['seite'], 'h': a['h'], 'n': a['n'], 'vorher': r.get('alt', ''), 'nachher': S.klar(r['neu']), 'nur': bool(r.get('nur_sprachen')), 'sp': {}}
            for x in codes:
                quelle = grundlage(haus, a['seite'], x['code'])
                g = _gegenstueck(haus, a['seite'], x['code'], 'texte', st)
                e['sp'][x['code']] = {'bisher': S.klar(_html(quelle, g)) if g else '', 'wert': S.klar((r.get('sprachen') or {}).get(x['code'], '')), 'da': g is not None}
            aus.append(e)
        elif a['art'] == 'hinweis' and (c.get('hinweis') or {}).get('an'):
            h = c['hinweis']
            e = {'key': 'hinweis', 'art': 'hinweis', 'wo': 'Alle Seiten', 'vorher': a['vorher'], 'nachher': h.get('text', ''), 'sp': {}}
            for x in codes:
                e['sp'][x['code']] = {'bisher': '', 'wert': ((h.get('sprachen') or {}).get(x['code']) or {}).get('text', ''), 'da': True}
            aus.append(e)
    return {'sprachen': [{'code': x['code'], 'name': x.get('name') or x['code']} for x in codes], 'zeilen': aus}


# ------------------------------------------------------------------ Speichern in den Entwurf
# Anrede (29.10.2026): Häuser, die ihr Team duzen (Culinarium, Robert); alle anderen behalten «Sie» wie bisher (wie DU in website.js und pruefung.js)
DU_HAEUSER = {'culinarium'}


def _datum(t, haus=''):
    t = str(t or '').strip()
    if not t:
        return ''
    m = re.fullmatch(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', t)
    if m:
        t = f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}'
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', t):
        raise Fehler(422, 'datum', 'Ein Datum schreibst du so: 24.12.2026' if haus in DU_HAEUSER else 'Ein Datum schreiben Sie so: 24.12.2026')
    try:
        time.strptime(t, '%Y-%m-%d')
    except ValueError:
        raise Fehler(422, 'datum', 'Dieses Datum gibt es nicht.')
    return t


def _weg(c, art, seite, a, n):
    feld = {'texte': 'h', 'bilder': 'b', 'links': 'h', 'aus': 'h', 'seo': 'h'}[art]
    c[art] = [x for x in c.get(art) or [] if not (x.get('seite') == seite and x.get(feld) == a and int(x.get('n') or 0) == n)]


def _op(haus, c, live, op, quittung):
    art = op.get('art')
    seite = op.get('seite') or ''
    if art in ('text', 'bild', 'link', 'aus') and seite not in seiten(haus):
        raise Fehler(404, 'seite-unbekannt', 'Diese Seite gehört nicht zur Website.')
    codes = [x['code'] for x in sprachen(haus)]
    if art == 'text':
        z, src = zer(haus, seite), grundlage(haus, seite)
        orte = op.get('orte') or [{'seite': seite, 'n': int(op.get('n') or 0)}]
        erste = _stelle(z, op.get('h'), int(op.get('n') or 0))
        if erste is None:
            raise Fehler(404, 'stelle-fehlt', 'Diese Stelle gibt es auf der Seite nicht mehr. Bitte die Seite neu laden.')
        erlaubt = ({(o['seite'], o['n']) for o in gleiche(haus, seite, erste)} if op.get('orte') else set()) | {(seite, erste['n'])}   # eine Stelle allein braucht den Abgleich über alle Seiten nicht (21.10.2026: Angaben mit 40 Stellen in 1 s statt 20 s)
        for o in orte:
            if (o.get('seite'), int(o.get('n') or 0)) not in erlaubt:
                raise Fehler(422, 'stelle-fehlt', 'Eine der Stellen passt nicht zu dieser Angabe.')
            zz, ss = zer(haus, o['seite']), grundlage(haus, o['seite'])
            st = _stelle(zz, op['h'], int(o['n']))
            if st.get('zu'):
                raise Fehler(423, 'gesperrt', 'Diese Stelle pflegt ein anderes Werkzeug.', werkzeug=st['zu'])
            original = _html(ss, st)
            neu = S.sauber(op.get('neu', ''), S.klassen_in(original))
            if not S.klar(neu):
                raise Fehler(422, 'leer', 'Ein leerer Text bleibt als Lücke stehen. Zum Entfernen gibt es «Abschnitt ausblenden».')
            if len(neu) > 6000:
                raise Fehler(422, 'zu-lang', 'Dieser Text ist zu lang für eine Stelle.')
            vor = _regel(c, 'texte', o['seite'], st['h'], st['n'])
            ue = dict((vor or {}).get('sprachen') or {})
            for sp, w in (op.get('sprachen') or {}).items():
                if sp in codes:
                    w = S.sauber(w, S.klassen_in(original))
                    if S.klar(w):
                        ue[sp] = w
                    else:
                        ue.pop(sp, None)
            _weg(c, 'texte', o['seite'], st['h'], st['n'])
            gleich = S.klar(neu) == st['t'] and re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', '<>', neu)) == re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', '<>', S.sauber(original, S.klassen_in(original))))
            if not gleich:
                c['texte'].append({'seite': o['seite'], 'h': st['h'], 'n': st['n'], 'neu': neu, 'alt': st['t'], 'sprachen': ue})
            elif ue:   # nur eine Übersetzung geändert: das Deutsche bleibt Zeichen für Zeichen, wie es auf der Seite steht
                c['texte'].append({'seite': o['seite'], 'h': st['h'], 'n': st['n'], 'neu': original, 'alt': st['t'], 'sprachen': ue, 'nur_sprachen': True})
            rl = _regel(live, 'texte', o['seite'], st['h'], st['n'])
            quittung.append({'key': S.schluessel('text', o['seite'], st['h'], st['n']), 'wo': seitenname(haus, o['seite']), 'was': 'Text',
                             'vorher': S.klar(vor['neu']) if vor else st['t'], 'nachher': S.klar(neu), 'stand': S.klar(rl['neu']) if rl else st['t']})
    elif art == 'bild':
        z = zer(haus, seite)
        f = next((x for x in z['fotos'] if x['b'] == op.get('b') and x['n'] == int(op.get('n') or 0)), None)
        if f is None:
            raise Fehler(404, 'stelle-fehlt', 'Dieses Foto gibt es auf der Seite nicht mehr.')
        if f.get('zu'):
            raise Fehler(423, 'gesperrt', 'Dieses Foto pflegt ein anderes Werkzeug.', werkzeug=f['zu'])
        ziel = op.get('neu') or f['b']
        if ziel not in spender(haus):
            raise Fehler(422, 'foto-unbekannt', 'Dieses Foto gibt es auf der Website nicht.')
        alt = re.sub(r'\s+', ' ', str(op.get('alt') if op.get('alt') is not None else f['alt'])).strip()[:400]
        vor = _regel(c, 'bilder', seite, f['b'], f['n'])
        ue = dict((vor or {}).get('alt_sprachen') or {})
        for sp, w in (op.get('alt_sprachen') or {}).items():
            if sp in codes:
                w = re.sub(r'\s+', ' ', str(w)).strip()[:400]
                if w:
                    ue[sp] = w
                else:
                    ue.pop(sp, None)
        _weg(c, 'bilder', seite, f['b'], f['n'])
        if ziel != f['b'] or alt != f['alt']:
            c['bilder'].append({'seite': seite, 'b': f['b'], 'n': f['n'], 'neu': ziel, 'alt': alt, 'alt_alt': f['alt'], 'alt_sprachen': ue})
        quittung.append({'key': S.schluessel('bild', seite, f['b'], f['n']), 'wo': seitenname(haus, seite), 'was': 'Foto', 'vorher': (vor or {}).get('neu') or f['b'], 'nachher': ziel,
                         'vorher_bild': kurz_bild(haus, (vor or {}).get('neu') or f['b']), 'nachher_bild': kurz_bild(haus, ziel)})
    elif art == 'link':
        z = zer(haus, seite)
        x = next((x for x in z['links'] if x['h'] == op.get('h') and x['n'] == int(op.get('n') or 0)), None)
        if x is None:
            raise Fehler(404, 'stelle-fehlt', 'Diesen Link gibt es auf der Seite nicht mehr.')
        if x.get('zu'):
            raise Fehler(423, 'gesperrt', 'Diesen Link pflegt ein anderes Werkzeug.', werkzeug=x['zu'])
        ziel = str(op.get('neu') or '').strip()
        if not S.link_gut(ziel):
            raise Fehler(422, 'link', 'Eine Adresse beginnt mit https://, mailto: oder tel:, oder sie nennt eine Seite oder ein PDF der Website.')
        vor = _regel(c, 'links', seite, x['h'], x['n'])
        _weg(c, 'links', seite, x['h'], x['n'])
        if ziel != x['href']:
            c['links'].append({'seite': seite, 'h': x['h'], 'n': x['n'], 'neu': ziel, 'alt': x['href'], 't': x['t']})
        quittung.append({'key': S.schluessel('link', seite, x['h'], x['n']), 'wo': seitenname(haus, seite), 'was': 'Link «' + x['t'] + '»', 'vorher': vor['neu'] if vor else x['href'], 'nachher': ziel})
    elif art == 'aus':
        z = zer(haus, seite)
        blk = next((x for x in z['bloecke'] if x['h'] == op.get('h') and x['n'] == int(op.get('n') or 0)), None)
        if blk is None:
            raise Fehler(404, 'stelle-fehlt', 'Diesen Abschnitt gibt es auf der Seite nicht mehr.')
        if blk.get('fest') or blk.get('zu'):
            raise Fehler(423, 'gesperrt', 'Dieser Abschnitt lässt sich hier nicht ausblenden.', werkzeug=blk.get('zu') or '')
        war = bool(_regel(c, 'aus', seite, blk['h'], blk['n']))
        _weg(c, 'aus', seite, blk['h'], blk['n'])
        if op.get('an'):
            c['aus'].append({'seite': seite, 'h': blk['h'], 'n': blk['n'], 't': blk['t'][:120]})
        quittung.append({'key': S.schluessel('aus', seite, blk['h'], blk['n']), 'wo': seitenname(haus, seite), 'was': 'Abschnitt',
                         'vorher': 'ausgeblendet' if war else 'zu sehen', 'nachher': 'ausgeblendet' if op.get('an') else 'zu sehen'})
    elif art == 'hinweis':
        alt = c.get('hinweis') or {}
        text = re.sub(r'\s+', ' ', str(op.get('text') or '')).strip()[:300]
        link = str(op.get('link') or '').strip()
        if link and not S.link_gut(link):
            raise Fehler(422, 'link', 'Eine Adresse beginnt mit https://, mailto: oder tel:, oder sie nennt eine Seite oder ein PDF der Website.')
        von, bis = _datum(op.get('von'), haus), _datum(op.get('bis'), haus)
        if von and bis and von > bis:
            raise Fehler(422, 'datum', '«Bis» liegt vor «Von».')
        if op.get('an') and not text:
            raise Fehler(422, 'leer', 'Ein Hinweis ohne Text bleibt unsichtbar. Bitte einen Satz schreiben oder den Hinweis ausschalten.')
        ue = {}
        for sp in codes:
            w = (op.get('sprachen') or {}).get(sp) or {}
            e = {k: re.sub(r'\s+', ' ', str(w.get(k) or '')).strip()[:300] for k in ('text', 'linktext')}
            if e['text'] or e['linktext']:
                ue[sp] = e
        neu = {'an': bool(op.get('an')), 'text': text, 'von': von, 'bis': bis, 'link': link, 'linktext': re.sub(r'\s+', ' ', str(op.get('linktext') or '')).strip()[:60], 'sprachen': ue}
        c['hinweis'] = neu if (neu['an'] or text) else {}
        quittung.append({'key': 'hinweis', 'wo': 'Alle Seiten', 'was': 'Hinweis für Gäste', 'vorher': alt.get('text', '') if alt.get('an') else 'aus', 'nachher': text if neu['an'] else 'aus'})
    elif art == 'wort':
        sp, wert = op.get('sp'), op.get('wert', '')
        if sp not in codes:
            raise Fehler(404, 'sprache-unbekannt', 'Diese Sprache hat das Haus nicht.')
        if op.get('key') == 'hinweis':
            h = c.get('hinweis') or {}
            e = dict((h.get('sprachen') or {}).get(sp) or {})
            vor = e.get('text', '')
            e['text'] = re.sub(r'\s+', ' ', str(wert)).strip()[:300]
            h.setdefault('sprachen', {})[sp] = e
            c['hinweis'] = h
            quittung.append({'key': 'hinweis', 'wo': 'Hinweis für Gäste', 'was': f'Übersetzung {sp}', 'vorher': vor, 'nachher': e['text']})
        else:
            r = _regel(c, 'texte', seite, op.get('h'), int(op.get('n') or 0))
            if r is None:
                raise Fehler(404, 'stelle-fehlt', 'Zu dieser Übersetzung gibt es keine Änderung mehr.')
            w = S.sauber(wert, S.klassen_in(r['neu']))
            vor = S.klar((r.get('sprachen') or {}).get(sp, ''))
            r.setdefault('sprachen', {})
            if S.klar(w):
                r['sprachen'][sp] = w
            else:
                r['sprachen'].pop(sp, None)
            quittung.append({'key': S.schluessel('text', seite, r['h'], r['n']), 'wo': seitenname(haus, seite), 'was': f'Übersetzung {sp}', 'vorher': vor, 'nachher': S.klar(w)})
    elif art == 'weg':   # eine offene Änderung zurücknehmen: der veröffentlichte Stand dieser Stelle gilt wieder
        key = str(op.get('key') or '')
        if key == 'hinweis':
            c['hinweis'] = json.loads(json.dumps(live.get('hinweis') or {}))
            quittung.append({'key': key, 'wo': 'Alle Seiten', 'was': 'Hinweis für Gäste', 'vorher': 'geändert', 'nachher': 'wie veröffentlicht'})
        else:
            teile = key.split('|')
            if len(teile) != 4 or teile[0] not in ('text', 'bild', 'link', 'aus', 'seo'):
                raise Fehler(422, 'stelle-fehlt', 'Diese Änderung gibt es nicht.')
            feld = {'text': 'texte', 'bild': 'bilder', 'link': 'links', 'aus': 'aus', 'seo': 'seo'}[teile[0]]
            n = int(teile[3])
            alt = _regel(live, feld, teile[1], teile[2], n)
            _weg(c, feld, teile[1], teile[2], n)
            if alt:
                c[feld].append(json.loads(json.dumps(alt)))
            quittung.append({'key': key, 'wo': seitenname(haus, teile[1]), 'was': 'Änderung zurückgenommen', 'vorher': 'geändert', 'nachher': 'wie veröffentlicht'})
    elif art == 'seo':
        _op_seo(haus, c, live, op, quittung)
    elif art == 'angabe':
        _op_angabe(haus, c, live, op, quittung)
    else:
        raise Fehler(400, 'anfrage', 'Diese Art von Änderung kennt das Werkzeug nicht.')


def aendern(haus, d, speicher):
    ops = d.get('ops')
    if not isinstance(ops, list) or not ops or len(ops) > 400:
        raise Fehler(400, 'anfrage', 'Es fehlt, was geändert werden soll.')
    s = stand_roh(haus, speicher)
    jetzt = s['kennung_entwurf'] or s['kennung_live']
    if d.get('erwartet') != jetzt:
        raise speicher.Konflikt('Der Stand wurde inzwischen geändert')
    live, c = schicht(s['live']), arbeits(s)
    vorher = json.loads(json.dumps(c))
    quittung = []
    for op in ops:
        _op(haus, c, live, op, quittung)
    for k in ('texte', 'bilder', 'links', 'aus', 'seo'):
        c[k].sort(key=lambda x: (x.get('seite') or '', str(x.get('h') or x.get('b')), int(x.get('n') or 0)))
    if speicher.kennung(c) == speicher.kennung(vorher):
        return 200, {'nichts': True, 'meldung': 'Nichts geändert, nichts gespeichert.', 'stand': stand(haus, speicher)}
    speicher.entwurf_schreiben(haus, WERKZEUG, c, jetzt, d.get('wer', ''))
    return 200, {'nichts': False, 'quittung': quittung, 'vorher_daten': vorher, 'stand': stand(haus, speicher)}


# ------------------------------------------------------------------ Veröffentlichen: prüfen, Stand wechseln, Seiten schreiben
def soll(haus, c):
    """Jede Seite der Website (alle Sprachen), wie sie mit der Schicht c online stehen muss. Dazu: welche Regel keinen Platz fand."""
    b = beschreibung(haus)
    sp_liste = sprachen(haus)
    aus, benutzt, fehlt = {}, set(), {}
    for n in seiten(haus):
        src = grundlage(haus, n)
        aus[n] = S.anwenden(n, src, c, benutzt=benutzt, regeln=b['regeln'], spender=spender(haus))
        for x in sp_liste:
            q = grundlage(haus, n, x['code'])
            if q is None:
                continue
            f = set()
            aus[f"{x['ordner']}/{n}"] = S.anwenden_sprache(n, q, src, c, x['code'], regeln=b['regeln'], spender=spender(haus), fehlt=f)
            if f:
                fehlt.setdefault(x['code'], set()).update(f)
    ohne = []
    for art, feld in (('text', 'texte'), ('bild', 'bilder'), ('link', 'links'), ('aus', 'aus'), ('seo', 'seo')):
        for i, r in enumerate(c.get(feld) or []):
            if (art, i) not in benutzt:
                ohne.append({'art': art, 'seite': r.get('seite'), 'was': r.get('alt') or r.get('b') or r.get('t') or '', 'key': S.schluessel(art, r.get('seite'), r.get('h') or r.get('b'), int(r.get('n') or 0))})
    return aus, ohne, {k: len(v) for k, v in fehlt.items()}


def veroeffentlichen(haus, d, speicher):
    with A.sperre(haus):
        s = stand_roh(haus, speicher)
        if not s['offen']:
            raise Fehler(409, 'nichts-offen', 'Nichts geändert, nichts veröffentlicht.')
        if d.get('erwartet') and d['erwartet'] != s['kennung_entwurf']:
            raise speicher.Konflikt('Der Entwurf wurde inzwischen geändert')
        c = schicht(s['entwurf'])
        seiten_neu, ohne, fehlt = soll(haus, c)
        if ohne:
            raise Fehler(422, 'stelle-fehlt', f'{len(ohne)} Änderung(en) finden ihre Stelle auf der Website nicht mehr. Nichts wurde veröffentlicht.', ohne=ohne)
        n_aend = len(aenderungen(haus, c, schicht(s['live'])))
        speicher.veroeffentlichen(haus, WERKZEUG, d.get('wer', ''), str(d.get('notiz') or '')[:300])
        try:
            geschrieben = A.schreibe(haus, {k: v.encode('utf-8') for k, v in seiten_neu.items()})
        except OSError as e:
            raise Fehler(500, 'ausgabe', f'Der Stand ist veröffentlicht, aber nicht jede Seite liess sich schreiben ({e}). In der Prüfung: «Seiten neu ausgeben».')
    return 200, {'geschrieben': geschrieben, 'aenderungen': n_aend, 'fehlt': fehlt, 'online': probe_adresse(haus, 'online'), 'stand': stand(haus, speicher)}


def verlauf(haus, speicher):
    s = stand_roh(haus, speicher)
    live = schicht(s['live'])
    aus = []
    for v in speicher.verlauf(haus, WERKZEUG):
        f = speicher.fassung_lesen(haus, WERKZEUG, v['fassung'])
        aus.append(dict(v, unterschiede=len(aenderungen(haus, schicht(f['daten']), live)), ursprung=False))
    if aus and S.ist_leer(schicht(speicher.fassung_lesen(haus, WERKZEUG, aus[-1]['fassung'])['daten'])):
        aus[-1]['ursprung'] = True   # R14: die älteste Fassung ist die Website, wie sie gebaut ist, und steht unten (neueste oben, wie der Speicher sie liefert)
    return {'verlauf': aus, 'protokoll': speicher.protokoll(haus, WERKZEUG)[:30]}


def fassung(haus, name, speicher):
    s = stand_roh(haus, speicher)
    f = speicher.fassung_lesen(haus, WERKZEUG, name)
    return {'fassung': name, 'abgeloest': f.get('abgeloest'), 'wer': f.get('wer'), 'notiz': f.get('notiz'),
            'aenderungen': aenderungen(haus, schicht(f['daten']), schicht(s['live']))}


# ------------------------------------------------------------------ Prüfung von der Seite des Servers
def pruefung(haus, speicher):
    punkte = []

    def punkt(pid, titel, gut, text, lex=''):   # lex = Stichwort im Lexikon der Prüfseite
        punkte.append({'id': pid, 'titel': titel, 'gut': bool(gut), 'text': text, 'lex': '' if gut else lex})
    try:
        b = beschreibung(haus)
        punkt('beschreibung', 'Beschreibung des Hauses', True, f'{len(b["seiten"])} Seiten, {len(sprachen(haus))} weitere Sprachen, {len([k for k, v in (b.get("bereiche") or {}).items() if v.get("an") is not False])} Bereiche')
    except Fehler as e:
        punkt('beschreibung', 'Beschreibung des Hauses', False, e.text, e.stichwort)
        return {'version': VERSION, 'punkte': punkte}
    try:
        probe(haus)
        fehlen = [n for n in seiten(haus) if not (A.probe_ordner() / haus / 'grundlage' / n).exists()]
        punkt('probe', 'Kopie der Seiten', not fehlen, 'Jede Seite liegt in der Kopie.' if not fehlen else 'Es fehlen: ' + ', '.join(fehlen[:6]), lex='seite-fehlt')
    except Fehler as e:
        punkt('probe', 'Kopie der Seiten', False, e.text, e.stichwort)
        return {'version': VERSION, 'punkte': punkte}
    try:
        s = stand_roh(haus, speicher)
        punkt('speicher', 'Stand im Speicher', True, 'Veröffentlichter Stand lesbar' + (', ein Entwurf ist offen.' if s['offen'] else ', kein Entwurf offen.'))
    except speicher.Beschaedigt as e:
        punkt('speicher', 'Stand im Speicher', False, str(e), lex='beschaedigt')
        return {'version': VERSION, 'punkte': punkte}
    live, c = schicht(s['live']), arbeits(s)
    ungleich = [n for n in seiten(haus) if S.anwenden(n, grundlage(haus, n), S.leer(), regeln=b['regeln']) != grundlage(haus, n)]
    punkt('unveraendert', 'Ohne Änderung bleibt jede Seite Byte für Byte gleich', not ungleich, f'{len(seiten(haus))} Seiten verglichen.' if not ungleich else 'Abweichung bei: ' + ', '.join(ungleich[:6]), lex='unveraendert')
    for name, lage in (('Veröffentlicht', live), ('Entwurf', c)):
        seiten_neu, ohne, fehlt = soll(haus, lage)
        punkt('platz-' + name.lower(), f'{name}: jede Änderung findet ihre Stelle', not ohne, 'Alle Änderungen haben ihren Platz.' if not ohne else f'{len(ohne)} ohne Platz: ' + '; '.join(f'{o["seite"]} «{o["was"][:40]}»' for o in ohne[:4]), lex='stelle-fehlt')
        if name == 'Veröffentlicht':
            anders = A.vergleich(haus, {k: v.encode('utf-8') for k, v in seiten_neu.items()})
            punkt('online', 'Die Seiten online entsprechen dem veröffentlichten Stand', not anders, f'{len(seiten_neu)} Dateien verglichen.' if not anders else f'{len(anders)} Dateien weichen ab: ' + ', '.join(anders[:6]), lex='ausgabe')
        else:
            gesamt = sum(fehlt.values())
            punkt('uebersetzung', 'Übersetzungen der offenen Änderungen', not gesamt, 'Keine fehlt.' if not gesamt else 'Es fehlen: ' + ', '.join(f'{k} {v}' for k, v in fehlt.items()) + '. Dort steht der deutsche Text.', lex='uebersetzung-fehlt')
    for x in sprachen(haus):
        da = ges = 0
        ohne_seite = []
        for n in seiten(haus):
            q = grundlage(haus, n, x['code'])
            if q is None:
                ohne_seite.append(n)
                continue
            a, g = S.paarung(q, grundlage(haus, n), b['regeln'])
            da, ges = da + a, ges + g
        anteil = da / ges if ges else 0
        punkt('sprache-' + x['code'], f'Zuordnung {x.get("name") or x["code"]}', anteil >= .9 and not ohne_seite,
              f'{da} von {ges} deutschen Stellen haben ihr Gegenstück' + (f', {len(ohne_seite)} Seiten fehlen in dieser Sprache' if ohne_seite else '') + '.', lex='sprache-zuordnung')
    bereiche = []
    for k, d in (b.get('bereiche') or {}).items():
        if d.get('an') is False:
            continue
        try:
            r = bereich(haus, k, c)
            bereiche.append((r['name'], len(r['eintraege']), r['fehlt']))
        except (Fehler, ValueError, KeyError) as e:
            bereiche.append((k, 0, [str(e)]))
    schlecht = [f'{n}: {f[0]}' for n, z, f in bereiche if f or not z]
    punkt('bereiche', 'Bereiche des Hauses lesen ihre Felder aus den Seiten', not schlecht, ', '.join(f'{n} {z}' for n, z, f in bereiche) or 'Keine Bereiche eingeschaltet.' if not schlecht else '; '.join(schlecht[:4]), lex='bereich-feld')
    try:
        zz = zahlen(haus, c)
        punkt('zahlen', 'Zeiten und Preise', zz['zahl'] > 0, f'{zz["zahl"]} Angaben gefunden.', lex='zahlen-leer')
    except Fehler as e:
        punkt('zahlen', 'Zeiten und Preise', False, e.text, e.stichwort)
    pr = speicher.protokoll(haus, WERKZEUG, 200)
    aus_sich = [z for z in pr if z.get('was') == 'aus-sicherung']
    punkt('protokoll', 'Protokoll', not aus_sich, f'{len(pr)} Einträge, zuletzt: {pr[0]["was"]} {pr[0]["zeit"]}' if pr and not aus_sich else (f'Am {aus_sich[0]["zeit"]} kam ein Stand aus der Sicherung zurück.' if aus_sich else 'Noch leer.'), lex='aus-sicherung')
    return {'version': VERSION, 'haus': haus, 'punkte': punkte, 'verlauf': len(speicher.verlauf(haus, WERKZEUG))}


def reparieren(haus, d, speicher):
    was = d.get('was')
    if was == 'ausgeben':   # die Seiten online noch einmal aus Grundlage + veröffentlichtem Stand schreiben
        with A.sperre(haus):
            s = stand_roh(haus, speicher)
            seiten_neu, ohne, _ = soll(haus, schicht(s['live']))
            geschrieben = A.schreibe(haus, {k: v.encode('utf-8') for k, v in seiten_neu.items()})
        return 200, {'meldung': f'{len(geschrieben)} Seiten neu geschrieben.' if geschrieben else 'Alle Seiten waren schon richtig.', 'geschrieben': geschrieben}
    if was == 'ohne-platz':   # Änderungen im Entwurf entfernen, die ihre Stelle nicht mehr finden
        s = stand_roh(haus, speicher)
        c = arbeits(s)
        _, ohne, _ = soll(haus, c)
        if not ohne:
            return 200, {'meldung': 'Jede Änderung hat ihren Platz. Nichts entfernt.'}
        for o in ohne:
            feld = {'text': 'texte', 'bild': 'bilder', 'link': 'links', 'aus': 'aus'}[o['art']]
            t = o['key'].split('|')
            _weg(c, feld, t[1], t[2], int(t[3]))
        speicher.entwurf_schreiben(haus, WERKZEUG, c, s['kennung_entwurf'] or s['kennung_live'], d.get('wer', ''))
        return 200, {'meldung': f'{len(ohne)} Änderung(en) ohne Platz aus dem Entwurf entfernt. Der veröffentlichte Stand ist unberührt.'}
    raise Fehler(400, 'anfrage', 'Diese Reparatur gibt es nicht.')


# ------------------------------------------------------------------ Eingang

# ------------------------------------------------------------------ Google-Texte (Master Werkzeug-Bau 4.2 I, 21.10.2026): Titel und Beschreibung je Seite
SEO_LANG = (60, 155)   # Richtwerte wie Le Bureau am Vorbild: so viel zeigt Google ungefähr, länger wird abgeschnitten


def _seo_original(haus, datei):
    src = grundlage(haus, datei)
    t = S._TITEL.search(src)
    d = S._BESCHR.search(src)
    return (S.klar(t.group(2)) if t else ''), (_unesc(d.group(2)) if d else ''), bool(d)


def _oben_fest(blk):
    while blk:
        if blk.get('fest'):
            return True
        blk = blk.get('eltern')
    return False


def seitenfoto(haus, datei, benutzt=(), wahl=None):
    """Das Foto einer Seite für Listen (Fehlerbuch 10a: jede Liste mit Bild, kein Foto zweimal auf einem Bildschirm): was die Beschreibung nennt,
    sonst das erste grosse Foto der Seite ausserhalb von Kopf und Fuss, das in der Liste noch nicht vorkam."""
    if wahl and wahl in spender(haus):
        return wahl
    kand = [f for f in zer(haus, datei)['fotos'] if not f.get('zu') and not _oben_fest(f.get('blk'))]
    gross = [f['b'] for f in kand if str(f['attrs'].get('width') or '').isdigit() and int(f['attrs']['width']) >= 800]
    return next((b for b in gross + [f['b'] for f in kand] if b not in benutzt), (gross or [''])[0])


def google(haus, c):
    if not (beschreibung(haus).get('google') or {}).get('an'):
        raise Fehler(404, 'weg-unbekannt', 'Google-Texte sind für dieses Haus nicht eingeschaltet.')
    aus, benutzt = [], set()
    eigen = {x['datei']: x.get('foto') for x in beschreibung(haus)['seiten'] if x.get('foto')}
    for n in seiten(haus):
        titel, beschr, hat = _seo_original(haus, n)
        r = _regel(c, 'seo', n, 'kopf', 0) or {}
        foto = seitenfoto(haus, n, benutzt, eigen.get(n))
        benutzt.add(foto)
        aus.append({'seite': n, 'name': seitenname(haus, n), 'titel': r.get('titel') or titel, 'beschreibung': r.get('beschreibung') or beschr,
                    'original_titel': titel, 'original_beschreibung': beschr, 'hat_beschreibung': hat, 'geaendert': bool(r), 'foto': kurz_bild(haus, foto) if foto else ''})
    return {'seiten': aus, 'richtwert': {'titel': SEO_LANG[0], 'beschreibung': SEO_LANG[1]}}


def _op_seo(haus, c, live, op, quittung):
    seite = op.get('seite') or ''
    if seite not in seiten(haus):
        raise Fehler(404, 'seite-unbekannt', 'Diese Seite gehört nicht zur Website.')
    titel0, beschr0, hat = _seo_original(haus, seite)
    titel = re.sub(r'\s+', ' ', S.klar(str(op.get('titel') or ''))).strip()
    beschr = re.sub(r'\s+', ' ', S.klar(str(op.get('beschreibung') or ''))).strip()
    if not titel:
        raise Fehler(422, 'leer', 'Ohne Titel zeigt Google die Seite mit ihrer Adresse. Bitte einen Titel schreiben.')
    if len(titel) > 120 or len(beschr) > 320:
        raise Fehler(422, 'zu-lang', 'Google schneidet so lange Texte ab. Titel höchstens 120, Beschreibung höchstens 320 Zeichen.')
    if beschr and not hat:
        raise Fehler(422, 'stelle-fehlt', 'Diese Seite hat keine Beschreibung für Google, die sich ändern liesse.')
    vor = _regel(c, 'seo', seite, 'kopf', 0)
    _weg(c, 'seo', seite, 'kopf', 0)
    if titel != titel0 or (beschr and beschr != beschr0):
        c.setdefault('seo', []).append({'seite': seite, 'h': 'kopf', 'n': 0, 'titel': titel, 'beschreibung': beschr if beschr != beschr0 else '',
                                        'alt_titel': titel0, 'alt_beschreibung': beschr0})
    quittung.append({'key': S.schluessel('seo', seite, 'kopf', 0), 'wo': seitenname(haus, seite), 'was': 'Google-Texte',
                     'vorher': (vor or {}).get('titel') or titel0, 'nachher': titel})


# ------------------------------------------------------------------ Angaben des Hauses (Master Werkzeug-Bau 4.2 E, L16): einmal ändern, überall richtig
def _muster(wert):
    """Ein Wert, wie er im HTML stehen kann: Leerzeichen auch als &nbsp;, & auch als &amp;."""
    teile = [re.escape(t).replace('&', '(?:&|&amp;)') for t in wert.split()]
    rand = (r'(?<![\d\w])', r'(?![\d\w])')   # «Oberdorfstrasse 8» nie in «Oberdorfstrasse 80», «8556» nie in «18556»
    return re.compile(rand[0] + r'(?:\s|&nbsp;|&#160;|\xa0)+'.join(teile) + (rand[1] if re.match(r'[\w]', wert[-1:] or '') else ''))


def _tel_link(wert):
    ziffern = re.sub(r'\D', '', wert)
    if wert.strip().startswith('+'):
        return 'tel:+' + ziffern
    return 'tel:+41' + ziffern[1:] if ziffern.startswith('0') else 'tel:' + ziffern


def _angabe_def(haus, key):
    a = next((x for x in beschreibung(haus).get('angaben') or [] if x.get('key') == key), None)
    if a is None:
        raise Fehler(404, 'angabe-unbekannt', 'Diese Angabe kennt das Werkzeug nicht.')
    return a


def _angabe_orte(haus, c, a):
    """Wo eine Angabe steht: jede Textstelle, deren Text sie enthält, und jeder Link, der auf sie zeigt. Gesucht wird nach dem Wert, den die
    Website gebaut hat, und nach dem Wert im Entwurf (c['angaben']); gesperrte Stellen (Karten) zählen nicht."""
    jetzt = ((c.get('angaben') or {}).get(a['key']) or a['wert'])
    werte = [w for w in dict.fromkeys([jetzt, a['wert']]) if w]
    texte, links = [], []
    href_alt = {a['wert']: a.get('link') or ('mailto:' + a['wert'] if a['art'] == 'mail' else a['wert'] if a['art'] == 'link' else _tel_link(a['wert']) if a['art'] == 'telefon' else None)}
    href_alt[jetzt] = _tel_link(jetzt) if a['art'] == 'telefon' else 'mailto:' + jetzt if a['art'] == 'mail' else jetzt if a['art'] == 'link' else None
    hrefs = {h for h in href_alt.values() if h}
    for n in seiten(haus):
        z, src = zer(haus, n), grundlage(haus, n)
        if a['art'] != 'link':
            for st in z['texte']:
                if st.get('zu'):
                    continue
                r = _regel(c, 'texte', n, st['h'], st['n'])
                html = r['neu'] if r else _html(src, st)
                if any(_muster(w).search(html) for w in werte):
                    texte.append({'seite': n, 'h': st['h'], 'n': st['n'], 'html': html, 't': S.klar(html)})
        for x in z['links']:
            if x.get('zu'):
                continue
            r = _regel(c, 'links', n, x['h'], x['n'])
            href = _unesc(r['neu'] if r else x['href'])
            if href in hrefs:
                links.append({'seite': n, 'h': x['h'], 'n': x['n'], 'href': href, 't': x['t']})
    return jetzt, texte, links


def angaben(haus, c):
    aus = []
    for a in beschreibung(haus).get('angaben') or []:
        jetzt, texte, links = _angabe_orte(haus, c, a)
        aus.append({'key': a['key'], 'label': a['label'], 'art': a['art'], 'wert': jetzt, 'original': a['wert'], 'geaendert': jetzt != a['wert'],
                    'stellen': len(texte), 'links': len(links), 'seiten': len({x['seite'] for x in texte + links}),
                    'beispiel': [{'seite': x['seite'], 'name': seitenname(haus, x['seite']), 't': kurz_satz(x['t'])} for x in texte[:3]]})
    return {'angaben': aus}


def kurz_satz(t, n=110):
    return t if len(t) <= n else t[:n - 1] + '…'


def _op_angabe(haus, c, live, op, quittung):
    a = _angabe_def(haus, op.get('key'))
    neu = re.sub(r'\s+', ' ', str(op.get('neu') or '')).strip()
    if not neu:
        raise Fehler(422, 'leer', 'Eine Angabe ohne Wert bleibt als Lücke auf der Website stehen.')
    if a['art'] == 'telefon' and not re.fullmatch(r'\+?[\d ]{8,20}', neu):
        raise Fehler(422, 'angabe-telefon', 'Eine Telefonnummer besteht nur aus Ziffern und Leerzeichen, vorne höchstens ein «+».')
    if a['art'] == 'mail' and not re.fullmatch(r'[^@\s<>"]+@[^@\s<>"]+\.[a-z]{2,}', neu, re.I):
        raise Fehler(422, 'angabe-mail', 'Eine E-Mail-Adresse sieht so aus: name@haus.ch')
    if a['art'] == 'link' and not re.fullmatch(r'https://[^\s"<>]+', neu):
        raise Fehler(422, 'link', 'Eine Adresse beginnt mit https://')
    if len(neu) > 200:
        raise Fehler(422, 'zu-lang', 'Diese Angabe ist zu lang.')
    jetzt, texte, links = _angabe_orte(haus, c, a)
    if neu == jetzt:
        return
    if not texte and not links:
        raise Fehler(422, 'stelle-fehlt', 'Diese Angabe steht auf keiner Seite mehr.')
    ersatz = _h.escape(neu, quote=False)
    for x in texte:
        html = x['html']
        for w in dict.fromkeys([jetzt, a['wert']]):
            html = _muster(w).sub(lambda m: ersatz, html)
        _op(haus, c, live, {'art': 'text', 'seite': x['seite'], 'h': x['h'], 'n': x['n'], 'neu': html}, [])
    ziel = _tel_link(neu) if a['art'] == 'telefon' else 'mailto:' + neu if a['art'] == 'mail' else neu if a['art'] == 'link' else None
    if ziel:
        for x in links:
            _op(haus, c, live, {'art': 'link', 'seite': x['seite'], 'h': x['h'], 'n': x['n'], 'neu': ziel}, [])
    c.setdefault('angaben', {})[a['key']] = neu
    if neu == a['wert']:
        c['angaben'].pop(a['key'], None)
    quittung.append({'key': 'angabe|' + a['key'], 'wo': f'{len(texte)} Stellen auf {len({x["seite"] for x in texte + links})} Seiten', 'was': a['label'], 'vorher': jetzt, 'nachher': neu})


# ------------------------------------------------------------------ Eigene Fotos hochladen (Master Werkzeug-Bau 4.2 D, 21.10.2026)
FOTO_BREITEN = (480, 900, 1400, 2000)
FOTO_MIN, FOTO_MAX_BYTES = 900, 25 * 1024 * 1024


def _fotos_ordner(haus):
    o = Path(os.environ.get('WERKZEUGE_DATEN') or WURZEL / 'daten') / haus / 'website-fotos'
    o.mkdir(parents=True, exist_ok=True)
    return o


def _hochgeladen(haus):
    """Die eigenen Fotos des Hauses: {schlüssel: {w, h, alt, breiten, zeit, name}}. Liegen im Datenordner (überstehen eine neue Kopie der Seiten)."""
    aus = {}
    for m in sorted(_fotos_ordner(haus).glob('u-*.json')):
        try:
            aus[m.stem] = json.loads(m.read_text(encoding='utf-8'))
        except ValueError:
            continue
    return aus


def _foto_ziel(haus):
    return ((beschreibung(haus).get('hochladen') or {}).get('ordner') or 'assets/img').strip('/')


def fotos_verteilen(haus):
    """Jedes eigene Foto liegt auch in der Kopie (grundlage und online), damit Vorschau und veröffentlichte Seiten es zeigen. Seiten werden nicht angefasst."""
    if not (beschreibung(haus).get('hochladen') or {}).get('an'):
        return 0
    n = 0
    for teil in ('grundlage', 'online'):
        ziel = A.probe_ordner() / haus / teil / _foto_ziel(haus)
        if not ziel.parent.exists():
            continue
        ziel.mkdir(parents=True, exist_ok=True)
        for f in _fotos_ordner(haus).glob('u-*.webp'):
            if not (ziel / f.name).exists():
                import shutil
                shutil.copy2(f, ziel / f.name)
                n += 1
    return n


def _spender_eigene(haus):
    if not (beschreibung(haus).get('hochladen') or {}).get('an'):
        return {}
    o, aus = _foto_ziel(haus), {}
    for k, m in _hochgeladen(haus).items():
        br = m['breiten']
        mitte = next((w for w in br if w >= 900), br[-1])
        satz = ', '.join(f'{o}/{k}-{w}.webp {w}w' for w in br)
        aus[k] = f'<img src="{o}/{k}-{mitte}.webp" srcset="{satz}" width="{m["w"]}" height="{m["h"]}" alt="{_h.escape(m.get("alt") or "", quote=True)}">'
    return aus


def hochladen(haus, d, speicher):
    """d = {name, daten: 'data:image/…;base64,…', alt}. Neu kodiert als WebP in vier Liefergrössen, keine fremden Bytes auf die Website."""
    import base64
    import hashlib
    import io
    if not (beschreibung(haus).get('hochladen') or {}).get('an'):
        raise Fehler(404, 'weg-unbekannt', 'Hochladen ist für dieses Haus nicht eingeschaltet.')
    roh = str(d.get('daten') or '')
    if ',' in roh[:100]:
        roh = roh.split(',', 1)[1]
    try:
        b = base64.b64decode(roh, validate=True)
    except (ValueError, TypeError):
        raise Fehler(400, 'bild-kaputt', 'Die Datei kam nicht vollständig an. Bitte noch einmal wählen.')
    if len(b) > FOTO_MAX_BYTES:
        raise Fehler(413, 'bild-gross', 'Das Foto ist grösser als 25 MB. Bitte eine kleinere Fassung wählen.')
    try:
        from PIL import Image, ImageOps
        Image.MAX_IMAGE_PIXELS = 60_000_000
        bild = Image.open(io.BytesIO(b))
        bild.load()
        bild = ImageOps.exif_transpose(bild)
    except Exception:
        raise Fehler(422, 'bild-art', 'Diese Datei ist kein Foto. Möglich sind JPG, PNG, WebP und HEIC aus dem Fotoapparat als JPG.')
    w, h = bild.size
    if w < FOTO_MIN:
        raise Fehler(422, 'bild-klein', f'Das Foto ist nur {w} Pixel breit. Für die Website braucht es mindestens {FOTO_MIN} Pixel, sonst wirkt es unscharf.')
    if bild.mode not in ('RGB', 'RGBA'):
        bild = bild.convert('RGB')
    if bild.mode == 'RGBA':
        grund = Image.new('RGB', bild.size, (255, 255, 255))
        grund.paste(bild, mask=bild.split()[3])
        bild = grund
    k = 'u-' + hashlib.sha1(b).hexdigest()[:12]
    o = _fotos_ordner(haus)
    breiten = [x for x in FOTO_BREITEN if x <= w] or [w]
    if w not in breiten and w < FOTO_BREITEN[-1] and w > breiten[-1]:
        breiten.append(w)
    for x in breiten:
        kl = bild if x == w else bild.resize((x, round(h * x / w)), Image.LANCZOS)
        tmp = o / f'{k}-{x}.webp.neu'
        kl.save(tmp, 'WEBP', quality=82, method=5)
        os.replace(tmp, o / f'{k}-{x}.webp')
    alt = re.sub(r'\s+', ' ', str(d.get('alt') or '')).strip()[:400]
    name = re.sub(r'[^\w .\-äöüÄÖÜ]', '', str(d.get('name') or ''))[:80]
    (o / f'{k}.json').write_text(json.dumps({'w': w, 'h': h, 'alt': alt, 'breiten': breiten, 'name': name, 'zeit': time.strftime('%Y-%m-%dT%H:%M:%S')}, ensure_ascii=False), encoding='utf-8')
    fotos_verteilen(haus)
    ZW.pop(('spender', haus), None)
    return 200, {'b': k, 'klein': f'{_foto_ziel(haus)}/{k}-{breiten[0]}.webp', 'w': w, 'h': h, 'alt': alt, 'meldung': f'Foto übernommen ({w} × {h} Pixel), in {len(breiten)} Grössen für die Website.'}


def bearbeite(methode, rest, daten, speicher):
    try:
        if len(rest) < 2:
            raise Fehler(404, 'weg-unbekannt', 'Weg unbekannt.')
        was, haus = rest[0], rest[1]
        mehr = rest[2:]
        if methode == 'GET':
            if was == 'haus':
                return 200, haus_info(haus)
            if was == 'stand':
                return 200, stand(haus, speicher)
            if was == 'pruefung':
                return 200, pruefung(haus, speicher)
            if was == 'ueberblick':   # Stand-Weg für La Maison / Die Stube, gleiche Form wie Le Bureau am Rivage (Master Werkzeug-Bau 4.1)
                st = stand(haus, speicher)
                return 200, {'aenderungen': len(st['aenderungen']), 'zuletzt': {'zeit': (st['zuletzt'] or {}).get('zeit')} if st['zuletzt'] else None,
                             'bereiche': [w['name'] for w in website_bereiche(haus)], 'seiten': len(beschreibung(haus)['seiten'])}
            s = stand_roh(haus, speicher)
            live, c = schicht(s['live']), arbeits(s)
            if was == 'seite' and len(mehr) == 1:
                _rel(haus, mehr[0])
                return 200, verzeichnis(haus, mehr[0], c)
            if was == 'stelle' and len(mehr) == 3:
                _rel(haus, mehr[0])
                return 200, stelle(haus, mehr[0], mehr[1], int(mehr[2]), c, live)
            if was == 'foto' and len(mehr) == 3:
                _rel(haus, mehr[0])
                return 200, foto(haus, mehr[0], mehr[1], int(mehr[2]), c)
            if was == 'fotos':
                return 200, fotos(haus)
            if was == 'google':
                return 200, google(haus, c)
            if was == 'angaben':
                return 200, angaben(haus, c)
            if was == 'vorschau' and len(mehr) == 3:
                return 200, vorschau(haus, mehr[0], mehr[1], mehr[2], s)
            if was == 'zahlen':
                return 200, zahlen(haus, c)
            if was == 'bereich' and len(mehr) == 1:
                return 200, bereich(haus, mehr[0], c)
            if was == 'sprachen':
                return 200, sprachen_liste(haus, c, live)
            if was == 'verlauf':
                return 200, verlauf(haus, speicher)
            if was == 'fassung' and len(mehr) == 1:
                return 200, fassung(haus, mehr[0], speicher)
        if methode == 'POST':
            if was == 'aendern':
                return aendern(haus, daten, speicher)
            if was == 'veroeffentlichen':
                return veroeffentlichen(haus, daten, speicher)
            if was == 'reparieren':
                return reparieren(haus, daten, speicher)
            if was == 'hochladen':
                return hochladen(haus, daten, speicher)
        raise Fehler(404, 'weg-unbekannt', 'Weg unbekannt.')
    except Fehler as f:
        return f.status, dict(f.mehr, fehler=f.text, stichwort=f.stichwort)
    except (ValueError, KeyError, TypeError, IndexError) as f:
        sys.stderr.write(f'FEHLER website {methode} {"/".join(rest)}: {f!r}\n')
        return 500, {'fehler': f'Unerwarteter Fehler: {f}', 'stichwort': 'unerwartet'}
