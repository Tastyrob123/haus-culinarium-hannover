// Probe: jedes Ziel einmal öffnen, Bild, Konsolenfehler, fehlgeschlagene Anfragen. node cloud/probe.js <ziele.json> <aus>
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright'), fs = require('fs'), path = require('path');
const [Z, A] = process.argv.slice(2); fs.mkdirSync(A, { recursive: true });
let ziele = JSON.parse(fs.readFileSync(Z, 'utf8')); ziele = ziele.ziele || ziele;
(async () => { const b = await pw.webkit.launch(); const aus = [];
  for (const z of ziele) { const c = await b.newContext({ viewport: { width: 1440, height: 900 } }); const p = await c.newPage(); const f = [];
    p.on('console', m => m.type() === 'error' && f.push('konsole: ' + m.text().slice(0, 200))); p.on('pageerror', e => f.push('fehler: ' + String(e).slice(0, 200)));
    p.on('response', r => r.status() >= 400 && f.push(r.status() + ' ' + r.url().slice(0, 160))); p.on('requestfailed', r => f.push('weg ' + r.url().slice(0, 160)));
    await p.goto(z.url, { waitUntil: 'load', timeout: 30000 }).catch(e => f.push('goto ' + e.message.slice(0, 100))); await p.waitForTimeout(2500);
    const t = await p.evaluate(() => ({ titel: document.title, text: document.body.innerText.slice(0, 200), knoepfe: document.querySelectorAll('button,a').length })).catch(() => ({}));
    await p.screenshot({ path: path.join(A, z.k + '.jpg'), type: 'jpeg', quality: 60 }); aus.push({ k: z.k, ...t, f: f.slice(0, 12) }); console.log(z.k, t.knoepfe, f.length, f.slice(0, 3).join(' | ')); await c.close(); }
  fs.writeFileSync(path.join(A, 'probe.json'), JSON.stringify(aus, null, 1)); await b.close(); })();
