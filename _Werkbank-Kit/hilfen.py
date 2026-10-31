"""Kleine Hilfen ohne Abhängigkeiten, damit haus.py sie beim Laden schon benutzen kann."""
import re


def svg_innen(pfad):
    """Innenleben einer SVG-Datei (potrace oder gezeichnet) + viewBox, Farbe über currentColor."""
    s = open(pfad, encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    vb = ' '.join(str(float(x)).rstrip('0').rstrip('.') for x in vb.split())
    innen = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    innen = re.sub(r'<metadata>.*?</metadata>|<!--.*?-->', '', innen, flags=re.S)
    innen = re.sub(r'\s+fill="(?:#000000|currentColor)"', '', innen)
    innen = re.sub(r'\s*\n\s*', ' ', innen).strip()
    return vb, innen


def text_pfad(schrift, text, sperr=0.0):
    """Ein Wort in einer Schrift als SVG-Pfad (viewBox, innen). sperr = Zeichenabstand in em. Braucht fontTools."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    f = TTFont(schrift)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm
    auf, ab = f['hhea'].ascent, f['hhea'].descent
    x, teile = 0, []
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            x += upm * .3; continue
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, auf)))
        d = pen.getCommands()
        if d:
            teile.append(d)
        x += gs[g].width + sperr * upm
    x -= sperr * upm
    return f'0 0 {x:.0f} {auf - ab}', '<path d="' + ' '.join(teile) + '"/>'
