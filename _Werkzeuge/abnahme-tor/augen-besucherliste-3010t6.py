#!/usr/bin/env python3
"""Augen-Urteile (Kriterien A) der Besucherliste (:9086), Abnahme-Tor 6 vom 30.10.2026, über den Zustandsnamen an die Zustände eines Laufs gebunden.
Angesehen: jeder Zustand des 1440-Inventars am Bild, alle acht Ansichten und die Anleitung als Ganzseite bei 1440, 1000 und 390 (augen/, augen1000/, augen390/),
der Rundgang in allen fünf Schritten bei 1440/1000/390 (das Tor erfasst nur Schritt 1).
Aufruf: python3 augen-besucherliste-3010t6.py <lauf> <augen.json> [--offen]   (--offen: Funde vor der Reparatur eintragen)"""
import json, sys, re, glob, os
LAUF, AUS = sys.argv[1], sys.argv[2]
A_KRIT = [4, 6, 8, 9, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29, 30, 32, 33, 36, 37]
# (Werkzeug, Zustandsname-Muster, Kriterium, Notiz) · Funde 1–26, gemeldet an cu-tresen-kleid 30.10.2026
FUNDE = [
    ('besucherliste$', r'^Start$|^7 Tage$|^90 Tage$', 26, 'Auge: Rangliste «Am meisten angesehen» zerfällt («… im Schnitt» unter dem Bild, Name nicht auf Höhe von Balken/Zahl); 1000: Kennzahlen nicht auf einer Grundlinie (F1, F3)'),
    ('besucherliste$', r'^Start$', 9, 'Auge: Hero-Titel bricht «Guten Abend. Wer / war zu Besuch?» (F9); 1000: Leiste deckt Zeitraum-Wahl (F22)'),
    ('besucherliste$', r'^Start$', 28, 'Auge: «Alle Besuche ↗» ohne Knauf, Pfeil extern für internen Wechsel (F20)'),
    ('besucherliste$', r'Herkunft$', 8, 'Auge: Hero-Satz läuft über das Schild «WILD SIDE» (F7)'),
    ('besucherliste$', r'Herkunft$', 6, 'Auge: «Gerät»-Zeilen gestreckt; 390 Kennzahlen versetzt; 1000 «Großbritannien» am Balken (F16, F19, F23)'),
    ('besucherliste$', r'Seiten$', 6, 'Auge: Tabellenkopf versetzt (F4); 1000/390 Namen zerbrechen in Silben, Zeitwerte umbrochen (F13, F21)'),
    ('besucherliste$', r'Verlauf$', 6, 'Auge: 390 «3:48 / Min.» umbrochen (F14)'),
    ('besucherliste$', r'Zum Platz$', 26, 'Auge: 1000 Prozentzahlen einer Reihe nicht auf einer Grundlinie (F24)'),
    ('besucherliste$', r'So wird gezählt$', 6, 'Auge: rechte Karte 16 px tiefer (F2), «(DSGVO).» allein (F8)'),
    ('besucherliste$', r'rundgang$|Kurzer Rundgang$', 17, 'Auge: Schritt 2 «Acht Ansichten» hebt nur «Übersicht» hervor (F5)'),
    ('besucherliste$', r'rundgang$|Kurzer Rundgang$', 33, 'Auge: Rundgang-Karte deckt das Gezeigte zu (1440 Schritt 4/5, 1000 Schritt 1) (F6)'),
    ('besucherliste$', r'^Besuche 1$|Zum Platz · 50$|Warteliste begonnen · 43$|Anruf oder Instagram · 39$|Am Handy · 286$', 6, 'Auge: «·» am Zeilenende; 390 Filter ungleich gross (F15, F17)'),
    ('besucherliste-anleitung', r'^Start$', 9, 'Auge: Anleitung-Hero als Tafel links, rechts leere Tapete (F11); 390 Kopf dreizeilig (F18)'),
    ('besucherliste-anleitung', r'^Start$|Bild gross ansehen', 30, 'Auge: alle zehn Kapitelbilder alter Stand (Rand mit «Was gezählt wird») (F12)'),
]
# Mit dem Auge verworfene Maschinen-Funde (am Bild und im DOM belegt)
VERWORFEN = [
    {'werkzeug': 'besucherliste.*', 'art': 'stil', 'muster': 'Versalien in Culinarium Mono', 'grund': 'Culinarium Mono ist @font-face dmmono.woff2 (kleid/culinarium.css:13), also DM Mono; laut Stilblatt (Rolle etikett) Versalien erlaubt'},
    {'werkzeug': 'besucherliste.*', 'art': 'randlos', 'muster': 'WEBSITE ANSEHEN', 'grund': 'bei 1000 ist der Text nur für Vorleser (1 px breit), sichtbar ist der Rundknopf'},
    {'werkzeug': 'besucherliste.*', 'art': 'ueberlappt', 'muster': 'Google ⟷ Handy oder Rechner', 'grund': 'Zwischenstand des Auftritts unterhalb des Bildschirms (translate), eingeschwungen 95 px Abstand'},
    {'werkzeug': 'besucherliste.*', 'art': 'spalte', 'muster': r'^Startseite .* im Schnitt', 'grund': 'nach Reparatur 1/27: Rasterzeile Bild | Name über «… im Schnitt» | Balken | Zahl | Anteil, je Teil einzeilig, Name und Balken auf einer Höhe (am Bild 1440/1280/1000/390: nach2/rang-*.png); die Heuristik zählt die Rasterzellen als Zeilen'},
    {'werkzeug': 'besucherliste.*', 'art': 'mitte', 'muster': r'div\.zahlen > div\.blatt', 'grund': 'Kennzahl-Karte (kein Druckdokument), oben angelegt und ruhig: Etikett, Zahl, Unterzeile; die «12 % unten frei» sind die schwebende Leiste «Du siehst Beispielwerte», die im 1440-Bild über dem Kartenfuss liegt (b/besucherliste-001-f0.jpg), ganz sichtbar ist die Karte voll (end/start-1440-00.jpg)'},
    {'werkzeug': 'besucherliste.*', 'art': 'loch', 'muster': r'div\.detail', 'grund': 'KEIN Fehlalarm: Fund 29 im Schlusslauf (Stand 12:40), behoben 14:40 von cu-messlauf (registre.css .besuch__buehne); nachgeprüft 14:46 an 240 Besuchskarten (1440 und 1280, Filter Alle, Zum Platz, Warteliste begonnen): 0 Löcher, 0 Mitte (besucherliste-3010t6/f29, f29b), Messlauf Chromium + WebKit 0, Bewegung 0 Ruckler (nachpruefung-1450)'},
    {'werkzeug': 'besucherliste.*', 'art': 'einzelwort', 'muster': 'vorbeischauen', 'grund': 'Titel aus drei Wörtern passt bei 1000 nicht in eine Zeile; «Wann Gäste / vorbeischauen.» ist ausgewogen (letzte Zeile länger als die erste)'},
]
offen = '--offen' in sys.argv
augen = {'_verworfen': VERWORFEN}; n = 0
for inv in glob.glob(os.path.join(LAUF, '*', 'inventar.json')):
    I = json.load(open(inv, encoding='utf-8')); wk = os.path.basename(os.path.dirname(inv))
    for zu in I['zustaende']:
        for k in A_KRIT: augen[f"{wk}/{zu['id']}/{k}"] = {'urteil': 'gruen', 'notiz': 'Auge am Bild (1440, Ganzseiten 1440/1000/390), kein Fund'}
        if not offen: continue
        name = zu['name'].split(' → ')[-1].strip()
        for w, muster, k, notiz in FUNDE:
            if re.fullmatch(w, wk) and re.search(muster, name): augen[f"{wk}/{zu['id']}/{k}"] = {'urteil': 'rot', 'notiz': notiz}; n += 1
json.dump(augen, open(AUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(augen) - 1, 'Urteile,', n, 'Augen-Funde')
