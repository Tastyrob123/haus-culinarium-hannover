#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, «Mitgebracht» als Kacheln mit Kuhle (12.10.2026, Master 5b Punkt 3).

Jede Gabe ist eine Holzplatte: das Foto oben hell und ungedimmt, die Zahl in einer Einkerbung der Bildecke, der Text in einer
vertieften Kuhle darunter. Fliesstext liegt nie auf einem Foto. Sechs Gaben stehen als zwei Reihen zu drei.
Eingehängt in haus.py: gabe_html = gaben_kuhle.gabe, GABEN_KLASSE, GABEN_BILD (ohne Dunkel), CSS am Dateiende."""

EINHEIT = dict(seite='Seiten', gaeste='Ideen', unterlagen='Unterlagen', papier='Ideen', material='Beiträge', studio='Bereiche')
GABEN_BILD = dict(dunkel=None, schnitt=4 / 3.1)
KLASSE = ' gaben--kuhle'


def gabe(g):
    return (f'<a class="gku" href="{g["ziel"]}" data-a="auf" style="--i:{g["i"] % 3}"><div class="gku__f">{g["bild"]("g-" + g["bk"])}'
            f'<div class="gku__kerbe"><b><span class="odo" data-z="{g["n"]}"></span></b><span class="gku__ein">{EINHEIT.get(g["bk"], "")}</span></div></div>'
            f'<div class="gku__kuhle"><h3>{g["t"]}</h3><p>{g["x"]}</p><span class="pfeil">{g["kt"]}{g["PF"]}</span></div></a>')


CSS = '''
/* ---------- «Mitgebracht»: Kacheln mit Kuhle (gaben_kuhle.py, 12.10.2026) ---------- */
.gaben.gaben--kuhle{display:grid;gap:clamp(14px,1.5vw,22px);grid-template-columns:repeat(3,minmax(0,1fr))}
.gku{display:flex;flex-direction:column;border-radius:30px;padding:7px;color:#fbf5ea;text-decoration:none;background:linear-gradient(180deg,#43291480 0%,#2a180a 62%),#321f10;
  box-shadow:inset 0 1px 0 rgba(255,236,200,.12),inset 0 0 0 1px rgba(201,133,67,.2),0 40px 50px -36px rgba(6,3,1,.95)}
.gku__f{position:relative;border-radius:24px;overflow:hidden;aspect-ratio:4/3.1;background:#2a180a}
.gku__f img{display:block;width:100%;height:100%;object-fit:cover;transform-origin:50% 40%;transition:transform 2.2s cubic-bezier(.16,1,.3,1)}
.gku__kerbe{position:absolute;left:0;bottom:0;padding:10px 20px 4px 16px;border-radius:0 22px 0 0;background:#2d1a0c;display:flex;align-items:baseline;gap:10px}
.gku__kerbe::before,.gku__kerbe::after{content:'';position:absolute;width:22px;height:22px;background:radial-gradient(circle at 100% 0,transparent 21.5px,#2d1a0c 22px)}
.gku__kerbe::before{left:0;top:-22px}.gku__kerbe::after{right:-22px;bottom:0}
.gku__kerbe b{font-family:var(--serif);font-weight:700;font-size:clamp(2.5rem,3.3vw,3.5rem);line-height:.9;color:var(--gold);white-space:nowrap}
.gku__ein{font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:rgba(243,205,148,.82)}
.gku__kuhle{flex:1;display:flex;flex-direction:column;margin-top:7px;border-radius:22px;padding:clamp(18px,1.8vw,26px) clamp(16px,1.7vw,24px) 18px;background:#1c1008;box-shadow:inset 0 2px 6px rgba(0,0,0,.5),inset 0 -1px 0 rgba(255,236,200,.06)}
.gku__kuhle h3{font-family:var(--serif);font-weight:700;font-size:clamp(1.36rem,1.6vw,1.62rem);line-height:1.14;margin:0 0 10px}
.gku__kuhle p{font-size:clamp(.98rem,1.04vw,1.06rem);line-height:1.58;color:rgba(251,245,234,.84);margin:0 0 18px}
.gku__kuhle .pfeil{margin-top:auto;align-self:flex-start;color:var(--gold)}
@media(hover:hover){.gku:hover .gku__f img{transform:scale(1.06);transition-duration:2.8s}}
@media(max-width:1060px){.gaben.gaben--kuhle{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){.gaben.gaben--kuhle{grid-template-columns:1fr}.gku__f{aspect-ratio:4/2.7}}
@media (prefers-reduced-motion:reduce){.gku__f img{transition:none;transform:none!important}}
'''
