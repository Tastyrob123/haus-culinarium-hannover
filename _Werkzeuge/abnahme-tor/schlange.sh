#!/bin/zsh
# Abnahme-Tor · Warteschlange: ein Lauf nach dem anderen, Start erst bei ruhiger Maschine (Last < 14), damit nichts im Gedränge hängt.
# Aufruf: ./schlange.sh <auftrag> … ; Auftrag = "voll|<ziele>|<ausgabe>|k1,k2" oder "stich390|<ziele>|<ausgabe>|k1,k2"
cd "$(dirname "$0")"
ruhe() { while :; do l=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$l" -lt ${TOR_LAST:-14} ] && return; sleep 30; done; }
for a in "$@"; do
  art=${a%%|*}; r=${a#*|}; ziele=${r%%|*}; r=${r#*|}; aus=${r%%|*}; ks=${r#*|}; mkdir -p "$aus"
  ruhe; echo "$(date +%H:%M) START $art $ks" >> "$aus/schlange.out"
  if [ "$art" = voll ]; then
    TOR_HANDY_ALLE=1 node lauf.js "$ziele" "$aus" --parallel 2 ${(s:,:)ks} >> "$aus/lauf.out" 2>&1
  else
    for k in ${(s:,:)ks}; do node tor.js "$ziele" "$aus" --nur "$k" --stichprobe 390x844 --jede 1 --stichmax 600 >> "$aus/$k.log" 2>&1; done
    zsh ../messlauf/messlauf.sh culinarium "$aus/messlauf" --nur "$ks" >> "$aus/messlauf.log" 2>&1
  fi
  node bewegung-tor.js "$ziele" "$aus/bewegung" --nur "$ks" > "$aus/bewegung.out" 2>&1
  echo "$(date +%H:%M) FERTIG $art $ks" >> "$aus/schlange.out"
done
