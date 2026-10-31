const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const URLS = process.argv.slice(2);
(async () => {
  const b = await pw.chromium.launch(); const c = await b.newContext({ viewport: { width: 1440, height: 900 } });
  await c.route(/^(mailto|tel):/, r => r.abort());
  const p = await c.newPage();
  for (const u of URLS) {
    await p.goto(u, { waitUntil: 'load' }).catch(e => console.log('ERR', e.message)); await p.waitForTimeout(2000);
    const r = await p.evaluate(() => {
      const sicht = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; };
      const pfad = e => { const t = e.tagName.toLowerCase(); const id = e.id ? '#' + e.id : ''; const k = typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return t + id + (k === '.' ? '' : k); };
      return [...document.querySelectorAll('button,a[href],[role=tab],[data-gehe],summary,[role=button],select')].filter(sicht).map(e => {
        const par = e.closest('nav,aside,header,[role=tablist],dialog,#rand,.wo-rand,.wo-kopf'); return `${pfad(e)} | ${(e.innerText || e.getAttribute('aria-label') || e.title || '').trim().replace(/\s+/g, ' ').slice(0, 40)} | in:${par ? pfad(par) : '-'} | ${e.getAttribute('href') || e.dataset.gehe || ''}`; });
    });
    console.log('##### ' + u + ' (' + r.length + ')'); console.log(r.slice(0, 70).join('\n'));
  }
  await b.close();
})();
