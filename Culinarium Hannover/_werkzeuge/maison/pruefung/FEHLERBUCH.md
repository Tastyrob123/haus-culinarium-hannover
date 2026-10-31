---
tags: [projekt, website]
status: aktiv
---

# La Maison · Culinarium Hannover · Fehlerbuch 10a Zeile für Zeile (28.10.2026)

Quelle: Master Werkzeug-Bau, Abschnitt 10a (Stand 28.10.2026). Jede Zeile, die die Zentrale oder das gemeinsame Kleid (`_werkzeuge/oberflaeche/`) betrifft, am neuen Stand nachgesehen. Zeilen nur zu anderen Werkzeugen (Karten-PDF, Feed, Gutschein, Imprimerie-Editor …) stehen unten gesammelt als «betrifft nicht».

| Zeile 10a | Regel (kurz) | Stand hier |
|---|---|---|
| Hafenbüro Empfang (19.10.) | erstes Bild: Kopf, Bühne, alle sechs ganz, echte Fotos, unten bündig | erfüllt: pruefe «Erstes Bild …» und «Bühne und Plakatwand beginnen und enden auf einer Linie» (beide Kerne) |
| Hafenbüro Leiste (19.10.) | Namen nur, wenn sie ganz zwischen die Eck-Knöpfe passen | erfüllt: `passt()` nach `document.fonts.ready`; pruefe «Leiste: Namen nie unter einem Knopf» |
| Hafenbüro Bewegung (19.10.) | Takt der abgenommenen Häuser | erfüllt (Block «Bewegung …» in `quelle/maison.css` übernommen) |
| Werkzeug-Übersicht mit Bild (Schlössli 19.10.) | je Werkzeug ein Bild | erfüllt: sechs Plakate mit Fotos aus dem Bildregister `BILD` |
| Kacheln bündig (20.10.) | nebeneinander unten bündig | erfüllt (ein Raster, gleiche Zeilenhöhe) |
| Kacheln gleichmässig verteilt (20.10.) | höchstens vier je Reihe, keine allein | erfüllt: 3 + 3, Handy 2 + 2 + 2 |
| Roher Code (19.10.) | nie `{`, `undefined`, `NaN`, `None` | erfüllt: pruefe «kein roher Code im Text» |
| Fakten nur aus dem Haus (19.10.) | keine Werte eines anderen Hauses | erfüllt: Adresse aus `_kette/03-sammler/fakten.json`, Fotos/Alt aus `website/bau.py BILD`, Abendfarben aus `marke.json`; `ohne_fremde()` bricht den Bau ab; Hausnamen-Suche im Revier: nur Herkunfts-Kommentare in `bau.py` und `oberflaeche/UMSTELLUNG.md` (gewollt), ausgelieferte Dateien frei |
| Titel auf Dunkel weiss (20.10.) | Betonung über Stärke, nie dunkle Farbe | erfüllt: `kleid/culinarium.css` (`.wo-sb__h em` weiss 300), Säle `.dunkel` hell |
| Dunkle Flächen nur in Tönen des Kleids (20.10.) | `--wo-nacht/-nacht2/-tief` | erfüllt; Werte aus der gebauten Website |
| Luft unter der Bühne (20.10.) | ≥ 30 px | erfüllt im Kleid (`.wo-sb{margin-bottom:34px}`, Handy 24) |
| Kopf bei wenig Breite (20.10.) | Titel nimmt nur freien Platz, kürzt mit «…» | erfüllt im Kleid (901–1240 px Regel aus der Vorlage) |
| Zierzeile (Demo-Check 21.10.) | bricht um statt zu kürzen | erfüllt im Kleid |
| Dunkle Taste mit dunkler Schrift (21.10.) | Schrift auf dunkler Fläche immer hell | erfüllt im Kleid (`.wo-re.wo-an *` hell) |
| Schild Rundgang wandert (20.10.) | steht fest | erfüllt: `rundgang.js` aus der berichtigten Vorlage |
| Zwischenbreiten (21.10.) | 920/1000/1024/1100/1240 messen | erfüllt: `pruefung/breiten-webkit.txt` (320–1600, `scrollWidth` = Breite); Bilder vor ihrem Auftritt (Skalierung 1,04) ragen kurz hinaus, nach dem Auftritt nichts (geprüft mit Durchscrollen) |
| Zurück zur Zentrale aus allen Werkzeugen (21.10., **wieder** Schäfli) | Zentrale auf eigenem Server, 127.0.0.1 | erfüllt: `ZUR_STUBE` auf 127.0.0.1:9081 im Bau; dazu neu im Kleid: lokal zeigen die Wege der anderen Werkzeuge auf deren Port (Fund culinarium-reception, neue Zeile 10a 28.10.); democheck Teil F aus allen sechs |
| Weg zum Tisch, dieselben Stufen wie das Besucherbuch (21.10.) | kein Anteil über 100 % | erfüllt: Stufen und Rechnung von culinarium-registre übernommen («Der Abend» geöffnet → Platz gebucht oder auf der Warteliste), democheck «Weg zum Tisch … kein Anteil über 100 %» |
| Werkbank-Herkunft `wb/wy/wbo` (21.10.) | ein Format, `zur-werkbank.js` | erfüllt: über den echten Weg aus der Werkbank geprüft (democheck Teil E grün) |
| Bilder in `url(...)` prüfen (21.10.) | jede Netzantwort ≥ 400 zählen | erfüllt: bild.js/pruefe zählen jede Netzantwort; 0 Fehler |
| Datum auf Bildern (21.10.) | Aufnahmen ohne feste Zone | erfüllt: `schirme.js` und Bildaufnahmen ohne `timezoneId`; nur Prüfläufe mit Europe/Berlin |
| Konsole leer (neu 28.10.) | nicht laufendes Werkzeug ohne roten Netzfehler | erfüllt: Weiterleiter 204 statt 502 (neue Zeile 10a 28.10.) |
| Texte: Wertigkeit, nie Masse (CLAUDE.md) | keine Stückzahlen als Pointe | erfüllt: Säle sprechen von «jedem Gang mit seinem Drink», «für jeden Abend sein eigenes Plakat»; «vierzehn» kommt nicht vor |
| Nie fett, nie kursiv (CHARAKTER 4) | | erfüllt: kursive Stamm-Stellen (Brief, Blatt, Lupe) im Kleid aufrecht; Titel Fraunces 300–360 |

**Betrifft nicht** (andere Werkzeuge oder Website): Registre-Ranglisten, Livre-Probe/Markenbuch-PDF, Bureau-Vorschau/Prüfseite/Listen, Imprimerie (Vorlagen, Gutschein, Filme, Fotoauswahl, Editor), Réception (Chat-Spalte, Probe-Antwort, Kontakt), Karten-PDF, Feed, Website-Seiten des Schlössli/Schäfli.
