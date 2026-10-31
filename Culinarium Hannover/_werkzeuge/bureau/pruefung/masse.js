/* masse.js · Le Bureau (Culinarium): Fehlerbuch 10a am echten Server (9082, nur lesen, nichts gespeichert), unsichtbar.
   node masse.js [chromium|webkit]
   - jede Ansicht bei 390, 920, 1000, 1100, 1240, 1440: kein Element ragt seitlich hinaus, Kopf-Titel überdeckt keinen Knopf (10a «Kopf», «Verlauf Woche»)
   - jede Seite der Website in der Vorschau des Bureau: Konsole und Netz (10a «Vorschau u. Konsole»), Anleitung und Prüfseite: Netz ab 400 (10a «Anleitung»)
   - jeder Link in Kopf und Rand antwortet (10a «Wege»), «Zur Werkbank» nur aus der Werkbank (10a «Zur Werkbank»)
   - Verlassen mit offener Eingabe fragt nach (R13). */
const path = require('path'), os = require('os');
const pw = require(process.env.PLAYWRIGHT_PFAD || path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const MOTOR = process.argv[2] || 'chromium', B = 'http://127.0.0.1:' + (process.env.PORT || 9082);
let n = 0; const rot = [];
const pruef = (ok, was, mehr) => { n++; console.log((ok ? 'gut    ' : 'FEHLT  ') + was + (!ok && mehr ? '  → ' + String(mehr).slice(0, 400) : '')); if (!ok) rot.push(was); };
(async () => {
  const br = await pw[MOTOR].launch({ headless: true });
  const neu = async (b, h = 900) => { const c = await br.newContext({ viewport: { width: b, height: h } }); await c.addInitScript(() => { try { localStorage.setItem('rundgang-culinarium-bureau', '1'); } catch (e) {} }); return c; };
  const ANS = ['start', 'e:termine', 'b:start', 'b:abend', 'b:dirty-chicken', 'haus:abende', 'angaben', 'zahlen', 'google', 'hinweis', 'entwurf', 'verlauf'];
  for (const b of [390, 920, 1000, 1100, 1240, 1440]) {
    const c = await neu(b), p = await c.newPage(), f = [];
    p.on('pageerror', e => f.push(e.message)); p.on('console', m => { if (m.type() === 'error') f.push(m.text()); });
    for (const a of ANS) {
      await p.goto(B + '/_werkzeuge/bureau/?ansicht=' + encodeURIComponent(a), { waitUntil: 'load' });
      await p.waitForSelector('#ws-mitte[data-ws-bereit]', { timeout: 20000 }).catch(() => f.push('nicht bereit: ' + a));
      await p.waitForTimeout(900);
      const m = await p.evaluate(() => {
        const W = innerWidth, raus = [];
        document.querySelectorAll('#ws-mitte *, #ws-kopf *, #ws-leiste *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.right > W + 1 || r.left < -1) && !e.closest('.cu-vs__huelle, .ws-vs, iframe, [hidden]') && !(e.closest('details:not([open])') && !e.closest('summary')) && getComputedStyle(e).visibility !== 'hidden') raus.push((e.className && e.className.baseVal === undefined ? e.className : e.tagName) + ' ' + Math.round(r.left) + '–' + Math.round(r.right)); });
        const t = document.querySelector('.wo-kopf__mitte, .wo-kopf__titel, #ws-ansicht-name'), kn = [...document.querySelectorAll('#ws-kopf a, #ws-kopf button')].filter(k => k.offsetWidth);
        const tr = t && t.offsetWidth ? t.getBoundingClientRect() : null;
        const deckt = tr ? kn.filter(k => { const r = k.getBoundingClientRect(); return !k.contains(t) && !t.contains(k) && r.left < tr.right && r.right > tr.left && r.top < tr.bottom && r.bottom > tr.top; }).length : 0;
        return { raus: raus.slice(0, 4), zahl: raus.length, ueber: document.documentElement.scrollWidth - W, deckt };
      });
      pruef(!m.zahl && m.ueber <= 0 && !m.deckt, `${a} bei ${b}: nichts ragt hinaus, Kopf-Titel deckt keinen Knopf`, JSON.stringify(m));
    }
    pruef(!f.length, `Konsole sauber bei ${b} (${ANS.length} Ansichten)`, f.join(' | '));
    await c.close();
  }
  // Vorschau jeder Seite (b:<bereich> zeigt die Seiten des Bereichs im Rahmen), Netz und Konsole der eingebetteten Seite
  {
    const c = await neu(1440), p = await c.newPage(), f = [], netz = [];
    p.on('pageerror', e => f.push(e.message)); p.on('console', m => { if (m.type() === 'error') f.push(m.text()); });
    p.on('response', r => { if (r.status() >= 400 && !/\/api\/x\/website\/(aendern|veroeffentlichen)/.test(r.url())) netz.push(r.status() + ' ' + r.url()); });
    p.on('requestfailed', r => { if (!/instagram|google|fonts\.g/.test(r.url()) && !/ERR_ABORTED|cancelled/i.test((r.failure() || {}).errorText || '')) netz.push('fehlgeschlagen ' + r.url() + ' ' + (r.failure() || {}).errorText); });
    const info = await (await fetch(B + '/api/x/website/haus/culinarium')).json();
    for (const s of info.seiten) {
      await p.goto(B + '/_werkzeuge/bureau/?seite=' + encodeURIComponent(s.datei), { waitUntil: 'load' });
      await p.waitForSelector('#ws-mitte[data-ws-bereit]', { timeout: 20000 }).catch(() => f.push('nicht bereit: ' + s.datei));
      await p.waitForTimeout(2200);
      const ok = await p.evaluate(() => { const r = document.querySelector('#ws-mitte iframe'); try { return !!(r && r.contentDocument && r.contentDocument.body && r.contentDocument.body.children.length > 2); } catch (e) { return false; } });
      pruef(ok, `Vorschau ${s.datei}: Seite steht im Rahmen`);
    }
    for (const a of ['anleitung.html', '']) { await p.goto(B + '/_werkzeuge/bureau/' + a, { waitUntil: 'load' }); await p.waitForTimeout(1200); }
    await p.goto(B + '/werkzeuge/website/pruefung.html?haus=culinarium', { waitUntil: 'load' }); await p.waitForTimeout(4000);
    pruef(!netz.length, 'Netz: keine Antwort ab 400 in Vorschau aller Seiten, Anleitung, Prüfseite', [...new Set(netz)].slice(0, 6).join(' | '));
    pruef(!f.length, 'Konsole sauber in der Vorschau aller Seiten', [...new Set(f)].slice(0, 6).join(' | '));
    // Links in Kopf und Rand
    await p.goto(B + '/_werkzeuge/bureau/?ansicht=start', { waitUntil: 'load' }); await p.waitForSelector('#ws-mitte[data-ws-bereit]');
    const links = await p.evaluate(() => [...document.querySelectorAll('#ws-kopf a[href], #ws-rand a[href], .wo-sb a[href]')].map(a => a.href).filter(h => /^http/.test(h)));
    const schlecht = [], fremdePorte = [];
    for (const h of [...new Set(links)]) {
      const u = new URL(h);
      if (u.port !== String(new URL(B).port)) { try { const r = await fetch(h, { redirect: 'manual' }); if (r.status >= 400) schlecht.push(r.status + ' ' + h); } catch (e) { fremdePorte.push(h); } continue; }
      const r = await fetch(h, { redirect: 'manual' });
      if (r.status >= 400) schlecht.push(r.status + ' ' + h);
      const ziel = r.headers.get('location');
      if (ziel && /^http/.test(ziel)) { if (/localhost/.test(ziel)) schlecht.push('localhost ' + ziel); try { const z = await fetch(ziel); if (z.status >= 400) schlecht.push(z.status + ' ' + ziel); } catch (e) { fremdePorte.push(ziel + ' (läuft nicht)'); } }
    }
    pruef(!schlecht.length, `Kopf und Rand: ${new Set(links).size} Links antworten, keiner auf localhost`, schlecht.join(' | '));
    if (fremdePorte.length) console.log('hinweis  Werkzeuge anderer Chats, die gerade nicht laufen: ' + fremdePorte.join(' | '));
    pruef(!(await p.locator('#zur-werkbank').count()), '«Zur Werkbank» fehlt, wenn nicht aus der Werkbank geöffnet');
    await c.close();
  }
  {
    const c = await neu(1440), p = await c.newPage();
    await p.goto(B + '/_werkzeuge/bureau/?ansicht=start&wb=de.werkzeuge&wbo=' + encodeURIComponent('http://127.0.0.1:9088'), { waitUntil: 'load' });
    await p.waitForTimeout(1500);
    const zw = await p.evaluate(() => { const a = document.getElementById('zur-werkbank'); if (!a) return ''; const l = (a.shadowRoot && a.shadowRoot.querySelector('a[href]')) || a.querySelector('a[href]'); return l ? l.href : 'Knopf ohne Link'; });
    pruef(/^http:\/\/127\.0\.0\.1:9088\/werkbank\/index\.html#werkzeuge$/.test(zw), '«Zur Werkbank» aus der Werkbank geöffnet, Ziel 127.0.0.1:9088', zw);
    // R13: Verlassen mit offener Eingabe fragt nach
    await p.goto(B + '/_werkzeuge/bureau/?ansicht=e:termine', { waitUntil: 'load' }); await p.waitForSelector('#ws-mitte[data-ws-bereit]');
    await p.locator('.cu-t input[name="plaetze"]').first().fill('13');
    let gefragt = false; p.on('dialog', d => { if (d.type() === 'beforeunload') gefragt = true; d.dismiss().catch(() => {}); });
    await p.locator('body').click({ position: { x: 5, y: 300 } }).catch(() => {});
    await p.close({ runBeforeUnload: true }); await new Promise(r => setTimeout(r, 800));
    pruef(gefragt, 'R13 Verlassen mit offener Termin-Eingabe: der Browser fragt nach');
    await c.close();
  }
  await br.close();
  console.log((rot.length ? 'NICHT BESTANDEN · ' + rot.length + ' von ' : 'BESTANDEN · ') + n + ' Prüfungen · ' + MOTOR);
})();
