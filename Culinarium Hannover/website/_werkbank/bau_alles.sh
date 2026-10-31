#!/bin/bash
# Werkbank Culinarium: das ganze Paket bauen (Werkbank-Chat 28.10.2026). Vorlage: bau_alles.sh des Schäfli (dort _Werkbank-Kit/alles.sh), ergänzt um die eigenen Schritte.
#   bash website/_werkbank/bau_alles.sh [--ohne-aufnahmen]
# Revier: website/_werkbank/ ist der Projektordner des Kits; die Website liegt eine Ebene höher und wird nur gelesen (assets ist ein Verweis).
# Voraussetzung: Vorschau-Server läuft:  python3 website/_werkbank/serve.py 9088   (Kit unverändert, ein Browser zur Zeit, headless; nichts geht online)
set -e
K=~/Desktop/Website-Projekte/_Werkbank-Kit
P="$(cd "$(dirname "$0")" && pwd)"; cd "$P"
export PYTHONPATH="$K" WB_PORT=9088
python3 _werkbank/druckschrift.py > /dev/null           # feste Schnitte von Fraunces und Urbanist (alle Achsen)
python3 "$K/kern.py" "$P" | grep -v "Schrift fehlt" || true
python3 "$K/schriften.py" "$P" > /dev/null
if [ "$1" != "--ohne-aufnahmen" ]; then
  node _werkbank/ansicht_lang.js "$P"                   # jede Seite am Rechner und am Handy
  node _werkbank/sb_ideen.js                            # Ideen und Gäste-Funktionen
  node _werkbank/sb_werkzeuge.js                        # Bildschirme der sieben Werkzeuge (Adressen aus _werkbank/werkzeuge.json)
fi
python3 _werkbank/sb_heute.py                           # heute (Instagram, Aufnahmen des Spähers) und neu
python3 _werkbank/sb_karten.py; [ -d unterlagen/pdf ] && python3 "$K/unterlagen.py" "$P" | grep -v "Schrift fehlt" || true   # Karten: heute und neu (PDFs von La Carte)
python3 _werkbank/papier.py "$P"; node "$K/papier_druck.js" "$P"; python3 "$K/papier_seiten.py" "$P" | grep -v "Schrift fehlt"   # Drucksachen und Untersetzer
python3 _werkbank/papier_nach.py   # Untersetzer-Seite: «je 94 mm», Du, ß (Tor 4, 30.10.2026)
PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/sticker.py "$P"; PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/beigaben.py "$P"; PYTHONPATH="$K:$P/_werkbank" node _werkbank/sticker_druck.js "$P"; PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/sticker.py "$P" --seite; PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/beigaben.py "$P" --seite   # Sticker und Beigaben (Prüfchat Gestaltung 29.10.2026)
PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/postkarten.py "$P"; PYTHONPATH="$K:$P/_werkbank" node _werkbank/postkarten_druck.js "$P"; PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/postkarten.py "$P" --seite   # 15 Postkarten
python3 "$K/feed.py" "$P"; node "$K/feed_druck.js" "$P"; python3 "$K/feed.py" "$P"; node "$K/feed_druck.js" "$P" --handy   # Feed
PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/feed_leicht.py "$P" 2>/dev/null || PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/feed_leicht.py   # gleich nach feed.py (imprimerie-sperrung 29.10.2026)
node _werkbank/geraete/schirme.js feed                  # Feed im Handy der Werkbank
python3 mails/_src/bau.py; node mails/_src/aufnahme.js  # zehn Mails
python3 "$K/material.py" "$P" | grep -v "Schrift fehlt" || true   # Dateien
PYTHONPATH="$K:$P/_werkbank" python3 _werkbank/material_mehr.py "$P"   # Sticker und Beigaben in den Dateien
node "$K/ziele.js" "$P" || true
node _werkbank/sb_strom.js || true                      # Befund, Prüfbericht, Karte «Ein Vorschlag.», Markenbuch für die Objekte
PYTHONPATH="$K:_werkbank" python3 _werkbank/objekte_bau.py "$P"
python3 "$K/bau.py" "$P" | grep -v "Schrift fehlt"      # die Werkbank (ruft haus.nach_bau: Kapitel, Befund, KI-Seite, Ihr-Form)
node _werkbank/sb_strom.js
PYTHONPATH="$K:_werkbank" python3 _werkbank/objekte_bau.py "$P"
python3 "$K/bau.py" "$P" | grep -v "Schrift fehlt"
echo "fertig: http://127.0.0.1:9088/werkbank/"
