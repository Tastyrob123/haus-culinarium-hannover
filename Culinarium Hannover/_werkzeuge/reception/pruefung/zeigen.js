// Bilder für den Oberchef und die Werkbank (28.10.2026): 1440 × 900 und 390 × 844, WebKit (Safari-Kern), ohne feste Zeitzone (Fehlerbuch 9: Datum stimmt mit dem Gerät).
// Server mit frischen Wegwerf-Daten (Beispiele), nie die Daten des Werkzeugs: node zeigen.js http://127.0.0.1:9184 <ziel-ordner>
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const SCHUTZ = require('./schutz');
const [, , BASIS = 'http://127.0.0.1:9184', ZIEL = path.join(__dirname, 'zeigen')] = process.argv;
const WZ = BASIS + '/_werkzeuge/reception/', sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  const br = await SCHUTZ.start(pw, 'webkit');
  for (const [W, H] of [[1440, 900], [390, 844]]) {
    const ctx = await SCHUTZ.kontext(br, { viewport: { width: W, height: H }, locale: 'de-DE', deviceScaleFactor: 2 });
    await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-reception', '1'); localStorage.setItem('rundgang-savoir', '1'); } catch (e) { /* */ } });
    const p = await ctx.newPage(); p.setDefaultTimeout(30000);
    const foto = async n => { await sleep(1300); await p.screenshot({ path: path.join(ZIEL, `reception-${W}-${n}.jpg`), type: 'jpeg', quality: 82 }); console.log(W, n); };
    const gehe = async a => { await p.goto('about:blank'); await p.goto(WZ + '#' + a, { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await sleep(1500); };
    await gehe('start'); await foto('1-uebersicht');
    await gehe('eingang'); const k = p.locator('.re-liste .re-a', { hasText: 'Jonas Albers' }).first(); await k.scrollIntoViewIfNeeded(); await k.click({ force: true }); await sleep(900);
    if (W > 700) { await p.evaluate(() => scrollTo(0, document.querySelector('.re-eingang').getBoundingClientRect().top + scrollY - 90)); } await foto('2-eingang');
    await p.evaluate(() => document.querySelector('#brief, .re-post').scrollIntoView({ block: 'start' })); await p.evaluate(() => scrollBy(0, -80)); await foto('3-brief');
    await gehe('gefragt'); await foto('4-gefragt');
    await gehe('wissen'); await foto('5-wissen');
    await gehe('start'); await p.evaluate(() => (document.querySelector('#k-probe') || document.querySelector('#rand [data-probe]')).click()); await p.waitForSelector('.ws-handy');
    await p.click('.probe__fragen [data-frage]'); await p.waitForFunction(() => document.querySelectorAll('#probe-l .ws-bl--haus').length >= 2 && !document.querySelector('.ws-bl--wartet'), null, { timeout: 20000 }); await foto('6-chat');
    await ctx.close();
  }
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
