#!/bin/bash
# Läuft nach jedem Werkzeugaufruf. Ist das Limit fast erreicht, bekommt Claude den Auftrag zur Übergabe.
D="$(cd "$(dirname "$0")" && pwd)"
python3 - "$D" <<'PY' 2>/dev/null
import json, os, sys, time
d = sys.argv[1]
try: s = json.load(open(os.path.join(d, "stand.json")))
except Exception: sys.exit(0)
fh = (s.get("five_hour") or {}).get("prozent") or 0
sd = (s.get("seven_day") or {}).get("prozent") or 0
stufe = 2 if (fh >= 95 or sd >= 97) else 1 if (fh >= 88 or sd >= 93) else 0
if not stufe: sys.exit(0)
merk = os.path.join(d, f"gewarnt-{stufe}")
if os.path.exists(merk) and time.time() - os.path.getmtime(merk) < 1800: sys.exit(0)
open(merk, "w").write(str(time.time()))
text = (f"LIMIT FAST ERREICHT (5 Stunden: {fh}%, Woche: {sd}%). Jetzt, vor allem anderen: UEBERGABE-LIMIT.md im Stamm des Repos "
        "vollständig schreiben (Auftrag, was fertig ist mit Links, was offen ist in Reihenfolge, nächster genauer Schritt, Zweige, Prüfstand, "
        "Stolpersteine), committen und pushen. Danach weiterarbeiten und die Datei nach jedem Schritt nachführen. Ein Chat in einem anderen "
        "Profil muss allein mit dieser Datei nahtlos weitermachen können.")
if stufe == 2: text = "LETZTE WARNUNG. " + text + " Keine neue grosse Arbeit mehr beginnen, bevor die Übergabe gepusht ist."
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": text}}))
PY
exit 0
