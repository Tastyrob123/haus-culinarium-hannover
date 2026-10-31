---
tags: [projekt, website]
status: aktiv
---

# Culinarium Hannover · Demo-Check der Website (Station D, 28.10.2026 abends)

**Urteil: Demo-Check grün.** Jeder sichtbare Weg der neun Seiten ist in Chromium und WebKit bei 1440 × 900, 1000 × 800 und 390 × 844 bedient. Es gab keinen Fehler, keinen toten Weg, kein Verrutschen und keinen Anschnitt. Nichts geht ungewollt raus. Ein Fehler stört die Demo nicht und steht auf der Liste: Esc schliesst das Menü nicht. Reparaturen waren nicht nötig, an der Website ist nichts geändert.

Geprüft: http://localhost:8765/ (Roberts Server, Version 26191, nicht angefasst). Prüfchat Gestaltung, hat nie an der Website gebaut. Headless, eine Browser-Instanz, mailto, tel und alle Anfragen nach aussen abgefangen.
Bilder: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/demo-check/safari-1000-index.jpg (je Seite `safari-1000-*`, `chrome-1440-*`, Handy `safari-390-alle-1..3`, Bedienung `bedienen-*`). Ordner `~/Desktop/Website-Projekte/_Oberchef/zeigen/culinarium/demo-check/`.

## Zahlen

| Prüfung | Ergebnis |
|---|---|
| Seitenaufrufe (9 Seiten × 2 Motoren × 3 Breiten) | 54 von 54: Antwort 200, 0 Konsolenfehler, 0 Skriptfehler, 0 Antworten ≥ 400, 0 px seitlicher Überlauf, 0 leere Bilder |
| Bildschirme mit dem Auge angesehen | 445 (Chromium 1440: 82, WebKit 1440: 82, WebKit 1000: 85, WebKit 390: 98, Chromium 390: 98) |
| Bedienlauf (6 Läufe, je 13 bis 15 Punkte) | 86 von 86 grün |
| Interne Verweise | 10 Ziele, alle 200; Sprungmarke `abend.html#warteliste` vorhanden |
| Texte (sichtbarer Text, alt, title, aria-label, meta) | kein Schweizer «ss», keine Bindestrich-Spanne zwischen Zahlen, keine Platzhalter, kein fremdes Haus, kein doppeltes Wort; jede Seite `noindex, nofollow` |
| Ladezeit gedrosselt (Chromium) | 1440, CPU 4×, schnelles Netz: Laden 0,4–0,6 s, LCP 0,3–1,5 s · 390, 4G (150 ms, 9 Mbit/s): CPU 4× Laden 1,3–1,8 s, LCP 0,9–2,4 s; CPU 6× gleich (LCP höchstens 2,4 s auf «Der Abend») · CLS höchstens 0,003 |
| Flüssigkeit beim Scrollen (gedrosselt 4× und 6×) | Bildabstand p50 8,3 ms, p95 ≤ 10,2 ms, ein Bild über 50 ms (Startseite 390, 4×) |

## Bediente Wege (jeder in allen sechs Kombinationen)

- **Leiste und Menü:** Das Menü öffnet mit allen Einträgen, schliesst mit dem Knopf, und ein Eintrag führt zur Seite. Auf der Startseite bleibt die Leiste im Auftakt ausgeblendet und kommt beim Hochscrollen und nach dem Auftakt; das ist gewollt (`culinarium.js` Zeile 130).
- **Startseite:** Alle 7 Fragen «Gut zu wissen» öffnen. Beide Filme laden (familie.mp4, opening.mp4), «Film noch einmal» läuft.
- **Alle Abende:** Alle 14 Plakate öffnen ihr Fenster mit Menü, Drinks, Ablauf und Stand. Das Fenster schliesst mit dem Knopf.
- **Der Abend, Platz buchen:** Fenster, Plätze plus und minus, Name, E-Mail, «Jetzt bezahlen», danach «Verbindung zu PayPal …» als Probe, dann Ticket (Probe) und «Fertig». Der Hinweis sagt deutlich, dass nichts verschickt wird.
- **Warteliste:** Leer abgeschickt meldet sie «Bitte Name und E-Mail eintragen». Ausgefüllt bestätigt sie «Danke, Probe Gast. Du stehst auf der Liste …» und «Diese Vorschau verschickt nichts».
- **Fuss «Vormerken»** (auf jeder Seite): führt zu `abend.html#warteliste` und übernimmt die E-Mail.
- **Dirty Chicken:** Alle 3 Gerichte sind wählbar, der Film lädt.
- **Fuss, Rechtstexte, Instagram, Google Maps, Telefon:** Die Ziele stimmen. Externe Wege und tel sind abgefangen und wurden nie ausgeführt.

## Funde

Demo-störend: keine.

Auf die Liste «Nach dem Auftrag» (nicht repariert, stört die Demo nicht):
1. **Esc schliesst das Menü nicht** (Handy und schmale Fenster). Nur der Knopf «Schließen» schliesst es. Abhilfe: in `website/assets/culinarium.js` beim Menü ein `keydown`-Esc, das denselben Weg geht wie der Knopf. Vor dem Hochladen bewusst nicht geändert, damit der geprüfte Stand bleibt.
2. **Knopf «Zur Website der Bar»** (bar.html) zeigt lokal in den Nachbarordner und antwortet auf :8765 mit 404. Online setzt `_online/online.py` ihn auf `wildside/index.html` (`pruef` blockiert sonst das Hochladen). Kein Fund für die Online-Fassung, dort nach dem Hochladen einmal klicken.
3. **Chronik der Startseite, September 2026:** «Der Abend ist ausgebucht, bevor er beginnt.» steht im Präsens für einen vergangenen Abend. Textfrage, nicht falsch.
4. **«Der Abend»:** Oben steht «Der nächste Termin steht noch nicht fest», darunter liegen die Beispiel-Termine 27./28.11. und 18./19.12. mit «Vorschau · Termine und Zahlung sind nur simuliert». Das passt für die Demo und ist gekennzeichnet; vor dem echten Betrieb gehören hier die echten Termine hinein.
5. **Impressum:** Anbieter, Kontakt und Verantwortlicher sind Entwurf. Robert hat entschieden: «Impressum so lassen: Entwurf, Angaben werden vor dem Start eingetragen.» Das ist kein Fund.

## Reparaturen

Keine. An `website/` ist nichts geändert, es gibt keine Sicherung `*.vor-democheck-2026-10-28`.

## Werkzeuge

`~/…/scratchpad/dc/lauf.js` (Seitenaufrufe, Bilder), `bedienen.js` (Wege), `drossel.js` (Ladezeit, Flüssigkeit), Ergebnisse `ergebnis-*.json`, `bed2.log`, `drossel.log`. Das sind Arbeitsdateien des Prüfchats.
