# Übergabe: Kunden-Demos online (Stand 1.11.2026, ca. 07:45 UTC)

## Was Robert will
Der Kunde bekommt **einen Link** zur Werkbank. Darüber öffnet er alle sieben Werkzeuge als **Demo mit Beispielwerten**: keine Anmeldung, keine Freigaben, keine Wirkung auf die echte Website. Das gilt für **beide Häuser**, Walk on the Wild Side und Culinarium. Gehostet wird **auf Vercel, wie immer**, nicht auf GitHub Pages und nicht als claude.ai-Artifact. Keine Rückfragen, keine Technik-Erklärungen an Robert.
- E-Mail: robertreff0@gmail.com = robert@tasty-studios.de, ein Postfach.

## Stand
- Beide Häuser sind fertig gebaut, jeweils als **eine statische Seite** im Zweig `demo-seite`:
  - `Tastyrob123/haus-wildside`: Website im Wurzelordner, Werkbank unter `/werkbank/`, Demos unter `/werkzeuge/<werkzeug>/`. Alle Links zeigen auf `https://wildside-hannover-entwurf.vercel.app`.
  - `Tastyrob123/haus-culinarium-hannover`: gebaut für GitHub Pages. Die Basisadresse `https://tastyrob123.github.io/haus-culinarium-hannover` muss vor dem Hochladen auf `https://culinarium-hannover-demo.vercel.app` umgestellt werden.
- Das Hochladen läuft in der Cloud-Sitzung «Wild Side: Kunden-Demo auf Vercel hochladen», Umgebung «Vercel», im Account robert@tasty-studios.de. Ihr Ergebnis steht in deren Verlauf.
- Die eingefrorene Live-Seite `culinarium-hannover-entwurf.vercel.app` **nicht anfassen**.

## Falls neu hochladen nötig (Mac mit Vercel-CLI oder Cloud-Umgebung mit Netz und `VERCEL_TOKEN`)
```
git clone --depth 1 -b demo-seite https://github.com/Tastyrob123/haus-wildside /tmp/wildside-hannover-entwurf
rm -rf /tmp/wildside-hannover-entwurf/.git
cd /tmp/wildside-hannover-entwurf && npx --yes vercel@latest deploy --prod --yes --name wildside-hannover-entwurf
```
Culinarium: genauso mit `-b demo-seite https://github.com/Tastyrob123/haus-culinarium-hannover`, vorher die Basisadresse ersetzen, Projektname `culinarium-hannover-demo`.
Danach:
- Ist die Seite hinter einer Vercel-Anmeldung? Dann im Projekt unter Settings → Deployment Protection «Vercel Authentication» ausschalten.
- Prüfen: `/werkbank/index.html` und `/werkzeuge/imprimerie/` antworten ohne Anmeldung mit 200.

## Wie die Demos gebaut werden
`cloud/demo/` in beiden Repos, siehe `LIESMICH.md`.
- **Aufnahme-Proxy:** zeichnet die echten Server-Antworten der Werkzeuge auf.
- **`bau.py`:** baut daraus einen statischen Ordner.
- **`shim.js`:** beantwortet Server-Anfragen mit den Beispielwerten. Speichern sagt «geklappt», ändert aber nichts.
- **`werkbank.py`:** baut die Werkbank.

Ein neuer Bau ist nötig, sobald ein Werkzeug geändert wird.

## Sonst offen
- Vercel-Schlüssel «wildside» nach dem Hochladen löschen: https://vercel.com/account/settings/tokens. Er stand im Chat.
- Wild Side, letzte Prüfung: Plakatwerkstatt-Kacheln wurden auf gleiche Höhe korrigiert. Die Nachprüfung dazu ist `[schnell: plakatwerkstatt-mail]` auf main, Ergebnis im Zweig `ergebnis`.
