# Haus in der Cloud — Arbeitsweise für den Cloud-Chat

Dieser Ordner ist **ein Haus** (hier: Culinarium Hannover). Robert hat Recherche, Konzept und Website selbst gebaut. Alles danach entsteht und wird geprüft **hier in der Cloud**, nie auf Roberts Mac (Robert 31.10.2026: «allerspätestens einem Tag»). Du bist der Oberchef dieses Hauses.

## Aufbau des Ordners
- `<Haus>/website/` Website (Quelle), `website/_werkbank/` Werkbank, `<Haus>/_werkzeuge/` die sieben Werkzeuge, `_kette/` Stationen.
- `_Werkzeuge/` Prüfwerkzeuge (Abnahme-Tor `abnahme-tor/`, Messlauf `messlauf/`), `ROBERTS-KRITERIEN.md`, `OBERCHEF-PAKET.md`.
- `vorgaben/` Werkzeug-Master, Website-Master, Tasty-Sprache (Pflichtlektüre laut Oberchef-Paket).
- `cloud/haus.json` Server und Ziellisten des Hauses · `cloud/*.sh|py` Einrichtung, Verteilung, Tafeln · `.github/workflows/abnahme.yml` Prüfablauf.
- Kundenmaterial liegt im Zweig `quelle` (nur für den Bau nötig): `git fetch origin quelle && git worktree add /tmp/quelle origin/quelle && ln -sfn "/tmp/quelle/<Haus>/_quelle" "<Haus>/_quelle"`.

## Ablauf (Schleife bis grün)
1. **Lesen:** `_Werkzeuge/OBERCHEF-PAKET.md`, `_Werkzeuge/ROBERTS-KRITERIEN.md`, `vorgaben/`, `<Haus>/_werkzeuge/AUFTRAG-GEMEINSAM.md`, `UEBERGABE.md`/`CHARAKTER.md` des Hauses.
2. **Einrichten** (einmal je Sitzung): `bash cloud/vorbereiten.sh chromium` und `bash cloud/server.sh` (gleiche Ports wie auf dem Mac, 9081–9088). Für schnelle Einzelblicke reicht Chromium hier; die volle Prüfung läuft in Actions.
3. **Bauen** nach dem Oberchef-Paket: Werkbank, die sieben Werkzeuge, Drucksachen. Kein Teil-Chat nötig, du arbeitest Revier für Revier; nur Roberts Auftrag und echte Fehler bauen. Sicherung vor jeder Änderung (`…vor-<thema>-<datum>`, sie wird nicht eingecheckt).
4. **Prüfen lassen:** committen und pushen mit `[abnahme]` in der Nachricht (alle Werkzeuge) oder `[abnahme: tresen,gaestebuch]` (nur diese). GitHub verteilt das auf bis zu ~190 Rechner (je Werkzeug Inventar in WebKit 1440, je Werkzeug und Breite 1280/1000/390 die Stichprobe, je Werkzeuggruppe × Chromium/WebKit × 1440/1280/1000/390 der Messlauf).
5. **Warten ohne Leerlauf:** `until git fetch -q origin ergebnis && git show origin/ergebnis:ergebnis/laeufe/<zweig>/lauf.json 2>/dev/null | grep -q "$(git rev-parse HEAD)"; do sleep 120; done` — dann `git worktree add -f /tmp/erg origin/ergebnis`.
6. **Funde lesen:** `/tmp/erg/ergebnis/laeufe/<zweig>/index.html` (Übersicht), `tor/funde.json` + `tor/b/*.jpg` (Abdeckungstafel, Bild je Fund), `messlauf/funde.json` + `messlauf/bilder/` (rot umrandete Ausschnitte).
7. **Mit den Augen prüfen:** jedes Fundbild und mindestens 15 zufällige Zustandsbilder je Werkzeug mit dem Read-Werkzeug ansehen (Kriterien **A** in ROBERTS-KRITERIEN.md). Urteile in `augen.json` des Laufs.
8. **Reparieren**, dann zurück zu Schritt 4. Fehlalarm einer Prüfregel: Regel in `messen.js`/`seite.js` schärfen (mit Beleg), nie den Fund wegerklären.
9. **Fertig** erst bei 100 % Abdeckung, null offenen Funden, nichts «nicht erreicht». Dann Meldung an Robert: **ein Satz plus Link** (siehe unten).

## Link für Robert
- Jeder Lauf liegt im Zweig `ergebnis` unter `ergebnis/laeufe/<zweig>/`; die Startseite `index.html` listet alle Läufe.
- Ist das Vercel-Projekt mit diesem Ordner verbunden (siehe `cloud/ANLEITUNG.md`), hat jeder Zweig automatisch eine Vorschau-Adresse; der Zweig `ergebnis` ist die Abnahme-Seite. Sonst: Link auf den Lauf in GitHub Actions (Paket «ergebnis»).

## Feste Regeln (aus Roberts globalen Regeln)
- Nichts verschicken, nichts veröffentlichen, nichts bezahlen. Die Live-Website des Hauses (z. B. culinarium-hannover-entwurf.vercel.app) wird **nicht** geändert, solange Robert sie eingefroren hat.
- Keine Schlüssel, keine Passwörter einchecken. KI-Prüfläufe nur mit Probe-Antworten (ohne `*_KI=1`).
- Grand Beau-Rivage nie anfassen. Port 8765 gehört nicht hierher.
- Antworten an Robert: Deutsch, kurz, Alltagssprache, Link vorne.
- Kosten: GitHub zählt jede angefangene Rechner-Minute. Ein voller Lauf kostet die in `zeiten.json` gemessenen Minuten; gezielte Läufe (`[abnahme: werkzeug]`) bevorzugen, wenn nur ein Werkzeug geändert wurde.
