#!/usr/bin/env python3
"""Culinarium: vierzig Sticker (Prüfchat Gestaltung 29.10.2026, Auftrag Oberchef nach Robert: «mach nochmal so 40 Sticker»).
Gebaut wie die Untersetzer (papier_kern.etikett, Druckbogen A3 mit Schnittlinie in Magenta), aber in einen eigenen Ordner sticker/.
Formen: rund, eckig und gestanzt (Ticket mit Kerben, Siegel mit Wellenrand, Schild mit Bogen, Kapsel). Inhalte: das C, Rudis Wortmarke,
Rudis Zeilen, Rudis Plakate ganz, Sätze der Bar mit Wertigkeit, Dirty Chicken und die Farben der Abende. Kein «x» als Zeichen (Kriterium 24).
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/sticker.py "<website/_werkbank>"   →  satz/sticker*.html, sticker_plan.json
   danach  node _werkbank/sticker_druck.js "<website/_werkbank>"   und   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/sticker.py "<…>" --seite"""
import json, math, os, sys
import papier_kern as P
import bogen_mitte  # noqa: F401  Druckbögen mittig (Tor 4, 30.10.2026)
from papier_kern import etikett, tx, hzz, hwz, blatt, t, e
from kern import H, ROOT, W
import papier_neu as N

NACHT, WEISS, CREME, SCHIEFER, KERZE, KERZEH, KERZET, VIOLETT = N.NACHT, N.WEISS, N.CREME, N.SCHIEFER, N.KERZE, N.KERZEH, N.KERZET, N.VIOLETT
ZEILE = 'A UNiQUE EXPERiENCE BY MOMO X RUDI'
MB = json.load(open(os.path.join(os.path.dirname(os.path.dirname(ROOT)), '_kette', '05-markenbauer', 'marke.json'), encoding='utf-8'))
ABEND = [(a['name'], a['hex'], a['plakat']) for a in MB['abendfarben']]


def hell(hx):
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    return (r * 299 + g * 587 + b * 114) / 1000 > 150


# ---------------------------------------------------------------- Formen (SVG-Pfade in mm)
def kreis(d):
    r = d / 2
    return f'M{r} 0A{r} {r} 0 1 1 {r - .01} 0Z'


def eck(b, h, r=3):
    return f'M{r} 0H{b - r}A{r} {r} 0 0 1 {b} {r}V{h - r}A{r} {r} 0 0 1 {b - r} {h}H{r}A{r} {r} 0 0 1 0 {h - r}V{r}A{r} {r} 0 0 1 {r} 0Z'


def kapsel(b, h):
    return eck(b, h, h / 2)


def ticket(b, h, k=4, r=2):
    m = h / 2
    return (f'M{r} 0H{b - r}A{r} {r} 0 0 1 {b} {r}V{m - k}A{k} {k} 0 0 0 {b} {m + k}V{h - r}A{r} {r} 0 0 1 {b - r} {h}H{r}A{r} {r} 0 0 1 0 {h - r}'
            f'V{m + k}A{k} {k} 0 0 0 0 {m - k}V{r}A{r} {r} 0 0 1 {r} 0Z')


def siegel(d, n=28, tief=1.6):
    r, c, p = d / 2, d / 2, []
    for i in range(n * 8):
        a = 2 * math.pi * i / (n * 8)
        rr = r - tief / 2 + tief / 2 * math.cos(n * a)
        p.append(f'{c + rr * math.sin(a):.2f},{c - rr * math.cos(a):.2f}')
    return 'M' + 'L'.join(p) + 'Z'


def schild(b, h):
    r = b / 2
    return f'M0 {r}A{r} {r} 0 0 1 {b} {r}V{h - 3}A3 3 0 0 1 {b - 3} {h}H3A3 3 0 0 1 0 {h - 3}Z'


# ---------------------------------------------------------------- Bausteine
def grund(form, farbe, rand=None, ab=2.2):
    r = f'<path d="{form}" fill="none" stroke="{rand}" stroke-width=".3" transform="translate({ab} {ab}) scale(1)" opacity="0"/>' if False else ''
    return f'<path d="{form}" fill="{farbe}"/>' + r


def ring_kreis(d, farbe, ab=2.4):
    return f'<circle cx="{d / 2}" cy="{d / 2}" r="{d / 2 - ab}" fill="none" stroke="{farbe}" stroke-width=".3"/>'


def ring_eck(b, h, farbe, ab=2.2, r=1.6):
    return f'<rect x="{ab}" y="{ab}" width="{b - 2 * ab}" height="{h - 2 * ab}" rx="{r}" fill="none" stroke="{farbe}" stroke-width=".3"/>'


def fr(x, y, text, gr, farbe):
    return tx(x, y, e(text), gr, farbe, 's', 0, 'middle', 'font-weight="340"')


def mo(x, y, text, gr, farbe, sp=.14):
    return tx(x, y, e(text.upper()), gr, farbe, 'm', sp)


def bildel(key, x, y, b, h, clip):
    return (f'<clipPath id="{clip}"><path d="{eck(b, h, 2)}" transform="translate({x} {y})"/></clipPath>'
            f'<image href="{e(N.bild(key))}" x="{x}" y="{y}" width="{b}" height="{h}" preserveAspectRatio="xMidYMid meet" clip-path="url(#{clip})"/>')


def ring_text(ident, d, text, farbe, gr=2.4, ab=6):
    r = d / 2 - ab
    return P.bogen_text(ident, f'M{d / 2 - r} {d / 2}A{r} {r} 0 1 1 {d / 2 + r} {d / 2}A{r} {r} 0 1 1 {d / 2 - r} {d / 2}', (e(text) + ' · ') * 2, gr, farbe, 'm', .14)


# ---------------------------------------------------------------- die vierzig (gemischt, Gegenprobe Oberchef 29.10.: keine Farbnamen, höchstens drei schlichte C)
def figur(k, hoehe):
    """Freigestellte Figur aus Rudis Motiv (eigen/figuren, Vision auf dem Rechner), mit weissem Stanzrand als Kontur."""
    import shutil
    F = json.load(open(os.path.join(W, 'eigen', 'figuren', 'figuren.json')))[k]
    os.makedirs(os.path.join(P.SATZ, 'bild'), exist_ok=True)
    shutil.copy2(os.path.join(W, 'eigen', 'figuren', f'fig_{k}.png'), os.path.join(P.SATZ, 'bild', f'fig_{k}.png'))
    s = hoehe / F['h']; b = F['w'] * s
    form = 'M' + 'L'.join(f'{x * s:.2f} {y * s:.2f}' for x, y in F['kontur']) + 'Z'
    innen = f'<path d="{form}" fill="#faf4f4"/><image href="bild/fig_{k}.png" x="0" y="0" width="{b:.2f}" height="{hoehe}" preserveAspectRatio="none"/>'
    return b, hoehe, form, innen, F['name']


def glas_kerze(d):
    c = d / 2
    return (f'<path d="{kreis(d)}" fill="{NACHT}"/>' + ring_kreis(d, KERZE, 2.4)
            + f'<path d="M{c - 13} {c - 8}Q{c - 4} {c + 6} {c - 4} {c + 2}" fill="none"/>'
            + f'<path d="M{c - 15} {c - 9}H{c - 1}Q{c - 3} {c + 3} {c - 8} {c + 4}Q{c - 13} {c + 3} {c - 15} {c - 9}Z" fill="none" stroke="{WEISS}" stroke-width=".6"/>'
            + f'<path d="M{c - 8} {c + 4}V{c + 15}M{c - 13} {c + 15}H{c - 3}" stroke="{WEISS}" stroke-width=".6" fill="none"/>'
            + f'<rect x="{c + 4}" y="{c - 2}" width="8" height="17" rx=".6" fill="{CREME}"/>'
            + f'<path d="M{c + 8} {c - 11}C{c + 11} {c - 7} {c + 10} {c - 3.5} {c + 8} {c - 3}C{c + 6} {c - 3.5} {c + 5} {c - 7} {c + 8} {c - 11}Z" fill="{KERZE}"/>'
            + f'<path d="M{c + 8} {c - 2.8}V{c - 2}" stroke="{NACHT}" stroke-width=".4"/>')


def alle():
    S, n = [], [0]

    def s(b, h, form, innen, name, satz):
        n[0] += 1
        S.append(etikett(f's{n[0]:02d}', b, h, form, innen, name, satz))
    T = N_TELLER
    hauskreis = lambda: ring_kreis(56, KERZEH, 2.4)
    # gemischt: Form, Grösse und Farbe wechseln von Stück zu Stück
    s(46, 46, kreis(46), grund(kreis(46), KERZE) + hzz(23, 11, 22, NACHT), 'Das C in Kerze', 'Rund, 46 mm. Das C aus Rudis Wortmarke.')
    b, h, f, i, nm = figur('DbYnkdkjrNy', 74); s(b, h, f, i, nm, f'Gestanzt, {h} mm hoch. Die {nm} aus Rudis Plakat vom September 2026, freigestellt.')
    s(100, 22, kapsel(100, 22), grund(kapsel(100, 22), NACHT) + tx(50, 13.6, e(T[0].upper()), 4.4, WEISS, 's', .06, 'middle', 'font-weight="340"'), T[0], 'Kapsel, 100 mm. Rudis Teller, wie er ihn schreibt.')
    s(56, 56, siegel(56), grund(siegel(56), SCHIEFER) + P.bogen_text('mr', 'M10 28A18 18 0 1 1 46 28A18 18 0 1 1 10 28', 'MOMO UND RUDI · MOMO UND RUDI · ', 2.6, KERZEH, 'm', .16) + hzz(28, 19, 16, WEISS),
      'Momo und Rudi', 'Gestanzt als Siegel, 56 mm. Die beiden Namen rundherum, in der Mitte das C.')
    s(80, 40, ticket(80, 40), grund(ticket(80, 40), WEISS) + f'<line x1="58" y1="4" x2="58" y2="36" stroke="{KERZET}" stroke-width=".35" stroke-dasharray="1 1.2"/><circle cx="69" cy="20" r="2.2" fill="none" stroke="{KERZET}" stroke-width=".35"/>'
      + mo(29, 13, 'Ticket · Culinarium', 1.9, KERZET) + fr(29, 24, '27. und 28. November', 4.8, SCHIEFER) + mo(29, 31, 'Freitag 19 Uhr', 1.8, KERZET),
      'Ticket November', 'Gestanzt als Ticket, 80 × 40 mm, mit Lochung und Abriss.')
    s(56, 56, kreis(56), grund(kreis(56), NACHT) + hauskreis() + fr(28, 18, 'Ich war', 5, KERZEH) + fr(28, 25, 'an der langen', 5, WEISS) + fr(28, 31.5, 'Tafel', 5, WEISS)
      + f'<rect x="15" y="37" width="26" height="8" rx="1" fill="none" stroke="{KERZEH}" stroke-width=".35" stroke-dasharray="1 .9"/>' + mo(28, 42.6, 'Datum', 1.6, KERZEH),
      'Ich war an der langen Tafel', 'Rund, 56 mm. Mit Feld für den Datum-Stempel des Abends.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), WEISS) + bildel('po_DbYnkdkjrNy', 2.5, 2.5, 55, 55, 'kp0'), 'Plakat: Tanz auf dem Mond', 'Eckig, 60 mm. Rudis Plakat ganz, mit schmalem Rand.')
    s(90, 26, kapsel(90, 26), grund(kapsel(90, 26), KERZE) + mo(45, 12.6, 'Walk on the Wild Side', 3, NACHT, .12) + mo(45, 18.6, 'Hannover-Linden', 2.2, NACHT, .14),
      'Walk on the Wild Side', 'Kapsel, 90 mm. Die Bar, in der die Tafel steht.')
    b, h, f, i, nm = figur('DFqbLG2s_dc', 60); s(b, h, f, i, nm, f'Gestanzt, {h} mm hoch. Aus Rudis Plakat vom Februar 2025, freigestellt.')
    dz = (N.dc_weiss(), 'bild/dc-weiss.webp')[1]
    s(56, 56, kreis(56), grund(kreis(56), VIOLETT) + f'<image href="{dz}" x="12" y="9" width="32" height="32" preserveAspectRatio="xMidYMid meet"/>' + mo(28, 49, 'Dirty Chicken', 2.2, WEISS), 'Dirty Chicken', 'Rund, 56 mm. Das D mit dem Hühnerfuss auf Violett.')
    s(56, 56, kreis(56), glas_kerze(56), 'Glas und Kerze', 'Rund, 56 mm. Ein Glas und eine Kerze, wie auf der Tafel.')
    s(56, 56, siegel(56), grund(siegel(56), KERZE) + hzz(28, 11, 13, NACHT) + fr(28, 34.5, 'Von Hand', 6, NACHT) + fr(28, 41.5, 'angerichtet', 6, NACHT), 'Von Hand angerichtet', 'Gestanzt als Siegel, 56 mm.')
    s(100, 30, kapsel(100, 30), grund(kapsel(100, 30), WEISS) + ''.join(tx(50, 13.4 + k * 7, e(z), 4.4, SCHIEFER, 's', .06, 'middle', 'font-weight="340"') for k, z in enumerate(['BLUMENKOHL / ROQUEFORT', 'KAPERN / QUINOA'])), T[1], 'Kapsel, 100 mm. Rudis Teller.')
    s(40, 40, kreis(40), grund(kreis(40), NACHT) + hzz(20, 10, 18, KERZE), 'Das C auf der Nacht', 'Rund, 40 mm.')
    b, h, f, i, nm = figur('DJw8OqGMY1G', 70); s(b, h, f, i, nm, f'Gestanzt, {h} mm hoch. Aus Rudis Plakat vom Juni 2025, freigestellt.')
    s(44, 62, schild(44, 62), grund(schild(44, 62), NACHT) + hzz(22, 10, 14, KERZE) + fr(22, 38, 'Rudi kocht.', 5.2, WEISS) + fr(22, 46, 'Momo mixt.', 5.2, WEISS), 'Rudi kocht. Momo mixt.', 'Gestanzt als Schild mit Bogen, 44 × 62 mm.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), WEISS) + bildel('po_DVjkofijp6R', 2.5, 2.5, 55, 55, 'kp1'), 'Plakat: Panther und Spaghetti-Eis', 'Eckig, 60 mm.')
    s(90, 30, kapsel(90, 30), grund(kapsel(90, 30), VIOLETT) + fr(45, 19.4, 'Dirty Food & Dirty Drinks', 6, WEISS), 'Dirty Food & Dirty Drinks', 'Kapsel, 90 mm.')
    s(80, 40, ticket(80, 40), grund(ticket(80, 40), NACHT) + f'<line x1="58" y1="4" x2="58" y2="36" stroke="{KERZEH}" stroke-width=".35" stroke-dasharray="1 1.2"/><circle cx="69" cy="20" r="2.2" fill="none" stroke="{KERZEH}" stroke-width=".35"/>'
      + mo(29, 13, 'Ticket · Culinarium', 1.9, KERZEH) + fr(29, 24, '18. und 19. Dezember', 4.8, WEISS) + mo(29, 31, 'Samstag 17 Uhr', 1.8, KERZEH),
      'Ticket Dezember', 'Gestanzt als Ticket, 80 × 40 mm, mit Lochung.')
    s(64, 64, kreis(64), grund(kreis(64), NACHT) + ring_text('rw', 64, ZEILE, KERZEH, 2.4, 6.5) + hwz(32, 29.5, 34, WEISS), 'Wortmarke im Kreis', 'Rund, 64 mm. Rudis Wortmarke, rundherum die Zeile der Plakate.')
    for j, (w, f2) in enumerate([('Fatwashing', KERZE), ('Milkwashing', '#b3ebfc'), ('Enzyme', '#94b253')]):
        s(44, 44, kreis(44), grund(kreis(44), NACHT) + ring_kreis(44, f2, 2) + mo(22, 15, 'Momo zeigt', 1.9, f2) + fr(22, 26, w, 5.6 if len(w) < 11 else 5, WEISS), w, 'Rund, 44 mm. Eine von Momos Techniken.')
        if j == 0:
            b, h, f, i, nm = figur('DCCf-ikoaGs', 64); s(b, h, f, i, nm, f'Gestanzt, {h} mm hoch. Aus Rudis Plakat vom November 2024, freigestellt.')
        if j == 1:
            s(70, 40, ticket(70, 40), grund(ticket(70, 40), WEISS) + mo(35, 13, 'Dirty Chicken', 2.1, VIOLETT) + fr(35, 26, 'Dit is keen Burger.', 5.6, VIOLETT), 'Dit is keen Burger.', 'Gestanzt als Ticket, 70 × 40 mm.')
    s(56, 56, siegel(56), grund(siegel(56), WEISS) + mo(28, 18, 'Momo', 2.4, KERZET) + fr(28, 30, 'Jeder Drink', 6, SCHIEFER) + fr(28, 37.5, 'wird erklärt', 6, SCHIEFER), 'Jeder Drink wird erklärt', 'Gestanzt als Siegel, 56 mm.')
    s(100, 30, kapsel(100, 30), grund(kapsel(100, 30), KERZE) + ''.join(tx(50, 10.6 + k * 5.6, e(z), 4.4, NACHT, 's', .06, 'middle', 'font-weight="340"') for k, z in enumerate(['HOKKAIDO', 'KÜRBISKERNÖL', 'HASELNUSS'])), T[2], 'Kapsel, 100 mm. Rudis Teller.')
    b, h, f, i, nm = figur('DPwlqcfiKcA', 62); s(b, h, f, i, nm, f'Gestanzt, {h} mm hoch. Aus Rudis Plakat vom November 2025, freigestellt.')
    s(44, 62, schild(44, 62), grund(schild(44, 62), WEISS) + mo(22, 20, 'Seit 2023', 2.3, KERZET) + fr(22, 34, 'An der', 6, SCHIEFER) + fr(22, 42, 'langen Tafel', 6, SCHIEFER), 'An der langen Tafel', 'Gestanzt als Schild mit Bogen, 44 × 62 mm.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), WEISS) + bildel('po_DJw8OqGMY1G', 2.5, 2.5, 55, 55, 'kp2'), 'Plakat: Spargel im Gewächshaus', 'Eckig, 60 mm.')
    s(56, 56, siegel(56), grund(siegel(56), VIOLETT) + mo(28, 22, 'Pop-up', 2.6, WEISS) + fr(28, 34, 'Nur an', 6, WEISS) + fr(28, 41, 'einzelnen Tagen', 4.6, WEISS), 'Nur an einzelnen Tagen', 'Gestanzt als Siegel, 56 mm.')
    s(40, 40, kreis(40), grund(kreis(40), WEISS) + ring_kreis(40, KERZE, 2) + hzz(20, 10, 18, SCHIEFER), 'Das C auf Warmweiss', 'Rund, 40 mm.')
    s(90, 34, eck(90, 34, 2), grund(eck(90, 34, 2), WEISS) + ring_eck(90, 34, KERZE) + hwz(45, 9.5, 64, SCHIEFER) + tx(45, 26.5, e(ZEILE), 2.1, KERZET, 'i', .06, 'middle', 'font-weight="600" font-family="Urbanist"'), 'Wortmarke mit Zeile', 'Eckig, 90 × 34 mm.')
    s(80, 40, ticket(80, 40), grund(ticket(80, 40), KERZE) + f'<line x1="58" y1="4" x2="58" y2="36" stroke="{NACHT}" stroke-width=".35" stroke-dasharray="1 1.2"/><circle cx="69" cy="20" r="2.2" fill="none" stroke="{NACHT}" stroke-width=".35"/>'
      + mo(29, 13, 'Ticket · Culinarium', 1.9, NACHT) + fr(29, 24, 'Dein Platz an der Tafel', 4.6, NACHT) + mo(29, 31, 'Haasemannstrasse 13', 1.8, NACHT), 'Ticket Platz', 'Gestanzt als Ticket, 80 × 40 mm, mit Lochung.')
    s(80, 22, kapsel(80, 22), grund(kapsel(80, 22), NACHT) + mo(40, 13.2, '@dirtychicken.hannover', 2.8, '#c9a6dc', .08), '@dirtychicken.hannover', 'Kapsel, 80 mm.')
    s(100, 30, kapsel(100, 30), grund(kapsel(100, 30), SCHIEFER) + ''.join(tx(50, 13.4 + k * 7, e(z), 4.4, WEISS, 's', .06, 'middle', 'font-weight="340"') for k, z in enumerate(['SPAGHETTI-EIS / KIWI', 'WEISSE SCHOKOLADE'])), T[3], 'Kapsel, 100 mm. Rudis Teller.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), WEISS) + bildel('po_DPwlqcfiKcA', 2.5, 2.5, 55, 55, 'kp3'), 'Plakat: Kürbis bei Kerzen', 'Eckig, 60 mm.')
    s(90, 26, kapsel(90, 26), grund(kapsel(90, 26), WEISS) + mo(45, 15.4, 'Haasemannstrasse 13 · Linden', 3, KERZET, .12), 'Haasemannstrasse 13', 'Kapsel, 90 mm.')
    s(52, 70, schild(52, 70), grund(schild(52, 70), SCHIEFER) + hzz(26, 11, 15, KERZEH) + mo(26, 37, 'Culinarium', 2.1, KERZEH) + fr(26, 48, 'Ein Abend,', 6, WEISS) + fr(26, 56, 'eine Tafel.', 6, WEISS), 'Ein Abend, eine Tafel.', 'Gestanzt als Schild mit Bogen, 52 × 70 mm.')
    s(56, 56, kreis(56), grund(kreis(56), KERZE) + mo(28, 21, 'Bis zum', 2.4, NACHT) + fr(28, 32, 'nächsten', 6.2, NACHT) + fr(28, 39.5, 'Abend', 6.2, NACHT), 'Bis zum nächsten Abend', 'Rund, 56 mm. Zum Abschied, auf die Tüte oder die Box.')
    return S


def fertig(S):
    """Satzdateien und Druckbögen wie papier_kern.fertig, aber für den Ordner sticker/."""
    alle = ''
    for x in S:
        svg = f'<svg class="abs" style="inset:0;width:{x["b"]}mm;height:{x["h"]}mm" viewBox="0 0 {x["b"]} {x["h"]}">{x["innen"]}</svg>'
        alle += blatt(x['b'], x['h'], svg, 'etikett', 'background:transparent')
    P.seite('sticker', [alle], 'Sticker')
    boegen, akt, x0, y0, zh = [], [], 14, 16, 0
    for x in S:
        if x0 + x['b'] > 420 - 14:
            x0, y0, zh = 14, y0 + zh + 9, 0
        if y0 + x['h'] > 297 - 12:
            boegen.append(akt); akt, x0, y0, zh = [], 14, 16, 0
        akt.append((x, x0, y0)); x0 += x['b'] + 9; zh = max(zh, x['h'])
    boegen.append(akt)
    seiten = []
    for nr, akt in enumerate(boegen):
        inn = ''.join(f'<svg class="abs" style="left:{ox}mm;top:{oy}mm;width:{x["b"]}mm;height:{x["h"]}mm;overflow:visible" viewBox="0 0 {x["b"]} {x["h"]}">'
                      f'{x["innen"].replace("id=\"", "id=\"b" + x["id"]).replace("url(#", "url(#b" + x["id"]).replace("href=\"#", "href=\"#b" + x["id"]).replace("#b" + x["id"] + "hz", "#hz").replace("#b" + x["id"] + "hw", "#hw")}'
                      f'<path d="{x["form"]}" fill="none" stroke="#e6007e" stroke-width=".15"/></svg>' for x, ox, oy in akt)
        inn += t(14, 6.5, f'{e(H.NAME)} · Sticker · Druckbogen {nr + 1} von {len(boegen)} · A3 quer · Originalgröße · Schnittlinie in Magenta', 'm', 'font-size:2.1mm;color:#26242d')
        seiten.append(blatt(420, 297, inn, '', 'background:#fff'))
    P.seite('sticker-bogen', seiten, 'Sticker, Druckbogen')
    plan = {'etiketten': [{k: x[k] for k in ('id', 'b', 'h', 'name', 'satz', 'form')} for x in S], 'boegen': len(boegen),
            'masse': [min(min(x['b'], x['h']) for x in S), max(max(x['b'], x['h']) for x in S)]}
    json.dump(plan, open(os.path.join(W, 'sticker_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Sticker gesetzt:', len(S), 'Stück,', len(boegen), 'Druckbögen')


def seite():
    """sticker/index.html mit der Seite der Untersetzer (papier_seiten.etiketten), umgestellt auf den Ordner sticker/."""
    import papier_seiten as PS
    plan = json.load(open(os.path.join(W, 'sticker_plan.json')))
    PS.plan = dict(PS.plan, etiketten=plan['etiketten'], boegen=plan['boegen'], masse=plan['masse'])
    PS.ROH = os.path.join(W, 'roh', 'sticker')
    PS.ET = dict(ordner='sticker', name='Sticker', einzahl='Sticker')
    PS.S = dict(PS.S, etik_titel=('Sticker', 'für alles, was rausgeht.'),
                etik_text='Für die Box mit dem Absacker, das Glas, die Tüte vom Pop-up und das Notizbuch der Gäste: {n} Ideen, rund, eckig und gestanzt.',
                etik_kap='Die Sticker', etik_kopf=['Vierzig', 'Sticker.'],
                etik_kopftext='Das C aus Rudis Wortmarke, die Wortmarke selbst, Rudis Zeilen, seine Plakate ganz, Sätze der Bar, Dirty Chicken und die Farben eurer Abende.',
                etik_auslage=[(2, 4, 24, -5), (30, 0, 24, 4), (58, 6, 20, -3), (78, 2, 20, 6), (4, 34, 34, 3), (42, 36, 22, -4), (68, 34, 26, 5), (10, 66, 30, 2), (46, 64, 24, -3), (74, 66, 22, 4)]
                + [(0, 0, 0, 0)] * 30, etik_haufen=None)
    PS.etiketten()
    glieder_titel(os.path.join(os.path.dirname(W), 'sticker', 'index.html'))
    print('Seite gebaut: sticker/ ·', len(plan['etiketten']), 'Sticker')


def glieder_titel(pfad):
    """Tor 4, 30.10.2026 (K7): Rudis Zeilen als Titel («LAUCH / BLUMENKOHL / CHIPOTLE») stehen Glied für Glied untereinander; der Schrägstrich bleibt
    für Vorleseprogramme im Text, steht aber nie sichtbar am Zeilenanfang oder -ende, und kein Glied bleibt allein in einer halben Zeile."""
    import re
    t = open(pfad, encoding='utf-8').read()
    def h3(m):
        teile = re.split(r'[\s\xa0]+/\s+', m.group(1))
        if len(teile) < 2: return m.group(0)
        return '<h3 class="gl3">' + '<span class="tr"> / </span>'.join(f'<span class="gl">{x}</span>' for x in teile) + '</h3>'
    t = re.sub(r'<h3>([^<]*)</h3>', h3, t)
    t = t.replace('und Ihre Unterlagen im selben Stil', 'und eure Unterlagen im selben Stil').replace('Originalgrösse', 'Originalgröße')   # Tor 4 30.10.2026: Du wie überall, ß wie auf den anderen Seiten
    css = '<style>.gl3 .gl{display:block}.gl3 .tr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}</style>'
    if '.gl3 .gl' not in t: t = t.replace('</head>', css + '</head>', 1)
    open(pfad, 'w', encoding='utf-8').write(t)


N_TELLER = []
if __name__ == '__main__':
    import papier as PA
    N_TELLER[:] = PA.TELLER
    if '--seite' in sys.argv:
        import kern as K
        K.gestaltung(); seite()
    else:
        fertig(alle())
