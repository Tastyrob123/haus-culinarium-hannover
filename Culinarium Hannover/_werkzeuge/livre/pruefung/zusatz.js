// Le Livre · Culinarium Hannover (Vorlage: zusatz.js der Taverne zum Schäfli, dort nur gelesen) · alles, was bedienen.js nicht bedient (FUNKTIONEN.md Zeilen 71–83 und 87–88): Rahmen R02/R03/R04/R15/R17/R18/R19,
// Vorher/Nachher bei allen nachgeschärften Fotos (auch Firefox), ungewöhnliche Eingaben, Netz weg, zwei Fenster, 320 und 390 px, Markenbuch und sein Druck.
//   BASIS=http://127.0.0.1:9085/ FEHLERLOG=<_werkzeuge/livre/_qa/fehler.jsonl der Probe-Kopie> node _werkzeuge/livre/pruefung/zusatz.js chromium|webkit|firefox
// Vorlage: Doldenhorn und Carlton _werkzeuge/livre/pruefung/zusatz.js. Testdateien entstehen in pruefung/_proben/ (geht nie online).
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const pw = require(path.join(process.env.HOME, 'Aussen-Pruefung/node_modules/playwright'));
const BASIS = process.env.BASIS || 'http://127.0.0.1:9085/', URL0 = BASIS + '_werkzeuge/livre/';
const motor = process.argv[2] || 'chromium';
const HIER = __dirname, PROBEN = path.join(HIER, '_proben'), BELEG = path.join(HIER, 'belege', 'zusatz-' + motor);
fs.mkdirSync(PROBEN, { recursive: true }); fs.mkdirSync(BELEG, { recursive: true }); fs.mkdirSync(path.join(HIER, 'ergebnisse'), { recursive: true });
const erg = []; const Z = (nr, t, ok, m = '') => { erg.push({ nr, t, ok: !!ok, m: String(m).slice(0, 240) }); console.log((ok ? '✓' : '✗') + ' ' + String(nr).padStart(2) + ' ' + t + (m !== '' ? ' · ' + String(m).slice(0, 160) : '')); };
const zeilen = () => process.env.FEHLERLOG && fs.existsSync(process.env.FEHLERLOG) ? fs.readFileSync(process.env.FEHLERLOG, 'utf8').split('\n').filter(Boolean).length : 0;

function proben() {   // Testdateien einmal erzeugen: über 30 MB, knapp unter 30 MB, 400 px, 13'000 × 13'000 (169 MP), PDF mit drei Seiten, «Bild» ohne Bild
  const py = `
import os, sys
from PIL import Image
P = sys.argv[1]
da = lambda n: os.path.exists(os.path.join(P, n))
if not da('klein-400.png'): Image.new('RGB', (400, 300), (13, 22, 33)).save(os.path.join(P, 'klein-400.png'))
if not da('riesig-169mp.png'): Image.new('RGB', (13000, 13000), (241, 236, 226)).save(os.path.join(P, 'riesig-169mp.png'), optimize=True)
if not da('gross-29mb.jpg') or not da('gross-31mb.jpg'):
    im = Image.frombytes('RGB', (2600, 2600), os.urandom(2600 * 2600 * 3))
    im.save(os.path.join(P, 'gross-29mb.jpg'), quality=100, subsampling=0)
    with open(os.path.join(P, 'gross-31mb.jpg'), 'wb') as f:
        f.write(open(os.path.join(P, 'gross-29mb.jpg'), 'rb').read() + b'\\0' * (31 * 1024 * 1024 - os.path.getsize(os.path.join(P, 'gross-29mb.jpg'))))
if not da('drei-seiten.pdf'):
    s = [Image.new('RGB', (595, 842), c) for c in ((241, 236, 226), (13, 22, 33), (227, 210, 166))]
    s[0].save(os.path.join(P, 'drei-seiten.pdf'), save_all=True, append_images=s[1:])
open(os.path.join(P, 'kein-bild.png'), 'wb').write(b'Das ist Text, kein Bild. <script>alert(1)</script>')
print(' '.join(f'{n}={os.path.getsize(os.path.join(P, n))}' for n in sorted(os.listdir(P))))`;
  return execFileSync('python3', ['-c', py, PROBEN], { encoding: 'utf8' }).trim();
}

(async () => {
  console.log('Proben:', proben());
  const b = await pw[motor].launch();
  const neu = async (opt = {}) => {
    const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true, ...opt });
    await ctx.addInitScript(() => { try { if (!sessionStorage.getItem('mit-schild')) localStorage.setItem('rundgang-culinarium-livre', '1'); } catch (e) {} });
    const p = await ctx.newPage(); p.fehler = [];
    p.on('pageerror', e => p.fehler.push('JS ' + e.message)); p.on('dialog', d => { p.fehler.push('DIALOG ' + d.message()); d.dismiss(); });
    return [ctx, p];
  };
  const warte = (p, ms) => p.waitForTimeout(ms);
  const n = (p, s) => p.locator(s).count();
  const text = async (p, s) => (await p.locator(s).first().innerText().catch(() => '')).replace(/\s+/g, ' ').trim();
  const meldung = async p => (await p.locator('#meldung .quit').allInnerTexts().catch(() => [])).join(' | ');
  const klickKachel = async (p, loc) => { await loc.evaluate(e => e.scrollIntoView({ block: 'center' })); await warte(p, 250); await loc.click(); };

  // ---- 71 R15 Ladezeichen erst nach 280 ms · 72 R02 Auftakt
  {
    const [ctx, p] = await neu();
    await p.route('**/_werkzeuge/livre/livre.json*', async r => { await new Promise(x => setTimeout(x, 1600)); r.continue(); });
    p.goto(URL0 + '#start').catch(() => {});
    await p.waitForSelector('#ansicht', { state: 'attached', timeout: 10000 });
    const t0 = await p.evaluate(() => performance.now());
    await warte(p, Math.max(0, 150 - t0));
    const frueh = await p.evaluate(() => [performance.now() | 0, !!document.querySelector('#ansicht .lade')]);
    await warte(p, 500);
    const spaet = await p.evaluate(() => [performance.now() | 0, !!document.querySelector('#ansicht .lade')]);
    Z(71, 'R15 Ladezeichen erst nach 280 ms', !frueh[1] && spaet[1], `bei ${frueh[0]} ms ${frueh[1] ? 'da' : 'nicht da'}, bei ${spaet[0]} ms ${spaet[1] ? 'da' : 'nicht da'}`);
    await p.waitForSelector('#ansicht .wo-sb', { timeout: 20000 });
    const zustand = await p.evaluate(() => ({ schrift: document.fonts.status, kopf: !!document.querySelector('#kopf .wo-kopf__mitte'), rand: !!document.querySelector('#rand [data-gehe]'), leiste: !!(document.querySelector('#leiste') || {}).textContent, bereit: !!window.LIVRE_BEREIT }));
    Z(72, 'R02 Auftakt: Kopf, Rand, Ansicht kommen zusammen, Schriften geladen', zustand.schrift === 'loaded' && zustand.kopf && zustand.rand && zustand.leiste && zustand.bereit, JSON.stringify(zustand));
    await ctx.close();
  }
  // ---- 73 R04 Startfehler-Tür
  {
    const [ctx, p] = await neu();
    await p.route('**/_werkzeuge/livre/livre.json*', r => r.fulfill({ status: 404, body: 'weg' }));
    await p.goto(URL0 + '#start'); await warte(p, 3000);
    const tuer = await text(p, '.li-tuer');
    const a = /startet nicht/.test(tuer) && /404/.test(tuer) && (await n(p, '.li-tuer [data-neu]')) === 1 && (await n(p, '.li-tuer a[href="anleitung.html"]')) === 1;
    await p.screenshot({ path: path.join(BELEG, 'r04-startfehler.jpg'), type: 'jpeg', quality: 70 });
    await p.unroute('**/_werkzeuge/livre/livre.json*'); await p.locator('.li-tuer [data-neu]').click(); await p.waitForSelector('#ansicht .wo-sb', { timeout: 20000 });
    const c = (await n(p, '#ansicht .wo-ag')) === 4;
    await ctx.close();
    const [ctx2, p2] = await neu();
    await p2.route('**/livre.js*', r => r.abort());
    await p2.goto(URL0); await warte(p2, 12800);
    const satz = await text(p2, '.li-tuer');
    Z(73, 'R04 Startfehler-Tür: Satz mit Namen (kein Platzhalter), Grund, «Neu laden», Anleitung; «Neu laden» startet; ohne Skript nach 12 s ein Satz', a && c && !/[{}]/.test(tuer) && /startet nicht/.test(satz), `${tuer.slice(0, 70)} | ${satz.slice(0, 60)}`);
    await ctx2.close();
  }
  // ---- 74 R03 Fehlermelder
  {
    const [ctx, p] = await neu();
    await p.goto(URL0 + '#start'); await p.waitForSelector('#ansicht .wo-ag'); await warte(p, 800);
    const vorher = zeilen();
    await p.evaluate(() => { for (let i = 0; i < 25; i++) setTimeout(() => { throw new Error('Probefehler ' + i + ' <b>x</b>'); }, i * 5); });
    await warte(p, 2000);
    const lokal = await p.evaluate(() => JSON.parse(localStorage.getItem('cu-livre-fehler') || '[]'));
    const nachher = zeilen();
    await p.route('**/_werkzeuge/livre/dateien/**', r => r.abort()); await p.evaluate(() => { location.hash = '#dateien'; }); await warte(p, 1500);
    const nach2 = zeilen();
    Z(74, 'R03 Fehlermelder: gemerkt (höchstens 20), an api/fehler (höchstens 20, F34 keiner verloren), Netzfehler nicht', lokal.length === 20 && /Probefehler/.test(lokal[0].text) && nachher - vorher === 20 && nach2 === nachher, `${lokal.length} im Browser, ${nachher - vorher} im Protokoll, Netzfehler ${nach2 - nachher}`);
    await ctx.close();
  }
  // ---- 75 R18 Rundgang · 76 R19 Zur Werkbank · 77 R17 weniger Bewegung
  {
    const [ctx, p] = await neu();
    await p.goto(URL0 + '#start'); await p.waitForSelector('#ansicht .wo-ag'); await warte(p, 4000);
    const kein = (await n(p, '.rdg-schild')) === 0 && (await n(p, '.rdg-kegel')) === 0, imRand = (await n(p, '#rand .wo-rand__wege .rdg-wieder')) === 1;
    await p.evaluate(() => { location.hash = '#bilder'; }); await warte(p, 1200);
    const nachWechsel = (await n(p, '#rand .wo-rand__wege .rdg-wieder')) === 1;
    await p.goto(URL0 + '?rundgang#start'); await p.waitForSelector('.rdg-kegel', { state: 'attached', timeout: 30000 }); await warte(p, 900);
    const schritte = [];
    for (let i = 0; i < 6; i++) {
      const k = await text(p, '.rdg-karte'); if (!k) break; schritte.push(k.replace(/Weiter|Los geht’s|Überspringen|Schliessen/g, '').slice(0, 60));
      await p.screenshot({ path: path.join(BELEG, `r18-rundgang-${i + 1}.jpg`), type: 'jpeg', quality: 70 });
      await p.locator('.rdg-karte .rdg-los').click(); await warte(p, 900);
    }
    Z(75, 'R18 Rundgang: Prüfbrowser ohne Schild, Weg im Rand (bleibt nach Wechsel), ?rundgang mit vier Schritten, was und wozu', kein && imRand && nachWechsel && schritte.length === 4 && (await n(p, '.rdg-kegel')) === 0 && schritte.every(s => !/klicken Sie|drücken Sie|tippen Sie/i.test(s)), schritte.join(' / ').slice(0, 200));
    const ohneWb = (await n(p, '#zur-werkbank, zur-werkbank, [data-zur-werkbank]')) === 0;
    await p.goto(URL0 + '?wb=de.werkzeuge&wbo=' + encodeURIComponent('http://127.0.0.1:9088') + '#start'); /* wie aus der Werkbank (:9088) geöffnet, Fehlerbuch 10a 21.10.: Herkunft wbo */ await p.waitForSelector('#ansicht .wo-ag'); await warte(p, 2500);
    const zw = await p.evaluate(() => { const el = [...document.querySelectorAll('body > *')].find(x => x.shadowRoot && /Werkbank/.test(x.shadowRoot.textContent)); if (!el) return null; const a = el.shadowRoot.querySelector('a'); return a ? [a.textContent.trim(), a.getAttribute('href')] : 'ohne Link'; });
    await p.screenshot({ path: path.join(BELEG, 'r19-zur-werkbank.jpg'), type: 'jpeg', quality: 70 });
    await p.evaluate(() => { location.hash = '#bilder'; }); await warte(p, 1200);
    const bleibt = await p.evaluate(() => !![...document.querySelectorAll('body > *')].find(x => x.shadowRoot && /Werkbank/.test(x.shadowRoot.textContent)));
    Z(76, 'R19 «Zur Werkbank» nur aus der Werkbank geöffnet, bleibt über weitere Klicks', ohneWb && zw && /Werkbank/.test(zw[0]) && /^http:\/\/127\.0\.0\.1:9088\/werkbank\/index\.html/.test(zw[1]) && bleibt, JSON.stringify(zw));
    await ctx.close();
    const [ctx2, p2] = await neu({ reducedMotion: 'reduce' });
    await p2.goto(URL0 + '#start'); await p2.waitForSelector('#ansicht .wo-ag'); await warte(p2, 300);
    const offen = await p2.evaluate(() => [...document.querySelectorAll('#ansicht [data-r]')].filter(x => !x.classList.contains('da')).length);
    const bewegt = await p2.evaluate(() => [...document.querySelectorAll('#ansicht *')].filter(x => getComputedStyle(x).animationName !== 'none' && !x.classList.contains('lade__r')).length);
    Z(77, 'R17 «Weniger Bewegung»: alles steht sofort', offen === 0 && bewegt === 0, `${offen} warten, ${bewegt} bewegen sich`);
    await ctx2.close();
  }
  // ---- 78 L09 Vorher/Nachher bei allen nachgeschärften Fotos
  {
    const [ctx, p] = await neu();
    await p.goto(URL0 + '#bilder'); await p.waitForSelector('#li-raster .li-f');
    const LJ = await p.evaluate(async () => (await fetch('livre.json')).json());
    const L = LJ.fotos.filter(f => f.vn).map(f => f.k);
    for (let i = 0; i < 4; i++) { await p.evaluate(() => scrollTo(0, document.body.scrollHeight)); await warte(p, 900); }
    let gut = 0, schieber = null; const schlecht = [];
    for (const k of L) {
      const kach = p.locator(`#li-raster .li-f[data-k="${k}"]`); if (!(await kach.count())) { schlecht.push(k + ' nicht im Raster'); continue; }
      await klickKachel(p, kach); await p.waitForSelector('#fenster:not([hidden]) .li-det');
      await p.waitForFunction(() => { const i = document.querySelector('.li-vn__v'); return i && i.complete && i.naturalWidth; }, null, { timeout: 15000 }).catch(() => {});
      const r = await p.evaluate(async () => {
        const v = document.querySelector('#li-bild'), o = document.querySelector('.li-vn__v'), nach = v.querySelector('img:not(.li-vn__v)');
        const k = [...document.querySelectorAll('[data-vn]')].map(b => b.dataset.vn).join(',');
        const vor = getComputedStyle(o).opacity;
        document.querySelector('[data-vn="vorher"]').click(); for (let i = 0; i < 30 && +getComputedStyle(o).opacity < .99; i++) await new Promise(r => setTimeout(r, 100));
        const opV = getComputedStyle(o).opacity, rahmenV = getComputedStyle(document.querySelector('#li-rahmen')).display;
        document.querySelector('[data-vn="schieber"]').click(); await new Promise(r => setTimeout(r, 120)); const clip = getComputedStyle(o).clipPath;
        document.querySelector('[data-vn="nachher"]').click(); for (let i = 0; i < 30 && +getComputedStyle(o).opacity > .01; i++) await new Promise(r => setTimeout(r, 100)); const opN = getComputedStyle(o).opacity;
        const orig = document.querySelector('.li-orig a'); const st = orig ? (await fetch(orig.href)).status : 0;
        return { k, vor, opV, rahmenV, clip, opN, o: [o.naturalWidth, o.naturalHeight], n: [nach.naturalWidth, nach.naturalHeight], st };
      });
      const masse = r.o[0] === r.n[0] && r.o[1] === r.n[1];
      if (r.k === 'vorher,nachher,schieber' && +r.vor < .05 && +r.opV > .95 && r.rahmenV === 'none' && /inset/.test(r.clip) && +r.opN < .05 && r.st === 200 && masse) gut++; else schlecht.push(k + ' ' + JSON.stringify(r).slice(0, 160));
      if (!schieber) {   // Schieber mit der Maus ziehen (F32: auch in Firefox)
        await p.locator('[data-vn="schieber"]').click(); const bb = await p.locator('#li-bild').boundingBox();
        await p.mouse.move(bb.x + bb.width * .5, bb.y + bb.height * .4); await p.mouse.down(); await p.mouse.move(bb.x + bb.width * .22, bb.y + bb.height * .4, { steps: 8 }); await p.mouse.up(); await warte(p, 200);
        schieber = await p.evaluate(() => document.querySelector('#li-bild').style.getPropertyValue('--p'));
        await p.screenshot({ path: path.join(BELEG, 'vorher-nachher-schieber.jpg'), type: 'jpeg', quality: 70 });
      }
      await p.keyboard.press('Escape'); await warte(p, 250);
    }
    const ohne = LJ.fotos.find(f => !f.vn); const k2 = p.locator(`#li-raster .li-f[data-k="${ohne.k}"]`); await klickKachel(p, k2); await p.waitForSelector('#fenster:not([hidden]) .li-det');
    const keine = (await n(p, '[data-vn]')) === 0; await p.keyboard.press('Escape');
    const pz = parseFloat(schieber || '50');
    Z(78, `L09 Vorher/Nachher bei allen ${L.length} nachgeschärften Fotos (Knöpfe, Original, Schieber folgt der Maus, gleicher Ausschnitt); ohne Nachschärfung keine Knöpfe`, schlecht.length === 0 && gut === L.length && pz > 15 && pz < 35 && keine, (schlecht.slice(0, 2).join(' | ') || gut + ' von ' + L.length) + ` · Schieber ${schieber}`);
    await ctx.close();
  }
  // ---- 79 Suche mit ungewöhnlichen Eingaben
  {
    const [ctx, p] = await neu();
    await p.goto(URL0 + '#bilder'); await p.waitForSelector('#li-raster .li-f'); await warte(p, 900);
    const suche = async q => { await p.locator('#li-q').fill(q); await warte(p, 700); return [await n(p, '#li-raster .li-f'), await n(p, '#li-raster .li-leer'), (await p.locator('#li-q').inputValue()).length]; };
    const r1 = await suche('Linden '.repeat(715).slice(0, 5000));
    const r2 = await suche('<script>alert(1)</script><img src=x onerror=alert(2)>'); const r2b = (await n(p, '#li-raster img[src="x"]')) === 0;
    const r3 = await suche('🍸🕯️');
    const r4 = await suche('Gläser'), r5 = await suche('gläser'), r6 = await suche('GLÄSER');
    const r7 = await suche('   ');
    Z(79, 'Suche mit 5’000 Zeichen, <script>, Emoji, Umlauten (gross/klein gleich), nur Leerzeichen', r1[1] === 1 && r2b && r3[1] === 1 && r4[0] > 0 && r4[0] === r5[0] && r5[0] === r6[0] && r7[0] === 48 && p.fehler.length === 0, `${r1[2]} Zeichen · Gläser ${r4[0]}/${r5[0]}/${r6[0]} · Leer ${r7[0]} · ${p.fehler.join('|')}`);
    await ctx.close();
  }
  // ---- 80 L10 Prüfung mit ungewöhnlichen Dateien · 81 Netz weg
  {
    const [ctx, p] = await neu();
    await p.goto(URL0 + '#pruefung'); await p.waitForSelector('#li-waehle'); await warte(p, 900);
    const waehle = async datei => { await p.locator('#li-datei').setInputFiles(path.join(PROBEN, datei)); await warte(p, 1600); };
    const pruefe = async () => { await p.locator('#li-los').click(); await p.waitForFunction(() => { const e = document.querySelector('#li-pr'); return e && !e.querySelector('.li-lauf'); }, null, { timeout: 120000 }); await warte(p, 900); return { erg: await n(p, '#li-pr .li-erg'), feld: await n(p, '#li-los'), melde: await meldung(p) }; };
    const zuruck = async () => { if (await n(p, '#li-pr [data-neu]')) { await p.locator('#li-pr [data-neu]').click(); await warte(p, 600); } await p.evaluate(() => document.querySelectorAll('#meldung .quit').forEach(q => q.remove())); };
    const r = {};
    await waehle('gross-31mb.jpg'); r.zuGross = (await n(p, '#li-los')) === 0 && /30 MB/.test(await meldung(p)); await zuruck();
    await waehle('gross-29mb.jpg'); r.knapp = (await pruefe()).erg === 1; await p.screenshot({ path: path.join(BELEG, 'pruefung-29mb.jpg'), type: 'jpeg', quality: 70 }); await zuruck();
    await waehle('klein-400.png'); r.klein = (await pruefe()).erg === 1 && /nächste Farbe der Marke/i.test(await text(p, '#li-pr')); await zuruck();
    await waehle('riesig-169mp.png'); const rr = await pruefe(); r.riesig = rr.erg === 1 || (rr.feld === 1 && /zu gross|Megapixel/.test(rr.melde)); await zuruck();
    await waehle('kein-bild.png'); const rk = await pruefe(); r.keinBild = rk.erg === 0 && rk.feld === 1 && /nicht öffnen|JPG/.test(rk.melde); await zuruck();
    await p.goto(URL0 + '#pruefung'); await p.waitForSelector('#li-waehle'); await warte(p, 600);
    await waehle('drei-seiten.pdf'); const rp = await pruefe(); r.pdf = rp.erg === 1 && /3 Seiten/.test(await text(p, '#li-pr')); await zuruck();
    Z(80, 'L10 Prüfung: über 30 MB abgewiesen, knapp 30 MB und 169 MP verkleinert geprüft, 400 px, «Bild» ohne Bild mit Meldung, PDF mit drei Seiten', Object.values(r).every(Boolean), JSON.stringify(r));
    await p.goto(URL0 + '#pruefung'); await p.waitForSelector('#li-waehle'); await waehle('klein-400.png');
    await ctx.setOffline(true); await p.locator('#li-los').click(); await warte(p, 2500);
    const m = await meldung(p); const bleibt = (await n(p, '#li-los')) === 1 && (await text(p, '.li-feld__name')).includes('klein-400');
    await ctx.setOffline(false); await warte(p, 500); const wieder = (await pruefe()).erg === 1;
    Z(81, 'Netz weg beim Prüfen: Meldung, Datei bleibt; Netz zurück: prüfen geht', /Verbindung|antwortet nicht/i.test(m) && bleibt && wieder && p.fehler.length === 0, m.slice(0, 100));
    await ctx.close();
  }
  // ---- 82 Zwei Fenster gleichzeitig
  {
    const [ctx, p] = await neu(); const p2 = await ctx.newPage();
    await Promise.all([p.goto(URL0 + '#pruefung'), p2.goto(URL0 + '#pruefung')]); await Promise.all([p.waitForSelector('#li-waehle'), p2.waitForSelector('#li-waehle')]);
    await p.locator('#li-datei').setInputFiles(path.join(PROBEN, 'klein-400.png')); await p2.locator('#li-datei').setInputFiles(path.join(PROBEN, 'drei-seiten.pdf')); await warte(p, 1000);
    await Promise.all([p.locator('#li-los').click(), p2.locator('#li-los').click()]);
    await Promise.all([p, p2].map(x => x.waitForFunction(() => { const e = document.querySelector('#li-pr'); return e && !e.querySelector('.li-lauf'); }, null, { timeout: 120000 })));
    const a = await text(p, '#li-pr .li-erg__bild'), c = await text(p2, '#li-pr .li-erg__bild');
    Z(82, 'Zwei Fenster prüfen gleichzeitig, je eigene Rückmeldung', /klein-400/.test(a) && /drei-seiten/.test(c) && /3 Seiten/.test(c), `${a.slice(0, 30)} | ${c.slice(0, 40)}`);
    await ctx.close();
  }
  // ---- 83 320 und 390 px, alle Ansichten ohne seitliches Verrutschen (Markenbuch und Anleitung dazu)
  {
    const mass = [];
    for (const w of [320, 390]) {
      const [ctx, p] = await neu({ viewport: { width: w, height: 760 }, hasTouch: motor !== 'firefox', isMobile: motor === 'chromium' });
      for (const a of ['#start', '#bilder', '#dateien', '#pruefung', '?beispiel=1#pruefung']) {
        await p.goto('about:blank'); await p.goto(URL0 + a); await p.waitForSelector('#ansicht .wo-sb', { timeout: 20000 }); await warte(p, 1200);
        for (let i = 0; i < 3; i++) { await p.evaluate(() => scrollBy(0, innerHeight)); await warte(p, 300); }
        mass.push(w + a + ':' + await p.evaluate(() => document.documentElement.scrollWidth - innerWidth));
        if (w === 320) await p.screenshot({ path: path.join(BELEG, `320-${a.replace(/\W+/g, '')}.jpg`), type: 'jpeg', quality: 70 });
      }
      await p.goto(URL0 + '#bilder'); await p.waitForSelector('#li-raster .li-f'); await klickKachel(p, p.locator('#li-raster .li-f[data-k="pass4"]')); await warte(p, 900);
      mass.push(w + '-fenster:' + await p.evaluate(() => { const k = document.querySelector('#fenster .fenster__k').getBoundingClientRect(); return Math.max(0, Math.round(k.right - innerWidth), Math.round(-k.left)); }));
      for (const s of ['buch.html', 'anleitung.html']) { await p.goto(URL0 + s); await warte(p, 1500); mass.push(w + s + ':' + await p.evaluate(() => document.documentElement.scrollWidth - innerWidth)); }
      await ctx.close();
    }
    const schlecht = mass.filter(x => +x.split(':').pop() > 1);
    Z(83, '320 und 390 px: alle Ansichten, Foto-Fenster, Markenbuch und Anleitung ohne seitliches Verrutschen', schlecht.length === 0, schlecht.join(' ') || mass.length + ' Messungen');
  }
  // ---- 87 L05 Markenbuch · 88 Markenbuch im Druck
  {
    const [ctx, p] = await neu();
    await p.goto(URL0 + 'buch.html'); await warte(p, 1500);
    const kap = await p.locator('section.blatt').evaluateAll(a => a.map(x => x.id).join(','));
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); } });
    await p.evaluate(async () => { [...document.images].forEach(i => { i.loading = 'eager'; }); await new Promise(r => setTimeout(r, 1500)); });
    const bilder = await p.evaluate(() => [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src));
    const rudi = await p.evaluate(() => document.querySelector('symbol#wortmarke').getAttribute('viewBox'));
    let druck = false; await p.exposeFunction('gedruckt', () => { druck = true; }).catch(() => {});
    await p.evaluate(() => { window.print = () => window.gedruckt(); });
    await p.locator('#bu-pdf').click(); await warte(p, 2600);
    Z(87, 'L05 Markenbuch der Station 05 im Stand der Website: zwölf Blätter (ohne «Farbwelt», Robert 29.10.2026), Rudis Wortmarke, alle Bilder, «Als PDF sichern» öffnet den Druck', kap === 'haltung,zeichen,farben,abende,herkunft,schrift,tapete,bilder,bausteine,logo,welt,mitnehmen' && rudi === '0.00 0.00 364.78 40.36' && !bilder.length && druck, `${kap} · Wortmarke ${rudi}en · ${bilder.length} Bilder fehlen`);
    if (motor === 'chromium') {
      await p.emulateMedia({ media: 'print' }); await warte(p, 400);
      const pdf = path.join(BELEG, 'markenbuch.pdf');
      await p.pdf({ path: pdf, format: 'A4', landscape: true, printBackground: true, preferCSSPageSize: true });
      const seiten = execFileSync('python3', ['-c', `import re,sys;d=open(sys.argv[1],'rb').read();print(len(re.findall(rb'/Type\\s*/Page[^s]', d)))`, pdf], { encoding: 'utf8' }).trim();
      Z(88, 'Markenbuch im Druck: Titel und je Blatt mindestens eine Seite A4 quer, Hintergründe mitgedruckt', +seiten >= 13 && +seiten <= 60, seiten + ' Seiten · ' + Math.round(fs.statSync(pdf).size / 1024) + ' KB');
    }
    await ctx.close();
  }
  await b.close();
  const gut = erg.filter(r => r.ok).length;
  console.log(`\nSumme ${motor}: ${gut}/${erg.length}`);
  fs.writeFileSync(path.join(HIER, 'ergebnisse', `zusatz-${motor}.json`), JSON.stringify(erg, null, 1));
  process.exit(gut === erg.length ? 0 : 1);
})().catch(e => { console.log('ABBRUCH', String(e && e.stack || e).slice(0, 800)); process.exit(2); });
