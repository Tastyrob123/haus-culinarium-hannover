#!/usr/bin/env python3
"""Tafel «Anrede du statt Sie» (29.10.2026): je Werkzeug Startansicht vorher/nachher, WebKit 1440 und 390.
python3 anrede_tafel.py → _Oberchef/zeigen/culinarium/anrede-2910/index.html"""
import os, html
Z = os.path.expanduser('~/Desktop/Website-Projekte/_Oberchef/zeigen/culinarium/anrede-2910')
W = [('tresen', 'Der Tresen', 'Rundgang und Kacheln: «Von hier aus pflegst du …», «Wer deine Website besucht»'),
     ('schaufenster', 'Das Schaufenster', '«Hier pflegst du die Website des Hauses …», «Was du speicherst, sammelt sich hier.» (gemeinsame website.js mit Schalter nur für Culinarium)'),
     ('pairing-karte', 'Die Pairing-Karte', '«Oben der nächste Abend, den du Gang für Gang einträgst.», «Wer bist du?»'),
     ('gaestebuch', 'Das Gästebuch', '«Entwurf für deine Antwort. Verschickt wird nur, was du selbst schickst.»'),
     ('markenbuch', 'Das Markenbuch', '«Guten Tag. Schön, dass du da bist. Womit fangen wir an?»'),
     ('besucherliste', 'Die Besucherliste', '«Wer deine Website besucht hat …», «So siehst du, ob ein Plakat …»')]
k = []
for s, n, satz in W:
    k.append(f'''<section><h2>{html.escape(n)}</h2><p class="s">{html.escape(satz)}</p>
<div class="paar"><figure><figcaption>vorher</figcaption><img src="{s}-vorher-1440.jpg" alt="{html.escape(n)} vorher, 1440 px" loading="lazy"></figure>
<figure><figcaption>nachher</figcaption><img src="{s}-nachher-1440.jpg" alt="{html.escape(n)} nachher, 1440 px" loading="lazy"></figure></div>
<div class="paar klein"><figure><figcaption>vorher · Handy</figcaption><img src="{s}-vorher-390.jpg" alt="" loading="lazy"></figure>
<figure><figcaption>nachher · Handy</figcaption><img src="{s}-nachher-390.jpg" alt="" loading="lazy"></figure></div></section>''')
open(os.path.join(Z, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anrede du · Culinarium</title><style>
:root{{--bg:#FAF4F4;--t:#16141B;--l:#3A3845;--k:#CF7233}}@media (prefers-color-scheme:dark){{:root{{--bg:#16141B;--t:#FAF4F4;--l:#C9C4CF}}}}
body{{margin:0;background:var(--bg);color:var(--t);font:16px/1.55 system-ui,sans-serif}}main{{max-width:1240px;margin:0 auto;padding:32px 16px 80px}}
h1{{font:400 clamp(34px,5vw,56px)/1.05 Georgia,serif;margin:0 0 10px}}h2{{font:400 28px/1.2 Georgia,serif;margin:46px 0 4px}}.s{{color:var(--l);margin:0 0 14px}}
.paar{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}.paar.klein{{grid-template-columns:repeat(2,minmax(0,260px));margin-top:12px}}
figure{{margin:0}}figcaption{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--k);margin-bottom:6px}}img{{width:100%;height:auto;border-radius:10px;display:block;box-shadow:0 10px 24px -14px rgba(0,0,0,.5)}}
@media (max-width:700px){{.paar{{grid-template-columns:1fr}}}}</style></head><body><main>
<h1>Die Werkzeuge sagen jetzt «du».</h1><p class="s">Robert, 29.10.2026: «Also wir siezen die jetzt nicht … ein bisschen persönlicher.» Tresen, Schaufenster, Pairing-Karte, Gästebuch, Markenbuch und Besucherliste, mit Rundgängen, Anleitungen (Bilder neu aufgenommen), Meldungen und Prüfseiten. Plakatwerkstatt macht die Imprimerie, die Werkbank bleibt bei «ihr». Startansicht in Safari (WebKit), 1440 und 390 px.</p>
{''.join(k)}</main></body></html>''')
print('ok')
