#!/bin/zsh
# Le Livre · Culinarium: alle Läufe nacheinander (nie zwei Browser zugleich) gegen den Prüfserver :9085 (Markenprüfung ohne Claude).
#   zsh _werkzeuge/livre/pruefung/matrix.sh      (aus _werkzeuge/livre/)
E=pruefung/ergebnisse; mkdir -p $E
for c in "chromium 1440x900" "webkit 1440x900" "chromium 390x844" "webkit 390x844"; do
  NODE_PATH=~/Aussen-Pruefung/node_modules node pruefung/bedienen.js ${=c} > $E/lauf-${c// /-}.txt 2>&1; tail -1 $E/lauf-${c// /-}.txt
done
for m in chromium webkit; do
  BASIS=http://127.0.0.1:9085/ FEHLERLOG="$PWD/_qa/fehler.jsonl" node pruefung/zusatz.js $m > $E/zusatz-$m.txt 2>&1; grep "Summe\|ABBRUCH\|✗" $E/zusatz-$m.txt
done
python3 pruefung/dateien_pruef.py > $E/dateien.txt 2>&1; tail -1 $E/dateien.txt
python3 pruefung/sicherheit.py > $E/sicherheit.txt 2>&1; tail -1 $E/sicherheit.txt
