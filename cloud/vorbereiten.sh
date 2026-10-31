#!/usr/bin/env bash
# Rechner in der Cloud so einrichten, dass die Werkzeuge dieselben Wege finden wie auf Roberts Mac:
# ~/Desktop/Website-Projekte zeigt auf diesen Ordner, Playwright liegt unter /Users/robertreff/Aussen-Pruefung.
set -euo pipefail
WS="${GITHUB_WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}"
PWV="1.62.1"
S=""; [ "$(id -u)" != 0 ] && command -v sudo >/dev/null && S=sudo
$S mkdir -p /Users/robertreff/Desktop /Users/robertreff/Aussen-Pruefung "$HOME/Desktop"
$S chown "$(id -u)" /Users/robertreff /Users/robertreff/Desktop /Users/robertreff/Aussen-Pruefung "$HOME/Desktop" 2>/dev/null || true
for H in "$HOME" /Users/robertreff; do [ -e "$H/Desktop/Website-Projekte" ] || ln -sfn "$WS" "$H/Desktop/Website-Projekte"; done
cd /Users/robertreff/Aussen-Pruefung
[ -f package.json ] || echo '{"name":"pruefung","private":true}' > package.json
[ -d node_modules/playwright ] || npm i "playwright@$PWV" --no-audit --no-fund --silent
BROWSER="${1:-webkit chromium}"
npx playwright install --with-deps $BROWSER >/tmp/pw-install.log 2>&1 || { tail -30 /tmp/pw-install.log; exit 1; }
python3 -c "import numpy, PIL" 2>/dev/null || pip install --quiet --break-system-packages numpy pillow
echo "bereit: $(node -v), python $(python3 -V), playwright $PWV ($BROWSER)"
