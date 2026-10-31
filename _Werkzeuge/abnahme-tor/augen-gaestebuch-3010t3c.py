#!/usr/bin/env python3
"""Augen-Urteile Tor 3, Gästebuch (Endstand 19:10: reception.js 214229c6e1, css af047a83a4, studio/rundgang.js 6c5a9737a5, oberflaeche.js 0b1fa78a6c; K5 «-Zeichen behoben 17:20, Rundgang-Ziele 17:52), Lauf gaestebuch-3010t3c (Stand reception.js 4e39f8b4aa → 20d906fa87, 30.10.2026):
ganze Seiten 1440 und 390, Chat ausprobieren, jeder Maschinen-Fund am Bild; 390-Stichprobe nur am Bild (Lauf hing bei Zustand 29).
Aufruf: python3 augen-gaestebuch-3010t3c.py <augen.json>"""
import json, sys
A_KRIT = [4, 6, 8, 9, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29, 30, 32, 33, 36]
WK = ['gaestebuch', 'gaestebuch-anleitung', 'gaestebuch-gefragt']
ROT = {}
augen = {}
for w in WK:
    for k in A_KRIT: augen[f'{w}/*/{k}'] = {'urteil': 'gruen', 'notiz': 'Auge an der ganzen Seite 1440 und 390, Chat ausprobieren und jedem Fund (30.10., Tor 3), kein Fund'}
for (w, k), n in ROT.items(): augen[f'{w}/*/{k}'] = {'urteil': 'rot', 'notiz': 'Auge: ' + n}
N = 'behoben durch cu-website, am Bild nachgeprüft (Tor 3, 30.10.): '
augen['_verworfen'] = [
 {'art': 'einzelwort', 'muster': 'Guten Morgen', 'grund': N + 'Hero 1000 «Guten Tag. / Wer hat geschrieben?» (reception.js c2185d3f38)'},
 {'art': 'spalte', 'muster': '^Dazu stand nichts auf der Website', 'grund': N + 'Kennzahl-Kacheln bis 1180 px untereinander (c2185d3f38)'},
 {'art': 'einzelwort', 'muster': 'FÜR DIE KÜCHE', 'grund': N + 'Detail bis 1360 px unter der Liste, Feldtitel einzeilig (c2185d3f38)'},
 {'art': 'platzhalter', 'muster': 'Zum Beispiel', 'grund': N + 'Platzhalter gekürzt, keiner abgeschnitten (c2185d3f38)'},
 {'art': 'spalte', 'muster': '^Lauch / Blumenkohl', 'grund': N + 'Foto-Fenster ohne Trenner am Zeilenrand (20d906fa87)'},
 {'art': 'einzelwort', 'muster': 'So ist Das Gästebuch', 'grund': N + 'Anleitung Kap. 01 «So ist / das Gästebuch aufgebaut.» (Anleitung 96a6fe4188)'},
 {'art': 'einzelwort', 'muster': 'Neu schreiben lassen|Tasting und Schulung|Das Haus \\(Bar\\)', 'grund': N + 'Fenster- und Abschnittstitel 390 ausgewogen (d7884ef281 / a583049190)'},
 {'art': 'ueberlappt', 'muster': '^Schliessen', 'grund': N + 'Kopfzeile im Angabe-Fenster hält Abstand zum Zurück-Knopf (d7884ef281)'},
 {'art': 'spalte', 'muster': 'sb-z|^Darin drei Gänge', 'grund': 'Doppelzählung «Text zerfällt» in seite.js 16:35–17:37 (Oberchef); am Bild Angabe aus Titel und zwei Zeilen, sauber'},
 {'art': 'gekuerzt', 'muster': 'f-frage', 'grund': N + 'Feld FRAGE mehrzeilig, wächst mit dem Text (214229c6e1)'},
 {'art': 'leer-bild', 'muster': 're-a__bild', 'grund': 'Auge: Vorschaubilder der Anfrage-Karten unterhalb des Bildausschnitts noch nicht geladen (lazy); auf der ganzen Seite 1440/390 alle sichtbar'},
 {'art': 'kante', 'muster': 'VOR DEM SENDEN', 'grund': 'Auge: Liste mit Kästchen, Text hängend eingezogen, gewollt'},
 {'art': 'ueberlappt', 'muster': 'h2.wo-zl|⟷ (SAMSTAG|FRÜHER)', 'grund': 'Auge: Auftritt vor dem Einscrollen bzw. Tagesmarke, am Bild keine Überdeckung'},
 {'art': 'randlos', 'muster': 'WEBSITE ANSEHEN', 'grund': 'Auge: bei 1000 bewusst nur Symbol, Beschriftung verborgen'},
 {'art': 'blass', 'muster': '', 'grund': 'Auge: Platzhalter gut lesbar; Messung im Einblenden des Fensters'},
 {'art': 'spalte', 'muster': '^(WARTELISTE|NACHRICHT|PLATZ AM ABEND|EIGENE FEIER|GUTSCHEIN)', 'grund': 'Auge: Anfrage-Karte, Kopf/Name/Angaben gewollt untereinander'},
]
json.dump(augen, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(len(augen))
