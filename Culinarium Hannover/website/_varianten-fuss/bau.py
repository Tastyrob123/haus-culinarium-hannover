#!/usr/bin/env python3
"""Culinarium · Fuss, unterer Teil der drei Spalten: Fassungen (29.10.2026, Robert: «Schreib uns, zur Bar untereinander als grosse Buttons,
darüber diese kleine Telefonnummer, daneben dieses @dirtychicken, wo keiner checkt … sehr unstrukturiert»).
Telefon und Instagram rücken in die Tabelle, die Wege bekommen eine einheitliche Form. Nur die Startseite, sonst alles wie heute. 00 = heute."""
import json, re, html, time
from pathlib import Path
HIER = Path(__file__).resolve().parent
WEB = HIER.parent
I = (WEB / "index.html").read_text()
assert len(I) > 10000, "index.html leer (läuft gerade ein Bau?)"
SP = re.search(r'<div class="fu-spalten">.*?</div></div></div>', I, re.S)
S = SP.group(0)
TAT = re.findall(r'<div class="fu-tat sw auf" style="--i:\d+">.*?</div>(?=</div>)', S, re.S)
assert len(TAT) == 3, len(TAT)
ZEITEN = re.findall(r'<dl class="fu-zeiten sw auf" style="--i:\d+">.*?</dl>', S, re.S)
assert len(ZEITEN) == 3
SCHREIB = re.search(r'<button class="knopf" type="button" data-anfrage="nachricht">.*?</button>', TAT[1], re.S).group(0)
BAR = re.search(r'<a class="knopf" href="([^"]*Walk[^"]*)"', TAT[1]).group(1)
PFEIL = re.search(r'(<svg viewBox="0 0 24 24".*?</svg>)', SCHREIB, re.S).group(1)
TEL = '<a href="tel:+491633909578">+49 163 3909578</a>'
IG = '<a class="fu-ig2" href="https://www.instagram.com/dirtychicken.hannover/" rel="noopener" target="_blank">@dirtychicken.<wbr>hannover</a>'
KI = lambda t: t.replace('i', '<em class="ki">i</em>')
WEGE = [[("Der Abend", "abend.html")], [("Schreib uns", None), ("Zur Bar", BAR)], [("Zum Pop-up", "dirty-chicken.html")]]


def knopf(t, h, cls="knopf"):
    if h is None:
        return f'<button class="{cls}" type="button" data-anfrage="nachricht"><span>{KI(t)}</span><i>{PFEIL}</i></button>'
    return f'<a class="{cls}" href="{h}" aria-label="{t}"><span>{KI(t)}</span><i>{PFEIL}</i></a>'


def zeile(dt, dd):
    return f'<div><dt>{dt}</dt><dd>{dd}</dd></div>'


def zeiten(extra2, extra3):
    z = list(ZEITEN)
    z[1] = z[1].replace('</dl>', extra2 + '</dl>'); z[2] = z[2].replace('</dl>', extra3 + '</dl>')
    return z


def spalten(z, taten):
    s = S
    for alt, neu in zip(ZEITEN, z):
        s = s.replace(alt, neu, 1)
    for alt, neu in zip(TAT, taten):
        s = s.replace(alt, alt[:alt.index('>') + 1] + neu + '</div>', 1)
    return s


TZ = zeiten(zeile("Telefon", TEL), zeile("Instagram", IG))
F = []
# 1 Wie die Tabelle: Telefon und Instagram als Zeilen, die Wege als Zeilen mit Pfeil darunter
F.append((1, "Wege als Zeilen", spalten(TZ, ['<nav class="fu-wege">' + "".join(knopf(t, h, "fu-weg") for t, h in w) + '</nav>' for w in WEGE]), """
.fu-wege{flex:1 1 100%;width:100%;border-top:1px solid rgba(250,244,244,.14)} .fu-s1 .fu-wege{max-width:352px}
.fu-weg{display:flex;width:100%;justify-content:space-between;align-items:center;gap:16px;padding:12px 0;border:0;border-bottom:1px solid rgba(250,244,244,.14);background:none;cursor:pointer;
 color:var(--weiss);font:340 clamp(19px,1.45vw,24px)/1.1 var(--titel);font-variation-settings:"SOFT" 100,"opsz" 144;text-align:left;text-decoration:none}
.fu-weg i{width:34px;height:34px;border-radius:50%;background:var(--kerze);color:var(--weiss);display:grid;place-items:center;flex:none;transition:transform .5s var(--k)}
.fu-weg i svg{width:15px;height:15px} .fu-weg:hover i{transform:translateX(5px)}
.fuss .fu-tat{padding-top:0;align-self:start}
"""))
# 2 Ein grosser Knopf je Spalte: Telefon, Nachricht und Instagram stehen in der Tabelle, darunter je Spalte ein Knopf über die ganze Breite
F.append((2, "Ein Knopf je Spalte", spalten(zeiten(zeile("Telefon", TEL) + zeile("Nachricht", '<button class="fu-mini" type="button" data-anfrage="nachricht">Schreib uns</button>'), zeile("Instagram", IG)),
                                      [knopf("Der Abend", "abend.html"), knopf("Zur Bar", BAR), knopf("Zum Pop-up", "dirty-chicken.html")]), """
.fu-tat .knopf{width:100%;justify-content:space-between} .fu-s1 .fu-tat{max-width:352px}
.fu-mini{background:none;border:0;padding:0 0 3px;border-bottom:1px solid var(--kerze);color:var(--weiss);font:400 16px/1.3 var(--text);cursor:pointer}
.fuss .fu-tat{align-self:start}
"""))
# 3 Eine Knopfleiste: Telefon und Instagram in der Tabelle, alle Wege in einer Reihe unter den drei Spalten
leiste = '<div class="fu-leiste sw auf" style="--i:9">' + "".join(knopf(t, h) for w in WEGE for t, h in w) + '</div>'
F.append((3, "Eine Knopfleiste", spalten(TZ, ["", "", ""]) + leiste, """
.fuss .fu-tat{display:none!important}
.fu-leiste{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;max-width:var(--max);margin:clamp(30px,4vh,44px) auto 0;padding-top:30px;border-top:1px solid rgba(250,244,244,.14)}
.fu-leiste .knopf{width:100%;justify-content:space-between}
@media (max-width:860px){.fu-leiste{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
"""))
NAMEN = [(0, "Heute")] + [(n, name) for n, name, _, _ in F]
ST = time.strftime("%d%H%M")


def seite(nr, name, sp=None, css=""):
    s = I if sp is None else I[:SP.start()] + sp + I[SP.end():]
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../">', 1)
    css += '.fu-zeiten dd:has(.fu-ig2){white-space:normal;text-align:right} .fu-ig2,.fu-zeiten dd a[href^=tel]{color:var(--weiss);border-bottom:1px solid var(--kerze);text-decoration:none}'
    s = s.replace('</head>', f'<style>{css}</style><link rel="stylesheet" href="_varianten-fuss/varianten-nav.css?v={ST}"></head>', 1)
    s = s.replace("</body>", f'<p class="vschild"><b>{nr:02d} / {len(F):02d}</b><span>{html.escape(name)}</span><i>← →</i></p>'
                             f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");'
                             f'if(!sessionStorage.getItem("vnav-stelle"))sessionStorage.setItem("vnav-stelle",JSON.stringify({{y:document.documentElement.scrollHeight}}));</script>'
                             f'<script src="_varianten-fuss/varianten-nav.js?v={ST}"></script></body>', 1)
    (HIER / f"{nr:02d}.html").write_text(s)


seite(0, "Heute")
for nr, name, sp, css in F:
    seite(nr, name, sp, css)
print("gebaut:", len(F) + 1)
