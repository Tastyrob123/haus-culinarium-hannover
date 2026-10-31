#!/usr/bin/env python3
"""Augen-Urteile Tor 3, Markenbuch (Lauf markenbuch-3010t3, 30.10.2026): ganze Seiten 1440 und 390 (Start, Hausregeln, Anleitung),
dazu jeder Maschinen-Fund am Bild. Aufruf: python3 augen-markenbuch-3010t3.py <augen.json>"""
import json, sys
A_KRIT = [4, 6, 8, 9, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29, 30, 32, 33, 36]
WK = ['plakatarchiv', 'plakatarchiv-buch', 'plakatarchiv-anleitung']
ROT = {   # (werkzeug, kriterium): Fund
 ('plakatarchiv', 23): 'Bildrechte-Leiste in jeder Ansicht: «wer fotografiert hat, ist noch nicht bei jedem Foto belegt» = offene Rechtefrage beim Kunden',
 ('plakatarchiv-buch', 23): 'Bilder: «Wer sie gemacht hat und wer darauf zu sehen ist, ist noch nicht belegt» = offene Rechtefrage',
 ('plakatarchiv-buch', 24): 'Einleitung «das C und das x» und Tapete «an jeder Kreuzung das x»: x als Zeichen des Hauses',
 ('plakatarchiv-buch', 26): 'Mengenverhältnis 1440: «5 %» tiefer als 52/34/9 %; 390 «5 %» rechts abgeschnitten (Tor 2 M4)',
 ('plakatarchiv-buch', 4): '390 Bilder: «Wild Side bei Nacht» allein in der Reihe; Logo «Richtig» 4+2; Downloads 1440 «Urbanist» allein (Tor 2 M6)',
 ('plakatarchiv-buch', 5): '390: dritte Reihe der Kapitel-Leiste liegt unter dem weissen Blatt',
 ('plakatarchiv-buch', 2): '390 Schrift: «S|esam», «f|ür dich», «PL|ÄTZE» mitten im Wort gebrochen; RGB-Zeilen der Farbkarten brechen',
 ('plakatarchiv-anleitung', 6): 'Kap. 01 «So ist das Markenbuch / ␣aufgebaut.»: zweite Zeile um ein Leerzeichen eingerückt',
 ('plakatarchiv-anleitung', 23): 'Kap. 07 «Solange die Prüfung durch Claude nicht eingeschaltet ist, antwortet eine Probe» und Kap. 04 Rechte «noch nicht belegt»',
 ('plakatarchiv-buch', 15): 'Tor 2 M3: nav.leiste und nav.index zu denselben Ankern; «Logo-Regeln als eigene Seite» und «Logo richtig und falsch» zum selben Ziel',
 ('plakatarchiv-buch', 3): 'Tor 2 M7: Haltung-Karten und Herkunft-Fotos mit verschiedenen Oberkanten; zweizeilige Logo-Titel verschieben die Texte',
 ('plakatarchiv-buch', 6): 'Tor 2 M10: 390 Kopf «WALK ON THE WILD SIDE ◇ / …» Raute am Zeilenende, Zeilen versetzt',
 ('plakatarchiv-anleitung', 4): 'Tor 2 M9: Inhalt 1440, «Die Hausregeln» allein in der letzten Reihe',
}
augen = {}
for w in WK:
    for k in A_KRIT:
        augen[f'{w}/*/{k}'] = {'urteil': 'gruen', 'notiz': 'Auge an der ganzen Seite 1440 und 390 und an jedem Fund (30.10., Tor 3), kein Fund'}
for (w, k), n in ROT.items(): augen[f'{w}/*/{k}'] = {'urteil': 'rot', 'notiz': 'Auge: ' + n}
augen['_verworfen'] = [
 {'werkzeug': 'plakatarchiv-buch', 'art': 'spalte', 'muster': 'kopiert', 'grund': 'Auge: Farbkarte der Hausregeln, Name/Rolle/HEX/RGB gewollt untereinander, am Bild sauber'},
 {'werkzeug': 'plakatarchiv', 'art': 'einzelwort', 'muster': 'JPG|PNG|SVG', 'grund': 'Auge: Bildzeile als Stapel Name / Grösse / Format, drei eigene Zeilen'},
 {'werkzeug': 'plakatarchiv-buch', 'art': 'bewegung', 'muster': 'bleiben .*unsichtbar: «KOPIERT», «kopiert»$', 'grund': 'Auge: «kopiert» ist die Rückmeldung nach dem Klick auf eine Farbe, vorher gewollt unsichtbar'},
 {'werkzeug': 'plakatarchiv', 'art': 'kante', 'muster': 'Beispiel-Entwurf', 'grund': 'Auge: zwei getrennte Karten, Text am Bild auf einer Kante'},
]
json.dump(augen, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(augen), 'Urteile')
