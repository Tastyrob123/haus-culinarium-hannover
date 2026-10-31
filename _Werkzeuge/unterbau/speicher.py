"""Speicher · die einzige Stelle, die Daten der Werkzeuge liest und schreibt.

Jedes Werkzeug hat je Haus drei Dinge:
  live      der veröffentlichte Stand
  entwurf   der gespeicherte, noch nicht veröffentlichte Stand
  verlauf   jede frühere veröffentlichte Fassung, zum Zurückholen

Regeln, die hier erzwungen werden (aus den Lehren der Studios):
  · Nichts wird still als leer gelesen. Ist eine Datei beschädigt, kommt die Sicherung
    (.gut) zurück, sonst bricht der Aufruf mit «Beschaedigt» ab.
  · Geschrieben wird erst in eine Nebendatei, dann umbenannt. Der vorige Stand bleibt als .gut.
  · Wer einen Entwurf schreibt, nennt die Kennung des Stands, den er gelesen hat. Hat inzwischen
    jemand anderes geschrieben, gibt es «Konflikt» statt stillem Überschreiben.
  · Zurückholen legt die alte Fassung als Entwurf an. Online geht sie erst mit Veröffentlichen.

Später kommt hier die echte Ablage (Datenbank, Anmeldung, Rechte) dahinter.
Die Funktionen und ihre Antworten bleiben dann dieselben.
"""
import fcntl
import hashlib
import json
import os
import re
import time
from contextlib import contextmanager
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent


def _daten():
    return Path(os.environ.get('WERKZEUGE_DATEN') or WURZEL / 'daten')


class Konflikt(Exception):
    """Der Stand wurde inzwischen von jemand anderem geändert."""


class Beschaedigt(Exception):
    """Eine Datei ist nicht lesbar und es gibt keine Sicherung."""


class Unbekannt(Exception):
    """Haus, Werkzeug oder Fassung gibt es nicht."""


_NAME = re.compile(r'^[a-z0-9][a-z0-9-]{0,40}$')


def _ordner(haus, werkzeug):
    if not _NAME.match(haus or '') or not _NAME.match(werkzeug or ''):
        raise Unbekannt('Haus und Werkzeug: nur Kleinbuchstaben, Ziffern, Bindestrich')
    o = _daten() / haus / werkzeug
    (o / 'verlauf').mkdir(parents=True, exist_ok=True)
    return o


def kennung(daten):
    roh = json.dumps(daten, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(roh.encode('utf-8')).hexdigest()[:16]


@contextmanager
def _sperre(o):
    with open(o / '.sperre', 'w') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def _lies(pfad):
    """None, wenn es die Datei nie gab. Beschädigt → Sicherung, sonst Abbruch."""
    gut = pfad.with_suffix(pfad.suffix + '.gut')
    if not pfad.exists():
        if gut.exists():
            raise Beschaedigt(f'{pfad.name} fehlt, Sicherung {gut.name} liegt vor')
        return None
    try:
        return json.loads(pfad.read_text(encoding='utf-8'))
    except (ValueError, OSError):
        if gut.exists():
            try:
                daten = json.loads(gut.read_text(encoding='utf-8'))
            except (ValueError, OSError):
                raise Beschaedigt(f'{pfad.name} und ihre Sicherung sind nicht lesbar')
            _schreib(pfad, daten, sichern=False)
            # nie still: die Sicherung ist der Stand VOR der letzten Änderung, das steht im Protokoll
            o = pfad.parent.parent if pfad.parent.name == 'verlauf' else pfad.parent
            _vermerk(o, 'aus-sicherung', 'speicher', datei=pfad.name)
            return daten
        raise Beschaedigt(f'{pfad.name} ist nicht lesbar, keine Sicherung')


def _schreib(pfad, daten, sichern=True):
    neben = pfad.with_suffix(pfad.suffix + '.neu')
    with open(neben, 'w', encoding='utf-8') as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
        f.flush()
        os.fsync(f.fileno())
    if sichern and pfad.exists():
        os.replace(pfad, pfad.with_suffix(pfad.suffix + '.gut'))
    os.replace(neben, pfad)


def _vermerk(o, was, wer, **mehr):
    zeile = {'zeit': time.strftime('%Y-%m-%dT%H:%M:%S'), 'was': was, 'wer': wer or '', **mehr}
    with open(o / 'protokoll.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(zeile, ensure_ascii=False) + '\n')


def _stand(o):
    live = _lies(o / 'live.json')
    entwurf = _lies(o / 'entwurf.json')
    return {
        'live': live,
        'entwurf': entwurf,
        'kennung_live': kennung(live) if live is not None else None,
        'kennung_entwurf': kennung(entwurf) if entwurf is not None else None,
        'offen': entwurf is not None and (live is None or kennung(entwurf) != kennung(live)),
    }


def lesen(haus, werkzeug):
    """Der ganze Stand eines Werkzeugs. «offen» sagt, ob ein Entwurf vom Live-Stand abweicht."""
    return _stand(_ordner(haus, werkzeug))


def grundstand_setzen(haus, werkzeug, daten, wer=''):
    """Erster Stand eines Werkzeugs (Einlesen aus dem Haus). Nur, solange es keinen gibt."""
    o = _ordner(haus, werkzeug)
    with _sperre(o):
        if _lies(o / 'live.json') is not None:
            raise Konflikt('Es gibt schon einen veröffentlichten Stand')
        _schreib(o / 'live.json', daten)
        _vermerk(o, 'grundstand', wer, kennung=kennung(daten))
    return lesen(haus, werkzeug)


def entwurf_schreiben(haus, werkzeug, daten, erwartet=None, wer=''):
    """Speichert als Entwurf. «erwartet» ist die Kennung, die der Schreibende zuletzt gelesen hat
    (kennung_entwurf, oder kennung_live, wenn es noch keinen Entwurf gab)."""
    o = _ordner(haus, werkzeug)
    with _sperre(o):
        s = _stand(o)
        jetzt = s['kennung_entwurf'] or s['kennung_live']
        if jetzt is not None and erwartet != jetzt:
            raise Konflikt('Der Stand wurde inzwischen geändert')
        _schreib(o / 'entwurf.json', daten)
        _vermerk(o, 'entwurf', wer, kennung=kennung(daten))
    return lesen(haus, werkzeug)


def entwurf_verwerfen(haus, werkzeug, wer=''):
    o = _ordner(haus, werkzeug)
    with _sperre(o):
        for name in ('entwurf.json', 'entwurf.json.gut'):
            if (o / name).exists():
                (o / name).unlink()
        _vermerk(o, 'verworfen', wer)
    return lesen(haus, werkzeug)


def veroeffentlichen(haus, werkzeug, wer='', notiz=''):
    """Entwurf wird Live-Stand. Der vorige Live-Stand kommt in den Verlauf."""
    o = _ordner(haus, werkzeug)
    with _sperre(o):
        s = _stand(o)
        if s['entwurf'] is None or not s['offen']:
            raise Konflikt('Nichts geändert, nichts veröffentlicht')
        if s['live'] is not None:
            fassung = time.strftime('%Y%m%d-%H%M%S') + '-' + s['kennung_live']
            _schreib(o / 'verlauf' / (fassung + '.json'),
                     {'fassung': fassung, 'abgeloest': time.strftime('%Y-%m-%dT%H:%M:%S'),
                      'wer': wer or '', 'notiz': notiz or '', 'daten': s['live']}, sichern=False)
        _schreib(o / 'live.json', s['entwurf'])
        for name in ('entwurf.json', 'entwurf.json.gut'):
            if (o / name).exists():
                (o / name).unlink()
        _vermerk(o, 'veroeffentlicht', wer, kennung=s['kennung_entwurf'], notiz=notiz or '')
    return lesen(haus, werkzeug)


def verlauf(haus, werkzeug):
    """Frühere veröffentlichte Fassungen, neueste zuerst, ohne die Daten selbst."""
    o = _ordner(haus, werkzeug)
    liste = []
    for p in sorted((o / 'verlauf').glob('*.json'), reverse=True):
        f = _lies(p)
        liste.append({k: f.get(k) for k in ('fassung', 'abgeloest', 'wer', 'notiz')})
    return liste


def fassung_lesen(haus, werkzeug, fassung):
    o = _ordner(haus, werkzeug)
    if not re.match(r'^[0-9]{8}-[0-9]{6}-[0-9a-f]{16}$', fassung or ''):
        raise Unbekannt('Fassung unbekannt')
    f = _lies(o / 'verlauf' / (fassung + '.json'))
    if f is None:
        raise Unbekannt('Fassung unbekannt')
    return f


def zurueckholen(haus, werkzeug, fassung, wer=''):
    """Legt eine frühere Fassung als Entwurf an. Online erst mit veroeffentlichen()."""
    daten = fassung_lesen(haus, werkzeug, fassung)['daten']
    o = _ordner(haus, werkzeug)
    with _sperre(o):
        _schreib(o / 'entwurf.json', daten)
        _vermerk(o, 'zurueckgeholt', wer, fassung=fassung)
    return lesen(haus, werkzeug)


def protokoll(haus, werkzeug, n=50):
    """Die letzten n Vermerke: wer hat wann was getan."""
    p = _ordner(haus, werkzeug) / 'protokoll.jsonl'
    if not p.exists():
        return []
    zeilen = p.read_text(encoding='utf-8').splitlines()[-n:]
    return [json.loads(z) for z in reversed(zeilen) if z.strip()]
