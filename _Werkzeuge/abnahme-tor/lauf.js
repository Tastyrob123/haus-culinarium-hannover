#!/usr/bin/env node
// Abnahme-Tor über alle Werkzeuge eines Hauses: Inventar + Messung WebKit 1440×900, höchstens N Werkzeuge gleichzeitig
// (damit die Werkzeug-Server nicht stocken), danach Stichproben 1280×800, 1000×650 (Roberts Safari) und 390×844.
// Aufruf: node lauf.js <ziele.json> <ausgabe-ordner> [--parallel 5] [k1 k2 …]
const { spawn } = require('child_process'), fs = require('fs'), path = require('path');
const [ZIELE, AUS, ...rest] = process.argv.slice(2);
const pi = rest.indexOf('--parallel'); const P = pi >= 0 ? +rest.splice(pi, 2)[1] : 5;
const KS = rest.length ? rest : JSON.parse(fs.readFileSync(ZIELE, 'utf8')).ziele.map(z => z.k);
fs.mkdirSync(AUS, { recursive: true });
const runde = extra => new Promise(fertig => { const offen = [...KS]; let laufen = 0;
  const weiter = () => { if (!offen.length && !laufen) return fertig();
    while (laufen < P && offen.length) { const k = offen.shift(); laufen++;
      const log = fs.openSync(path.join(AUS, k + '.log'), 'a');
      spawn('node', [path.join(__dirname, 'tor.js'), ZIELE, AUS, '--nur', k, ...extra], { stdio: ['ignore', log, log] }).on('exit', () => { laufen--; weiter(); }); } };
  weiter(); });
// Danach der Messlauf (Pflicht vor jeder Übergabe, Oberchef 29.10.2026): Chromium + WebKit, 1440/1280/390, Tafel unter <ausgabe>/messlauf
let haus = path.basename(ZIELE).replace(/^ziele-|\.json$/g, '').replace(/-alt$/, '');
while (haus.includes('-') && !fs.existsSync(path.join(__dirname, '..', 'messlauf', 'ziele-' + haus + '.json'))) haus = haus.replace(/-[^-]*$/, '');   // Teil-Ziellisten (z. B. -wb-tresen) messen mit der Zielliste des Hauses
const messlauf = () => new Promise(f => { const log = fs.openSync(path.join(AUS, 'messlauf.log'), 'a');
  spawn('zsh', [path.join(__dirname, '..', 'messlauf', 'messlauf.sh'), haus, path.join(AUS, 'messlauf'), '--nur', KS.join(',')], { stdio: ['ignore', log, log] }).on('exit', f); });
(async () => { await runde([]); for (const g of (process.env.TOR_GROESSEN || '1280x800,1000x650,390x844').split(',')) await runde(['--stichprobe', g, ...(g === '390x844' && process.env.TOR_HANDY_ALLE ? ['--jede', '1', '--stichmax', '400'] : [])]); await messlauf(); console.log('LAUF FERTIG', new Date().toTimeString().slice(0, 5)); })();
