/* pdf.js · druckt eine Karte als PDF. Aufgerufen von api.py, nie direkt vom Browser.
     Eingabe (stdin, JSON):  { karte, welt, haus, allergene, zeichen (Zeichnung des Hauses), zeichen_mass, tapete (Adresse) }
     Ausgabe (stdout, JSON): { pdf (base64), seiten, regeln: [...], ueberlauf: [...] }  oder  { fehler }
   Gedruckt wird druck.html mit satz.js und satz.css: genau die Seite, die im Werkzeug als Vorschau steht.
   Der Browser läuft unsichtbar, lädt nichts von aussen (die wenigen Dateien kommen von der Platte, die Daten aus der Eingabe)
   und schreibt keine Datei. Er wird nach dem Druck wieder beendet. */
const fs = require('fs'), path = require('path'), os = require('os');
const WURZEL = path.resolve(__dirname, '..', '..');
const ERLAUBT = [/^\/stamm\/welt\.css$/, /^\/stamm\/schriften\/[A-Za-z0-9_.-]+\.woff2$/, /^\/werkzeuge\/karten\/(druck\.html|satz\.css|satz\.js)$/, /^\/werkzeuge\/karten\/kleid\/[a-z0-9-]+\/[A-Za-z0-9_-]+\.webp$/];
const ART = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.woff2': 'font/woff2', '.webp': 'image/webp' };

function finde() {
  const npx = path.join(os.homedir(), '.npm/_npx');
  for (const d of fs.existsSync(npx) ? fs.readdirSync(npx) : []) {
    const p = path.join(npx, d, 'node_modules/playwright');
    if (fs.existsSync(p)) return p;
  }
  throw new Error('Playwright nicht gefunden (einmal: npx -y playwright --version)');
}
function shell() {
  const c = path.join(os.homedir(), 'Library/Caches/ms-playwright');
  if (!fs.existsSync(c)) return undefined;
  for (const n of fs.readdirSync(c).filter(n => n.startsWith('chromium_headless_shell-')).sort().reverse()) {
    const p = path.join(c, n, 'chrome-headless-shell-mac-arm64/chrome-headless-shell');
    if (fs.existsSync(p)) return p;
  }
  return undefined;
}

(async () => {
  let b;
  try {
    const ein = JSON.parse(fs.readFileSync(0, 'utf8'));
    const { chromium } = require(finde());
    b = await chromium.launch({ headless: true, executablePath: shell() });
    const p = await b.newPage({ viewport: { width: 1300, height: 1400 } });
    const fehler = [];
    p.on('pageerror', e => fehler.push(String(e)));
    await p.route('**/*', route => {
      const u = new URL(route.request().url());
      if (u.hostname !== 'karten.lokal' || !ERLAUBT.some(r => r.test(u.pathname))) return route.abort();
      const datei = path.join(WURZEL, u.pathname);
      return route.fulfill({ status: 200, contentType: ART[path.extname(datei)] || 'application/octet-stream', body: fs.readFileSync(datei) });
    });
    await p.goto('http://karten.lokal/werkzeuge/karten/druck.html', { waitUntil: 'load', timeout: 30000 });
    const r = await p.evaluate(e => window.KT_DRUCK.zeige(e.karte, { welt: e.welt, haus: e.haus, allergene: e.allergene, zeichen: e.zeichen, zeichenMass: e.zeichen_mass, tapete: e.tapete }), ein);
    if (fehler.length) throw new Error('Satz: ' + fehler.join(' · ').slice(0, 300));
    await p.emulateMedia({ media: 'print' });
    const f = ein.karte.format || [210, 297];
    const pdf = await p.pdf({ width: f[0] + 'mm', height: f[1] + 'mm', preferCSSPageSize: true, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    process.stdout.write(JSON.stringify({ pdf: pdf.toString('base64'), seiten: r.seiten, regeln: r.regeln, ueberlauf: r.ueberlauf }));
  } catch (e) {
    process.stdout.write(JSON.stringify({ fehler: String(e && e.message || e).slice(0, 500) }));
    process.exitCode = 1;
  } finally {
    if (b) await b.close();
  }
})();
