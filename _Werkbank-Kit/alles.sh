#!/bin/bash
# Baut das ganze Werkbank-Paket eines Hauses:  bash alles.sh "<Projektordner>" [--ohne-aufnahmen]
# Voraussetzung: der Vorschau-Server des Projekts läuft (serve.py, Port in _werkbank/haus.py) und _werkbank/ enthält
#   haus.py (Inhalt), papier.py (Drucksachen und Etiketten), satz_daten.py (Unterlagen), feed_daten.py (Feed).
set -e
K="$(cd "$(dirname "$0")" && pwd)"; P="$(cd "$1" && pwd)"; cd "$P"
export PYTHONPATH="$K"
python3 "$K/kern.py" "$P"                       # Plan für die Aufnahmen, Gestaltung nach werkbank/
python3 "$K/schriften.py" "$P" > /dev/null      # feste Schriftschnitte für den Druck
[ "$2" = "--ohne-aufnahmen" ] || node "$K/ansicht.js" "$P"   # jede Seite am Rechner und am Handy (dauert einige Minuten)
python3 "$K/satz.py" "$P"; node "$K/satz_druck.js" "$P"; python3 "$K/satz_pruefe.py" "$P"   # Unterlagen setzen, drucken, Wortlaut prüfen
python3 "$K/unterlagen.py" "$P"                 # Seite «Unterlagen»
python3 _werkbank/papier.py "$P"; node "$K/papier_druck.js" "$P"; python3 "$K/papier_seiten.py" "$P"   # Drucksachen und Etiketten
python3 "$K/feed.py" "$P"; node "$K/feed_druck.js" "$P"; python3 "$K/feed.py" "$P"; node "$K/feed_druck.js" "$P" --handy   # Feed
python3 "$K/material.py" "$P"                   # Ordner «Material»
node "$K/ziele.js" "$P"                         # Vorschaubilder für die Link-Galerie
python3 "$K/bau.py" "$P"                        # die Werkbank
echo "fertig: http://localhost:$(python3 -c "import json;print(json.load(open('_werkbank/plan.json'))['port'])")/werkbank/"
