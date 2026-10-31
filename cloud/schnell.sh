#!/usr/bin/env bash
# Schnelle Prüfung eines Werkzeugs in der Cloud (31.10.2026): tor-schnell.js mit sinnvoller Abdeckung –
# Start, jeder Navigationspunkt, jeder Reiter, jedes Fenster, je Gruppe drei Stücke, höchstens 40 Zustände, zwei Ebenen tief,
# jeder Zustand in 1440/1280/1000/390. Kein «jeder Zustand»-Lauf mehr (Robert 31.10.: «die sowieso kein Schwein jemals öffnet»).
# Aufruf: cloud/schnell.sh <k> [max=40] [tiefe=2]     Ergebnis: aus/<k>/ (inventar.json, bilder/, stich-*.json, stich-*/)
set -uo pipefail
K="$1"; MAX="${2:-40}"; TIEFE="${3:-2}"
H="$(python3 -c "import json;print(json.load(open('cloud/haus.json'))['tor_ziele'])")"
mkdir -p aus aus/_zeiten; t0=$(date +%s)
TOR_NEUSTART=30 timeout 60m node _Werkzeuge/abnahme-tor/tor-schnell.js "$H" aus --nur "$K" --max "$MAX" --tiefe "$TIEFE" --breiten 1440,1280,1000,390 > "aus/$K.log" 2>&1; rc=$?
n=$(python3 -c "import json;print(len(json.load(open('aus/$K/inventar.json'))['zustaende']))" 2>/dev/null || echo 0)
echo "{\"job\":\"schnell\",\"k\":\"$K\",\"zustaende\":$n,\"sek\":$(( $(date +%s) - t0 )),\"ende\":$rc}" > "aus/_zeiten/schnell-$K.json"
echo "$K: $n Zustände in $(( ($(date +%s) - t0) / 60 )) min (Ende $rc)"; tail -2 "aus/$K.log"
