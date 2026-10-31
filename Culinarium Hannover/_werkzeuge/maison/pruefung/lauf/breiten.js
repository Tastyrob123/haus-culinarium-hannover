#!/usr/bin/env node
/* Zwischenbreiten (Fehlerbuch 10a): je Breite seitliches Überragen (jedes Element gegen die Fensterbreite, ohne Laufband), abgeschnittener Text in Leiste und Plakaten,
   Leistennamen unter Knöpfen. node breiten.js <url> [kern] */
const pw = require('playwright');
(async () => {
  const [url, kern = 'webkit'] = process.argv.slice(2); const br = await pw[kern].launch(); const aus = [];
  for (const b of [320, 390, 760, 920, 1000, 1024, 1100, 1180, 1240, 1280, 1366, 1440, 1600]) {
    const p = await br.newPage({ viewport: { width: b, height: 900 } });
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
    const r = await p.evaluate(() => {
      const W = innerWidth; let raus = [];
      document.querySelectorAll('body *').forEach(e => { if (e.closest('.m-band,[data-laufband],.hz-bild,.wo-sb__foto')) return; const q = e.getBoundingClientRect(); const cs = getComputedStyle(e);
        if (q.width && cs.visibility !== 'hidden' && cs.display !== 'none' && (q.right > W + 1 || q.left < -1) && !e.closest('[aria-hidden="true"]')) raus.push((e.className || e.tagName) + ' ' + Math.round(q.right)); });
      const ab = [...document.querySelectorAll('.m-f5__t b,.m-f5__w,.m-f5__t small,.m-f5__titel,.m-f5__zeile,.m-insel__p,.m-saal__titel')].filter(e => e.offsetParent && e.scrollWidth > e.clientWidth + 1).map(e => e.textContent.trim().slice(0, 30));
      return { doc: document.documentElement.scrollWidth, raus: raus.slice(0, 4), ab };
    });
    aus.push(b + ': doc ' + r.doc + (r.raus.length ? ' RAUS ' + r.raus.join(', ') : '') + (r.ab.length ? ' ABGESCHNITTEN ' + r.ab.join(' | ') : ''));
    await p.close();
  }
  await br.close(); console.log(aus.join('\n'));
})();
