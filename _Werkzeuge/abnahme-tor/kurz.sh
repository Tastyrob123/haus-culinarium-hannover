#!/bin/zsh
# Abnahme-Tor, kurzer Umfang (Oberchef 30.10.2026, «Entwurf vor dem Auftrag»): je Werkzeug Start, Rundgang, Anleitung und die
# ersten Ansichten (höchstens ~30 Zustände), WebKit 1440 + 1000 + 390, danach Messlauf. Eines nach dem anderen.
# Aufruf: ./kurz.sh <ziele.json> <ausgabe> <max je Ziel> k1 k2 …
cd "$(dirname "$0")"
ZIELE="$1"; AUS="$2"; MAX="$3"; shift 3; mkdir -p "$AUS"
for k in "$@"; do
  node tor.js "$ZIELE" "$AUS" --nur "$k" --max "$MAX" >> "$AUS/$k.log" 2>&1
  for g in 1000x650 390x844; do node tor.js "$ZIELE" "$AUS" --nur "$k" --stichprobe "$g" --jede 1 --stichmax 60 >> "$AUS/$k.log" 2>&1; done
done
zsh ../messlauf/messlauf.sh culinarium "$AUS/messlauf" --nur "${(j:,:)@}" >> "$AUS/messlauf.log" 2>&1
echo "KURZ FERTIG $(date +%H:%M)" >> "$AUS/lauf.out"
