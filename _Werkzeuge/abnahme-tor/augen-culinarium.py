#!/usr/bin/env python3
"""Augen-Urteile (Kriterien A) der Augenprüfung an den Kontaktbögen vom 29.10.2026, über Titel an die Dokumente eines Laufs gebunden.
Angesehen: alle Vorlagen, alle Entwerfen-Muster, die Vorschläge Bogen 1 (20 von 39). Nicht angesehen: Arten, Muster aus dem Reiter «Vorlagen».
Aufruf: python3 augen-culinarium.py <lauf> <augen.json>"""
import json, sys, re
LAUF, AUS = sys.argv[1], sys.argv[2]
D = json.load(open(LAUF + '/dokumente.json', encoding='utf-8'))['dokumente']
A_KRIT = [10, 11, 14, 19, 20, 22, 25, 29]
FUNDE = [   # (Quelle, Titel-Muster, Kriterium, Notiz)
    ('Vorlage', r'^Momos Drinks auf Instagram$|^Dirty Chicken · Pop-up · Dirty Drinks$|^Jeder Teller von Hand angerichtet$', 10, 'Auge: Fusszeile klebt ohne Abstand am Lesetext'),
    ('Vorlage', r'^Für das Team: (Ablauf des Abends|Allergien an der Tafel)$', 10, 'Auge: Gruppe sitzt hoch, unteres Drittel bis zur Fusszeile leer'),
    # Rudis Zeilen in Versalien mit «/» sind Hausregel (Oberchef 29.10.2026: verworfen war bei «Vom Pass» der Satz, nicht die Schreibung): diese Karten nur auf Satz und Proportion prüfen
    ('Vorlage', r'Das erste Pop-up-Plakat|Erstes Pop-up, Sa 20\. Mai 2023', 19, 'Auge: Bestand als Vorlage (Foto eines aufgehängten Plakats bzw. Collage), keine setzbare Vorlage'),
    ('Entwerfen', r'^Platzkarten mit Namen', 22, 'Auge: Auftrag «Platzkarten mit Namen» liefert Einladungen ohne Namen'),
    ('Entwerfen', r'^Flyer für das Pop-up Dirty Chicken · Entwurf [25]', 14, 'Auge: Dirty-Chicken-Flyer mit dem Culinarium-«C» statt dem Zeichen von Dirty Chicken'),
    ('Entwerfen', r'^Plakat A3 für die Wand neben der Bar · Entwurf [2-5]', 11, 'Auge: Entwurf ohne Titel und Text, nur Motiv und grosse leere Fläche (Entwurf 5 zeigt «undefined»)'),
    ('Vorschlag', r'· (A3 hoch|Story 9:16)$', 10, 'Auge: Vorderseite zeigt das Motiv klein in der Mitte, oben und unten leere Farbfläche'),
]
angesehen = lambda d: d['quelle'] in ('Vorlage', 'Entwerfen') or (d['quelle'] == 'Vorschlag' and int(d['id']) - min(int(x['id']) for x in D if x['quelle'] == 'Vorschlag') < 20)
augen = {}; n = 0
for d in D:
    if not angesehen(d): continue
    for k in A_KRIT: augen[f"{d['quelle']}/{d['id']}/{k}"] = {'urteil': 'gruen', 'notiz': 'Auge am Kontaktbogen, kein Fund'}
    for q, muster, k, notiz in FUNDE:
        if d['quelle'] == q and re.search(muster, d['titel'] or ''): augen[f"{d['quelle']}/{d['id']}/{k}"] = {'urteil': 'rot', 'notiz': notiz}; n += 1
json.dump(augen, open(AUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(augen), 'Urteile,', n, 'Augen-Funde')
