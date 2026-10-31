#!/bin/zsh
# Messlauf · ein Befehl: ./messlauf.sh [haus] [ordner] [weitere Schalter für messlauf.js]
#   ./messlauf.sh culinarium                → _Oberchef/zeigen/<haus>/messlauf-<datum>/lauf-<zeit>/ (funde.json, bilder/, tafel.html)
#   ./messlauf.sh culinarium "" --browser webkit --groesse 390 --nur schaufenster
# Pflicht vor jeder Übergabe an Robert (Oberchef 29.10.2026). Browser unsichtbar, ein Browser zur Zeit, nur GET; Schreibwege werden abgefangen.
HIER=${0:A:h}
HAUS=${1:-culinarium}; shift 2>/dev/null
AUS=${1:-}; shift 2>/dev/null
[ -z "$AUS" ] && AUS=~/Desktop/Website-Projekte/_Oberchef/zeigen/$HAUS/messlauf-$(date +%d%m)/lauf-$(date +%H%M)
mkdir -p "$AUS"
node "$HIER/messlauf.js" "$HIER/ziele-$HAUS.json" "$AUS" "$@" | tee "$AUS/lauf.log"
python3 "$HIER/tafel.py" "$AUS"
echo "Tafel: $AUS/tafel.html"
