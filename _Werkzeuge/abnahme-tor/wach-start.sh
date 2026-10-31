#!/bin/zsh
# Wartet, bis der Mac 10 Minuten am Stück wach ist (keine Schlaf-Lücke zwischen zwei Minuten-Takten), dann voller Werkstatt-Lauf.
cd "$(dirname "$0")"; W="$1"; ok=0
while [ $ok -lt 10 ]; do a=$(date +%s); sleep 60; b=$(date +%s); if [ $((b-a)) -lt 75 ]; then ok=$((ok+1)); else ok=0; fi; done
mkdir -p "$W"; echo "$(date +%H:%M) WACH, Start" >> "$W/stand.out"
TOR_SPUR=1 TOR_HAENGER_MIN=10 caffeinate -i node tor.js ziele-culinarium.json "$W" --nur plakatwerkstatt >> "$W/plakatwerkstatt.log" 2>&1 &
P=$!; TOR_HAENGER_MIN=25 caffeinate -i ./werkstatt-weiter.sh "$W" $P
