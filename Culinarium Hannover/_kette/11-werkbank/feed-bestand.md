---
tags: [projekt, feed]
status: aktiv
---

# Feed-Bestand und Gegenprobe · Culinarium (Werkbank-Chat, 28.10.2026)

Rolle: `~/Desktop/Website-Projekte/_Kette/rollen/feed-planer.md` · Master Website-Bau 5a Regel 10 und 10a. Bestand der früheren Feeds: `Taverne zum Schäfli Wigoltingen/website/_werkbank/feed-bestand.md` (Gegenprobe Stand 21.10.2026, dort mit Schlössli, Maeder-Häusern, Rivage, Carlton).

## Dieses Haus: Culinarium · «Momo x Rudi» (erste Fassung, 28.10.2026)

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
| Grand Beau-Rivage | Plakat jede vierte Reihe | Tafeln | Plakat Haus | Plakat in jeder Reihe, immer in derselben Spalte |
| Wirtschaft am Schlössli | ein Breitbild 3 × 1 in der Mitte | keine | Dessert, Abend, Glas | kein Breitbild |
| Taverne zum Schäfli | drei Blöcke 2 × 2 links/rechts | keine | Stube (vier Felder) | keine Blöcke, alles Einzelfelder |
| Tasty Hub | Banner oben | – | Banner | kein Banner |

Ergebnis: Kein bisheriger Feed hat eine feste Mittelspalte, die durch alle Reihen läuft. Die Form kommt aus dem «x» von «Momo x Rudi».
