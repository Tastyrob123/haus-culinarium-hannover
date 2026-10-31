---
tags: [projekt, feed]
status: aktiv
---

# Feed-Bestand und Gegenprobe · Culinarium (Werkbank-Chat, 28.10.2026)

Rolle: `~/Desktop/Website-Projekte/_Kette/rollen/feed-planer.md` · Master Website-Bau 5a Regel 10 und 10a. Bestand der früheren Feeds: `Taverne zum Schäfli Wigoltingen/website/_werkbank/feed-bestand.md` (Gegenprobe Stand 21.10.2026, dort mit Schlössli, Maeder-Häusern, Rivage, Carlton).

## Dieses Haus: Culinarium · «Fortsetzung», die nächsten 60 Beiträge (Fassung 3, 29.10.2026)

Robert: «die werden jetzt nicht ihren gesamten Feed löschen … man muss gucken, was sie an Bildern benutzt haben, damit wir jetzt diese 60 Beiträge darauf aufbauen können … bei den Plakaten … eine Ausnahme». Der Feed setzt @culinarium_hannover fort.
- **Bestandsabgleich:** Kit-Schritt `_Werkbank-Kit/feed_bestand.py` (pHash und Ausschnitt-Vergleich mit Inhaltsprobe) gegen alle 56 Bilder der 20 Beiträge in `_quelle/extern/ig/` und Rudis Beitrag mit Culinarium als Mitautor (DLSA60BMwiG). 50 Fotos der Website sind schon gepostet und gesperrt (u. a. alle `ab_…`, lauch, g3, m8, ws03, ws28); Plakate sind Ausnahme (`BESTAND_AUSNAHMEN`). Bericht `feed/bestand.json`.
- **Die nächsten 60 in Reihenfolge des Postens** (`JAHR` in `_werkbank/feed_daten.py`, im Raster umgekehrt): Abend 27./28.11. (Ankündigung, «Noch eine Woche.», «Noch drei Plätze.», Abend, «Danke für zwei Abende.»), 18./19.12. («Samstag ausgebucht.», «Danke für 2026.»), Dirty Chicken [Datum], Abend im Frühjahr [Datum] mit Countdown, Abend im Sommer [Datum] mit «Ausgebucht.», Dirty Chicken, nächster Abend [Datum]. 7 Plakate «Aus dem Archiv». Keine gleiche Art neben- oder untereinander (`nachbarn()`).
- **Profil:** oben die 60 neuen (nummeriert in Reihenfolge des Postens, Nummern abschaltbar), ein Band «Die nächsten 60 · Euer Feed heute», darunter die 21 echten bisherigen Beiträge (leicht zurückgenommen); Schalter «Heute» / «Mit den nächsten 60» mit wachsendem Feed; Kopf 88 bzw. 28. Bausteine: `feed/uebergang.css`, `feed/uebergang.js`, eingebaut von `_werkbank/feed_leicht.py`.
- Sicherungen: `*.vor-fortsetzung-2026-10-29`, `*.vor-uebergang-2026-10-29`.

## Frühere Fassung: Culinarium · «Ein Abend in Folgen», 60 Beiträge (Fassung 2b, 29.10.2026, ersetzt)

Robert zur Fassung 2: «das gefällt mir sehr gut … aus 36 Beiträgen … so 60 machen». Die 36 oben bleiben unverändert; darunter acht Reihen (37–60) als dritte Folge: Karussell «Fünf Drinks, ein Abend», Blick durch die Tür, Zeile «ROTE BEETE / ZWIEBEL / PARMESAN», Blumenkohl mit Kürbis, Plakat November 2025, Momo, Momos Drink «Black Pearl» als Schrift, Pass, Longdrink, Service, Reel «Geklärt, Glas für Glas», Dirty Chicken in Violett («Dit ist wahre Liebe!»), Knödel, «Danke für gestern.», Plakat November 2024, Tafel, Dessert mit Drink, Dirty Chicken von oben, Zeile «BLUMENKOHL / ROQUEFORT / KAPERN / QUINOA», das Team, Coupe, Plakat April 2024, Fenster der Bar, Karussell «Wie es kam». Neun Plakate von 60, nie neben- oder untereinander; jedes Foto einmal. Im Kopf 60 Beiträge (aus len(P) und feed.json); die ersten zwölf Kacheln laden sofort, alle mit Motivfarbe (`_werkbank/feed_leicht.py`). Sicherung der 36er-Fassung: `*.vor-feed60-2026-10-29`.

## Dieses Haus: Culinarium · «Ein Abend in Folgen» (Fassung 2, 29.10.2026, oberste 36 der Fassung 2b)

Ersetzt Fassung 1 «Momo x Rudi» (Plakat-Säule in der Mitte; Robert 29.10.2026: «diese gerade Reihe in der Mitte … mit den Plakaten … total monoton und billig»). Sicherung: `feed.vor-feed-2026-10-29/`, `_werkbank/feed_daten.py.vor-feed-2026-10-29`.

- **Idee:** Der Feed erzählt den Abend in Folgen, von oben nach unten: Ankündigung, Tafel bei Kerzenlicht, Teller, Drink, Hände am Pass, die Leute, Rückblick, dann die nächste Folge. Keine feste Spalte; jede Reihe anders gemischt.
- **36 Beiträge, 12 Reihen:** 19 Fotos, 6 Plakate, 3 Zeilen von Rudi als reine Schrift (Fraunces 360, Schrägstriche in Kerze, auf Nacht oder Warmweiss), 2 Stimmen (Momo, Rudi), 2 Text-Beiträge (Ankündigung 27./28.11., «Ausgebucht.» September), 2 Karussell-Deckblätter («Was im Glas passiert», «Ein Abend an der langen Tafel»), 2 Reel-Titel («Jeder Teller von Hand angerichtet», «Durchs Sieb, ins Glas»).
- **Plakate:** September 2026, März 2026, Juni 2025, Februar 2025, Juli 2024, November 2023; ganz, nie beschnitten, auf Nacht oder Warmweiss; nie zwei neben- oder untereinander.
- **Raster:** hell und dunkel, warm und kühl, nah und weit wechseln; keine zwei Schrift-Beiträge untereinander; das «C» aus Rudis Wortmarke ist das einzige Zeichen.
- **Bilder:** nur Fotos des Hauses aus dem Bildregister der Website und Rudis Plakate, jedes einmal. Echte Gästestimmen mit Wortlaut gibt es in den Quellen nicht; die Zitate sind Momo und Rudi.
- **Bau:** `_werkbank/feed_daten.py` (REGEL «bogen», Liste FEED Reihe für Reihe), `python3 _Werkbank-Kit/feed.py "<…>/website/_werkbank"`, `node feed_druck.js …`, noch einmal feed.py, `node feed_druck.js … --handy`, `node _werkbank/geraete/schirme.js feed`.
- **Tafel:** http://localhost:8978/haus/_Oberchef/zeigen/culinarium/feed-2910/index.html

## Frühere Fassung: Culinarium · «Momo x Rudi» (erste Fassung, 28.10.2026, ersetzt)

- **Idee:** Auf den Plakaten steht «BY MOMO X RUDI». Das Raster ebenso: in jeder Reihe links ein Teller aus Rudis Küche, rechts ein Glas von Momo, und in der Mitte, wo das «x» steht, das Plakat eines Abends. Die Mittelspalte läuft vom neuesten Plakat (September 2026) oben bis April 2024 unten: das Profil bleibt eine Sammlung der Plakate, wie heute, und zeigt dazu, was an der Tafel passiert.
- **Plakate:** ganz, nicht beschnitten, auf der Nacht der Bar mit dem Raster der Website (als Tafel gesetzt, `BOGEN_CSS`), damit Wortmarke und Zeile des Plakats lesbar bleiben.
- **Menschen:** keine. Teller und Gläser tragen das Raster; Gesichter stehen auf der Website und im Brief.
- **Raster:** 24 Beiträge, 8 Reihen, jede Reihe Teller · Plakat · Glas. Keine Schrift außer der auf den Plakaten.
- **Erste neun:** Lauch/Blumenkohl/Chipotle · Plakat September 2026 · Drink mit Schaum · Blumenkohl/Roquefort · Plakat März 2026 · Schaum bei Kerzenlicht · Hokkaido · Plakat November 2025 · Glas mit Feige.
- **Farbbett:** helle Teller nie übereinander (Spaghetti-Eis in Reihe 5 zwischen Rote Bete und Knödeln), die Gläser rechts im Wechsel hell und dunkel.
- **Bilder:** 16 Fotos und 8 Plakate, alle aus dem Bildregister der Website (`website/assets/bild`, geschärfte Fassungen kommen von selbst nach). Jedes einmal. Rudis Dateien und eigene Plakate; keine Gästefotos, keine Fotos Dritter, keine erzeugten Bilder.
- **Profil:** 28 Beiträge, 1.079 Follower, 305 gefolgt (abgelesen ohne Anmeldung, `_qa/spaeher/ig-profil-handy.txt`, 25.10.2026).
- **Bau:** `website/_werkbank/_werkbank/feed_daten.py` (REGEL «bogen»), `python3 _Werkbank-Kit/feed.py "<…>/website/_werkbank"`.

## Gegenprobe

| Feed | Leitform | Schrift | Erste Reihe | Unterschied zu Culinarium |
|---|---|---|---|---|
| Carlton-Europe | Paar 1 + 2, Hochkant 1 × 2 | Sätze auf Fotos | Abzug + Häuser heute | keine Paare über zwei Felder, kein Hochkant, keine Sätze |
| Waldhotel Doldenhorn | Titelseite 2 × 2 oben, Zahl darunter | Titel und Zahlen | Titelseite «Das Haus» | keine Blöcke, keine Zahlen |
| Landgasthof Ruedihus | Bild über sechs 3 × 2 oben, Raumnamen | Namen auf Fotos | Haus im Grünen | nie über mehrere Felder, keine Namen |
| Berghotel Gasterntal | drei Wortplakate 3 × 1 | Satz groß im Plakat | Plakat Fest | keine Wortplakate; die Plakate sind die echten des Hauses, je ein Feld |
| Grand Beau-Rivage | Plakat jede vierte Reihe | Tafeln | Plakat Haus | Plakate verteilt, nie in einem festen Takt |
| Wirtschaft am Schlössli | ein Breitbild 3 × 1 in der Mitte | keine | Dessert, Abend, Glas | kein Breitbild |
| Taverne zum Schäfli | drei Blöcke 2 × 2 links/rechts | keine | Stube (vier Felder) | keine Blöcke, alles Einzelfelder |
| Tasty Hub | Banner oben | – | Banner | kein Banner |

Ergebnis (Fassung 2): Kein bisheriger Feed erzählt einen Abend in Folgen mit reinen Schrift-Beiträgen (Rudis Zeilen), Karussell- und Reel-Titeln; alle Stücke sind Einzelfelder, ohne festes Muster.
