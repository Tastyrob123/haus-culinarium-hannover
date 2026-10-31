#!/usr/bin/env python3
"""La Carte · Culinarium Hannover — setzt die Menükarten der Abende neu, im Kleid des Culinarium (28.10.2026, Muster: satz_bau.py der Tafel im Schäfli).

Grundlage ist die Machart des Hauses (Fehlerbuch 10a: das Original ist die Grundlage, nie schwächer): die gedruckte Karte am Platz (Foto in
_quelle/extern/ig-highlights/2025-02-22_highlight-4865-06.jpg) hat oben die Wortmarke CULINARIUM mit «Menü», darunter mittig Gang für Gang den Namen
des Gangs, Rudis Teller in Versalien, Momos Drink klein darunter und einen senkrechten Strich zwischen den Gängen. Verfeinert in den Farben und
Schriften der Website (website/assets/culinarium.css): Warmweiss, Nacht und Kerze; Wortmarke als nachgezogener Vektor (marke.svg #wm, unverändert);
Titel in Fraunces mit weichen Enden; Rudis Zeilen in Versalien mit Schrägstrich wie in seinen Beiträgen («LAUCH / BLUMENKOHL / CHIPOTLE»); Gang als
Etikett in Urbanist; Datum in DM Mono; zwischen Teller und Drink das «x» von «Momo x Rudi» als Zeichnung; Ticketpreis als ruhige Marke unten.

Nichts ist abgetippt: jeder Gang, Teller, Drink, Preis und jedes Datum kommt aus _daten/quelle/<karte>.json (karten_lesen.py, gegen die Website
geprüft). Bewusst anders als das Original (typografisch, der Wortlaut bleibt): Trennstrich «|» in Rudis Tellern als « / » (so schreibt Rudi selbst);
die Drinks behalten ihre Zeichen. Gesperrte Versalien höchstens .08em (pdftotext, Abschnitt 9).

Aus dem Satz liest einlesen.py die Karte als Baum; satz/satz.js setzt daraus Zeichen für Zeichen dasselbe HTML (Vorschau, PDF, Werkbank).
Die Karte «Der nächste Abend» setzt satz.js selbst (Teil ABEND) mit denselben Klassen.

    python3 _werkzeuge/carte/satz_bau.py          setzt alle Karten nach satz/u-<karte>.html, die Zeichen nach satz/zeichen.json
"""
import html, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(HAUS, 'website')
QD = os.path.join(HIER, '_daten', 'quelle')
SATZ = os.path.join(HIER, 'satz')
e = lambda t: html.escape(t, quote=False)

# Hausangaben aus der Website (weg_wahl2.py führt die Adresse der Bar, website/bau.py den Namen); als Text gelesen, nie importiert
NAME = 'Culinarium'
BAR = 'Walk on the Wild Side'
_weg = open(os.path.join(WEB, 'weg_wahl2.py'), encoding='utf-8').read()
_adr = re.search(r"\('Adresse', '([^']+)'\)", _weg).group(1).split('<br>')
FUSS = f'{NAME} · {BAR} · {_adr[0]} · {_adr[1]}'


def wortmarke():
    """Die Wortmarke CULINARIUM als eigenes svg aus marke.svg #wm (unverändert, nur als Ganzes eingesetzt)."""
    s = open(os.path.join(WEB, 'assets', 'zeichen', 'marke.svg'), encoding='utf-8').read()
    m = re.search(r'<symbol id="wm" viewBox="([^"]+)">(.*?)</symbol>', s, re.S)
    return f'<svg class="cu-wm" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="{m.group(1)}" fill="currentColor">{m.group(2).strip()}</svg>'


WM = wortmarke()


def q(kid):
    return json.load(open(os.path.join(QD, kid + '.json'), encoding='utf-8'))


def rudi(t):
    """Rudis Teller: Trennstrich der gedruckten Karte « | » als « / » wie in seinen Beiträgen; Versalien macht der Satz (CSS), der Wortlaut bleibt."""
    return re.sub(r'\s*\|\s*', ' / ', t.strip())


def preis_teile(p):
    """«89,00 EUR» → ('89,00', 'EUR')"""
    m = re.match(r'^\s*([\d.,]+)\s*(.*?)\s*$', p)
    return (m.group(1), m.group(2)) if m else (p, '')


# ---------------------------------------------------------------- Bausteine (dieselben Klassen setzt satz.js für «Der nächste Abend»)
def gang(g, erstes):
    trenn = '' if erstes else '<div class="sb-gang"><i></i></div>'
    innen = f'<p class="sb-gn">{e(g["gang"])}</p>'
    if g['teller']:
        innen += f'<p class="sb-n">{e(rudi(g["teller"]))}</p>'
    if g['drink']:
        innen += f'<p class="sb-dr">{e(g["drink"])}</p>'
    return trenn + f'<div class="sb-m">{innen}</div>'


def oben(d):
    titel = d['motto'] or d['titel'] or 'Menü'
    return (f'<div class="sb-oben"><span class="uz sb-zeichen">{WM}</span>'
            f'<h2 class="sb-band">{e(titel)}</h2><p class="sb-datum">{e(d["datum"])}</p>'
            + (f'<p class="sb-mit">{e(d["mit"])}</p>' if d.get('mit') else '') + '</div>')


def unten(d):
    z, w = preis_teile(d['preis'])
    return (f'<div class="sb-unten"><div class="sb-g sb-lunchpreis"><p class="sb-p"><span><em>Ticket</em><b>{e(z)}</b>'
            + (f'<small>{e(w)}</small>' if w else '') + '</span></p></div></div>')


def blatt(inhalt, mx='1.8'):
    return (f'<section data-max="{mx}" class="blatt cu" data-b="210" data-h="297" style="width:210mm;height:297mm">'
            f'<div class="inhalt">{inhalt}</div><footer class="ufuss2">{e(FUSS)}</footer></section>')


def doc(titel, seiten):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{e(titel)} · {e(NAME)}</title>\n'
            f'<link rel="stylesheet" href="satz.css"><style>@page{{size:210mm 297mm;margin:0}}</style></head><body>' + ''.join(seiten) + '</body></html>')


def abendkarte(kid):
    d = q(kid)
    gaenge = ''.join(gang(g, i == 0) for i, g in enumerate(d['gaenge']))
    up = ''
    if d['upgrade']:
        up = ('<div class="sb-upg"><p class="sb-h sb-up">Upgrade nach Wahl</p>'
              + ''.join(f'<div class="sb-m sb-m--up"><p class="sb-n sb-n--satz">{e(u)}</p></div>' for u in d['upgrade']) + '</div>')
    menue = f'<div class="sb-menue">{gaenge}{up}</div>'
    return doc('Menü ' + d['name'], [blatt(f'<div class="sb-quer">{oben(d)}{menue}{unten(d)}</div>')])


def zeichen():
    """Feste Teile für das Blatt «Der nächste Abend» (satz.js ABEND): Wortmarke, Strich zwischen den Gängen, Fusszeile."""
    return dict(ZEICHEN=WM, BLATT='<i></i>', FUSS=FUSS, HAUS=NAME, WORTMARKE=WM)


def _schreib(p, t):
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        f.write(t)
    os.replace(p + '.neu', p)


if __name__ == '__main__':
    os.makedirs(SATZ, exist_ok=True)
    for f in sorted(os.listdir(QD)):
        kid = f[:-5]
        if not f.startswith('abend-') or not f.endswith('.json'):
            continue
        _schreib(os.path.join(SATZ, f'u-{kid}.html'), abendkarte(kid))
        print('gesetzt:', f'satz/u-{kid}.html')
    with open(os.path.join(SATZ, 'zeichen.json'), 'w', encoding='utf-8') as f:
        json.dump(zeichen(), f, ensure_ascii=False)
    print('Zeichen: satz/zeichen.json')
