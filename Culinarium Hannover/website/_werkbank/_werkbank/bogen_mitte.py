"""Druckbögen A3 (Sticker, Untersetzer): die Stücke stehen nicht oben links gesammelt, sondern jede Reihe waagrecht mittig und der ganze Block
senkrecht mittig auf dem Bogen (Tor 4, 30.10.2026: «rechte Spalte und unteres Drittel leer», «letzte Reihe nur fünf Sticker links»).
Hängt sich an papier_kern.seite: jede Seite, deren Name auf «-bogen» endet, wird vor dem Schreiben zentriert. Das Kit bleibt unverändert."""
import re
import papier_kern as P

SVG = re.compile(r'<svg class="abs" style="left:([\d.]+)mm;top:([\d.]+)mm;width:([\d.]+)mm;height:([\d.]+)mm')
OBEN, UNTEN, BREITE = 12, 287, 420


def mitte(html):
    stuecke = [(float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))) for m in SVG.finditer(html)]
    if not stuecke:
        return html
    reihen = {}
    for x, y, b, h in stuecke:
        reihen.setdefault(y, []).append((x, b))
    oben, unten = min(y for _, y, _, _ in stuecke), max(y + h for _, y, _, h in stuecke)
    dy = max(OBEN - oben, (OBEN + UNTEN) / 2 - (oben + unten) / 2)
    dx = {y: BREITE / 2 - (min(x for x, _ in r) + max(x + b for x, b in r)) / 2 for y, r in reihen.items()}
    def setz(m):
        x, y = float(m.group(1)), float(m.group(2))
        return f'<svg class="abs" style="left:{x + dx[y]:.2f}mm;top:{y + dy:.2f}mm;width:{m.group(3)}mm;height:{m.group(4)}mm'
    return SVG.sub(setz, html)


_seite = P.seite


def seite(ident, blaetter, titel):
    if ident.endswith('-bogen'):
        blaetter = [mitte(b) for b in blaetter]
    return _seite(ident, blaetter, titel)


P.seite = seite
