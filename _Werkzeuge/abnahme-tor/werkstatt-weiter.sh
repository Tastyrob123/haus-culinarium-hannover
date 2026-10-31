#!/bin/zsh
# Abnahme-Tor · Fortsetzung eines Werkstatt-Laufs nach dem Inventar (Oberchef 30.10. 13:25: Speicher voll → Stichproben in 2 statt 4 Teilen,
# 4 erst wieder bei Last unter 30). Wartet auf das laufende Inventar (PID), dann Stichproben, Messlauf, Bewegung.
# Aufruf: ./werkstatt-weiter.sh <ausgabe> <inventar-pid>
cd "$(dirname "$0")"; W="$1"; P="$2"; k=plakatwerkstatt
while kill -0 $P 2>/dev/null; do sleep 20; done
grep -q "HÄNGER" "$W/$k.log" && { echo "$(date +%H:%M) HÄNGER im Inventar, keine Stichproben" >> "$W/stand.out"; exit 3; }
echo "$(date +%H:%M) INVENTAR" >> "$W/stand.out"
last() { sysctl -n vm.loadavg | awk '{print int($2)}'; }
for g in 1000x650 390x844 1280x800; do
  while [ $(last) -ge 60 ]; do sleep 30; done
  n=2; [ $(last) -lt 40 ] && n=4
  for t in $(seq 1 $n); do caffeinate -i node tor.js ziele-culinarium.json "$W" --nur $k --stichprobe $g --jede 1 --stichmax 900 --teil $t/$n >> "$W/$k-$g-$t.log" 2>&1 & done; wait
  echo "$(date +%H:%M) STICH $g ($n Teile)" >> "$W/stand.out"
done
# Bewegung und Messlauf auch bei hoher Last (Oberchef 30.10. 13:30), Ruckler werden bei ruhiger Last gegengemessen
caffeinate -i zsh ../messlauf/messlauf.sh culinarium "$W/messlauf" --nur $k >> "$W/messlauf.log" 2>&1
caffeinate -i node bewegung-tor.js ziele-culinarium.json "$W/bewegung" --nur $k > "$W/bewegung.out" 2>&1
echo "$(date +%H:%M) FERTIG" >> "$W/stand.out"
