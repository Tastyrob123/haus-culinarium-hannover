#!/bin/zsh
# La Carte · Culinarium Hannover — alle Prüfläufe nacheinander auf eigenen Prüfports (9089, 9090, 9091) mit Wegwerf-Daten; La Carte auf 9083 bleibt unberührt.
#   zsh _werkzeuge/carte/pruef/alle.sh            → Protokolle in pruef/aus/<lauf>.txt, danach python3 pruef/bericht.py
cd "$(dirname "$0")/.."
A=pruef/aus; mkdir -p $A
for b in chromium webkit firefox; do
  for m in "1440 900" "1366 650" "390 844" "320 640"; do
    set -- ${=m}
    node pruef/lauf.js $b $1 $2 > $A/lauf-$b-$1.txt 2>&1; echo "lauf $b $1: $(tail -1 $A/lauf-$b-$1.txt)"
  done
done
for b in chromium webkit; do node pruef/gleich.js $b > $A/gleich-$b.txt 2>&1; echo "gleich $b: $(tail -1 $A/gleich-$b.txt)"; done
python3 pruefe.py alles > $A/pruefe.txt 2>&1; echo "pruefe: $(tail -1 $A/pruefe.txt)"
node pruef/rund.js > $A/rund.txt 2>&1; echo "rund: $(grep -c gleich $A/rund.txt) gleich"
# Flüssigkeit nur unter Rechnerlast 8 (höchstens 15 Minuten warten), danach die Bildschirmbilder
for i in {1..30}; do python3 -c 'import os,sys;sys.exit(0 if os.getloadavg()[0]<8 else 1)' && break; sleep 30; done
for b in chromium webkit; do node pruef/fluessig.js $b > $A/fluessig-$b.txt 2>&1; echo "fluessig $b: $(grep -c '^ok' $A/fluessig-$b.txt) ok, $(grep -c '^FEHLER' $A/fluessig-$b.txt) rot, $(grep -m1 'Rechnerlast' $A/fluessig-$b.txt)"; done
node pruef/bilder.js > $A/bilder.txt 2>&1; echo "bilder: $(wc -l < $A/bilder.txt) Bilder"
