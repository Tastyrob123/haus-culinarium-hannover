#!/usr/bin/env python3
"""Werkbank Culinarium: kein Einzelwort allein in der letzten Titelzeile (Roberts Kriterium 7, Abnahme-Tor 30.10.2026: «Was alles geprüft / wurde.»,
«Auf die / Warteliste.», «Was ihr / bekommt.», «Der Chat für eure / Gäste» …), dazu die Aufschrift im Fensterstapel der Startseite frei (K2/K5: sie lag
unter dem Abzug links oben, zu sehen war nur «…artseite»).
- Titel mit festen Zeilen (.zt > .z): steht in der letzten Zeile nur ein Wort, werden kurze Titel (bis 20 Zeichen) zu einer Zeile,
  bei längeren wandert das letzte Wort der Zeile davor mit («Einen / Abend verschenken.» passt so auch am Handy).
- Alle Titel h1–h4: die letzten zwei Wörter fest verbunden (geschütztes Leerzeichen), dazu text-wrap: balance.
- Feed: «Wie es weitergeht.» auf einer Zeile, Grösse nach der Breite der Spalte.
Läuft in haus.nach_bau vor text_mitte über alle Seiten der Werkbank, wiederholbar.   python3 _werkbank/zeile_ganz.py [<website/_werkbank>]"""
import glob, os, re, sys

CSS = ('h1,h2,h3,h4,.z>span{text-wrap:balance}h1 br+em,h2 br+em{display:inline-block;text-wrap:balance}'
       '.stapel .fen__k{position:relative}.stapel .fen__k span{position:absolute;left:50%;transform:translateX(-50%);margin:0;overflow:visible}'
       '@media(max-width:860px){.stapel .fen__k span{display:none}}'
       '@media(max-width:480px){.etk{grid-template-columns:minmax(0,1fr)!important}}'   # Untersetzer, Postkarten, Sticker am Handy einspaltig: Namen mit Datum stehen ganz (Tor 30.10.)
       '@media(min-width:900px) and (max-width:1279px){.brett-p{grid-template-columns:300px minmax(0,1fr)}.brett-p__k{grid-column:1/-1}}@media(max-width:1279px){.brett-p p{text-wrap:balance}}'   # Leitlinie bei 1000: Knöpfe in eigene Reihe, der Satz bekommt die Breite (Tor 30.10.)
       '.da:not([data-drift]){will-change:auto!important}'   # nach dem Auftritt keine eigene Ebene mehr (Speicher in WebKit, Tor 4)
    '.mb-ueber__t small{display:grid;grid-template-columns:64px minmax(0,1fr);align-items:baseline}.mb-ueber__t small span{min-width:0}'   # Mail-Karten: Wert von Wann/Betreff hängt unter sich, nie unter dem Etikett (Tor 30.10.)
       '@media(max-width:480px){.mn-titel{font-size:clamp(1.5rem,8vw,2.2rem);letter-spacing:.03em}.mn-ende{gap:10px}.mn-ende i{width:18px}.mn-ende span{letter-spacing:.12em;white-space:nowrap}a.kn[href="../index.html#geprueft"]{letter-spacing:.04em;font-size:9.5px;white-space:nowrap;padding-left:14px}.stapel .tel{width:21%;right:-2%}}'
    '@media(max-width:480px){.wege__t,figcaption,.mb-ueber__t small{text-wrap:balance}.sag-h{font-size:1.32rem;letter-spacing:.03em;gap:10px}.hs2-her{grid-template-columns:repeat(2,minmax(0,1fr))!important}.hs2-her figcaption small{font-size:9px;letter-spacing:0}.ki-knoepfe{flex-direction:column;align-items:stretch}.ki-knoepfe .kn{white-space:nowrap;letter-spacing:.04em;font-size:10px}#sag-aufbau[data-a=\"heben\"]:not(.da){transform:translateY(56px) scale(.98)!important}.faecher--2 .blattk span{flex-direction:column;gap:3px;font-size:9.5px;letter-spacing:.08em}}'
       '.stage>.aside h1{font-size:clamp(2rem,3.6vw,3.3rem);white-space:nowrap}.stage>.aside h1 em{display:inline}')   # ohne container-type: die Spalte misst sich am Inhalt (Tor 30.10.)
BLOCK = '<style id="zeile-ganz">' + CSS + '</style>'
TITEL = re.compile(r'(<(h[1-6]) class="[^"]*\bzt\b[^"]*">)(.*?)(</\2>)', re.S)
ZEILE = re.compile(r'<span class="z"><span>(.*?)</span></span>', re.S)


def woerter(h):
    return re.sub(r'<[^>]+>', ' ', h).split()


def titel(m):
    zeilen = ZEILE.findall(m.group(3))
    if len(zeilen) < 2 or ''.join(f'<span class="z"><span>{z}</span></span>' for z in zeilen) != m.group(3) or len(woerter(zeilen[-1])) != 1:
        return m.group(0)
    davor = zeilen[-2]
    kurz = len(' '.join(woerter(davor + ' ' + zeilen[-1]))) <= 20   # passt auch am Handy (t2 32 px auf 350 px) auf eine Zeile
    if not kurz and len(woerter(davor)) >= 2 and '<' not in davor:
        rest, wort = davor.rsplit(' ', 1)
        zeilen[-2:] = [rest, wort + ' ' + zeilen[-1]]
    else:
        zeilen[-2:] = [davor + ' ' + zeilen[-1]]
    return m.group(1) + ''.join(f'<span class="z"><span>{z}</span></span>' for z in zeilen) + m.group(4)


H = re.compile(r'(<(h[1-4])\b[^>]*>)(.*?)(</\2>)', re.S)
# Weitere Zeilen mit Wort allein unten (Tor 30.10., 390 px): Fusszeilen-Titel, KI-Zahlen, Bildzeilen, Kopfzeilen der Mail-Karten
MEHR = re.compile(r'(<(b) class="wege__t">|<(p) class="ki-zahl__t">|<(figcaption)\b[^>]*>|<(small)>)(.*?)(</(?:\2|\3|\4|\5)>)', re.S)


def kleben(m):
    """Die letzten zwei Wörter eines Titels fest verbinden (geschütztes Leerzeichen im Text, nie in einem Tag): so steht nie ein Wort allein unten."""
    innen = m.group(3)
    if len(woerter(innen)) < 2 or re.search('\u00a0[^\\s\u00a0]+\\s*$', re.sub(r'<[^>]+>', '', innen)):   # schon geklebt: wiederholbar, nie ein zweites Mal
        return m.group(0)
    if ' / ' in re.sub(r'<[^>]+>', '', innen).replace('\u00a0', ' '):
        return m.group(0)   # Rudis Zeilen mit «/»: kleben schöbe den Trenner an den Zeilenrand
    teile = re.split(r'(<[^>]+>)', innen)
    for i in range(len(teile) - 1, -1, -1):
        s = teile[i]
        if s.startswith('<'):
            if s.lower().startswith('<br'):
                return m.group(0)   # Umbruch steht vor dem letzten Wort: nichts zu kleben
            continue
        k = s.rstrip()
        j = k.rfind(' ')
        if j > 0 and k[:j].strip():
            teile[i] = s[:j] + '\u00a0' + s[j + 1:]
            return m.group(1) + ''.join(teile) + m.group(4)
        if k.strip():   # ein Wort in diesem Textstück: der Abstand davor liegt weiter vorn
            if j == 0 or (i > 0 and s[:1] == ' '):
                teile[i] = '\u00a0' + s.lstrip()
                return m.group(1) + ''.join(teile) + m.group(4)
            for h in range(i - 1, -1, -1):
                if teile[h].startswith('<'):
                    if teile[h].lower().startswith('<br'):
                        return m.group(0)
                    continue
                if teile[h].endswith(' '):
                    teile[h] = teile[h][:-1] + '\u00a0'
                    return m.group(1) + ''.join(teile) + m.group(4)
                return m.group(0)
            return m.group(0)
    return m.group(0)


class _M:
    def __init__(self, a, b, c): self.g = (None, a, None, b, c)
    def group(self, i): return ''.join(x for x in self.g if x) if i == 0 else self.g[i]


def kleben_mehr(m):
    tag = next(t for t in m.groups()[1:5] if t)
    if not m.group(7).startswith('</' + tag):
        return m.group(0)
    return kleben(_M(m.group(1), m.group(6), m.group(7)))


def mail_kopf(s, i):
    """<small> nur in den Kopfzeilen der Mail-Karten (Von, Wann, Betreff)."""
    a = s.rfind('<span class="mb-ueber__t">', 0, i)
    return a >= 0 and '</header>' not in s[a:i]


MASS = re.compile(r'(\d+(?:[.,]\d+)?)(?:\s|&nbsp;|\u00a0)*×(?:\s|&nbsp;|\u00a0)*(\d+(?:[.,]\d+)?)')


def zahl(t):
    """63.329918… mm aus dem Seitenverhältnis gerundet, ganze Zahlen bleiben."""
    return t if re.fullmatch(r'\d+', t) else str(round(float(t.replace(',', '.'))))


def anwenden(root):
    n = 0
    for f in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
        rel = os.path.relpath(f, root)
        if rel.startswith(('_werkbank', '_sicherung', 'node_modules')) or '.vor-' in rel:
            continue
        s = open(f, encoding='utf-8').read()
        if '</head>' not in s:
            continue
        neu = TITEL.sub(titel, re.sub(r'<style id="zeile-ganz">.*?</style>', '', s, flags=re.S))
        neu = H.sub(kleben, neu)
        neu = re.sub(r'(<span class="mb-ueber__t">.*?</header>)', lambda m: re.sub(r'(<small><span>[^<]*</span>)\s+', r'\1', m.group(1)), neu, flags=re.S)   # Werte ohne Leerzeichen davor: alle beginnen auf derselben Kante (Tor 30.10.)
        neu = MEHR.sub(lambda m: kleben_mehr(m) if m.group(5) is None or mail_kopf(neu, m.start()) else m.group(0), neu)
        if not rel.startswith('feed'):   # Robert: kein «×» auf der ganzen Seite, auch nicht als Masszeichen (Tor 4, 30.10.); Feed gehört der Imprimerie
            neu = MASS.sub(lambda m: f'{zahl(m.group(1))} auf {zahl(m.group(2))}', neu)
        neu = neu.replace('gelesen am 28. Oktober 2026:', 'gelesen am 28.\u00a0Oktober\u00a02026:')   # Tor 4: «2026:» nie allein
        neu = neu.replace('</head>', BLOCK + '</head>', 1)
        if neu != s:
            open(f, 'w', encoding='utf-8').write(neu); n += 1
    return n


if __name__ == '__main__':
    print('zeile-ganz:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Seiten')
