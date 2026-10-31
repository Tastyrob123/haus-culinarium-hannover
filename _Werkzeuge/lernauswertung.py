#!/usr/bin/env python3
"""Lernauswertung eines fertigen Projekts (Tasty-Sprache Teil F, CLAUDE.md Regel 60i).

Liest alle Claude-Code-Unterhaltungen seit einem Zeitpunkt, die das Projekt erwähnen,
zieht Roberts eigene Nachrichten samt Bildschirmfotos heraus und legt sie zum Lesen ab:
  <ziel>/nachrichten.json   alle Nachrichten (Zeit, Chat, Text, Bilder)
  <ziel>/dump.txt           dieselben Nachrichten als Lesetext, nummeriert
  <ziel>/bilder/            jedes Bildschirmfoto als Datei
  <ziel>/tafeln/tNN.jpg     je vier Bildschirmfotos auf einer Tafel, beschriftet mit [Nummer]

Aufruf:
  python3 lernauswertung.py --woerter "Schlössli,Bottighofen" --gegen "Schäfli,Wigoltingen" \
      --seit 2026-10-18 --ziel /tmp/lern-schloessli
--gegen: Wörter eines Nachbarprojekts; Chats, in denen diese überwiegen, fallen weg.
"""
import argparse, base64, glob, json, os, re, time
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument('--woerter', required=True)
ap.add_argument('--gegen', default='')
ap.add_argument('--seit', required=True, help='JJJJ-MM-TT oder JJJJ-MM-TTTHH:MM')
ap.add_argument('--ziel', required=True)
ap.add_argument('--mindest', type=int, default=150, help='Mindestzahl Treffer je Chat')
a = ap.parse_args()

def muster(w):
    teile = [re.escape(x.strip()) for x in w.split(',') if x.strip()]
    if not teile: return None
    # Umlaute auch in JSON-Schreibweise finden
    alt = []
    for t in teile:
        alt.append(t)
        alt.append(t.encode('ascii', 'backslashreplace').decode().replace('\\x', '\\\\u00'))
    return re.compile('|'.join(alt))

M, G = muster(a.woerter), muster(a.gegen)
seit = datetime.fromisoformat(a.seit).timestamp()
os.makedirs(a.ziel + '/bilder', exist_ok=True)
SKIP = ('Task (from', 'Background (from', '<cross-session', '<side-sessions', '<task-notification',
        'Caveat:', '<command-', '<local-command', 'Another Claude', 'Base directory',
        'This session is being continued', 'Analysiere diese Claude-Code')
rows = []
for f in glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')):
    if os.path.getmtime(f) < seit: continue
    s = open(f, errors='ignore').read()
    if 'Analysiere diese Claude-Code' in s[:3000]: continue
    n = len(M.findall(s)); g = len(G.findall(s)) if G else 0
    if n < a.mindest or (G and g > 1.5 * n): continue
    sid = os.path.basename(f)[:8]
    for line in s.splitlines():
        try: d = json.loads(line)
        except Exception: continue
        if d.get('type') != 'user' or d.get('isSidechain'): continue
        ts = d.get('timestamp', '')
        if ts and datetime.fromisoformat(ts.replace('Z', '+00:00')).timestamp() < seit: continue
        c = d['message']['content']
        items = [{'type': 'text', 'text': c}] if isinstance(c, str) else c
        if any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in items): continue
        txt = '\n'.join(x.get('text', '') for x in items if isinstance(x, dict) and x.get('type') == 'text')
        txt = re.sub(r'<system-reminder>.*?</system-reminder>', '', txt, flags=re.S)
        txt = re.sub(r'\[Image: [^\]]*\]', '', txt).strip()
        imgs = []
        for k, x in enumerate(x for x in items if isinstance(x, dict) and x.get('type') == 'image'):
            src = x.get('source', {})
            if src.get('type') == 'base64':
                ext = 'png' if 'png' in src.get('media_type', '') else 'jpg'
                p = f"{a.ziel}/bilder/{sid}-{ts[11:19].replace(':', '')}-{k}.{ext}"
                open(p, 'wb').write(base64.b64decode(src['data'])); imgs.append(os.path.basename(p))
        if txt.startswith(SKIP) and not imgs: continue
        if not txt and not imgs: continue
        rows.append(dict(chat=sid, zeit=ts[:19], text=txt, bilder=imgs))
rows.sort(key=lambda r: r['zeit'])
json.dump(rows, open(a.ziel + '/nachrichten.json', 'w'), ensure_ascii=False, indent=1)
with open(a.ziel + '/dump.txt', 'w') as fh:
    for i, r in enumerate(rows):
        b = (' BILD:' + ' '.join(r['bilder'])) if r['bilder'] else ''
        fh.write(f"[{i}] {r['zeit']} {r['chat']}{b}\n   {r['text'][:1500].replace(chr(10), ' ⏎ ')}\n")
try:
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(a.ziel + '/tafeln', exist_ok=True)
    try: font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
    except Exception: font = None
    alle = [(i, a.ziel + '/bilder/' + b) for i, r in enumerate(rows) for b in r['bilder']]
    W = 900
    for t, k in enumerate(range(0, len(alle), 4)):
        ims = []
        for i, p in alle[k:k + 4]:
            im = Image.open(p).convert('RGB'); im.thumbnail((W, W)); ims.append((i, im))
        H = max(im.height for _, im in ims) + 40
        sh = Image.new('RGB', (W * 2 + 10, H * 2 + 10), 'white'); d = ImageDraw.Draw(sh)
        for j, (i, im) in enumerate(ims):
            x = (j % 2) * (W + 10); y = (j // 2) * (H + 5)
            d.rectangle([x, y, x + W, y + 36], fill='black'); d.text((x + 8, y + 4), f'[{i}]', fill='yellow', font=font)
            sh.paste(im, (x, y + 40))
        sh.save(f"{a.ziel}/tafeln/t{t:02d}.jpg", quality=80)
except ImportError:
    print('Pillow fehlt: keine Tafeln')
print(f"{len(rows)} Nachrichten, {sum(len(r['bilder']) for r in rows)} Bilder, "
      f"{len({r['chat'] for r in rows})} Chats -> {a.ziel}")
