#!/usr/bin/env python3
"""Startseite des Zweigs «ergebnis»: alle Läufe (je Bau-Zweig der jüngste) mit Zahlen und Link."""
import glob, html, json, os, sys
D = sys.argv[1]; e = html.escape; z = []
for f in sorted(glob.glob(os.path.join(D, '*', 'lauf.json'))):
    o = os.path.dirname(f); l = json.load(open(f))
    zz = json.load(open(os.path.join(o, 'zeiten.json'))) if os.path.exists(os.path.join(o, 'zeiten.json')) else {}
    z.append((l.get('zeit', ''), f"<tr><td><a href='{e(o)}/index.html'>{e(l.get('zweig', ''))}</a></td><td>{e(l.get('zeit', '')[:16].replace('T', ' '))} UTC</td><td>{zz.get('gesamt_minuten', '–')} min</td><td>{zz.get('rechner_minuten', '–')}</td><td>{e(l.get('stand', '')[:7])}</td></tr>"))
z.sort(reverse=True)
print(f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Abnahmen</title>
<style>body{{font:16px/1.5 -apple-system,system-ui,sans-serif;margin:0;background:#f6f4ef}}main{{max-width:900px;margin:0 auto;padding:40px 20px}}h1{{font-size:44px}}table{{width:100%;border-collapse:collapse;background:#fff}}td,th{{padding:10px;border-bottom:1px solid #eee;text-align:left}}</style></head>
<body><main><h1>Abnahmen in der Cloud</h1><table><tr><th>Stand</th><th>Zeit</th><th>Dauer</th><th>Rechner-Minuten</th><th>Commit</th></tr>{''.join(r for _, r in z)}</table></main></body></html>""")
