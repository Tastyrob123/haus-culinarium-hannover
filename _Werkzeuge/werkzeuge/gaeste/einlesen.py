"""Einlesen · liest den ersten Stand eines Hauses für das Werkzeug «gaeste» aus den Quellen des Hauses.

Die Quellen werden NUR gelesen (STAND.md, «Wem was gehört», Punkt 3). Was gelesen wurde, legt api.py über den Speicher ab.
Welche Dateien zu welchem Haus gehören, steht in quellen.json. Fehlt eine Angabe, wird nichts erfunden:
das Feld bleibt leer und die Lücke steht in «offen».

Von Hand:  python3 werkzeuge/gaeste/einlesen.py <haus>            zeigt, was gelesen würde (schreibt nichts)
           python3 werkzeuge/gaeste/einlesen.py <haus> grundstand legt den ersten Stand über den Speicher ab
"""
import ast
import glob
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from html.parser import HTMLParser
from pathlib import Path

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parent.parent
ARTEN = ('zimmer', 'tisch', 'feier', 'tagung')
# Aus den Vorlagen übernommen (Carlton-Europe und Grand Beau-Rivage, _gast/gast.py, Stand 12.10.2026); gilt, wenn die Quelle nichts nennt.
GRENZEN_VORLAGE = {'besucher_10min': 20, 'besucher_tag': 80, 'gesamt_tag': 2000, 'anfrage_tag': 60}


class Leser(HTMLParser):
    """Text einer Seite ohne Kopf, Fuss, Menü und Skripte (wie gast_haeuser.py der Familie Maeder)."""
    WEG = {'script', 'style', 'svg', 'nav', 'footer', 'noscript', 'template', 'header'}
    BLOCK = ('h1', 'h2', 'h3', 'h4', 'p', 'li', 'dt', 'dd', 'tr', 'figcaption', 'div', 'section', 'blockquote', 'td', 'th', 'br')
    WORT = ('a', 'button', 'span', 'small', 'time')     # hier ein Leerzeichen, sonst kleben Wörter zusammen («SaunaOffen»)

    def __init__(self):
        super().__init__()
        self.aus, self.tief = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.WEG:
            self.tief += 1
            return
        if not self.tief and tag in self.BLOCK:
            self.aus.append('\n' + ('## ' if tag in ('h1', 'h2', 'h3') else '') + (' | ' if tag in ('td', 'th') else ''))
        elif not self.tief and tag in self.WORT:
            self.aus.append(' ')

    def handle_endtag(self, tag):
        if tag in self.WEG and self.tief:
            self.tief -= 1
        elif not self.tief and tag in self.WORT:
            self.aus.append(' ')

    def handle_data(self, d):
        if not self.tief:
            self.aus.append(d)


def _glatt(t):
    t = re.sub(r'[ \t ]+', ' ', t)
    t = re.sub(r' ?\n ?', '\n', t)
    return re.sub(r'\n{2,}', '\n', t).strip()


def _kennung(art, titel):
    k = re.sub(r'[^a-z0-9]+', '-', titel.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('é', 'e').replace('è', 'e')).strip('-')[:48]
    return f'{art}-{k or hashlib.sha1(titel.encode()).hexdigest()[:8]}'


def _abschnitt(art, titel, quelle, text):
    return {'id': _kennung(art, titel), 'art': art, 'titel': titel, 'quelle': quelle, 'text': text.strip()}


def _konstante(pfad, name):
    """Liest eine wörtliche Zuweisung (NAME = {...}) aus einer Python-Datei, ohne sie auszuführen."""
    try:
        baum = ast.parse(Path(pfad).read_text(encoding='utf-8'))
    except (OSError, SyntaxError):
        return None
    for k in baum.body:
        if isinstance(k, ast.Assign) and getattr(k.targets[0], 'id', '') == name:
            try:
                return ast.literal_eval(k.value)
            except (ValueError, SyntaxError):
                continue
    return None


def _bloecke(text, art):
    """Teilt eine Wissensdatei an ihren Kopfzeilen «=== Seite: … ===» in Abschnitte."""
    aus, vor = [], ''
    teile = re.split(r'^=== (.+?) ===\s*$', text, flags=re.M)
    vor = teile[0].strip()
    for i in range(1, len(teile), 2):
        kopf, inhalt = teile[i], teile[i + 1]
        m = re.match(r'(Seite|Unterlage des Hauses|Talwissen): (.*)$', kopf)
        sorte = {'Seite': 'seite', 'Unterlage des Hauses': 'unterlage', 'Talwissen': 'tal'}.get(m.group(1) if m else '', art)
        rest = m.group(2) if m else kopf
        if sorte == 'tal':
            t = [x.strip() for x in rest.split(' · ')]
            titel, quelle = t[0], ' · '.join(t[1:])
        else:
            q = re.search(r'\((?:Entwurf: )?([^()]*)\)\s*$', rest)
            titel, quelle = (rest[:q.start()].strip(), q.group(1)) if q else (rest, '')
        aus.append(_abschnitt(sorte, titel, quelle, inhalt))
    return vor, aus


def _seite(pfad):
    h = Path(pfad).read_text(encoding='utf-8', errors='replace')
    titel = re.search(r'<title>(.*?)</title>', h, re.S)
    l = Leser()
    l.feed(h)
    name = html.unescape(titel.group(1).strip()) if titel else os.path.basename(pfad)
    return _abschnitt('seite', name, os.path.basename(pfad), _glatt(html.unescape(''.join(l.aus))))


def _vorlage_text(pfad):
    s = Path(pfad).read_text(encoding='utf-8')
    s = re.sub(r'<(script|style|head)[^>]*>.*?</\1>', '', s, flags=re.S | re.I)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</(p|tr|h\d|div|td)>', '\n', s)
    t = html.unescape(re.sub(r'<[^>]+>', '', s))
    t = re.sub(r'[͏﻿​]', '', t)
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t ]+', ' ', t)).strip()


def _modul(pfad):
    """Lädt eine Python-Datei eines Hauses, ohne dort etwas zu schreiben (auch keinen Zwischenspeicher)."""
    alt = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location('gaeste_quelle_' + hashlib.sha1(str(pfad).encode()).hexdigest()[:8], pfad)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    finally:
        sys.dont_write_bytecode = alt


def lies(haus):
    """Der erste Stand eines Hauses als Dokument für den Speicher. Wirft ValueError mit klarem Text, wenn die Quelle fehlt."""
    hp = WURZEL / 'haeuser' / haus / 'haus.json'
    if not re.match(r'^[a-z0-9][a-z0-9-]{0,40}$', haus or '') or not hp.exists():
        raise ValueError('Dieses Haus gibt es nicht.')
    stamm = json.loads(hp.read_text(encoding='utf-8'))
    rezept = json.loads((HIER / 'quellen.json').read_text(encoding='utf-8')).get(haus)
    offen, quellen = [], []
    doc = {'fassung': 1,
           'haus': {'name': stamm.get('name', ''), 'ort': '', 'tel': '', 'mail': '', 'adresse': '', 'zeiten': '', 'fahrplan': '', 'buchung': '',
                    'sprachen': {}, 'absender': {}, 'orte': [], 'modell': ''},
           'karten': [], 'muster': '', 'wissen': [], 'vorlagen': {}, 'team': [],
           'einstellungen': {'obergrenze_monat_usd': None, **GRENZEN_VORLAGE, 'aufbewahrung_monate': 12},
           'probefragen': []}
    if not rezept:
        offen.append('Für dieses Haus ist in quellen.json keine Quelle eingetragen. Wissen, Kontakt und Vorlagen sind offen.')
        doc['eingelesen'] = {'zeit': time.strftime('%Y-%m-%dT%H:%M:%S'), 'quellen': [], 'offen': offen}
        return doc
    q = Path(os.path.expanduser(stamm.get('quelle', '')))
    if not q.is_dir():
        raise ValueError(f'Die Quelle des Hauses ist nicht erreichbar: {stamm.get("quelle", "")}')

    def weg(rel):
        return (q / rel).resolve()

    # ---- Angaben zum Haus
    h = {}
    if rezept.get('haus_json') and weg(rezept['haus_json']).exists():
        h = json.loads(weg(rezept['haus_json']).read_text(encoding='utf-8'))
        quellen.append(rezept['haus_json'])
    if rezept.get('haus_py') and weg(rezept['haus_py']['datei']).exists():
        m = _modul(weg(rezept['haus_py']['datei']))
        e = dict(m.HAEUSER[rezept['haus_py']['schluessel']])
        h = {'name': e['name'], 'ort': e['ort'], 'tel': e['tel'], 'mail': e['mail'], 'adresse': e['adresse'], 'zeiten': e['zeiten'],
             'fahrplan': getattr(m, 'FAHRPLAN', ''), 'buchung': e.get('buchung', ''), 'orte': getattr(m, 'ORTE_KANDERSTEG', []),
             'muster': getattr(m, 'MUSTER', {}).get(rezept['haus_py']['schluessel'], ''), 'karten': [list(x[:3]) for x in e.get('karten', [])],
             'modell': getattr(m, 'MODELL', {}).get(rezept['haus_py']['schluessel'], '')}
        quellen.append(os.path.basename(rezept['haus_py']['datei']))
    for k in ('name', 'ort', 'tel', 'mail', 'adresse', 'zeiten', 'fahrplan', 'buchung', 'orte', 'modell'):
        if h.get(k):
            doc['haus'][k] = h[k]
    doc['muster'] = h.get('muster', '')
    doc['karten'] = h.get('karten', [])
    if rezept.get('chat_skript') and weg(rezept['chat_skript']).exists():
        m = re.search(r'/\*HAUS\*/(.*?)/\*ENDEH\*/', weg(rezept['chat_skript']).read_text(encoding='utf-8'), re.S)
        try:
            c = json.loads(m.group(1)) if m else {}
        except ValueError:
            c = {}
        doc['haus']['buchung'] = doc['haus']['buchung'] or c.get('buchung', '')
        doc['karten'] = doc['karten'] or [list(x[:3]) for x in (c.get('karten') or {}).get('de', [])]
        quellen.append(rezept['chat_skript'])
    if rezept.get('konstanten') and weg(rezept['konstanten']).exists():
        k = weg(rezept['konstanten'])
        doc['haus']['sprachen'] = _konstante(k, 'SPRACHE') or {}
        g = _konstante(k, 'GRENZEN')
        if g:
            doc['einstellungen'].update({x: g[x] for x in GRENZEN_VORLAGE if x in g})
        doc['haus']['modell'] = doc['haus']['modell'] or _konstante(k, 'MODELL') or ''
        quellen.append(os.path.basename(str(k.parent.parent)) + '/' + k.parent.name + '/' + k.name)
    for k, was in (('tel', 'Telefon'), ('mail', 'E-Mail'), ('adresse', 'Adresse'), ('buchung', 'Adresse der Buchung'), ('modell', 'Modell der KI')):
        if not doc['haus'][k]:
            offen.append(f'{was} des Hauses steht in keiner Quelle.')
    if not doc['haus']['sprachen']:
        offen.append('In welchen Sprachen der Chat antwortet, steht in keiner Quelle.')

    # ---- Wissen
    if rezept.get('wissen_datei') and weg(rezept['wissen_datei']).exists():
        _, l = _bloecke(weg(rezept['wissen_datei']).read_text(encoding='utf-8'), 'seite')
        doc['wissen'] += l
        quellen.append(rezept['wissen_datei'])
    if rezept.get('seiten'):
        nicht = re.compile(rezept['seiten'].get('nicht') or r'^$')
        for f in sorted(glob.glob(str(q / rezept['seiten']['muster']))):
            if not nicht.match(os.path.basename(f)):
                doc['wissen'].append(_seite(f))
        quellen.append('Seiten ' + rezept['seiten']['muster'])
    if rezept.get('unterlagen'):
        for f in sorted(glob.glob(str(q / rezept['unterlagen']))):
            try:
                t = subprocess.run(['pdftotext', '-enc', 'UTF-8', f, '-'], capture_output=True, text=True, timeout=60).stdout
            except (OSError, subprocess.SubprocessError):
                t = ''
            t = re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t ]+', ' ', t)).strip()
            if t:
                doc['wissen'].append(_abschnitt('unterlage', os.path.basename(f)[:-4], os.path.basename(f), t[:60000]))
            else:
                offen.append(f'Die Unterlage {os.path.basename(f)} liess sich nicht lesen.')
        quellen.append('Unterlagen ' + rezept['unterlagen'])
    if rezept.get('tal_datei') and weg(rezept['tal_datei']).exists():
        vor, l = _bloecke(weg(rezept['tal_datei']).read_text(encoding='utf-8'), 'tal')
        doc['wissen'] += l
        doc['tal_hinweis'] = vor
        quellen.append(os.path.basename(rezept['tal_datei']))
    # gleiche Kennungen eindeutig machen
    gesehen = {}
    for a in doc['wissen']:
        n = gesehen.get(a['id'], 0)
        gesehen[a['id']] = n + 1
        if n:
            a['id'] += f'-{n + 1}'
    if not doc['wissen']:
        offen.append('Es liess sich kein Wissen des Hauses lesen (keine Seiten, keine Unterlagen).')

    # ---- Mail-Vorlagen und Absender je Anliegen
    v = rezept.get('vorlagen')
    if v and weg(v['ordner']).is_dir():
        zu = _konstante(weg(v['zuordnung'][0]), v['zuordnung'][1]) or {}
        for art in ARTEN:
            if art not in zu:
                continue
            nr, absender = zu[art]
            texte = {}
            for sp in sorted(os.listdir(weg(v['ordner']))):
                p = weg(v['ordner']) / sp / nr / 'template.html'
                if len(sp) == 2 and p.exists():
                    texte[sp] = _vorlage_text(p)
            if texte:
                doc['vorlagen'][art] = {'nr': nr, 'texte': texte}
                doc['haus']['absender'][art] = absender
        quellen.append(v['ordner'] + '/ (Mail-Vorlagen)')
    for art in ARTEN:
        if art not in doc['vorlagen']:
            offen.append(f'Für Anfragen der Art «{art}» liegt keine Mail-Vorlage des Hauses vor. Antwortentwürfe entstehen dann ohne Vorlage.')

    # ---- Fragen, die es im Projekt schon gibt (Probeläufe; keine Fragen von Gästen)
    p = rezept.get('probefragen')
    if p and weg(p['datei']).exists():
        d = json.loads(weg(p['datei']).read_text(encoding='utf-8'))
        paare = [(f, a) for f, a in d.get('fragen', [])]
        for k in ('film', 'wetter'):
            if d.get(k):
                a = d[k][1]
                paare.append((d[k][0], a.get('text', '') if isinstance(a, dict) else a))
        for i, (f, a) in enumerate(paare):
            doc['probefragen'].append({'frage': f, 'antwort': a, 'zeit': f"{p['tag']}T12:00:{i:02d}"})
        quellen.append(os.path.basename(p['datei']))
    else:
        offen.append('Im Projekt des Hauses liegen keine gespeicherten Fragen. «Das wurde gefragt» beginnt leer.')
    offen.append('Fragen echter Gäste liegen im Online-Speicher der Häuser und sind hier nicht eingelesen. Das Fenster für Gäste auf der Website ist noch nicht an dieses Werkzeug angeschlossen.')
    doc['eingelesen'] = {'zeit': time.strftime('%Y-%m-%dT%H:%M:%S'), 'quellen': quellen, 'offen': offen}
    return doc


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    d = lies(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == 'grundstand':
        sys.path.insert(0, str(WURZEL / 'unterbau'))
        import speicher  # noqa: E402
        speicher.grundstand_setzen(sys.argv[1], 'gaeste', d, 'einlesen')
        print('Grundstand gesetzt.')
    zeichen = sum(len(a['text']) for a in d['wissen'])
    print(json.dumps({'haus': d['haus'], 'karten': d['karten'], 'einstellungen': d['einstellungen'], 'vorlagen': {k: (v['nr'], sorted(v['texte'])) for k, v in d['vorlagen'].items()},
                      'probefragen': len(d['probefragen']), 'eingelesen': d['eingelesen']}, ensure_ascii=False, indent=1))
    print(f'{len(d["wissen"])} Abschnitte, {zeichen:,} Zeichen')
    for a in d['wissen']:
        print(f'  {a["art"]:9} {len(a["text"]):7,}  {a["id"]:44} {a["titel"][:60]} · {a["quelle"][:50]}')
