#!/usr/bin/env python3
"""Kein Einzelwort allein in der letzten Titelzeile (Kriterium 7, Abnahme-Tor 30.10.2026).
Läuft am Ende von bau_en.py über die fertigen Seiten (de und en): in jeder Überschrift h1–h3 und jedem dt wird das letzte Leerzeichen
zwischen zwei Wörtern zu &nbsp;, damit die letzten zwei Wörter nie getrennt umbrechen. Text und Aussehen bleiben sonst gleich;
dazu culinarium.css «text-wrap-style: pretty». Ausgenommen: der senkrechte Titel (.pp15-senk, eine gedrehte Zeile)."""
import os, re

HIER = os.path.dirname(os.path.abspath(__file__))
SEITEN = ['index', 'abend', 'abende', 'bar', 'leute', 'weg', 'dirty-chicken', 'impressum', 'datenschutz', 'termine-pflege']
NBSP = ' '


def schuetzen(inner, aw=False, lang=False):
    # Textzeichen samt Lage im HTML sammeln (Tags überspringen), dann das letzte Leerzeichen mit Text davor und danach ersetzen
    teile, pos = [], 0
    for m in re.finditer(r'<[^>]*>', inner):
        teile.append((pos, inner[pos:m.start()])); pos = m.end()
    teile.append((pos, inner[pos:]))
    zeichen = [(p + i, c) for p, t in teile for i, c in enumerate(t)]
    for k in range(len(zeichen) - 2, 0, -1):
        if zeichen[k][1] == ' ' and not zeichen[k - 1][1].isspace() and not zeichen[k + 1][1].isspace() and zeichen[k + 1][1] != '&':
            # nur kurze Paare (Abnahme-Tor 30.10.2026): ein langes Paar wie «deinem Geschmack.» passt in schmalen Spalten nicht mehr in eine Zeile und wird abgeschnitten
            text = ''.join(c for _, c in zeichen)
            vor = text[:k].rstrip().split()[-1] if text[:k].strip() else ''
            nach = text[k + 1:].split()[0] if text[k + 1:].strip() else ''
            if len(vor) + 1 + len(nach) > (18 if lang else 16 if aw else 12):   # Begriffe der Liste «Ungefähr so» (.aw-liste dt): bis 16 Zeichen, Schrift dort am Handy 17 px (Oberchef 30.10.2026)
                return inner
            p = zeichen[k][0]
            return inner[:p] + NBSP + inner[p + 1:]
        if zeichen[k][1] == NBSP:
            return inner
    return inner


def seite(pfad):
    h = open(pfad, encoding='utf-8').read()
    n = [0]
    def eins(m, h=h):
        tag, auf, inner = m.group(1), m.group(2), m.group(3)
        if 'pp15-senk' in auf:
            return m.group(0)
        if 'ad-titel' in auf:
            # Titel der Ansicht «Mehr zum Abend» (Tor 30.10.2026): Bindestrich in Wortverbindungen nicht trennen («Culinarium‑Wochenende»), letztes Paar bis 18 Zeichen zusammenhalten
            inner = re.sub(r'(?<=[A-Za-zÄÖÜäöüß])-(?=[A-Za-zÄÖÜäöüß])', '\u2011', inner)
        neu = schuetzen(inner, aw=(tag == 'dt' and 'aw-liste' in h[max(0, m.start() - 600):m.start()]), lang=('ad-titel' in auf))
        if neu != inner:
            n[0] += 1
        return '<%s%s>%s</%s>' % (tag, auf, neu, tag)
    h2 = re.sub(r'<(h1|h2|h3|dt)(\b[^>]*)>(.*?)</\1>', eins, h, flags=re.S)
    if h2 != h:
        open(pfad, 'w', encoding='utf-8').write(h2)
    return n[0]


if __name__ == '__main__':
    gesamt = 0
    for d in ('', 'en'):
        for s in SEITEN:
            p = os.path.join(HIER, d, s + '.html')
            if os.path.exists(p):
                gesamt += seite(p)
    print('Waisen: %d Überschriften mit geschütztem letzten Wortpaar (de + en)' % gesamt)
