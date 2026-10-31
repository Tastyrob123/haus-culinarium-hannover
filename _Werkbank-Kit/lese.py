#!/usr/bin/env python3
"""Liest ein Original-PDF des Hauses zeilenweise aus (Text, Schnitt, Grösse, Ort): pdftohtml -xml → Zeilen je Seite.
python3 lese.py <pfad.pdf> [seite …]   druckt die Zeilen zum Ansehen. Als Modul: seiten(name) → [[Zeile]]"""
import os, re, subprocess, sys, tempfile
import xml.etree.ElementTree as ET



# Unterlagen, deren Schriften keine Fett-/Kursiv-Marke tragen: Schriftname → (fett, kursiv)
SCHNITT = {}
WEISS_ZEIGEN = set()   # Dateien, in denen weisse Schrift auf einem Foto steht und deshalb zum Wortlaut gehört


def roh(name):
    with tempfile.TemporaryDirectory() as t:
        z = os.path.join(t, 'x')
        subprocess.run(['pdftohtml', '-xml', '-i', '-q', '-hidden', name, z], check=True)
        s = open(z + '.xml', encoding='utf-8', errors='replace').read()
    s = re.sub(r'<a [^>]*>|</a>', '', s)
    return s


def seiten(name, spalt=9, ytol=4):
    """→ je Seite: (breite, hoehe, [zeile]); zeile = dict(y, zellen=[dict(x, x2, t, b, i, g)])"""
    s = roh(name)
    gr = {m.group(1): int(m.group(2)) for m in re.finditer(r'<fontspec id="(\d+)" size="(\d+)"', s)}
    fam = {m.group(1): m.group(2) for m in re.finditer(r'<fontspec id="(\d+)" size="\d+" family="([^"]*)"', s)}
    schnitt = SCHNITT.get(name, {})
    weiss = {m.group(1) for m in re.finditer(r'<fontspec id="(\d+)"[^>]*color="#ffffff"', s)}   # weisse Schrift ist im Original unsichtbar
    aus = []
    for pm in re.finditer(r'<page number="(\d+)"[^>]*height="(\d+)" width="(\d+)">(.*?)</page>', s, re.S):
        H, W = int(pm.group(2)), int(pm.group(3))
        st = []
        for m in re.finditer(r'<text top="(-?\d+)" left="(-?\d+)" width="(\d+)" height="(\d+)" font="(\d+)">(.*?)</text>', pm.group(4), re.S):
            y, x, w, h, f, inn = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5), m.group(6)
            if f in weiss and name not in WEISS_ZEIGEN:
                continue
            b, i = '<b>' in inn, '<i>' in inn
            if fam.get(f) in schnitt:
                b, i = schnitt[fam[f]]
            t = re.sub(r'<[^>]+>', '', inn)
            t = t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#34;', '"').replace('&#39;', "'").replace('\xa0', ' ')
            if not t.strip():
                continue
            # ein Stück mit langer Leerstrecke (Name … Preis) wird an der Lücke geteilt, der Ort anteilig geschätzt
            stuecke = [(mm.start(), mm.group()) for mm in re.finditer(r'\S(?:.*?\S)?(?=\s{4,}|\s*$)', t)]
            if len(stuecke) < 2:
                stuecke = [(0, t)]
            L = max(len(t.rstrip()), 1)
            for k, (a0, tt) in enumerate(stuecke):
                xa = x + round(w * a0 / max(len(t), 1)) if k else x
                xb = x + round(w * min(a0 + len(tt), L) / max(len(t), 1))
                st.append(dict(y=y + h, x=xa, x2=max(xb, xa + 1), t=tt, b=b, i=i, g=gr.get(f, 0), h=h, teil=k))  # y = Unterkante
        st.sort(key=lambda a: (a['y'], a['x']))
        zeilen = []
        for a in st:
            for z in reversed(zeilen[-6:]):
                if abs(z['y'] - a['y']) <= ytol:
                    z['st'].append(a)
                    break
            else:
                zeilen.append(dict(y=a['y'], st=[a]))
        for z in zeilen:
            z['st'].sort(key=lambda a: a['x'])
            zellen = []
            for a in z['st']:
                if zellen and a['x'] - zellen[-1]['x2'] <= spalt:
                    c = zellen[-1]
                    if a['x'] - c['x2'] >= 3 and not c['teile'][-1]['t'].endswith(' ') and not a['t'].startswith(' '):
                        a = dict(a, t=' ' + a['t'])     # sichtbare Lücke ohne Leerzeichen im PDF
                    c['teile'].append(a)
                    c['x2'] = max(c['x2'], a['x2'])
                else:
                    zellen.append(dict(x=a['x'], x2=a['x2'], y=a['y'], teile=[a]))
            for c in zellen:
                t0 = c['teile'][0]['t']
                vor = len(t0) - len(t0.lstrip())
                if vor >= 2 and t0.strip() and not c['teile'][0].get('teil'):   # Einzug aus Leerzeichen: der Text beginnt weiter rechts
                    q = c['teile'][0]
                    c['x'] = q['x'] + round((q['x2'] - q['x']) * vor * 0.55 / (vor * 0.55 + len(t0) - vor))   # Leerzeichen sind schmaler als Buchstaben
                c['t'] = re.sub(r'\s+', ' ', ' '.join(p['t'] for p in c['teile'])).strip() if any(p.get('teil') for p in c['teile']) else re.sub(r'\s+', ' ', ''.join(p['t'] for p in c['teile'])).strip()
                c['b'] = all(p['b'] for p in c['teile'] if p['t'].strip())
                c['i'] = all(p['i'] for p in c['teile'] if p['t'].strip())
                echt = [p for p in c['teile'] if re.sub('[\uf000-\uf8ff\\s]', '', p['t'])] or c['teile']
                c['g'] = max(p['g'] for p in echt)   # Zeichen aus Symbolschriften (Kästchen) bestimmen die Grösse nicht
            z['zellen'] = zellen
            del z['st']
        zeilen.sort(key=lambda z: z['y'])
        aus.append((W, H, zeilen))
    return aus


if __name__ == '__main__':
    name = sys.argv[1]
    nur = [int(a) for a in sys.argv[2:]]
    for n, (W, H, zz) in enumerate(seiten(name), 1):
        if nur and n not in nur:
            continue
        print(f'===== Seite {n}  ({W}×{H})')
        for z in zz:
            print(f"{z['y']:5d} | " + ' ‖ '.join(f"{c['x']}:{'B' if c['b'] else ''}{'I' if c['i'] else ''}{c['g']} {c['t']}" for c in z['zellen']))
