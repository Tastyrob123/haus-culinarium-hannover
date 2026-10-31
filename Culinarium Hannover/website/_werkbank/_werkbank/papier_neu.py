#!/usr/bin/env python3
"""Culinarium: zwanzig weitere Drucksachen für Tafel, Theke und Abend (Prüfchat Gestaltung 29.10.2026, Auftrag Oberchef nach Robert:
«die Drucksachen ist viel zu wenig … 24 draus machen»). Von papier.py eingebunden (NEU, SEITE). Satz nach dem Stilblatt der Drucksachen
(_werkzeuge/imprimerie/haeuser/culinarium/STILBLATT-DRUCKSACHEN.md): eine Achse, Zeichen und Inhalt als Gruppe auf der optischen Mitte,
Kopf- und Fusszeile gleich weit vom Rahmen, Schriftgrösse nach Zweck, ein Zeichen je Haus (das C), kein Zierzeichen.
Inhalte aus der Website und den Vorlagen der Plakatwerkstatt gelesen; Namen und Nummern sind Beispielwerte. Rudis Plakate stehen nur ganz."""
import json, os
import papier_kern as P
from papier_kern import blatt, e, SATZ
from kern import ROOT

WEB = os.path.dirname(ROOT)
PROJ = os.path.dirname(WEB)
BILD = os.path.join(PROJ, '_werkzeuge', 'imprimerie', 'haeuser', 'culinarium', 'bilder')
VORL = os.path.join(PROJ, '_werkzeuge', 'imprimerie', 'haeuser', 'culinarium', 'vorlagen')
NACHT, WEISS, CREME, SCHIEFER, TINTE, LEISE = '#16151a', '#faf4f4', '#f3ecea', '#3a3845', '#26242d', '#5b5763'
KERZE, KERZEH, KERZET, VIOLETT = '#ef7649', '#f5a689', '#b15736', '#8953a9'
_Z = os.path.relpath(os.path.join(WEB, 'assets', 'zeichen'), SATZ)
TAPETE = f'url({_Z}/tapete-dunkel.svg) 50% 0/16mm auto'
TAPETE_H = f'url({_Z}/tapete-hell.svg) 50% 0/16mm auto'
ADR = 'Haasemannstraße 13 · 30449 Hannover'
ZEILE = 'A UNiQUE EXPERiENCE BY MOMO X RUDI'
FR, MO, IN = "'Fraunces',Georgia,serif", "'DM Mono',Menlo,monospace", "'Instrument Sans',Arial,sans-serif"

TOENE = {
    'dunkel': dict(grund=f'background:{NACHT} {TAPETE}', titel=WEISS, text=CREME, et=KERZEH, linie=KERZE, zeichen=KERZE, rahmen='rgba(239,118,73,.75)'),
    'hell': dict(grund=f'background:{WEISS}', titel=SCHIEFER, text=TINTE, et=KERZET, linie=KERZE, zeichen=SCHIEFER, rahmen='rgba(239,118,73,.75)'),
    'creme': dict(grund=f'background:{CREME} {TAPETE_H}', titel=SCHIEFER, text=TINTE, et=KERZET, linie=KERZE, zeichen=SCHIEFER, rahmen='rgba(239,118,73,.75)'),
    'dc': dict(grund=f'background:{VIOLETT}', titel=WEISS, text=WEISS, et=WEISS, linie=WEISS, zeichen=WEISS, rahmen='rgba(250,244,244,.7)'),
}


def vorlage(art, ident):
    return next(v for v in json.load(open(os.path.join(VORL, art + '.json'), encoding='utf-8'))['vorlagen'] if v['id'] == ident)


def bild(key):
    """Foto aus den Bildern der Plakatwerkstatt, kopiert unter satz/bild/ (der Vorschau-Server liefert nur die Werkbank aus)."""
    import shutil
    z = os.path.join(SATZ, 'bild'); os.makedirs(z, exist_ok=True)
    q, ziel = os.path.join(BILD, key + '.webp'), os.path.join(z, key + '.webp')
    if not os.path.exists(ziel) or os.path.getmtime(ziel) < os.path.getmtime(q):
        shutil.copy2(q, ziel)
    return 'bild/' + key + '.webp'


# ---------------------------------------------------------------- Bausteine im Fluss (Masse in mm)
def zw(b, farbe):
    """Das C aus Rudis Wortmarke, im Fluss."""
    vb = P.H.ZEICHEN[0]; _, _, w, h = (float(x) for x in vb.split())
    return f'<svg viewBox="{vb}" style="display:block;width:{b}mm;height:{b * h / w}mm;color:{farbe};flex:none" fill="currentColor"><use href="#hz"/></svg>'


def wm(b, farbe):
    vb = P.H.WORT[0]; _, _, w, h = (float(x) for x in vb.split())
    return f'<svg viewBox="{vb}" style="display:block;width:{b}mm;height:{b * h / w}mm;color:{farbe};flex:none" fill="currentColor"><use href="#hw"/></svg>'


def dc_weiss():
    """Das D von Dirty Chicken in Warmweiss (das Original ist violett und verschwindet auf seinem eigenen Grund), unter satz/bild/."""
    from PIL import Image
    z = os.path.join(SATZ, 'bild', 'dc-weiss.webp'); os.makedirs(os.path.dirname(z), exist_ok=True)
    im = Image.open(os.path.join(WEB, 'assets', 'zeichen', 'dc-original.webp')).convert('RGBA')
    w = Image.new('RGBA', im.size, (250, 244, 244, 0)); w.putalpha(im.getchannel('A')); w.save(z, 'WEBP', quality=92)


def dz(b):
    """Das D mit Hühnerfuss von Dirty Chicken (nur auf seinen Stücken)."""
    import shutil
    dc_weiss()
    return f'<img src="bild/dc-weiss.webp" style="display:block;width:{b}mm;height:auto;flex:none" alt="">'


def et(text, gr, farbe, sp=.12):
    return f'<div style="font:400 {gr}mm/1.4 {MO};letter-spacing:{sp}em;text-transform:uppercase;color:{farbe};text-wrap:balance">{e(text)}</div>'


def ti(text, gr, farbe, zl=1.1):
    return f'<div style="font:340 {gr}mm/{zl} {FR};color:{farbe};text-wrap:balance">{text}</div>'


def rz(text, gr, farbe):
    """Rudis Zeile: Versalien mit Schrägstrich, wie er sie schreibt; umbrochen nur zwischen den Gliedern."""
    teile = [x.strip() for x in text.split('/')]
    g = ' '.join(f'<span style="white-space:nowrap">{e(x)}{"" if k == len(teile) - 1 else " /"}</span>' for k, x in enumerate(teile))
    return f'<div style="font:340 {gr}mm/1.3 {FR};letter-spacing:.06em;text-transform:uppercase;color:{farbe};text-wrap:balance">{g}</div>'


def tx(text, gr, farbe, breite=None, zl=1.45):
    b = f'max-width:{breite}mm;' if breite else ''
    return f'<div style="font:400 {gr}mm/{zl} {IN};color:{farbe};{b}text-wrap:balance">{e(text)}</div>'


def glieder(text, gr, farbe, art='titel'):
    """Momos Zeilen mit « | »: Umbruch nur zwischen den Gliedern."""
    f = FR if art == 'titel' else IN
    teile = [x.strip() for x in text.split('|')]
    g = ' '.join(f'<span style="white-space:nowrap">{e(x)}{"" if k == len(teile) - 1 else " <span style=opacity:.55>|</span>"}</span>' for k, x in enumerate(teile))
    return f'<div style="font:{340 if art == "titel" else 400} {gr}mm/1.3 {f};color:{farbe};text-wrap:balance">{g}</div>'


def li(b, farbe, d=.35):
    return f'<i style="display:block;width:{b}mm;height:{d}mm;background:{farbe};flex:none"></i>'


def ab(mm):
    return f'<i style="display:block;height:{mm}mm;flex:none"></i>'


def foto(key, b, h, lage='50% 50%', rand=None):
    r = f'outline:.3mm solid {rand};outline-offset:1.4mm;' if rand else ''
    return f'<img src="{e(bild(key))}" style="display:block;width:{b}mm;height:{h}mm;object-fit:cover;object-position:{lage};{r}flex:none" alt="">'


def ganz(key, b):
    """Rudis Plakat ganz, nie beschnitten."""
    return f'<img src="{e(bild(key))}" style="display:block;width:{b}mm;height:auto;flex:none" alt="">'


def zeit(paare, gr, ton, breite):
    """Zeitleiste: Uhrzeit in DM Mono, Schritt daneben, als Block mittig."""
    T = TOENE[ton]
    z = ''.join(f'<div style="display:flex;gap:{gr * 1.1}mm;align-items:baseline;margin:{gr * .55}mm 0"><span style="flex:none;width:{gr * 3.6}mm;font:400 {gr * .8}mm/1 {MO};letter-spacing:.06em;color:{T["et"]}">{e(a)}</span>'
                f'<span style="font:400 {gr}mm/1.3 {IN};color:{T["text"]};text-align:left">{e(b)}</span></div>' for a, b in paare)
    return f'<div style="max-width:{breite}mm">{z}</div>'


def seite(b, h, ton, inhalt, rahmen=True, kopf='Walk on the Wild Side', fuss=ADR + ' · @culinarium_hannover', unten='', extra=''):
    """Eine Seite: Rahmen, Kopf- und Fusszeile gleich weit vom Rahmen, die Gruppe im Fluss auf der optischen Mitte."""
    T, u = TOENE[ton], min(b, h)
    r = max(4.5, .045 * u); a = r + max(3.5, .05 * u); g = max(1.5, .014 * u)
    rah = f'<i class="abs" style="left:{r}mm;top:{r}mm;width:{b - 2 * r}mm;height:{h - 2 * r}mm;border:{max(.25, .0018 * u)}mm solid {T["rahmen"]};border-radius:{max(1.2, .011 * u)}mm"></i>' if rahmen else ''
    k = f'<div class="abs" style="left:0;top:{a}mm;width:{b}mm;text-align:center">{et(kopf, g, T["et"], .1)}</div>' if kopf else ''
    f = f'<div class="abs" style="left:{r + .06 * u}mm;bottom:{a}mm;width:{b - 2 * (r + .06 * u)}mm;text-align:center">{et(fuss, g, T["et"], .08)}</div>' if fuss else ''
    ob, un = (a + g * 2.4) if kopf else r, (a + g * 2.4) if fuss else r
    mitte = (f'<div class="abs" style="left:{r + .07 * u}mm;width:{b - 2 * (r + .07 * u)}mm;top:{ob + .03 * u}mm;bottom:{un + .03 * u}mm;display:flex;flex-direction:column;'
             f'align-items:center;justify-content:safe center;text-align:center;padding-bottom:{.06 * (h - ob - un)}mm">{inhalt}</div>')
    return blatt(b, h, f'<i class="abs" style="inset:0;{T["grund"]}"></i>' + extra + rah + k + mitte + f + unten, '', f'background:{NACHT if ton == "dunkel" else WEISS}')


def bild_oben(b, h, ton, key, anteil, inhalt, lage='50% 50%', fuss=ADR + ' · @culinarium_hannover'):
    """Foto randlos oben, das C auf der Naht, darunter die Gruppe."""
    T, u = TOENE[ton], min(b, h)
    ph = h * anteil; d = .15 * u
    oben = (f'<img class="abs" src="{e(bild(key))}" style="left:0;top:0;width:{b}mm;height:{ph}mm;object-fit:cover;object-position:{lage}">'
            f'<i class="abs" style="left:{(b - d) / 2}mm;top:{ph - d / 2}mm;width:{d}mm;height:{d}mm;border-radius:50%;{T["grund"]}"></i>'
            f'<div class="abs" style="left:{(b - d * .6) / 2}mm;top:{ph - d * .3}mm">{zw(d * .6, T["zeichen"]) if ton != "dc" else dz(d * .6)}</div>')
    r = max(4.5, .045 * u); a = r + max(3.5, .05 * u); g = max(1.5, .014 * u)
    f = f'<div class="abs" style="left:{r}mm;bottom:{a}mm;width:{b - 2 * r}mm;text-align:center">{et(fuss, g, T["et"], .08)}</div>'
    mitte = (f'<div class="abs" style="left:{r + .06 * u}mm;width:{b - 2 * (r + .06 * u)}mm;top:{ph + d / 2 + .04 * u}mm;bottom:{a + g * 2.4 + .03 * u}mm;display:flex;flex-direction:column;'
             f'align-items:center;justify-content:center;text-align:center">{inhalt}</div>')
    return blatt(b, h, f'<i class="abs" style="inset:0;{T["grund"]}"></i>' + oben + mitte + f, '', f'background:{NACHT}')


# ---------------------------------------------------------------- die zwanzig Stücke
def stuecke(TELLER, TECHNIK):
    NEU, SEITE = [], {}

    def d(ident, name, format_, blaetter, karton, titel, satz, quelle, breit=False):
        namen = [n for n, _, _ in karton]
        NEU.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=[(n, i + 1) for i, n in enumerate(namen)], satz=satz, quelle=quelle))
        SEITE[ident] = dict(karton=('', karton), titel=titel, breit=set(namen) if breit else set())

    mk = vorlage('menuekarte', 'menuekarte-005')   # Februar 2025, Momos Karte mit « | »
    gaenge = ''.join(et(g['gang'], 2.2, KERZET, .14) + ab(1.8) + glieder(g['name'], 5.3, SCHIEFER) + ab(1.4) + glieder(g['detail'], 3.0, LEISE, 'text') + ab(8.5)
                     for g in mk['inhalt']['liste'] if g['name'])
    d('menue', 'Menükarte des Abends', 'DL hoch, 99 × 210 mm', [seite(99, 210, 'hell', wm(58, SCHIEFER) + ab(2.4) + f'<div style="font:600 1.75mm/1 Urbanist,{IN};letter-spacing:.06em;color:{KERZET}">{ZEILE}</div>' + ab(12)
                                                                  + ti('Menü', 13, SCHIEFER, 1) + ab(2.6) + et(mk['inhalt']['ueber'], 2.2, KERZET) + ab(4.5) + li(9, KERZE) + ab(10) + gaenge,
                                                                  kopf='', fuss='Walk on the Wild Side · ' + ADR)],
      [('menue', 40, '')], ['Die Menükarte', 'am Platz.'],
      'Oben Rudis Wortmarke mit der Zeile der Plakate, darunter «Menü», das Datum und die Gänge, jeder mit seinem Drink. Hier mit der Karte vom Februar 2025.',
      'Menükarten der Abende (Website, «Alle Abende»)')

    d('platzkarte', 'Platzkarte', 'A7 quer, 105 × 74 mm', [seite(105, 74, 'hell', zw(10, SCHIEFER) + ab(4) + ti('Lena Brandt', 11, SCHIEFER) + ab(3.4) + li(8, KERZE) + ab(3.4) + et('Dein Platz an der Tafel', 1.9, KERZET), kopf='', fuss=''),
                                                           seite(105, 74, 'dunkel', zw(10, KERZE) + ab(4) + ti('Jonas Weber', 11, WEISS) + ab(3.4) + li(8, KERZE) + ab(3.4) + et('Dein Platz an der Tafel', 1.9, KERZEH), kopf='', fuss='')],
      [('platz-h', 46, 'Warmweiss'), ('platz-d', 46, 'Nacht')], ['Ein Name', 'für jeden Platz.'],
      'Eine Karte mit dem Namen jedes Gastes, hell oder auf der Nacht der Bar. Der Name trägt die Karte, darüber das C.', 'Namen als Beispiel')

    d('reserviert', 'Die Tafel ist reserviert', 'A6 hoch, als Aufsteller', [seite(105, 148, 'dunkel', zw(15, KERZE) + ab(6.5) + et('Heute Abend', 2.1, KERZEH) + ab(4) + ti('Die lange Tafel ist reserviert.', 11, WEISS) + ab(5.5) + li(9, KERZE) + ab(6)
                                                                                    + tx('Ab 19 Uhr sitzen hier die Gäste von Culinarium. Die Bar ist für euch wie immer geöffnet.', 4.4, CREME, 80))],
      [('reserviert', 42, '')], ['Die Tafel', 'ist reserviert.'],
      'Steht am Nachmittag auf der langen Tafel, damit sich niemand an den gedeckten Platz setzt.', 'Website, «Der Abend»')

    d('willkommen', 'Willkommen am Platz', 'A6 hoch, 105 × 148 mm', [seite(105, 148, 'creme', zw(13, SCHIEFER) + ab(5.5) + et('Culinarium', 2.0, KERZET) + ab(3.6) + ti('Schön, dass du da bist.', 11, SCHIEFER) + ab(5) + li(9, KERZE) + ab(5)
                                                                    + zeit([('19:00', 'Ankommen, der Aperitif'), ('19:30', 'Drei Gänge von Rudi'), ('', 'Zu jedem Gang ein Drink von Momo'), ('22:30', 'Der Absacker')], 3.8, 'creme', 76))],
      [('willkommen', 42, '')], ['Willkommen', 'am Platz.'],
      'Liegt auf dem Teller, wenn die Gäste kommen: wie der Abend läuft, als kleine Zeitleiste.', 'Website, «Der Abend»')

    d('ausgebucht', 'Heute ausgebucht', 'A4 hoch, Aushang', [seite(210, 297, 'dunkel', zw(28, KERZE) + ab(11) + et('Culinarium', 3.5, KERZEH) + ab(7) + ti('Heute ausgebucht', 28, WEISS) + ab(10) + li(17, KERZE) + ab(11)
                                                                + tx('Der Abend ist ausgebucht, bevor er beginnt. Auf die Warteliste kommst du über Instagram.', 8, CREME, 150) + ab(13) + et('@culinarium_hannover', 3.5, KERZEH), fuss=ADR)],
      [('ausgebucht', 44, '')], ['Heute', 'ausgebucht.'],
      'Für die Tür der Bar, aus drei Metern lesbar.', 'Website, «Der Abend»')

    d('warteliste', 'Auf die Warteliste', 'A4 hoch, Aushang', [seite(210, 297, 'creme', zw(28, SCHIEFER) + ab(11) + et('Culinarium', 3.5, KERZET) + ab(7) + ti('Auf die Warteliste', 26, SCHIEFER) + ab(10) + li(17, KERZE) + ab(11)
                                                                 + tx('Vierzehn Plätze an einer Tafel. Trag dich ein: Sobald der nächste Abend feststeht, erfährst du es vor allen anderen.', 7.6, TINTE, 156) + ab(13) + et('@culinarium_hannover', 3.5, KERZET), fuss=ADR)],
      [('warteliste', 44, '')], ['Auf die', 'Warteliste.'],
      'Hängt an der Theke, wenn ein Abend voll ist.', 'Website, Warteliste')

    d('plakat-a3', 'Plakat zum Aushang', 'A3 hoch, 297 × 420 mm', [seite(297, 420, 'dunkel', ganz('po_DbYnkdkjrNy', 210) + ab(16) + et('Fr 25. und Sa 26. September 2026 · 19 Uhr', 5, KERZEH) + ab(6)
                                                                       + tx('Drei Gänge von Rudi, fünf Drinks von Momo, eine lange Tafel.', 9.5, CREME, 220), fuss=ADR + ' · @culinarium_hannover')],
      [('plakat-a3', 44, '')], ['Das Plakat', 'an der Wand.'],
      'Rudis Plakat des Abends ganz, wie es auf Instagram stand, darunter Datum und ein Satz. Für den Eingang und die Wand mit den Plakaten.', 'Plakat vom September 2026')

    drinks = vorlage('menuekarte', 'menuekarte-2910-02')['inhalt']['liste']
    d('fuenf-drinks', 'Die fünf Drinks', 'DL hoch, 99 × 210 mm', [seite(99, 210, 'dunkel', zw(12, KERZE) + ab(5) + et('Momo', 2, KERZEH) + ab(3.4) + ti('Fünf Signature Drinks', 9.4, WEISS) + ab(4.4) + li(9, KERZE) + ab(9)
                                                                    + ''.join(ti(e(x['name']), 5.8, WEISS) + ab(1.4) + glieder(x['detail'], 3.0, CREME, 'text') + ab(7) for x in drinks), fuss='Walk on the Wild Side · ' + ADR)],
      [('fuenf-drinks', 40, '')], ['Fünf Drinks', 'von Momo.'],
      'Die Drinks eines Abends mit dem, was darin steckt. Hier die fünf vom April 2024.', 'Menükarte vom April 2024')

    d('rudis-zeilen', 'Rudis Zeilen', 'A5 hoch, 148 × 210 mm', [seite(148, 210, 'hell', zw(14, SCHIEFER) + ab(6) + et('Vom Pass', 2.4, KERZET) + ab(4) + ti('Was Rudi schreibt', 13, SCHIEFER) + ab(5) + li(10, KERZE) + ab(11)
                                                                    + ''.join(rz(z, 6.6, SCHIEFER) + ab(9) for z in TELLER), fuss='Walk on the Wild Side · ' + ADR)],
      [('rudis-zeilen', 44, '')], ['Rudis', 'Zeilen.'],
      'Rudi schreibt seine Teller in drei, vier Wörtern. Hier stehen sie, wie er sie schreibt, als Einleger zur Karte.', 'Startseite, «Teller von Rudi»')

    d('flyer', 'Flyer', 'A5 hoch, zwei Seiten', [bild_oben(148, 210, 'dunkel', 'anstossen', .5, et('Culinarium', 2.4, KERZEH) + ab(4) + ti('Food-Pairing an einer langen Tafel', 11, WEISS) + ab(5) + li(10, KERZE) + ab(5)
                                                         + tx('Drei Gänge aus Rudis Küche, zu jedem Gang ein Drink von Momo, persönlich erklärt.', 4.4, CREME, 110)),
                                                         seite(148, 210, 'hell', zw(14, SCHIEFER) + ab(6) + et('Die nächsten Abende', 2.4, KERZET) + ab(6)
                                                               + ti('27. und 28. November', 8.4, SCHIEFER) + ab(2) + et('Freitag 19 Uhr · Samstag 17 Uhr', 2.2, KERZET) + ab(8)
                                                               + ti('18. und 19. Dezember', 8.4, SCHIEFER) + ab(2) + et('Freitag 19 Uhr · Samstag 17 Uhr', 2.2, KERZET) + ab(9) + li(10, KERZE) + ab(8)
                                                               + tx('Tickets über die Website, die Warteliste über Instagram.', 4, TINTE, 100))],
      [('flyer', 44, 'Vorderseite'), ('flyer-r', 44, 'Rückseite')], ['Ein Flyer', 'für die Theke.'],
      'Vorne ein Foto vom Anstossen, hinten die nächsten Abende mit ihren Zeiten.', 'Website, Termine (Beispieltermine)')

    d('danke', 'Danke für den Abend', 'A6 hoch, zum Mitnehmen', [seite(105, 148, 'dunkel', zw(15, KERZE) + ab(6.5) + ti('Danke für den Abend.', 11.5, WEISS) + ab(5) + li(9, KERZE) + ab(5.5)
                                                                     + tx('Schön, dass du an der Tafel gesessen hast. Den nächsten Abend erfährst du zuerst auf Instagram.', 4.4, CREME, 80) + ab(7) + et('@culinarium_hannover', 1.9, KERZEH), fuss=ADR)],
      [('danke', 42, '')], ['Danke', 'für den Abend.'],
      'Liegt am Ende des Abends neben der Rechnung, zum Mitnehmen.', 'Eigener Satz')

    d('allergien', 'Allergien am Platz', 'A7 quer, 105 × 74 mm', [seite(105, 74, 'creme', et('Für Rudis Küche', 1.9, KERZET) + ab(2.6) + ti('Verträgst du etwas nicht?', 8.2, SCHIEFER) + ab(3) + li(8, KERZE) + ab(3)
                                                                    + tx('Sag es uns vorher, dann kocht Rudi deinen Teller danach.', 3.6, TINTE, 74), kopf='', fuss='')],
      [('allergien', 46, '')], ['Allergien', 'am Platz.'],
      'Eine kleine Karte für die Buchungsbestätigung oder den Tisch.', 'Eigener Satz')

    d('visitenkarte', 'Visitenkarte', '85 × 55 mm, zwei Seiten', [seite(85, 55, 'dunkel', wm(52, WEISS) + ab(2.6) + f'<div style="font:600 1.5mm/1 Urbanist,{IN};letter-spacing:.06em;color:{KERZEH}">{ZEILE}</div>', kopf='', fuss='', rahmen=False),
                                                                    seite(85, 55, 'hell', zw(7, SCHIEFER) + ab(3) + ti('Momo und Rudi', 6, SCHIEFER) + ab(2.4) + et('Walk on the Wild Side', 1.6, KERZET) + ab(1) + et(ADR, 1.6, KERZET) + ab(1) + et('@culinarium_hannover', 1.6, KERZET), kopf='', fuss='', rahmen=False)],
      [('visite', 46, 'Vorderseite'), ('visite-r', 46, 'Rückseite')], ['Eine Karte', 'zum Weitergeben.'],
      'Vorne Rudis Wortmarke mit der Zeile, hinten der Ort und Instagram.', 'Plakate und Website')

    dc = vorlage('menuekarte', 'menuekarte-2910-01')['inhalt']
    d('dc-karte', 'Dirty Chicken: die Karte', 'A5 hoch, 148 × 210 mm', [seite(148, 210, 'dc', dz(20) + ab(7) + et('Dirty Chicken', 2.4, WEISS) + ab(4) + ti(e(dc['titel']), 14, WEISS) + ab(3.4) + tx(dc['text'], 4.2, WEISS, 104) + ab(5) + li(10, WEISS) + ab(9)
                                                                           + ''.join(ti(e(x['name']), 7.2, WEISS) + ab(1.4) + tx(x['detail'], 3.6, WEISS) + ab(7) for x in dc['liste']),
                                                                           kopf='Pop-up im Walk on the Wild Side', fuss=ADR + ' · @dirtychicken.hannover')],
      [('dc-karte', 44, '')], ['Dirty Chicken:', 'die Karte.'],
      'Die Karte des Pop-ups in seinem Violett, mit dem D und seinen vier Posten.', 'Vorlagen Dirty Chicken')

    d('dc-flyer', 'Dirty Chicken: Flyer', 'A6 hoch, 105 × 148 mm', [bild_oben(105, 148, 'dc', 'dc_burger', .5, et('Pop-up', 2, WEISS) + ab(3) + ti('Dirty Food & Dirty Drinks', 9, WEISS) + ab(4) + li(9, WEISS) + ab(4)
                                                                         + tx('Sandwiches & More, Dirty Drinks und Live-Musik.', 3.9, WEISS, 80), fuss=ADR + ' · @dirtychicken.hannover')],
      [('dc-flyer', 42, '')], ['Dirty Chicken:', 'der Flyer.'],
      'Für die Theke an den Tagen des Pop-ups, vorne der Burger.', 'Website, Dirty Chicken')

    d('heute-abend', 'Heute Abend an der Theke', 'A6 hoch, als Aufsteller', [seite(105, 148, 'hell', zw(15, SCHIEFER) + ab(6.5) + et('Heute Abend', 2.1, KERZET) + ab(4) + ti('Culinarium an der langen Tafel', 10.5, SCHIEFER) + ab(5) + li(9, KERZE) + ab(5.5)
                                                                                   + tx('Die Bar ist für euch wie immer da: Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr.', 4.2, TINTE, 82))],
      [('heute-abend', 42, '')], ['Heute Abend', 'an der Theke.'],
      'Sagt den Gästen der Bar, dass hinten die Tafel gedeckt ist und vorne alles wie immer läuft.', 'Website, «Die Bar»')

    d('pressemappe', 'Pressemappe', 'A4 hoch, Deckblatt', [bild_oben(210, 297, 'dunkel', 'tafelleer', .52, et('Pressemappe', 3.4, KERZEH) + ab(6) + ti('Culinarium', 26, WEISS) + ab(8) + li(16, KERZE) + ab(8)
                                                               + tx('Food-Pairing-Abende im Walk on the Wild Side in Hannover-Linden, seit 2023.', 7, CREME, 150), fuss=ADR + ' · @culinarium_hannover')],
      [('presse', 44, '')], ['Ein Deckblatt', 'für die Presse.'],
      'Die gedeckte Tafel, darunter Name und ein Satz.', 'Website, «Geschichte»')

    d('termine', 'Die nächsten Abende', 'DL hoch, 99 × 210 mm', [seite(99, 210, 'creme', zw(12, SCHIEFER) + ab(5) + et('Culinarium', 2, KERZET) + ab(3.6) + ti('Die nächsten Abende', 9.4, SCHIEFER) + ab(4.4) + li(9, KERZE) + ab(10)
                                                                       + ''.join(et(t, 2.3, KERZET) + ab(1.8) + ti(n, 7.2, SCHIEFER) + ab(1.2) + tx(z, 3.5, TINTE) + ab(9.5)
                                                                                 for t, n, z in [('Freitag', '27. November', '19:00 Uhr'), ('Samstag', '28. November', '17:00 Uhr'), ('Freitag', '18. Dezember', '19:00 Uhr'), ('Samstag', '19. Dezember', '17:00 Uhr')]),
                                                                       fuss='Walk on the Wild Side · ' + ADR)],
      [('termine', 40, '')], ['Die nächsten', 'Abende.'],
      'Die Termine zum Mitnehmen. Hier mit den Beispielterminen der Website.', 'Website, Termine (Beispiele)')

    d('ablauf-team', 'Ablauf für das Team', 'A4 hoch, intern', [seite(210, 297, 'hell', zw(24, SCHIEFER) + ab(9) + et('Für das Team', 3.4, KERZET) + ab(6) + ti('Ablauf des Abends', 22, SCHIEFER) + ab(8) + li(16, KERZE) + ab(10)
                                                                    + zeit([('bis 18:00', 'Eindecken, Kerzen bereit'), ('18:45', 'Kerzen an'), ('19:00', 'Gäste kommen, der Aperitif'), ('19:15', 'Momo erklärt den ersten Drink'),
                                                                            ('19:30', 'Erster Gang'), ('20:30', 'Zweiter Gang'), ('21:30', 'Dessert'), ('22:30', 'Der Absacker')], 7, 'hell', 150), fuss=ADR)],
      [('ablauf', 44, '')], ['Der Ablauf', 'für das Team.'],
      'Hängt in der Küche und hinter der Bar: jede Uhrzeit mit ihrem Schritt.', 'Website, «Der Abend»; Zeiten als Beispiel')

    d('einladung', 'Einladung an Stammgäste', 'Quadrat 148 × 148 mm, zwei Seiten', [seite(148, 148, 'dunkel', zw(16, KERZE) + ab(6) + et('Für dich', 2.2, KERZEH) + ab(4) + ti('Ein Abend an der Tafel', 11.5, WEISS) + ab(5) + li(10, KERZE) + ab(5)
                                                                                           + ti('Freitag, 27. November · 19 Uhr', 5.2, WEISS), kopf='', fuss=''),
                                                                                     seite(148, 148, 'hell', tx('Wir halten einen Platz für dich frei, bevor der Abend für alle aufgeht. Sag uns bis Sonntag Bescheid, als Antwort auf Instagram.', 6, TINTE, 110)
                                                                                           + ab(8) + et('Momo, Derya und Rudi', 2.2, KERZET), kopf='Walk on the Wild Side', fuss=ADR)],
      [('einladung', 46, 'Vorderseite'), ('einladung-r', 46, 'Rückseite')], ['Eine Einladung', 'für Stammgäste.'],
      'Für die Gäste, die schon an der Tafel sassen: der Platz wird für sie zuerst freigehalten.', 'Eigener Satz, Beispieltermin')

    return NEU, SEITE


# ---------------------------------------------------------------- Beigaben: fünf Druckvorlagen
def beigaben(TELLER):
    B, SEITE = [], {}

    def d(ident, name, format_, blaetter, karton, titel, satz):
        namen = [n for n, _, _ in karton]
        B.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=[(n, i + 1) for i, n in enumerate(namen)], satz=satz, quelle='Eigene Idee'))
        SEITE[ident] = dict(karton=('', karton), titel=titel)

    # 1 Menü-Rolle mit Banderole: das Menü gerollt, eine Banderole mit dem C hält sie zusammen
    d('menuerolle', 'Menü-Rolle mit Banderole', 'Banderole 210 × 40 mm, Menü A5 quer zum Rollen',
      [seite(210, 40, 'dunkel', f'<div style="display:flex;align-items:center;gap:8mm">{zw(12, KERZE)}{ti("Dein Menü für heute Abend", 6.4, WEISS)}</div>', kopf='', fuss='', rahmen=False),
       seite(210, 148, 'hell', et('Menü', 2.6, KERZET) + ab(5) + ''.join(rz(z, 5.4, SCHIEFER) + ab(6) for z in TELLER), kopf='Culinarium', fuss='Walk on the Wild Side · ' + ADR)],
      [('rolle-band', 90, 'Banderole'), ('rolle-menue', 70, 'Menü zum Rollen')], ['Das Menü', 'als Rolle.'],
      'Das Menü liegt gerollt auf jedem Teller, eine Banderole mit dem C hält es zusammen. Der Gast öffnet es selbst.')
    # 2 Streichholzbriefchen
    d('streichholz', 'Streichholzbriefchen', 'Briefchen 50 × 110 mm (gefalzt 50 × 40)',
      [seite(50, 110, 'dunkel', zw(14, KERZE) + ab(5) + et('Culinarium', 1.7, KERZEH) + ab(16) + et('Für die Kerze an der Tafel', 1.6, CREME), kopf='', fuss='Haasemannstr. 13', rahmen=False)],
      [('streichholz', 30, '')], ['Streichhölzer', 'für die Kerzen.'],
      'Für die Kerzen an der Tafel, zum Mitnehmen nach dem Abend. Außen das C auf der Nacht.')
    # 3 Drink-Fähnchen
    fa = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;margin:0 3mm">{zw(7, KERZE)}{ab(2)}{ti(n, 4.2, WEISS)}</div>' for n, _ in TECHNIK_NAMEN)
    d('faehnchen', 'Drink-Fähnchen', 'Fähnchen 30 × 20 mm, gefalzt am Stäbchen',
      [seite(120, 30, 'dunkel', f'<div style="display:flex;justify-content:center">{fa}</div>', kopf='', fuss='', rahmen=False)],
      [('faehnchen', 80, '')], ['Ein Fähnchen', 'am Glas.'],
      'Am Stäbchen im Glas: welche Technik in diesem Drink steckt. Drei Fähnchen für Momos drei Techniken.')
    # 4 Postkarten: eigene Serie aller Plakate (postkarten.py, Robert 29.10.)
    # 5 Rezeptkarte eines Drinks
    d('rezept', 'Rezeptkarte eines Drinks', 'A6 quer, 148 × 105 mm',
      [seite(148, 105, 'creme', et('Momo zeigt', 2, KERZET) + ab(3) + ti('Fatwashing zu Hause', 9, SCHIEFER) + ab(4) + li(9, KERZE) + ab(5)
             + zeit([('1', 'Spirituose mit warmem Fett ansetzen'), ('2', 'Über Nacht kalt stellen'), ('3', 'Das feste Fett abheben'), ('4', 'Durch ein feines Tuch giessen')], 3.6, 'creme', 100), kopf='Culinarium', fuss='@culinarium_hannover')],
      [('rezept', 50, '')], ['Ein Rezept', 'zum Mitnehmen.'],
      'Die Technik eines Drinks in vier Schritten, zum Nachmachen zu Hause. Momo erklärt sie am Tisch.')

    # 6 Gutschein für einen Abend (Robert 29.10.: «Ein Gutschein für einen Abend können wir doch auch schon entwerfen»): DL quer, Rückseite, Umschlag
    vorn = blatt(210, 99, f'<i class="abs" style="inset:0;{TOENE["dunkel"]["grund"]}"></i>'
                 + f'<div class="abs" style="left:9mm;top:9mm;width:81mm;height:81mm;background:{WEISS};padding:2.4mm">{ganz("po_DbYnkdkjrNy", 76.2)}</div>'
                 + f'<div class="abs" style="left:98mm;top:0;width:104mm;height:99mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-bottom:4mm">'
                 + et('Gutschein', 2.6, KERZEH, .2) + ab(6)   # Wortmarke steht im Plakat links; kein C daneben (Stilblatt: C und Wortmarke nie auf einer Seite)
                 + ti('Ein Abend an der langen Tafel', 10, WEISS) + ab(4) + li(9, KERZE) + ab(4) + tx('Drei Gänge von Rudi, fünf Drinks von Momo.', 3.6, CREME, 90) + '</div>', '', f'background:{NACHT}')
    def feld(name, wert=''):
        return (f'<div style="display:flex;align-items:baseline;gap:3mm;width:100%;margin:2.6mm 0"><span style="flex:none;width:26mm;font:400 2mm/1 {MO};letter-spacing:.14em;text-transform:uppercase;color:{KERZET}">{e(name)}</span>'
                f'<span style="flex:1;border-bottom:.25mm solid rgba(38,36,45,.4);font:340 4.4mm/1.2 {FR};color:{SCHIEFER};padding-bottom:.6mm;min-height:5.6mm">{e(wert)}</span></div>')
    hinten = blatt(210, 99, f'<i class="abs" style="inset:0;background:{WEISS}"></i>'
                   + f'<div class="abs" style="left:14mm;top:12mm;width:112mm;bottom:12mm;display:flex;flex-direction:column;justify-content:center">'
                   + feld('Für') + feld('Von') + feld('Personen') + feld('Gültig bis', '[Datum]') + feld('Wert', '[Preis] je Person') + '</div>'
                   + f'<i class="abs" style="left:136mm;top:14mm;width:.25mm;height:71mm;background:{KERZE}"></i>'
                   + f'<div class="abs" style="left:142mm;top:0;width:58mm;height:99mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">'
                   + zw(11, SCHIEFER) + ab(4) + et('Nr. C-[0000]', 2.2, KERZET) + ab(6) + tx('Einzulösen für einen Abend nach Wahl. Den Termin vereinbart ihr über Instagram.', 3.1, TINTE, 52) + ab(4) + et('@culinarium_hannover', 1.8, KERZET)
                   + '</div>', '', f'background:{WEISS}')
    umschlag = blatt(220, 110, f'<i class="abs" style="inset:0;{TOENE["dunkel"]["grund"]}"></i>'
                     + f'<div class="abs" style="left:0;top:0;width:220mm;height:110mm;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-bottom:6mm">'
                     + zw(16, KERZE) + ab(6) + ti('Für dich', 10, WEISS) + ab(3.6) + li(9, KERZE) + ab(3.6) + et('Ein Abend an der langen Tafel', 2.3, KERZEH) + '</div>', '', f'background:{NACHT}')
    d('gutschein', 'Gutschein für einen Abend', 'DL quer, 210 × 99 mm, zwei Seiten, Umschlag DL',
      [vorn, hinten, umschlag], [('gs-vorn', 90, 'Vorderseite'), ('gs-hinten', 90, 'Rückseite'), ('gs-umschlag', 90, 'Umschlag')], ['Einen Abend', 'verschenken.'],
      'Vorne Rudis Plakat ganz mit seiner Wortmarke und «Ein Abend an der langen Tafel», hinten für wen, von wem, wie viele, gültig bis und die Nummer. Wert und Gültigkeit stehen in Klammern, bis das Haus sie festlegt. Dazu ein Umschlag auf der Nacht, auch als PDF zum Verschicken.')
    return B, SEITE


TECHNIK_NAMEN = [('Fatwashing', ''), ('Milkwashing', ''), ('Enzyme', '')]
