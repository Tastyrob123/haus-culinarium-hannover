#!/bin/bash
# Bekommt von Claude Code die Sitzungsdaten (JSON) und hält den Limit-Stand fest.
D="$(cd "$(dirname "$0")" && pwd)"
IN=$(cat)
python3 - "$D/stand.json" "$IN" <<'PY' 2>/dev/null
import json, sys, time
z, raw = sys.argv[1], sys.argv[2]
try: d = json.loads(raw)
except Exception: sys.exit(0)
rl = d.get("rate_limits") or {}
out = {"zeit": int(time.time())}
for k in ("five_hour", "seven_day"):
    w = rl.get(k) or {}
    if "used_percentage" in w: out[k] = {"prozent": w["used_percentage"], "neu_ab": w.get("resets_at")}
if len(out) > 1: json.dump(out, open(z, "w"))
fh = out.get("five_hour", {}).get("prozent"); sd = out.get("seven_day", {}).get("prozent")
print(f"5h {fh if fh is not None else '?'}% · Woche {sd if sd is not None else '?'}%")
PY
