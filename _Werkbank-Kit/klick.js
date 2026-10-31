// Klickprüfung der Werkbank und ihrer Unterseiten: node _werkbank/klick.js
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.env.B || 'http://127.0.0.1:8912/', ROOT = process.env.ROOT || path.join(__dirname, '..');
(async () => {
  const b = await chromium.launch({ headless: true });
  const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
  const fehler = []; p.on('pageerror', e => fehler.push(String(e)));
  const kaputt = []; p.on('response', r => { if (r.status() >= 400) kaputt.push(r.status() + ' ' + r.url()); });
  await p.goto(B + 'werkbank/', { waitUntil: 'load' });
  await p.waitForTimeout(4200);
  const aus = {};
  aus.tor_weg = await p.evaluate(() => !document.querySelector('.tor'));
  const zu = async id => { await p.evaluate(i => { const x = document.getElementById(i); if (x) x.scrollIntoView(); }, id); };
  await zu('mitgebracht'); await p.waitForTimeout(await p.$('#mitgebracht') ? 3800 : 200);   // «Mitgebracht» gibt es nicht in jeder Werkbank
  aus.zahlen = await p.$$eval('.odo', os => os.map(o => o.getAttribute('data-z') + '=' + [...o.querySelectorAll('.od')].map(s => Math.round(-new DOMMatrix(getComputedStyle(s).transform).m42 / s.firstChild.getBoundingClientRect().height)).join('')));
  await zu('vergleich'); await p.waitForTimeout(700);
  await p.evaluate(() => { const i = document.querySelector('.vgl input'); i.value = 20; i.dispatchEvent(new Event('input')); });
  aus.vergleich = await p.$eval('.vgl', e => e.style.getPropertyValue('--x'));
  await zu('ideen'); await p.waitForTimeout(900); await p.evaluate(() => scrollBy(0, 300)); await p.waitForTimeout(900);
  for (let i = 0; i < 3; i++) { await p.click('#ideen [data-vor]'); await p.waitForTimeout(700); }
  aus.ideen = await p.$eval('#ideen .gang__z', e => e.textContent);
  await zu('gefuege'); await p.waitForTimeout(600); await p.evaluate(() => scrollBy(0, 420)); await p.waitForTimeout(4600);
  aus.kacheln = await p.$$eval('.bn', e => e.length); aus.linien = await p.$$eval('.bl', e => e.length);
  await p.click('.bn--sys button'); await p.waitForTimeout(600);
  aus.gefuege = await p.evaluate(() => [document.getElementById('bp-t').textContent, document.querySelectorAll('.bn.heiss').length, document.querySelectorAll('.bl.heiss').length, document.getElementById('bp-w').textContent.slice(0, 80)]);
  await p.click('.bn--sys button'); await p.waitForTimeout(300);
  await p.click('#brett-rund'); await p.waitForTimeout(4700);
  aus.rundgang = await p.evaluate(() => [document.getElementById('bp-t').textContent, document.getElementById('brett-rund').firstChild.textContent]);
  await p.click('#brett-rund'); await p.waitForTimeout(300);
  aus.kacheln_ueberlappen = await p.evaluate(() => { const r = [...document.querySelectorAll('.bn')].map(e => e.getBoundingClientRect()); let n = 0; for (let i = 0; i < r.length; i++) for (let j = i + 1; j < r.length; j++) if (r[i].left < r[j].right && r[j].left < r[i].right && r[i].top < r[j].bottom && r[j].top < r[i].bottom) n++; return n; });
  await zu('seiten'); await p.waitForTimeout(600); await p.evaluate(() => scrollBy(0, 380)); await p.waitForTimeout(1500);
  const stand = () => p.evaluate(() => [document.querySelector('.schau__t h3').textContent, document.querySelector('.schau__z').textContent, document.querySelectorAll('.schau__s img.an').length, (document.querySelector('.schau__s img.an') || {}).naturalWidth, document.querySelectorAll('.schau__r .tel img.an').length]);
  aus.seiten_start = await stand();
  let alle = 0; const total = await p.evaluate(() => window.SEITEN.reduce((a, s) => a + s.n, 0));
  for (let i = 0; i < total; i++) { await p.click('.schau [data-vor]'); await p.waitForTimeout(260); const s = await stand(); if (s[2] === 1 && s[3] > 0 && s[4] === 1) alle++; }
  aus.seiten_rundum = alle + ' von ' + total + ' Ansichten mit Rechner- und Handybild';
  await p.click('.wahl button:nth-child(3)'); await p.waitForTimeout(900);
  aus.seiten_wahl = await stand(); aus.seiten_link = await p.$eval('.schau__t a', a => a.getAttribute('href'));
  const links = await p.$$eval('a[href]', as => as.map(a => a.getAttribute('href')));
  aus.lokal_fehlt = [...new Set(links.filter(h => h.startsWith('../')))].filter(h => !fs.existsSync(path.join(ROOT, decodeURIComponent(h.replace('../', '').split('#')[0].split('?')[0]))));
  aus.leer = links.filter(h => !h || h === '#' || h === 'None').length;
  aus.anker_tot = await p.evaluate(() => [...document.querySelectorAll('a[href^="#"]')].filter(a => a.getAttribute('href').length > 1 && !document.querySelector(a.getAttribute('href'))).map(a => a.getAttribute('href')));
  aus.bilder_kaputt = await p.evaluate(async () => { const o = []; for (const i of document.querySelectorAll('img')) { const s = i.currentSrc || i.src; const r = await fetch(s); if (!r.ok) o.push(s); } return o; });
  aus.titel_zu_breit = await p.evaluate(() => [...document.querySelectorAll('.zt')].filter(t => [...t.querySelectorAll('.z>span')].some(s => s.offsetWidth > t.clientWidth + 1)).map(t => t.textContent));
  // Unterseiten: jeder Link, jede Datei
  for (const s of ['unterlagen', 'drucksachen', process.env.ETIK || 'kofferetiketten', 'material']) {
    await p.goto(B + s + '/index.html', { waitUntil: 'load' }); await p.waitForTimeout(1800);
    const l = await p.$$eval('a[href]', as => as.map(a => a.getAttribute('href')));
    const fehlt = [...new Set(l.filter(h => !/^(https?:|mailto:|#)/.test(h)))].filter(h => !fs.existsSync(path.join(ROOT, s, decodeURIComponent(h.split('#')[0].split('?')[0]))));
    const zb = await p.evaluate(() => [...document.querySelectorAll('.zt')].filter(t => [...t.querySelectorAll('.z>span')].some(x => x.offsetWidth > t.clientWidth + 1)).map(t => t.textContent));
    aus[s] = { links: l.length, fehlt, titel_zu_breit: zb };
    if (s === 'unterlagen') {
      const n = await p.evaluate(() => window.UNTERLAGEN.reduce((a, d) => a + d.neu.length, 0)); let gut = 0;
      await p.evaluate(() => document.getElementById('blaettern').scrollIntoView()); await p.waitForTimeout(800);
      for (let i = 0; i < n; i++) {
        const ok = await p.evaluate(async () => { const a = [...document.querySelectorAll('.ublatt__b')].map(k => { const im = k.querySelectorAll('img'); return im[im.length - 1]; }); await Promise.all(a.map(i => i.decode().catch(() => 0))); return a.every(i => i && i.naturalWidth > 0); });
        if (ok) gut++;
        if (i < n - 1) { await p.click('.uschau [data-vor]'); await p.waitForTimeout(120); }
      }
      aus.unterlagen.blaettern = gut + ' von ' + n + ' Seiten, beide Fassungen geladen';
      aus.unterlagen.ende = await p.$eval('.ufuss p', e => e.textContent);
      await p.click('.uwahl button:last-child'); await p.waitForTimeout(500);
      aus.unterlagen.wahl = [await p.$eval('.ufuss h3', e => e.textContent), await p.$eval('[data-pdf]', e => e.getAttribute('href'))];
    }
  }
  console.log(JSON.stringify(aus, null, 1), kaputt.length ? 'KAPUTT ' + JSON.stringify(kaputt.slice(0, 6)) : 'nichts kaputt', fehler.length ? 'FEHLER ' + JSON.stringify(fehler) : 'keine Fehler');
  await b.close();
})();
