#!/bin/zsh
# Probe-Kopie für die Prüfläufe des Besucherbuchs · Culinarium Hannover (Werkzeug-Master F25: je Chat eine eigene Kopie, Wegwerf-Daten; Muster Schäfli).
# Aufbau wie das Projekt: website/ (APFS-Klon von assets/ und den Seiten) neben _werkzeuge/ (registre frisch, oberflaeche und maison nur gelesen).
# Am echten Culinarium wird nichts geschrieben; Zählungen der Prüfläufe gehen in einen eigenen Ordner unter /tmp (REGISTRE_ORDNER).
set -e
QUELLE="$HOME/Desktop/Website-Projekte/Culinarium Hannover"
PROBE="$HOME/Desktop/Website-Projekte/_Probe Culinarium Registre"
mkdir -p "$PROBE/website" "$PROBE/_werkzeuge"
rm -rf "$PROBE/website/assets"; cp -c -R "$QUELLE/website/assets" "$PROBE/website/assets"
rm -f "$PROBE"/website/*.html(N)
for f in "$QUELLE"/website/*.html; do cp -c "$f" "$PROBE/website/" 2>/dev/null || cp "$f" "$PROBE/website/"; done
# Oberfläche des Hauses und die Zentrale (anderer Chat, nur gelesen)
for w in oberflaeche maison; do [ -d "$QUELLE/_werkzeuge/$w" ] && { rm -rf "$PROBE/_werkzeuge/$w"; cp -c -R "$QUELLE/_werkzeuge/$w" "$PROBE/_werkzeuge/$w"; } || true; done
rm -rf "$PROBE/_werkzeuge/registre"
cp -c -R "$QUELLE/_werkzeuge/registre" "$PROBE/_werkzeuge/registre"
rm -rf "$PROBE/_werkzeuge/registre/_daten"
# messung.js für den Zähl-Test an Seiten der Probe-Kopie: am Ende jeder Seite (wie es auf der Website stehen soll: assets/messung.js nach culinarium.js)
cp "$QUELLE/_werkzeuge/registre/vorschlag/messung.js" "$PROBE/website/assets/messung.js"
for f in "$PROBE"/website/*.html; do grep -q 'assets/messung.js' "$f" || perl -0pi -e 's#</body>#<script src="assets/messung.js?v=probe" defer></script>\n</body>#' "$f"; done
echo "Probe-Kopie: $PROBE"
