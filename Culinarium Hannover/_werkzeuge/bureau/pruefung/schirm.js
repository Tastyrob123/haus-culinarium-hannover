/* schirm.js · Le Bureau (Culinarium): Ansicht fotografieren, Konsolenfehler zählen (unsichtbar, eigener Browser, schliesst sich selbst).
   node schirm.js <ansicht> <datei.png> [breite] [höhe] [ganz]   MOTOR=webkit für Safari-Kern. PORT (9082). */
const path = require('path'), os = require('os');
const pw = require(process.env.PLAYWRIGHT_PFAD || path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
(async () => {
  const [ans, datei, b = 1440, h = 900, ganz] = process.argv.slice(2);
  const br = await pw[process.env.MOTOR || 'chromium'].launch({ headless: true });
  const ctx = await br.newContext({ viewport: { width: +b, height: +h }, isMobile: +b < 700 && (process.env.MOTOR || 'chromium') === 'chromium', hasTouch: +b < 700 });
  await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-culinarium-bureau', '1'); } catch (e) {} });
  const p = await ctx.newPage(), f = [];
  p.on('console', m => { if (m.type() === 'error') f.push(m.text()); });
  p.on('pageerror', e => f.push('pageerror: ' + e.message));
  await p.goto(`http://127.0.0.1:${process.env.PORT || 9082}/_werkzeuge/bureau/?ansicht=` + encodeURIComponent(ans), { waitUntil: 'networkidle' });
  await p.waitForSelector('#ws-mitte[data-ws-bereit]', { timeout: 15000 }).catch(() => f.push('nicht bereit'));
  await p.waitForTimeout(1600);
  const breit = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  await p.screenshot({ path: datei, fullPage: !!ganz });
  console.log(JSON.stringify({ ansicht: ans, breite: +b, fehler: f, ueberstand: breit }));
  await br.close();
})();
