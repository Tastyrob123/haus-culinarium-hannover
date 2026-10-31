#!/bin/zsh
# Abnahme-Tor · schneller Volllauf eines Hauses (31.10.2026): je Werkzeug tor-schnell.js (WebKit, alle Breiten im selben Fenster),
# höchstens P Werkzeuge gleichzeitig (Speicher: ein WebKit braucht 400–800 MB), danach bewegung-tor.js und die Auswertung je Werkzeug.
# Aufruf: ./lauf-schnell.sh <haus> <lauf-name> [P=3] [k1 k2 …]      Beispiel: ./lauf-schnell.sh culinarium 0111 3
#   Ergebnis: <Haus-Ordner>/_qa/abnahme-tor/<lauf-name>/ (Rohdaten) und _Oberchef/zeigen/<haus>/abnahme-tor/<lauf-name>/ (Tafeln)
#   Nur ein Werkzeug gleich nach dem Bau: ./lauf-schnell.sh culinarium 0111-werkbank 1 werkbank
cd "$(dirname "$0")"
HAUS="$1"; LAUF="$2"; P="${3:-3}"; shift 3 2>/dev/null
ZIELE="ziele-$HAUS.json"
HAUSORDNER=$(python3 -c "import json;print(json.load(open('$ZIELE'))['haus'])")
QA="$HOME/Desktop/Website-Projekte/$HAUSORDNER/_qa/abnahme-tor/$LAUF"
TAFEL="$HOME/Desktop/Website-Projekte/_Oberchef/zeigen/$HAUS/abnahme-tor/$LAUF"
mkdir -p "$QA" "$TAFEL"
if [ $# -gt 0 ]; then KS=("$@"); else KS=($(python3 -c "import json;print(' '.join(z['k'] for z in json.load(open('$ZIELE'))['ziele']))")); fi
T0=$(date +%s); echo "$(date +%H:%M) START $LAUF: ${KS[*]} (je $P gleichzeitig)" | tee -a "$QA/lauf.out"
# Warteschlange: je Werkzeug ein Prozess, höchstens P gleichzeitig (xargs -P; «jobs» zählt in Skripten nicht zuverlässig, 31.10.: 25 Browser auf einmal)
export ZIELE QA
printf '%s\n' "${KS[@]}" | xargs -P "$P" -I{} zsh -c 't=$(date +%s); caffeinate -i node tor-schnell.js "$ZIELE" "$QA" --nur "{}" >> "$QA/{}.log" 2>&1; echo "$(date +%H:%M) {} fertig in $(( ($(date +%s)-t)/60 )) min" >> "$QA/lauf.out"'
echo "$(date +%H:%M) TORE FERTIG nach $(( ($(date +%s)-T0)/60 )) min" | tee -a "$QA/lauf.out"
# Bewegung (Kriterien 34 und 37), ein Browser, alle Ziele
caffeinate -i node bewegung-tor.js "$ZIELE" "$QA/bewegung" --nur "${(j:,:)KS}" > "$QA/bewegung.out" 2>&1
echo "$(date +%H:%M) BEWEGUNG FERTIG" | tee -a "$QA/lauf.out"
# Dokumente der Plakatwerkstatt (dok-tor.js, ca. 2 min für 330 Blätter), wenn das Haus eine Werkstatt und ein Stilblatt hat
WS_URL=$(python3 -c "import json;z=[z for z in json.load(open('$ZIELE'))['ziele'] if z['k']=='plakatwerkstatt'];print(z[0]['url'] if z else '')")
STIL=$(python3 -c "import json;print(json.load(open('$ZIELE')).get('stilblatt',''))")
if [ -n "$WS_URL" ] && [ -f "$STIL" ] && { [ $# -eq 0 ] || [[ " ${KS[*]} " == *" plakatwerkstatt "* ]]; }; then
  WS_ORDNER="${STIL%/haeuser/*}"
  caffeinate -i ./dok-lauf.sh "$WS_URL" "$QA/dokumente" "$STIL" "$WS_ORDNER" >> "$QA/lauf.out" 2>&1
  python3 dok-auswertung.py "$QA/dokumente" "$TAFEL/dokumente" --titel "Dokumente $HAUS · $LAUF" >> "$QA/auswertung.out" 2>&1
  echo "$(date +%H:%M) DOKUMENTE FERTIG · http://localhost:8978/haus/_Oberchef/zeigen/$HAUS/abnahme-tor/$LAUF/dokumente/index.html" | tee -a "$QA/lauf.out"
fi
# Auswertung: eine Tafel je Werkzeug und eine über alles
python3 auswertung.py "$QA" "$TAFEL" --titel "Abnahme-Tor $HAUS · $LAUF" $( [ -f "gegenprobe-$HAUS.json" ] && echo --gegenprobe "gegenprobe-$HAUS.json" ) >> "$QA/auswertung.out" 2>&1
python3 zeiten.py "$QA" >> "$QA/lauf.out"
echo "$(date +%H:%M) FERTIG nach $(( ($(date +%s)-T0)/60 )) min · Tafel: http://localhost:8978/haus/_Oberchef/zeigen/$HAUS/abnahme-tor/$LAUF/index.html" | tee -a "$QA/lauf.out"
