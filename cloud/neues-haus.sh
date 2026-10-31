#!/bin/zsh
# Neues Haus in die Cloud schicken (läuft einmal auf Roberts Mac, dauert nur so lange wie das Hochladen).
#   cloud/neues-haus.sh "Taverne zum Schäfli Wigoltingen" schaefli
# Legt ~/Cloud-Haeuser/<kurz>/ an, kopiert Website, Werkbank, Werkzeuge (ohne alte Prüfbilder, Sicherungen, Schlüssel),
# die Prüfwerkzeuge und den Cloud-Rahmen, legt den privaten GitHub-Ordner Tastyrob123/haus-<kurz> an und lädt hoch.
# Das Kundenmaterial (_quelle) kommt in den Zweig «quelle», damit die Prüfrechner es nicht laden müssen.
set -e
HAUS="$1"; KURZ="$2"; [ -z "$HAUS" -o -z "$KURZ" ] && { echo 'Aufruf: neues-haus.sh "<Hausordner>" <kurz>'; exit 2; }
WP=~/Desktop/Website-Projekte; Q="$WP/$HAUS"; [ -d "$Q" ] || { echo "Ordner fehlt: $Q"; exit 2; }
VORLAGE=${0:A:h:h}; R=~/Cloud-Haeuser/$KURZ; REPO=Tastyrob123/haus-$KURZ
AUS=$(mktemp); cat > $AUS <<'EOF'
.DS_Store
__pycache__/
node_modules/
.vercel/
.git/
.env
*.env
.env.*
*.pem
*.key
_qa/
_archiv*/
*sicherung*/
_sicherung/
*.vor-*
*.stand-vor-*
*.log
_roh/
_online/
_probe/
EOF
mkdir -p "$R/_Werkzeuge" "$R/vorgaben" "$R/cloud" "$R/.github/workflows"
rsync -a --exclude-from=$AUS --exclude='/website.*' --exclude='/_quelle/' "$Q/" "$R/$HAUS/"
for d in abnahme-tor messlauf stamm unterbau haeuser daten werkzeuge; do rsync -a --exclude-from=$AUS "$WP/_Werkzeuge/$d" "$R/_Werkzeuge/"; done
cp "$WP/_Werkzeuge/"{ROBERTS-KRITERIEN.md,OBERCHEF-PAKET.md,STAND.md,lernauswertung.py} "$R/_Werkzeuge/"
rsync -a --exclude-from=$AUS "$WP/_Werkbank-Kit" "$R/"
cp "$VORLAGE/vorgaben/"*.md "$R/vorgaben/"; cp "$VORLAGE/cloud/"*.{sh,py,md} "$R/cloud/" 2>/dev/null; cp "$VORLAGE/.github/workflows/abnahme.yml" "$R/.github/workflows/"
sed "s/Culinarium Hannover/$HAUS/g" "$VORLAGE/CLAUDE.md" > "$R/CLAUDE.md"; sed "s#/Culinarium Hannover/_quelle/#/$HAUS/_quelle/#" "$VORLAGE/.gitignore" > "$R/.gitignore"
[ -f "$R/cloud/haus.json" ] || python3 - "$HAUS" "$KURZ" "$R/cloud/haus.json" <<'PY'
import json, sys
h, k, z = sys.argv[1:]
json.dump({"haus": h, "kurz": k, "ordner": h, "tor_ziele": f"_Werkzeuge/abnahme-tor/ziele-{k}.json", "mess_ziele": f"_Werkzeuge/messlauf/ziele-{k}.json",
           "tor_groessen": ["1280x800", "1000x650", "390x844"], "mess_groessen": ["1440", "1280", "1000", "390"], "browser": ["chromium", "webkit"],
           "server": []}, open(z, "w"), ensure_ascii=False, indent=2)
PY
# Schlüssel-Suche: bricht ab, wenn etwas wie ein Schlüssel aussieht
if grep -rIlE "sk-ant-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|github_pat_|AKIA[0-9A-Z]{16}|-----BEGIN (RSA|OPENSSH|PRIVATE)|vercel_[A-Za-z0-9]{20,}" "$R" | grep -v '/cloud/neues-haus.sh$'; then echo "Schlüssel gefunden, nichts hochgeladen"; exit 1; fi
cd "$R"; [ -d .git ] || git init -q -b main; git config core.quotepath false; git add -A; git commit -qm "$HAUS: Stand für die Cloud" || true
gh repo view $REPO >/dev/null 2>&1 || gh repo create $REPO --private --source . --remote origin
git -c http.postBuffer=524288000 push -u origin main
if [ -d "$Q/_quelle" ]; then T=$(mktemp -d); mkdir -p "$T/$HAUS"; rsync -a --exclude-from=$AUS "$Q/_quelle" "$T/$HAUS/"
  ( cd $T && git init -q -b quelle && git add -A && git commit -qm "Kundenmaterial" && git remote add origin https://github.com/$REPO.git && git -c http.postBuffer=524288000 push -f origin quelle ); rm -rf $T; fi
echo "Fertig: https://github.com/$REPO  ·  nächster Schritt: Cloud-Chat in diesem Ordner starten (cloud/ANLEITUNG.md)"
