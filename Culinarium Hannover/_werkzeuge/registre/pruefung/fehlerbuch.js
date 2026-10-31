/* Fehlerbuch 10a des Werkzeug-Masters Zeile für Zeile am Besucherbuch von Culinarium messen (28.10.2026, Vorlage Schäfli). Läuft gegen den Werkzeug-Server :9086 (nur lesen, Beispielwerte).
   node pruefung/fehlerbuch.js  → fehlerbuch-ergebnis.json + Bilder kopf-<breite>.png */
const path = require('path'), fs = require('fs');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const A = 'http://127.0.0.1:9086/_werkzeuge/registre/?gruss=tag#';
const ANS = ['start', 'besuche', 'herkunft', 'zeit', 'seiten', 'verlauf', 'buchung', 'zaehlung'];
const erg = {};
const merk = (k, ok, info) => { (erg[k] = erg[k] || []).push({ ok, info }); };
(async () => {
  for (const eng of ['chromium', 'webkit']) {
    const b = await PW[eng].launch();
    for (const [w, h] of [[1440, 900], [1366, 650], [1240, 800], [1180, 800], [1100, 800], [1000, 800], [920, 800], [390, 844], [320, 640]]) {
      const c = await b.newContext({ viewport: { width: w, height: h } });
      await c.addInitScript(() => { try { localStorage.setItem('rundgang-culinarium-registre', '1'); } catch (e) {} });
      for (const a of ANS) {
        const p = await c.newPage(); await p.goto(A + a); await p.waitForFunction(() => window.BG_REGISTRE === 1 && document.documentElement.classList.contains('auftakt-da')); await p.waitForTimeout(1200);
        await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); }); await p.waitForTimeout(3200);
        const r = await p.evaluate(() => {
          const txt = document.body.innerText;
          const roh = /\{[A-Za-z_]|undefined|NaN|\bNone\b|\[object/.test(txt);
          /* Titel im Kopf überdeckt nie einen Knopf */
          const t = document.querySelector('#kopf .wo-kopf__mitte'), kn = [...document.querySelectorAll('#kopf a, #kopf button')].filter(x => x.offsetWidth && !t?.contains(x));
          const tr = t && t.offsetWidth ? t.getBoundingClientRect() : null;
          const kopf = !tr || kn.every(k => { const q = k.getBoundingClientRect(); return q.right <= tr.left + 1 || q.left >= tr.right - 1 || q.bottom <= tr.top || q.top >= tr.bottom; });
          /* Titel auf dunkler Fläche hell */
          const em = [...document.querySelectorAll('.wo-sb h1, .wo-sb h1 em')].map(e => getComputedStyle(e).color);
          const hell = em.every(c => { const m = c.match(/\d+(\.\d+)?/g).map(Number); return 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2] > 200; });
          /* Luft unter der Bühne */
          const sb = document.querySelector('.wo-sb'), nach = sb && sb.nextElementSibling; let luft = null;
          if (sb && nach) luft = Math.round(nach.getBoundingClientRect().top - sb.getBoundingClientRect().bottom);
          /* Abstand Schrift → Kachel/Liste in Blättern: Überschrift zum ersten Inhalt */
          const nah = [...document.querySelectorAll('.blatt h3')].map(h => { const n = h.parentElement.matches('header') ? h.parentElement.nextElementSibling : h.nextElementSibling; return n ? Math.round(n.getBoundingClientRect().top - h.getBoundingClientRect().bottom) : 99; }).filter(x => x < 10);
          /* Kacheln je Reihe: keine Reihe mit einer einzelnen Karte neben Lücke */
          const reihen = sel => { const el = [...document.querySelectorAll(sel)].filter(e => e.offsetWidth); const ys = {}; el.forEach(e => { const y = Math.round(e.getBoundingClientRect().top); ys[y] = (ys[y] || 0) + 1; }); return Object.values(ys); };
          const zahlen = reihen('.zahlen > .blatt'), werte = reihen('.werte > .wert');
          /* Seitlich verrutscht */
          const breit = document.documentElement.scrollWidth - innerWidth;
          /* Bild in jeder Liste von Seiten oder Besuchen */
          const listen = [...document.querySelectorAll('.besuch, .tabelle .zeile:not(.zeile--kopf), .weg li')].filter(e => e.offsetWidth);
          const ohneBild = listen.filter(e => !e.querySelector('img.sbild')).length;
          const bildKlein = [...document.querySelectorAll('.besuch img.sbild, .tabelle img.sbild')].filter(i => i.offsetWidth && i.offsetWidth < 72).length;
          /* Fehlerbuch 10a Zeile 112: jedes Element gegen die Fensterbreite, nicht nur scrollWidth (das Zeichen-Depot #zeichen ausgenommen) */
          const ragt = [...document.querySelectorAll('#ansicht *, #kopf *, #leiste *')].filter(x => { const q = x.getBoundingClientRect(); return q.width && q.right > innerWidth + 1 && !x.closest('svg defs'); }).length;
          /* Zeile 1 (Demo-Check Schäfli): abgeschnittener Text bei verstecktem Überlauf; Auslassungspunkte nur im Kopf-Titel (Zeile 107 erlaubt dort «…») */
          const kappe = [...document.querySelectorAll('#ansicht *, #leiste *')].filter(x => { const c = getComputedStyle(x); return x.offsetWidth && x.childNodes.length && [...x.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && /hidden|clip/.test(c.overflowX) && x.scrollWidth > x.clientWidth + 1; }).map(x => x.textContent.trim().slice(0, 30));
          /* Zeile 115: im Vergleich stösst der Name nie an die Zahl */
          const stoss = [...document.querySelectorAll('.vergleich .vz:not(.vz--kopf)')].filter(z => { const a = z.children[0], b = z.children[1]; if (!a || !b) return false; const r = document.createRange(); r.selectNodeContents(a); const ar = r.getBoundingClientRect(), br = b.getBoundingClientRect(); return ar.top < br.bottom && br.top < ar.bottom && ar.right > br.left - 4; }).length;
          /* Zeile 36: kein mailto: und kein tel: im Werkzeug */
          const mt = [...document.querySelectorAll('a[href^="mailto:"], a[href^="tel:"]')].length;
          /* Zeile 121: der Titel des Startbilds passt in sein Kopfbild (nie abgeschnitten) */
          const h1 = document.querySelector('.wo-sb h1'), sbk = document.querySelector('.wo-sb'); const titel = !h1 || !sbk || h1.scrollWidth <= sbk.getBoundingClientRect().width;
          /* Zeile 88 / 150: kein Foto zweimal auf einem Bildschirm (Besuchsliste ausgenommen: dort trägt jeder Besuch das Foto seiner Startseite, so festgelegt) */
          const fotos = [...document.querySelectorAll('#ansicht img')].filter(i => i.offsetWidth && !i.closest('.besuch')).map(i => i.getAttribute('src'));
          const doppelt = fotos.filter((f, i) => fotos.indexOf(f) !== i);
          return { roh, kopf, hell, em, luft, nah: nah.length, zahlen, werte, breit, ohneBild, bildKlein, ragt, kappe, stoss, mt, titel, doppelt };
        });
        const id = `${eng} ${w} ${a}`;
        merk('Roher Vorlagen-Code nirgends', !r.roh, id);
        merk('Kopf-Titel überdeckt keinen Knopf (920/1000/1100/1240/1440)', r.kopf, id);
        merk('Titel auf dunkler Bühne hell', r.hell, id + ' ' + r.em.join(','));
        if (r.luft != null) merk('Unter der Bühne mindestens 30 px (Handy 24)', r.luft >= (w < 600 ? 24 : 30), id + ' ' + r.luft + ' px');
        merk('Überschrift nie ohne Luft auf Inhalt (< 10 px)', r.nah === 0, id + ' ' + r.nah);
        const gleich = l => !l.length || l.length === 1 || l.every(x => x === 1) && w < 600 || Math.max(...l) - Math.min(...l) <= 1 && l[l.length - 1] !== 1;   /* am Handy eine Spalte ist richtig (Fehlerbuch 10a Zeile 86) */
        merk('Kacheln gleichmässig auf Reihen, keine allein', gleich(r.zahlen) && gleich(r.werte), id + ' ' + JSON.stringify([r.zahlen, r.werte]));
        merk('Kein seitliches Verrutschen', r.breit <= 0, id + ' ' + r.breit);
        merk('Jeder Eintrag einer Liste mit Bild', r.ohneBild === 0, id + ' ' + r.ohneBild);
        merk('Listenbilder nie unter 72 px', r.bildKlein === 0, id + ' ' + r.bildKlein);
        merk('Kein Element ragt aus dem Fenster (jedes Element gemessen)', r.ragt === 0, id + ' ' + r.ragt);
        merk('Kein abgeschnittener Text, keine Auslassungspunkte im Inhalt', !r.kappe.length, id + ' ' + r.kappe.join(' | '));
        merk('Vergleich: Name stösst nie an die Zahl', r.stoss === 0, id + ' ' + r.stoss);
        merk('Kein mailto: und kein tel: im Werkzeug', r.mt === 0, id + ' ' + r.mt);
        merk('Titel des Startbilds passt in sein Kopfbild', r.titel, id);
        merk('Kein Foto zweimal auf einem Bildschirm (ausser Besuchsliste, so festgelegt)', !r.doppelt.length, id + ' ' + r.doppelt.join(','));
        if (a === 'start' && (w === 1440 || w === 1000 || w === 390)) await p.screenshot({ path: path.join(__dirname, `fehlerbuch-${eng}-${w}.png`) });
        await p.close();
      }
      /* Rundgang-Schild steht fest beim Scrollen */
      const c2 = await b.newContext({ viewport: { width: w, height: h } }); const p2 = await c2.newPage();
      await p2.goto(A + 'besuche'); await p2.waitForTimeout(2500);
      const s1 = await p2.evaluate(() => { const s = [...document.querySelectorAll('body *')].find(e => /Kurzer Rundgang/.test(e.textContent) && getComputedStyle(e).position === 'fixed'); return s ? Math.round(s.getBoundingClientRect().top) : null; });
      await p2.mouse.wheel(0, 900); await p2.waitForTimeout(700);
      const s2 = await p2.evaluate(() => { const s = [...document.querySelectorAll('body *')].find(e => /Kurzer Rundgang/.test(e.textContent) && getComputedStyle(e).position === 'fixed'); return s ? Math.round(s.getBoundingClientRect().top) : null; });
      merk('Rundgang-Schild steht fest beim Scrollen', s1 === null || s1 === s2, `${eng} ${w} ${s1}→${s2}`);
      await c2.close(); await c.close();
    }
    await b.close();
  }
  const kurz = Object.fromEntries(Object.entries(erg).map(([k, l]) => [k, { gruen: l.filter(x => x.ok).length, von: l.length, rot: l.filter(x => !x.ok).map(x => x.info).slice(0, 8) }]));
  fs.writeFileSync(path.join(__dirname, 'fehlerbuch-ergebnis.json'), JSON.stringify(kurz, null, 1));
  console.log(JSON.stringify(kurz, null, 1));
})();
