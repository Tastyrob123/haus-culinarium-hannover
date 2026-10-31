#!/usr/bin/env python3
"""Unterlagen aus dem Original-PDF heraus neu setzen: liest jede Zeile mit Ort, Grösse und Schnitt (lese.py) und macht daraus
die Bausteine aus satz_kern (Rubrik, Posten mit Preis, Absatz). Der Wortlaut bleibt, weil jede gelesene Zelle wieder gesetzt wird;
satz_pruefe.py vergleicht am Ende trotzdem Wort für Wort.

Gebrauch in <Projekt>/_werkbank/satz_daten.py:
    A = satz_auto.Dok('<pfad zum original.pdf>', rubrik=27, posten=20)      # ab welcher Schriftgrösse fett = Rubrik bzw. Gericht
    A.fluss(seite, x0, x1, y0, y1)        → HTML der Karte in diesem Ausschnitt (Rubriken, Gerichte, Preise)
    A.text(seite, x0, x1, y0, y1)         → Fliesstext in Absätzen, fette Zeilen als Zwischentitel
    A.zeilen(seite, x0, x1, y0, y1)       → die rohen Zeilen, falls ein Ausschnitt von Hand gebaut wird
Koordinaten sind die des Originals (python3 lese.py <pdf> <seite> zeigt sie)."""
import html, re
import lese
import satz_kern as S

e = html.escape
PREIS = re.compile(r'^(?:CHF\s*)?\d{1,4}[.,]\d{2}\.?$|^\d{1,4}\.[–—-]+$')
ODER = re.compile(r'^(?:oder|ou|or)(?:\s*/\s*(?:oder|ou|or))*$', re.I)


def _klein(t):
    return bool(re.match(r'^(kleine|chlini|chline|petite|small)\b', t, re.I))


def _gross(t):
    w = re.sub(r'[^A-Za-zÄÖÜäöüÉÈÊÀÂÎÔÛÇŒéèêàâîôûçœ]', '', t.split(' ')[0])
    return len(w) >= 3 and w.isupper()


class Dok:
    def __init__(self, pfad, rubrik=27, posten=20, preis_min=None, fremd=None, schnitt=None, ytol=4, locker=False, weiss=False, umschrift=None, kopfgroesse=0, mehrzellig=False, rubrik_mager=False):
        """rubrik/posten: Schriftgrösse (Einheiten des Originals), ab der eine fette Zeile Rubrik bzw. Gericht ist.
        fremd(zeile_text, zelle) → True, wenn die Zeile eine Übersetzung ist (wird kursiv und heller gesetzt)."""
        if schnitt:
            lese.SCHNITT[pfad] = schnitt
        if weiss:
            lese.WEISS_ZEIGEN.add(pfad)
        self.pfad, self.R, self.N = pfad, rubrik, posten
        self.seiten = lese.seiten(pfad, ytol=ytol)
        self.locker = locker
        self.um = umschrift or {}
        self.mehrzellig, self.rubrik_mager = mehrzellig, rubrik_mager
        self.kopfgroesse = kopfgroesse      # Zeilen bis zu dieser Schriftgrösse über einem Gericht sind Spaltenköpfe seiner Preise (KLEIN, MEDIUM)
        self.fremd = fremd or (lambda t, c: c['i'] or _gross(t))
        self.benutzt = set()

    def lies_wort(self, t):
        """Gesperrt gesetzte Wörter («S U P P E N») zusammenziehen; Mehrwort-Titel stehen in umschrift."""
        teile = t.split(' ')
        if len(teile) >= 3 and all(len(x) == 1 for x in teile):
            j = ''.join(teile)
            return self.um.get(j, j[0] + j[1:].lower())
        return self.um.get(t, t)

    def zeilen(self, seite, x0=0, x1=1e9, y0=0, y1=1e9):
        W, H, zz = self.seiten[seite - 1]
        aus = []
        for z in zz:
            if not (y0 <= z['y'] < y1):
                continue
            cc = []
            for c in z['zellen']:
                if not (x0 <= c['x'] < x1 and c['t'].strip()):
                    continue
                self.benutzt.add((seite, z['y'], c['x']))
                t = self.lies_wort(c['t'].strip())
                c = dict(c, t=t)
                if re.match(r'^\d{1,4}\.\d{2}(\s+\d{1,4}\.\d{2})+$', t):        # «14.00 16.00» in einer Zelle
                    cc += [dict(c, t=p) for p in t.split()]
                elif re.match(r'^.*[A-Za-zäöüé]\d{1,3}\.\d{2}$', t):                 # «… cream7.50»: Preis klebt am Wort
                    m = re.match(r'^(.*[A-Za-zäöüé])(\d{1,3}\.\d{2})$', t)
                    cc += [dict(c, t=m.group(1)), dict(c, t=m.group(2), x=c['x2'])]
                elif len(t) < 46 and '/' not in t and not t.startswith('CHF') and re.match(r'^.+[^\d\s.]\s+\d{1,3}\.\d{2}$', t):       # «vegetarisch 32.00»
                    m = re.match(r'^(.+?)\s+(\d{1,3}\.\d{2})$', t)
                    cc += [dict(c, t=m.group(1)), dict(c, t=m.group(2), x=c['x2'])]
                else:
                    cc.append(c)
            if cc:
                aus.append(dict(y=z['y'], zellen=cc))
        return aus

    def unbenutzt(self):
        """Zellen, die in keinem Ausschnitt lagen (zur Kontrolle beim Einrichten)."""
        aus = []
        for n, (W, H, zz) in enumerate(self.seiten, 1):
            for z in zz:
                for c in z['zellen']:
                    if c['t'].strip() and (n, z['y'], c['x']) not in self.benutzt:
                        aus.append((n, z['y'], c['x'], c['t'][:50]))
        return aus

    # ------------------------------------------------------------ Karte
    def fluss(self, seite, x0=0, x1=1e9, y0=0, y1=1e9, rubrik=None, posten=None, kopf_als_titel=False, spaltenkopf=None):
        R, N = rubrik or self.R, posten or self.N
        o, akt = [], None

        def schliess():
            nonlocal akt
            if akt:
                o.append(self._posten(akt))
                akt = None
        wartet = None
        for z in self.zeilen(seite, x0, x1, y0, y1):
            cc = z['zellen']
            erste = cc[0]
            if self.kopfgroesse and all(c['g'] <= self.kopfgroesse for c in cc) and all(len(c['t']) <= 14 for c in cc):
                schliess(); wartet = [c['t'] for c in cc]; continue
            preise = [c['t'] for c in cc[1:] if PREIS.match(c['t'])] if len(cc) > 1 else []
            rest = [c for c in cc[1:] if not PREIS.match(c['t'])]
            if len(cc) == 1 and PREIS.match(erste['t']) and akt is not None:   # Preis steht allein in der Zeile
                akt['preise'].append(erste['t']); continue
            if all(PREIS.match(c['t']) for c in cc) and akt is not None:
                akt['preise'] += [c['t'] for c in cc]; continue
            if re.match(r'^[*\s]+$', ' '.join(c['t'] for c in cc)):
                if akt is not None and self.locker:
                    schliess()
                    o.append(f'<p class="stern">{e(" ".join(c["t"] for c in cc))}</p>')
                elif akt is not None:
                    akt['zeilen'].append((' '.join(c['t'] for c in cc), False, False, []))
                else:
                    o.append(f'<p class="stern">{e(" ".join(c["t"] for c in cc))}</p>')
                continue
            if (erste['b'] or (self.rubrik_mager and len(cc) == 1)) and erste['g'] >= R:
                schliess()
                kopf = [c['t'] for c in rest if len(c['t']) <= 14 and c['g'] < R and c['x'] > x0 + (min(x1, self.seiten[seite - 1][0]) - x0) * .55] if spaltenkopf else []
                zus = ' '.join(c['t'] for c in rest if c['t'] not in kopf)
                o.append(S.rubrik(e(erste['t']), e(zus), kopf) if not preise else S.rubrik(e(erste['t']), e(zus)).replace('</h2>', '<span class="rp">' + ' '.join(e(p) for p in preise) + '</span></h2>'))
            elif (akt is not None and akt['name'] and not akt['zeilen'] and erste['b'] and erste['g'] >= N and len(cc) == 1 and not PREIS.match(erste['t'])
                  and z['y'] - akt['y'] <= erste['g'] * 1.36):
                akt['name'] += ' ' + erste['t']; akt['y'] = z['y']      # der Name des Gerichts läuft im Original über zwei Zeilen
            elif erste['g'] >= N and (erste['b'] or (preise and not _klein(erste['t'])) or (self.locker and akt is None) or (self.mehrzellig and len(cc) >= 2)) and not PREIS.match(erste['t']):
                schliess()
                akt = dict(name=erste['t'], zusatz=' '.join(c['t'] for c in rest), preise=preise, zeilen=[], kopf=wartet, y=z['y'])
                wartet = None
            elif ODER.match(' '.join(c['t'] for c in cc)):
                schliess()
                o.append(f'<p class="oder">{e(" ".join(c["t"] for c in cc))}</p>')
            else:
                t = ' '.join(c['t'] for c in cc if not PREIS.match(c['t']))
                if akt is None:
                    akt = dict(name='', zusatz='', preise=[], zeilen=[], y=z['y'])
                zp = [c['t'] for c in cc if PREIS.match(c['t'])]
                if t:
                    vor = akt['zeilen'][-1][1] if akt['zeilen'] else False
                    fr = self.fremd(t, erste) or (vor and t[:1].islower())
                    akt['zeilen'].append((t, fr, erste['b'], zp))
                else:
                    akt['preise'] += zp
        schliess()
        return ''.join(o)

    def _posten(self, a):
        zl = ''
        for t, fr, b, zp in a['zeilen']:
            kl = 'fr' if fr and not zp else ''
            pr = ''.join(f'<b>{e(p)}</b>' for p in zp)
            if re.match(r'^[*\s]+$', t):
                zl += f'<p class="stern">{e(t)}</p>'; continue
            fett = b and not fr
            zl += f'<p class="{kl}{" mp" if zp else ""}{" halb" if fett else ""}"><span>{e(t)}</span>{pr}</p>'
        kopf = a.get('kopf') or []
        if kopf and len(kopf) == len(a['preise']):
            pr = ''.join(f'<span class="pz pz--k"><em>{e(k)}</em><b>{e(p)}</b></span>' for k, p in zip(kopf, a['preise']))
        else:
            pr = ''.join(f'<span class="pz"><em>{e(k)}</em></span>' for k in kopf) if kopf and not a['preise'] else ''
            pr += ''.join(f'<span class="pz"><b>{e(p)}</b></span>' for p in a['preise'])
        z = f' <small>{e(a["zusatz"])}</small>' if a['zusatz'] else ''
        kopf = f'<h4>{e(a["name"])}{z}</h4>' if a['name'] else ''
        return f'<div class="po{" po--frei" if not a["name"] else ""}"><div class="po__t">{kopf}{zl}</div><div class="po__p{" po__p--reihe" if len(a["preise"]) > 1 else ""}">{pr}</div></div>'

    # ------------------------------------------------------------ Fliesstext
    def text(self, seite, x0=0, x1=1e9, y0=0, y1=1e9, titel=None, kl='', luecke=1.45, mitte=False, trenn=False):
        """Zeilen zu Absätzen fügen. Neuer Absatz bei grösserem Zeilenabstand oder wenn eine fette Zeile beginnt/endet.
        titel: Schriftgrösse, ab der eine fette Zeile als Zwischentitel gesetzt wird."""
        zz = self.zeilen(seite, x0, x1, y0, y1)
        if not zz:
            return ''
        abst = sorted(b['y'] - a['y'] for a, b in zip(zz, zz[1:]) if b['y'] > a['y'])
        norm = abst[len(abst) // 3] if abst else 20
        o, puffer, fett_vor, y_vor = [], [], None, None

        def schliess():
            nonlocal puffer
            if puffer:
                t = ' '.join(puffer)
                if trenn:   # Silbentrennung des Originals am Zeilenende auflösen («mittle- rem» → «mittlerem»)
                    t = re.sub(r'([a-zäöüß])- ([a-zäöüß])', r'\1\2', t)
                o.append((t, fett_vor))
                puffer = []
        for z in zz:
            t = ' '.join(c['t'] for c in z['zellen'])
            fett = all(c['b'] for c in z['zellen'])
            gross = max(c['g'] for c in z['zellen'])
            if titel and fett and gross >= titel:
                schliess(); o.append((t, 'titel')); fett_vor, y_vor = None, z['y']; continue
            if y_vor is not None and (z['y'] - y_vor > norm * luecke or fett != fett_vor):
                schliess()
            puffer.append(t); fett_vor, y_vor = fett, z['y']
        schliess()
        aus = ''
        for t, art in o:
            if art == 'titel':
                aus += S.titel(e(t), 'klein' + (' mitte' if mitte else ''))
            else:
                aus += S.absatz(('<b>' if art else '') + e(t) + ('</b>' if art else ''), kl + (' mitte' if mitte else ''))
        return aus

    def raster(self, seite, grenzen, y0=0, y1=1e9, kopf=1):
        """Eine Tabelle: Zellen nach x-Grenzen in Spalten, Zeile für Zeile. Die ersten «kopf» Zeilen sind Spaltenköpfe."""
        o, n = '', 0
        for z in self.zeilen(seite, grenzen[0], grenzen[-1], y0, y1):
            sp = ['' for _ in grenzen[:-1]]
            for c in z['zellen']:
                for i in range(len(grenzen) - 1):
                    if grenzen[i] <= c['x'] < grenzen[i + 1]:
                        sp[i] = (sp[i] + ' ' + c['t']).strip()
            kl = 'kopf' if n < kopf else ''
            o += f'<div class="rz {kl}">' + ''.join(f'<span class="{"fr" if i and not kl else ""}">{e(t)}</span>' for i, t in enumerate(sp)) + '</div>'
            n += 1
        return f'<div class="uraster" style="--n:{len(grenzen) - 1}">{o}</div>'

    def roh(self, seite, x0=0, x1=1e9, y0=0, y1=1e9, trenner='<br>'):
        return trenner.join(e(' '.join(c['t'] for c in z['zellen'])) for z in self.zeilen(seite, x0, x1, y0, y1))

    # ------------------------------------------------------------ Spalten einer Tabelle (Wochenmenü)
    def spalte(self, seite, x0, x1, y0=0, y1=1e9, gross=17, kopf=1):
        """Eine Spalte als Liste: Zeilen ab Grösse «gross» sind Gerichte, kleinere Übersetzungen, Sternchen trennen die Gänge."""
        o, n = '', 0
        for z in self.zeilen(seite, x0, x1, y0, y1):
            t = ' '.join(c['t'] for c in z['zellen']); g = max(c['g'] for c in z['zellen'])
            if re.match(r'^\*+$', t.replace(' ', '')):
                o += f'<p class="stern">{e(t)}</p>'
            elif n < kopf and g >= gross:
                o += f'<h4 class="tag">{e(t)}</h4>'; n += 1
            elif g >= gross:
                o += f'<p class="gang">{e(t)}</p>'
            else:
                o += f'<p class="fr">{e(t)}</p>'
        return f'<div class="tmsp">{o}</div>'
