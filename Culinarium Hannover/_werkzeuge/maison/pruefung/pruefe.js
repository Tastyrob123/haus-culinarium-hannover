#!/usr/bin/env node
/* Prüflauf von La Maison · Culinarium Hannover (Master 9a: bedient, nicht nur geladen). node pruefung/pruefe.js chromium|webkit [basis]
   Grössen 1440 × 900 und 390 × 844 (GROESSEN=…). Unsichtbar, eine Browser-Instanz, nichts wird geschrieben. Ergebnis pruefung/ergebnis-<browser>.json */
const path = require('path'), os = require('os'), fs = require('fs');
module.paths.push(path.join(os.homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
const MOTOR = process.argv[2] || 'chromium', BASIS = process.argv[3] || 'http://127.0.0.1:9081/_werkzeuge/maison/';
const GROESSEN = (process.env.GROESSEN || '1440x900,390x844').split(',').map(g => g.split('x').map(Number));
const erg = [];
const ok = (w, name, gut, info) => { erg.push({ w, name, gut: !!gut, info: info === undefined ? '' : info }); };
(async () => {
  const browser = await pw[MOTOR].launch({ headless: true });
  for (const [B, H] of GROESSEN) {
    const w = `${MOTOR} ${B}`, hand = B < 1000;
    const neu = async (opt = {}) => {
      const ctx = await browser.newContext({ viewport: { width: B, height: H }, deviceScaleFactor: 1, locale: 'de-DE', timezoneId: 'Europe/Berlin', reducedMotion: opt.ruhig ? 'reduce' : 'no-preference', hasTouch: hand });
      const page = await ctx.newPage(); const f = [];
      page.on('console', m => { if (m.type() === 'error') f.push(m.text()); });
      page.on('pageerror', e => f.push(String(e)));
      if (opt.route) await opt.route(page);
      return { ctx, page, f };
    };
    // 1 zweimal laden, ohne Fehler, ohne Überlauf, alle Bilder da nach dem Durchscrollen
    for (const lauf of [1, 2]) {
      const { ctx, page, f } = await neu();
      const r = await page.goto(BASIS, { waitUntil: 'load' });
      await page.waitForTimeout(1600);
      ok(w, `Laden ${lauf}: Antwort 200`, r.status() === 200, r.status());
      const hoch = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < hoch; y += 500) { await page.evaluate(v => scrollTo(0, v), y); await page.waitForTimeout(90); }
      await page.waitForTimeout(1500);
      const b = await page.evaluate(() => [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.getAttribute('src')));
      ok(w, `Laden ${lauf}: keine kaputten Bilder`, !b.length, b.join(' '));
      const ue = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      ok(w, `Laden ${lauf}: kein seitliches Überlaufen`, ue <= 0, ue + ' px');
      const tuer = await page.evaluate(() => !document.getElementById('tuer').hidden);
      ok(w, `Laden ${lauf}: Startfehler-Tür zu`, !tuer);
      const nichtda = await page.evaluate(() => [...document.querySelectorAll('[data-r]')].filter(x => !x.classList.contains('da')).length);
      ok(w, `Laden ${lauf}: alle Stücke aufgetreten`, nichtda === 0, nichtda);
      ok(w, `Laden ${lauf}: Konsole leer`, !f.length, f.slice(0, 3).join(' | '));
      const roh = await page.evaluate(() => document.body.innerText.match(/\{|\}|undefined|NaN|\bNone\b|\bnull\b/g));
      ok(w, `Laden ${lauf}: kein roher Code im Text ({ undefined NaN None)`, !roh, roh && roh.join(' '));
      if (lauf === 1) {
        await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(400);
        const erst = await page.evaluate(() => { const g = [...document.querySelectorAll('.m-f5__k'), document.querySelector('.m-f5__zeile')].map(x => x.getBoundingClientRect().bottom); return [Math.max(...g), innerHeight, document.querySelector('.m-f5__titel').getBoundingClientRect().top]; });
        if (!hand) ok(w, 'Erstes Bild: Titel, Zahlenzeile und alle sechs Werkzeuge ganz (10a)', erst[0] <= erst[1] + .5 && erst[2] >= 0, erst.map(Math.round).join(' / '));
        const leiste = await page.evaluate(() => { const o = document.querySelector('.m-oben'); const wege = document.querySelector('.m-insel__wege'); if (!wege || getComputedStyle(wege).display === 'none') return 'nur Marke'; const r = [...document.querySelectorAll('.m-oben__ecke')].filter(x => getComputedStyle(x).display !== 'none').map(x => x.getBoundingClientRect()); const i = document.querySelector('.m-insel').getBoundingClientRect(); return r.every(k => k.right <= i.left + .5 || k.left >= i.right - .5) ? 'Namen frei' : 'UEBERLAPPT'; });
        ok(w, 'Leiste: Namen nie unter einem Knopf (10a)', leiste !== 'UEBERLAPPT', leiste);
      }
      await ctx.close();
    }
    // 2 Gruss nach Tageszeit und Datum
    for (const [g, t] of [['morgen', 'Guten Morgen.'], ['tag', 'Guten Tag.'], ['abend', 'Guten Abend.']]) {
      const { ctx, page } = await neu(); await page.goto(BASIS + '?gruss=' + g, { waitUntil: 'load' });
      const x = await page.evaluate(() => [document.getElementById('gruss').textContent, document.getElementById('datum').textContent]);
      ok(w, `Gruss ${g}`, x[0] === t && /\d{4}/.test(x[1]), x.join(' · ')); await ctx.close();
    }
    // 3 Empfang: Vorschau je Zeile (M23), zurück in Ruhe, Tastatur-Fokus, nichts bewegt sich an der Zeile
    {
      const { ctx, page, f } = await neu(); await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(1800);
      const zeilen = await page.$$('.hz-z a');
      ok(w, 'Sechs Werkzeuge in der Tafel', zeilen.length === 6, zeilen.length);
      if (!hand) {
        for (let i = 0; i < zeilen.length; i++) {
          const lage = j => page.evaluate(k => { const r = document.querySelectorAll('.hz-z a')[k].getBoundingClientRect(); return { y: r.top + scrollY, height: r.height }; }, j);
          await zeilen[i].scrollIntoViewIfNeeded(); const vor = await lage(i);
          { const bb = await zeilen[i].boundingBox(); await zeilen[i].hover({ position: { x: Math.min(30, bb.width / 2), y: Math.max(4, bb.height - 30) } }); } await page.waitForTimeout(700);   /* unten im Fenster: in der Mitte liegt die Zahlenzeile darüber */
          const an = await page.evaluate(() => [...document.querySelectorAll('.hz-z a')].findIndex(a => a.classList.contains('an')));
          const nach = await lage(i);
          ok(w, `Zeile ${i + 1}: Zeiger hebt Werkzeug ${i + 1} hervor`, an === i, an);
          ok(w, `Zeile ${i + 1}: nichts hüpft`, Math.abs(vor.y - nach.y) < 0.5 && Math.abs(vor.height - nach.height) < 0.5);
        }
        { await page.evaluate(() => scrollTo(0, 0)); const z = await page.evaluate(() => { const r = document.querySelector('.m-f5__zeile').getBoundingClientRect(); return [r.left + 40, r.top + r.height / 2]; }); await page.mouse.move(z[0], z[1]); await page.mouse.move(z[0] + 3, z[1]); } await page.waitForTimeout(700);   /* Zeiger auf die Zahlenzeile: die Fenster reichen über den ganzen Schirm */
        ok(w, 'Zeiger weg: kein Werkzeug hervorgehoben', await page.evaluate(() => ![...document.querySelectorAll('.hz-z a')].some(a => a.classList.contains('an'))));
        await page.focus('.m-f5__reihe .hz-z:nth-child(3) a'); await page.waitForTimeout(700);
        ok(w, 'Tastatur-Fokus auf Zeile 3 hebt sie hervor', await page.evaluate(() => document.querySelectorAll('.hz-z a')[2].classList.contains('an')));
        await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(1600);
        const fe = await page.evaluate(() => [...document.querySelectorAll('.m-f5__k')].map(a => { const r = a.getBoundingClientRect(); return [r.top, r.height, r.width]; }));
        ok(w, 'Fünf Fenster nebeneinander: gleiche Oberkante, Höhe und Breite', fe.length === 5 && fe.every(x => Math.abs(x[0] - fe[0][0]) <= 1 && Math.abs(x[1] - fe[0][1]) <= 1 && Math.abs(x[2] - fe[0][2]) <= 4), JSON.stringify(fe.map(x => x.map(Math.round))));
        const na = await page.evaluate(() => [...document.querySelectorAll('.m-f5__t b')].filter(b => !b.closest('small')).map(b => Math.round(b.getBoundingClientRect().top)));
        ok(w, 'Namen der Fenster auf einer Linie (Kriterium 3)', na.every(y => Math.abs(y - na[0]) <= 1), na.join(' / '));
        
      } else {
        ok(w, 'Handy: Fenster untereinander, ganz im Bild', await page.evaluate(() => { const k = [...document.querySelectorAll('.m-f5__k')].map(a => a.getBoundingClientRect()); return k.every((r, i) => r.width <= innerWidth + .5 && r.left >= -.5 && (!i || r.top >= k[i - 1].bottom - .5)); }));
      }
      ok(w, 'Empfang ohne Fehler', !f.length, f.slice(0, 3).join(' | '));
      await ctx.close();
    }
    // 4 Taste 1 bis 6 öffnet (M12); Ziel abgefangen
    if (!hand) for (let i = 1; i <= 6; i++) {
      const { ctx, page } = await neu(); await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(900);
      const href = await page.evaluate(j => document.querySelectorAll('.hz-z a')[j].href, i - 1);
      await page.keyboard.press(String(i)); await page.waitForTimeout(700);
      ok(w, `Taste ${i} öffnet das Werkzeug`, page.url() === href || page.url().split('#')[0] === href.split('#')[0] && page.url().endsWith(href.split('#')[1] ? '#' + href.split('#')[1] : ''), page.url());
      await ctx.close();
    }
    // 5 Leiste: Ecke führt nach oben; Laufzeile läuft nur im Bild
    {
      const { ctx, page } = await neu(); await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(800);
      await page.evaluate(() => document.querySelector('[data-laufband]').scrollIntoView({ block: 'center' })); await page.waitForTimeout(500);
      ok(w, 'Laufzeile läuft im Bild', await page.evaluate(() => document.querySelector('[data-laufband]').classList.contains('laeuft')));
      await page.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await page.waitForTimeout(500);
      ok(w, 'Laufzeile hält ausserhalb', await page.evaluate(() => !document.querySelector('[data-laufband]').classList.contains('laeuft')));
      await page.evaluate(() => scrollTo(0, 400)); await page.waitForTimeout(400);
      await page.click('.m-ecke'); await page.waitForTimeout(600);
      ok(w, 'Ecke führt nach oben', await page.evaluate(() => location.hash === '#oben'));
      const knoepfe = await page.evaluate(() => [...document.querySelectorAll('.m-oben a')].every(a => { const r = a.getBoundingClientRect(); return r.right <= innerWidth + .5 && r.left >= -.5; }));
      ok(w, 'Eck-Knöpfe ganz im Bild', knoepfe);
      await ctx.close();
    }
    // 6 Weniger Bewegung: alles steht sofort
    {
      const { ctx, page } = await neu({ ruhig: true }); await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(300);
      const t = await page.evaluate(() => [...document.querySelectorAll('[data-r],.m-f5__k,.m-f5__t,.m-f5__titel,.m-f5__zeile')].filter(x => getComputedStyle(x).transform !== 'none' && !(innerWidth <= 800 && x.matches('.m-f5__t'))).length);
      ok(w, 'Weniger Bewegung: nichts verschoben', t === 0, t); await ctx.close();
    }
    // 7 Startfehler-Tür (R04): maison.js fehlt
    {
      const { ctx, page } = await neu({ route: p => p.route('**/maison.js*', r => r.abort()) });
      await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(600);
      const x = await page.evaluate(() => [!document.getElementById('tuer').hidden, document.getElementById('tuer-t').textContent]);
      ok(w, 'Startfehler-Tür öffnet bei fehlendem Skript', x[0], x[1]); await ctx.close();
    }
    // 8 Werkzeuge antworten nicht: Satz ohne Zahl, nichts geschätzt
    {
      const { ctx, page } = await neu({ route: p => p.route('**/_weiter/**', r => r.fulfill({ status: 500, body: '{}' })) });
      await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(1500);
      const z = await page.evaluate(() => [...document.querySelectorAll('[data-stand$="-kurz"]')].map(x => x.textContent));
      ok(w, 'Ohne Antwort: Sätze ohne Zahl', z.length >= 6 && z.every(t => !/\d/.test(t)), z.join(' | '));
      ok(w, 'Ohne Antwort: Zahlenzeile «–»', await page.evaluate(() => document.querySelector('[data-stand="registre-heute"]').textContent === '–'));
      await ctx.close();
    }
  }
  await browser.close();
  const rot = erg.filter(x => !x.gut);
  fs.writeFileSync(path.join(__dirname, `ergebnis-${MOTOR}.json`), JSON.stringify({ zeit: new Date().toISOString(), basis: BASIS, gruen: erg.length - rot.length, rot: rot.length, ergebnis: erg }, null, 1));
  console.log(`${MOTOR}: ${erg.length - rot.length} grün, ${rot.length} rot`); rot.forEach(x => console.log('  ROT', x.w, x.name, x.info));
})().catch(e => { console.error(String(e)); process.exit(1); });
