#!/bin/zsh
# Dokument-Tor: setzt jedes Dokument der Werkstatt (Vorlagen, Entwerfen-Muster, Muster, Vorschläge) und prüft es; danach Auswertung.
# Aufruf: ./dok-lauf.sh <werkstatt-url> <ausgabe> <stilblatt.json> <werkstatt-ordner>
cd "$(dirname "$0")"
URL="$1"; AUS="$2"; STIL="$3"; WS="$4"; mkdir -p "$AUS"
python3 entwerfen.py "$WS" "$AUS/entwerfen.json"
node dok-tor.js "$URL" "$AUS" --stilblatt "$STIL" > "$AUS/lauf.log" 2>&1
echo "DOK FERTIG $(date +%H:%M)"
