#!/bin/zsh
# Nachlauf K23 (Übergabe von culinarium-imprimerie 30.10.2026): Anleitungsbilder neu, Bedienprüfung kurz, Fassungsnummern. Wartet auf Last unter 30 (Oberchef 30.10.2026).
S=$(mktemp -d); R=~/Desktop/Website-Projekte/"Culinarium Hannover"
while true; do l=$(sysctl -n vm.loadavg | awk '{print $2}'); [ ${l%.*} -lt 30 ] && break; sleep 20; done
echo "Last $l"
rm -rf $S/rdaten; cp -R "$R/_werkzeuge/reception/daten" $S/rdaten; cd "$R"; RECEPTION_DATEN=$S/rdaten RECEPTION_FORMULAR_GRENZE=200 python3 _werkzeuge/reception/server.py 9184 > $S/srv9184.log 2>&1 & SP=$!; sleep 2
cd "$R/_werkzeuge/reception/pruefung"; node anleitung_bilder.js http://127.0.0.1:9184/_werkzeuge/reception/ 2>&1 | tail -3
node culinarium.js http://127.0.0.1:9184 webkit 1440 2>&1 | grep -v "^ok " | tail -3
node culinarium.js http://127.0.0.1:9184 chromium 390 2>&1 | grep -v "^ok " | tail -3
lsof -a -p $SP -d cwd | grep -q "Culinarium Hannover" && kill $SP
cd "$R/_werkzeuge/reception"; python3 _bau/fassungen.py | tail -1
