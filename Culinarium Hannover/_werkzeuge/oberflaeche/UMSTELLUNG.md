---
tags: [projekt, website]
status: aktiv
---

# Werkzeug-Oberfläche · Culinarium Hannover

Angelegt am 28.10.2026 vom Chat `culinarium-maison` (Zentrale), dem **einzigen Schreiber dieses Ordners**. Paket = Stamm der Häuser (`grund.css`, `rahmen-buehne.css`, `rahmen-inseln.css`, `oberflaeche.js`, `muster.html`, Klon aus dem Schäfli, unverändert), Kleid eigen: `kleid/culinarium.js` + `kleid/culinarium.css` + `kleid/culinarium-zeichen.svg` (das «C» der Wortmarke, unverändert aus `website/assets/zeichen/marke.svg #wm`, die die Website aus Rudis Original `_quelle/logo/original/culinarium-logo-original.svg` baut). Rahmen «Die Bühne»: Kopf dunkel, Raum hell (Werkzeuge hell).

## Einbinden (jedes Werkzeug gleich)

Der Server des Werkzeugs liefert `/assets/oberflaeche/…` aus **diesem Ordner** und `/assets/…` sonst aus `website/assets/` (Fotos `/assets/bild/<schlüssel>-<breite>.webp`, Schriften `/assets/schrift/`, Wortmarke und Tapeten `/assets/zeichen/`). Muster: `_werkzeuge/maison/server.py` (`translate_path`, Port 9081).

```html
<script src="/assets/oberflaeche/kleid/culinarium.js?v=1"></script>          <!-- vor allem anderen, ohne defer -->
<link rel="preload" href="/assets/schrift/fraunces-soft.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v=1">
<link rel="stylesheet" href="/assets/oberflaeche/rahmen-buehne.css?v=1">
<link rel="stylesheet" href="/assets/oberflaeche/kleid/culinarium.css?v=1">
<!-- eigenes CSS des Werkzeugs danach -->
<script src="/assets/oberflaeche/oberflaeche.js?v=1"></script>            <!-- vor dem Skript des Werkzeugs -->
```

`?v=` beim Bau aus dem Inhalt bilden (M20), nie von Hand. Gerüst und Zeichen-Funktionen (`WO.kopf`, `WO.startbild`, `WO.rand`, `WO.leiste`, `WO.knopf`, `WO.name`) wie im Schäfli. Musterseite mit jedem Baustein: http://127.0.0.1:9081/assets/oberflaeche/muster.html?haus=culinarium (Server von La Maison).

## Werte des Hauses (nur lesen, nie abtippen)

- **Namen der Werkzeuge:** nur `WO.name('<teil>')` bzw. `WO_HAUS.namen` (Teile: zentrale, website, karten, gaeste, marke, besuche, druck). Robert hat am 28.10.2026 Satz A gewählt: Der Tresen · Das Schaufenster · Die Pairing-Karte · Das Gästebuch · Das Markenbuch · Die Besucherliste · Die Plakatwerkstatt; dazu je Werkzeug ein Satz in `WO_HAUS.saetze`. Nirgends Namen fest schreiben. Python-Seiten lesen sie aus `kleid/culinarium.js` (Regex auf `namen:`). Wechseln die Namen, ändert sich nur diese eine Zeile.
- **Wege und Ports:** `WO_HAUS.wege` (`/_werkzeuge/<werkzeug>/`), `WO_HAUS.ports` (9081 Zentrale … 9087 Drucksachen, 9088 Werkbank, 8765 Website). Wege zu anderen Werkzeugen immer `http://127.0.0.1:<port>/…`, nie `localhost` (Fehlerbuch 10a); die Zentrale: `http://127.0.0.1:9081/_werkzeuge/maison/`.
- **Farben:** nur die Variablen. Dunkle Flächen `--wo-nacht` (#1C1B21 Strasse), `--wo-nacht2` (#3A3845 Schiefer), `--wo-tief` (#16151A Nacht); Licht `--wo-kerze` (#EF7649), `--wo-gold` (#F5A689 Kerze hell, Linien und Zeichen auf Dunkel), `--wo-akzent` (#B15736 Kerze tief, Betonung auf Hell); Raum `--wo-papier`, `--wo-blatt` (#FAF4F4 Warmweiss), `--wo-weiss`; Schrift `--wo-tinte` (#26242D), `--wo-leise` (#5B5763). Dirty Chicken: Klasse `.wo-dc` setzt Akzent auf Violett #8953A9, **nur** wo es um Dirty Chicken geht. Keine eigenen Hexwerte für dunkle Flächen (Fehlerbuch 10a). Werte stammen aus `website/assets/culinarium.css` (gebaut), nicht aus dem Entwurf (`CHARAKTER.md` nennt Kerze #CF7233, verbaut ist #EF7649; Oberchef 28.10.2026: die gebaute Website gilt).
- **Schrift:** Titel `var(--wo-titel)` = Fraunces, wght 340 (300–420), `font-variation-settings:"SOFT" 100` (in `.wo-sb__h`, `.wo-zw` schon gesetzt); Rudis Zeilen Klasse `.wo-rudi` (Versalien, Schrägstrich als Trenner im Text: «LAUCH / BLUMENKOHL / CHIPOTLE»); Lauf `var(--wo-sans)` = Instrument Sans (wie der Fliesstext der Website); Etiketten `var(--wo-etikett)` = Urbanist; Zahlen und Daten `var(--wo-mono)` = DM Mono (`.wo-zahl`). **Nie fett, nie kursiv** (die kursiven Stamm-Stellen sind im Kleid aufrecht gestellt).
- **Form:** Flächen wie angeschlagene Plakate (Radius 10 px wie die Website, oben eine Kante in Kerzenlicht); einziges Ornament = das «x» von «Momo x Rudi» zwischen zwei Linien (`--cu-x`, über jedem `.wo-zw`); Zeichen = das «C» der Wortmarke im Ring; Knopf = dunkle Platte mit rundem Knauf in Kerze. Keine Einkerbungen, keine Punkt-Etiketten, keine Pillen-Reihen, nicht das warmweisse Band mit Doppelrahmen (abgelehnt 26.10.).
- **Ganze Wortmarke** (wo das Werkzeug sie braucht, z. B. Briefkopf): `<svg viewBox="0 0 364.78 40.36"><use href="/assets/zeichen/marke.svg#wm"/></svg>`, Farbe über `color`. Nie neu zeichnen, nie aus dem Profilbild, nie eine eigene Nachzeichnung.
- **Aussenfoto des Startbilds:** `WO_HAUS.foto` = `/assets/bild/fassade-1600.webp` (Schlüssel `fassade`, «Die Fenster der Bar am Abend»). Weitere Fotos nur aus dem Register `BILD` in `website/bau.py` (der Bilder-Chat schärft, die Pfade bleiben).
- **Texte:** Besucher kennen Rudi, Momo und das Konzept nicht: kein Insider-Wort ohne Erklärung. Jeder Satz wertet auf (Sorgfalt, Handarbeit, der einzelne Gast), Zahlen nur als Exklusivität (wenige Plätze), nie als Menge.

## Änderungen

Nur `culinarium-maison` schreibt hier. Wer etwas am Kleid braucht, meldet es per SendMessage an `culinarium-maison` (oder über den Oberchef); nie in diesem Ordner selbst ändern. Jede Änderung mit Sicherung `*.vor-<was>-<datum>` und Eintrag unten.

| Datum | Was | Für wen |
|---|---|---|
| 28.10.2026 | Angelegt: Paket aus dem Schäfli, Kleid Culinarium, Zeichen «C» | alle sieben |
| 28.10.2026 | `kleid/culinarium.js`: lokal zeigen `WO_HAUS.wege` der anderen Werkzeuge auf `http://127.0.0.1:<port>/…` (Fund culinarium-reception); online relativ. Eigene Umschreibungen in den Werkzeugen nur noch für Wege, die mit «/» beginnen, oder ganz weg. Sicherung `kleid/culinarium.js.vor-wege-2026-10-28` | alle sechs |
| 28.10.2026 | Namen nach Roberts Wahl (Satz A «An der Bar») in `kleid/culinarium.js` (`namen`, neu `saetze`); Sicherung `kleid/culinarium.js.vor-namen-2026-10-28` | alle sieben |
| 29.10.2026 | `kleid/culinarium.js`: `namen.marke` heisst jetzt «Das Markenbuch» (Robert, über den Oberchef); Sicherung `kleid/culinarium.js.vor-markenbuch-2026-10-29` | alle sieben |
| 29.10.2026 | Startbild-Foto: srcset 640/1000 aus den Grössen der Website (bei 2× höchstens rund 2× die Anzeigebreite), erstes Startbild mit Vorrang, weitere (verborgene Ansichten) lazy, Platzhalter `WO_HAUS.fotoFarbe`; `WO_HAUS.foto` jetzt fassade-1000 statt -1600 (wer es vorlädt, lädt dasselbe Bild) | Oberchef, Leistung |
| 29.10.2026 | Bewegung für alle Werkzeuge: `bewegung.js` (vom Kleid async nachgeladen) lässt Zwischentitel, Karten, Blätter, Kacheln (`.wo-zw .wo-ag .wo-bk .wo-lage .wo-re .wo-bl .blatt .besuch .re-a .mw-t .wo__k`) gestaffelt heraufschweben, Fotos darin zoomen, Zahlen zoomen; Startbild-Auftritt in `kleid/culinarium.css` ruhiger und länger (Foto zoomt 2,6 s, Parallaxe per Scroll-Zeitachse), Knöpfe geben beim Drücken nach. Was eigene Bewegung hat (data-sw, data-r, laufende Animation), bleibt unberührt. Abschalten je Element: `data-wo-bw-nie` | Robert über Oberchef |
| 30.10.2026 | Bewegung vollständig (Kriterium 37): `kleid/culinarium.js` neu `WO_ZEILEN(el)` (Titel in Wörter mit Zeilennummer, bleibt ein Block, wenn sich der Umbruch ändern würde) und das Teilen des Startbild-Titels vor dem ersten Bild; `kleid/culinarium.css` Startbild-Titel Zeile für Zeile (0,11 s Staffel); `bewegung.js?v=2`: Zwischentitel (`.wo-zw`, `main h2`, `.wo-app h2`, `.ms-zeile > h2`) Zeile für Zeile, grosse Zahlen (ab 22 px, keine Jahreszahl) laufen von null hoch (Zwilling hält die Breite, schreibt das Werkzeug neu, gilt sein Wert), neu als Kacheln `.mk`, `.pk-karte` (Plakatwerkstatt), `.kap__b`, `.thema` (Anleitungen). Nie doppelt: alles in oder unter `[data-fd]`, `[data-r]`, `[data-sw]` bleibt dem Werkzeug, auch wenn es seine Bewegung erst später setzt. Gemessen: Tafel `_Oberchef/zeigen/culinarium/tresen-3010/`. Abschalten je Zahl: `data-wo-zl-nie` | Robert über Oberchef |
| 30.10.2026 | `bewegung.js?v=3`: `.blatt` aus der Liste genommen. In Plakatwerkstatt und Pairing-Karte ist `.blatt` das gesetzte Druckblatt, das vermessen wird (Fund culinarium-imprimerie: Schrift im PDF 3–5 mm daneben). Die Kennzahl-Blätter der Besucherliste bewegen sich selbst | alle sieben |

## 30.10.2026 (Abend) · Rand ohne ResizeObserver
- oberflaeche.js: Die Höhe des Randes (--wo-rand-top) wird nicht mehr über einen ResizeObserver nachgeführt, sondern über Mutation, Übergangsende, Aufklappen, load und Fenstergrösse (alles über ein requestAnimationFrame gebündelt, Wert nur geschrieben, wenn er sich ändert). Grund: WebKit meldete beim Laden des Schaufensters «ResizeObserver loop completed …», zusammen mit der neuen Bewegung; der Bedienlauf fiel auf 87/88. Danach 88/88 WebKit und Chromium 1440, 89/89 WebKit 390. Sicherung: oberflaeche.js.vor-ro-2026-10-30.

## Handy: Kopf-Knöpfe im Rand, Rundgang klappt den Rand auf (30.10.2026, Tor 5)
- `oberflaeche.js` `kopfImRand()`: Was der Kopf bis 900 px ausblendet (`.wo-kopf__r`), steht im Rand als `.wo-rand__kopf` noch einmal. Links mit Ziel, Knöpfe lösen den Kopf-Knopf aus. Was der Rand schon als Weg führt, steht nicht doppelt da. Den Block baut ein MutationObserver neu, wenn ein Werkzeug Kopf oder Rand neu zeichnet. Sichtbar ist er nur bis 900 px (`grund.css`).
- `WO.randZiel(e)` / `WO.randZurueck(ziel)`: Die Rundgänge (carte, bureau, registre, livre, reception/studio, maison/quelle/rundgang-vorlage) rufen sie in `sichtbar()`, in `zeige()` und in `ende()` auf. Liegt ein Ziel im zugeklappten Rand, klappt der Rundgang ihn auf. Ein kleines Ziel rückt dabei über die Karte. Beim nächsten Schritt ausserhalb des Rands und am Ende klappt der Rundgang ihn wieder zu. Einen Rand, den der Gast selbst geöffnet hat, lässt er offen.
