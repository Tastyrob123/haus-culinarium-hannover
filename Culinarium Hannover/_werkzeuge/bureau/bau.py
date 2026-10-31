#!/usr/bin/env python3
"""Fassungsnummern von Le Bureau (Culinarium) aus dem Inhalt setzen (Master Werkzeug-Bau M20: ?v= nie von Hand, nie nach Datum).
   python3 _werkzeuge/bureau/bau.py      nach jeder Änderung an einer Datei, die index.html oder anleitung.html lädt.
Schreibt nur index.html und anleitung.html dieses Ordners, und nur die Zahl hinter ?v=."""
import hashlib
import re
from pathlib import Path

HIER = Path(__file__).resolve().parent
QUELLEN = {'/assets/oberflaeche/': HIER.parent / 'oberflaeche', '/werkzeuge/website/': Path.home() / 'Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website',
           '/stamm/': Path.home() / 'Desktop/Website-Projekte/_Werkzeuge/stamm'}


def datei(adr):
    for vor, ordner in QUELLEN.items():
        if adr.startswith(vor):
            return ordner / adr[len(vor):]
    return None if adr.startswith('/') else HIER / adr


def stempel(m):
    p = datei(m.group(2))
    if not p or not p.is_file():
        return m.group(0)
    return f'{m.group(1)}{m.group(2)}?v={hashlib.sha1(p.read_bytes()).hexdigest()[:10]}{m.group(4)}'


for name in ('index.html', 'anleitung.html'):
    p = HIER / name
    alt = p.read_text(encoding='utf-8')
    neu = re.sub(r'((?:src|href)=")([^"?#]+\.(?:js|css))(\?v=[^"]*)?(")', stempel, alt)
    if neu != alt:
        p.write_text(neu, encoding='utf-8')
    print(name, len(re.findall(r'\?v=[0-9a-f]{10}"', neu)), 'Dateien mit Fassung aus dem Inhalt')
