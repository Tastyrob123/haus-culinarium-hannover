#!/usr/bin/env bash
# Ein Werkzeug-Teil auf einem Rechner: Teil-Inventar (WebKit 1440), Neuversuch bei Hänger, danach Stichproben 1280/1000/390 parallel.
# Aufruf: cloud/teil.sh <k> <zweig i/n> <name>    Ergebnis: aus/_teile/<name>/<k>/ (inventar.json, bilder/, stich-*.json, stich-*/)
set -uo pipefail
K="$1"; ZW="$2"; NAME="$3"
H="$(python3 -c "import json;print(json.load(open('cloud/haus.json'))['tor_ziele'])")"
A="aus/_teile/$NAME"; mkdir -p "$A" aus/_zeiten; t0=$(date +%s)
for v in 1 2; do
  timeout 200m node _Werkzeuge/abnahme-tor/tor.js "$H" "$A" --nur "$K" --zweig "$ZW" --browser webkit --groesse 1440x900 > "$A/inventar-v$v.txt" 2>&1; rc=$?
  n=$(python3 -c "import json;print(len(json.load(open('$A/$K/inventar.json'))['zustaende']))" 2>/dev/null || echo 0)
  echo "Inventar Versuch $v: Ende $rc, $n Zustände"; tail -2 "$A/inventar-v$v.txt"
  [ "$rc" = 0 ] && break
  [ "$n" -gt 3 ] && break   # Hänger nach vielen Zuständen: Inventar bleibt, Rest steht als «nicht erreicht» im Protokoll
done
t1=$(date +%s)
if [ -f "$A/$K/inventar.json" ]; then
  for G in 1280x800 1000x650 390x844; do
    EXTRA=""; [ "$G" = "390x844" ] && EXTRA="--jede 1 --stichmax 400"
    ( timeout 150m node _Werkzeuge/abnahme-tor/tor.js "$H" "$A" --nur "$K" --zweig "$ZW" --browser webkit --stichprobe "$G" $EXTRA > "$A/stich-${G%x*}.txt" 2>&1; echo "Stichprobe $G: Ende $?, $(tail -1 "$A/stich-${G%x*}.txt" | cut -c1-80)" ) &
  done
  wait
fi
echo "{\"job\":\"teil\",\"k\":\"$K\",\"teil\":\"$ZW\",\"inventar_sek\":$((t1 - t0)),\"stich_sek\":$(( $(date +%s) - t1 )),\"sek\":$(( $(date +%s) - t0 ))}" > "aus/_zeiten/teil-$NAME.json"
cat "aus/_zeiten/teil-$NAME.json"
