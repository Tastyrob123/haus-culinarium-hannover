#!/usr/bin/env bash
# Alle Server des Hauses starten (wie auf Roberts Mac, gleiche Ports) und warten, bis jeder antwortet.
set -uo pipefail
WS="${GITHUB_WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}"
HJ="$WS/cloud/haus.json"
ORD="$WS/$(python3 -c "import json;print(json.load(open('$HJ'))['ordner'])")"
mkdir -p /tmp/server
export WERKZEUGE_DATEN=/tmp/werkzeuge-daten BUREAU_PRUEFLAUF=1 RECEPTION_FORMULAR_GRENZE=999
python3 - "$HJ" <<'PY' > /tmp/server/liste
import json, sys
for s in json.load(open(sys.argv[1]))['server']:
    print(f"{s['port']}\t{s['wo']}\t{s['befehl']}\t{s['pruef']}")
PY
while IFS=$'\t' read -r port wo befehl pruef; do
  ( cd "$ORD/$wo" && nohup $befehl > "/tmp/server/$port.log" 2>&1 & )
done < /tmp/server/liste
fehler=0
while IFS=$'\t' read -r port wo befehl pruef; do
  ok=0
  for i in $(seq 1 60); do
    c=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$port$pruef" || true)
    [ "$c" = "200" ] && { ok=1; break; }; sleep 1
  done
  if [ $ok = 1 ]; then echo "Server $port bereit"; else echo "Server $port antwortet nicht ($c)"; tail -20 "/tmp/server/$port.log"; fehler=1; fi
done < /tmp/server/liste
exit $fehler
