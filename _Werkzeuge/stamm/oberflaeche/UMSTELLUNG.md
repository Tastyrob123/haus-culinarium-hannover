---
tags: [projekt, website]
status: aktiv
---

# Werkzeug-Oberfläche · Umstellung der sechs Werkzeuge je Haus

Angelegt am 17.10.2026 (Chat «Werkzeug-Oberfläche», Auftrag Oberchef · vier Hotels). Vorlage mit allen Bildschirmen: `~/Desktop/Website-Projekte/_Werkzeug-Oberflaeche/` (http://127.0.0.1:8995/).

## Was Robert entschieden hat

- Innerhalb eines Hauses sehen **Le Bureau, La Carte, La Réception, Le Livre, Le Registre und L’Imprimerie** gleich aus: gleicher Kopf, gleiche Navigation, gleiches Startbild, gleiche Knöpfe, Listen, Felder, Meldungen. Nur der Inhalt wechselt. Bei **La Carte** darf der Arbeitsbereich mit der Karte anders sein, Rahmen und Startbild nicht.
- **La Maison bleibt je Haus eigen** («das kannst du sehr individuell für jedes Hotel halten»). Sie wird nicht umgestellt; jedes Werkzeug erreicht sie über das Zeichen bzw. den Haus-Knopf im Kopf.
- **Je Haus eine eigene Stilfassung** bei gleichem Aufbau und gleichen Wegen («dass man jedes der Tools für jedes Hotel stilistisch anpasst»): Formen, Ornamente, Kanten, Bildbehandlung, Schriftmischung.
- **Rahmen je Haus:** Carlton-Europe = «Die Inseln» · Waldhotel Doldenhorn und Landgasthof Ruedihus = «Die Bühne» («bei doldenhof und ruedlihaus die bühne»). **Berghotel Gasterntal = «Die Bühne»** (nicht von Robert gewählt; gesetzt wie die beiden anderen Häuser im Kandertal, Wechsel = eine Zeile in `kleid/gasterntal.js`).

## Was im Paket liegt

| Datei | Was |
|---|---|
| `grund.css` | alle Bausteine: Schrift, Knöpfe (mit Speichern-Zuständen grau/gelb/grün), Segment-Wahl, Felder, Wahl, Marke «Entwurf», Startbild, Lage (drei Fächer), Kacheln mit Foto, Bereich-Liste, Eingang, Brief, Karten-Liste, Feld-Fenster, Quittung, Rand, Leiste, Kopf-Marke, Handy |
| `rahmen-inseln.css` | wo was sitzt, «Die Inseln» |
| `rahmen-buehne.css` | wo was sitzt, «Die Bühne» |
| `kleid/<haus>.css` | Farben, Schriften, Rundungen, Tapete und Stil des Hauses (carlton, doldenhorn, ruedihus, gasterntal) |
| `kleid/<haus>.js` | Hauswerte: Name, Ort, Welt (Grandhotel- oder Landhaus-Namen), Rahmen, Aussenfoto, Zeichen, Wege der Werkzeuge. Setzt `data-wo-haus` und `data-wo-rahmen` am `<html>` |
| `kleid/*-zeichen.svg`, `doldenhorn-tanne(n).svg` | Zeichen der Häuser, Tannenreihe des Doldenhorn |
| `oberflaeche.js` | baut Kopf, Startbild, Rand, Leiste, Knöpfe als HTML (`WO.kopf`, `WO.startbild`, `WO.rand`, `WO.leiste`, `WO.knopf`, `WO.ic`, `WO.zeichen`, `WO.gruss`, `WO.name`) und klappt am Handy den Rand auf und nach der Wahl wieder zu |
| `muster.html` | jeder Baustein einmal: `/assets/oberflaeche/muster.html?haus=<haus>` |

Alle Klassen und Werte tragen die Vorsilbe `wo-`. Dadurch kann das Paket neben dem bisherigen CSS eines Werkzeugs liegen, ohne etwas zu verschieben: was umgestellt ist, nimmt `wo-`-Klassen, alles andere bleibt, wie es war.

## Ins Haus legen (einmal je Haus)

1. Sicherung: `cp -cR "<Haus>/assets" "<Haus>/_sicherung/vor-oberflaeche-<datum>/assets"` (APFS-Klon) und je Werkzeug den Ordner, der geändert wird.
2. Paket kopieren: `rsync -a ~/Desktop/Website-Projekte/_Werkzeuge/stamm/oberflaeche/ "<Haus>/assets/oberflaeche/"`. Der Weg ist lokal und online derselbe (`/assets/oberflaeche/…`).
3. Prüfen: `/assets/oberflaeche/muster.html?haus=<haus>` im Haus öffnen (unsichtbar, Abschnitt Prüfen). Alles hat Schrift, Tapete, Zeichen und Foto; keine 404.
4. `kleid/<haus>.js`: die Wege der Werkzeuge mit dem Haus abgleichen (Stand 17.10.: Carlton `/control/`, `/maison/`, sonst `/_werkzeuge/<werkzeug>/`; Doldenhorn, Ruedihus, Gasterntal Le Bureau unter `/studio/`, La Maison unter `/_werkzeuge/maison/`).

## Ein Werkzeug umstellen (gilt für alle sechs)

**Was ersetzt wird:** der Rahmen (Kopf, Rand, Leiste), das Startbild jeder Ansicht und die Übersicht-Bausteine (Lage, Kacheln, Bereich-Listen, Knöpfe in Kopf, Startbild und Leiste). **Was bleibt:** jede Funktion, jeder Weg (`/api/…`), alle Daten, alle Ids, `data-`-Attribute und Klick-Handler, die Arbeitsflächen im Inneren (Seite bearbeiten mit Vorschau, Karten-Satz, Brief-Editor, Bildarchiv, Statistiken, Canva-Fläche), Fenster (`#fenster`), Quittungen (`#meldung`), Fehlermelder, Startfehler-Tür, Rundgang, «Zur Werkbank».

1. **Kopf der Seite** (`index.html`), in dieser Reihenfolge:
   ```html
   <script src="/assets/oberflaeche/kleid/<haus>.js?v=1"></script>          <!-- vor allem anderen, ohne defer -->
   … bisheriges CSS des Werkzeugs …
   <link rel="stylesheet" href="/assets/oberflaeche/grund.css?v=1">
   <link rel="stylesheet" href="/assets/oberflaeche/rahmen-<inseln|buehne>.css?v=1">
   <link rel="stylesheet" href="/assets/oberflaeche/kleid/<haus>.css?v=1">
   ```
   Vor dem Skript des Werkzeugs: `<script src="/assets/oberflaeche/oberflaeche.js?v=1"></script>`.
2. **Gerüst** (`index.html`): Ids bleiben, nur die Klassen wechseln.
   ```html
   <body class="… wo-app">
     <header class="wo-kopf" id="kopf"></header>
     <aside  class="wo-rand" id="rand"></aside>      <!-- Reihenfolge egal, der Rahmen ordnet -->
     <main   class="wo-raum" id="haupt">…</main>
     <footer class="wo-leiste" id="leiste"></footer>
   ```
   Ein Behälter darum (`<div class="wo-app">`) geht auch. Skripte, die das Startbild selbst bauen (`buehne.js`), fallen weg. In `schweben.js`-Aufrufen und im Rundgang die Wähler auf die neuen Klassen setzen (`.wo-sb`, `.wo-lage`, `.wo-aufg > .wo-ag`, `.wo-ber > .wo-bk`, `#rand`).
3. **Zeichen-Funktionen** des Werkzeugs (Namen am Carlton): Ausgabe durch das Paket ersetzen, Handler danach wie bisher setzen.
   - `kopfLeiste()` → `$('#kopf').innerHTML = WO.kopf({ werkzeug, unter, titel, stand, pruefung, anleitung, website, marke: 'data-gehe="start"' })`; beim Klick auf die Marke `e.preventDefault()`.
   - `rand()` → `$('#rand').innerHTML = WO.rand([{ titel, eintraege: [{ text, zahl, an, attr: 'data-gehe="…"', extra }] }], { website, anleitung, pruefung })`. Eigene «Bereiche»-Knöpfe fürs Handy entfernen, das Paket bringt sie im Kopf mit.
   - `leiste()` → `$('#leiste').innerHTML = WO.leiste({ titel, satz, entwurf, knoepfe })` mit `WO.knopf(text, zeichen, art, { id, klein: true, disabled })`. Speichern: `art` = `'glas'` (nichts offen), `'wartet'` (Eingaben offen, gelb), `'fertig'` («Gespeichert», grün). Ids wie `#l-sp`, `#l-vgl`, `#l-raus` bleiben.
   - `kopf(…)` / Startbild → `WO.startbild({ werkzeug, zier, h1, satz, knoepfe, art: 'voll' | 'buehne', foto })`. Übersicht = `'voll'` mit dem Aussenfoto (ohne `foto`), jede andere Ansicht = `'buehne'` (darf ein eigenes Foto tragen). Gruss nach Tageszeit mit `WO.gruss()`. `zier` ist HTML (schon maskiert).
   - Übersicht: `.lage/.lg` → `wo-lage/wo-lg` (Text im `<p>`, Weg als `wo-lk`), Kacheln → `<button class="wo-ag" data-gehe><span class="wo-ag__b"><img></span><span class="wo-ag__t"><i class="wo-ag__z">…</i><b>…</b><span>…</span></span></button>` in `wo-aufg`, Bereiche → `wo-bk` in `wo-ber`. Überschriften `<h2 class="wo-zw">Häufig <em>gebraucht</em></h2>`. Fertige Form zum Abschreiben: `muster.html` und die Vorlage `_Werkzeug-Oberflaeche/bau.py`.
4. **Fassungsnummern hochzählen** (`?v=`) an jeder geänderten Datei, sonst zeigt Vercel die alte.

### Je Werkzeug (Stand Carlton 17.10.2026; Doldenhorn und Ruedihus haben dieselben Funktionsnamen, vor dem Umbau nachsehen)

| Werkzeug | Dateien | Zeichen-Funktionen | Besonderheit | Zeit (ungefähr) |
|---|---|---|---|---|
| **Le Bureau** | `control/index.html`, `bureau.js`, `rundgang.js` (Doldenhorn/Ruedihus: `studio/…`) | `kopfLeiste`, `rand`, `leiste`, `kopf`, `start` | Probelauf gemacht (unten). Die Ansicht «Bereich» (Stellen + Seitenvorschau) bleibt innen unverändert | 20 min |
| **La Réception** | `_werkzeuge/reception/index.html`, `reception.js` | `kopfLeiste`, `rand`, `leiste`, `kopf`, `start` | gleicher Bau wie Le Bureau. Leiste: «Text kopieren», «Als PDF speichern»; Brief-Editor und Eingang bleiben innen, die Eingangsliste darf `wo-eing`/`wo-an` nehmen | 30 min |
| **Le Registre** | `_werkzeuge/registre/index.html`, `registre.js` | `kopfLeiste`, `rand`, `leiste`, `kopf`, `start` | Rand steht im HTML vor dem Kopf (egal, der Rahmen ordnet). Zahlen-Kacheln bleiben eigene Bausteine | 30 min |
| **Le Livre** | `_werkzeuge/livre/index.html`, `livre.js` | `kopf`, `rand`, `leiste`, Startbild in `titel(ansicht, mono, h1, satz, kn, stats)` («li-hero») | das eigene Startbild «li-hero» weicht `WO.startbild`, die Zahlen (`stats`) stehen darunter als `wo-lage`; sechs Sprachen: Texte der Oberfläche wie bisher aus den Sprachdaten übergeben | 40 min |
| **La Carte** | `_werkzeuge/carte/index.html`, `carte.js`, `carte.css` | `rand`, `kopf`, `leiste`; Gerüst mit `#oben` (Kopf) und `#kopf` (Kopf der Arbeitsfläche) | `#oben` wird `wo-kopf`, `#kopf` wird das Startbild als `'buehne'`. Karten im Rand mit Foto: `WO.rand`-Einträge mit `extra` (oder `wo-rk`-Zeilen wie in der Vorlage). **Arbeitsbereich (Liste, Vorschau, Fortgeschritten) bleibt**, nur Knöpfe und Felder dürfen `wo-` nehmen | 45 min |
| **L’Imprimerie** | `_werkzeuge/imprimerie/index.html`, `start.js`, `studio.js`, `studio.css` | eigenes Gerüst (`header.kopf`, `main.studio`, `aside.links`, `aside.rechts`) | Kopf → `WO.kopf`, `aside.links` → `wo-rand`, Startseite bekommt `WO.startbild('voll')`. Die Canva-Fläche (Bearbeiten) bleibt; dort nur Kopf und Knöpfe tauschen | 60 min |

Dazu je Werkzeug die eigene Prüfung (unten). **La Maison wird nicht angefasst.** Ein Haus mit sechs Werkzeugen braucht so etwa vier Stunden, die Prüfung eingeschlossen.

### Online (`online.json` je Werkzeug)

Das Paket liegt unter `assets/`. Damit es sicher mitgeht, trägt jedes umgestellte Werkzeug in seiner Andock-Datei unter `statik` ein:

```json
"statik": { "assets/oberflaeche": "assets/oberflaeche", … bisherige Einträge … }
```

Mehrere Werkzeuge dürfen das gleich eintragen (es wird nur kopiert). Sonst ändert sich nichts an `online.json`: keine neuen Funktionen, Wege oder Umleitungen. Nach `werkzeuge_online.py stell` liegt `assets/oberflaeche/grund.css` im Online-Ordner.

## Prüfen (je Werkzeug, vor dem Melden)

Unsichtbar (Playwright headless, nie ein Fenster auf Roberts Bildschirm, `mailto:`/`tel:` abfangen), **1440 × 900 und 390 × 844, Chromium und Safari-Kern (WebKit)**:

1. Laden ohne Skriptfehler und ohne 404 (auch Schrift, Tapete, Zeichen, Foto).
2. Kein seitliches Verrutschen (`scrollWidth - innerWidth = 0`, auch bei 320).
3. **Senkrecht hängt nichts:** kein Element mit eigener senkrechter Scrollfläche (`overflow-y:auto|scroll` und `scrollHeight > clientHeight`); das Mausrad läuft immer an die Seite weiter. Seitliche Bänder dürfen bleiben.
4. **Jede Hauptfunktion einmal bedienen**, nicht nur laden: im Rand einen Bereich wählen (Titel im Kopf wechselt), eine Eingabe machen (Speichern wird gelb), speichern (Leiste zeigt den Entwurf, «Vorher, nachher» wird aktiv), über die Marke zurück zur Übersicht, eine Arbeitsfläche öffnen. Je Werkzeug zusätzlich das Eigene: La Réception eine Anfrage öffnen und den Brief als PDF; La Carte einen Eintrag ändern und die Probe-PDF; Le Livre ein Bild herunterladen; Le Registre Zeitraum wechseln; L’Imprimerie eine Vorlage öffnen.
5. Am Handy: «Bereiche» klappt den Rand auf, eine Wahl klappt ihn zu.
6. Bild ansehen: Startbild gleich wie in den anderen Werkzeugen des Hauses (gleiche Form, Grösse, Foto), Rot nur für «Entwurf».

Vorlage für den Prüflauf: `~/Desktop/Website-Projekte/_Werkzeug-Oberflaeche/_qa/probe.js` (Le Bureau, 13 Prüfpunkte je Lauf, vier Läufe). Geprüft wird an einer Kopie oder einem eigenen Port mit Wegwerf-Daten, nie gegen die echten Daten des Hauses.

## Probelauf Le Bureau · Carlton-Europe (17.10.2026)

- Kopie: `~/Desktop/Website-Projekte/_Probe Carlton Oberflaeche 1710/` (APFS-Klon), Server `python3 serve.py 8997`. Das Haus selbst ist unberührt.
- Geändert in der Kopie: `control/index.html` (18 Zeilen), `control/bureau.js` (Kopf, Rand, Leiste, Startbild, Übersicht; rund 100 Zeilen), `control/rundgang.js` (3 Wähler). Paket unter `assets/oberflaeche/`.
- Ergebnis `_qa/probe.js`: Chromium und WebKit, 1440 und 390, je 13 Prüfpunkte grün (Übersicht mit Startbild, 3 Fächern, 8 Kacheln, 12 Bereichen; sechs Werkzeuge im Kopf; kein Verrutschen; keine Scrollfläche; Handy-Rand auf und zu; Angaben mit Bühne und Titel; Eingabe gelb; Speichern legt in den Entwurf; «Vorher, nachher» aktiv; Marke zurück; Bereich mit Seitenvorschau).
- Zeit: rund 10 Minuten Einlesen in `bureau.js`, 9 Minuten Umbau und vier Prüfläufe. Speichern dauert in Le Bureau rund 8 Sekunden (setzt die Seiten neu), Prüfläufe darauf warten lassen.

## Fallen, die schon einmal Zeit gekostet haben

- `url()` in einer CSS-Variable wird dort aufgelöst, wo die Variable **benutzt** wird (in `grund.css`), nicht wo sie steht. Deshalb steht die Tapete in den Kleidern mit absolutem Weg (`/assets/img/…`).
- Werkzeuge zeichnen den Rand beim Klick sofort neu; das Zuklappen am Handy läuft deshalb in der Fangphase (`oberflaeche.js`). Nicht auf `bubble` zurückbauen.
- Einträge als `<button>` bekommen sonst Rahmen und Grund des Browsers; `grund.css` setzt sie zurück. Eigene Knopf-Klassen im Rand nicht wieder einführen.
- `zier` im Startbild ist HTML; schon maskierte Namen («Zimmer &amp; Suiten») nicht noch einmal maskieren.
- Ein Leerzeichen am Ende ist «nichts geändert» (R10): zum Prüfen ein echtes Zeichen tippen.

## Gasterntal

Die Werkzeuge des Gasterntal werden noch gebaut und entstehen direkt mit diesem Paket: `kleid/gasterntal.js` + `kleid/gasterntal.css` (Fels, Kander, Tanne; Barlow Semi, Lauben-Raute, Tannengrün als Akzent, Holz als Gold, Rot nur für «Entwurf»), Rahmen «Die Bühne». Das Gerüst und die Zeichen-Funktionen von Anfang an wie oben bauen, kein eigener Kopf und kein eigenes Startbild.

## Zurück

Jede Änderung ist auf die Zeilen in Abschnitt «Ein Werkzeug umstellen» begrenzt. Zurück: die Sicherung aus Schritt 1 zurückkopieren oder die fünf Kopf-Zeilen entfernen und die Zeichen-Funktionen aus der Sicherung nehmen; Funktionen und Daten waren nie betroffen.
