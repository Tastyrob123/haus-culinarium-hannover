#!/usr/bin/env python3
"""Probe-Kopie eines Hauses anlegen. Start: python3 werkzeuge/website/probe.py <haus> [--neu]

Die Quelle des Hauses wird nur gelesen. Kopiert wird, was die Beschreibung (haeuser/<haus>.json, Abschnitt «kopie») nennt:
  _probe/<haus>/grundlage/   die Seiten, wie das Haus sie gebaut hat. Wird danach nie mehr verändert
  _probe/<haus>/online/      was «online» wäre: Grundlage + veröffentlichte Schicht. Schreibt nur ausgabe.py
Kopiert wird mit cp -c -R (Kopie ohne Platzverbrauch). Der Ordner _probe kommt nicht in Git.
--neu: vorhandene Kopie ersetzen (nach einem neuen Bau des Hauses). Die Schicht im Speicher bleibt, die Prüfung zeigt, ob jede Änderung ihren Platz noch findet."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parent.parent


def probe_ordner():
    return Path(os.environ.get('WEBSITE_PROBE') or HIER / '_probe')


def kopiere(quelle, ziel):
    ziel.parent.mkdir(parents=True, exist_ok=True)
    if subprocess.run(['cp', '-c', '-R', str(quelle), str(ziel)], capture_output=True).returncode != 0:
        (shutil.copytree if quelle.is_dir() else shutil.copy2)(quelle, ziel)


def lege_an(haus, neu=False):
    b = json.loads((HIER / 'haeuser' / f'{haus}.json').read_text(encoding='utf-8'))
    stamm = json.loads((WURZEL / 'haeuser' / haus / 'haus.json').read_text(encoding='utf-8'))
    quelle = Path(os.path.expanduser(stamm['quelle'])) / (b['kopie'].get('unter') or '')   # unter: Unterordner der gebauten Seiten, falls die Quelle der Projektordner ist
    ziel = probe_ordner() / haus
    if ziel.exists():
        if not neu:
            return f'{haus}: Kopie liegt schon vor ({ziel})'
        shutil.rmtree(ziel)
    seiten = [s['datei'] for s in b['seiten']]
    sprachen = [s['ordner'] for s in b.get('sprachen') or []]
    for teil in ('grundlage', 'online'):
        z = ziel / teil
        z.mkdir(parents=True)
        for n in seiten:
            kopiere(quelle / n, z / n)
        for o in sprachen:
            (z / o).mkdir()
            for n in seiten:
                if (quelle / o / n).exists():
                    kopiere(quelle / o / n, z / o / n)
        for o in b['kopie']['ordner']:
            kopiere(quelle / o, z / o)
    return f'{haus}: {len(seiten)} Seiten, {len(sprachen)} weitere Sprachen, Ordner {", ".join(b["kopie"]["ordner"])} → {ziel}'


if __name__ == '__main__':
    namen = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not namen:
        sys.exit('Haus fehlt: python3 werkzeuge/website/probe.py gasterntal')
    for h in namen:
        print(lege_an(h, '--neu' in sys.argv))
