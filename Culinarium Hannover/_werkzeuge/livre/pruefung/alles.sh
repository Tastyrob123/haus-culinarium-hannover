#!/bin/zsh
# Le Livre · Culinarium: Gesamtlauf gegen den Prüfserver :9085 (nacheinander, nie zwei Browser zugleich): Matrix, Fehlerbuch, Anleitung-Bilder, Schirmbilder, Flüssigkeit.
#   zsh _werkzeuge/livre/pruefung/alles.sh <zielordner-fuer-bilder>      (aus _werkzeuge/livre/)
E=pruefung/ergebnisse
zsh pruefung/matrix.sh
for m in chromium webkit; do NODE_PATH=~/Aussen-Pruefung/node_modules node pruefung/fehlerbuch.js $m > /dev/null 2>&1; tail -1 $E/fehlerbuch-$m.txt; done
node anleitung_bilder.js > /dev/null 2>&1 && echo "Anleitung-Bilder neu"
node pruefung/schirm.js "$1" && echo "Schirmbilder in $1"
TROTZDEM=1 BASIS=http://127.0.0.1:9085/ node pruefung/fluss.js > $E/fluss-lauf.txt 2>&1; echo "Fluss: $(wc -l < $E/fluss-lauf.txt) Zeilen"
