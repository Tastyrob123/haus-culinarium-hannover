"""api.py · die eigenen Wege des Werkzeugs «karten» (La Carte · Die Tafel), eingehängt unter /api/x/karten/…

  GET  uebersicht/<haus>             Haus (Name, Welt), Stand der PDF je Karte, Sprachen, Liste der Allergene
  PUT  entwurf/<haus>                {daten, erwartet, wer} · prüft die Form, dann speichert der Speicher den Entwurf
  POST probe/<haus>/<karte>          Probe-PDF aus dem Entwurf (sonst aus dem veröffentlichten Stand), nichts wird abgelegt
  POST veroeffentlichen/<haus>       {erwartet, wer, notiz} · druckt jede geänderte Karte neu, prüft PDF gegen Daten und
                                     die Regeln des Umbruchs, legt die PDF ab und schaltet ERST DANN um
  GET  pdf/<haus>/<karte>            die PDF der veröffentlichten Karte (base64)
  GET  kontrolle/<haus>              prüft den veröffentlichten Stand: Form, PDF vorhanden, PDF = Daten

Alles geht über den Speicher. Die PDF liegen dort je Karte unter «karten-pdf-<karte>» (Kennung der Daten, Seiten, PDF als
base64), weil der Speicher heute nur Daten kennt (STAND.md, Wünsche an den Stamm). Gedruckt wird mit pdf.js: dieselbe
Druckseite und derselbe Satz wie die Vorschau im Werkzeug. Es entsteht keine Datei und es läuft nichts im Hintergrund:
der Druck dauert etwa eine Sekunde je Karte und gehört zur Anfrage.

Fehler: (status, {"fehler": Satz in Alltagssprache, "stichwort": …}). Stichwörter: haus-ohne-karten · karte-unbekannt ·
pruefung · nichts-geaendert · konflikt · druck · umbruch · pdf-ungleich-daten · weg-unbekannt.
"""
import base64
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parent.parent
sys.path.insert(0, str(HIER))
import importlib  # noqa: E402
import modell as M  # noqa: E402
M = importlib.reload(M)   # der Server lädt api.py bei jedem Aufruf frisch; modell.py bliebe sonst bis zu einem Neustart beim alten Stand

W = 'karten'
_NAME = re.compile(r'^[a-z0-9][a-z0-9-]{0,40}$')


class Halt(Exception):
    def __init__(self, status, text, stichwort, **mehr):
        super().__init__(text)
        self.status, self.antwort = status, dict(fehler=text, stichwort=stichwort, **mehr)


def kleid_von(haus):
    """Zeichen, Tapete und Fotos des Hauses aus kleid/<haus>/ (angelegt mit kleid.py, gehört zum Werkzeug wie seine Schriften).
    Ohne Kleid: None. Dann druckt die Karte den Namen des Hauses und das Werkzeug zeigt Anfangsbuchstaben."""
    ordner = HIER / 'kleid' / haus
    if not _NAME.match(haus) or not (ordner / 'kleid.json').exists():
        return None
    try:
        k = json.loads((ordner / 'kleid.json').read_text(encoding='utf-8'))
        svg = (ordner / k['zeichen']).read_text(encoding='utf-8') if k.get('zeichen') else ''
    except (ValueError, OSError, KeyError):
        return None
    return {'zeichen': k.get('zeichen'), 'zeichen_mass': k.get('zeichen_mass'), 'tapete': k.get('tapete'), 'fotos': k.get('fotos') or {},
            'svg': svg, 'kennung': M.kennung({'z': svg, 't': k.get('tapete') or ''})}


def haus_angaben(haus):
    """Name und Welt des Hauses aus haeuser/<haus>/haus.json (nur gelesen). Fehlt die Datei: Kennung als Name, Welt Grandhotel.
    «druckname»: was auf der Karte als Name steht; leer, wenn das Haus ein Zeichen hat (dann steht das Zeichen da)."""
    aus = {'kennung': haus, 'name': haus, 'welt': 'grand'}
    p = WURZEL / 'haeuser' / haus / 'haus.json'
    if _NAME.match(haus) and p.exists():
        try:
            h = json.loads(p.read_text(encoding='utf-8'))
            aus['name'] = str(h.get('name') or haus)[:120]
            aus['welt'] = 'land' if h.get('welt') == 'land' else 'grand'
        except (ValueError, OSError):
            pass
    k = kleid_von(haus)
    aus['kleid'] = k
    aus['druckname'] = '' if k and k['svg'] else aus['name']
    aus['kleid_kennung'] = k['kennung'] if k else ''
    return aus


def _oeffentlich(h):
    """Angaben zum Haus für das Werkzeug: ohne die Zeichnung selbst (die holt es als Datei)."""
    k = h.get('kleid')
    return {'kennung': h['kennung'], 'name': h['name'], 'welt': h['welt'],
            'kleid': {x: k[x] for x in ('zeichen', 'zeichen_mass', 'tapete', 'fotos')} if k else None}


def _stand(sp, haus):
    if not _NAME.match(haus or ''):
        raise Halt(404, 'Dieses Haus gibt es nicht.', 'haus-ohne-karten')
    s = sp.lesen(haus, W)
    if s['live'] is None:
        raise Halt(404, 'Für dieses Haus sind noch keine Karten eingelesen.', 'haus-ohne-karten')
    return s


def _karte(doc, kid):
    for e in doc['karten']:
        if e['id'] == kid:
            return e
    raise Halt(404, 'Diese Karte gibt es nicht.', 'karte-unbekannt')


def drucke(karte, haus):
    """Karte → (PDF als Bytes, Bericht). Bricht mit Halt ab, wenn der Druck nicht gelingt."""
    k = haus.get('kleid') or {}
    ein = json.dumps({'karte': karte, 'welt': haus['welt'], 'haus': haus['name'], 'allergene': M.ALLERGENE, 'zeichen': k.get('svg') or '',
                      'zeichen_mass': k.get('zeichen_mass'), 'tapete': f"kleid/{haus['kennung']}/{k['tapete']}" if k.get('tapete') else ''}, ensure_ascii=False)
    try:
        r = subprocess.run(['node', str(HIER / 'pdf.js')], input=ein.encode('utf-8'), capture_output=True, timeout=120)
        aus = json.loads(r.stdout.decode('utf-8') or '{}')
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError) as f:
        raise Halt(500, 'Die PDF liess sich nicht drucken.', 'druck', einzelheit=str(f)[:300])
    if 'pdf' not in aus:
        raise Halt(500, 'Die PDF liess sich nicht drucken.', 'druck', einzelheit=str(aus.get('fehler') or r.stderr.decode('utf-8', 'replace'))[:300])
    return base64.b64decode(aus['pdf']), aus


def drucke_und_pruefe(karte, haus):
    """Druckt und prüft. Rückgabe (pdf, bericht). bericht['ok'] sagt, ob PDF, Daten und Umbruch stimmen."""
    pdf, aus = drucke(karte, haus)
    try:
        p = M.pdf_gegen_daten(pdf, karte, haus['druckname'])
    except RuntimeError as f:
        raise Halt(500, str(f), 'druck')
    bericht = {'seiten': p['seiten'], 'woerter': p['woerter'], 'pdf_gleich_daten': p['ok'], 'fehlt': p['fehlt'], 'dazu': p['dazu'],
               'regeln': aus.get('regeln') or [], 'ueberlauf': aus.get('ueberlauf') or []}
    bericht['ok'] = p['ok'] and not bericht['regeln'] and not bericht['ueberlauf'] and p['seiten'] == aus.get('seiten')
    return pdf, bericht


def _pdf_lesen(sp, haus, kid):
    return sp.lesen(haus, f'{W}-pdf-{kid}')['live']


def _pdf_ablegen(sp, haus, kid, eintrag, wer):
    schluessel = f'{W}-pdf-{kid}'
    s = sp.lesen(haus, schluessel)
    if s['live'] is None:
        sp.grundstand_setzen(haus, schluessel, eintrag, wer)
    elif s['live'].get('kennung') != eintrag['kennung']:
        sp.entwurf_schreiben(haus, schluessel, eintrag, s['kennung_entwurf'] or s['kennung_live'], wer)
        sp.veroeffentlichen(haus, schluessel, wer, 'PDF neu gedruckt')


def _eintrag(pdf, bericht, kennung):
    return {'kennung': kennung, 'seiten': bericht['seiten'], 'erzeugt': time.strftime('%Y-%m-%dT%H:%M:%S'), 'pdf': base64.b64encode(pdf).decode('ascii')}


def _abbruch_text(name, b):
    if b['regeln']:
        return 422, f'«{name}» lässt sich so nicht drucken: ' + b['regeln'][0], 'umbruch'
    if b['ueberlauf']:
        return 422, f'«{name}» lässt sich so nicht drucken: ' + b['ueberlauf'][0], 'umbruch'
    return 422, f'Die gedruckte Karte «{name}» zeigt nicht genau die Daten. Es wurde nichts veröffentlicht.', 'pdf-ungleich-daten'


# ---------- die Wege ----------

def uebersicht(sp, haus):
    s = _stand(sp, haus)
    h = haus_angaben(haus)
    pdf = {}
    for e in s['live']['karten']:
        alt = _pdf_lesen(sp, haus, e['id'])
        pdf[e['id']] = {'vorhanden': alt is not None, 'passt': bool(alt) and alt['kennung'] == M.druck_kennung(e['karte'], h['welt'], h['name'], h['kleid_kennung']),
                        'seiten': alt['seiten'] if alt else 0, 'erzeugt': alt['erzeugt'] if alt else ''}
    # Ein Entwurf, der am Werkzeug vorbei in falscher Form gespeichert wurde, darf die Übersicht nicht zu Fall bringen
    kaputt = s['entwurf'] is not None and bool(M.pruefe(s['entwurf'], haus))
    arbeit = s['entwurf'] if s['entwurf'] is not None and not kaputt else s['live']
    return 200, {'haus': _oeffentlich(h), 'pdf': pdf, 'sprachen': M.sprachen_stand(arbeit), 'allergene': M.ALLERGENE, 'satz': M.SATZ_VERSION, 'entwurf_kaputt': kaputt}


def entwurf(sp, haus, k):
    s = _stand(sp, haus)
    d = k.get('daten')
    f = M.pruefe(d, haus)
    if f:
        raise Halt(422, f, 'pruefung')
    jetzt = s['kennung_entwurf'] or s['kennung_live']
    if k.get('erwartet') != jetzt:
        raise sp.Konflikt('Inzwischen hat jemand anderes gespeichert. Ihre Änderung wurde nicht gespeichert, nichts wurde überschrieben.')
    wer = str(k.get('wer') or '')[:80]
    if sp.kennung(d) == jetzt:
        return 200, {'geaendert': False, 'stand': s}
    if sp.kennung(d) == s['kennung_live']:
        return 200, {'geaendert': True, 'wie_veroeffentlicht': True, 'stand': sp.entwurf_verwerfen(haus, W, wer)}
    return 200, {'geaendert': True, 'stand': sp.entwurf_schreiben(haus, W, d, k.get('erwartet'), wer)}


def probe(sp, haus, kid):
    s = _stand(sp, haus)
    doc = s['entwurf'] if s['entwurf'] is not None else s['live']
    e = _karte(doc, kid)
    pdf, bericht = drucke_und_pruefe(e['karte'], haus_angaben(haus))
    return 200, {'pdf': base64.b64encode(pdf).decode('ascii'), 'aus': 'entwurf' if s['entwurf'] is not None else 'veroeffentlicht', 'bericht': bericht,
                 'datei': f'{haus}-{kid}-probe.pdf'}


def veroeffentlichen(sp, haus, k):
    s = _stand(sp, haus)
    if s['entwurf'] is None or not s['offen']:
        raise Halt(409, 'Nichts geändert, nichts veröffentlicht.', 'nichts-geaendert')
    if k.get('erwartet') and k['erwartet'] != s['kennung_entwurf']:
        raise sp.Konflikt('Der Entwurf hat sich inzwischen geändert. Bitte neu laden und noch einmal ansehen.')
    f = M.pruefe(s['entwurf'], haus)
    if f:
        raise Halt(422, f, 'pruefung')
    h = haus_angaben(haus)
    wer, notiz = str(k.get('wer') or '')[:80], str(k.get('notiz') or '')[:300]
    berichte, neu = [], []
    for e in s['entwurf']['karten']:
        dk = M.druck_kennung(e['karte'], h['welt'], h['name'], h['kleid_kennung'])
        alt = _pdf_lesen(sp, haus, e['id'])
        if alt and alt['kennung'] == dk:
            berichte.append({'id': e['id'], 'name': e['karte']['name'], 'neu_gedruckt': False, 'seiten': alt['seiten']})
            continue
        pdf, b = drucke_und_pruefe(e['karte'], h)
        if not b['ok']:
            status, text, stichwort = _abbruch_text(e['karte']['name'], b)
            raise Halt(status, text, stichwort, karte=e['id'], bericht=b)
        neu.append((e['id'], _eintrag(pdf, b, dk)))
        berichte.append({'id': e['id'], 'name': e['karte']['name'], 'neu_gedruckt': True, 'seiten': b['seiten'], 'woerter': b['woerter']})
    # Geprüft ist genau der Entwurf, der oben gelesen wurde. Hat ihn inzwischen jemand geändert, wird nicht umgeschaltet.
    if sp.lesen(haus, W)['kennung_entwurf'] != s['kennung_entwurf']:
        raise sp.Konflikt('Während des Drucks hat jemand den Entwurf geändert. Es wurde nichts veröffentlicht.')
    for kid, eintrag in neu:
        _pdf_ablegen(sp, haus, kid, eintrag, wer)
    return 200, {'stand': sp.veroeffentlichen(haus, W, wer, notiz), 'bericht': berichte}


def pdf(sp, haus, kid):
    s = _stand(sp, haus)
    e = _karte(s['live'], kid)
    h = haus_angaben(haus)
    dk = M.druck_kennung(e['karte'], h['welt'], h['name'], h['kleid_kennung'])
    alt = _pdf_lesen(sp, haus, kid)
    nachgedruckt = False
    if not alt or alt['kennung'] != dk:
        # Es liegt keine PDF zum veröffentlichten Stand vor (erster Abruf, oder am Werkzeug vorbei veröffentlicht): drucken, prüfen, ablegen
        roh, b = drucke_und_pruefe(e['karte'], h)
        if not b['ok']:
            status, text, stichwort = _abbruch_text(e['karte']['name'], b)
            raise Halt(status, text, stichwort, karte=kid, bericht=b)
        alt = _eintrag(roh, b, dk)
        _pdf_ablegen(sp, haus, kid, alt, 'karten')
        nachgedruckt = True
    return 200, {'pdf': alt['pdf'], 'seiten': alt['seiten'], 'erzeugt': alt['erzeugt'], 'kennung': alt['kennung'], 'nachgedruckt': nachgedruckt, 'datei': f'{haus}-{kid}.pdf'}


def kontrolle(sp, haus):
    s = _stand(sp, haus)
    h = haus_angaben(haus)
    punkte = [{'was': 'Form der Daten', 'gut': not M.pruefe(s['live'], haus), 'einzelheit': M.pruefe(s['live'], haus)}]
    if s['entwurf'] is not None:
        punkte.append({'was': 'Form des Entwurfs', 'gut': not M.pruefe(s['entwurf'], haus), 'einzelheit': M.pruefe(s['entwurf'], haus)})
    for e in s['live']['karten']:
        alt = _pdf_lesen(sp, haus, e['id'])
        name = e['karte']['name']
        if not alt:
            punkte.append({'was': f'PDF «{name}»', 'gut': False, 'einzelheit': 'Zu dieser Karte liegt noch keine PDF vor. Sie entsteht beim ersten Öffnen oder Veröffentlichen.'})
            continue
        passt = alt['kennung'] == M.druck_kennung(e['karte'], h['welt'], h['name'], h['kleid_kennung'])
        try:
            p = M.pdf_gegen_daten(base64.b64decode(alt['pdf']), e['karte'], h['druckname']) if passt else None
        except RuntimeError as f:
            raise Halt(500, str(f), 'druck')
        punkte.append({'was': f'PDF «{name}»', 'gut': passt and p['ok'], 'seiten': alt['seiten'],
                       'einzelheit': '' if passt and p['ok'] else ('Die PDF gehört zu einem früheren Stand.' if not passt else f'PDF und Daten weichen ab: fehlt {p["fehlt"]}, zu viel {p["dazu"]}')})
    return 200, {'gut': all(p['gut'] for p in punkte), 'punkte': punkte}


def bearbeite(methode, rest, daten, speicher):
    try:
        was = rest[0] if rest else ''
        if was == 'uebersicht' and len(rest) == 2 and methode == 'GET':
            return uebersicht(speicher, rest[1])
        if was == 'entwurf' and len(rest) == 2 and methode == 'PUT':
            return entwurf(speicher, rest[1], daten or {})
        if was == 'probe' and len(rest) == 3 and methode == 'POST':
            return probe(speicher, rest[1], rest[2])
        if was == 'veroeffentlichen' and len(rest) == 2 and methode == 'POST':
            return veroeffentlichen(speicher, rest[1], daten or {})
        if was == 'pdf' and len(rest) == 3 and methode == 'GET':
            return pdf(speicher, rest[1], rest[2])
        if was == 'kontrolle' and len(rest) == 2 and methode == 'GET':
            return kontrolle(speicher, rest[1])
        return 404, {'fehler': 'Diesen Weg kennt das Werkzeug nicht.', 'stichwort': 'weg-unbekannt'}
    except Halt as f:
        return f.status, f.antwort
