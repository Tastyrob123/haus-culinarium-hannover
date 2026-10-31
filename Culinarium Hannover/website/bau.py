#!/usr/bin/env python3
"""Culinarium Hannover · Website, Neubau vom 26.10.2026 (nach Roberts Ablehnung des ersten Rohbaus).
Baut alle Seiten, Bilder, Filme und das Zeichen aus _quelle/. Nur lokal, noindex.
Aufruf: python3 website/bau.py   ·   Ansehen: http://127.0.0.1:8978/haus/Culinarium%20Hannover/website/index.html
Fakten nur aus _kette/03-sammler/fakten.json und den Beitragstexten in _quelle/ (je Stelle im Kommentar)."""
import base64, html, io, json, os, re, shutil, subprocess, sys
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HIER)
A = os.path.join(HIER, 'assets')
E = html.escape
V = '_quelle/vom-kunden/'
D = V + 'drive/'
IG = '_quelle/extern/ig/'
DC = '_quelle/dirty-chicken/'
WS = '_quelle/walk-on-the-wild-side/ig/'
VERSION = '26218'   # 31.10.2026 Robert/Oberchef: Wild-Side-Logo = rotes Schild der Bar-Website (#F0323F, WILD / SIDE ausgespart), das weisse Quadrat (26217) war falsch; davor 30.10.2026 Oberchef: Chat-Kopf «Neu beginnen» statt Symbol; davor 30.10.2026 Tor: schwebende Knöpfe treten bei offenem Dialog zurück; davor 30.10.2026 Oberchef: Schliessen ohne «×» (Chat, Anfrage-Fenster, Abend-Ansicht, Ticket), Zurück-Pfeil; davor 30.10.2026 Tor: Vitrinen-Beschriftung, Detail-Titel, Jahreszahlen 1280, Karte Weg Handy; davor 30.10.2026 Oberchef: Bar-Textspalte breiter (Titel bleibt gross), Signature-Liste Handy 17 px; davor 30.10.2026 K37: Abendlauf-Strich über transform, reduced-motion ohne Bewegung; davor 30.10.2026 waisen nur kurze Wortpaare (Bar-Titel abgeschnitten); davor 30.10.2026 Vitrinen-Plakate lazy; davor 30.10.2026 Fuss: Culinarium-Spalte füllt ihre Höhe, 861–1300 px drei gleiche Spalten, Handy untereinander (Oberchef-Entscheid); davor 30.10.2026 Abnahme-Tor: Titel ohne Einzelwort, Team-Hero und Weg-Handy über der Knopfreihe, EN im Sprachknopf am Handy, Vitrinen gleich hoch, Kennzahlen Bar, Foto statt leerem Plakat 2023, Jahreszahlen mittig, DC-Fussspalte; davor 30.10.2026 wildside eingefroren, Lichtschein der Vitrinen am Handy beschnitten; davor 30.10.2026 Dirty Chicken: drei Kacheln mit Vorrang statt zwölf; davor 30.10.2026 Robert: «×» im Fuss raus, ruhiger Punkt; davor 30.10.2026 Tempo: Fraunces geteilt (weich 53 KB vorgeladen, hart 58 KB bei Bedarf), DC-Zeichen im Fuss lazy, Tapete DC als Daten, Abend-Auftakt am Rechner sofort, Bar: d3 zuerst; davor 29.10.2026 29.10.2026 Sprachschalter unten links als Knopf des Hauses, Textmitte in allen Knöpfen (text-box), Hero sofort, Robert-Befunde Handy
# vorher 26199: 29.10.2026 Chat als Eckfenster (Vorbild Rivage), Zugänge sichtbar: Gutschein, lange Tafel, «Schreib uns» als Knopf
# vorher 26198: 29.10.2026 Sprachschalter DE/EN (englische Fassung unter en/, bau_en.py), hreflang
ADRESSE = 'https://culinarium-hannover-entwurf.vercel.app/'   # für hreflang; die Website hat keine andere Adresse (ONLINE.md)
SEITE_AKTUELL = ['index.html']                                # kopf() setzt sie, fuss() liest sie (Sprachschalter im Fuss)
# vorher 26196: 29.10.2026 Anschluss ans Gästebuch (anfrage.js/.css, «Schreib uns», «Die lange Tafel für euch»)
# vorher 26195: 28.10.2026 Handy-Fassung (handy.css, Bilder am Handy)

# ---------------------------------------------------------------- Bilder
# Schlüssel: (Quelle, Bildausschnitt, Beschreibung für alt). Nur Rudis Dateien, Culinarium-Plakate und Dirty Chicken (Rudi).
BILD = {
    # Auftakt-Fassungen
    'momo': (D + '4568.jpg', '50% 40%', 'An der Bar wird ein Drink geschüttelt'),
    'rudi': (D + '5301.jpg', '50% 30%', 'Der Koch erklärt am Tisch einen Teller'),
    'glas': (D + '5369.jpg', '50% 55%', 'Ein Drink im Nick-and-Nora-Glas auf dunklem Tisch'),
    'tarte': (D + '5345.jpg', '30% 50%', 'Tarte mit roten Früchten und Eis'),
    'tafelleer': (D + '4972.jpg', '50% 50%', 'Die lange Tafel mit Kerzen, gedeckt'),
    'toast': (D + '4024.jpg', '50% 40%', 'Am Tisch wird angestoßen'),
    'tablett': (D + '63972.jpg', '50% 50%', 'Ein Tablett mit Gläsern wird gebracht'),
    'schildnacht': (D + '4096.jpg', '50% 50%', 'Das Schild Walk on the Wild Side bei Nacht'),
    'barnacht': (D + '4093.jpg', '50% 50%', 'Die Fenster der Bar von außen bei Nacht'),
    'anrichten': (V + '36738.png', '50% 50%', 'Der Koch richtet Teller an'),
    'kerze1': (D + '3855.jpg', '50% 40%', 'Ein Drink wird bei Kerzenlicht erklärt'),
    'kerze2': (D + '3858.jpg', '50% 40%', 'Gäste und Kerzen an der Tafel'),
    'kerze3': (D + '3859.jpg', '50% 40%', 'Blick durch die Tür auf die Tafel'),
    'theke': (D + '3925.jpg', '50% 40%', 'Hinter der Theke unter dem Negroni-Schriftzug'),
    'theke2': (D + '4019.jpg', '50% 50%', 'An der Bar wird vorbereitet'),
    'm1': (D + '4829.jpg', '50% 50%', 'Gekühlte Schalen werden bereitgestellt'),
    'm2': (D + '36593.jpg', '50% 50%', 'Mit dem Brenner über den Tellern'),
    'm3': (D + '4834.jpg', '50% 50%', 'Gläser mit Goldrand'),
    'm4': (D + '36378.jpg', '50% 50%', 'Ein Löffel über dem Dessert'),
    'm5': (D + '4840.jpg', '50% 50%', 'Eine Schale mit Haselnüssen'),
    'm6': (V + '36611.jpg', '50% 50%', 'Mit dem Spritzbeutel am Fenster'),
    'm7': (D + '4828.jpg', '50% 50%', 'Hände an den Gläsern'),
    'm8': (D + '4866.jpg', '50% 50%', 'Sauce wird angegossen'),
    'kueche': (V + '4869.jpg', '50% 40%', 'Zwei Köche von hinten am Pass'),
    'service': (D + '63990.jpg', '50% 40%', 'Ein Teller wird an den Tisch gebracht'),
    # Ankommen
    'schildtag': (D + '5541.jpg', '50% 40%', 'Die Schilder Walk on the Wild Side an der Hausecke'),
    'ecke': (V + '3967.jpg', '50% 50%', 'Die Hausecke mit der Bar'),
    'fassade': (D + '4951.jpg', '50% 50%', 'Die Fenster der Bar am Abend'),
    'flur': (D + '3887.jpg', '50% 50%', 'Durch den Flur in die Bar'),
    # Fenster
    'anstossen': (D + '5376.jpg', '50% 38%', 'Am Tisch wird bei Kerzen angestoßen'),
    # Aperitif
    'bar': (D + '3823.jpg', '50% 35%', 'An der Bar wird eingeschenkt'),
    'klaeren': (V + '4313.jpg', '50% 50%', 'Ein Drink läuft durch den Filter in die Gläser'),
    'g1': (D + '4558.jpg', '50% 45%', 'Drink mit Schaum und Garnitur'),
    'g2': (D + '5289.jpg', '50% 50%', 'Ein heller Drink mit Kräutern'),
    'g3': (D + '4858.jpg', '50% 50%', 'Ein Longdrink mit Erdbeere'),
    'g4': (D + '4876.jpg', '50% 50%', 'Ein Glas mit Feige'),
    'g5': (D + '63741.jpg', '50% 55%', 'Ein Drink auf dem Holztresen'),
    # Am Pass
    'pass': (D + '36567.jpg', '50% 50%', 'Am Pass werden die Teller angerichtet'),
    'pass2': (D + '36565.jpg', '50% 50%', 'Zwei Köche am Pass'),
    'pass3': (V + '4203.jpg', '50% 50%', 'Eine Reihe Teller wird garniert'),
    'pass4': (V + '36740.png', '50% 50%', 'Die Sauce kommt auf den Teller'),
    # Rudis Zeilen (Teller und Beitrag belegt, siehe ZEILEN)
    'lauch': (D + '5379.jpg', '50% 50%', 'Lauch, Blumenkohl und Chipotle auf dem Teller'),
    'roq1': (D + '64061.jpg', '50% 50%', 'Blumenkohl mit Roquefort, Kapern und Quinoa, daneben der Drink'),
    'roq2': (D + '64062.jpg', '50% 50%', 'Derselbe Teller, durch das Glas gesehen'),
    'hok1': (V + '4278.jpg', '50% 50%', 'Hokkaido mit Kürbiskernöl und Haselnuss im Glas'),
    'hok2': (V + '4274.jpg', '50% 50%', 'Das Dessert neben dem Drink'),
    'spag': (D + '64148.jpg', '50% 55%', 'Spaghetti-Eis mit Kiwi und weißer Schokolade'),
    # Tafel (14)
    't01': (D + '5005.jpg', '50% 40%', 'An der Tafel'), 't02': (D + '5022.jpg', '50% 40%', 'An der Tafel'),
    't03': (D + '3842.jpg', '50% 40%', 'An der Tafel'), 't04': (D + '3916.jpg', '50% 40%', 'An der Tafel'),
    't05': (D + '4398.jpg', '50% 40%', 'An der Tafel'), 't06': (D + '36543.jpg', '50% 40%', 'An der Tafel'),
    't07': (D + '36913.jpg', '50% 40%', 'An der Tafel'), 't08': (D + '3901.jpg', '50% 40%', 'An der Tafel'),
    't09': (D + '4004.jpg', '50% 40%', 'An der Tafel'), 't10': (D + '4365.jpg', '50% 40%', 'An der Tafel'),
    't11': (D + '37016.jpg', '50% 40%', 'An der Tafel'), 't12': (D + '64066.jpg', '50% 40%', 'An der Tafel'),
    't13': (D + '5037.jpg', '50% 40%', 'An der Tafel'), 't14': (D + '4462.jpg', '50% 40%', 'An der Tafel'),
    # Familie, Schluss
    'trio': (D + '63873.jpg', '50% 45%', 'Drei aus dem Team vor der Bar'),
    'glaeser': (D + '4026.jpg', '50% 45%', 'Zwei Gläser stoßen an'),
    'barlicht': (D + '3998.jpg', '50% 50%', 'Die Bar bei Nacht von draußen'),
    # Dirty Chicken (Fotos focusonbiz_hannover für Dirty Chicken)
    'dc_burger': (DC + 'ig/2026-06-03_dirtychicken.hannover_DZId0KMoAtq-1.jpg', '50% 50%', 'Ein Dirty-Chicken-Burger'),
    'dc_drink': (DC + 'ig/2026-06-03_dirtychicken.hannover_DZIo4FHIqRR-1.jpg', '50% 50%', 'Chicken und ein Drink'),
    'dc_tisch': (DC + 'ig/2026-06-13_dirtychicken.hannover_DZiug6EoMRr-1.jpg', '50% 50%', 'Ein Tisch voller Dirty Chicken'),
    'dc_team': (DC + 'ig/2026-06-03_dirtychicken.hannover_DZIjZWNCGZT-1.jpg', '50% 50%', 'Die Mannschaft an der Theke'),
    'dc_plakat': (DC + 'ig/2026-06-06_dirtychicken.hannover_DZPYEOJIfVb-1.jpg', '50% 50%', 'Das Pop-up-Plakat von Dirty Chicken'),
    'dc_plakat_ganz': ('website/_zuschnitt/dc-plakat-ganz.jpg', '50% 50%', 'Das Pop-up-Plakat von Dirty Chicken'),   # Zuschnitt aufs Plakat (Oberchef 28.10.2026), Original bleibt
    # Unterseiten
    'beete': (D + '4890.jpg', '50% 55%', 'Rote Bete mit Schaum'),
    'beeteglas': (D + '4893.jpg', '50% 50%', 'Der Drink zum Teller'),
    'karte': (D + '4075.jpg', '50% 50%', 'Die gedruckte Karte am Platz'),
    'kartglas': (D + '3930.jpg', '50% 50%', 'Gläser und Karte auf dem Tisch'),
    'trio2': (V + '63875.jpg', '50% 45%', 'Das Team vor der Bar'),
    # Hero Team (Robert 27.10.2026: Bild D, mit KI auf 4K geschärft, Fassung 2 «Über den Köpfen» aus leute-kopf-wahl.html)
    'team_alle': (DC + 'hochgerechnet/DZIjZWNCGZT-2-4k.png', '50% 44%', 'Das ganze Team hinter der Theke'),
    'w1': (D + '85109.jpg', '50% 40%', 'Am Fenster der Küche'), 'w2': (D + '36911.jpg', '50% 40%', 'Im Service'),
    'w3': (D + '4020.jpg', '50% 40%', 'In der Bar'), 'w4': (D + '4052.jpg', '50% 40%', 'Am Durchgang'),
    'w5': (D + '3866.jpg', '50% 40%', 'An einem Tisch der Bar'), 'w6': (D + '4894.jpg', '50% 40%', 'Service an der Tafel'),
    'w7': (V + '36427.jpg', '50% 50%', 'Mit dem Brenner über dem Teller'),
    'schildnah': (D + '3964.jpg', '50% 50%', 'Das Schild Walk on the Wild Side'),
    'kanister': (V + '3937.jpg', '50% 50%', 'Glasballons mit Sirup und Saft an der Bar'),
    'schaum': (D + '63963.jpg', '50% 50%', 'Schaum aus dem Siphon auf einem Drink'),
    'schaumglas': (D + '4108.jpg', '50% 50%', 'Ein Drink mit Schaum bei Kerzenlicht'),
    'coupe': (D + '36627.jpg', '50% 50%', 'Ein Drink und ein Dessert auf dem Tresen'),
    'baiser': (D + '5271.jpg', '50% 45%', 'Baiser mit Beeren'),
    'kopf_momo': ('website/_zuschnitt/kopf-momo.jpg', '50% 40%', 'Momo'),
    'kopf_derya': ('website/_zuschnitt/kopf-derya.jpg', '50% 40%', 'Derya Ivkin'),
    'kopf_rudi': ('website/_zuschnitt/kopf-rudi.jpg', '50% 40%', 'Rudi Napieraj'),
    'momo_hoch': ('website/_zuschnitt/momo-hoch.jpg', '50% 30%', 'Momo vor der Bar'),
    'pop23': ('_quelle/extern/ig-team/2023-05-18_momo012027_CsZTwYtMoyC-1.jpg', '50% 50%', 'Das Plakat zum ersten Pop-up am 20. Mai 2023'),
    'pl23': ('_quelle/extern/ig-team/2023-09-08_momo012027_Cw8KZ8Lsiiu-1.jpg', '50% 50%', 'Das erste Culinarium-Plakat, September 2023'),
    # Rudis neue Dirty-Chicken-Fotos (Robert 27.10.2026, aus Downloads)
    'dn_burger': (DC + 'vom-kunden-2026-10-27/84673.jpg', '50% 55%', 'Ein Chicken-Sandwich im Papier'),
    'dn_sosse': (DC + 'vom-kunden-2026-10-27/84676.jpg', '50% 55%', 'Grüne Sauce kommt auf die Chicken Chunks'),
    'dn_bar': (DC + 'vom-kunden-2026-10-27/84611.jpg', '50% 50%', 'Ein Drink und Chicken an der Theke'),
    'dn_glas': (DC + 'vom-kunden-2026-10-27/84612.jpg', '50% 50%', 'Ein klarer Drink neben dem Chicken'),
    'dn_karte': (DC + 'vom-kunden-2026-10-27/84626.jpg', '50% 50%', 'Die Karte von Dirty Chicken'),
    'dn_tisch': (DC + 'vom-kunden-2026-10-27/84678.jpg', '50% 50%', 'Ein Tisch voller Dirty Chicken von oben'),
    'dn_drinks': (DC + 'vom-kunden-2026-10-27/84683.jpg', '50% 45%', 'Drinks, Pommes und Chicken auf dem Tisch'),
    'dn_salat': (DC + 'vom-kunden-2026-10-27/84607.jpg', '50% 50%', 'Krautsalat, Pommes und ein Longdrink'),
    'dn_team': (DC + 'vom-kunden-2026-10-27/84558.jpg', '50% 40%', 'Das Team hinter der Theke'),
    'dc_zeichen': (DC + 'logo/original/dirtychicken-logo-lila-1440.png', '50% 50%', 'Das Logo von Dirty Chicken: das D mit Hühnerfuß über dem Schriftzug, Sandwiches & More'),   # Original von Rudi (28.10.2026), vorher das Instagram-Profilbild
    'dc_team2': (DC + 'ig/2026-06-03_dirtychicken.hannover_DZIjZWNCGZT-2.jpg', '50% 50%', 'Die Mannschaft an der Theke'),
    'glasnacht': (V + 'drive-arw-vorschau/5408.jpg', '50% 50%', 'Ein Drink im Stielglas auf dunklem Tisch'),   # Schluss Alle Abende, gross genug für volle Breite (27.10.2026)
    'flaschen': (D + '3956.jpg', '50% 50%', 'Flaschen an der Bar'),
    'loch': (D + '4029.jpg', '50% 50%', 'Durch die Wand auf einen Tisch mit Kerzen'),
    'lachen': (D + '3831.jpg', '50% 35%', 'Zwei Gäste lachen an der Bar'),
    # Weitere Teller und Drinks aus Rudis Drive (bisher ungenutzt, 26.10.2026)
    'r01': (D + '4238.jpg', '50% 50%', 'Blumenkohl mit Kürbis auf weißem Teller'),
    'r02': (D + '4298.jpg', '50% 50%', 'Ein Teller mit oranger Sauce auf dunklem Tisch'),
    'r03': (D + '4343.jpg', '50% 50%', 'Ein Teller und ein Glas Weißwein'),
    'r04': (D + '4474.jpg', '50% 50%', 'Ein Dessert im Glas mit Deckel'),
    'r05': (D + '4582.jpg', '50% 50%', 'Ein Teller von oben, daneben die Karte'),
    'r06': (D + '5041.jpg', '50% 50%', 'Ein Gast am Teller'),
    'r07': (D + '5045.jpg', '50% 50%', 'Ein Teller mit Röstzwiebeln'),
    'r08': (D + '5098.jpg', '50% 50%', 'Zwei Knödel mit Kräutern'),
    'r09': (D + '5146.jpg', '50% 50%', 'Ein Teller auf Porzellan mit grünem Rand'),
    'r10': (D + '64059.jpg', '50% 50%', 'Ein Teller und ein Glas von oben'),
    'r11': (D + '3983.jpg', '50% 50%', 'Ein gebackenes Dessert'),
    'd1': (D + '4843.jpg', '50% 50%', 'Zwei Drinks auf dem Tisch'),
    'd2': (D + '4921.jpg', '50% 50%', 'Ein heller Drink mit Minze'),
    'd3': (D + '63740.jpg', '50% 50%', 'Ein Drink wird durch das Sieb gegossen'),
    'barneg': (D + '5062.jpg', '50% 50%', 'Die Rückwand der Bar mit dem Negroni-Schriftzug'),
    # Instagram der Bar Walk on the Wild Side (das Haus von Culinarium; Freigabe der Bar offen, nur lokal)
    'ws00': (WS + '2023-11-09_walkonthewildside_hannover_CzbxDQMMKQ3-1.jpg', '50% 50%', 'Die Bar am Abend, Kerze auf dem Tisch'),
    'ws01': (WS + '2023-11-12_walkonthewildside_hannover_CzjTFZSsFa5-1.jpg', '50% 50%', 'Hinter der Theke unter dem Negroni-Schriftzug'),
    'ws02': (WS + '2023-12-07_walkonthewildside_hannover_C0j1thbsh_y-1.jpg', '50% 50%', 'Die Karte zum Valentinstag bei Kerzenlicht'),
    'ws03': (WS + '2024-01-01_walkonthewildside_hannover_C1khavJsCR2-1.jpg', '50% 50%', 'Ein roter Drink vor der vollen Bar'),
    'ws05': (WS + '2024-02-26_walkonthewildside_hannover_C30ngEIrNQM-1.jpg', '50% 50%', 'Gastschicht: zwei Bartender an der Theke'),
    'ws07': (WS + '2024-03-08_walkonthewildside_hannover_C4QsQhqM2s1-1.jpg', '50% 50%', 'An der Theke, ein Drink und ein Fächer'),
    'ws09': (WS + '2024-03-26_walkonthewildside_hannover_C4-zC6JIO_Y-1.jpg', '50% 50%', 'Konzert in der Bar'),
    'ws10': (WS + '2024-04-10_walkonthewildside_hannover_C5ljExNs6kE-1.jpg', '50% 50%', 'Gast hinter der Bar'),
    'ws11': (WS + '2024-05-16_walkonthewildside_hannover_C7Bco_FsO1O-1.jpg', '50% 50%', 'Gastschicht'),
    'ws12': (WS + '2024-05-17_walkonthewildside_hannover_C7D_5dfsn1i-1.jpg', '50% 50%', 'Ein Drink wird eingeschenkt'),
    'ws13': (WS + '2024-05-17_walkonthewildside_hannover_C7D_5dfsn1i-2.jpg', '50% 50%', 'Die Rückwand der Bar mit Negroni-Schriftzug'),
    'ws14': (WS + '2024-06-07_walkonthewildside_hannover_C76ERk_oJal-1.jpg', '50% 50%', 'Duo im Konzert'),
    'ws15': (WS + '2024-06-07_walkonthewildside_hannover_C76ERk_oJal-2.jpg', '50% 50%', 'Gitarre beim Konzert'),
    'ws16': (WS + '2024-06-07_walkonthewildside_hannover_C76ERk_oJal-3.jpg', '50% 50%', 'Sängerin beim Konzert'),
    'ws19': (WS + '2024-08-25_walkonthewildside_hannover_C_GTXkOsQLH-1.jpg', '50% 50%', 'Konzert mit Gitarre'),
    'ws20': (WS + '2024-10-14_walkonthewildside_hannover_DBHXxmYM0vY-1.jpg', '50% 50%', 'Gast-Bartender mit Drink'),
    'ws21': (WS + '2024-11-10_walkonthewildside_hannover_DCMDSnpIOHt-1.jpg', '50% 50%', 'Plakat Anniversary Night, 30. November 2024'),
    'ws25': (WS + '2024-11-21_walkonthewildside_hannover_DCpKG5ossk4-1.jpg', '50% 50%', 'Plakat Silvester-Frühshoppen'),
    'ws28': (WS + '2024-12-18_walkonthewildside_hannover_DDuvG1Rs7kq-1.jpg', '50% 50%', 'Ein Glas vor der vollen Bar'),
    'ws29': (WS + '2025-01-15_walkonthewildside_hannover_DE1rV7YML5A-3.jpg', '50% 50%', 'Gläser beim Klären'),
    'ws30': (WS + '2025-01-15_walkonthewildside_hannover_DE1rV7YML5A-4.jpg', '50% 50%', 'Kleine Teller zum Teilen'),
    'ws31': (WS + '2025-01-15_walkonthewildside_hannover_DE1rV7YML5A-5.jpg', '50% 50%', 'Ein Drink im Gegenlicht'),
    'ws32': (WS + '2025-04-13_walkonthewildside_hannover_DIZXgSVMXWs-1.jpg', '50% 50%', 'Plakat Tanz in den Mai'),
    'ws33': (WS + '2025-06-16_walkonthewildside_hannover_DK-GT7TITWD-1.jpg', '50% 50%', 'Flaschen auf dem Tresen'),
    'ws35': (WS + '2025-06-16_walkonthewildside_hannover_DK-GT7TITWD-4.jpg', '50% 50%', 'Das Schild Wild Side bei Nacht'),
    'ws37': (WS + '2025-08-31_walkonthewildside_hannover_DOCMXG-iC59-1.jpg', '50% 50%', 'Plakat SESSION Sip & Sounds, 6. September'),
    'ws39': (WS + '2025-10-02_walkonthewildside_hannover_DPTyybwiFIB-1.jpg', '50% 50%', 'Plakat Two Years, 5. Dezember 2025'),
    'ws40': (WS + '2025-11-17_walkonthewildside_hannover_DRK_iVDiChc-1.jpg', '50% 50%', 'Plakat SESSION Sip & Sounds, 22. November'),
    'ws41': (WS + '2025-11-25_walkonthewildside_hannover_DRfZEXXiHLj-1.jpg', '50% 50%', 'Plakat Silvester-Frühshoppen'),
    'ws42': (WS + '2026-01-14_walkonthewildside_hannover_DTf-jwUCObe-1.jpg', '50% 50%', 'Plakat SESSION Sip & Sounds, 24. Januar'),
    'ws43': (WS + '2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-1.jpg', '50% 50%', 'Wild Side x Rudi in Love'),
    'ws44': (WS + '2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-2.jpg', '50% 50%', 'Karte Drunk in Love'),
    'ws45': (WS + '2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-3.jpg', '50% 50%', 'Karte Dishes in Love'),
    'ws47': (WS + '2026-03-13_walkonthewildside_hannover_DV1fl7MCO3q-1.jpg', '50% 50%', 'Plakat SESSION Sip & Sounds, 21. März'),
    'ws48': (WS + '2026-03-16_walkonthewildside_hannover_DV9QHR0iE4V-1.jpg', '50% 50%', 'Plakat Mystic Mella'),
    'ws49': (WS + '2026-05-11_walkonthewildside_hannover_DYNDzMgIR7M-1.jpg', '50% 50%', 'Plakat SESSION Sip & Sounds, 16. Mai'),
    'ws50': (WS + '2026-09-02_walkonthewildside_hannover_DcxmPV3oZbA-1.jpg', '50% 50%', 'Plakat SESSION Sip & Sounds, 5. September'),
    'ws51': (WS + '2026-09-29_walkonthewildside_hannover_Dd3Vx4lolo3-1.jpg', '50% 50%', 'Plakat SESSION Sip & Sounds, 3. Oktober'),
    'ws52': (WS + '2026-10-13_walkonthewildside_hannover_DecaAh8oxYw-1.jpg', '50% 50%', 'Plakat SESSION Sip & Sounds, 17. Oktober'),
    'fensterdraussen': (D + '4032.jpg', '50% 50%', 'Von draußen durchs Fenster der Bar'),
    'plakatwand': ('website/_zuschnitt/plakatwand.jpg', '50% 50%', 'Alle Culinarium-Plakate seit dem ersten Pop-up an einer dunklen Wand, der letzte Platz ist noch frei'),   # Schluss Alle Abende, aus plakatwand.py (27.10.2026)
}

# Plakate seit 2023 (Beitragstexte in _quelle/extern/ig/beitraege.md, je Eintrag die Beitrags-ID)
ABENDE = [
    # (jahr, daten, zusatz, preis, plakat-ID oder None, mit)
    ('2023', 'Fr 15. und Sa 16. September', 'mit Live-Act, 15 Plätze', '80,00 EUR', 'CxNkFWTIvL2', 'BY MOMO X CHRISTOPH'),
    ('2023', 'Fr 22. und Sa 23. September', '', '59,00 EUR', None, 'BY MOMO X CHRISTOPH'),
    ('2023', 'Sa 21. Oktober', '20 Plätze', '59,00 EUR', 'CyT32RTMB4d', 'BY MOMO X CHRISTOPH'),
    ('2023', 'Fr 17. und Sa 18. November', '15 Plätze', '59,00 EUR', 'CzMcqNcMCqG', 'BY MOMO X CHRISTOPH'),
    ('2023', 'So 31. Dezember', 'Silvester Edition', '109,00 EUR', 'C0w6iuCMcnF', 'BY MOMO X CHRISTOPH'),
    ('2024', 'Fr 26. und Sa 27. Januar', '12 Plätze', '69,00 EUR', 'C17kqAXLfs_', 'BY MOMO X CHRISTOPH'),
    ('2024', 'Fr 26. und Sa 27. April', '12 Plätze', '69,00 EUR', 'C56bJeds8PF', 'BY MOMO'),
    ('2024', 'Fr 19. und Sa 20. Juli', '12 Plätze', '69,00 EUR', 'C8cgYVSouVT', 'BY MOMO X RUDI'),
    ('2024', 'Fr 29. und Sa 30. November', '', '69,00 EUR', 'DCCf-ikoaGs', 'BY MOMO X RUDI'),
    ('2025', 'Fr 21. und Sa 22. Februar', '14 Plätze', '79,00 EUR', 'DFqbLG2s_dc', 'BY MOMO X RUDI'),
    ('2025', 'Fr 13. und Sa 14. Juni', '', '79,00 EUR', 'DJw8OqGMY1G', 'BY MOMO X RUDI'),
    ('2025', 'Fr 14. und Sa 15. November', 'Freitag ausverkauft', '79,00 EUR', 'DPwlqcfiKcA', 'BY MOMO X RUDI'),
    ('2026', 'Fr 27. und Sa 28. März', '', '89,00 EUR', 'DVjkofijp6R', 'BY MOMO X RUDI'),
    ('2026', 'Fr 25. und Sa 26. September', 'ausgebucht', '89,00 EUR', 'DbYnkdkjrNy', 'BY MOMO X RUDI'),
]
# Bilder je Abend (abende_info.py, Robert 27.10.2026): Rückseiten der Plakate, Danke-Beiträge, Highlights, Rudis Beiträge
import abende_info as _AI
for _key, _inf in _AI.INFO.items():
    for _n, _q in enumerate(_inf['bilder']):
        BILD['ab_%s_%d' % (_key.replace('-', '_'), _n)] = (_q, '50% 50%', 'Culinarium, Bild zum Abend')
    for _n, (_dat, _ger, _q) in enumerate(_inf['rudi']):
        if _q:
            BILD['abr_%s_%d' % (_key.replace('-', '_'), _n)] = (_q, '50% 50%', _ger)
for _j, _d, _z, _p, _id, _m in ABENDE:
    if _id:
        _f = [f for f in os.listdir(os.path.join(PROJ, IG)) if _id in f and f.endswith('-1.jpg')][0]
        BILD['p_' + _id] = (IG + _f, '50% 50%', 'Plakat Culinarium, %s %s' % (_d, _j))

# KI-geschärfte Quellen (culinarium-bilder, 28.10.2026): Higgsfield Upscale 4K, jedes Bild gegen das Original geprüft,
# Schrift auf Karten und Etiketten bleibt Original. Gründe, Vorher/Nachher: _quelle/ki/geschaerft/LIEFERUNG.md
# Greift nur, solange der Schlüssel noch das alte Original zeigt. Zurück: diesen Block löschen.
GESCHAERFT = {
    'barlicht': ('_quelle/vom-kunden/drive/3998.jpg', '_quelle/ki/geschaerft/3998-geschaerft.jpg'),
    'dn_salat': ('_quelle/dirty-chicken/vom-kunden-2026-10-27/84607.jpg', '_quelle/ki/geschaerft/84607-geschaerft.jpg'),
    'karte': ('_quelle/vom-kunden/drive/4075.jpg', '_quelle/ki/geschaerft/4075-geschaerft.jpg'),
    'lachen': ('_quelle/vom-kunden/drive/3831.jpg', '_quelle/ki/geschaerft/3831-geschaerft.jpg'),
    'loch': ('_quelle/vom-kunden/drive/4029.jpg', '_quelle/ki/geschaerft/4029-geschaerft.jpg'),
    'ws09': ('_quelle/walk-on-the-wild-side/ig/2024-03-26_walkonthewildside_hannover_C4-zC6JIO_Y-1.jpg', '_quelle/ki/geschaerft/2024-03-26_walkonthewildside_hannover_C4-zC6JIO_Y-1-geschaerft.jpg'),
    'ws12': ('_quelle/walk-on-the-wild-side/ig/2024-05-17_walkonthewildside_hannover_C7D_5dfsn1i-1.jpg', '_quelle/ki/geschaerft/2024-05-17_walkonthewildside_hannover_C7D_5dfsn1i-1-geschaerft.jpg'),
    'ab_C17kqAXLfs__0': ('_quelle/extern/ig-zuschnitt-2/2024-01-29_culinarium_hannover_C2sFkpSscHP-1.jpg', '_quelle/ki/geschaerft/2024-01-29_culinarium_hannover_C2sFkpSscHP-1-geschaerft.jpg'),
    'pass': ('_quelle/vom-kunden/drive/36567.jpg', '_quelle/ki/geschaerft/36567-geschaerft.jpg'),
    'schildnacht': ('_quelle/vom-kunden/drive/4096.jpg', '_quelle/ki/geschaerft/4096-geschaerft.jpg'),
    'tafelleer': ('_quelle/vom-kunden/drive/4972.jpg', '_quelle/ki/geschaerft/4972-geschaerft.jpg'),
    'ab_C56bJeds8PF_0': ('_quelle/extern/ig-zuschnitt-2/2024-04-27_highlight-8299-03.jpg', '_quelle/ki/geschaerft/2024-04-27_highlight-8299-03-geschaerft.jpg'),
    'glaeser': ('_quelle/vom-kunden/drive/4026.jpg', '_quelle/ki/geschaerft/4026-geschaerft.jpg'),
    'kartglas': ('_quelle/vom-kunden/drive/3930.jpg', '_quelle/ki/geschaerft/3930-geschaerft.jpg'),
    'ab_CxNkFWTIvL2_1': ('_quelle/extern/ig/2023-09-16_culinarium_hannover_CxQg56AItz6-4.jpg', '_quelle/ki/geschaerft/2023-09-16_culinarium_hannover_CxQg56AItz6-4-geschaerft.jpg'),
    'ab_DJw8OqGMY1G_2': ('_quelle/extern/ig-zuschnitt-2/2025-06-15_highlight-6684-10.jpg', '_quelle/ki/geschaerft/2025-06-15_highlight-6684-10-geschaerft.jpg'),
    'theke2': ('_quelle/vom-kunden/drive/4019.jpg', '_quelle/ki/geschaerft/4019-geschaerft.jpg'),
    'r04': ('_quelle/vom-kunden/drive/4474.jpg', '_quelle/ki/geschaerft/4474-geschaerft.jpg'),
    'schaumglas': ('_quelle/vom-kunden/drive/4108.jpg', '_quelle/ki/geschaerft/4108-geschaerft.jpg'),
    't08': ('_quelle/vom-kunden/drive/3901.jpg', '_quelle/ki/geschaerft/3901-geschaerft.jpg'),
    'ab_DFqbLG2s_dc_0': ('_quelle/extern/ig-zuschnitt-2/2025-02-22_highlight-4865-02.jpg', '_quelle/ki/geschaerft/2025-02-22_highlight-4865-02-geschaerft.jpg'),
    'abr_DbYnkdkjrNy_0': ('_quelle/extern/ig-team/2026-10-23_rudi__san_De1pn9ttMoX-1.jpg', '_quelle/ki/geschaerft/2026-10-23_rudi__san_De1pn9ttMoX-1-geschaerft.jpg'),
    'theke': ('_quelle/vom-kunden/drive/3925.jpg', '_quelle/ki/geschaerft/3925-geschaerft.jpg'),
}
for _k, (_alt, _neu) in GESCHAERFT.items():
    if _k in BILD and BILD[_k][0] == _alt:
        BILD[_k] = (_neu,) + BILD[_k][1:]

# Rudis Zeilen: Wortlaut aus _quelle/extern/ig-team/beitraege.md, Teller am Bild des Beitrags erkannt
ZEILEN = [
    (['LAUCH /', 'BLUMENKOHL /', 'CHIPOTLE'], ['lauch'], 'DLSA60BMwiG'),
    (['BLUMENKOHL /', 'ROQUEFORT /', 'KAPERN /', 'QUINOA'], ['roq1', 'roq2'], 'DW4V45ujR0B'),   # Beitrag schreibt «ROGUEFORT»
    (['HOKKAIDO /', 'KÜRBISKERNÖL /', 'HASELNUSS'], ['hok2', 'hok1'], 'C-OFq0msPA7'),
    (['SPAGHETTI-EIS /', 'KIWI /', 'WEISSE', 'SCHOKOLADE'], ['spag'], 'DZIlJu-N0w4'),
]

FILM = {'familie': DC + 'video/2026-06-03_dirtychicken.hannover_DZIjZWNCGZT-3.mp4',
        'opening': DC + 'video/2026-06-06_dirtychicken.hannover_DZPYEOJIfVb-1.mp4'}

STUFEN = (640, 1000, 1600, 2400)


def bildstufen(q):
    im = Image.open(os.path.join(PROJ, q))
    return [w for w in STUFEN if w <= im.width] or [im.width]


def bilder():
    os.makedirs(os.path.join(A, 'bild'), exist_ok=True)
    meta = {}
    mpfad = os.path.join(A, 'bild', 'meta.json')
    alt = json.load(open(mpfad)) if os.path.exists(mpfad) else {}
    for k, (q, _p, _a) in BILD.items():
        st = os.stat(os.path.join(PROJ, q))
        sig = '%s|%d|%d' % (q, st.st_size, int(st.st_mtime))
        if alt.get(k, {}).get('sig') == sig and all(os.path.exists(os.path.join(A, 'bild', '%s-%d.webp' % (k, w))) for w in alt[k]['stufen']):
            meta[k] = alt[k]
            continue
        im = Image.open(os.path.join(PROJ, q))
        im = ImageOps.exif_transpose(im).convert('RGB')
        stufen = [w for w in STUFEN if w <= im.width] or [im.width]
        for w in stufen:
            x = im if im.width == w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            x.save(os.path.join(A, 'bild', '%s-%d.webp' % (k, w)), 'WEBP', quality=80, method=6)
        kl = im.copy(); kl.thumbnail((20, 20))
        buf = io.BytesIO(); kl.save(buf, 'JPEG', quality=55)
        meta[k] = {'sig': sig, 'w': im.width, 'h': im.height, 'stufen': stufen,
                   'lq': 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()}
        print('Bild', k, im.width, im.height)
    json.dump(meta, open(mpfad, 'w'))
    return meta


def akzent(k):
    """Akzentfarbe eines Plakats: gesättigtster häufiger Ton der Illustration (oberes Drittel bis Band)."""
    im = Image.open(os.path.join(PROJ, BILD[k][0])).convert('RGB')
    w, h = im.size
    x = im.crop((int(w * .06), int(h * .06), int(w * .94), int(h * .68))).resize((120, 120))
    q = x.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:24]
    cnt = sorted(q.getcolors(), reverse=True)
    best, bs = (58, 56, 69), -1
    for n, i in cnt:
        r, g, b = pal[i * 3:i * 3 + 3]
        mx, mn = max(r, g, b), min(r, g, b)
        sat = (mx - mn) / (mx or 1)
        sc = sat * (n ** .5) * (1 if 50 < mx < 245 else .3)
        if sc > bs:
            bs, best = sc, (r, g, b)
    return '#%02x%02x%02x' % best


def filme():
    os.makedirs(os.path.join(A, 'film'), exist_ok=True)
    for k, q in FILM.items():
        z = os.path.join(A, 'film', k + '.mp4')
        if not os.path.exists(z):
            # ohne Ton, schneller Start im Browser
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(PROJ, q), '-an', '-c:v', 'libx264', '-crf', '27', '-maxrate', '1600k', '-bufsize', '3200k',
                            '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', z], check=True)
        p = os.path.join(A, 'film', k + '.webp')
        if not os.path.exists(p):
            j = p[:-5] + '.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '6' if k == 'opening' else '0.5', '-i', z, '-frames:v', '1', '-q:v', '2', j], check=True)
            Image.open(j).save(p, 'WEBP', quality=82); os.remove(j)


# Culinarium-Logo: Original-Vektor von Rudi (28.10.2026), aus dem PDF gelöst; vorher vom Plakat nachgezogen
LOGO = os.path.join(PROJ, '_quelle/logo/original/culinarium-logo-original.svg')
_lg = open(LOGO).read()
LOGO_WM = re.search(r'data-wm="([^"]+)"', _lg).group(1).split()
LOGO_ZEILE = re.search(r'data-zeile="([^"]+)"', _lg).group(1).split()
LOGO_VB = re.search(r'viewBox="([^"]+)"', _lg).group(1)
DC_D = os.path.join(PROJ, '_quelle/dirty-chicken/logo/original/dirtychicken-d-lila-original.png')   # das D, Original von Rudi (28.10.2026)


def zeichen():
    os.makedirs(os.path.join(A, 'zeichen'), exist_ok=True)
    d = {k: re.search(r'<path id="%s"[^>]* d="([^"]+)"' % k, _lg).group(1) for k in ('wm', 'zeile')}
    syms = ['<symbol id="wm" viewBox="%s"><path fill="currentColor" d="%s"/></symbol>' % (' '.join(LOGO_WM), d['wm']),
            '<symbol id="wmz" viewBox="%s"><path fill="currentColor" d="%s%s"/></symbol>' % (LOGO_VB, d['wm'], d['zeile']),
            '<symbol id="zeile" viewBox="%s"><path fill="currentColor" d="%s"/></symbol>' % (' '.join(LOGO_ZEILE), d['zeile'])]
    open(os.path.join(A, 'zeichen', 'marke.svg'), 'w').write(
        '<svg xmlns="http://www.w3.org/2000/svg">' + ''.join(syms) + '</svg>')
    Image.open(DC_D).save(os.path.join(A, 'zeichen', 'dc-original.webp'), 'WEBP', quality=90, method=6)
    # Wild-Side-Schild und das D von Dirty Chicken (beide nachgezogen, nicht die Originale), für den Footer
    # Wild Side: das Schild aus der Website der Bar (Walk on the Wild Side Hannover/website, Leiste und Hero), rote Form #F0323F (--rot dort),
    # «WILD / SIDE» ausgespart (Robert/Oberchef 31.10.2026; das weisse Quadrat von 26217 war falsch, Stand davor bau.py.vor-logo-schild-rot-2026-10-31)
    haus = []
    for sid, f, vb in (('ws', '_quelle/walk-on-the-wild-side/logo/wildside-logo-nachgezogen.svg', '0 0 1296 1600'),
                       ('dc', '_quelle/dirty-chicken/logo/dirtychicken-zeichen-nachgezogen.svg', '214 197 652 712')):
        s = open(os.path.join(PROJ, f)).read()
        g = re.search(r'<g transform="([^"]+)"', s).group(1)
        pf = ''.join('<path d="%s"/>' % ' '.join(d.split()) for d in re.findall(r'<path d="([^"]+)"', s))
        haus.append('<symbol id="%s" viewBox="%s"><g transform="%s"%s>%s</g></symbol>' % (sid, vb, g, ' fill="#F0323F"' if sid == 'ws' else '', pf))
    open(os.path.join(A, 'zeichen', 'haus.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg">' + ''.join(haus) + '</svg>')


META = {}


def srcset(k):
    m = META[k]
    return ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in m['stufen'])


PLAKAT_GANZ = {'pop23', 'pl23', 'dc_plakat', 'dc_plakat_ganz'}   # Plakate, die in fremden Seitenverhältnissen stehen


def foto(k, cls='', sizes='50vw', eager=False, auf=True, pos=None, extra='', ratio=False):
    """Foto im Rahmen: deckend, kommt von unten, zoomt in den Rahmen. Abbild des Fotos als Grund, nie ein grauer Kasten."""
    m = META[k]
    q, p, alt = BILD[k]
    pos = pos or p
    if k in PLAKAT_GANZ:   # Plakate nie anschneiden: ganz, mit Innenrand (Oberchef/Robert 28.10.2026, «komische Cuts»)
        cls = (cls + ' plakat-ganz').strip()
    klein = 'assets/bild/%s-%d.webp?v=%s' % (k, m['stufen'][0], VERSION)
    if eager:
        im = '<img src="%s" srcset="%s" sizes="%s" alt="%s" fetchpriority="high" decoding="async" style="object-position:%s">' % (
            klein, srcset(k), sizes, E(alt), pos)
    else:
        im = '<img data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" style="object-position:%s">' % (
            srcset(k), sizes, E(alt), pos)
    st = '--lq:url(%s)' % m['lq'] + (';aspect-ratio:%d/%d;--r:%.4f' % (m['w'], m['h'], m['w'] / m['h']) if ratio else '')
    if 'style="' in extra:
        st += ';' + re.search(r'style="([^"]*)"', extra).group(1)
        extra = re.sub(r'style="[^"]*"', '', extra)
    return '<figure class="foto%s%s" style="%s" %s>%s</figure>' % (
        ' auf' if auf else '', (' ' + cls) if cls else '', st, extra, im)


def zl(zeilen, tag='h2', cls='', i0=0):
    """Überschrift, die zeilenweise aus dem Schlitz kommt."""
    t = ' '.join(re.sub('<[^>]+>', '', z) for z in zeilen)
    if 'rudi' in cls:
        zeilen = [z.replace(' /', '&#160;<i class="sl">/</i>') for z in zeilen]
    inner = ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i0 + i, z) for i, z in enumerate(zeilen))
    return '<%s class="zl auf%s" aria-label="%s">%s</%s>' % (tag, (' ' + cls) if cls else '', E(t), inner, tag)


def sw(text, tag='p', cls='', i=0):
    return '<%s class="sw auf%s" style="--i:%d">%s</%s>' % (tag, (' ' + cls) if cls else '', i, text, tag)


PFEIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def knopf(text, href, cls='', neu=False):
    t = E(text).replace('i', '<em class="ki">i</em>')
    return '<a class="knopf%s" href="%s"%s aria-label="%s"><span>%s</span><i>%s</i></a>' % (
        (' ' + cls) if cls else '', href, ' target="_blank" rel="noopener"' if neu else '', E(text), t, PFEIL)


def marke(sym='wm', cls=''):
    vb = {'wm': '0 0 %s %s' % tuple(LOGO_WM[2:]), 'wmz': LOGO_VB, 'zeile': '0 0 %s %s' % tuple(LOGO_ZEILE[2:])}[sym]
    return '<svg class="marke %s" viewBox="%s" role="img" aria-label="Culinarium"><use href="assets/zeichen/marke.svg?v=%s#%s"/></svg>' % (
        cls, vb, VERSION, sym)


# ---------------------------------------------------------------- Rahmen
# Dach Walk on the Wild Side (Rudi 26.10.2026: «das Hauptgeschäft»), Culinarium die Abende, Dirty Chicken das Pop-up
# Robert 26.10.2026: «wir bauen fürs Kulinarium»; das Wild Side ist das Haus, Dirty Chicken nicht vorn
NAV = [('abend.html', 'Der Abend'), ('abende.html', 'Alle Abende'), ('bar.html', 'Das Haus'),
       ('leute.html', 'Team'), ('weg.html', 'Der Weg'), ('dirty-chicken.html', 'Dirty Chicken')]


def kopf(titel, beschreibung, seite, ton='nacht'):
    # Mittelachse (Robert 26.10.2026: «5 aber die sachen um die mittelachse mehr zentriert»): Marke in der Mitte, je drei Seiten eng daneben
    SEITE_AKTUELL[0] = seite
    # Sprachschalter DE/EN (29.10.2026, Oberchef: englische Fassung unter en/, Bau website/bau_en.py): rechts in der Leiste, im Menü und im Fuss
    # Robert 29.10.2026: «den Sprachen-Button unten links, nicht oben mit in die Leiste»: Knopf des Hauses, fest unten links, Gegenstück zum Chat-Knopf
    # unten rechts (anfrage.css .cc-knopf: gleiche Höhe, gleicher Rand, geht mit der Leiste; culinarium.js «Sprachknopf»). Am Handy nur der Kreis.
    sprache = ('<a class="knopf sprache-knopf" href="en/%s" hreflang="en" lang="en" aria-label="English version">'
               '<span>Engl<em class="ki">i</em>sh</span><i><span>EN</span></i></a>' % seite)
    nav = ['<nav class="leiste-nav %s" aria-label="%s">%s</nav>' % (cls, label, ''.join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == seite else '', E(t)) for h, t in teil))
        for cls, label, teil in (('links', 'Seiten', NAV[:3]), ('rechts', 'Weitere Seiten', NAV[3:]))]
    de_url = ADRESSE + ('' if seite == 'index.html' else seite)
    en_url = ADRESSE + 'en/' + ('' if seite == 'index.html' else seite)
    return '''<!doctype html>
<html lang="de" class="vor">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>%s</title>
<meta name="description" content="%s">
<link rel="alternate" hreflang="de" href="%s">
<link rel="alternate" hreflang="en" href="%s">
<link rel="alternate" hreflang="x-default" href="%s">
<meta name="theme-color" content="#16151A">
<link rel="preload" href="assets/schrift/fraunces-weich.woff2" as="font" type="font/woff2" crossorigin fetchpriority="low">
<link rel="preload" href="assets/schrift/instrument.woff2" as="font" type="font/woff2" crossorigin fetchpriority="low">
<link rel="stylesheet" href="assets/culinarium.css?v=%s">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%%3E%%3Crect width='64' height='64' rx='14' fill='%%2316151A'/%%3E%%3Ctext x='32' y='45' font-family='Georgia' font-size='38' text-anchor='middle' fill='%%23EF7649'%%3EC%%3C/text%%3E%%3C/svg%%3E">
<script>document.documentElement.classList.add('js');try{if(matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('ruhig')}catch(e){}addEventListener('DOMContentLoaded',function(){if(!window.culinariumAlles)document.documentElement.classList.remove('js')})</script>
</head>
<body data-ton="%s">
<a class="sprungmarke" href="#inhalt">Zum Inhalt</a>
<header class="leiste%s" id="leiste">
  %s
  <a class="leiste-marke" href="index.html" aria-label="Culinarium, zur Startseite">%s</a>
  %s
  <a class="leiste-knopf" href="abend.html#warteliste"><span>Warteliste</span></a>
  <button class="leiste-menue" type="button" aria-expanded="false" aria-controls="menue"><span>Menü</span></button>
</header>
<div class="menue" id="menue" hidden>
  <nav aria-label="Seiten">%s<a href="index.html">Startseite</a><a class="menue-sprache" href="en/%s" hreflang="en" lang="en">English</a></nav>
  <p class="menue-ort">Walk on the Wild Side · Haasemannstraße 13 · 30449 Hannover</p>
</div>
%s
<main id="inhalt">
''' % (E(titel), E(beschreibung), de_url, en_url, de_url, VERSION, ton, ' weg' if seite == 'index.html' else '', nav[0], marke('wm'), nav[1],
       ''.join('<a href="%s">%s</a>' % (h, E(t)) for h, t in NAV), seite, sprache)


def zeichen_haus(sid, cls=''):
    """Zeichen der Bar (ws) oder des Pop-ups (dc). Aussen nie verschieben, der Ausschnitt steckt im Symbol (Safari verschiebt sonst doppelt)."""
    vb, name = {'ws': ('0 0 1296 1600', 'Walk on the Wild Side'), 'dc': ('0 0 652 712', 'Dirty Chicken')}[sid]
    if sid == 'dc':
        # Original-D von Rudi (28.10.2026) mit seiner Farbe und Struktur, deshalb als Bild statt als einfarbiges Symbol
        # lazy (30.10.2026, Tempo): 156 KB, stand im Fuss jeder Seite und lud sonst gleichzeitig mit dem ersten Bild
        w, h = Image.open(DC_D).size
        return '<img class="fu-zn fu-zn-%s %s" src="assets/zeichen/dc-original.webp?v=%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async">' % (
            sid, cls, VERSION, w, h, name)
    return '<svg class="fu-zn fu-zn-%s %s" viewBox="%s" role="img" aria-label="%s"><use href="assets/zeichen/haus.svg?v=%s#%s"/></svg>' % (
        sid, cls, vb, name, VERSION, sid)


def fu_bild(k, sizes, pos):
    m = META[k]
    _q, _p, alt = BILD[k]
    return '<figure class="fu-bild" style="--lq:url(%s)"><img data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" style="object-position:%s"></figure>' % (
        m['lq'], srcset(k), sizes, E(alt), pos)


# Warteliste im Fuss als Höhepunkt: Ticket mit Einkerbungen, die Tafel mit vierzehn Plätzen, E-Mail direkt eintragen (Robert 27.10.2026)
WARTELISTE_FUSS = ('<div class="fu-wl2 auf"><div class="fu-wl2-stub"><b>14</b><span>Plätze</span></div>'
    '<div class="fu-wl2-text"><p class="fu-wl2-k zl auf"><span class="z"><span style="--i:1">Warteliste</span></span></p><p class="fu-wl2-t zl auf"><span class="z"><span style="--i:2">Dein Platz am nächsten Abend.</span></span></p></div>'
    '<form class="fu-wl-f fu-wl2-f" action="abend.html#warteliste" novalidate><label class="fu-wl2-feld"><span class="vh">Deine E-Mail</span>'
    '<input type="email" name="mail" autocomplete="email" placeholder="Deine E-Mail"></label>'
    '<button class="knopf" type="submit"><span>Vormerken</span><i>%s</i></button></form></div>') % PFEIL


def fuss(extra_js=''):
    """Footer «Mit Fotos» (Robert 26.10.2026: aus den 15 Fassungen von «Das ×» Nummer 10).
    Drei Zeichen nach Gewicht, verbunden durch das x der Plakate (aus + wird ×), darunter je Zeichen sein Bild,
    darunter drei gleich gebaute Spalten auf einem gemeinsamen Zeilenraster. Fakten wie im alten Footer und im Charakterblatt."""
    nav = ''.join('<a href="%s">%s</a>' % (h, E(t)) for h, t in NAV)
    def spalte(n, etikett, name, satz, zeilen, tat, ncls='fu-name'):
        dl = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % z for z in zeilen)
        # Auftritt wie auf der ganzen Seite (Robert 27.10.2026): Etikett und Name aus dem Schlitz, Text, Zeiten und Link schweben nach, Spalte für Spalte versetzt
        i = (n - 1) * 2
        return ('<div class="fu-s%d"><p class="fu-k zl auf"><span class="z"><span style="--i:%d">%s</span></span></p>'
                '<div class="fu-kopf"><p class="%s zl auf"><span class="z"><span style="--i:%d">%s</span></span></p><p class="fu-text sw auf" style="--i:%d">%s</p></div>'
                '<dl class="fu-zeiten sw auf" style="--i:%d">%s</dl><div class="fu-tat sw auf" style="--i:%d">%s</div></div>') % (
            n, i, etikett, ncls, i + 1, name, i + 2, satz, i + 3, dl, i + 4, tat)
    x = '<span class="fu-x" aria-hidden="true"></span>'   # Robert 30.10.2026: kein «×» auf der Seite, ruhiger Punkt statt gedrehtem «+»
    return '''</main>
<footer class="fuss">
  <div class="fu-trio auf"><div class="fu-cul">%s</div>%s<div class="fu-ws">%s</div>%s<div class="fu-dc">%s</div></div>
  <div class="fu-bilder auf">%s<span></span>%s<span></span>%s</div>
  <div class="fu-spalten">%s%s%s</div>
  %s
  <div class="fu-unten"><nav class="fu-nav sw auf" style="--i:0" aria-label="Seiten">%s</nav>
    <p class="fu-ig sw auf" style="--i:1"><a href="https://www.instagram.com/culinarium_hannover/" rel="noopener" target="_blank">@culinarium_hannover</a><a href="https://www.instagram.com/walkonthewildside_hannover/" rel="noopener" target="_blank">@walkonthewildside_hannover</a><a href="https://www.instagram.com/dirtychicken.hannover/" rel="noopener" target="_blank">@dirtychicken.hannover</a></p>
    <div class="fu-recht sw auf" style="--i:2"><span>Culinarium im Walk on the Wild Side</span><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a><a class="fu-sprache" href="en/%s" hreflang="en" lang="en">English</a></div></div>
</footer>
<script src="assets/culinarium.js?v=%s" defer></script>%s
</body>
</html>
''' % (marke('wmz'), x, zeichen_haus('ws'), x, zeichen_haus('dc'),
       fu_bild('tafelleer', '(max-width:860px) 60vw, 56vw', '50% 58%'), fu_bild('theke', '(max-width:860px) 20vw, 14vw', '50% 40%'),
       fu_bild('dc_tisch', '(max-width:860px) 20vw, 12vw', '50% 50%'),
       spalte(1, 'Culinarium', 'Ein Menü, fünf passende Drinks, eine lange Tafel.', 'An einzelnen Wochenenden, vierzehn Plätze pro Abend.',
              [('Freitag', 'ab 19:00 Uhr'), ('Samstag', 'ab 17:00 Uhr')], knopf('Der Abend', 'abend.html'), 'fu-name fu-gross'),
       spalte(2, 'Das Haus', 'Walk on the Wild Side', 'Haasemannstraße 13<br>30449 Hannover-Linden',
              [('Do', '19 bis 1 Uhr'), ('Fr und Sa', '19 bis 2 Uhr'), ('Telefon', '<a class="fu-zl" href="tel:+491633909578">+49 163 3909578</a>'),
               ('Nachricht', '<button class="fu-zl" type="button" data-anfrage="nachricht">Schreib uns</button>')],
              knopf('Zur Bar', '../../Walk%20on%20the%20Wild%20Side%20Hannover/website/index.html')),   # Robert 29.10.2026: Fassung 2 aus _varianten-fuss (Telefon, Nachricht, Instagram in der Tabelle, je Spalte ein Knopf); Stand davor *.vor-fuss2-2026-10-29
       spalte(3, 'Das Pop-up', 'Dirty Chicken', 'Aus der Familie<br>der Bar', [('Küche', 'Sandwiches &amp; More'), ('Termine', 'auf Instagram'),
               ('Instagram', '<a class="fu-zl fu-ig2" href="https://www.instagram.com/dirtychicken.hannover/" rel="noopener" target="_blank">@dirtychicken.<wbr>hannover</a>')],
              knopf('Zum Pop-up', 'dirty-chicken.html')),
       WARTELISTE_FUSS, nav, SEITE_AKTUELL[0], VERSION, extra_js)


def filmgrund(k):
    im = Image.open(os.path.join(A, 'film', k + '.webp')).convert('RGB'); im.thumbnail((20, 20))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=55)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def schreibe(name, inhalt):
    for k in FILM:
        inhalt = inhalt.replace('--lq:url(assets/film/%s.webp)' % k, '--lq:url(%s)' % filmgrund(k))
    open(os.path.join(HIER, name), 'w').write(inhalt)
    print('Seite', name, len(inhalt) // 1024, 'KB')


# ---------------------------------------------------------------- Startseite
AUFTAKT_WAHL = 11  # Robert 26.10.2026 abends: «8» aus den 15 neuen Auftakten (auftakt-wahl.html) = «Ebenen»; vorher Nummer 4 «Anstossen»
AUFTAKT_TEXT = 'Food-Pairing-Abende im Walk on the Wild Side in Linden: ein Menü mit fünf passenden Drinks an einer langen Tafel für vierzehn Gäste.'


def auftakt_fassungen():
    F = []
    def text(cls=''):
        return ('<div class="at-text %s"><p class="at-satz sw auf" style="--i:2">%s</p>%s</div>'
                % (cls, AUFTAKT_TEXT, '<div class="sw auf" style="--i:3">' + knopf('Zum nächsten Abend', '#bisbald') + '</div>'))

    def lockup(cls=''):
        return '<div class="at-marke %s"><h1 class="vh">Culinarium</h1><div class="at-wm">%s</div><div class="at-zeile">%s</div></div>' % (   # h1 unsichtbar für Google (Oberchef 28.10.2026)
            cls, '<span class="z"><span style="--i:0">' + marke('wm') + '</span></span>',
            '<span class="z"><span style="--i:1">' + marke('zeile') + '</span></span>')

    F.append(('Momo x Rudi', 'f-paar', '<div class="at-paar paar auf">%s%s</div><div class="at-hof"></div>%s%s' % (
        foto('momo', 'at-l', '50vw', True, False), foto('rudi', 'at-r', '50vw', True, False), lockup('zl auf'), text())))
    F.append(('Glas x Teller', 'f-galerie', '%s<div class="at-paar paar auf">%s%s</div>%s' % (
        lockup('zl auf'), foto('glas', '', '34vw', True, False), foto('tarte', '', '34vw', True, False), text('mitte'))))
    F.append(('Die Tafel', 'f-tafel', '<div class="at-links">%s<p class="at-zahl sw auf" style="--i:2"><b data-zahl="14">14</b> Plätze an einem Tisch</p>%s</div><div class="at-rechts">%s</div>' % (
        lockup('zl auf'), text(), foto('tafelleer', '', '46vw', True))))
    F.append(('Anstoßen', 'f-hoehen', '<div class="at-paar paar auf">%s%s</div>%s%s' % (
        foto('toast', 'hoch', '38vw', True, False), foto('tablett', 'tief', '38vw', True, False), lockup('zl auf'), text())))
    F.append(('Linden bei Nacht', 'f-nacht', '<div class="at-paar paar auf">%s%s</div><div class="at-hof"></div><p class="at-ort zl auf"><span class="z"><span style="--i:0">Haasemannstraße 13</span></span></p>%s%s' % (
        foto('schildnacht', 'n1', '40vw', True, False), foto('barnacht', 'n2', '60vw', True, False), lockup('zl auf'), text())))
    F.append(('Rudis Zeile', 'f-zeile hell', '<div class="at-links">%s%s%s</div><div class="at-rechts">%s</div>' % (
        lockup('zl auf'),
        zl(['AUBERGINE /', 'KOKOS /', 'LIMETTE /', 'SESAM'], 'p', 'at-rudi', 2),
        text(), foto('anrichten', '', '42vw', True))))
    F.append(('Kerzen', 'f-kerzen', '<div class="at-drei flaeche auf">%s%s%s</div><div class="at-hof"></div>%s%s' % (
        foto('kerze1', '', '34vw', True, False), foto('kerze2', '', '34vw', True, False), foto('kerze3', '', '34vw', True, False), lockup('zl auf'), text())))
    F.append(('Die Theke', 'f-theke', '<div class="at-rechts">%s</div><div class="at-links">%s%s%s</div>' % (
        foto('theke', '', '52vw', True), lockup('zl auf'), text(), foto('theke2', 'klein', '22vw', True))))
    wand = ''.join(foto(k, '', '24vw', True, False) for k in ('m1', 'm2', 'm3', 'm4')) + '<div class="at-wandmitte">%s<div class="sw auf" style="--i:3">%s</div></div>' % (lockup('zl auf'), knopf('Zum nächsten Abend', '#bisbald')) + ''.join(
        foto(k, '', '24vw', True, False) for k in ('m5', 'm6', 'm7', 'm8'))
    F.append(('Handwerk', 'f-wand', '<div class="at-wand flaeche auf">%s</div>' % wand))
    F.append(('In der Küche', 'f-kueche', '<div class="at-paar paar auf">%s%s</div><div class="at-hof"></div>%s%s' % (
        foto('kueche', 'gross', '60vw', True, False), foto('service', '', '40vw', True, False), lockup('zl auf'), text())))
    # Ebenen: der Name steht zwischen den Bildern, die Ebenen folgen der Maus mit eigener Tiefe (Wahlseite Nummer 8)
    F.append(('Ebenen', 'f-ebenen', '<div class="ve-e auf" data-t="-.4">%s%s</div>%s<div class="ve-e auf" data-t="1">%s%s</div>%s' % (
        # Auftakt behält Tafel und Theke (Robert 26.10.2026: «wieder zurück»); «Flankiert» darunter zeigt dafür t09 und theke2
        foto('tafelleer', 've-a', '(max-width:860px) 52vw, 34vw', True, False, '50% 40%'), foto('theke', 've-b', '(max-width:860px) 48vw, 30vw', True, False, '50% 35%'),
        lockup('zl auf'), foto('g1', 've-c', '(max-width:860px) 24vw, 16vw', True, False), foto('roq1', 've-d', '(max-width:860px) 24vw, 17vw', True, False), text())))
    out = []
    for i, (name, cls, inner) in enumerate(F, 1):
        if i != AUFTAKT_WAHL:
            continue
        out.append('<div class="fassung %s offen" data-nr="%d" data-name="%s">%s</div>' % (cls, i, E(name), inner))
    return ('<section class="auftakt" data-ton="nacht" id="auftakt" aria-label="Culinarium">%s</section>' % ''.join(out),
            [(i, n) for i, (n, _c, _x) in enumerate(F, 1)])


def startseite():
    auf, fliste = auftakt_fassungen()
    s = [kopf('Culinarium Hannover · Momo x Rudi', 'Food Pairing in der Bar Walk on the Wild Side, Hannover-Linden: drei Gänge von Rudi, fünf Drinks von Momo, vierzehn Plätze an einer Tafel.', 'index.html')]
    s.append(auf)

    # Ankommen · Ort und Zeiten: fakten.json › adresse, restaurants.zeiten
    s.append('''<section class="ankommen" data-ton="strasse" id="ankommen" data-lauf="Ankommen">
  <div class="ank-kopf">
    %s
    <div class="ank-text">%s%s</div>
  </div>
  <div class="treppe flaeche auf">%s%s%s%s</div>
  <p class="ueber sw auf">Die Tür ist offen.</p>
</section>''' % (zl(['Haasemannstraße', '13.'], 'h2', 'gross'),
                 sw('Linden-Mitte, an einzelnen Wochenenden im Jahr. Culinarium ist zu Gast in der Bar Walk on the Wild Side, an einer langen Tafel.'),
                 sw('<span class="mono">Freitag ab 19:00 · Samstag ab 17:00</span>', 'p', '', 1),
                 foto('schildtag', 's1', '(max-width:860px) 50vw, 24vw', auf=False), foto('ecke', 's2', '(max-width:860px) 50vw, 24vw', auf=False),
                 foto('fassade', 's3', '(max-width:860px) 50vw, 24vw', auf=False), foto('flur', 's4', '(max-width:860px) 50vw, 24vw', auf=False)))

    # Das eine Fenster
    s.append('''<section class="fenster" id="fenster" aria-label="Drinnen">
  <div class="fenster-schicht">%s<div class="fenster-hof"></div><p class="fenster-satz zl"><span class="z"><span style="--i:0">Drinnen wird</span></span><span class="z"><span style="--i:1">schon angestoßen.</span></span></p></div>
</section>''' % foto('anstossen', '', '100vw', auf=False))

    # Aperitif · Momo: Beitrag DbYnkdkjrNy (Techniken, «Momo wird persönlich …»)
    s.append('''<section class="aperitif" data-ton="warm" id="aperitif" data-lauf="Aperitif">
  <div class="ap-raster">
    <div class="ap-paar paar auf">%s%s</div>
    <div class="ap-text">
      %s
      %s
      <blockquote class="zitat sw auf" style="--i:1"><p>„Momo wird persönlich jeden Drink für dich erklären.“</p></blockquote>
      <dl class="techniken">
        <div class="sw auf" style="--i:2"><dt>Fatwashing</dt><dd>Die Spirituose nimmt den Geschmack eines Fetts an, von Butter, Nuss oder Öl. Kalt gestellt, wird das Fett wieder abgehoben.</dd></div>
        <div class="sw auf" style="--i:3"><dt>Milkwashing</dt><dd>Milch bindet die Trübstoffe und wird abgefiltert. Übrig bleibt ein klarer, weicher Drink.</dd></div>
        <div class="sw auf" style="--i:4"><dt>Enzyme</dt><dd>Enzyme lösen die Trübung aus Fruchtsaft. Der Drink wird klar, der Geschmack bleibt.</dd></div>
      </dl>
    </div>
  </div>
  <div class="glaeser-kopf">%s%s</div>
  <div class="glaeser staffel auf">%s</div>
  <p class="ueber sw auf">Und während du trinkst, wird drüben angerichtet.</p>
</section>''' % (foto('bar', '', '(max-width:860px) 50vw, 26vw', auf=False), foto('klaeren', '', '(max-width:860px) 50vw, 26vw', auf=False),
                 zl(['FATWASHING /', 'MILKWASHING /', 'ENZYME'], 'h2', 'rudi'),
                 sw('Bevor der erste Teller kommt, steht das erste Glas. Momo mixt fünf eigene Drinks, passend zum Essen, und zeigt dir, wie sie gemacht sind.'),
                 zl(['Fünf Gläser.'], 'h3', 'mittel'),
                 sw('„5 von Momos Signature Drinks, kreativ kreiert passend zum Essen.“', 'p', 'glaeser-satz', 1),
                 ''.join(foto(k, '', '(max-width:860px) 46vw, 19vw', auf=False, extra='style="--i:%d"' % i) for i, k in enumerate(('g1', 'g2', 'g3', 'g4', 'g5')))))

    # Am Pass und Rudis Zeilen (ZEILEN: Wortlaut der Beiträge)
    zeilen = []
    for i, (z, bilder, bid) in enumerate(ZEILEN):
        art = 'paar' if len(bilder) == 2 else 'einzel'
        bild = '<div class="zeile-bild %s auf">%s</div>' % (art, ''.join(foto(b, '', '(max-width:860px) 92vw, 30vw' if art == 'paar' else '(max-width:860px) 92vw, 52vw', auf=False) for b in bilder))
        zeilen.append('<article class="zeile %s %s">%s<div class="zeile-wort">%s</div></article>' % (
            'rechts' if i % 2 else 'links', art, bild, zl(z, 'h3', 'rudi')))
    s.append('''<section class="pass" data-ton="hell" id="gaenge" data-lauf="Drei Gänge">
  <div class="pass-kopf">%s%s</div>
  <div class="pass-band flaeche auf">%s%s%s%s</div>
  <div class="pass-satz">%s</div>
  <div class="zeilen">%s</div>
  <p class="ueber dunkel sw auf">Drei Gänge sind erst ein Abend, wenn vierzehn Leute daran sitzen.</p>
</section>''' % (zl(['Am Pass.'], 'h2', 'gross'),
                 sw('Rudi kocht ein Menü in drei Gängen. Angerichtet wird Teller für Teller, für die ganze Tafel.'),
                 foto('pass', 'b1', '(max-width:860px) 100vw, 46vw', auf=False), foto('pass2', 'b2', '(max-width:860px) 50vw, 17vw', auf=False),
                 foto('pass3', 'b3', '(max-width:860px) 50vw, 17vw', auf=False), foto('pass4', 'b4', '(max-width:860px) 100vw, 20vw', auf=False),
                 sw('Rudi schreibt seine Teller in drei, vier Wörtern. So stehen sie auch hier.', 'p', 'gross-satz'),
                 ''.join(zeilen)))

    # Tafel · «nur 14 Plätze pro Abend» (DFqbLG2s_dc)
    tafel_o = ''.join(foto('t%02d' % i, '', '(max-width:860px) 30vw, 14vw', auf=False) for i in range(1, 8))
    tafel_u = ''.join(foto('t%02d' % i, '', '(max-width:860px) 30vw, 14vw', auf=False) for i in range(8, 15))
    s.append('''<section class="tafel" data-ton="kerze" id="tafel" data-lauf="Die Tafel">
  <div class="tafel-kopf">%s%s</div>
  <div class="tafel-tisch flaeche auf">
    <div class="tafel-reihe">%s</div>
    <div class="tafel-platte"><span class="zahl"><b data-zahl="14">14</b> Plätze</span><span class="mono">Freitag 19:00 · Samstag 17:00</span><span class="mono">Linden</span></div>
    <div class="tafel-reihe">%s</div>
  </div>
  <p class="ueber sw auf">Jeder dieser Abende hatte sein eigenes Plakat.</p>
</section>''' % (zl(['Vierzehn Plätze.', 'Eine Tafel.'], 'h2', 'gross'),
                 sw('Wer kommt, sitzt mit allen anderen an einem Tisch, auf der kleinen Empore der Bar.'),
                 tafel_o, tafel_u))

    # Plakate
    plak = [a for a in ABENDE if a[4]][::-1][:9]
    def pl(i, p, sz):
        r = META['p_' + p[4]]['w'] / META['p_' + p[4]]['h']
        return '<a class="plakat" href="abende.html#a-%s" style="--i:%d;--akz:%s;--r:%.4f">%s<span class="plakat-datum"><span>%s %s</span><em>%s</em></span></a>' % (
            p[4], i, akzent('p_' + p[4]), r, foto('p_' + p[4], '', sz, auf=False, ratio=True), E(p[1]), p[0], E(p[3]))
    reihen = ((0, 2, '(max-width:860px) 46vw, 46vw'), (2, 5, '(max-width:860px) 46vw, 31vw'), (5, 9, '(max-width:860px) 46vw, 23vw'))
    wand = ''.join('<div class="pw-reihe">%s</div>' % ''.join(pl(i, plak[i], sz) for i in range(a, b)) for a, b, sz in reihen)
    s.append('''<section class="plakate" data-ton="schiefer" id="plakate" data-lauf="Die Plakate">
  <div class="plakate-kopf">%s<div>%s<div class="sw auf" style="--i:1">%s</div></div></div>
  <div class="plakatwand flaeche auf">%s</div>
  <p class="ueber sw auf">Hinter den Plakaten stehen dieselben Leute, Abend für Abend.</p>
</section>''' % (zl(['Jeder Abend', 'hat sein Plakat.'], 'h2', 'gross'),
                 sw('Seit September 2023 bekommt jeder Abend ein eigenes Plakat, darunter immer dieselbe Wortmarke. Zusammen sehen sie aus wie die Ausgaben eines Magazins.'),
                 knopf('Alle Abende ansehen', 'abende.html'), wand))

    # Familie · Satz aus Beitrag DZIjZWNCGZT (Dirty Chicken mit Rudi, 03.06.2026); Rollen fakten.json › personen
    s.append('''<section class="familie" data-ton="hell" id="familie" data-lauf="Die Familie">
  <div class="fam-raster">
    <div class="fam-film paar auf">
      <figure class="film quadrat" style="--lq:url(assets/film/familie.webp)"><video muted playsinline preload="none" poster="assets/film/familie.webp?v=%s" data-src="assets/film/familie.mp4?v=%s" aria-label="Die Mannschaft an der Theke"></video><button class="film-nochmal" type="button" aria-label="Film noch einmal abspielen">Noch einmal</button></figure>
      %s
    </div>
    <div class="fam-text">
      %s
      %s
      <ul class="namen">
        <li class="sw auf" style="--i:2"><b>Rudi Napieraj</b><span>Küche</span></li>
        <li class="sw auf" style="--i:3"><b>Momo</b><span>Drinks, Tasting und Schulung</span></li>
        <li class="sw auf" style="--i:4"><b>Derya Ivkin</b><span>Gastgeberin</span></li>
      </ul>
      <div class="sw auf" style="--i:5">%s</div>
    </div>
  </div>
  <p class="ueber dunkel sw auf">Und dieselben Leute haben noch eine zweite Küche.</p>
</section>''' % (VERSION, VERSION, foto('trio', '', '(max-width:860px) 92vw, 30vw', auf=False),
                 zl(['Wenn aus Freunden', 'und Kollegen', 'Familie wird.'], 'h2', 'gross'),
                 sw('<span class="handschrift">Dann haste allet richtig jemacht!</span>', 'p', '', 1),
                 knopf('Momo x Rudi', 'leute.html', 'hell')))

    # Dirty Chicken · Beiträge DZiug6EoMRr («Dit ist wahre Liebe!»), DZIo4FHIqRR, DZPYEOJIfVb («Opening 2026!»)
    s.append('''<section class="dc" data-ton="dc" id="dirty-chicken" data-lauf="Dirty Chicken">
  <div class="dc-raster">
    <div class="dc-text">
      %s
      %s
      %s
      <div class="sw auf" style="--i:3">%s</div>
    </div>
    <div class="dc-buehne">
      <div class="dc-seite links">%s</div>
      <figure class="film hoch auf" style="--lq:url(assets/film/opening.webp)"><video muted playsinline preload="none" poster="assets/film/opening.webp?v=%s" data-src="assets/film/opening.mp4?v=%s" aria-label="Opening 2026 bei Dirty Chicken"></video><button class="film-nochmal" type="button" aria-label="Film noch einmal abspielen">Noch einmal</button></figure>
      <div class="dc-seite rechts">%s</div>
    </div>
  </div>
</section>''' % (zl(['Dit ist', 'wahre Liebe!'], 'h2', 'gross'),
                 sw('Rudis zweite Küche heisst Dirty Chicken: Sandwiches &amp; More, Dirty Food &amp; Dirty Drinks.'),
                 sw('Am 30. Mai 2026 war Opening. „Wat ne Sause.“', 'p', '', 2),
                 knopf('Zu Dirty Chicken', 'dirty-chicken.html', 'violett'),
                 foto('dc_burger', '', '(max-width:860px) 40vw, 16vw'), VERSION, VERSION, foto('dc_drink', '', '(max-width:860px) 40vw, 16vw')))

    # Der nächste Abend · zuletzt DbYnkdkjrNy (25./26.09.2026, 89,00 EUR, ausgebucht); nächster Termin offen (Profil 25.10.2026)
    s.append('''<section class="naechster" data-ton="nacht" id="naechster" data-lauf="Nächster Abend">
  <div class="nae-raster">
    <div class="nae-paar paar auf">%s%s</div>
    <div class="nae-text">
      %s
      %s
      <p class="zuletzt sw auf" style="--i:2"><span class="mono">Zuletzt</span> Freitag, 25. und Samstag, 26. September 2026 · 89,00 EUR · ausgebucht</p>
      <div class="knoepfe sw auf" style="--i:3">%s%s</div>
    </div>
  </div>
</section>''' % (foto('glaeser', '', '(max-width:860px) 46vw, 24vw', auf=False), foto('barlicht', '', '(max-width:860px) 46vw, 24vw', auf=False),
                 zl(['Der nächste', 'Abend.'], 'h2', 'gross'),
                 sw('Der Termin steht noch nicht fest. Wer auf der Warteliste steht, erfährt ihn zuerst.'),
                 knopf('Auf die Warteliste', 'abend.html#warteliste'), knopf('Was zum Abend gehört', 'abend.html', 'leise')))

    lauf = '<nav class="abendlauf" aria-label="Der Abend">%s</nav>' % ''.join(
        '<a href="#%s" data-ziel="%s"><span>%s</span></a>' % (i, i, t) for i, t in (
            ('ankommen', 'Ankommen'), ('aperitif', 'Aperitif'), ('gaenge', 'Drei Gänge'), ('tafel', 'Die Tafel'),
            ('plakate', 'Die Plakate'), ('familie', 'Die Familie'), ('dirty-chicken', 'Dirty Chicken'), ('naechster', 'Nächster Abend')))
    s.append(fuss(lauf))
    # Abendlauf und Fassungsleiste gehören vor die Skripte, ausserhalb von main
    html_ = ''.join(s)
    schreibe('index.html', html_)


# ---------------------------------------------------------------- Der Abend (Menü, Preis, Warteliste)
def abend():
    s = [kopf('Culinarium · Walk on the Wild Side', 'Was zu einem Culinarium-Abend gehört: Aperitif, drei Gänge, fünf Drinks von Momo mit Tasting und Schulung. Termine, Preis und Warteliste.', 'abend.html')]
    s.append('''<section class="seitenkopf" data-ton="nacht">
  <div class="sk-paar paar auf">%s%s</div>
  <div class="sk-text">%s%s</div>
</section>''' % (foto('beete', '', '(max-width:860px) 50vw, 30vw', True, False), foto('beeteglas', '', '(max-width:860px) 50vw, 30vw', True, False),
                 zl(['Culinarium.'], 'h1', 'gross'),
                 sw('Die Abende an der langen Tafel des Walk on the Wild Side: drei Gänge, fünf Drinks, vierzehn Plätze. Und wer dir erklärt, was auf dem Teller und im Glas ist.')))
    # Was auf den Tisch kommt: Vier Säulen (Robert wählte Fassung 1 der zweiten Runde, 27.10.2026). Je Teil eine hohe Säule, versetzt gehängt,
    # jede gleitet beim Scrollen in eigenem Tempo (nur transform). Menükarte: Beitrag DbYnkdkjrNy; Aperitif C56bJeds8PF, C8cgYVSouVT; Robert 27.10.2026: keine Zutaten-Zeile vom letzten Abend unter «Drei Gänge»
    SAEULEN = [('Aperitif', 'zum Ankommen', 'toast', 'glaeser', '0px', '.05'),
               ('Drei Gänge', 'von Rudi, an jedem Abend neu', 'beete', 'anrichten', '96px', '-.04'),
               ('Fünf Drinks', 'Momos Signature Drinks, passend zum Essen', 'g1', 'momo', '28px', '.07'),
               ('Tasting und Schulung', 'Momo erklärt jeden Drink am Tisch: Fatwashing, Milkwashing, Klärung mit Enzymen', 'klaeren', 'schaum', '128px', '-.02')]
    s.append('''<section class="menuekarte saeulen" data-ton="warm">
  <div class="ms-in">
    <div class="ms-kopf">%s%s</div>
    <div class="ms-reihe">%s</div>
  </div>
</section>''' % (zl(['Was auf den', 'Tisch kommt.'], 'h2', 'gross'),
                 sw('Das Menü ändert sich mit jedem Abend. Rudi kocht drei Gänge, dazu kommen fünf Signature Drinks von Momo, mit Tasting und einer kleinen Schulung am Tisch. Was genau es gibt, steht auf der Karte an deinem Platz.'),
                 ''.join('<div class="ms-s" data-ms-par="%s" style="--o:%s">%s<div class="ms-text sw auf" style="--i:%d"><h3>%s</h3><p>%s</p></div>%s</div>' % (
                     sp, o, foto(a, 'ms-b', '(max-width:860px) 46vw, 22vw'), i, n, u, foto(b, 'ms-b2', '(max-width:860px) 46vw, 22vw'))
                     for i, (n, u, a, b, o, sp) in enumerate(SAEULEN))))
    # Termine und Tickets: DbYnkdkjrNy, DVjkofijp6R; Storno wörtlich
    s.append('''<section class="termine" data-ton="nacht">
  <div class="te-buehne">
    <div class="te-bild auf">%s</div>
    <div class="te-hof"></div>
    <div class="te-inhalt">
      %s
      <div class="te-zahlen staffel auf">
        <div class="te-z" style="--i:0"><b>19:00</b><span>freitags ab</span></div>
        <div class="te-z" style="--i:1"><b>17:00</b><span>samstags ab</span></div>
        <div class="te-z" style="--i:2"><b data-zahl="14">14</b><span>Plätze an einer Tafel</span></div>
        <div class="te-z" style="--i:3"><b>89&#160;€</b><span>zuletzt, 25. und 26. September 2026, ausgebucht</span></div>
      </div>
      <p class="te-satz sw auf">Culinarium findet an einzelnen Wochenenden statt. Der nächste Termin steht noch nicht fest. Tickets gibt es bisher nur im Vorverkauf. „Da die Plätze begrenzt sind, bitten wir um Verständnis, dass Tickets nicht rückerstattet werden können.“</p>
    </div>
  </div>
</section>''' % (foto('tafelleer', '', '100vw', auf=False), zl(['Wann und', 'wie viel.'], 'h2', 'gross')))
    # Warteliste als Ticket mit Abriss (Robert 27.10.2026: Fassung 2 aus warteliste-wahl.html); Formular geht nirgendwohin (Vorgabe 26.10.2026)
    tage = ''.join('<label><input type="radio" name="tag" value="%s"%s><span><b>%s</b><em>%s</em></span></label>' % (
        k, ' checked' if k == 'fr' else '', t, z) for k, t, z in [('fr', 'Freitag', 'ab 19:00'), ('sa', 'Samstag', 'ab 17:00'), ('egal', 'Egal', 'beides geht')])
    s.append('''<section class="warteliste" data-ton="kerze" id="warteliste">
  <div class="wt">
    <div class="wt-kopf">
      %s
      %s
    </div>
    <form class="wt-form wt-ticket auf" novalidate>
      %s
      <div class="wt-mitte">
        <div class="wt-marke">%s<span>A UNiQUE EXPERiENCE BY MOMO X RUDI</span></div>
        <div class="wt-tage" role="radiogroup" aria-label="Welcher Tag passt dir?"><p class="wt-k">Tag</p><div class="wt-wahl">%s</div></div>
        <div class="wt-plaetze"><p class="wt-k">Plätze</p><div class="wt-zaehler"><button type="button" data-schritt="-1" aria-label="Weniger">−</button><output data-feld="n" aria-live="polite">2</output><button type="button" data-schritt="1" aria-label="Mehr">+</button></div></div>
        <div class="wt-felder">
          <label class="wt-feld"><span>Name</span><input name="name" autocomplete="name" required></label>
          <label class="wt-feld"><span>E-Mail</span><input name="mail" type="email" autocomplete="email" required></label>
        </div>
        <div class="wt-tat"><button class="knopf" type="submit"><span>Auf d<em class="ki">i</em>e Warteliste</span><i>%s</i></button></div>
        <p class="wt-meldung" role="status" aria-live="polite"></p>
      </div>
      <div class="wt-abriss" aria-hidden="true"><p class="wt-k">Warteliste</p><b data-feld="n">2</b><span class="wt-klein">Plätze</span>
        <p class="wt-tag" data-feld="tag">Freitag</p><p class="wt-klein" data-feld="zeit">ab 19:00</p><p class="wt-name" data-feld="name">Dein Name</p><p class="wt-ok">Vorgemerkt</p></div>
    </form>
  </div>
</section>''' % (zl(['Dein Platz', 'an der Tafel.'], 'h2', 'mittel'),
                 sw('Vierzehn Plätze an einer Tafel, und der letzte Abend war ausgebucht. Trag dich ein: Sobald der nächste Termin feststeht, erfährst du es vor allen anderen.', 'p', '', 1),
                 foto('anstossen', 'wt-bild', '(max-width:860px) 100vw, 30vw', auf=False), marke('wm'), tage, PFEIL))
    # Fenster zwischen Warteliste und Fuss (Robert 27.10.2026). Satz Robert 28.10.2026: nichts mehr mit Platz oder Tafel, das steht schon darüber. Stand davor bau.py.vor-fenster2-satz-2026-10-28
    s.append('''<section class="fenster" id="fenster2" aria-label="Ein Teller, den man festhalten will.">
  <div class="fenster-schicht">%s<div class="fenster-hof"></div><p class="fenster-satz zl"><span class="z"><span style="--i:0">Ein Teller, den man</span></span><span class="z"><span style="--i:1">festhalten will.</span></span></p></div>
</section>''' % foto('t12', '', '100vw', auf=False, pos='50% 45%'))  # Bild 8 aus fenster2-wahl.html (Robert 27.10.2026)
    s.append(fuss())
    schreibe('abend.html', ''.join(s))


# ---------------------------------------------------------------- Alle Abende
def abend_dialoge():
    """Zu jedem Abend ein Blatt. Oben Plakat und Angaben; darunter die Tafel wie beim Schlössli (Robert 27.10.2026):
    die Menükarte in der Mitte, die Bilder ringsum, alle bündig zugeschnitten, keine Leerflächen, keine Instagram-Namen.
    Bilder je Seite: eins füllt die Spalte, zwei liegen übereinander, drei als ein breites und zwei halbe. Was über sechs
    hinausgeht, folgt in vollen Reihen gleicher Höhe."""
    def kachel(k, cap='', cls=''):
        c = '<span class="ad-cap">%s</span>' % cap if cap else ''
        # loading lazy (30.10.2026): die Bilder stehen in der verborgenen Ansicht «Mehr zum Abend» und laden erst, wenn sie aufgeht, nicht mehr alle beim Laden der Seite
        return '<figure class="ad-k-b%s"><img src="assets/bild/%s-%d.webp?v=%s" srcset="%s" sizes="(max-width:860px) 50vw, 420px" alt="%s" loading="lazy" decoding="async">%s</figure>' % (
            (' ' + cls) if cls else '', k, META[k]['stufen'][min(1, len(META[k]['stufen']) - 1)], VERSION, srcset(k), E(BILD[k][2]), c)

    def seite(ks, rechts=False):
        """Eine Seite neben der Karte: 1 voll, 2 übereinander, 3 = breit oben und zwei halbe (rechts gespiegelt: breit unten)."""
        if not ks:
            return ''
        if len(ks) == 3:
            breit, halb = kachel(*ks[0], cls='breit'), kachel(*ks[1]) + kachel(*ks[2])
            inner = (halb + breit) if rechts else (breit + halb)
        else:
            inner = ''.join(kachel(*x) for x in ks)
        return '<div class="ad-seite n%d%s">%s</div>' % (len(ks), ' rechts' if rechts else '', inner)

    teile = []
    for j, d, z, p, pid, mit in ABENDE:
        key = pid or 'ohne-%s' % j
        inf = _AI.INFO.get(key)
        if not inf:
            continue
        kk = key.replace('-', '_')
        plakat = ('<img src="assets/bild/p_%s-1000.webp?v=%s" alt="Plakat" loading="lazy" decoding="async">' % (pid, VERSION)) if pid else (
            '<img src="assets/bild/ab_%s_0-1000.webp?v=%s" alt="%s" loading="lazy" decoding="async">' % (kk, VERSION, E(BILD['ab_%s_0' % kk][2])) if 'ab_%s_0' % kk in BILD
            else '<div class="vit-ohne">%s</div>' % marke('wm'))   # ohne Plakat: erstes Foto des Abends (30.10.2026)
        zeilen = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(a_), E(b_)) for a_, b_ in inf['zeilen'])
        # Rückblick als breites Zitat über die ganze Breite, nicht mehr in der Spalte neben dem Plakat (Robert 27.10.2026)
        rb = ('<blockquote class="ad-zitat"><p>%s</p><cite>Rückblick von Culinarium, %s</cite></blockquote>' % (E(inf['rueckblick'][0]), inf['rueckblick'][1])) if inf['rueckblick'] else ''
        # Bilder: Rudis Teller zuerst (die stärksten Fotos), dann die Bilder des Abends
        # ohne Schrift im Bild: Rudis Teller stehen mit Namen auf der Karte (Vom Pass)
        bilder = [('abr_%s_%d' % (kk, n), '') for n, (dat, g, q) in enumerate(inf['rudi']) if q]
        bilder += [('ab_%s_%d' % (kk, n), '') for n in range(len(inf['bilder']))]
        if len(bilder) > 6 and (len(bilder) - 6) % 4 == 1 and (len(bilder) - 6) < 5:
            bilder = bilder[:6]                      # ein einzelnes übriges Bild bekäme eine eigene Reihe: weglassen
        # Menükarte
        k = _AI.KARTEN.get(key)
        datum = '%s %s' % (E(d), j)
        if k:
            gaenge = ''.join('<div class="mk2-g"><p class="mk2-n">%s</p>%s%s</div>' % (
                E(g), ('<p class="mk2-t">%s</p>' % E(t)) if t else '', ('<p class="mk2-d">%s</p>' % E(dr)) if dr else '') for g, t, dr in k['gaenge'])
            if k.get('upgrade'):
                gaenge += '<div class="mk2-g mk2-up"><p class="mk2-n">Upgrade nach Wahl</p>%s</div>' % ''.join('<p class="mk2-t">%s</p>' % E(u) for u in k['upgrade'])
            fuss = '<p class="mk2-q">%s%s</p>' % (E(k['quelle']), '' if k['voll'] else ' · Rest der Karte nicht lesbar')
            teller = [g for _dat, g, _q in inf['rudi'] if g.isupper()]
            if teller:
                gaenge += '<div class="mk2-g mk2-up"><p class="mk2-n">Vom Pass</p>%s</div>' % ''.join('<p class="mk2-t">%s</p>' % E(g) for g in teller)
        else:
            # Keine Karte überliefert: die Karte zeigt, was belegt ist (Satz zum Menü aus der Ankündigung, Rudis Teller), kein Platzhalter
            menue = next((b_ for a_, b_ in inf['zeilen'] if a_ == 'Menü'), '')
            gaenge = '<div class="mk2-g"><p class="mk2-satz">%s</p></div>' % E(menue) if menue else ''
            teller = [g for _dat, g, _q in inf['rudi'] if g.isupper()]
            if teller:
                gaenge += '<div class="mk2-g"><p class="mk2-n">Vom Pass</p>%s</div>' % ''.join('<p class="mk2-t">%s</p>' % E(g) for g in teller)
            fuss = '<p class="mk2-q">%s · %s</p>' % (E(p), E(mit))
        karte = '<div class="mk2"><div class="mk2-kopf">%s<span>Menü</span></div><p class="mk2-datum">%s</p>%s%s</div>' % (marke('wm'), datum, gaenge, fuss)
        # Tafel: Karte in der Mitte, bis zu sechs Bilder ringsum
        vorn, rest = bilder[:6], bilder[6:]
        links, rechts = vorn[:(len(vorn) + 1) // 2], vorn[(len(vorn) + 1) // 2:]
        tafel = '<div class="ad-tafel n%d">%s<div class="ad-karte">%s</div>%s</div>' % (len(vorn), seite(links), karte, seite(rechts, True))
        reihen = ''
        if rest:
            anz = -(-len(rest) // 4)
            groessen = [len(rest) // anz + (1 if i < len(rest) % anz else 0) for i in range(anz)]
            a_ = 0
            for g_ in groessen:
                r = rest[a_:a_ + g_]; a_ += g_
                reihen += '<div class="ad-reihe" style="--n:%d">%s</div>' % (len(r), ''.join(kachel(*x) for x in r))
        kopf_ = '<p class="ad-k">%s · %s%s</p>' % (datum, E(p), (' · ' + E(z)) if z else '')
        titel = inf['motto'] or inf['titel'] or 'Culinarium'
        teile.append(('<div class="ad" id="ad-%s" hidden role="dialog" aria-modal="true" aria-label="%s"><div class="ad-grund" data-zu></div><div class="ad-blatt">'
                      '<button class="ad-zu" type="button" data-zu aria-label="Schließen"></button>'
                      '<div class="ad-oben"><div class="ad-plakat">%s</div><div class="ad-text">%s<p class="ad-mit">%s</p>%s<h2 class="ad-titel">%s</h2><dl class="ad-liste">%s</dl></div></div>%s'
                      '%s%s'
                      '<p class="ad-quelle">Wörtlich aus den Beiträgen von @culinarium_hannover (%s). Bilder: Instagram von Culinarium und Rudi.</p></div></div>') % (
            key, E(titel), plakat, kopf_, E(mit), ('<p class="ad-motto">Motto</p>' if inf['motto'] else ''), E(titel), zeilen, rb,
            tafel, reihen, E(inf['quelle'])))
    return '<div class="ad-alle">%s</div>' % ''.join(teile)


def abende():
    s = [kopf('Alle Abende · Culinarium Hannover', 'Jeder Culinarium-Abend seit 2023 mit seinem Plakat, Datum und Preis.', 'abende.html', 'schiefer')]
    # Kopf «Geteilt» (Robert 27.10.2026: «3» aus abende-kopf-wahl.html, Stand davor *.vor-kopf-geteilt-2026-10-27):
    # Hero über den ganzen ersten Bildschirm, links das Glas, rechts die Tafel Kante an Kante, der Titel über der Naht.
    # Keine Plakate im Kopf, die zeigt die Seite darunter (Robert: «Es macht jetzt überhaupt keinen Sinn, ein Hero zu bauen, wo schon wieder Poster sind»).
    def halb(k, seite):
        return '<figure class="kg-h %s auf" style="--lq:url(%s)"><img src="assets/bild/%s-1000.webp?v=%s" srcset="%s" sizes="(max-width:860px) 100vw, 50vw" alt="%s" fetchpriority="high" decoding="async" style="object-position:%s"></figure>' % (
            seite, META[k]['lq'], k, VERSION, srcset(k), E(BILD[k][2]), '50% 50%')
    # Übergang «Die Schere» (Robert 27.10.2026: «17» aus abende-uebergang-wahl3.html, Stand davor *.vor-schere-2026-10-27):
    # der Kopf steht, die linke Hälfte geht beim Scrollen hoch, die rechte runter, dazwischen liegt schon das Fenster. Nur transform.
    s.append('''<div class="kg-buehne"><section class="kopf-geteilt" data-ton="nacht">
  %s%s<div class="kg-grund" aria-hidden="true"></div>
  <div class="kg-text">%s%s</div>
</section></div>''' % (halb('schaumglas', 'l'), halb('t08', 'r'), zl(['Alle Abende.'], 'h1', 'gross'),
                 sw('Jeder Abend seit dem ersten Pop-up im Mai 2023. Darunter alle Plakate, so wie sie angekündigt wurden.')))
    # Fenster als Übergang vom dunklen Kopf ins Helle (Robert 27.10.2026: «ein Bild …, was ein bisschen einen neutralen Übergang … gibt. Keine Poster»):
    # Bild 7 aus abende-fenster-wahl.html (Robert 27.10.2026, davor g5 ‹Glas vor der Betonwand›): der gedeckte Platz mit der Karte bei Tageslicht; der Satz führt zu den Plakaten
    s.append('''<section class="fenster" id="fenster-abende" aria-label="Übergang">
  <div class="fenster-schicht">%s<div class="fenster-hof"></div><p class="fenster-satz zl"><span class="z"><span style="--i:0">Jeder Abend</span></span><span class="z"><span style="--i:1">hatte sein Plakat.</span></span></p></div>
</section>''' % foto('karte', '', '100vw', auf=False, pos='50% 58%'))
    # Die Vitrinen (Robert 27.10.2026: Fassung 9 aus abende-wahl.html, Stand davor *.vor-vitrinen-2026-10-27):
    # je Jahr eine Vitrine, die Plakate stehen auf einem Glasboden und spiegeln sich, darunter der Sockel mit dem Jahr
    ZAHL = {1: 'Ein Abend', 2: 'Zwei Abende', 3: 'Drei Abende', 4: 'Vier Abende', 5: 'Fünf Abende'}
    vitrinen = []
    for j in ('2026', '2025', '2024', '2023'):
        abende_j = [x for x in ABENDE if x[0] == j][::-1]
        # Plakate der Vitrinen laden erst beim Hinscrollen (30.10.2026: am Handy kamen rund 20 Plakate gleichzeitig mit dem ersten Bild)
        stuecke = []
        for i, (_j, d, z, p, pid, mit) in enumerate(abende_j):
            if pid:
                k = 'p_' + pid
                bild = '<img src="assets/bild/%s-640.webp?v=%s" srcset="%s" sizes="(max-width:860px) 46vw, 360px" alt="%s" loading="lazy" decoding="async">' % (
                    k, VERSION, srcset(k), E(BILD[k][2]))
                spiegel = '<img src="assets/bild/%s-640.webp?v=%s" alt="" loading="lazy" decoding="async">' % (k, VERSION)
            elif 'ab_ohne_%s_0' % j in BILD:
                # Abend ohne Plakat (22./23.09.2023): erstes Foto des Abends statt leerem Blatt mit Wortmarke (Abnahme-Tor 30.10.2026, K14)
                k = 'ab_ohne_%s_0' % j
                bild = '<img src="assets/bild/%s-640.webp?v=%s" srcset="%s" sizes="(max-width:860px) 46vw, 360px" alt="%s" loading="lazy" decoding="async">' % (
                    k, VERSION, srcset(k), E(BILD[k][2]))
                spiegel = '<img src="assets/bild/%s-640.webp?v=%s" alt="" loading="lazy" decoding="async">' % (k, VERSION)
            else:
                bild = spiegel = '<div class="vit-ohne">%s</div>' % marke('wm')
            stuecke.append(('<figure class="vit-p" id="a-%s" style="--i:%d" data-abend="' + (pid or 'ohne-%s' % j) + '" role="button" tabindex="0" aria-label="Mehr zu diesem Abend"><div class="vit-bild"><span class="vit-rahmen">%s</span><span class="vit-spiegel" aria-hidden="true">%s</span><span class="vit-mehr">Mehr zum Abend</span></div>'
                           '<figcaption><p class="vit-datum">%s %s</p><p class="vit-mono">%s%s</p><p class="vit-mit">%s</p></figcaption></figure>') % (
                               pid or ('ohne-%s' % j), i, bild, spiegel, E(d), j, E(p), (' · ' + E(z)) if z else '', E(mit)))
        mits = ' · '.join(E(m) for m in sorted({x[5] for x in abende_j}, key=lambda m: -len(m)))
        # Jahr über der Vitrine statt als Sockel darunter (Robert 27.10.2026: «Überschrift mit den Jahren bitte oberhalb der Abschnitte»)
        # Robert 27.10.2026: alle Plakate einer Vitrine schweben gemeinsam ein, sobald die Vitrine ins Bild kommt, nicht eins nach dem anderen
        vitrinen.append('<div class="vit auf"><div class="vit-sockel"><span class="vit-jahr">%s</span><span class="vit-zahl">%s</span><span class="vit-mit">%s</span></div><div class="vit-glas"><div class="vit-reihe n%d">%s</div></div></div>' % (
            j, ZAHL[len(abende_j)], mits, len(abende_j), ''.join(stuecke)))
    s.append('<section class="jahre" data-ton="hell"><div class="vitrinen">%s</div><p class="jahre-hinweis sw auf">Das erste Pop-up gab es am 20. Mai 2023 mit Momo. 2023 hießen die Abende „by Momo x Christoph“, seit Juli 2024 „by Momo x Rudi“.</p></section>' % ''.join(vitrinen))
    s.append(abend_dialoge())
    s.append('<section class="schluss" data-ton="nacht">%s%s<div class="sw auf" style="--i:1">%s</div></section>' % (
        zl(['Das nächste Plakat', 'kommt bestimmt.'], 'h2', 'gross'), sw('Der nächste Termin steht noch nicht fest.'), knopf('Auf die Warteliste', 'abend.html#warteliste')))
    s.append(fuss())
    schreibe('abende.html', ''.join(s))


# ---------------------------------------------------------------- Momo x Rudi
def leute():
    s = [kopf('Team · Culinarium im Walk on the Wild Side', 'Wer hinter Culinarium und seinem Haus, dem Walk on the Wild Side, steht: Derya Ivkin, Momo und Rudi Napieraj.', 'leute.html')]
    s.append('''<section class="seitenkopf breit" data-ton="nacht">
  <div class="sk-text mitte">%s%s</div>
  <div class="sk-bild auf">%s</div>
</section>''' % (zl(['Das Team.'], 'h1', 'gross'),
                 sw('Die Abende von Culinarium und ihr Haus, das Walk on the Wild Side: getragen von denselben Leuten.'),
                 foto('trio2', '', '(max-width:860px) 100vw, 80vw', True, False)))
    # Personen: fakten.json › personen; Geschichte: termine, kueche_2023
    s.append('''<section class="koepfe" data-ton="hell">
  <div class="kopf-reihe">
    <article class="kopf-karte sw auf" style="--i:0"><p class="kk-was mono">Das Haus</p><h2>Derya Ivkin</h2><p>Führt das Walk on the Wild Side, das Haus von Culinarium, seit dem Reopening im November 2023. Eine Karte gibt es bei ihr nicht: Wer an die Theke kommt, bekommt einen Drink nach seinem Geschmack.</p><a class="link" href="https://www.instagram.com/derrisch__/" target="_blank" rel="noopener">@derrisch__</a></article>
    <article class="kopf-karte sw auf" style="--i:1"><p class="kk-was mono">Drinks</p><h2>Momo</h2><p>Steht hinter der Bar und mixt die Signature Drinks, auch die fünf eines Culinarium-Abends, und erklärt jeden selbst. Das erste Pop-up gab es am 20. Mai 2023.</p><a class="link" href="https://www.instagram.com/momo012027/" target="_blank" rel="noopener">@momo012027</a></article>
    <article class="kopf-karte sw auf" style="--i:2"><p class="kk-was mono">Küche</p><h2>Rudi Napieraj</h2><p>Kocht seit 2024 bei Culinarium, drei Gänge an der langen Tafel, und steht beim Pop-up Dirty Chicken in der Küche.</p><a class="link" href="https://www.instagram.com/rudi__san/" target="_blank" rel="noopener">@rudi__san</a></article>
  </div>
</section>''')
    band = ''.join(foto(k, '', '(max-width:860px) 46vw, 18vw', auf=False) for k in ('w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7'))
    s.append('''<section class="werkband" data-ton="nacht">
  <div class="wb-kopf">%s%s</div>
  <div class="wb-wand flaeche auf">%s</div>
</section>''' % (zl(['Bei der Arbeit.'], 'h2', 'gross'), sw('An einem Abend, zwischen Pass, Theke und Tafel.'), band))
    s.append('''<section class="chronik" data-ton="hell">
  %s
  <div class="chronik-zeilen">
    <div class="ch sw auf" style="--i:0"><span class="mono">Oktober 2017</span><p>Das Walk on the Wild Side öffnet in Linden, Haasemannstraße 13.</p></div>
    <div class="ch sw auf" style="--i:1"><span class="mono">Mai 2023</span><p>Erstes Pop-up mit Momo.</p></div>
    <div class="ch sw auf" style="--i:2"><span class="mono">Herbst 2023</span><p>Die ersten Abende unter dem Namen Culinarium, „by Momo x Christoph“.</p></div>
    <div class="ch sw auf" style="--i:3"><span class="mono">November 2023</span><p>Reopening der Bar unter Derya Ivkin. Mixology ohne Karte.</p></div>
    <div class="ch sw auf" style="--i:4"><span class="mono">2024</span><p>Rudi kommt in die Küche von Culinarium, „by Momo x Rudi“.</p></div>
    <div class="ch sw auf" style="--i:5"><span class="mono">2026</span><p>Der September-Abend ist ausgebucht, Dirty Chicken feiert Opening.</p></div>
  </div>
</section>''' % zl(['Wie es kam.'], 'h2', 'gross'))
    s.append('<section class="schluss" data-ton="kerze">%s<div class="knoepfe sw auf">%s%s</div></section>' % (
        zl(['Am besten lernst du', 'sie an der Theke kennen.'], 'h2', 'gross'), knopf('Der Abend', 'abend.html'), knopf('Das Haus', 'bar.html', 'leise')))
    s.append(fuss())
    schreibe('leute.html', ''.join(s))


# ---------------------------------------------------------------- Dirty Chicken
def dirtychicken():
    s = [kopf('Dirty Chicken · Culinarium Hannover', 'Dirty Chicken Hannover, das Pop-up im Walk on the Wild Side: Sandwiches & More, Dirty Food & Dirty Drinks.', 'dirty-chicken.html', 'dc')]
    s.append('''<section class="dc dc-seite-kopf" data-ton="dc">
  <div class="dc-raster">
    <div class="dc-text">%s%s%s</div>
    <div class="dc-buehne">
      <div class="dc-seite links">%s</div>
      <figure class="film hoch auf" style="--lq:url(assets/film/opening.webp)"><video muted playsinline preload="metadata" poster="assets/film/opening.webp?v=%s" data-src="assets/film/opening.mp4?v=%s" aria-label="Opening 2026 bei Dirty Chicken"></video><button class="film-nochmal" type="button" aria-label="Film noch einmal abspielen">Noch einmal</button></figure>
      <div class="dc-seite rechts">%s</div>
    </div>
  </div>
</section>''' % (zl(['Dirty', 'Chicken.'], 'h1', 'gross'),
                 sw('Ein Pop-up mit Sandwiches &amp; More aus der Familie des Walk on the Wild Side, dem Haus von Culinarium. Opening war am 30. Mai 2026 im AM:PM Café im Tiedthof; die nächsten Termine stehen auf Instagram.'),
                 sw('„Dirty Food &amp; Dirty Drinks. Jenau meen Ding wa.“', 'p', 'zitat-dc', 1),
                 foto('dc_tisch', '', '(max-width:860px) 40vw, 16vw', True), VERSION, VERSION, foto('dc_plakat', '', '(max-width:860px) 40vw, 16vw', True)))
    s.append('''<section class="dc dc-zwei" data-ton="dc">
  <div class="dc-burger-raster">
    <div class="dc-paar paar auf">%s%s</div>
    <div>%s%s<div class="sw auf" style="--i:2"><a class="knopf hell" href="https://www.instagram.com/dirtychicken.hannover/" target="_blank" rel="noopener"><span>Instagram @dirtychicken.hannover</span><i>%s</i></a></div></div>
  </div>
</section>''' % (foto('dc_burger', '', '(max-width:860px) 50vw, 28vw', auf=False), foto('dc_team', '', '(max-width:860px) 50vw, 28vw', auf=False),
                 zl(['Dit is keen Burger.', 'Dit Ding is ’ne Ansage.'], 'h2', 'mittel'),
                 sw('Wann und wo es Dirty Chicken als Nächstes gibt, steht zuerst auf Instagram.', 'p', '', 1), PFEIL))
    s.append('<section class="schluss" data-ton="nacht">%s<div class="sw auf">%s</div></section>' % (
        zl(['Zurück zu', 'Culinarium.'], 'h2', 'gross'), knopf('Culinarium', 'index.html')))
    s.append(fuss())
    schreibe('dirty-chicken.html', ''.join(s))


# ---------------------------------------------------------------- Der Weg
def weg():
    s = [kopf('Der Weg · Culinarium Hannover', 'Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover-Linden: die Bar, die Culinarium-Abende und das Pop-up Dirty Chicken.', 'weg.html', 'strasse')]
    # Adresse, Plus Code, Öffnungszeiten der Bar: fakten.json › adresse, anreise, oeffnungszeiten
    s.append('''<section class="weg-kopf" data-ton="strasse">
  <div class="weg-raster">
    <div class="weg-text">
      %s
      %s
      <dl class="weg-daten">
        <div class="sw auf" style="--i:2"><dt class="mono">Adresse</dt><dd>Walk on the Wild Side<br>Haasemannstraße 13<br>30449 Hannover</dd></div>
        <div class="sw auf" style="--i:3"><dt class="mono">Plus Code</dt><dd>9PC7+49 Hannover</dd></div>
        <div class="sw auf" style="--i:4"><dt class="mono">Culinarium</dt><dd>Freitag ab 19:00<br>Samstag ab 17:00</dd></div>
        <div class="sw auf" style="--i:5"><dt class="mono">Die Bar</dt><dd>Donnerstag 19:00 bis 01:00<br>Freitag und Samstag 19:00 bis 02:00<br><a href="tel:+491633909578">+49 163 3909578</a></dd></div>
      </dl>
      <div class="sw auf" style="--i:6">%s</div>
    </div>
    <div class="weg-bild auf">%s</div>
  </div>
</section>''' % (zl(['Haasemann-', 'straße 13.'], 'h1', 'gross'),
                 sw('Linden-Mitte. Die Bar heisst Walk on the Wild Side, am Schild über der Hausecke erkennst du sie schon von weitem.', 'p', '', 1),
                 knopf('In Google Maps öffnen', 'https://www.google.com/maps/search/?api=1&query=Walk+on+the+Wild+Side+Haasemannstra%C3%9Fe+13+30449+Hannover'),
                 foto('schildnah', '', '(max-width:860px) 100vw, 40vw', True, False)))
    s.append('''<section class="weg-band" data-ton="nacht">
  <div class="wegbilder flaeche auf">%s%s%s</div>
  <p class="ueber sw auf">Die Bar an der Hausecke, Haasemannstraße 13.</p>
</section>''' % (foto('fensterdraussen', '', '(max-width:860px) 92vw, 30vw', auf=False), foto('barnacht', '', '(max-width:860px) 46vw, 30vw', auf=False),
                 foto('schildnacht', '', '(max-width:860px) 46vw, 30vw', auf=False)))
    s.append('<section class="schluss" data-ton="kerze">%s<div class="sw auf">%s</div></section>' % (
        zl(['Bis zum', 'nächsten Abend.'], 'h2', 'gross'), knopf('Auf die Warteliste', 'abend.html#warteliste')))
    s.append(fuss())
    schreibe('weg.html', ''.join(s))


# ---------------------------------------------------------------- Rechtliches (Gerüst, Vertragspartner offen)
def recht(name, titel, abschnitte):
    s = [kopf('%s · Culinarium Hannover' % titel, titel + ' von Culinarium Hannover.', name)]
    inner = ''.join('<div class="recht-block sw auf"><h2>%s</h2>%s</div>' % (h, ''.join('<p>%s</p>' % p for p in ps)) for h, ps in abschnitte)
    s.append('<section class="recht" data-ton="hell"><div class="recht-satz">%s%s</div></section>' % (zl([titel + '.'], 'h1', 'gross'), inner))
    s.append(fuss())
    schreibe(name, ''.join(s))


def rechtstexte():
    recht('impressum.html', 'Impressum', [
        ('Anbieter', ['Die Angaben zum Anbieter nach § 5 DDG werden vor dem Start eingetragen: Name oder Firma, Anschrift, Vertretung, Kontakt.']),
        ('Kontakt', ['Telefon und E-Mail folgen mit den Angaben des Anbieters.']),
        ('Verantwortlich für den Inhalt', ['Name und Anschrift nach § 18 Abs. 2 MStV folgen.']),
        ('Bilder', ['Fotos: Culinarium und Dirty Chicken Hannover. Plakate: Culinarium.']),
    ])
    recht('datenschutz.html', 'Datenschutz', [
        ('Verantwortlicher', ['Die Angaben zum Verantwortlichen folgen mit dem Impressum.']),
        ('Diese Website', ['Die Seite lädt keine Inhalte von Dritten und setzt keine Cookies. Schriften und Bilder liegen auf demselben Server.']),
        ('Warteliste und Anfragen', ['Was du in die Warteliste, eine Anfrage für eure Feier, einen Gutschein oder eine Nachricht an uns einträgst (Name, E-Mail oder Telefon, Tag, Plätze und deine Zeilen), geht verschlüsselt an das Team von Culinarium. Es liegt nur so lange auf einem Server in Frankfurt am Main, bis das Team es abholt, danach allein beim Team. Nach zwölf Monaten wird es gelöscht, auf Wunsch sofort: schreib uns oder ruf in der Bar an.']),
        ('Frag uns zum Abend', ['Was du den Chat fragst, wird mit seiner Antwort gespeichert und geht auf demselben Weg an das Team, damit es Fragen ohne Antwort selbst beantworten kann. Dein Name und deine Adresse gehören nicht dazu, ein Cookie wird nicht gesetzt; eine Prüfsumme, die jeden Tag wechselt, begrenzt nur, wie oft ein Gerät fragen kann.']),
        ('Deine Rechte', ['Auskunft, Berichtigung, Löschung, Einschränkung, Widerspruch und Datenübertragbarkeit nach Art. 15 bis 21 DSGVO; Beschwerde bei der Landesbeauftragten für den Datenschutz Niedersachsen.']),
    ])


SEITEN = ('index', 'abend', 'abende', 'bar', 'leute', 'weg', 'dirty-chicken', 'termine-pflege', 'impressum', 'datenschutz')


def knopf_auf(text, art, cls=''):
    """Knopf des Hauses, der eine Karte von anfrage.js öffnet (ohne JS: Sprung auf #anfrage-…)."""
    return knopf(text, '#anfrage-' + art, cls).replace('<a class="knopf', '<a data-anfrage="%s" class="knopf' % art, 1)


GUTSCHEIN_BILD = ('<img src="assets/gutschein/vorn.webp?v=%s" width="1000" height="472" loading="lazy" decoding="async" '
                  'alt="Der Gutschein: Rudis Plakat und «Ein Abend an der langen Tafel»">')


def zugang(art, breit=False):
    """Sichtbare Zugänge (Robert 29.10.2026: «wie kommt man zu den Sachen?»): Gutschein und lange Tafel als Kachel mit Bild, Satz mit Wertigkeit und Knopf."""
    if art == 'gutschein':
        bild = '<figure class="zg-bild zg-gutschein sw auf" style="--i:0">%s</figure>' % (GUTSCHEIN_BILD % VERSION)
        text = ('<p class="zg-k mono">Gutschein</p>' + zl(['Einen Abend', 'verschenken.'], 'h3', 'mittel zg-t') +
                sw('Ein Abend an der langen Tafel als Geschenk: drei Gänge von Rudi, fünf Drinks von Momo, für einen Menschen, der dir wichtig ist.', 'p', 'zg-s', 2) +
                '<div class="sw auf" style="--i:3">%s</div>' % knopf_auf('Gutschein anfragen', 'gutschein'))
    else:
        bild = '<div class="zg-bild sw auf" style="--i:0">%s</div>' % foto('t09', 'zg-foto', '(max-width:860px) 100vw, 40vw', auf=False)
        text = ('<p class="zg-k mono">Eigene Feier</p>' + zl(['Die lange Tafel', 'für euch.'], 'h3', 'mittel zg-t') +
                sw('Geburtstag, Team, ein Abend unter Freunden: Die lange Tafel im Walk on the Wild Side gibt es auch für eure eigene Feier. Erzählt uns, was ihr vorhabt.', 'p', 'zg-s', 2) +
                '<div class="sw auf" style="--i:3">%s</div>' % knopf_auf('Die lange Tafel anfragen', 'feier'))
    return '<article class="zg%s">%s<div class="zg-text">%s</div></article>' % (' zg-breit' if breit else '', bild, text)


def anfrage_einbau():
    """Anschluss ans Gästebuch (29.10.2026, Oberchef): assets/anfrage.css und anfrage.js in jede Seite; sichtbare Zugänge (26199): Gutschein auf Startseite
    und Der Abend, die lange Tafel auf Startseite und Alle Abende, «Schreib uns» als Knopf in der Kontaktspalte des Fusses und auf Der Weg.
    Den Chat (Eckfenster unten rechts) setzt anfrage.js selbst.
    Die Karte selbst baut anfrage.js; Links auf die Warteliste öffnen sie. Läuft nach varianten.py (wie handy_css), mehrfach ohne sich zu verdoppeln."""
    beide = '<section class="zugaenge" data-ton="nacht" aria-label="Schenken und feiern"><div class="zg-reihe">%s%s</div></section>' % (zugang('gutschein'), zugang('feier'))
    band = lambda art: '<section class="zugaenge" data-ton="nacht" aria-label="%s"><div class="zg-reihe">%s</div></section>' % (
        'Einen Abend verschenken' if art == 'gutschein' else 'Die lange Tafel für euch', zugang(art, breit=True))
    schreib = '<button class="knopf" type="button" data-anfrage="nachricht"><span>Schre<em class="ki">i</em>b uns</span><i>%s</i></button>' % PFEIL
    for n in SEITEN:
        p = os.path.join(HIER, n + '.html')
        if not os.path.exists(p) or n == 'termine-pflege':
            continue
        h = open(p, encoding='utf-8').read()
        h = re.sub(r'\n?<link rel="stylesheet" href="assets/anfrage\.css[^>]*>', '', h)
        h = re.sub(r'\n?<script src="assets/anfrage\.js[^>]*></script>', '', h)
        h = h.replace('</head>', '<link rel="stylesheet" href="assets/anfrage.css?v=%s">\n</head>' % VERSION, 1)
        h, k = re.subn(r'(<script src="assets/culinarium\.js\?v=[^"]*" defer></script>)',
                       r'\1\n<script src="assets/anfrage.js?v=%s" defer></script>' % VERSION, h, count=1)
        if not k:
            raise SystemExit('anfrage_einbau: %s ohne culinarium.js' % n)
        # «Schreib uns»: als Knopf in der Kontaktspalte des Fusses (Das Haus, neben dem Telefon der Bar)
        if 'data-anfrage="nachricht"' not in h:
            h, k = re.subn(r'(<a class="fu-link" href="tel:\+491633909578">[^<]*</a>)', lambda m: m.group(1) + schreib, h, count=1)
            if not k:
                raise SystemExit('anfrage_einbau: %s ohne Telefon in der Kontaktspalte des Fusses' % n)
        def vor(marke, html, was):
            i = h.find(marke)
            if i < 0:
                raise SystemExit('anfrage_einbau: %s ohne %s' % (n, was))
            return h[:i] + html + h[i:]
        if n == 'index' and 'class="zugaenge"' not in h:      # Startseite: Gutschein und lange Tafel nebeneinander, vor «Bis zum nächsten Abend»
            h = vor('<section class="vab v-bisbald', beide, 'Bis bald')
        if n == 'abend' and 'class="zugaenge"' not in h:      # Der Abend: Gutschein direkt nach der Warteliste
            i = h.find('id="warteliste"'); j = h.find('</section>', i)
            if i < 0 or j < 0:
                raise SystemExit('anfrage_einbau: abend.html ohne Warteliste')
            h = h[:j + 10] + band('gutschein') + h[j + 10:]
        if n == 'abende' and 'class="zugaenge"' not in h:     # Alle Abende: die lange Tafel vor dem letzten Fenster
            h = vor('<section class="vab bar-ab v-schluss', band('feier'), 'Schlussfenster')
        if n == 'weg' and 'data-anfrage="nachricht" class="knopf' not in h:   # Der Weg: «Schreib uns» neben der Warteliste
            h, k = re.subn(r'(<div class="knoepfe[^"]*"[^>]*><a class="knopf" href="abend\.html#warteliste".*?</a>)', lambda m: m.group(1) + knopf_auf('Schreib uns', 'nachricht', 'leise'), h, count=1, flags=re.S)
            if not k:
                raise SystemExit('anfrage_einbau: weg.html ohne die Knöpfe mit der Warteliste')
        open(p, 'w', encoding='utf-8').write(h)
    print('anfrage.js/.css in', len(SEITEN) - 1, 'Seiten; «Schreib uns» als Knopf im Fuss und auf Der Weg, Gutschein auf Startseite und Der Abend, lange Tafel auf Startseite und Alle Abende')


# Seiten, deren grösste Bilder im ersten Bildschirm nicht die ersten zwei im Quelltext sind (gemessen 30.10.2026, Chromium 1440 und 390):
# Bar: am Rechner das Negativ der Bar, am Handy das breite Bild d3 (153 000 px² von 290 000 sichtbar)
# Dirty Chicken: zwölf Kacheln im ersten Bildschirm, alle mit Vorrang hielten die CSS auf (live gedrosselt 3,0 s bis zum ersten Bild); nur drei leichte, an Rechner und Handy sichtbare
ZUERST = {'bar': ['barneg', 'd3'], 'dirty-chicken': ['dc_drink', 'dn_glas', 'dn_bar']}

def hero_sofort():
    """Erster Bildschirm (Robert 29.10.2026: «wenn ich die Dirty Chicken Seite lade, laden die Bilder im Hero erst spät»; Oberchef: auf allen Seiten).
    Läuft nach varianten.py über die fertigen Seiten: im ersten Kind von <main> wird jedes Bild sofort geladen (src/srcset statt data-srcset, kein loading="lazy"),
    die zuerst sichtbaren bekommen fetchpriority="high" und einen preload im Kopf mit imagesrcset/imagesizes passend zur Breite, jedes Bild ohne Abbild-Grund
    (--lq) bekommt die Motivfarbe als Grund statt Dunkel. Dirty Chicken: vier Säulen, zwei davon laufen von der Hälfte aus, dort sind die Doppel (6, 7) zuerst
    im Bild; sie zeigen dieselben Dateien wie 1 und 2. Alles Weitere lädt wie gehabt verzögert."""
    import base64
    VOID = ('img', 'source', 'br', 'input', 'link', 'meta', 'use', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'stop', 'textpath')
    def farbe(k):
        m = META.get(k)
        if not m or not m.get('lq'):
            return None
        try:
            im = Image.open(io.BytesIO(base64.b64decode(m['lq'].split(',', 1)[1]))).convert('RGB').resize((1, 1), Image.BOX)
            return '#%02x%02x%02x' % im.getpixel((0, 0))
        except Exception:
            return None
    def erstes_kind(h):
        a = h.find('<main id="inhalt">')
        if a < 0:
            return None
        a = h.find('<', a + 18)
        tiefe, pos = 0, a
        for m in re.finditer(r'<(/?)([a-zA-Z0-9-]+)[^>]*?(/?)>', h[a:]):
            tn = m.group(2).lower()
            if m.group(1):
                tiefe -= 1
                if tiefe == 0:
                    return a, a + m.end()
            elif not m.group(3) and tn not in VOID:
                tiefe += 1
        return None
    n_seiten = 0
    for n in SEITEN:
        p = os.path.join(HIER, n + '.html')
        if not os.path.exists(p) or n in ('termine-pflege', 'impressum', 'datenschutz'):
            continue
        h = open(p, encoding='utf-8').read()
        h = re.sub(r'\n?<link rel="preload" as="image"[^>]*>', '', h)
        ab = erstes_kind(h)
        if not ab:
            continue
        a, b = ab
        seg = h[a:b]
        imgs = list(re.finditer(r'<img\b[^>]*>', seg))
        if not imgs:
            continue
        # welche Bilder zuerst im Bild stehen: Dirty-Chicken-Säulen je Säule die ersten zwei (bei den Säulen von der Hälfte aus die Doppel 6, 7 = gleiche Dateien), sonst die ersten zwei
        hoch, lazy_bleibt = set(), set()
        if 'am-saeulen' in seg:
            for sm in re.finditer(r'<div class="am-s am-s(\d)"[^>]*>(.*?)</div></div>', seg, re.S):
                fig = [x.start() + sm.start(2) for x in re.finditer(r'<img\b', sm.group(2))]
                for i in ([0, 1, 5, 6] if sm.group(1) in '13' else [0, 1]):
                    if i < len(fig):
                        hoch.add(fig[i])
                for i, f in enumerate(fig):   # Kacheln 4, 5, 9, 10 je Säule sind erst nach dem Lauf im Bild: bleiben lazy, damit sie nicht mit dem ersten Bild konkurrieren
                    if i in (3, 4, 8, 9):
                        lazy_bleibt.add(f)
        else:
            hoch = {m.start() for m in imgs[:2]}
        if n in ZUERST:
            hoch = {m.start() for m in imgs if any('assets/bild/%s-' % k in m.group(0) for k in ZUERST[n])}
        vorladen, neu, versatz = [], [], 0
        for m in imgs:
            t = m.group(0)
            srcset = re.search(r'\bdata-srcset="([^"]*)"', t)
            if srcset:
                sizes = (re.search(r'\bdata-sizes="([^"]*)"', t) or [None, '100vw'])[1]
                klein = srcset.group(1).split(',')[0].split()[0]
                t = re.sub(r'\bdata-srcset="[^"]*"', 'src="%s" srcset="%s" sizes="%s"' % (klein, srcset.group(1), sizes), t)
                t = re.sub(r'\s*\bdata-sizes="[^"]*"', '', t)
            if m.start() not in lazy_bleibt:
                t = re.sub(r'\s*\bloading="lazy"', '', t)
            t = re.sub(r'\s*\bfetchpriority="[^"]*"', '', t)
            if m.start() in hoch:
                t = t.replace('<img ', '<img fetchpriority="high" ', 1)
                ss = re.search(r'\bsrcset="([^"]*)"', t); sz = re.search(r'\bsizes="([^"]*)"', t)
                if ss and ss.group(1) not in [v[0] for v in vorladen]:
                    vorladen.append((ss.group(1), sz.group(1) if sz else '100vw'))
            neu.append((m.start(), m.end(), t))
        aus, letzte = [], 0
        for st, en, t in neu:
            aus.append(seg[letzte:st]); aus.append(t); letzte = en
        aus.append(seg[letzte:])
        seg = ''.join(aus)
        # Motivfarbe als Grund für Rahmen ohne Abbild (--lq)
        def grund(m):
            fig, img = m.group(0), m.group(1)
            if '--lq' in fig or 'style="' in fig[:fig.find('>')]:
                return fig
            k = re.search(r'assets/bild/([a-z0-9_]+)-\d+\.webp', img)
            f = farbe(k.group(1)) if k else None
            return fig.replace('<figure', '<figure style="background:%s"' % f, 1) if f else fig
        seg = re.sub(r'<figure(?:\s[^>]*)?>\s*(<img\b[^>]*>)', grund, seg)
        h = h[:a] + seg + h[b:]
        links = ''.join('\n<link rel="preload" as="image" imagesrcset="%s" imagesizes="%s" fetchpriority="high">' % v for v in vorladen[:4])
        # Tapete der violetten Karte (Dirty Chicken): Grund aus der CSS, unversioniert, war der späteste Teil des ersten Bildschirms
        for tap in sorted(set(re.findall(r'zeichen/tapete-[a-z]+\.svg', seg))):
            links += '\n<link rel="preload" as="image" href="assets/%s">' % tap
        # am-schild: Tapete steht seit 30.10.2026 als Daten in culinarium.css (--tapete-dc), kein preload mehr
        if links:
            h = h.replace('</title>', '</title>' + links, 1)
        open(p, 'w', encoding='utf-8').write(h)
        n_seiten += 1
    print('Hero sofort:', n_seiten, 'Seiten (erster Bildschirm eager, fetchpriority, preload, Motivfarbe)')


def handy_css():
    """Handy-Fassung (28.10.2026): assets/handy.css als letzte Stilschicht in jede Seite, nach allen Seiten-Stilen (abend-auftakt, buchen, ueberleitung, dirty-chicken).
    Läuft nach varianten.py und seinen Unterskripten, weil die ihre Stile vor </head> nachschieben."""
    for n in SEITEN:
        p = os.path.join(HIER, n + '.html')
        if not os.path.exists(p):
            continue
        h = open(p, encoding='utf-8').read()
        h = re.sub(r'\n?<link rel="stylesheet" href="assets/handy\.css[^>]*>', '', h)
        h = h.replace('</head>', '<link rel="stylesheet" href="assets/handy.css?v=%s">\n</head>' % VERSION, 1)
        open(p, 'w', encoding='utf-8').write(h)
    print('handy.css in', len(SEITEN), 'Seiten')


if __name__ == '__main__':
    META.update(bilder())
    filme()
    zeichen()
    startseite()
    abend()
    abende()
    leute()
    dirtychicken()
    weg()
    rechtstexte()
    # Die gültigen Seiten baut varianten.py; ohne diesen Schritt stünden hier alte Fassungen (26.10.2026)
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'varianten.py')], check=True)
    anfrage_einbau()
    hero_sofort()
    handy_css()
