# Inhalt des Konzept-Boards, Station 06, Culinarium Hannover (26.10.2026).
# Jede Angabe hat eine Quelle im Projektordner; Sätze des Hauses stehen in «…» mit Fundstelle.
# Stationen 04 und 05 liegen noch nicht vor: Farben aus den Plakaten (fakten.json › marke), Akzent aus den Fotos gemessen, Titelschrift Fraunces wie beim Späher (vorläufig).
V = '_quelle/vom-kunden/'
D = V + 'drive/'
IG = '_quelle/extern/ig/'
DC = '_quelle/dirty-chicken/'

# Bilder: Schlüssel → (Datei, Breite, Höhe)
B = {
    'momo':      (D + '4568.jpg', 5304, 6630),
    'rudi':      (D + '5301.jpg', 5304, 7952),
    'glas':      (D + '5369.jpg', 5304, 7952),
    'teller':    (D + '5379.jpg', 7952, 5304),
    'tafelleer': (D + '4972.jpg', 1638, 2048),
    'schild':    (D + '4096.jpg', 1536, 2048),
    'fassade':   (D + '4951.jpg', 1638, 2048),
    'flur':      (D + '3887.jpg', 1536, 2048),
    'wandloch':  (D + '4029.jpg', 1536, 2048),
    'licht':     (D + '3998.jpg', 1536, 2048),
    'kanister':  (V + '3937.jpg', 1536, 2048),
    'milch':     (V + '4313.jpg', 1536, 2048),
    'schaum':    (D + '63963.jpg', 2498, 3330),
    'bar':       (D + '3823.jpg', 1536, 2048),
    'feige':     (D + '4876.jpg', 1638, 2048),
    'pass':      (V + '36740.png', 2582, 1936),
    'kohl':      (D + '4298.jpg', 1536, 2048),
    'spritz':    (D + '4921.jpg', 1536, 2048),
    'zwiebel':   (D + '5045.jpg', 1638, 2048),
    'highball':  (D + '4858.jpg', 1638, 2048),
    'bete':      (D + '4890.jpg', 1638, 2048),
    'milchglas': (D + '4893.jpg', 1638, 2048),
    't01': (D + '5005.jpg', 1638, 2048), 't02': (D + '5022.jpg', 1638, 2048), 't03': (D + '3842.jpg', 1536, 2048),
    't04': (D + '3916.jpg', 1536, 2048), 't05': (D + '3858.jpg', 1536, 2048), 't06': (D + '5376.jpg', 5304, 7952),
    't07': (D + '36543.jpg', 1366, 2048), 't08': (D + '36913.jpg', 1366, 2048), 't09': (D + '4024.jpg', 1638, 2048),
    't10': (D + '3855.jpg', 1536, 2048), 't11': (D + '3901.jpg', 1536, 2048), 't12': (D + '4004.jpg', 1536, 2048),
    't13': (D + '4574.jpg', 5304, 7952), 't14': (D + '37016.jpg', 1366, 2048),
    'p_ski':     (IG + '2024-11-06_culinarium_hannover_DCCf-ikoaGs-1.jpg', 1440, 1432),
    'p_sessel':  (IG + '2025-02-04_culinarium_hannover_DFqbLG2s_dc-1.jpg', 1440, 1432),
    'p_garten':  (IG + '2025-05-17_culinarium_hannover_DJw8OqGMY1G-1.jpg', 1440, 1432),
    'p_kuerbis': (IG + '2025-10-13_culinarium_hannover_DPwlqcfiKcA-1.jpg', 1440, 1432),
    'p_panther': (IG + '2026-03-06_culinarium_hannover_DVjkofijp6R-1.jpg', 1440, 1432),
    'p_mond':    (IG + '2026-07-29_culinarium_hannover_DbYnkdkjrNy-1.jpg', 2014, 2003),
    'trio':      (D + '63873.jpg', 4004, 3003),
    'dc_burger': (DC + 'ig/2026-06-03_dirtychicken.hannover_DZId0KMoAtq-1.jpg', 1440, 1440),
    'dc_tisch':  (DC + 'ig/2026-06-03_dirtychicken.hannover_DZIo4FHIqRR-1.jpg', 1440, 1440),
    'dc_liebe':  (DC + 'ig/2026-06-13_dirtychicken.hannover_DZiug6EoMRr-1.jpg', 1440, 1440),
    'kueche':    (V + '36829.jpg', 788, 1402),
    'anstossen': (D + '4026.jpg', 1638, 2048),
}

# Filme: Schlüssel → (Datei, Breite, Höhe, Sekunden)
F = {
    'familie': (DC + 'video/2026-06-03_dirtychicken.hannover_DZIjZWNCGZT-3.mp4', 720, 720, 11),
    'opening': (DC + 'video/2026-06-06_dirtychicken.hannover_DZPYEOJIfVb-1.mp4', 720, 1280, 33),
    'teilen':  (D + '52799.mp4', 1920, 1080, 16),
}

K = 'http://127.0.0.1:8978/haus/'
HAEUSER = {
    'Grand Beau-Rivage': 'http://localhost:8940/',
    'Carlton-Europe': 'https://carlton-europe-entwurf.vercel.app/',
    'Hotel Seiler au Lac': 'http://localhost:8921/',
    'Waldhotel Doldenhorn': 'https://waldhotel-doldenhorn-entwurf.vercel.app/',
    'Landgasthof Ruedihus': 'https://landgasthof-ruedihus-entwurf.vercel.app/',
    'Berghotel Gasterntal': 'https://berghotel-gasterntal-entwurf.vercel.app/',
    'Salt & Silver': 'https://salt-and-silver-studie.vercel.app/',
    'Taverne zum Schäfli': K + 'Taverne%20zum%20Sch%C3%A4fli%20Wigoltingen/_kette/06-konzepter/konzept.html',
    'Wirtschaft am Schlössli': K + 'Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen/_kette/06-konzepter/konzept.html',
    'Zurbriggen Wellness': K + 'Zurbriggen%20Wellnesshotel%20Saas-Almagell/_kette/06-konzepter/konzept.html',
    'Zurbriggen Monte-Moro': K + 'Zurbriggen%20Hotel%20Monte-Moro%20Saas-Almagell/_kette/06-konzepter/konzept.html',
    'Castell Son Claret': None,
}

GESCHICHTE_SATZ = ('Einer kocht, einer mixt und erklärt, vierzehn Gäste sitzen an einer langen Tafel in einer Bar in Linden: '
                   'Die Seite läuft wie ein Culinarium-Abend, Gang für Gang, und jeder Gang ist ein Paar aus Teller und Glas.')
GESCHICHTE = ('Die Konzepte und die Menschen bekommen keine eigenen Abteilungen, sie kommen in der Reihenfolge des Abends an den Tisch: '
              'erst die Strasse und die Tür, dann Momo mit dem ersten Glas, dann Rudis Teller, dann die Tafel, die Plakate aller bisherigen Abende, '
              'die Leute dahinter und zum Schluss Rudis zweite Küche, Dirty Chicken. Am Ende steht der nächste Abend. '
              'Ordnung gibt, was Culinarium selbst schon hat: das Paar (Momo x Rudi, Teller und Drink), das warmweisse Band mit der doppelt gerahmten Wortmarke von den Plakaten '
              'und Rudis Art, ein Gericht in vier Wörtern zu schreiben.')

# Robert 26.10.2026: «wie wir die Geschichte mit diesen ganzen Konzepten und den ganzen Menschen erzählen wollen»
WEGE = [
    ('Empfohlen', 'Ein Abend, Gang für Gang',
     'Die Startseite ist der Abend selbst: ankommen, Aperitif, drei Gänge, die Tafel, der Absacker. Jedes Konzept und jeder Mensch sitzt an der Stelle, an der er an so einem Abend dran ist: Momo beim ersten Glas, Rudi beim Teller, alle zusammen an der Tafel, Dirty Chicken als zweite Küche nach dem Dessert. Wer die Seite einmal herunterscrollt, war einmal da.',
     ['momo', 'rudi']),
    ('Überlegt', 'Die Ausgaben',
     'Die Seite als Zeitschrift, jedes Konzept eine Ausgabe mit eigenem Plakat. Trägt nicht die ganze Seite: Die Plakate gibt es nur in Instagram-Grösse, die Rechte an den Illustrationen sind offen, und eine Grafik statt eines echten Fotos im Auftakt ist bei Robert noch nie durchgegangen. Bleibt als eigenes Kapitel, die Plakatwand.',
     ['p_mond', 'p_panther']),
    ('Überlegt', 'Die Menschen führen',
     'Rudi, Momo und Derya je ein Kapitel mit ihrem Konzept. Scheitert heute am Material: Es gibt keine einzige Zeile über die drei ausserhalb von Instagram, die Texte entstehen erst im Gespräch, und wer auf welchem Foto ist, ist nicht belegt. Die Menschen tragen deshalb die Gänge, statt eigene Abteilungen zu bekommen; das Familien-Video ist ihr Kapitel.',
     ['trio']),
]

# Ideen, die es bei Tasty Studios noch nicht gab: (Art, Name, Satz)
IDEEN = [
    ('Darstellung', 'Das Paar',
     'Was Culinarium verkauft, ist ein Paar: ein Teller von Rudi, ein Glas von Momo. Die Seite zeigt deshalb fast nie ein Bild allein, sondern zwei nebeneinander, Wand an Wand, links das Essen, rechts das Glas oder links Momo, rechts Rudi. Die Naht zwischen beiden ist die Mitte jedes Kapitels.'),
    ('Bewegung', 'Anstossen',
     'Die beiden Hälften eines Paars steigen getrennt von unten herauf, die zweite eine Achtelsekunde später, und treffen sich an der Naht mit einem gemeinsamen, einzigen Puls, wie zwei Gläser, die sich berühren. Nichts kommt von der Seite, nichts geht auf wie eine Tür. Die Fotos 4024, 4026, 5376 und 4574 zeigen genau diesen Moment.'),
    ('Beschriftung', 'Das Band',
     'Auf jedem Plakat seit 2023 sitzt die Wortmarke in einem warmweissen Band mit doppeltem Rahmen. Dieses Band beschriftet die Seite: Namen der Gänge, Datum, Menschen, der nächste Abend. Es ersetzt Einkerbungen, Etiketten und Kicker, und es kommt vom Haus, nicht aus unserem Fundus.'),
    ('Satz', 'Vier Wörter',
     'Rudi schreibt ein Gericht als Zutatenzeile: «AUBERGINE / KOKOS / LIMETTE / SESAM». Diese Zeile ist die Überschrift der Gänge, gross in der Titelschrift, und Momos Techniken bekommen dieselbe Form: «FATWASHING / MILKWASHING / ENZYME».'),
]

# Bühne: Skizze mit echten Bildern, Masse in Hundertsteln der Breite (cqw). el: (art, …)
SZENEN = [
    dict(teil='auftakt', titel='Momo x Rudi.', flaeche='dunkel',
         satz='Zwei Hochformate Wand an Wand über die ganze Breite, links der Shaker an der Bar, rechts der Koch am Tisch, über der Naht das Band mit CULINARIUM und der Zeile der Plakate. Darunter der nächste Abend und ein Knopf.',
         bilder=['momo', 'rudi'],
         stage=dict(h=56, el=[
             ('bild', 'momo', 0, 0, 50, 56, '50% 30%'), ('bild', 'rudi', 50, 0, 50, 56, '50% 30%'),
             ('band', 'CULINARIUM', 'A unique experience by Momo x Rudi', 27, 30, 46),
             ('knopf', 'Auf die Warteliste', 41.5, 47.5)]),
         einfall='Die Zeile der Plakate heisst «A UNiQUE EXPERiENCE BY MOMO X RUDI». Der Auftakt nimmt sie wörtlich: zwei Menschen, ein x dazwischen.',
         komposition='Zwei Hälften, kein Gebäude, kein Teller allein. Das Band liegt quer über der Naht und hält beide zusammen. Am Handy stehen die Hälften schmal nebeneinander, das Band darüber, der Knopf im ersten Bildschirm.',
         moment='Beim Öffnen steigen beide Hälften herauf und stossen an der Naht an, das Band rollt aus dem Schlitz, im selben Takt.',
         baustein='Das Paar', quelle='neu',
         skizze='Paare zur Wahl, Robert entscheidet: A Momo | Rudi (4568 | 5301, Tageslicht, beide über 5000 Pixel), B Glas | Teller (5369 | 5379, dunkel, 7952 Pixel), C die leere Tafel mit Kerzen allein (4972, nur 1638 Pixel breit). Kein Preis im Auftakt; steht ein Datum fest, kommt es ins Band unter die Wortmarke, sonst führt der Knopf auf die Warteliste.',
         bewegung='Anstossen: links von unten, rechts eine Achtelsekunde später, ein Puls an der Naht; Band aus dem Schlitz.',
         unterschied='Kein Haus hatte einen Auftakt aus zwei gleichwertigen Bildern. Die Hälften öffnen nicht wie Türflügel (das Carlton), sie kommen von unten zusammen.',
         bisher={'Carlton-Europe': 'Türflügel, Bild zuerst', 'Grand Beau-Rivage': 'Foto mit Name über die ganze Fläche', 'Waldhotel Doldenhorn': 'Foto mit Name, Satz zuerst',
                 'Hotel Seiler au Lac': 'Dunst über dem See', 'Taverne zum Schäfli': 'Gegenstand gross, Name zuerst, Ortsname', 'Salt & Silver': 'Vorhang mit Zeichen'}),

    dict(teil='strasse', titel='Haasemannstraße 13.', flaeche='hell',
         satz='Der Weg hinein in drei Bildern, die von draussen nach drinnen wärmer werden: das Schild in der Nacht, der Flur mit der offenen Tür, der gedeckte Tisch.',
         bilder=['schild', 'flur', 'fassade'],
         stage=dict(h=46, el=[
             ('text', 'Haasemannstraße 13', 4, 3, 40, 'ort'),
             ('text', 'Linden-Mitte, im Walk on the Wild Side. Freitag ab sieben, Samstag ab fünf.', 4, 11.5, 34, 'lauf'),
             ('bild', 'schild', 42, 0, 17, 46, '50% 40%'), ('bild', 'flur', 59, 0, 20, 46, '50% 50%'), ('bild', 'fassade', 79, 0, 21, 46, '50% 50%')]),
         einfall='Der Abend beginnt auf der Strasse: Die Plakate stehen unter dem Kopf «WALK ON THE WILD SIDE», die Bar ist der Gastgeber. Der Ortsname ist die Überschrift, geschrieben wie bei Google Maps (Haasemannstraße), nicht wie in den Beiträgen.',
         komposition='Drei Hochformate Wand an Wand rechts, Ortsname und eine Zeile links. Die Bilder werden von links nach rechts wärmer: Blau der Strasse, Orange im Flur.',
         moment='Die drei Bilder kommen als eine Fläche gemeinsam herauf, ohne Staffel, und zoomen leise in ihre Rahmen.',
         baustein='Wand an Wand', quelle='fundus',
         bewegung='Hochschweben als Fläche gemeinsam, leiser Zoom.',
         unterschied='Ein Weg von draussen nach drinnen in drei Schritten, über die Farbe des Lichts erzählt. Die Bar wird als Gastgeber genannt, nicht als eigenes Haus gezeigt.',
         bisher={'Taverne zum Schäfli': 'Region als Strassenzug, langes Band mit Abzügen', 'Berghotel Gasterntal': 'Der Weg hinauf als Faden der ganzen Seite', 'Zurbriggen Wellness': 'Anreise als Mittelachse'}),

    dict(teil='fenster', titel='Durch die Wand.', flaeche='bild',
         satz='Das einzige Fenster der Seite ist ein echtes Loch in der Wand der Bar, durch das man auf einen Tisch mit Kerzen sieht.',
         bilder=['wandloch'],
         stage=dict(fenster='wandloch', satz='Hinter der Wand ist der Tisch schon gedeckt.'),
         einfall='Das Foto 4029 ist schon ein Fenster: ein Durchbruch im Putz, dahinter Kerzen und Flaschen.',
         komposition='Fenster mit stehendem Bild, Satz rechts unten im weichen Hof.',
         moment='Der Ausschnitt geht auf, der Satz rollt zeilenweise.',
         baustein='Fenster', quelle='fundus',
         bewegung='Fenster, Bild steht, Satz aus dem Schlitz.',
         unterschied='Nur ein Fenster auf der ganzen Startseite, und das Bild ist selbst eine Öffnung in der Wand. Fenster als Übergang steht bei sieben Häusern; die anderen Übergänge laufen hier über das Paar.',
         bisher={'Grand Beau-Rivage': 'fünf Fenster', 'Carlton-Europe': 'drei Fenster', 'Landgasthof Ruedihus': 'drei Fenster, Bild wandert gegen die Scrollrichtung', 'Waldhotel Doldenhorn': 'drei Fenster'}),

    dict(teil='aperitif', titel='FATWASHING / MILKWASHING / ENZYME', flaeche='dunkel',
         satz='Momos Kapitel. Die drei Techniken aus den Beiträgen stehen als Zutatenzeile in Rudis Schreibweise; wer ein Wort antippt, tauscht das grosse Bild an derselben Stelle.',
         bilder=['milch', 'kanister', 'schaum', 'bar'],
         stage=dict(h=50, el=[
             ('bild', 'milch', 0, 0, 38, 50, '50% 50%'), ('bild', 'bar', 38, 0, 24, 50, '50% 30%'),
             ('worte', ['FATWASHING', 'MILKWASHING', 'ENZYME'], 66, 6, 32),
             ('text', '«Momo wird persönlich jeden Drink für dich erklären.»', 66, 30, 30, 'zitat'),
             ('band', 'Fünf Drinks', 'zu drei Gängen', 66, 40, 26)]),
         einfall='«Hierbei kannst du in eine Welt spannender Techniken wie Fatwashing, Milkwashing und Klärung von Drinks durch Enzyme eintauchen» (Beitrag DbYnkdkjrNy, 29.07.2026). Das ist das, was sonst niemand in Hannover so vorführt.',
         komposition='Ein Paar: das Bild der Technik gross, Momo an der Bar daneben. Rechts die Zeile aus drei Wörtern und sein Satz. Welches Foto zu welcher Technik gehört, sagt Momo; bis dahin stehen die Bilder ohne Zuordnung.',
         moment='Ein Wort antippen, das Bild links tauscht an Ort und Stelle; nichts springt, die Fläche bleibt gleich gross.',
         baustein='neu: Zutatenzeile mit Bildtausch', quelle='neu',
         skizze='Drei Wörter in der Titelschrift, getrennt durch Schrägstriche wie auf Rudis Tellern. Das aktive Wort in Kerzenlicht-Orange, die anderen im Ton der Fläche. Unter dem Bild ein Band mit dem Namen der Technik.',
         bewegung='Paar steigt herauf und stösst an; Tippen tauscht das Bild; Wörter rollen zeilenweise.',
         unterschied='Kein Haus hatte ein Kapitel über eine Technik hinter der Bar. Die Überschrift ist eine Zeile aus Zutaten, keine Frage an den Gast, kein Zeichen-Titel-Untertitel.',
         bisher={'Salt & Silver': 'Karte als Erkunder: Drinks, Essen, Wein', 'Grand Beau-Rivage': 'Bar als Kachel im Kapitel «im Haus»', 'Taverne zum Schäfli': 'Bar und Humidor als Bildgruppe'}),

    dict(teil='gaenge', titel='AUBERGINE / KOKOS / LIMETTE / SESAM', flaeche='hell',
         satz='Rudis Kapitel. Erst der Pass mit den angerichteten Tellern über die ganze Breite, dann drei Paare aus Teller und Glas, je eines pro Gang, im Wechsel links und rechts.',
         bilder=['pass', 'kohl', 'spritz', 'zwiebel', 'highball', 'bete', 'milchglas'],
         stage=dict(h=74, el=[
             ('bild', 'pass', 0, 0, 100, 30, '50% 40%'),
             ('bild', 'kohl', 0, 33, 30, 40, '50% 50%'), ('bild', 'spritz', 30, 33, 18, 40, '50% 50%'),
             ('bild', 'zwiebel', 52, 33, 30, 40, '50% 50%'), ('bild', 'highball', 82, 33, 18, 40, '50% 50%'),
             ('band', 'Gang für Gang', 'ein Teller, ein Glas', 31, 24.5, 38)]),
         einfall='Rudi schreibt seine Teller in vier Wörtern (Beiträge DW4V45ujR0B, De1pn9ttMoX, DZIlJu-N0w4). Die Zeile der nächsten Ausgabe steht oben, gross; jedes Paar trägt darunter seine eigene, sobald Rudi das Menü schickt.',
         komposition='Ein Querformat vom Pass (36740), darunter Paare: Teller breit, Glas schmal, Wand an Wand. Drei Paare für drei Gänge, das zweite gespiegelt. Am Handy steht jedes Paar als eigenes Hochformat-Paar.',
         moment='Jedes Paar stösst an, wenn es den Rand berührt; die Vier-Wörter-Zeile darüber rollt aus dem Schlitz.',
         baustein='Das Paar', quelle='neu',
         skizze='Welche Teller zu welchem Menü gehören, ist nicht belegt; die Paare auf dem Board zeigen nur das Prinzip mit echten Bildern aus Rudis Ordner (4298 mit 4921, 5045 mit 4858, 4890 mit 4893).',
         bewegung='Anstossen je Paar; Zeile aus dem Schlitz.',
         unterschied='Die Gänge stehen als Paare, nicht als Stapel. Beim Zurbriggen Wellness landen die Gänge als Stapel untereinander; hier sitzt zu jedem Teller sein Glas Wand an Wand daneben.',
         bisher={'Zurbriggen Wellness': 'Gang für Gang als Stapel, der landet', 'Salt & Silver': 'Karte mit Gruppen zum Aufklappen', 'Taverne zum Schäfli': 'Karten-Erkunder mit Wahlschalter', 'Wirtschaft am Schlössli': 'Teller im Auftakt, Makro'}),

    dict(teil='tafel', titel='Vierzehn an einem Tisch.', flaeche='dunkel',
         satz='Vierzehn Plätze, vierzehn Bilder: zwei Reihen zu sieben Hochformaten Wand an Wand, dazwischen ein schmales Band wie die Tischplatte, mit Tag und Uhrzeit.',
         bilder=['t01', 't02', 't03', 't04', 't05', 't06', 't07', 't08', 't09', 't10', 't11', 't12', 't13', 't14'],
         stage=dict(h=52, el=[('tafel', ['t01', 't02', 't03', 't04', 't05', 't06', 't07'], ['t08', 't09', 't10', 't11', 't12', 't13', 't14'],
                               'Freitag 19 Uhr · Samstag 17 Uhr · 14 Plätze')]),
         einfall='«nur 14 Plätze pro Abend» (Beitrag DFqbLG2s_dc, 04.02.2025). Die Zahl der Bilder ist die Zahl der Stühle.',
         komposition='Oben sieben, unten sieben, wie die beiden Seiten einer langen Tafel. Das Band in der Mitte ist die Tischplatte. Alles Gäste-Bilder aus Rudis eigenem Ordner, keine Fotos von Gästen aus Instagram.',
         moment='Beide Reihen kommen als eine Fläche gemeinsam herauf, die 14 im Band zählt einmal hoch.',
         baustein='neu: Die Tafel', quelle='neu',
         skizze='Am Handy wird die Tafel ein Band zum Wischen, eine Reihe, das Band mit Tag und Uhrzeit bleibt stehen. Ob 14 noch stimmt: 2023 waren es 15, die Bar nennt für ihre Tafel bis 12 oder bis 14 (fakten.json › plaetze).',
         bewegung='Als Fläche gemeinsam, keine Staffel; Zahl zählt einmal.',
         unterschied='Die Anzahl der Bilder trägt eine Tatsache des Hauses. Bildwände anderer Häuser sind Mosaike ohne Ordnung; hier sitzen zwei Reihen gegenüber, wie am Tisch.',
         bisher={'Castell Son Claret': 'Bildwand mit Fächern, Mosaik dicht', 'Grand Beau-Rivage': 'Mosaik und Filmstreifen', 'Waldhotel Doldenhorn': 'Mosaik', 'Carlton-Europe': 'grosse Zahlen zählen hoch'}),

    dict(teil='plakate', titel='Jeder Abend hat sein Plakat.', flaeche='tapete',
         satz='Die Plakatwand: alle Plakate seit 2024 Wand an Wand geklebt, das neueste gross, darunter je ein Band in der Akzentfarbe dieses Abends mit dem Datum.',
         bilder=['p_mond', 'p_panther', 'p_kuerbis', 'p_garten', 'p_sessel', 'p_ski'],
         stage=dict(h=40, el=[
             ('bild', 'p_mond', 0, 0, 40, 40, '50% 50%'),
             ('bild', 'p_panther', 40, 0, 20, 20, '50% 50%'), ('bild', 'p_kuerbis', 60, 0, 20, 20, '50% 50%'), ('bild', 'p_garten', 80, 0, 20, 20, '50% 50%'),
             ('bild', 'p_sessel', 40, 20, 20, 20, '50% 50%'), ('bild', 'p_ski', 60, 20, 20, 20, '50% 50%'),
             ('text', 'September 2026 · ausgebucht', 82, 23, 16, 'mono'),
             ('text', 'März 2026 · November 2025 · Juni 2025 · Februar 2025 · November 2024', 82, 28.5, 16, 'klein')]),
         einfall='«Jedes Plakat seit 2023 folgt demselben System» (befund.md): Illustration oben, das Band mit der Wortmarke unten, eine Akzentfarbe je Abend. Im Profil sieht das aus wie eine Sammlung. Die Seite nimmt die Sammlung ernst.',
         komposition='Ein grosses Plakat, fünf kleine, ohne Lücke geklebt wie an einer Litfasssäule. Ein Plakat antippen: Datum, Menü und Drinks dieses Abends, soweit belegt.',
         moment='Die Wand kommt gemeinsam herauf, danach läuft einmal ein Glanzstreif über das Papier, Plakat für Plakat.',
         baustein='neu: Die Plakatwand', quelle='neu',
         skizze='Die Akzentfarbe der Seite folgt dem Plakat des nächsten Abends (Kundenprofil Blatt 5: Eisblau, Orange, Grasgrün, Nachtblau, Ochsenblut, Sepia). Rechte und Herkunft der Illustrationen sind offen; ohne Rudis Bestätigung kommt die Wand nicht online.',
         bewegung='Als Fläche gemeinsam; Glanzstreif einmal je Plakat.',
         unterschied='Kein Haus hatte ein Archiv seiner eigenen Ankündigungen. Es sind keine losen Abzüge auf Tapete, sondern geklebte Plakate ohne Lücke, keines gekippt.',
         bisher={'Carlton-Europe': 'Abzüge als Stapel', 'Landgasthof Ruedihus': 'Abzüge landen, Chronik', 'Hotel Seiler au Lac': 'Abzüge', 'Berghotel Gasterntal': 'Abzüge landen'}),

    dict(teil='familie', titel='Wenn aus Freunden und Kollegen Familie wird.', flaeche='hell',
         satz='Der Film mit der ganzen Mannschaft an der Theke steht in der Mitte, quadratisch und gross; daneben das Bild der drei vor dem Negroni-Schriftzug und die Namen mit ihren Aufgaben im Band.',
         bilder=['trio'],
         filme=['familie'],
         stage=dict(h=44, el=[
             ('film', 'familie', 4, 0, 44, 44),
             ('bild', 'trio', 52, 0, 44, 33, '50% 40%'),
             ('band', 'Rudi · Momo · Derya', 'Aufgaben aus dem Gespräch', 52, 35, 44)]),
         einfall='«Wenn aus Freunden und Kollegen Familie wird. Dann haste allet richtig jemacht!» (Rudi mit Dirty Chicken, Beitrag DZIjZWNCGZT, 03.06.2026). Der Satz ist die Überschrift, der Film ist das Gruppenbild.',
         komposition='Ein bewegtes Gruppenbild statt drei Porträts nebeneinander. Der Film läuft einmal, wenn er ganz zu sehen ist, und bleibt auf dem letzten Bild stehen; antippen spielt ihn noch einmal. Ton aus.',
         moment='Film und Foto stossen aneinander an; das Band mit den Namen rollt.',
         baustein='Das Paar, mit Film', quelle='neu',
         skizze='Der Film ist von Dirty Chicken, die Leute sind dieselben. Wer auf dem Foto 63873 wer ist, ist nicht belegt; Derya als «Gastgeberin» steht so in fakten.json für 2024, ihre heutige Rolle ist offen.',
         bewegung='Anstossen; Film spielt einmal beim Sichtbarwerden, steht dann.',
         unterschied='Die Menschen kommen als Film, nicht als Porträt-Trio. Beim Schäfli steht die Familie als Bildgruppe mit drei Porträts.',
         bisher={'Taverne zum Schäfli': 'Familie: drei Porträts, verschränkt', 'Salt & Silver': 'Gründer im Willkommen', 'Grand Beau-Rivage': 'Gastgeber im Willkommen'}),

    dict(teil='dirtychicken', titel='Dit is wahre Liebe.', flaeche='dc',
         satz='Rudis zweite Küche als eingelegtes Blatt in eigener Farbe: der Eröffnungsfilm hochkant wie ein Handy in der Mitte, links und rechts je ein Bild aus dem Profil, darunter ein Knopf zu Dirty Chicken.',
         bilder=['dc_burger', 'dc_liebe', 'dc_tisch'],
         filme=['opening'],
         stage=dict(h=47, el=[
             ('bild', 'dc_burger', 2, 6, 32, 32, '50% 50%'),
             ('film', 'opening', 38, 0, 24, 42.7),
             ('bild', 'dc_liebe', 66, 6, 32, 32, '50% 50%'),
             ('text', 'Dirty Chicken · Sandwiches & More', 2, 42.5, 40, 'mono'),
             ('knopf', 'Zu Dirty Chicken', 76, 42)]),
         einfall='«Dit is wahre Liebe!» und «Dirty Food & Dirty Drinks. Jenau meen Ding wa» (Beiträge DZiug6EoMRr, DZIo4FHIqRR). Dirty Chicken spricht anders als Culinarium; das Kapitel darf das auch.',
         komposition='Ein Blatt in der Farbe von Dirty Chicken mitten in der Culinarium-Seite, wie eine Beilage in einem Heft. Der Film ist das Herz, die Bilder rahmen ihn.',
         moment='Der Film steigt herauf und startet, die beiden Bilder stossen links und rechts an ihn an.',
         baustein='neu: Die Beilage', quelle='neu',
         skizze='Der Film trägt das Logo von Dirty Chicken am Anfang und am Ende eingebrannt; das passt hier, weil das Kapitel Dirty Chicken heisst. Ob es dazu eine eigene Seite oder eine eigene Adresse gibt, ist offen (Robert bot im Juli beides an). Farben und Logo als Vektor: offen.',
         bewegung='Hochschweben, Film spielt beim Sichtbarwerden; Anstossen der Bilder an den Film.',
         unterschied='Zum ersten Mal ein zweites Konzept mit eigener Farbe mitten auf der Seite, nicht als Schwesterhaus im Fuss.',
         bisher={'Taverne zum Schäfli': 'Schwesterhaus als Kapitel und im Fuss', 'Salt & Silver': 'Bühne der Häuser, je Haus andere Anordnung', 'Wirtschaft am Schlössli': 'Familie im Fuss'}),

    dict(teil='betriebe', titel='Für Betriebe.', flaeche='matt',
         satz='Platz gehalten für «Schulungen, Events, Consulting», die heute nur im Namen des Instagram-Profils stehen. Kommt erst auf die Seite, wenn Rudi sagt, was dahinter steht.',
         bilder=['kueche'],
         filme=['teilen'],
         stage=dict(h=30, el=[
             ('bild', 'kueche', 0, 0, 17, 30, '50% 40%'),
             ('film', 'teilen', 17, 0, 53.3, 30),
             ('text', 'Schulungen · Events · Consulting', 73, 4, 26, 'ort'),
             ('text', 'Nur mit Inhalt von Rudi. Bis dahin bleibt der Platz leer.', 73, 16, 24, 'lauf')]),
         einfall='Name des Profils: «Food Pairing | Schulungen | Events | Consulting» (_qa/spaeher/ig-profil-rechner.txt). Belegt ist davon nur die Schulung als Teil des Abends.',
         komposition='Nur als Platzhalter auf dem Board. Rudis Film 52799 (Tageslicht, Teller zum Teilen mit Auster und Ente) und das Küchenbild 36829 könnten hierher gehören; zu welchem Konzept sie gehören, ist offen.',
         moment='keiner, solange kein Inhalt da ist',
         baustein='offen', quelle='neu',
         bewegung='offen',
         unterschied='Hier steht noch nichts; es wird nichts dazuerfunden.',
         bisher={'Taverne zum Schäfli': 'Feiern als Rechner', 'Wirtschaft am Schlössli': 'Feiern als Rechner nach Anlass'}),

    dict(teil='naechster', titel='Der nächste Abend.', flaeche='dunkel',
         satz='Zum Schluss wieder ein Paar: zwei Gläser, die sich berühren, und das Licht der Bar von draussen. Dazwischen das Band mit dem nächsten Datum, dem Preis und dem Knopf.',
         bilder=['anstossen', 'licht'],
         stage=dict(h=44, el=[
             ('bild', 'anstossen', 0, 0, 34, 44, '50% 50%'), ('bild', 'licht', 66, 0, 34, 44, '50% 50%'),
             ('text', 'Freitag 19 Uhr · Samstag 17 Uhr', 37, 6, 26, 'mono'),
             ('band', 'Nächster Abend', 'Datum folgt', 35.5, 13, 29),
             ('text', 'Drei Gänge, fünf Drinks, Momo erklärt jeden selbst.', 37, 25, 26, 'lauf'),
             ('knopf', 'Platz sichern', 43, 35)]),
         einfall='Heute: «Tickets ausschließlich per Vorverkauf über PayPal. Schreibt uns hierzu gerne eine Nachricht» (DbYnkdkjrNy). Die Seite macht daraus einen Knopf; ausgebucht führt er auf die Warteliste.',
         komposition='Paar aus Anstossen (4026) und Fenster der Bar bei Nacht (3998), in der Mitte das Band. Preis nur zusammen mit dem Datum, aus einer Quelle für Seite und Ticket; zuletzt 89,00 EUR (März und September 2026).',
         moment='Die Gläser links stossen an das Fenster rechts an; das Band rollt, der Knopf ist sofort da.',
         baustein='Das Paar mit Band', quelle='neu',
         skizze='Welches Ticketsystem kommt, entscheidet Robert mit Rudi (Vergleich in Kundenprofil Blatt 9). Stornoregel im Wortlaut aus den Beiträgen, rechtlich erst mit AGB.',
         bewegung='Anstossen; Band aus dem Schlitz; Knopf ohne Verzögerung.',
         unterschied='Der Schluss ist ein Termin, kein Abschied und keine zweite Buchungsleiste eines Hotels.',
         bisher={'Grand Beau-Rivage': 'Einladung mit zweiter Buchungsleiste, Bewertungen', 'Carlton-Europe': 'Einladung, Ticket', 'Taverne zum Schäfli': '«Wir fahren Sie wieder zurück.»'}),
]

# Was zwischen den Szenen steht, damit es eine Geschichte bleibt (teil → Satz)
UEBERLEITUNG = {
    'auftakt': 'Die beiden laden ein, also geht es zuerst dorthin, wo sie kochen und mixen.',
    'strasse': 'Wer drin ist, sieht den Tisch zuerst durch die Wand.',
    'fenster': 'Bevor gegessen wird, kommt das erste Glas.',
    'aperitif': 'Nach dem Glas der Teller, in Rudis Schreibweise.',
    'gaenge': 'Aus drei Gängen wird ein Abend, wenn vierzehn Leute daran sitzen.',
    'tafel': 'Jeder dieser Abende hatte sein eigenes Plakat.',
    'plakate': 'Hinter den Plakaten stehen dieselben Leute, Abend für Abend.',
    'familie': 'Und dieselben Leute haben noch eine zweite Küche.',
    'dirtychicken': 'Was sie sonst noch machen, steht hier, sobald sie es erzählen.',
    'betriebe': 'Zum Schluss das Wichtigste: der nächste Abend.',
}

# Unterseiten: Seite, Titel, Szenen (Teil, Satz, Bilder)
SEITEN = [
    dict(seite='abend.html', titel='Der Abend', szenen=[
        ('Kopf', 'Ein Paar im Kopf wie auf der Startseite, andere Bilder: Teller und Glas des nächsten Menüs.', ['zwiebel', 'highball']),
        ('Ablauf', 'Was an so einem Abend passiert, in der Reihenfolge, wie Culinarium es schreibt: drei Gänge, fünf Drinks, Tasting und Schulung. Nur Belegtes.', []),
        ('Menü', 'Rudis Zeilen in vier Wörtern, je Gang mit dem Drink daneben; eine Quelle für Seite, PDF und Plakat.', []),
        ('Buchen', 'Datum, Plätze, Preis, Platz sichern oder Warteliste, Stornoregel im Wortlaut.', []),
    ]),
    dict(seite='plakate.html', titel='Alle Abende', szenen=[
        ('Kopf', 'Die Plakatwand gross, alle Plakate seit 2023, auch die Pop-ups «BY MOMO X CHRISTOPH».', ['p_mond']),
        ('Je Abend', 'Datum, Plakat, Menü und Drinks, soweit belegt; Preise nur mit Datum.', ['p_panther', 'p_kuerbis']),
    ]),
    dict(seite='leute.html', titel='Momo x Rudi', szenen=[
        ('Kopf', 'Das Paar Bar | Küche wie im Auftakt, in anderen Bildern.', ['bar', 'pass']),
        ('Wer was macht', 'Texte erst aus dem Gespräch mit Rudi; keine Zeile aus Instagram-Bios übernehmen.', ['trio']),
    ]),
    dict(seite='dirty-chicken.html', titel='Dirty Chicken', szenen=[
        ('Kopf', 'In der Farbe von Dirty Chicken; Opening-Film, Bilder aus dem Profil.', ['dc_tisch']),
        ('Offen', 'Kapitel, eigene Unterseite oder eigene Adresse: entscheidet Robert mit Rudi.', []),
    ]),
    dict(seite='anfahrt.html', titel='Haasemannstraße 13', szenen=[
        ('Kopf', 'Das Schild der Bar bei Nacht, Adresse gross.', ['schild']),
        ('Weg', 'Adresse und Plus Code; Anreise-Angaben gibt es heute keine, also nur, was Rudi liefert.', []),
    ]),
    dict(seite='impressum.html · datenschutz.html · agb.html', titel='Rechtstexte', szenen=[
        ('Inhalt', 'Erst mit Vertragspartner, Anschrift und Stornoregel; heute gibt es keine Rechtstexte.', []),
    ]),
]

GESTRICHEN = [
    ('Die Seite als Zeitschrift mit Ausgaben', 'Plakate nur in Instagram-Grösse, Rechte an den Illustrationen offen, Grafik statt Foto im Auftakt. Bleibt als Kapitel «Plakatwand».'),
    ('Jeder Mensch ein eigenes Kapitel', 'Keine Texte über die drei, wer auf welchem Foto ist, ist nicht belegt. Die Menschen tragen die Gänge, das Familien-Video ist ihr Kapitel.'),
    ('Ein Plakat als Auftakt', 'Zu klein für die volle Breite, Rechte offen, und Robert will im Auftakt echte Fotos.'),
    ('Plakate als Fächer, leicht gekippt', 'Kacheln und Bilder werden nie gekippt (Website-Bau Kern, Abschnitt 4).'),
    ('Mehr als ein Fenster', 'Fenster als Übergang steht bei sieben Häusern; hier reicht das eine Loch in der Wand, die übrigen Übergänge macht das Paar.'),
    ('Preis im Auftakt', 'Kein Preis im Auftakt (Website-Bau Kern, Abschnitt 4). Der Preis steht nur beim nächsten Abend, mit Datum.'),
    ('Falstaff-Punkte als Siegel oder Laufband', 'Die 91 Punkte gehören der Bar, nicht Culinarium; nur mit Freigabe der Bar und dann als Satz, nie als Siegel.'),
    ('Kerzen, die flackern', 'Erfundener Effekt; die Kerzen leuchten auf den Fotos schon.'),
    ('Filme als Hintergrund einer Fläche', 'Regel 55: Filme stehen als Bild, spielen einmal, nie in Dauerschleife hinter Text.'),
    ('Bilder von Gästen aus Instagram', 'Luisa Verfürth, Hannover Eats und Gäste nie auf der Seite; die Tafel nimmt nur Bilder aus Rudis Ordner.'),
    ('Das Private Dining der Bar', 'Fremdes Angebot am selben Tisch; gehört nicht auf die Seite von Culinarium.'),
]

OFFEN = [
    ('Leitbild-Paar für den Auftakt', 'Robert wählt: A Momo | Rudi (4568 | 5301), B Glas | Teller (5369 | 5379), C Tafel allein (4972).'),
    ('Wer ist wer auf den Fotos', 'Rudi, Momo, Derya sind auf vielen Bildern, aber nirgends benannt; Zuordnung vor jeder Bildzeile mit Rudi klären.'),
    ('Rechte an Rudis Bildern', 'Fotograf je Datei unbekannt (focusonbiz_hannover, Irina Voronov oder andere); _quelle/vom-kunden/drive/herkunft.json.'),
    ('Rechte und Herkunft der Plakat-Illustrationen', 'Kundenprofil Blatt 5; ohne Bestätigung keine Plakatwand online.'),
    ('Nächster Termin und Ticketsystem', 'Profil 25.10.2026 ohne Ankündigung; Vergleich in Kundenprofil Blatt 9.'),
    ('Dirty Chicken: Kapitel, Unterseite oder eigene Adresse', 'Beide Filme sind von @dirtychicken.hannover, Logo im Opening-Film eingebrannt; Logo als Vektor und Farben fehlen.'),
    ('Film 52799.mp4', 'Tageslicht, Teller zum Teilen mit Auster und Ente am Fenster: zu welchem Konzept er gehört, ist nicht belegt.'),
    ('Schulungen, Events, Consulting', 'Nur der Profilname; Inhalte von Rudi.'),
    ('Vegetarisch als fester Standard', 'Dezember 2025 Ente, «auch in Veggie möglich» (DSnlBLECGyD).'),
    ('Freigabe der Bar', 'Bilder mit dem Schild WILD SIDE, Falstaff, Nennung als Gastgeber.'),
    ('Vertragspartner und Impressum', 'fakten.json › rechtstraeger.'),
    ('Fünf Dateien fehlen', '115351, 115389, 115442, 115445, 36541 (.jpg): nicht freigegeben, nicht im Ordner «Robert tasty».'),
    ('4128.jpg ist ein HEIC-Bild', 'Aus Mail 1a16c05a4695979d, Endung .jpg, Inhalt HEIC; öffnet mit sips, nicht mit jedem Werkzeug.'),
    ('Markenbuch fehlt', 'Stationen 04 und 05 liegen nicht vor; Farben vorläufig aus den Plakaten (#FAF4F4, #3A3845), Akzent aus den Fotos gemessen, Titelschrift Fraunces wie beim Späher.'),
]
