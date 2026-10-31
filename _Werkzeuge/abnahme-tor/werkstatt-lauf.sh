#!/bin/zsh
# Abnahme-Tor · Plakatwerkstatt voll: Inventar 1440 (ein Browser), dann Stichproben 1000 und 390 für alle Zustände in 4 Teilen parallel,
# danach 1280 in 4 Teilen, Messlauf, Bewegung. Aufruf: ./werkstatt-lauf.sh <ausgabe>
cd "$(dirname "$0")"; W="$1"; k=plakatwerkstatt; mkdir -p "$W"
node tor.js ziele-culinarium.json "$W" --nur $k >> "$W/$k.log" 2>&1; echo "$(date +%H:%M) INVENTAR" >> "$W/stand.out"
for g in 1000x650 390x844 1280x800; do
  for t in 1 2 3 4; do node tor.js ziele-culinarium.json "$W" --nur $k --stichprobe $g --jede 1 --stichmax 900 --teil $t/4 >> "$W/$k-$g-$t.log" 2>&1 & done; wait
  echo "$(date +%H:%M) STICH $g" >> "$W/stand.out"
done
zsh ../messlauf/messlauf.sh culinarium "$W/messlauf" --nur $k >> "$W/messlauf.log" 2>&1
node bewegung-tor.js ziele-culinarium.json "$W/bewegung" --nur $k > "$W/bewegung.out" 2>&1
echo "$(date +%H:%M) FERTIG" >> "$W/stand.out"
