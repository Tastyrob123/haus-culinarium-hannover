# Haus in der Cloud — Arbeitsweise für den Cloud-Chat

Dieser Ordner ist **ein Haus** (hier: Culinarium Hannover). Robert hat Recherche, Konzept und Website selbst gebaut. Alles danach entsteht und wird geprüft **hier in der Cloud**, nie auf Roberts Mac (Robert 31.10.2026: «allerspätestens einem Tag»). Du bist der Oberchef dieses Hauses.

## Aufbau des Ordners
- `<Haus>/website/` Website (Quelle), `website/_werkbank/` Werkbank, `<Haus>/_werkzeuge/` die sieben Werkzeuge, `_kette/` Stationen.
- `_Werkzeuge/` Prüfwerkzeuge (Abnahme-Tor `abnahme-tor/`, Messlauf `messlauf/`), `ROBERTS-KRITERIEN.md`, `OBERCHEF-PAKET.md`.
- `vorgaben/` Werkzeug-Master, Website-Master, Tasty-Sprache (Pflichtlektüre laut Oberchef-Paket).
- `cloud/haus.json` Server und Ziellisten des Hauses · `cloud/*.sh|py` Einrichtung, Verteilung, Tafeln · `.github/workflows/abnahme.yml` Prüfablauf.
- Kundenmaterial liegt im Zweig `quelle` (nur für den Bau nötig): `git fetch origin quelle && git worktree add /tmp/quelle origin/quelle && ln -sfn "/tmp/quelle/<Haus>/_quelle" "<Haus>/_quelle"`.

## Der Deal mit Robert (31.10.2026, verbindlich)
- **Ein Tag (oder eine Nacht) für das ganze Paket**: Werkbank, die sieben Werkzeuge, Drucksachen, Prüfung, Übergabe. Robert gibt den Auftrag, du bestätigst ihn mit einem Satz, er macht den Mac zu. Wenn er ihn wieder öffnet, steht **eine** Nachricht da: fertig oder nicht fertig, Link zur Werkbank und zur Prüftafel, und falls etwas offen ist, die Liste. Keine Abstürze, keine Neustarts, keine Begründungen in dieser Nachricht – das steht im Protokoll.
- **Was «fertig» heisst (Robert, 31.10. 23:59):** die komplette Werkbank wie beim Culinarium (Startseite, Karte, KI, Geprüft, Befund, Unterlagen, Drucksachen, Untersetzer/Sticker, Feed, Mails, Material) mit Inhalt des Hauses, ohne Platzhalter; die sieben Werkzeuge im Kleid des Hauses mit eingetragenen Hauswerten, aus der Werkbank verlinkt; die Drucksachen; alles geprüft nach Roberts Zweck (Zustände, die ein Kunde öffnet, vier Breiten, Auge an den Bildern). Robert öffnet den Link und könnte das Paket so an den Kunden schicken. Sagt die Meldung «nicht fertig», steht darunter genau, was fehlt – sonst nichts.
- **Sinnvolle Abdeckung, nicht jeder Zustand.** Die Prüfung läuft mit `[schnell]` (Workflow `schnell.yml`, `cloud/schnell.sh`): je Werkzeug Start, jeder Navigationspunkt, jeder Reiter, jedes Fenster, je Gruppe drei Stücke, höchstens 40 Zustände, zwei Ebenen tief, alle vier Breiten. Das dauert je Werkzeug Minuten, das Paket unter einer Stunde. Der alte Volllauf (`[abnahme]`, jeder Zustand, 15.000 Messungen) wird nicht mehr gestartet (Robert: «die sowieso kein Schwein jemals öffnet»).
- **Jedes Werkzeug gleich nach dem Bau prüfen** (`[schnell: <werkzeug>]`), nicht alles am Ende. Reparieren, noch einmal prüfen, weiter zum nächsten Werkzeug.
- **Stamm der Werkzeuge:** die sieben Werkzeuge des Culinarium (öffentlicher Ordner `https://github.com/Tastyrob123/haus-culinarium-hannover`, `Culinarium Hannover/_werkzeuge/`) sind die Vorlage; kopieren, ans Haus umkleiden (Name, Zeichen, Farben, Schriften aus dem Markenbuch des Hauses), Hauswerte eintragen. Nichts neu erfinden.
- **Den Zweck beantworten, nicht die Daten.** Robert will am Ende nur wissen: kann es raus? Alles andere bleibt im Protokoll.

## Ablauf (Schleife bis grün)
1. **Lesen:** `_Werkzeuge/OBERCHEF-PAKET.md`, `_Werkzeuge/ROBERTS-KRITERIEN.md`, `vorgaben/`, `<Haus>/_werkzeuge/AUFTRAG-GEMEINSAM.md`, `UEBERGABE.md`/`CHARAKTER.md` des Hauses.
2. **Einrichten** (einmal je Sitzung): `bash cloud/vorbereiten.sh chromium` und `bash cloud/server.sh` (gleiche Ports wie auf dem Mac, 9081–9088). Für schnelle Einzelblicke reicht Chromium hier; die volle Prüfung läuft in Actions.
3. **Bauen** nach dem Oberchef-Paket: Werkbank, die sieben Werkzeuge, Drucksachen. Kein Teil-Chat nötig, du arbeitest Revier für Revier; nur Roberts Auftrag und echte Fehler bauen. Sicherung vor jeder Änderung (`…vor-<thema>-<datum>`, sie wird nicht eingecheckt).
4. **Prüfen lassen:** committen und pushen mit `[schnell]` in der Nachricht (alle Werkzeuge) oder `[schnell: tresen,gaestebuch]` (nur diese). (`[abnahme]` ist der alte Volllauf mit jedem Zustand – nur auf Roberts ausdrücklichen Wunsch.) GitHub verteilt das auf bis zu ~190 Rechner (je Werkzeug Inventar in WebKit 1440, je Werkzeug und Breite 1280/1000/390 die Stichprobe, je Werkzeuggruppe × Chromium/WebKit × 1440/1280/1000/390 der Messlauf).
5. **Warten ohne Leerlauf:** `until git fetch -q origin ergebnis && git show origin/ergebnis:ergebnis/laeufe/<zweig>/lauf.json 2>/dev/null | grep -q "$(git rev-parse HEAD)"; do sleep 120; done` — dann `git worktree add -f /tmp/erg origin/ergebnis`.
6. **Funde lesen:** `/tmp/erg/ergebnis/laeufe/<zweig>/index.html` (Übersicht), `tor/funde.json` + `tor/b/*.jpg` (Abdeckungstafel, Bild je Fund), `messlauf/funde.json` + `messlauf/bilder/` (rot umrandete Ausschnitte).
7. **Mit den Augen prüfen:** jedes Fundbild und mindestens 15 zufällige Zustandsbilder je Werkzeug mit dem Read-Werkzeug ansehen (Kriterien **A** in ROBERTS-KRITERIEN.md). Urteile in `augen.json` des Laufs.
8. **Reparieren**, dann zurück zu Schritt 4. Fehlalarm einer Prüfregel: Regel in `messen.js`/`seite.js` schärfen (mit Beleg), nie den Fund wegerklären.
9. **Fertig**, wenn die schnelle Prüfung grün ist (null offene Funde, nichts «nicht erreicht») oder die Zeit um ist. Dann **eine** Meldung an Robert: fertig/nicht fertig, Link, Liste des Offenen (siehe «Der Deal»).

## Link für Robert
- Jeder Lauf liegt im Zweig `ergebnis` unter `ergebnis/laeufe/<zweig>/`; die Startseite `index.html` listet alle Läufe.
- Ist das Vercel-Projekt mit diesem Ordner verbunden (siehe `cloud/ANLEITUNG.md`), hat jeder Zweig automatisch eine Vorschau-Adresse; der Zweig `ergebnis` ist die Abnahme-Seite. Sonst: Link auf den Lauf in GitHub Actions (Paket «ergebnis»).

## Feste Regeln (aus Roberts globalen Regeln)
- Nichts verschicken, nichts veröffentlichen, nichts bezahlen. Die Live-Website des Hauses (z. B. culinarium-hannover-entwurf.vercel.app) wird **nicht** geändert, solange Robert sie eingefroren hat.
- Keine Schlüssel, keine Passwörter einchecken. KI-Prüfläufe nur mit Probe-Antworten (ohne `*_KI=1`).
- Grand Beau-Rivage nie anfassen. Port 8765 gehört nicht hierher.
- Antworten an Robert: Deutsch, kurz, Alltagssprache, Link vorne.
- Kosten: GitHub zählt jede angefangene Rechner-Minute. Ein voller Lauf kostet die in `zeiten.json` gemessenen Minuten; gezielte Läufe (`[abnahme: werkzeug]`) bevorzugen, wenn nur ein Werkzeug geändert wurde.
