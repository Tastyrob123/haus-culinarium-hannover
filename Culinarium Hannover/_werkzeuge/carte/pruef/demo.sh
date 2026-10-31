#!/bin/zsh
# La Carte · Culinarium Hannover — Bau-Selbstprüfung (Chromium und Safari-Kern, 1440 und 390 px), nacheinander auf dem Prüfport 9089.
cd "$(dirname "$0")/.."
A=pruef/aus; mkdir -p $A
for b in chromium webkit; do
  for m in "1440 900" "390 844"; do
    set -- ${=m}
    node pruef/lauf.js $b $1 $2 > $A/lauf-$b-$1.txt 2>&1; echo "lauf $b $1: $(tail -1 $A/lauf-$b-$1.txt)"
  done
done
