#!/usr/bin/env python3
"""Augen-Urteile Tor 3, Gästebuch (Lauf gaestebuch-3010t3, 30.10.2026): ganze Seiten 1440 und 390 (Übersicht, Anleitung bis zum Ende),
Chat ausprobieren am lebenden Werkzeug (das Tor klickt «ausprobieren» nicht), jeder Maschinen-Fund am Bild.
Aufruf: python3 augen-gaestebuch-3010t3.py <augen.json>"""
import json, sys
A_KRIT = [4, 6, 8, 9, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29, 30, 32, 33, 36]
WK = ['gaestebuch', 'gaestebuch-anleitung']
ROT = {
 ('gaestebuch', 23): 'Hero «Solange dies ein Entwurf ist, sind alle Anfragen hier Beispiele und Proben.»; Chat ausprobieren «Auf der Website … steht der Chat noch nicht.»',
 ('gaestebuch', 33): 'Chat ausprobieren: mittiges Fenster über abgedunkelter Seite statt an der Ecke aufklappend',
 ('gaestebuch-anleitung', 23): 'Kap. 01 «Einträge mit dem Wort «Beispiel» sind erfunden»; Kap. 11 «Anmeldung … wenn das Werkzeug an dein Haus übergeben wird»; Kap. 12 Bild «Probe-Antwort ohne KI … Demo»; Einträge mit Marke «Beispiel» und @example.com-Adressen',
 ('gaestebuch', 12): 'Eingang 1440: Trenner am Zeilenanfang/-ende in den Anfrage-Karten («Freitag oder Samstag / · 4 Plätze», «WARTELISTE · / 03:05», «TERMIN OFFEN · / KÜCHE FRAGEN»)',
 ('gaestebuch-anleitung', 24): 'Bilder Kap. 03, 08, 12 zeigen noch Schliessen-Knöpfe mit «×»',
}
augen = {}
for w in WK:
    for k in A_KRIT: augen[f'{w}/*/{k}'] = {'urteil': 'gruen', 'notiz': 'Auge an der ganzen Seite 1440 und 390 und an jedem Fund (30.10., Tor 3), kein Fund'}
for (w, k), n in ROT.items(): augen[f'{w}/*/{k}'] = {'urteil': 'rot', 'notiz': 'Auge: ' + n}
augen['_verworfen'] = [
 {'art': 'ueberlappt', 'muster': 'h2.wo-zl', 'grund': 'Auge: Titelwörter vor dem Einscrollen noch im Auftritt-Versatz; nach dem Auftritt am Bild keine Überdeckung (augen2/anleitung-1440-11)'},
 {'art': 'kante', 'muster': 'VOR DEM SENDEN', 'grund': 'Auge: Liste mit Kästchen, Text hängend eingezogen, gewollt'},
]
json.dump(augen, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(len(augen), 'Urteile')
