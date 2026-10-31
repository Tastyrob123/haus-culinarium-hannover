#!/usr/bin/env python3
"""Augen-Urteile der Augenprüfung vom 30.10.2026 (Lauf dok-3010), über Titel/ID an die Dokumente gebunden.
Angesehen: alle 117 Vorlagen, alle 39 Vorschläge, alle 40 Entwerfen-Muster, Stichprobe 60 Muster und 30 Arten (Kontaktbögen bogen/).
Aufruf: python3 augen-culinarium-3010.py <lauf> <augen.json>"""
import json, sys, re
LAUF, AUS = sys.argv[1], sys.argv[2]
D = json.load(open(LAUF + '/dokumente.json', encoding='utf-8'))['dokumente']
A_KRIT = [7, 8, 10, 11, 13, 14, 19, 20, 22, 23, 25, 29]
FUNDE = [   # (Quelle-Muster, Titel-Muster, Kriterium, Notiz)
    ('Vorlage', r'^Menükarte · Fr 22\. und Sa 23\. September 2023$', 10, 'Auge: Löcher nach Hauptgang und Dessert; die Drinks «Butternut Old Fashioned» und «Escape» stehen abgesetzt und wirken wie Teil des nächsten Gangs, «Birne» klebt am Vorspeisen-Teller'),
    ('Vorlage|Art|Muster|Entwerfen', r'27\.–28\. November · Menükarte|18\.–19\. Dezember · Menükarte|^Menükarte am Tisch', 19, 'Auge: Menükarte für einen Abend im November/Dezember 2026 trägt das Menü vom 21./22. Februar 2025 (Sauerteig | Tomate | Butter …): Bestand als Ersatz, für den Abend nicht belegt'),
    ('Entwerfen', r'^Menükarte am Tisch: Gang, Teller und Drink, schmal', 22, 'Auge: die fünf Entwürfe sind fast gleich (gleicher Aufbau, gleicher Inhalt), keine echte Auswahl'),
    ('Vorlage|Art|Muster', r'Immer dieselben Leute|Wer dahinter steht|Danke für den Abend|Bild im Rahmen(?!.*· dc)', 20, 'Auge: Culinarium-Blatt mit dem Satz «Dann haste allet richtig jemacht!»; der stammt aus einem Beitrag von Dirty Chicken (_quelle/dirty-chicken/ig), nicht aus der Stimme des Culinarium'),
    ('Muster', r'^Titelblatt · DL quer · dc$', 11, 'Auge: Inhalt klein in der Mitte des DL-Querformats, ringsum leer (wenig Inhalt = grösser)'),
    ('Muster', r'^Rückseite mit Adresse · (A5 quer · dc|Quadrat · creme)$', 11, 'Auge: Inhalt klein, eine Hälfte des Blatts bleibt leer (wenig Inhalt = grösser)'),
    ('Muster', r'^Plakat aus dem Archiv, ganz · (A6 hoch|A4 hoch|Story 9:16)', 11, 'Auge: Plakat steht klein, darunter (Story: darüber und darunter) eine grosse leere Fläche, Roberts Fund «Plakat als Story» besteht weiter'),
    ('Muster|Entwerfen', r'^Bild oben · Newsletter 600 px · dunkel$|^Plakat für den nächsten Abend, vorne die Illustratio.*aushang|Entwurf 4', 7, 'Auge: Titel «An / der langen Tafel», ein Wort allein in der ersten Zeile'),
]
ANGESEHEN_ALLE = {'Vorlage', 'Vorschlag', 'Entwerfen'}
augen = {}; n = 0
for q in ('Muster', 'Art'):
    for k in A_KRIT: augen[f'{q}/*/{k}'] = {'urteil': 'gruen', 'notiz': 'Auge an der Stichprobe (60 Muster, 30 Arten), kein Fund'}
for d in D:
    if d['quelle'] in ANGESEHEN_ALLE:
        for k in A_KRIT: augen[f"{d['quelle']}/{d['id']}/{k}"] = {'urteil': 'gruen', 'notiz': 'Auge am Kontaktbogen, kein Fund'}
    for q, muster, k, notiz in FUNDE:
        if re.fullmatch(q, d['quelle']) and re.search(muster, d['titel'] or '') and not (k == 7 and d['quelle'] == 'Entwerfen' and 'An der langen' not in json.dumps(d, ensure_ascii=False) and 'Plakat für den nächsten Abend' not in d['titel']):
            augen[f"{d['quelle']}/{d['id']}/{k}"] = {'urteil': 'rot', 'notiz': notiz}; n += 1
json.dump(augen, open(AUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(augen), 'Urteile,', n, 'Augen-Funde')
