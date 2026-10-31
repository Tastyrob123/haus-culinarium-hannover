/* gaeste.js · das Werkzeug «gaeste» (Grandhotel: La Réception, Landhaus: Der Gastgeber). Gilt für jedes Haus: ?haus=<kennung>.

   Eingang              Anfragen von Gästen (Zimmer, Tisch, Feier, Tagung) mit Antwortentwurf. Verschickt wird nichts.
   Das wurde gefragt    jede Frage an den Chat; wo er keine Antwort hatte, trägt das Team sie einmal nach.
   Wissen des Hauses    ansehen und ergänzen: Entwurf → Vorher, nachher → Veröffentlichen → Verlauf → Zurückholen.
   Probe-Chat           das Team sieht, was ein Gast sehen würde (wie veröffentlicht oder mit dem Entwurf).
   Auswertung           die häufigsten Fragen.
   Kosten und Schutz    Stand der KI, Kosten, Grenzen, Daten von Gästen löschen.

   Das Wissen geht über den gemeinsamen Speicher (/api/stand, /api/veroeffentlichen …), alles andere über
   werkzeuge/gaeste/api.py (/api/x/gaeste/<haus>/…). Was von Gästen oder aus der KI kommt, wird nur als Text gesetzt, nie als HTML. */
'use strict';
(function () {
  var HAUS = Welt.haus;
  var W = 'gaeste';
  var X = '/api/x/' + W + '/' + encodeURIComponent(HAUS) + '/';
  var PFEIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  var KREUZ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>';
  var WINKEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>';
  var ART = { zimmer: 'Zimmer', tisch: 'Tisch', feier: 'Feier', tagung: 'Tagung' };
  var SPRACHE = { de: 'Deutsch', en: 'Englisch', fr: 'Französisch', zh: 'Chinesisch', ko: 'Koreanisch', ar: 'Arabisch' };
  var HERKUNFT = { gast: 'Gast', probe: 'Probe-Chat', quelle: 'Probelauf im Projekt', beispiel: 'Beispiel, kein echter Gast' };
  var BEREICHE = [['start', 'Übersicht'], ['eingang', 'Eingang'], ['gefragt', 'Das wurde gefragt'], ['wissen', 'Wissen des Hauses'], ['probe', 'Probe-Chat'],
    ['auswertung', 'Auswertung'], ['verlauf', 'Verlauf'], ['betrieb', 'Kosten und Schutz']];
  var S = { stand: null, betrieb: null, ue: null, haus: '', ansicht: 'start', wahl: '', eingang: 'offen', gefragt: 'luecke', mitProben: true, wissen: 'team', suche: '',
    zeitraum: 'alles', ausProben: false, verlauf: null, protokoll: null, chat: { nachrichten: [], gespraech: '', stand: 'live', laeuft: false }, schreibt: {}, offenText: {}, treffer: null, kleid: null, auftritt: true, spur: [], beispieleDa: false };

  /* ---------- kleine Helfer ---------- */
  function $(s, r) { return (r || document).querySelector(s); }
  function h(tag, eig) {
    var e = document.createElement(tag), i, k;
    eig = eig || {};
    for (k in eig) {
      if (eig[k] == null || eig[k] === false) continue;
      if (k === 'class') e.className = eig[k];
      else if (k === 'text') e.textContent = eig[k];
      else if (k === 'html') e.innerHTML = eig[k];          // nur für feste Zeichen aus dieser Datei
      else if (k === 'klick') e.addEventListener('click', eig[k]);
      else e.setAttribute(k, eig[k] === true ? '' : eig[k]);
    }
    for (i = 2; i < arguments.length; i++) haenge(e, arguments[i]);
    return e;
  }
  function haenge(e, kind) {
    if (kind == null || kind === false) return;
    if (Array.isArray(kind)) return kind.forEach(function (x) { haenge(e, x); });
    e.appendChild(typeof kind === 'string' || typeof kind === 'number' ? document.createTextNode(String(kind)) : kind);
  }
  function kn(text, klick, art) {
    art = art || {};
    var b = h('button', { class: 'kn' + (art.dunkel ? ' kn--d' : '') + (art.gross ? '' : ' kn--klein') + (art.ohne ? ' kn--ohne' : ''), type: 'button', klick: klick, id: art.id, disabled: art.aus }, text);
    if (!art.ohne) b.appendChild(h('i', { 'aria-hidden': 'true', html: PFEIL }));
    return b;
  }
  function link(text, klick, id) { return h('button', { class: 'ga-link', type: 'button', klick: klick, id: id }, text); }
  function feld(name, id, wert, art) {
    art = art || {};
    var ein = art.lang ? h('textarea', { id: id, rows: art.zeilen || 5, placeholder: art.platz, maxlength: art.max }) : h('input', { id: id, type: 'text', placeholder: art.platz, maxlength: art.max, autocomplete: 'off', inputmode: art.zahl ? 'decimal' : null });
    ein.value = wert || '';
    return h('div', { class: 'feld' }, h('label', { for: id }, name), ein);
  }
  function wahl(name, punkte, an, klick) {
    return h('div', { class: 'wahl', role: 'group', 'aria-label': name }, punkte.map(function (p) {
      return h('button', { type: 'button', 'aria-pressed': String(p[0] === an), 'data-wahl': String(p[0]), disabled: p[2], klick: function () { klick(p[0]); } }, p[1]);
    }));
  }
  function titel(kap, eins, zwei, satz, knoepfe, gruss) {
    return h('header', { class: 'ga-titel' + (gruss ? ' ga-titel--gruss' : '') }, h('p', { class: 'kap' }, kap), h('h1', { class: 't-ansicht' + (gruss ? ' ga-gruss' : '') }, eins, zwei ? [' ', h('span', { class: 't-akzent' }, zwei)] : null),
      satz ? h('p', {}, satz) : null, knoepfe ? h('div', { class: 'ga-titel__kn' }, knoepfe) : null);
  }
  function zw(eins, zwei) { return h('h2', { class: 't-zwischen ga-zwischen' }, eins, zwei ? [' ', h('span', { class: 't-akzent' }, zwei)] : null); }
  function bild(name) { return S.kleid && name ? 'kleid/' + encodeURIComponent(HAUS) + '/' + name : ''; }
  function leer(kopf, satz, knopf) { return h('div', { class: 'platte ga-leer' }, h('p', { class: 't-zwischen' }, kopf), h('p', {}, satz), knopf || null); }
  function gleich(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
  function kopie(a) { return JSON.parse(JSON.stringify(a)); }
  function mal(n, eins, viele) { return n === 1 ? eins : n + ' ' + viele; }
  function datum(iso) { var d = new Date(iso); return isNaN(d) ? '' : d.toLocaleDateString('de-CH', { day: '2-digit', month: '2-digit', year: 'numeric' }); }
  function zeit(iso) { var d = new Date(iso); return isNaN(d) ? '' : datum(iso) + ', ' + d.toLocaleTimeString('de-CH', { hour: '2-digit', minute: '2-digit' }) + ' Uhr'; }
  function kurzZeit(iso) {      // wie in einem Posteingang: heute die Uhrzeit, gestern, sonst das Datum
    var d = new Date(iso), h0 = new Date(); if (isNaN(d)) return '';
    var uhr = d.toLocaleTimeString('de-CH', { hour: '2-digit', minute: '2-digit' }), tage = Math.round((new Date(h0.getFullYear(), h0.getMonth(), h0.getDate()) - new Date(d.getFullYear(), d.getMonth(), d.getDate())) / 864e5);
    return tage === 0 ? uhr : tage === 1 ? 'gestern, ' + uhr : d.toLocaleDateString('de-CH', { day: '2-digit', month: '2-digit' }) + ', ' + uhr;
  }
  function usd(x) { return 'USD ' + (x >= 1 ? x.toFixed(2) : x.toFixed(4)); }
  function wer() { try { return localStorage.getItem('gaeste-wer') || 'Team'; } catch (e) { return 'Team'; } }
  function doc() { return S.stand.entwurf || S.stand.live; }
  function kennung() { return S.stand.kennung_entwurf || S.stand.kennung_live; }

  /* ---------- Server ---------- */
  function ruf(methode, weg, daten) {
    return fetch(weg, { method: methode, cache: 'no-store', headers: daten !== undefined ? { 'Content-Type': 'application/json' } : undefined, body: daten !== undefined ? JSON.stringify(daten) : undefined })
      .catch(function () { var f = new Error('Der Server antwortet nicht. Ihre Eingabe ist noch nicht gespeichert.'); f.stichwort = 'verbindung'; throw f; })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (d) {
          if (!r.ok) { var f = new Error(d.fehler || ('Fehler ' + r.status)); f.status = r.status; f.stichwort = d.stichwort || ''; f.daten = d; throw f; }
          return d;
        });
      });
  }
  function eigen(was, daten) { return ruf(daten === undefined ? 'GET' : 'POST', X + was, daten); }
  function speicher(was, methode, daten, mehr) { return ruf(methode, '/api/' + was + '/' + encodeURIComponent(HAUS) + '/' + W + (mehr ? '/' + mehr : ''), daten); }

  /* ---------- Quittung: nichts speichert still ---------- */
  function quittung(kopf, text, aktionen, art) {
    art = art || {};
    var q = h('div', { class: 'quittung ga-quittung' + (art.fehl ? ' ga-quittung--fehl' : ''), role: art.fehl ? 'alert' : 'status' },
      h('div', { class: 'ga-quittung__t' }, h('b', {}, kopf), text ? h('span', {}, text) : null));
    (aktionen || []).forEach(function (a) { q.appendChild(link(a[0], function () { q.remove(); a[1](); })); });
    q.appendChild(h('button', { class: 'ga-zu', type: 'button', 'aria-label': 'Schliessen', html: KREUZ, klick: function () { q.remove(); } }));
    var ort = $('#ga-quittungen');
    ort.appendChild(q);
    while (ort.children.length > 3) ort.firstChild.remove();
    setTimeout(function () { q.remove(); }, art.fehl ? 20000 : 12000);
    return q;
  }
  function fehl(e) { quittung('Das hat nicht geklappt', String((e && e.message) || e) + (e && e.stichwort ? ' (Stichwort: ' + e.stichwort + ')' : ''), [], { fehl: true }); }

  /* ---------- Fenster ---------- */
  var vorFenster = null;
  function fenster(eins, zwei, inhalt, knoepfe) {
    var f = $('#ga-fenster');
    vorFenster = document.activeElement;
    f.textContent = '';
    f.appendChild(h('div', { class: 'ga-fenster__k', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'ga-f-titel' },
      h('div', { class: 'ga-fenster__kopf' }, h('h2', { class: 't-zwischen', id: 'ga-f-titel' }, eins, zwei ? [' ', h('span', { class: 't-akzent' }, zwei)] : null),
        h('button', { class: 'ga-zu', type: 'button', 'aria-label': 'Schliessen', html: KREUZ, klick: fensterZu })),
      inhalt, h('p', { class: 'angabe', id: 'ga-f-meldung', role: 'alert' }), knoepfe ? h('div', { class: 'ga-fenster__kn' }, knoepfe) : null));
    f.hidden = false;
    var erstes = f.querySelector('input,textarea') || f.querySelector('.ga-fenster__kn button') || f.querySelector('button');
    if (erstes) erstes.focus();
  }
  function fensterZu() { var f = $('#ga-fenster'); f.hidden = true; f.textContent = ''; if (vorFenster && vorFenster.focus) { try { vorFenster.focus(); } catch (e) { /* weg */ } } }
  function fensterMeldung(t) { var m = $('#ga-f-meldung'); if (m) m.textContent = t; }
  document.addEventListener('keydown', function (e) {
    var f = $('#ga-fenster');
    if (f.hidden) return;
    if (e.key === 'Escape') return fensterZu();
    if (e.key !== 'Tab') return;
    var l = f.querySelectorAll('button:not([disabled]),input,textarea,a[href]');
    if (!l.length) return;
    if (e.shiftKey && document.activeElement === l[0]) { e.preventDefault(); l[l.length - 1].focus(); }
    else if (!e.shiftKey && document.activeElement === l[l.length - 1]) { e.preventDefault(); l[0].focus(); }
  });
  $('#ga-fenster').addEventListener('mousedown', function (e) { if (e.target === this) fensterZu(); });

  /* ---------- Vorher, nachher ---------- */
  function marke(a, b) {          // markiert in zwei Texten das Stück, das sich unterscheidet
    a = String(a == null ? '' : a); b = String(b == null ? '' : b);
    var v = 0, n = 0, max = Math.min(a.length, b.length);
    while (v < max && a[v] === b[v]) v++;
    while (n < max - v && a[a.length - 1 - n] === b[b.length - 1 - n]) n++;
    while (v > 0 && /\S/.test(a[v - 1])) v--;      // am Wortanfang beginnen
    function teil(t) {
      var ende = t.length - n, vor = t.slice(Math.max(0, v - 160), v), mitte = t.slice(v, ende), nach = t.slice(ende, ende + 160);
      return h('div', { class: 'kuhle ga-text' }, v > 160 ? '… ' : '', vor, mitte ? h('mark', {}, mitte.length > 1200 ? mitte.slice(0, 1200) + ' …' : mitte) : null, nach, t.length - ende > 160 ? ' …' : '');
    }
    return [teil(a), teil(b)];
  }
  function unterschied(a, b) {
    var aus = [], k;
    function stelle(wo, wie, vorher, nachher) { aus.push({ wo: wo, wie: wie, vorher: vorher, nachher: nachher }); }
    function liste(ka, kb, name, text) {
      var ia = {}, ib = {};
      (ka || []).forEach(function (x) { ia[x.id] = x; });
      (kb || []).forEach(function (x) { ib[x.id] = x; });
      (kb || []).forEach(function (x) { if (!ia[x.id]) stelle(name(x), 'neu', '', text(x)); else if (!gleich(ia[x.id], x) && text(ia[x.id]) !== text(x)) stelle(name(x), 'geändert', text(ia[x.id]), text(x)); });
      (ka || []).forEach(function (x) { if (!ib[x.id]) stelle(name(x), 'entfernt', text(x), ''); });
    }
    liste(a.team, b.team, function (x) { return 'Vom Team: ' + x.frage; }, function (x) { return 'Frage: ' + x.frage + '\nAntwort: ' + x.antwort; });
    liste(a.wissen, b.wissen, function (x) { return 'Eingelesen: ' + x.titel; }, function (x) { return x.titel + '\n' + x.text; });
    var hNamen = { name: 'Name des Hauses', ort: 'Ort', tel: 'Telefon', mail: 'E-Mail', adresse: 'Adresse', zeiten: 'Erreichbarkeit', fahrplan: 'Fahrplan', buchung: 'Adresse der Buchung', modell: 'Modell der KI',
      sprachen: 'Sprachen des Chats', absender: 'Absender je Anliegen', orte: 'Orte für das Wetter' };
    for (k in hNamen) if (!gleich((a.haus || {})[k], (b.haus || {})[k])) stelle('Angabe des Hauses: ' + hNamen[k], 'geändert', lesbar((a.haus || {})[k]), lesbar((b.haus || {})[k]));
    var eNamen = { obergrenze_monat_usd: 'Obergrenze je Monat (USD)', besucher_10min: 'Fragen je Gespräch in 10 Minuten', besucher_tag: 'Fragen je Gespräch am Tag', gesamt_tag: 'Fragen gesamt am Tag',
      anfrage_tag: 'Antwortentwürfe der KI am Tag', aufbewahrung_monate: 'Aufbewahrung in Monaten' };
    for (k in eNamen) if (!gleich((a.einstellungen || {})[k], (b.einstellungen || {})[k])) stelle('Einstellung: ' + eNamen[k], 'geändert', lesbar((a.einstellungen || {})[k]), lesbar((b.einstellungen || {})[k]));
    [['karten', 'Startfragen im Chat'], ['muster', 'Musterantworten'], ['vorlagen', 'Mail-Vorlagen des Hauses'], ['tal_hinweis', 'Hinweis zum Talwissen']].forEach(function (p) {
      if (!gleich(a[p[0]], b[p[0]])) stelle(p[1], 'geändert', lesbar(a[p[0]]), lesbar(b[p[0]]));
    });
    return aus;
  }
  function lesbar(x) { return x == null || x === '' ? 'offen' : typeof x === 'string' ? x : typeof x === 'number' ? String(x) : JSON.stringify(x, null, 1); }
  function vnListe(stellen, links, rechts) {
    return h('div', { class: 'ga-vn' }, stellen.map(function (s) {
      var paar = marke(s.vorher, s.nachher);
      return h('div', { class: 'ga-vn__stelle' },
        h('div', { class: 'ga-eintrag__kopf' }, h('b', {}, s.wo), h('span', { class: 'ga-schild' }, s.wie)),
        h('div', { class: 'ga-vn__paar' }, h('div', {}, h('span', { class: 'angabe' }, links || 'Vorher'), s.vorher ? paar[0] : h('div', { class: 'kuhle ga-text ga-leise' }, 'gab es nicht')),
          h('div', {}, h('span', { class: 'angabe' }, rechts || 'Nachher'), s.nachher ? paar[1] : h('div', { class: 'kuhle ga-text ga-leise' }, 'entfällt'))));
    }));
  }
  function zeigeUnterschied(vorher, nachher, eins, zwei) {
    var st = unterschied(vorher, nachher);
    fenster(eins || 'Vorher,', zwei || 'nachher', st.length ? vnListe(st) : h('p', {}, 'Die beiden Stände sind gleich.'), [kn('Schliessen', fensterZu, { ohne: true })]);
  }

  /* ---------- Wissen speichern: immer als Entwurf, mit Kennung, mit Quittung ---------- */
  function Kollision(andere) { this.andere = andere; }
  function speichere(tun, was, mehr) {
    mehr = mehr || {};
    var vorher = kopie(doc()), hatteEntwurf = !!S.stand.entwurf, neu = kopie(vorher);
    try { tun(neu, !!mehr.zwang); } catch (e) { if (e instanceof Kollision) return kollision(tun, was, mehr, e.andere); throw e; }
    if (gleich(neu, vorher)) { quittung('Nichts geändert, nichts gespeichert.', mehr.gleichText || ''); return Promise.resolve(false); }
    return eigen('speichern', { daten: neu, erwartet: kennung(), wer: wer() }).then(function (st) {
      S.stand = st;
      var meine = st.kennung_entwurf, danach = mehr.nach ? mehr.nach() : null;
      return Promise.resolve(danach).then(function () {
        rahmen(); zeichne();
        quittung(was, 'Als Entwurf gespeichert. Der Chat arbeitet damit, sobald Sie veröffentlichen.', [
          ['Vorher, nachher', function () { zeigeUnterschied(vorher, neu); }],
          ['Rückgängig', function () { rueckgaengig(vorher, hatteEntwurf, mehr.zurueck, meine); }]]);
        return true;
      });
    }).catch(function (e) {
      if (e.status === 409) return konflikt(tun, was, mehr);
      fehl(e); return false;
    });
  }
  function rueckgaengig(vorher, hatteEntwurf, zurueck, meine) {
    eigen('stand').then(function (jetzt) {      // nur zurücknehmen, wenn seither niemand anderes gespeichert hat
      if (jetzt.kennung_entwurf !== meine) { S.stand = jetzt; rahmen(); zeichne(); var f = new Error('anders'); f.status = 409; throw f; }
      return hatteEntwurf ? eigen('speichern', { daten: vorher, erwartet: meine, wer: wer() }) : eigen('verwerfen', { erwartet: meine, wer: wer() });
    }).then(function (st) {
      S.stand = st;
      return zurueck ? zurueck() : null;
    }).then(function () { rahmen(); zeichne(); quittung('Rückgängig gemacht', 'Der Stand ist wieder wie vor der Änderung.'); })
      .catch(function (e) { if (e.status === 409) quittung('Nicht rückgängig gemacht', 'Inzwischen hat jemand anderes gespeichert. Bitte die Änderung von Hand zurücknehmen.', [], { fehl: true }); else fehl(e); });
  }
  function konflikt(tun, was, mehr) {      // jemand anderes hat inzwischen gespeichert: nichts wird überschrieben
    var meiner = kopie(doc());
    return eigen('stand').then(function (st) {
      var fremd = unterschied(meiner, st.entwurf || st.live);
      S.stand = st; rahmen(); zeichne();
      return new Promise(function (fertig) {
        fenster('Jemand anderes', 'hat gespeichert.', [
          h('p', { id: 'ga-konflikt' }, 'Während Sie gearbeitet haben, wurde der Stand geändert. Ihre Änderung («' + was + '») ist noch nicht gespeichert, und nichts wurde überschrieben.'),
          fremd.length ? [h('p', { class: 'angabe' }, 'Das ist inzwischen dazugekommen'), vnListe(fremd, 'Ihr Stand', 'Neuer Stand')] : null],
          [link('Meine Änderung verwerfen', function () { fensterZu(); quittung('Verworfen', 'Ihre Änderung wurde nicht gespeichert.'); fertig(false); }),
            kn('Dazunehmen', function () { fensterZu(); fertig(speichere(tun, was, mehr)); }, { dunkel: true, id: 'ga-f-dazu' })]);
      });
    }).catch(function (e) { fehl(e); return false; });
  }
  function kollision(tun, was, mehr, andere) {   // derselbe Eintrag wurde von jemand anderem geändert oder entfernt
    return new Promise(function (fertig) {
      fenster('Derselbe Eintrag', 'wurde geändert.', [
        h('p', {}, andere ? 'Jemand anderes hat genau diesen Eintrag inzwischen geändert. So steht er jetzt da:' : 'Jemand anderes hat diesen Eintrag inzwischen entfernt.'),
        andere ? h('div', { class: 'kuhle ga-text' }, 'Frage: ' + andere.frage + '\nAntwort: ' + andere.antwort) : null],
        [link('Die andere Fassung behalten', function () { fensterZu(); fertig(false); }),
          andere ? kn('Meine Fassung', function () { fensterZu(); mehr.zwang = true; fertig(speichere(tun, was, mehr)); }, { dunkel: true }) : null]);
    });
  }

  /* ---------- Rahmen: Kopf, Hinweise, Bereiche, Entwurfs-Leiste ---------- */
  function rahmen() {
    var u = S.ue, n = u.anfragen_neu, name = Welt.name(W);
    $('#ga-haus').textContent = S.haus;
    $('#ga-wer').textContent = wer();
    document.title = (n ? '(' + n + ') ' : '') + name + ' · ' + S.haus;

    var band = $('#ga-wartet');
    band.textContent = ''; band.hidden = !n;
    if (n) {
      var a = u.wartet[0] || {};
      band.appendChild(h('div', {}, h('b', {}, n === 1 ? 'Eine Anfrage wartet' : n + ' Anfragen warten'),
        h('span', { class: 'angabe' }, [(ART[a.art] || 'Anfrage'), a.name || 'ohne Namen', 'seit ' + zeit(a.zeit)].join(' · '))));
      band.appendChild(kn('Öffnen', function () { gehe('eingang', a.id); }, { dunkel: true, id: 'ga-wartet-kn' }));
    }
    var ki = $('#ga-ki'), lage = u.ki || {};
    ki.textContent = ''; ki.hidden = lage.stand === 'ok';
    if (lage.stand !== 'ok') {
      ki.appendChild(h('div', {}, h('b', {}, lage.stand === 'probe' ? 'Probe-Antworten' : 'Die KI antwortet gerade nicht'), h('span', {}, lage.text)));
      if (lage.art === 'echt' && lage.stand !== 'obergrenze') ki.appendChild(kn('Erneut prüfen', kiPruefen, { id: 'ga-ki-kn' }));
    }

    var rand = $('#ga-rand'), ort = $('#ga-nav-ort'), offen = rand.classList.contains('ga-offen'), zahl = { eingang: n, gefragt: u.ohne_antwort };
    $('#ga-zurueck').hidden = S.ansicht === 'start';
    ort.textContent = '';
    ort.appendChild(h('button', { class: 'ga-rand__auf', type: 'button', 'aria-expanded': String(offen), klick: function () { rand.classList.toggle('ga-offen'); this.setAttribute('aria-expanded', String(rand.classList.contains('ga-offen'))); } },
      h('span', {}, h('span', { class: 'angabe' }, 'Bereich '), (BEREICHE.filter(function (b) { return b[0] === S.ansicht; })[0] || BEREICHE[0])[1]), h('span', { 'aria-hidden': 'true', html: WINKEL })));
    ort.appendChild(h('nav', { class: 'ga-nav', 'aria-label': 'Bereiche' }, BEREICHE.map(function (b) {
      return h('button', { type: 'button', 'data-gehe': b[0], 'aria-current': S.ansicht === b[0] ? 'true' : null, klick: function () { gehe(b[0]); } }, h('span', {}, b[1]), zahl[b[0]] ? h('i', {}, zahl[b[0]]) : null);
    })));

    var leiste = $('#ga-leiste'), st = S.stand.offen ? unterschied(S.stand.live, S.stand.entwurf) : [];
    leiste.textContent = '';
    if (S.stand.offen) {
      leiste.appendChild(h('div', { class: 'ga-leiste__t' }, h('span', { class: 'marke' }, 'Entwurf'), h('span', {}, h('b', {}, st.length ? mal(st.length, 'Eine Änderung', 'Änderungen') : 'Änderungen'), ' am Wissen, noch nicht veröffentlicht')));
      leiste.appendChild(h('div', { class: 'ga-leiste__kn' }, kn('Vorher, nachher', function () { veroeffentlichenFenster(); }, { id: 'ga-l-vn' }), kn('Veröffentlichen', function () { veroeffentlichenFenster(); }, { id: 'ga-l-los' })));
    } else {
      leiste.appendChild(h('div', { class: 'ga-leiste__t' }, h('span', {}, h('b', {}, 'Alles veröffentlicht.'), ' Der Chat arbeitet mit dem Wissen, das Sie hier sehen.')));
      leiste.appendChild(h('div', { class: 'ga-leiste__kn' }, kn('Veröffentlichen', function () {}, { id: 'ga-l-los', aus: true })));
    }
  }
  function gehe(ziel, wahl_, zurueck) {
    if (!zurueck && S.ansicht !== ziel) { S.spur.push(S.ansicht); if (S.spur.length > 30) S.spur.shift(); }
    S.auftritt = S.ansicht !== ziel;
    S.ansicht = ziel; S.wahl = wahl_ || '';
    if (ziel === 'verlauf') S.verlauf = null;
    var marke = ziel + (S.wahl ? '/' + S.wahl : '');
    if (location.hash.slice(1) !== marke) history.replaceState(null, '', location.pathname + location.search + '#' + marke);
    $('#ga-rand').classList.remove('ga-offen');
    rahmen(); zeichne();
    window.scrollTo(0, 0);
    $('#ga-haupt').focus({ preventScroll: true });
    ladeBetrieb().then(function () { rahmen(); if (S.ansicht === ziel && ruhig()) zeichne(); }).catch(function () { /* der alte Stand bleibt stehen */ });
  }
  function ruhig() { return $('#ga-fenster').hidden && !document.querySelector('#ga-haupt textarea:focus, #ga-haupt input:focus') && !S.chat.laeuft && !Object.keys(S.schreibt).length; }
  $('#ga-zurueck').addEventListener('click', function () { gehe(S.spur.length ? S.spur.pop() : 'start', '', true); });
  function ladeBetrieb() {
    return eigen('betrieb').then(function (d) { S.betrieb = d; S.ue = d.ueberblick; });
  }
  function kiPruefen() {
    eigen('ki-pruefen', { wer: wer() }).then(function (d) {
      S.ue = d.ueberblick; rahmen(); if (S.ansicht === 'betrieb') ladeBetrieb().then(zeichne);
      quittung(S.ue.ki.stand === 'ok' ? 'Die KI antwortet wieder' : 'Die KI antwortet noch nicht', S.ue.ki.stand === 'ok' ? '' : S.ue.ki.text);
    }).catch(fehl);
  }

  /* ---------- Veröffentlichen ---------- */
  function veroeffentlichenFenster() {
    eigen('stand').then(function (st) {
      S.stand = st; rahmen();
      if (!st.offen) { quittung('Nichts zu veröffentlichen', 'Der Entwurf ist derselbe wie der veröffentlichte Stand.'); return zeichne(); }
      var stellen = unterschied(st.live, st.entwurf), gesehen = st.kennung_entwurf, sicher = false;
      var verwerfen = link('Entwurf verwerfen', function () {
        if (!sicher) { sicher = true; verwerfen.textContent = 'Wirklich verwerfen? Noch einmal drücken.'; return; }
        var gefallen = (st.entwurf.team || []).filter(function (x) { return x.aus && !(st.live.team || []).some(function (y) { return y.id === x.id; }); });
        eigen('verwerfen', { erwartet: gesehen, wer: wer() }).then(function (neu) {
          S.stand = neu; fensterZu();
          return Promise.all(gefallen.map(function (x) { return eigen('frage', { id: x.aus, erledigt: false, wer: wer() }).catch(function () {}); }));
        }).then(ladeBetrieb).then(function () { rahmen(); zeichne(); quittung('Entwurf verworfen', 'Es gilt wieder der veröffentlichte Stand.'); }).catch(fehl);
      }, 'ga-f-verwerfen');
      fenster('Vorher,', 'nachher', [
        h('p', {}, 'Das ändert sich für die Gäste, sobald Sie veröffentlichen: ' + mal(stellen.length, 'eine Stelle', 'Stellen') + '.'),
        vnListe(stellen, 'Heute online', 'Nach dem Veröffentlichen'),
        feld('Notiz für den Verlauf (freiwillig)', 'ga-f-notiz', '', { platz: 'Zum Beispiel: Antwort zum Parkplatz nachgetragen', max: 200 })],
        [verwerfen, kn('Veröffentlichen', function () {
          eigen('veroeffentlichen', { erwartet: gesehen, wer: wer(), notiz: $('#ga-f-notiz').value.trim() }).then(function (neu) {
            S.stand = neu; S.verlauf = null; fensterZu(); rahmen(); zeichne();
            quittung('Veröffentlicht', 'Der Chat antwortet ab jetzt mit diesem Stand.', [['Im Verlauf ansehen', function () { gehe('verlauf'); }]]);
          }).catch(function (e) {
            if (e.status !== 409) return fensterMeldung(e.message);
            fensterZu();
            eigen('stand').then(function (jetzt) { S.stand = jetzt; rahmen(); zeichne(); }).catch(function () {});
            quittung('Der Entwurf hat sich geändert', 'Jemand anderes hat inzwischen gespeichert. Bitte sehen Sie sich die Änderungen noch einmal an.', [['Ansehen', veroeffentlichenFenster]], { fehl: true });
          });
        }, { dunkel: true, id: 'ga-f-los' })]);
    }).catch(fehl);
  }

  /* ---------- Ansichten ---------- */
  function zeichne() {
    var m = $('#ga-haupt'), bau = { start: start, eingang: eingang, gefragt: gefragt, wissen: wissen, probe: probe, auswertung: auswertung, verlauf: verlauf, betrieb: betrieb }[S.ansicht] || start;
    var kommt = S.auftritt;
    m.textContent = '';
    haenge(m, bau());
    m.classList.toggle('ga-auftritt', kommt);      // nur beim Wechsel des Bereichs gleiten die Stücke herein, nicht bei jeder Änderung
    if (kommt) {
      Array.prototype.forEach.call(m.children, function (e, i) { e.style.setProperty('--i', i); });
      Array.prototype.forEach.call(m.querySelectorAll('.ga-k3'), function (e, i) { e.style.setProperty('--i', i); });
    }
    S.auftritt = false;
  }

  function start() {
    var u = S.ue, st = new Date().getHours(), gruss = st >= 5 && st < 11 ? 'Guten Morgen.' : st >= 11 && st < 18 ? 'Guten Tag.' : 'Guten Abend.';
    var neueste = S.betrieb.anfragen.slice(0, 3), offen = (doc().eingelesen || {}).offen || [], kacheln = (S.kleid || {}).kacheln || {};
    if (doc().einstellungen.obergrenze_monat_usd == null) offen = offen.concat(['Für die Kosten der KI ist keine Obergrenze je Monat gesetzt (unter «Kosten und Schutz»).']);
    function lage(kap, zahl, kopf, satz, ziel, foto, w) {
      return h('button', { class: 'ga-k3', type: 'button', 'data-lage': ziel, klick: function () { if (w) S[w[0]] = w[1]; gehe(ziel); } },
        h('span', { class: 'ga-k3__bild' }, bild(foto) ? h('img', { src: bild(foto), alt: '', decoding: 'async' }) : null, h('span', { class: 'kap ga-k3__kap' }, kap), zahl ? h('span', { class: 'ga-k3__zahl' }, zahl) : null),
        h('span', { class: 'ga-k3__text' }, h('span', { class: 't-zwischen' }, kopf), h('span', {}, satz)));
    }
    return [titel(Welt.name(W) + ' · ' + S.haus, gruss, 'Wer hat geschrieben?',
      'Hier sehen Sie, was Gäste die Rezeption im Chat fragen. Möchte jemand ein Zimmer, einen Tisch, eine Feier oder eine Tagung, liegt die Anfrage im Eingang, mit einem Entwurf für Ihre Antwort. Verschickt wird nur, was Sie selbst schicken.', null, true),
      h('div', { class: 'ga-lage' },
        lage('Eingang', u.anfragen_neu || '', u.anfragen_neu ? mal(u.anfragen_neu, 'Eine neue Anfrage', 'neue Anfragen') : u.anfragen_offen ? mal(u.anfragen_offen, 'Eine Anfrage offen', 'Anfragen offen') : 'Nichts Neues',
          u.anfragen_gesamt ? mal(u.anfragen_gesamt, 'Eine Anfrage', 'Anfragen') + ' aus dem Chat bisher.' : 'Sobald ein Gast im Chat etwas anfragt, steht es hier.', 'eingang', kacheln.eingang),
        lage('Ohne Antwort', u.ohne_antwort || '', u.ohne_antwort ? mal(u.ohne_antwort, 'Eine Frage', 'Fragen') : 'Keine Lücke',
          u.ohne_antwort ? 'Dazu stand nichts im Wissen. Einmal nachtragen genügt.' : 'Jede Frage hatte eine Antwort.', 'gefragt', kacheln.gefragt, ['gefragt', 'luecke']),
        lage('Wissen', '', S.stand.offen ? 'Entwurf liegt bereit' : 'Veröffentlicht', mal((doc().team || []).length, 'Eine Antwort', 'Antworten') + ' vom Team, ' + (doc().wissen || []).length + ' Abschnitte aus Website und Unterlagen.', 'wissen', kacheln.wissen)),
      zw('Zuletzt', 'angefragt'),
      neueste.length ? h('div', { class: 'ga-anfragen' }, neueste.map(function (a) { return anfrageKarte(a, false); }))
        : leer('Der Eingang ist leer.', 'Fragt ein Gast im Chat nach einem Zimmer, einem Tisch, einer Feier oder einer Tagung und nennt Name und Kontakt, liegt die Anfrage hier. Im Probe-Chat können Sie es ausprobieren.',
          kn('Zum Probe-Chat', function () { gehe('probe'); })),
      offen.length ? [zw('Noch', 'offen'), h('ul', { class: 'liste' }, offen.map(function (t) { return h('li', {}, h('span', {}, t), h('span', {}, 'offen')); }))] : null];
  }

  /* --- Eingang --- */
  function anfrageKarte(a, mitWahl) {
    var stand_ = a.status === 'erledigt' ? 'Erledigt' : a.entwurf ? 'Antwortentwurf bereit' : 'Gelesen';
    return h('button', { class: 'platte' + (a.status === 'neu' ? ' ga-neu' : ''), type: 'button', 'data-anfrage': a.id, 'aria-current': mitWahl && S.wahl === a.id ? 'true' : null, klick: function () { gehe('eingang', a.id); } },
      h('span', { class: 'ga-eintrag__kopf' }, h('b', {}, a.name || 'Ohne Namen'), h('span', { class: 'angabe' }, kurzZeit(a.zeit))),
      h('span', { class: 'ga-anfrage__vorschau' }, a.anliegen),
      h('span', { class: 'ga-reihe ga-reihe--eng' }, h('span', { class: 'ga-schild' }, ART[a.art] || a.art), a.status === 'neu' ? h('span', { class: 'ga-schild ga-schild--voll' }, 'Neu') : null,
        a.herkunft === 'beispiel' ? h('span', { class: 'ga-schild' }, 'Beispiel') : null,
        h('span', { class: 'angabe' }, [a.status === 'neu' ? '' : stand_, a.personen ? a.personen + ' Personen' : '', SPRACHE[a.sprache] && a.sprache !== 'de' ? SPRACHE[a.sprache] : '', a.herkunft === 'probe' ? 'Probe-Chat' : ''].filter(Boolean).join(' · '))));
  }
  function eingang() {
    var alle = S.betrieb.anfragen, l = alle.filter(function (a) { return S.eingang === 'alle' || (S.eingang === 'erledigt') === (a.status === 'erledigt'); });
    if (S.wahl && !alle.some(function (a) { return a.id === S.wahl; })) S.wahl = '';
    if (S.wahl && !l.some(function (a) { return a.id === S.wahl; })) { S.eingang = 'alle'; l = alle; }
    var a = l.filter(function (x) { return x.id === S.wahl; })[0];      // geöffnet wird nur, was jemand anklickt: eine neue Anfrage bleibt neu, bis sie gelesen ist
    if (a && a.status === 'neu') gelesen(a);
    return [titel('Eingang', 'Anfragen', 'aus dem Chat.', 'Zimmer, Tische, Feiern und Tagungen, die Gäste im Chat angefragt haben. Zu jeder Anfrage gibt es einen Antwortentwurf. Sie lesen, ändern und schicken selbst: Hier wird nichts verschickt.'),
      h('div', { class: 'ga-reihe ga-reihe--auseinander' },
        wahl('Auswahl', [['offen', 'Offen' + (alle.filter(function (x) { return x.status !== 'erledigt'; }).length ? ' · ' + alle.filter(function (x) { return x.status !== 'erledigt'; }).length : '')], ['erledigt', 'Erledigt'], ['alle', 'Alle']], S.eingang, function (w) { S.eingang = w; S.wahl = ''; zeichne(); }),
        S.ue.beispiele ? link('Beispiele entfernen', function () { beispiele('entfernen'); }, 'ga-bsp-weg') : S.beispieleDa ? link('Beispiele laden', function () { beispiele('laden'); }, 'ga-bsp-laden') : null),
      S.ue.beispiele ? h('p', { class: 'angabe', id: 'ga-bsp-hinweis' }, 'Anfragen mit dem Schild «Beispiel» sind erfunden. Sie zeigen, wie der Eingang im Betrieb aussieht, und zählen nicht als Gäste.') : null,
      l.length ? h('div', { class: 'ga-eingang' }, h('div', { class: 'ga-anfragen' }, l.map(function (x) { return anfrageKarte(x, true); })), a ? h('div', { class: 'ga-spalte', id: 'ga-detail' }, anfrageDetail(a))
        : h('div', { class: 'platte ga-leer', id: 'ga-detail-leer' }, h('p', { class: 't-zwischen' }, mal(l.length, 'Eine Anfrage', 'Anfragen') + '.'), h('p', {}, 'Wählen Sie eine Anfrage aus der Liste. Sie sehen dann die Angaben, das Gespräch im Chat und den Antwortentwurf.')))
        : leer(S.eingang === 'erledigt' ? 'Noch nichts erledigt.' : 'Der Eingang ist leer.', 'Sobald ein Gast im Chat etwas anfragt und Name und Kontakt nennt, steht die Anfrage hier.', kn('Zum Probe-Chat', function () { gehe('probe'); }))];
  }
  function beispiele(tun) {
    eigen('beispiele', { tun: tun, wer: wer() }).then(function (d) {
      S.wahl = '';
      return ladeBetrieb().then(function () { rahmen(); zeichne(); quittung(tun === 'laden' ? 'Beispiele geladen' : 'Beispiele entfernt', mal(d.anzahl, 'Ein Eintrag', 'Einträge') + (tun === 'laden' ? ' mit dem Schild «Beispiel» im Eingang.' : ' endgültig gelöscht.')); });
    }).catch(fehl);
  }
  function gelesen(a) {      // geöffnet heisst gelesen: der Hinweis «wartet» verschwindet
    a.status = 'gelesen';
    eigen('anfrage', { id: a.id, status: 'gelesen', wer: wer() }).then(function (d) { uebernimm(d.anfrage); S.ue = d.ueberblick; rahmen(); }).catch(function () { a.status = 'neu'; });
  }
  function uebernimm(a) {       // dasselbe Objekt behalten: offene Knöpfe zeigen darauf und brauchen die neue Zählung «v»
    var x = S.betrieb.anfragen.filter(function (y) { return y.id === a.id; })[0], k;
    if (!x) return S.betrieb.anfragen.unshift(a);
    for (k in x) delete x[k];
    for (k in a) x[k] = a[k];
  }
  function kontakt(k) {
    var t = String(k || '').trim();
    if (/^[\w.+-]+@[\w-]+\.[\w.-]+$/.test(t)) return h('a', { href: 'mailto:' + t }, t);
    if (/^[+\d][\d\s/().-]{6,}$/.test(t)) return h('a', { href: 'tel:' + t.replace(/[^\d+]/g, '') }, t);
    return t || 'offen';
  }
  function anfrageDetail(a) {
    var e = a.entwurf, laeuft = S.schreibt[a.id], kiDa = S.ue.ki.art === 'echt' && S.ue.ki.stand !== 'obergrenze' && S.ue.ki.stand !== 'guthaben-leer' && S.ue.ki.stand !== 'schluessel-ungueltig';
    var angaben = [['Anliegen', ART[a.art] || a.art], ['Name', a.name || 'nicht genannt'], ['Kontakt', kontakt(a.kontakt)], ['Datum', a.datum || 'nicht genannt'], ['Personen', a.personen || 'nicht genannt'],
      ['Sprache', SPRACHE[a.sprache] || a.sprache], ['Eingegangen', zeit(a.zeit)], ['Herkunft', HERKUNFT[a.herkunft] || 'Gast']];
    var zeigt = S.offenText['g' + a.id];
    var kopf = h('section', { class: 'platte ga-eintrag' },
      h('div', { class: 'ga-eintrag__kopf' }, h('h2', { class: 't-zwischen' }, a.name || 'Ohne Namen'),
        h('div', { class: 'ga-reihe' }, link('Löschen', function () { loeschenFenster(a); }, 'ga-a-weg'),
          kn(a.status === 'erledigt' ? 'Wieder offen' : 'Erledigt', function () { setzeStatus(a, a.status === 'erledigt' ? 'gelesen' : 'erledigt'); }, { id: 'ga-a-status' }))),
      h('div', { class: 'ga-angaben' }, angaben.map(function (p) { return h('div', {}, h('span', { class: 'angabe' }, p[0]), h('b', {}, p[1])); })),
      h('p', {}, a.anliegen),
      h('button', { class: 'ga-auf', type: 'button', 'aria-expanded': String(!!zeigt), klick: function () { S.offenText['g' + a.id] = !zeigt; zeichne(); } }, zeigt ? 'Gespräch im Chat schliessen' : 'Das Gespräch im Chat ansehen'),
      zeigt ? h('div', { class: 'ga-gespraech' }, (a.verlauf || []).map(function (v) { return h('div', { class: 'ga-blase ' + (v.rolle === 'user' ? 'ga-blase--gast' : 'ga-blase--haus') }, v.text); })) : null);
    var teil;
    if (laeuft) {
      teil = [h('p', {}, h('b', {}, 'Der Antwortentwurf wird geschrieben.')), h('p', { class: 'ga-leise' }, 'Die KI liest die Anfrage, die Mail-Vorlage des Hauses und das Wissen. Das dauert etwa zwanzig Sekunden.')];
    } else if (e) {
      var klammern = (e.text.match(/\[[^\]]+\]/g) || []).length;
      teil = [
        h('p', { class: 'angabe' }, [e.art === 'ki' ? 'Von der KI geschrieben' : e.art === 'probelauf' ? 'Von der KI geschrieben, im Probelauf des Projekts' : 'Gerüst ohne KI', e.vorlage ? 'Grundlage: Mail-Vorlage ' + e.vorlage : 'ohne Mail-Vorlage des Hauses', 'Absender: ' + (e.absender || 'offen'),
          e.geaendert ? 'geändert ' + zeit(e.geaendert) + (e.geaendert_von ? ' von ' + e.geaendert_von : '') : 'geschrieben ' + zeit(e.zeit)].join(' · ')),
        feld('Betreff', 'ga-e-betreff', e.betreff, { max: 300 }),
        feld('Text' + (klammern ? ' · ' + mal(klammern, 'eine Stelle', 'Stellen') + ' in [Klammern] klären' : ''), 'ga-e-text', e.text, { lang: true, zeilen: 16, max: 12000 }),
        e.team ? h('div', { class: 'kuhle ga-text' }, h('b', {}, 'Nur für das Team'), '\n' + e.team) : null,
        h('div', { class: 'ga-reihe' },
          kn('Kopieren', function () { mitEntwurf(a, 'kopieren'); }, { dunkel: true, id: 'ga-e-kopieren' }),
          /@/.test(a.kontakt || '') ? kn('Im Mailprogramm', function () { mitEntwurf(a, 'mail'); }, { id: 'ga-e-mail' }) : null,
          kn('Änderung sichern', function () { mitEntwurf(a, 'sichern'); }, { id: 'ga-e-sichern' }),
          link('Neu schreiben lassen', function () { neuSchreibenFenster(a); }, 'ga-e-neu')),
        h('p', { class: 'ga-leise' }, 'Verschickt wird hier nichts. Kopieren Sie den Text in Ihr Mailprogramm oder öffnen Sie ihn dort, klären Sie die Stellen in [Klammern] und schicken Sie selbst.')];
    } else {
      teil = [h('p', {}, kiDa ? 'Noch kein Antwortentwurf. Die KI schreibt ihn aus der Anfrage, der Mail-Vorlage des Hauses und dem Wissen. Jeder Entwurf kostet einen Aufruf der KI.'
        : 'Noch kein Antwortentwurf. Die KI ist gerade nicht angeschlossen: Sie bekommen ein Gerüst mit den Angaben aus der Anfrage und füllen den Rest selbst.'),
      kiDa ? feld('Hinweis für den Entwurf (freiwillig)', 'ga-e-hinweis', '', { platz: 'Zum Beispiel: An dem Tag ist noch Platz, Angebot mit Apéro', max: 2000 }) : null,
      h('div', { class: 'ga-reihe' }, kn(kiDa ? 'Entwurf schreiben' : 'Gerüst anlegen', function () { schreibe(a, ($('#ga-e-hinweis') || {}).value || '', !kiDa); }, { dunkel: true, id: 'ga-e-los' }),
        kiDa ? link('Gerüst ohne KI', function () { schreibe(a, '', true); }, 'ga-e-geruest') : null)];
    }
    return [kopf, h('section', { class: 'platte ga-eintrag' }, h('div', { class: 'ga-eintrag__kopf' }, h('h2', { class: 't-zwischen' }, 'Antwort an den Gast')), teil)];
  }
  function schreibe(a, hinweis, ohneKi) {
    S.schreibt[a.id] = true; zeichne();
    eigen('entwurf', { id: a.id, hinweis: hinweis, ohne_ki: ohneKi, wer: wer() }).then(function (d) {
      uebernimm(d.anfrage); S.ue = d.ueberblick;
      quittung(d.anfrage.entwurf.art === 'ki' ? 'Antwortentwurf geschrieben' : 'Gerüst angelegt', d.hinweis || 'Bitte lesen, die Stellen in [Klammern] klären und selbst schicken.');
    }).catch(fehl).then(function () { delete S.schreibt[a.id]; rahmen(); zeichne(); });
  }
  function neuSchreibenFenster(a) {
    fenster('Neu', 'schreiben lassen.', [h('p', {}, 'Der jetzige Antwortentwurf wird ersetzt, auch Ihre Änderungen daran. Möchten Sie der KI etwas mitgeben?'),
      feld('Hinweis (freiwillig)', 'ga-f-hinweis', '', { platz: 'Zum Beispiel: kürzer, mit dem Preis der Pauschale', max: 2000 })],
    [link('Abbrechen', fensterZu), kn('Neu schreiben', function () { var t = $('#ga-f-hinweis').value; fensterZu(); schreibe(a, t, false); }, { dunkel: true, id: 'ga-f-los' })]);
  }
  function mitEntwurf(a, was) {
    var betreff = $('#ga-e-betreff').value, text = $('#ga-e-text').value, e = a.entwurf, anders = betreff !== e.betreff || text !== e.text;
    function weiter() {
      if (was === 'kopieren') {
        var roh = 'Betreff: ' + betreff + '\n\n' + text;
        return (navigator.clipboard ? navigator.clipboard.writeText(roh) : Promise.reject()).then(function () { quittung('Kopiert', 'Betreff und Text liegen in der Zwischenablage' + (anders ? ', Ihre Änderung ist gesichert.' : '.')); },
          function () { quittung('Nicht kopiert', 'Der Browser hat die Zwischenablage nicht freigegeben. Markieren Sie den Text und kopieren Sie ihn von Hand.', [], { fehl: true }); });
      }
      if (was === 'mail') { location.href = 'mailto:' + encodeURIComponent(a.kontakt.trim()) + '?subject=' + encodeURIComponent(betreff) + '&body=' + encodeURIComponent(text); return quittung('Im Mailprogramm geöffnet', 'Dort prüfen und selbst schicken.'); }
      quittung(anders ? 'Gesichert' : 'Nichts geändert, nichts gespeichert.', anders ? 'Ihre Änderung am Antwortentwurf ist gespeichert.' : '');
    }
    if (!anders) return weiter();
    sichere(a, { betreff: betreff, text: text }, weiter);
  }
  function sichere(a, was, danach) {
    var k = { id: a.id, v: a.v, wer: wer() }, n;
    for (n in was) k[n] = was[n];
    eigen('anfrage', k).then(function (d) { uebernimm(d.anfrage); S.ue = d.ueberblick; rahmen(); zeichne(); if (danach) danach(); }).catch(function (e) {
      if (e.status !== 409) return fehl(e);
      var andere = e.daten.anfrage;
      fenster('Jemand anderes', 'hat diese Anfrage geändert.', [h('p', {}, 'Ihre Änderung ist noch nicht gespeichert, und nichts wurde überschrieben. So steht die Anfrage jetzt da:'),
        h('div', { class: 'kuhle ga-text' }, 'Stand: ' + andere.status + (andere.entwurf ? '\nBetreff: ' + andere.entwurf.betreff + '\n\n' + andere.entwurf.text : ''))],
      [link('Die andere Fassung laden', function () { fensterZu(); uebernimm(andere); zeichne(); }),
        kn('Meine Fassung', function () { fensterZu(); a.v = andere.v; sichere(a, was, danach); }, { dunkel: true })]);
    });
  }
  function setzeStatus(a, status) {
    var vorher = a.status;
    sichere(a, { status: status }, function () {
      quittung(status === 'erledigt' ? 'Erledigt' : 'Wieder offen', 'Vorher: ' + (vorher === 'erledigt' ? 'erledigt' : 'offen') + '. Nachher: ' + (status === 'erledigt' ? 'erledigt' : 'offen') + '.',
        [['Rückgängig', function () { var jetzt = S.betrieb.anfragen.filter(function (x) { return x.id === a.id; })[0]; if (jetzt) sichere(jetzt, { status: vorher === 'neu' ? 'gelesen' : vorher }, function () { quittung('Rückgängig gemacht', ''); }); }]]);
    });
  }
  function loeschenFenster(a) {
    fenster('Anfrage', 'löschen?', h('p', {}, 'Die Anfrage von ' + (a.name || 'diesem Gast') + ' wird mit Antwortentwurf, Gespräch und den Fragen aus diesem Gespräch endgültig gelöscht. Das lässt sich nicht zurückholen. Richtig ist das, wenn der Gast es wünscht oder alles erledigt ist.'),
      [link('Abbrechen', fensterZu), kn('Endgültig löschen', function () {
        eigen('weg', { id: a.id, wer: wer() }).then(function (d) { fensterZu(); S.wahl = ''; return ladeBetrieb().then(function () { rahmen(); zeichne(); quittung('Gelöscht', mal(d.geloescht, 'Ein Eintrag', 'Einträge') + ' endgültig entfernt.'); }); }).catch(function (e) { fensterMeldung(e.message); });
      }, { dunkel: true, id: 'ga-f-los' })]);
  }

  /* --- Das wurde gefragt --- */
  function istLuecke(f) { return f.belegt === false && !f.erledigt; }
  function gefragt() {
    var alle = S.betrieb.fragen.filter(function (f) { return S.mitProben || f.herkunft === 'gast'; }), luecken = alle.filter(istLuecke);
    var l = S.gefragt === 'luecke' ? luecken : S.gefragt === 'erledigt' ? alle.filter(function (f) { return f.erledigt; }) : alle, gruppen = {}, reihe;
    l.forEach(function (f) { (gruppen[f.gruppe] = gruppen[f.gruppe] || []).push(f); });
    reihe = Object.keys(gruppen).sort(function (x, y) { return gruppen[y].filter(istLuecke).length - gruppen[x].filter(istLuecke).length || gruppen[y].length - gruppen[x].length; });
    function frage(f) {
      var auf = S.offenText['f' + f.id];
      return h('div', { class: 'platte ga-eintrag', 'data-frage': f.id },
        h('div', { class: 'ga-eintrag__kopf' }, h('span', { class: 'angabe' }, [zeit(f.zeit), SPRACHE[f.sprache] || f.sprache, HERKUNFT[f.herkunft] || '', f.anfrage ? 'wurde zur Anfrage' : '', f.buchung ? 'Weg zur Buchung gezeigt' : '',
          f.art === 'probe' ? 'Probe-Antwort' : '', f.mit_entwurf ? 'mit dem Entwurf geprobt' : ''].filter(Boolean).join(' · ')),
        f.belegt === false ? h('span', { class: 'ga-schild' }, f.erledigt ? 'nachgetragen oder abgehakt' : 'ohne Antwort') : f.art === 'ausfall' ? h('span', { class: 'ga-schild' }, 'KI hat nicht geantwortet') : f.thema === 'abgelehnt' ? h('span', { class: 'ga-schild' }, 'abgelehnt') : null),
        h('p', {}, h('b', {}, f.frage)),
        h('button', { class: 'ga-auf', type: 'button', 'aria-expanded': String(!!auf), klick: function () { S.offenText['f' + f.id] = !auf; zeichne(); } }, auf ? 'Antwort des Chats schliessen' : 'Antwort des Chats ansehen'),
        auf ? h('div', { class: 'kuhle ga-text' }, f.antwort) : null,
        istLuecke(f) ? h('div', { class: 'ga-reihe' }, kn('Antwort nachtragen', function () { nachtragenFenster({ frage: f.frage, antwort: '', aus: f.id }); }, { dunkel: true }),
          link('Ohne Antwort abhaken', function () { hake(f, true); })) : f.belegt === false && f.erledigt ? h('div', { class: 'ga-reihe' }, link('Wieder als offen zeigen', function () { hake(f, false); })) : null);
    }
    return [titel('Das wurde gefragt', 'Was Gäste', 'wissen wollen.', luecken.length ? mal(luecken.length, 'Eine Frage hatte', 'Fragen hatten') + ' keine Antwort, weil dazu nichts im Wissen des Hauses steht. Tragen Sie die Antwort einmal nach. Sobald Sie veröffentlichen, antwortet der Chat selbst, in jeder Sprache.'
      : 'Jede Frage an die Rezeption im Chat, nach Themen. Hat der Chat keine Antwort, steht die Frage hier zum Nachtragen.'),
    h('div', { class: 'platte ga-zahlen' }, [[alle.length, 'Fragen'], [luecken.length, 'ohne Antwort'], [(doc().team || []).length, 'vom Team nachgetragen'], [alle.filter(function (f) { return f.anfrage; }).length, 'wurden zur Anfrage']].map(function (z) {
      return h('div', {}, h('b', { class: 't-zwischen zahl' }, z[0]), h('span', { class: 'angabe' }, z[1])); })),
    h('div', { class: 'ga-reihe ga-reihe--auseinander' },
      wahl('Auswahl', [['luecke', 'Ohne Antwort' + (luecken.length ? ' · ' + luecken.length : '')], ['alle', 'Alle Fragen'], ['erledigt', 'Erledigt']], S.gefragt, function (w) { S.gefragt = w; zeichne(); }),
      wahl('Herkunft', [[true, 'Mit Proben'], [false, 'Nur Gäste']], S.mitProben, function (w) { S.mitProben = w; zeichne(); })),
    reihe.length ? reihe.map(function (g) {
      var n = gruppen[g].filter(istLuecke).length;
      return h('section', { class: 'ga-gruppe' }, h('header', {}, h('h2', { class: 't-zwischen' }, g), h('span', { class: 'angabe' }, mal(gruppen[g].length, 'eine Frage', 'Fragen') + (n ? ' · ' + n + ' ohne Antwort' : ''))), gruppen[g].map(frage));
    }) : leer(S.gefragt === 'luecke' ? 'Keine Lücke.' : 'Noch keine Frage.', S.gefragt === 'luecke' ? 'Jede Frage liess sich aus dem Wissen des Hauses beantworten.'
      : S.mitProben ? 'Sobald jemand die Rezeption im Chat fragt, steht es hier.' : 'Noch keine Frage von Gästen. Offen: Das Fenster für Gäste auf der Website ist noch nicht an dieses Werkzeug angeschlossen. Mit «Mit Proben» sehen Sie die Fragen aus dem Probe-Chat.',
    kn('Zum Probe-Chat', function () { gehe('probe'); }))];
  }
  function hake(f, erledigt) {
    eigen('frage', { id: f.id, erledigt: erledigt, wer: wer() }).then(function (d) {
      f.erledigt = erledigt; S.ue = d.ueberblick; rahmen(); zeichne();
      quittung(erledigt ? 'Abgehakt' : 'Wieder offen', erledigt ? 'Die Frage bleibt im Protokoll, ohne Markierung.' : '', [['Rückgängig', function () { hake(f, !erledigt); }]]);
    }).catch(fehl);
  }
  function nachtragenFenster(x) {       // x: {id?, frage, antwort, aus?}  ·  mit id: bestehende Antwort ändern
    var basis = x.id ? kopie((doc().team || []).filter(function (e) { return e.id === x.id; })[0] || null) : null;
    fenster(basis ? 'Antwort' : 'Antwort', basis ? 'ändern.' : 'nachtragen.', [
      h('p', {}, 'So, wie die Rezeption es einem Gast sagen würde. Gespeichert wird als Entwurf. Nach dem Veröffentlichen antwortet der Chat damit, in jeder Sprache. Bitte keine Namen von Gästen hineinschreiben.'),
      feld('Frage', 'ga-f-frage', x.frage, { max: 400 }),
      feld('Antwort des Hauses', 'ga-f-antwort', x.antwort, { lang: true, zeilen: 6, max: 2000, platz: 'In ganzen Sätzen, so wie Sie es einem Gast am Telefon sagen würden.' })],
    [link('Abbrechen', fensterZu), kn(basis ? 'Änderung speichern' : 'Nachtragen', function () {
      var frage = $('#ga-f-frage').value.trim(), antwort = $('#ga-f-antwort').value.trim();
      if (frage.length < 3 || antwort.length < 3) return fensterMeldung('Bitte Frage und Antwort ausfüllen.');
      var eintrag = { id: x.id || ('t' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6)), frage: frage, antwort: antwort, zeit: new Date().toISOString(), wer: wer(), aus: x.aus || (basis && basis.aus) || '' };
      if (basis && basis.frage === frage && basis.antwort === antwort) { fensterZu(); return quittung('Nichts geändert, nichts gespeichert.', ''); }
      fensterZu();
      speichere(function (d, zwang) {
        var i = (d.team || []).map(function (e) { return e.id; }).indexOf(eintrag.id);
        if (basis) {
          if (i < 0) throw new Kollision(null);
          if (!zwang && !gleich(d.team[i], basis)) throw new Kollision(d.team[i]);
          d.team[i] = eintrag;
        } else if (i < 0) d.team.push(eintrag);
      }, basis ? 'Antwort geändert' : 'Antwort nachgetragen', {
        nach: x.aus ? function () { return eigen('frage', { id: x.aus, erledigt: true, wer: wer() }).then(ladeBetrieb).catch(function () {}); } : null,
        zurueck: x.aus ? function () { return eigen('frage', { id: x.aus, erledigt: false, wer: wer() }).then(ladeBetrieb).catch(function () {}); } : null });
    }, { dunkel: true, id: 'ga-f-los' })]);
  }

  /* --- Wissen des Hauses --- */
  function wissen() {
    var d = doc(), live = S.stand.live, team = (d.team || []).slice().reverse(), teil;
    function istEntwurf(e) { var a = (live.team || []).filter(function (y) { return y.id === e.id; })[0]; return !a || a.frage !== e.frage || a.antwort !== e.antwort; }
    if (S.wissen === 'team') {
      teil = [h('div', { class: 'ga-reihe' }, kn('Antwort anlegen', function () { nachtragenFenster({ frage: '', antwort: '' }); }, { dunkel: true, id: 'ga-w-neu' })),
        team.length ? h('div', { class: 'ga-eintraege' }, team.map(function (e) {
          return h('div', { class: 'platte ga-eintrag', 'data-team': e.id },
            h('div', { class: 'ga-eintrag__kopf' }, h('span', { class: 'angabe' }, zeit(e.zeit) + (e.wer ? ' · ' + e.wer : '')), istEntwurf(e) ? h('span', { class: 'marke' }, 'Entwurf') : null),
            h('p', {}, h('b', {}, e.frage)), h('p', {}, e.antwort),
            h('div', { class: 'ga-reihe' }, kn('Ändern', function () { nachtragenFenster({ id: e.id, frage: e.frage, antwort: e.antwort }); }),
              link('Entfernen', function () { entfernenFenster(e); })));
        })) : leer('Noch nichts nachgetragen.', 'Hatte der Chat auf eine Frage keine Antwort, steht sie unter «Das wurde gefragt» mit dem Knopf «Antwort nachtragen». Sie können hier auch eine Antwort ohne Frage anlegen.'),
        (live.team || []).filter(function (a) { return !(d.team || []).some(function (y) { return y.id === a.id; }); }).map(function (a) {
          return h('div', { class: 'kuhle ga-eintrag' }, h('div', { class: 'ga-eintrag__kopf' }, h('span', { class: 'angabe' }, 'Im Entwurf entfernt, online noch da'), h('span', { class: 'marke' }, 'Entwurf')), h('p', {}, h('b', {}, a.frage)), h('p', {}, a.antwort));
        })];
    } else if (S.wissen === 'quelle') {
      var s = S.suche.trim().toLowerCase(), l = (d.wissen || []).filter(function (a) { return !s || (a.titel + ' ' + a.text).toLowerCase().indexOf(s) >= 0; });
      var such = feld('Im Wissen suchen', 'ga-w-suche', S.suche, { platz: 'Zum Beispiel: Frühstück, Parkplatz, Sauna' });
      such.querySelector('input').addEventListener('input', function () { S.suche = this.value; clearTimeout(wissen.t); wissen.t = setTimeout(function () { zeichne(); var f = $('#ga-w-suche'); f.focus(); f.setSelectionRange(f.value.length, f.value.length); }, 250); });
      teil = [h('p', {}, 'Diese Texte hat das Werkzeug von der Website und aus den Unterlagen des Hauses gelesen. Der Chat antwortet nur daraus. Geändert werden sie dort, wo sie herkommen, zum Beispiel in «' + Welt.name('website') + '». «Neu einlesen» holt den heutigen Stand.'),
        h('div', { class: 'platte ga-insel' }, h('div', { class: 'ga-reihe ga-reihe--unten' }, such, kn('Neu einlesen', neuEinlesen, { id: 'ga-w-einlesen' }))),
        h('p', { class: 'angabe' }, 'Eingelesen ' + zeit((d.eingelesen || {}).zeit) + ' · ' + mal(l.length, 'ein Abschnitt', 'Abschnitte') + (s ? ' mit «' + S.suche.trim() + '»' : '')),
        l.length ? h('div', { class: 'ga-eintraege' }, l.map(function (a) {
          var auf = S.offenText['w' + a.id], stelle = '';
          if (s) { var i = a.text.toLowerCase().indexOf(s); if (i >= 0) stelle = (i > 80 ? '… ' : '') + a.text.slice(Math.max(0, i - 80), i + 160) + ' …'; }
          return h('div', { class: 'platte ga-eintrag', 'data-wissen': a.id },
            h('div', { class: 'ga-eintrag__kopf' }, h('b', {}, a.titel), h('span', { class: 'ga-schild' }, { seite: 'Website', unterlage: 'Unterlage', tal: 'Umgebung' }[a.art] || a.art)),
            h('span', { class: 'angabe' }, [a.quelle, a.text.length.toLocaleString('de-CH') + ' Zeichen'].filter(Boolean).join(' · ')),
            stelle && !auf ? h('p', { class: 'ga-leise' }, stelle) : null,
            h('button', { class: 'ga-auf', type: 'button', 'aria-expanded': String(!!auf), klick: function () { S.offenText['w' + a.id] = !auf; zeichne(); } }, auf ? 'Text schliessen' : 'Text ansehen'),
            auf ? h('div', { class: 'kuhle ga-text ga-text--lang', tabindex: '0' }, a.text) : null);
        })) : leer('Nichts gefunden.', 'Zu «' + S.suche.trim() + '» steht nichts im eingelesenen Wissen. Wenn Gäste danach fragen, tragen Sie die Antwort unter «Vom Team» nach.')];
    } else {
      var hh = d.haus || {}, zeilen = [['Name', hh.name], ['Ort', hh.ort], ['Telefon', hh.tel], ['E-Mail', hh.mail], ['Adresse', hh.adresse], ['Erreichbarkeit', hh.zeiten], ['Fahrplan für Ausflüge', hh.fahrplan], ['Adresse der Buchung', hh.buchung],
        ['Sprachen des Chats', Object.keys(hh.sprachen || {}).map(function (k) { return SPRACHE[k] || k; }).join(', ')],
        ['Absender je Anliegen', Object.keys(ART).map(function (k) { return (hh.absender || {})[k] ? ART[k] + ': ' + hh.absender[k] : ''; }).filter(Boolean).join(' · ')],
        ['Mail-Vorlagen', Object.keys(ART).map(function (k) { return (d.vorlagen || {})[k] ? ART[k] + ': ' + d.vorlagen[k].nr : ''; }).filter(Boolean).join(' · ')],
        ['Startfragen im Chat', (d.karten || []).map(function (k) { return k[2]; }).join(' · ')], ['Modell der KI', hh.modell]];
      teil = [h('p', {}, 'Diese Angaben stammen aus den Quellen des Hauses und stehen hier zum Nachsehen. Was fehlt, ist als «offen» gekennzeichnet und wird nicht geraten.'),
        h('div', { class: 'liste' }, zeilen.map(function (z) { return h('div', {}, h('span', {}, z[0]), h('span', {}, z[1] || 'offen')); })),
        h('p', { class: 'angabe' }, 'Gelesen aus: ' + ((d.eingelesen || {}).quellen || []).join(' · '))];
    }
    return [titel('Wissen des Hauses', 'Was der Chat', 'weiss.', 'Der Chat antwortet nur mit dem, was hier steht: mit dem, was Ihr Team nachgetragen hat, und mit den Texten von Website und Unterlagen. Jede Änderung ist zuerst ein Entwurf. Online geht sie mit «Veröffentlichen».'),
      wahl('Teil', [['team', 'Vom Team · ' + (d.team || []).length], ['quelle', 'Aus Website und Unterlagen · ' + (d.wissen || []).length], ['haus', 'Angaben des Hauses']], S.wissen, function (w) { S.wissen = w; zeichne(); }), teil];
  }
  function entfernenFenster(e) {
    fenster('Antwort', 'entfernen?', h('p', {}, 'Im Entwurf fällt diese Antwort weg. Nach dem Veröffentlichen weiss der Chat das nicht mehr und verweist bei dieser Frage wieder an die Rezeption.'),
      [link('Abbrechen', fensterZu), kn('Entfernen', function () {
        fensterZu();
        var basis = kopie(e);
        speichere(function (d, zwang) {
          var i = (d.team || []).map(function (y) { return y.id; }).indexOf(e.id);
          if (i < 0) return;
          if (!zwang && !gleich(d.team[i], basis)) throw new Kollision(d.team[i]);
          d.team.splice(i, 1);
        }, 'Antwort entfernt');
      }, { dunkel: true, id: 'ga-f-los' })]);
  }
  function neuEinlesen() {
    var knopf = $('#ga-w-einlesen');
    if (knopf) knopf.disabled = true;
    eigen('einlesen', {}).then(function (neu) {
      return speichere(function (d) {
        var vor = JSON.stringify(d);
        ['haus', 'karten', 'muster', 'wissen', 'vorlagen', 'tal_hinweis'].forEach(function (k) { if (neu[k] != null) d[k] = neu[k]; });
        if (JSON.stringify(d) !== vor) d.eingelesen = neu.eingelesen;
      }, 'Wissen neu eingelesen', { gleichText: 'Website und Unterlagen sind unverändert seit dem letzten Einlesen.' });
    }).catch(fehl).then(function () { var k = $('#ga-w-einlesen'); if (k) k.disabled = false; });
  }

  /* --- Probe-Chat: links das Handy des Gastes, rechts was das Team dazu sieht --- */
  function probe() {
    var c = S.chat, d = c.stand === 'entwurf' && S.stand.entwurf ? S.stand.entwurf : S.stand.live, neuAb = c.gezeigt == null ? 0 : c.gezeigt, k = S.kleid || {};
    if (c.stand === 'entwurf' && !S.stand.offen) c.stand = 'live';
    c.gezeigt = c.nachrichten.length;
    function blase(n, i) { return h('div', { class: 'ga-blase ' + (n.rolle === 'user' ? 'ga-blase--gast' : 'ga-blase--haus') + (i >= neuAb ? ' ga-neu-da' : '') }, n.text); }
    function notiz(n, i) {
      if (n.rolle === 'user') return null;
      return h('div', { class: 'platte ga-eintrag ga-team__zu', 'data-antwort': i },
        h('span', { class: 'angabe' }, [n.grenze ? 'Grenze erreicht' : n.ausfall ? 'KI hat nicht geantwortet' : n.belegt === false ? 'ohne Antwort im Wissen' : n.thema === 'abgelehnt' ? 'abgelehnt' : 'aus dem Wissen beantwortet',
          n.mit_entwurf ? 'mit dem Entwurf' : 'wie veröffentlicht', SPRACHE[n.sprache] || ''].filter(Boolean).join(' · ')),
        h('p', {}, h('b', {}, n.frage)),
        n.belegt === false && !n.ausfall ? kn('Antwort nachtragen', function () { nachtragenFenster({ frage: n.frage, antwort: '', aus: n.frage_id }); }, { dunkel: true }) : null,
        n.anfrage ? kn('Im Eingang öffnen', function () { gehe('eingang', n.anfrage); }) : null,
        n.buchung ? h('span', {}, 'Hier sieht der Gast den Weg zur Buchung: ', n.buchung === 'offen' ? 'offen, die Adresse der Buchung fehlt' : h('a', { href: n.buchung, target: '_blank', rel: 'noopener' }, n.buchung)) : null);
    }
    var ein = feld('Ihre Frage als Gast', 'ga-c-frage', '', { lang: true, zeilen: 1, max: 600, platz: 'Ihre Frage als Gast' });
    ein.querySelector('textarea').addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sende(this.value); } });
    var notizen = c.nachrichten.map(notiz).filter(Boolean).reverse();
    return [titel('Probe-Chat', 'Was ein Gast', 'sehen würde.', 'Schreiben Sie ins Handy, wie ein Gast schreiben würde. Daneben steht zu jeder Antwort, woher sie kommt. Der Chat antwortet in der Sprache der Frage. Fragen aus dem Probe-Chat zählen in der Auswertung nicht als Gäste.'),
      h('div', { class: 'ga-probe' },
        h('div', { class: 'ga-handy' + (S.auftritt ? ' ga-dreht' : '') }, h('div', { class: 'ga-handy__schirm' },
          h('div', { class: 'ga-handy__kopf' }, k.zeichen && Welt.welt() === 'grand' ? h('img', { src: bild(k.zeichen), alt: '' }) : null, h('span', {}, h('b', {}, 'Rezeption im Chat'), h('span', { class: 'angabe' }, S.haus))),
          h('div', { class: 'ga-chat', id: 'ga-chat', 'aria-live': 'polite' },
            c.nachrichten.length ? c.nachrichten.map(blase) : [h('p', { class: 'ga-leise' }, 'Mit diesen Fragen beginnt das Fenster für Gäste:'),
              (d.karten || []).length ? h('div', { class: 'wahl' }, d.karten.map(function (x) { return h('button', { type: 'button', klick: function () { sende(x[2]); } }, x[2]); })) : h('p', { class: 'ga-leise' }, 'offen: Für dieses Haus sind keine Startfragen hinterlegt.')],
            c.laeuft ? h('div', { class: 'ga-blase ga-blase--haus ga-leise ga-neu-da' }, 'Die Rezeption schreibt …') : null),
          h('div', { class: 'ga-chat__feld' }, ein, h('button', { class: 'ga-senden', type: 'button', id: 'ga-c-los', 'aria-label': 'Senden', disabled: c.laeuft, html: PFEIL, klick: function () { sende($('#ga-c-frage').value); } })))),
        h('div', { class: 'ga-team' },
          h('div', { class: 'platte ga-insel' }, h('p', { class: 'kap' }, 'Für das Team'),
            wahl('Stand des Wissens', [['live', 'Wie veröffentlicht'], ['entwurf', 'Mit dem Entwurf', !S.stand.offen]], c.stand, function (w) { c.stand = w; zeichne(); }),
            h('div', { class: 'ga-reihe' }, kn('Neues Gespräch', function () { S.chat = { nachrichten: [], gespraech: '', stand: c.stand, laeuft: false }; zeichne(); }, { id: 'ga-c-neu' }))),
          notizen.length ? notizen : h('div', { class: 'platte ga-insel' }, h('p', {}, 'Zu jeder Antwort steht hier, ob sie aus dem Wissen kam, und was Sie damit tun können: nachtragen, im Eingang öffnen.'))))];
  }
  function sende(text) {
    var c = S.chat;
    text = String(text || '').trim();
    if (!text || c.laeuft) return;
    if (!c.gespraech) c.gespraech = 'p' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    c.nachrichten.push({ rolle: 'user', text: text });
    c.laeuft = true; zeichne(); unten();
    eigen('chat', { messages: c.nachrichten.map(function (n) { return { role: n.rolle, content: n.text }; }), gespraech: c.gespraech, stand: c.stand, herkunft: 'probe', sprache: 'de', heute: new Date().toISOString().slice(0, 10), wer: wer() })
      .then(function (a) {
        a.rolle = 'assistant'; a.frage = text;
        c.nachrichten.push(a);
        if (a.ueberblick) { var neu = a.ueberblick.anfragen_neu > S.ue.anfragen_neu; S.ue = a.ueberblick; if (neu) quittung('Neue Anfrage im Eingang', 'So meldet sich das Werkzeug, wenn eine Anfrage wartet.', [['Öffnen', function () { gehe('eingang', a.anfrage); }]]); }
        return ladeBetrieb();
      }).catch(function (e) { c.nachrichten.pop(); fehl(e); })
      .then(function () { c.laeuft = false; rahmen(); if (S.ansicht === 'probe') { zeichne(); unten(); var f = $('#ga-c-frage'); if (f) f.focus({ preventScroll: true }); } });
  }
  function unten() { var b = $('#ga-chat'); if (b) b.scrollTop = b.scrollHeight; }

  /* --- Auswertung: die häufigsten Fragen --- */
  var STOPP = 'aber alle auch bitte dann dass denn doch eine einem einen einer eines gibt haben habt haus hier ihnen ihre ihrem ihren ihrer kann kein keine können mein nach nicht noch oder sein sich sind über unter wann welche welcher wenn werden wieder wird wollen würde gerne there what when where have with your does this that from would could about hotel'.split(' ');
  function worte(t) { return (String(t || '').toLowerCase().match(/[a-zäöüéèàç]{4,}/g) || []).filter(function (w) { return STOPP.indexOf(w) < 0; }); }
  function auswertung() {
    var grenze = S.zeitraum === '30' ? Date.now() - 30 * 864e5 : 0;
    var l = S.betrieb.fragen.filter(function (f) { return (S.ausProben || f.herkunft === 'gast') && new Date(f.zeit).getTime() >= grenze && f.art !== 'ausfall'; });
    var haufen = [], themen = {}, sprachen = {};
    l.forEach(function (f) {
      var w = worte(f.frage), bester = null, wert = 0;
      haufen.forEach(function (hf) { var gemein = w.filter(function (x) { return hf.w.indexOf(x) >= 0; }).length, j = gemein / (new Set(w.concat(hf.w)).size || 1); if (j > wert) { wert = j; bester = hf; } });
      if (bester && wert >= 0.5) { bester.l.push(f); } else haufen.push({ w: w, l: [f] });
      (themen[f.gruppe] = themen[f.gruppe] || []).push(f);
      sprachen[f.sprache] = (sprachen[f.sprache] || 0) + 1;
    });
    haufen.sort(function (a, b) { return b.l.length - a.l.length || (a.l[0].zeit < b.l[0].zeit ? 1 : -1); });
    var tn = Object.keys(themen).sort(function (a, b) { return themen[b].length - themen[a].length; }), max = tn.length ? themen[tn[0]].length : 1;
    var kopf = [titel('Auswertung', 'Die häufigsten', 'Fragen.', 'Was Gäste am häufigsten wissen wollen, nach Themen und im Wortlaut. Gezählt wird, was im Speicher liegt, nichts wird hochgerechnet.'),
      h('div', { class: 'ga-reihe ga-reihe--auseinander' },
        wahl('Zeitraum', [['alles', 'Alles (bis 12 Monate)'], ['30', 'Letzte 30 Tage']], S.zeitraum, function (w) { S.zeitraum = w; zeichne(); }),
        wahl('Herkunft', [[false, 'Nur Gäste'], [true, 'Mit Proben']], S.ausProben, function (w) { S.ausProben = w; zeichne(); }))];
    if (!l.length) return kopf.concat([leer(S.ausProben ? 'Noch keine Frage.' : 'Noch keine Frage von Gästen.', S.ausProben ? 'Sobald jemand die Rezeption im Chat fragt, entsteht hier die Auswertung.'
      : 'Offen: Das Fenster für Gäste auf der Website ist noch nicht an dieses Werkzeug angeschlossen. Mit «Mit Proben» sehen Sie die Auswertung der Fragen aus dem Probe-Chat und aus den Probeläufen im Projekt.',
    S.ausProben ? kn('Zum Probe-Chat', function () { gehe('probe'); }) : null)]);
    return kopf.concat([
      h('p', { class: 'angabe', id: 'ga-aus-grund' }, 'Grundlage: ' + mal(l.length, 'eine Frage', 'Fragen') + (S.ausProben ? ', Proben eingeschlossen' : ' von Gästen') + (l.length < 20 ? '. Für eine belastbare Aussage ist das wenig.' : '.')),
      h('div', { class: 'platte ga-zahlen' }, [[l.length, 'Fragen'], [l.filter(function (f) { return f.belegt === false; }).length, 'ohne Antwort im Wissen'], [l.filter(function (f) { return f.anfrage; }).length, 'wurden zur Anfrage'],
        [l.filter(function (f) { return f.buchung; }).length, 'führten zur Buchung']].map(function (z) { return h('div', {}, h('b', { class: 't-zwischen zahl' }, z[0]), h('span', { class: 'angabe' }, z[1])); })),
      zw('Am häufigsten', 'gestellt'),
      h('div', { class: 'liste', id: 'ga-aus-haeufig' }, haufen.slice(0, 10).map(function (hf) {
        var offen = hf.l.filter(istLuecke).length;
        return h('div', {}, h('span', {}, hf.l[0].frage, offen ? [' ', h('span', { class: 'ga-schild' }, 'ohne Antwort')] : null), h('span', {}, hf.l.length + ' × · zuletzt ' + datum(hf.l[0].zeit)));
      })),
      zw('Nach', 'Themen'),
      h('div', { class: 'platte ga-eintrag' }, h('div', { class: 'ga-balken' }, tn.map(function (t) {
        var n = themen[t].length, ohne = themen[t].filter(function (f) { return f.belegt === false; }).length, spur = h('i');
        spur.style.width = Math.round(n / max * 100) + '%';
        return h('div', {}, h('span', {}, t), h('div', { class: 'ga-balken__spur', role: 'img', 'aria-label': n + ' Fragen' }, spur), h('span', { class: 'angabe' }, n + (ohne ? ' · ' + ohne + ' ohne Antwort' : '')));
      }))),
      zw('Nach', 'Sprache'),
      h('div', { class: 'liste' }, Object.keys(sprachen).sort(function (a, b) { return sprachen[b] - sprachen[a]; }).map(function (k) { return h('div', {}, h('span', {}, SPRACHE[k] || k), h('span', {}, sprachen[k])); }))]);
  }

  /* --- Verlauf --- */
  function verlauf() {
    if (!S.verlauf) {
      Promise.all([speicher('verlauf', 'GET'), speicher('protokoll', 'GET')]).then(function (r) { S.verlauf = r[0]; S.protokoll = r[1]; if (S.ansicht === 'verlauf') zeichne(); }).catch(fehl);
      return [titel('Verlauf', 'Frühere', 'Fassungen.', ''), h('p', { class: 'angabe' }, 'Wird geladen.')];
    }
    var WAS = { grundstand: 'Erster Stand eingelesen', entwurf: 'Als Entwurf gespeichert', verworfen: 'Entwurf verworfen', veroeffentlicht: 'Veröffentlicht', zurueckgeholt: 'Frühere Fassung als Entwurf zurückgeholt', 'aus-sicherung': 'Aus der Sicherung wiederhergestellt' };
    return [titel('Verlauf', 'Frühere', 'Fassungen.', 'Jeder veröffentlichte Stand des Wissens bleibt hier liegen. Zurückholen legt eine frühere Fassung als Entwurf an. Online geht sie erst mit «Veröffentlichen».'),
      S.verlauf.length ? h('div', { class: 'ga-eintraege', id: 'ga-v-liste' }, S.verlauf.map(function (v) {
        return h('div', { class: 'platte ga-eintrag', 'data-fassung': v.fassung },
          h('div', { class: 'ga-eintrag__kopf' }, h('b', {}, 'Online bis ' + zeit(v.abgeloest)), h('span', { class: 'angabe' }, 'abgelöst von ' + (v.wer || 'unbekannt'))),
          v.notiz ? h('p', {}, 'Notiz zur Ablösung: ' + v.notiz) : null,
          h('div', { class: 'ga-reihe' }, kn('Ansehen', function () { fassungAnsehen(v); }), kn('Zurückholen', function () { zurueckholen(v); }, { dunkel: true })));
      })) : leer('Noch keine frühere Fassung.', 'Sobald Sie zum ersten Mal veröffentlichen, liegt der Stand davor hier.'),
      zw('Wer hat wann', 'was getan'),
      h('div', { class: 'liste', id: 'ga-v-protokoll' }, (S.protokoll || []).slice(0, 30).map(function (p) { return h('div', {}, h('span', {}, (WAS[p.was] || p.was) + (p.notiz ? ': ' + p.notiz : '')), h('span', {}, (p.wer || 'unbekannt') + ' · ' + zeit(p.zeit))); }))];
  }
  function fassungAnsehen(v) {
    speicher('fassung', 'GET', undefined, v.fassung).then(function (f) {
      var st = unterschied(f.daten, S.stand.live);
      fenster('Diese Fassung', 'und heute.', st.length ? vnListe(st, 'Diese Fassung', 'Heute online') : h('p', {}, 'Diese Fassung ist dieselbe wie der Stand, der heute online ist.'), [kn('Schliessen', fensterZu, { ohne: true })]);
    }).catch(fehl);
  }
  function zurueckholen(v) {
    function los() {
      var vorher = kopie(S.stand.live);
      eigen('zurueckholen', { fassung: v.fassung, erwartet: S.stand.kennung_entwurf, wer: wer() }).then(function (st) {
        S.stand = st; S.protokoll = null; S.verlauf = null;
        if (!st.offen) return eigen('verwerfen', { erwartet: st.kennung_entwurf, wer: wer() }).then(function (neu) { S.stand = neu; rahmen(); zeichne(); quittung('Nichts zurückzuholen', 'Diese Fassung ist dieselbe wie der Stand, der heute online ist.'); });
        rahmen(); zeichne();
        quittung('Als Entwurf zurückgeholt', 'Online ist weiter der heutige Stand. Die frühere Fassung geht erst mit «Veröffentlichen» online.', [['Vorher, nachher', function () { zeigeUnterschied(vorher, st.entwurf); }]]);
      }).catch(fehl);
    }
    if (!S.stand.offen) return los();
    fenster('Im Entwurf', 'liegt schon etwas.', h('p', {}, 'Zurückholen ersetzt den jetzigen Entwurf mit ' + mal(unterschied(S.stand.live, S.stand.entwurf).length, 'einer Änderung', 'Änderungen') + '. Veröffentlichen Sie ihn vorher, wenn er bleiben soll.'),
      [link('Abbrechen', fensterZu), kn('Entwurf ersetzen', function () { fensterZu(); los(); }, { dunkel: true, id: 'ga-f-los' })]);
  }

  /* --- Kosten und Schutz --- */
  function betrieb() {
    var b = S.betrieb, d = doc(), e = d.einstellungen, lage = S.ue.ki, monat = (b.kosten.monate || {})[b.kosten.monat] || { aufrufe: 0, ein: 0, schreiben: 0, lesen: 0, aus: 0, usd: 0, ohne_preis: 0 }, p = b.preise;
    var kiText = { ok: 'antwortet', probe: 'Probe-Antworten, die KI ist nicht angeschlossen', 'kein-schluessel': 'nicht angeschlossen, kein Schlüssel', obergrenze: 'Obergrenze dieses Monats erreicht', 'guthaben-leer': 'Guthaben aufgebraucht',
      'schluessel-ungueltig': 'Schlüssel wird nicht angenommen', ueberlastet: 'gerade überlastet', fehler: 'Störung' }[lage.stand] || lage.stand;
    var kosten = [['Stand der KI', kiText], ['Modell', b.modell || 'offen'],
      ['Aufrufe diesen Monat', monat.aufrufe], ['Gelesene Tokens diesen Monat', (monat.ein + monat.schreiben + monat.lesen).toLocaleString('de-CH') + ' (davon ' + monat.lesen.toLocaleString('de-CH') + ' aus dem Zwischenspeicher)'],
      ['Geschriebene Tokens diesen Monat', monat.aus.toLocaleString('de-CH')],
      ['Kosten diesen Monat', p ? usd(monat.usd) + (monat.ohne_preis ? ' · ' + monat.ohne_preis + ' Aufrufe ohne hinterlegten Preis' : '') : 'offen, für dieses Modell ist kein Preis hinterlegt'],
      ['Im Schnitt je Aufruf', monat.aufrufe && p ? usd(monat.usd / monat.aufrufe) + ' (gemessen)' : 'noch kein Aufruf gemessen'],
      ['Preis je Million Tokens', p ? 'Eingang ' + p.ein.toFixed(2) + ' · Zwischenspeicher schreiben ' + p.schreiben.toFixed(2) + ' · lesen ' + p.lesen.toFixed(2) + ' · Ausgang ' + p.aus.toFixed(2) + ' USD (Preisliste vom ' + b.preis_stand + ')' : 'offen'],
      ['Obergrenze je Monat', e.obergrenze_monat_usd == null ? 'offen, keine gesetzt' : usd(e.obergrenze_monat_usd)]];
    var grenzen = [['Fragen heute', b.kosten.heute.fragen + ' von höchstens ' + e.gesamt_tag], ['Antwortentwürfe der KI heute', b.kosten.heute.entwuerfe + ' von höchstens ' + e.anfrage_tag],
      ['Fragen je Gespräch', 'höchstens ' + e.besucher_10min + ' in zehn Minuten, ' + e.besucher_tag + ' am Tag'], ['Länge einer Frage', 'höchstens 600 Zeichen, die letzten 12 Beiträge reisen mit']];
    var daten = [['Fragen an den Chat', 'Wortlaut der Frage und der Antwort, Sprache, Zeit. E-Mail-Adressen und Nummern werden vor dem Speichern abgedeckt.'],
      ['Anfragen im Eingang', 'Name, Kontakt, Datum, Personen, Anliegen und das Gespräch, so wie der Gast es geschrieben hat.'],
      ['Aufbewahrung', 'Fragen und Anfragen fallen nach ' + e.aufbewahrung_monate + ' Monaten von selbst heraus.'],
      ['Im Verlauf des Wissens', 'stehen keine Daten von Gästen.'], ['Ort der Daten', 'auf diesem Rechner, im Speicher der Werkzeuge. Die Frage selbst geht zur Antwort an die KI (Anthropic).']];
    var ober = feld('Obergrenze je Monat in USD (leer = keine)', 'ga-b-ober', e.obergrenze_monat_usd == null ? '' : String(e.obergrenze_monat_usd), { zahl: true, platz: 'Zum Beispiel: 20', max: 8 });
    var such = feld('Name, E-Mail oder Telefonnummer des Gastes', 'ga-b-suche', '', { max: 120 });
    return [titel('Kosten und Schutz', 'Was die KI kostet', 'und was sie darf.', 'Die KI kostet je Frage einen kleinen Betrag. Hier sehen Sie, was diesen Monat angefallen ist, welche Grenzen gelten und welche Daten von Gästen gespeichert sind.'),
      zw('Kosten', 'der KI'),
      h('div', { class: 'liste', id: 'ga-b-kosten' }, kosten.map(function (z) { return h('div', {}, h('span', {}, z[0]), h('span', {}, z[1])); })),
      h('div', { class: 'platte ga-insel' }, h('div', { class: 'ga-reihe ga-reihe--unten' }, ober, kn('Obergrenze speichern', function () {
        var roh = $('#ga-b-ober').value.trim().replace(',', '.'), wert = roh === '' ? null : Number(roh);
        if (wert !== null && !(wert > 0 && wert <= 10000)) return quittung('Nicht gespeichert', 'Die Obergrenze ist eine Zahl zwischen 0 und 10 000, oder leer.', [], { fehl: true });
        speichere(function (x) { x.einstellungen.obergrenze_monat_usd = wert; }, wert === null ? 'Obergrenze entfernt' : 'Obergrenze gesetzt');
      }, { id: 'ga-b-ober-kn' })),
      h('p', { class: 'ga-leise' }, 'Ist die Obergrenze erreicht, verweist der Chat bis zum Monatswechsel an die Rezeption, und Antwortentwürfe kommen als Gerüst. Die Obergrenze gilt, sobald sie veröffentlicht ist.')),
      zw('Grenzen', 'gegen Überflutung'),
      h('div', { class: 'liste' }, grenzen.map(function (z) { return h('div', {}, h('span', {}, z[0]), h('span', {}, z[1])); })),
      zw('Daten', 'von Gästen'),
      h('div', { class: 'platte ga-eintrag ga-zeilen' }, daten.map(function (z) { return h('div', {}, h('b', {}, z[0]), h('span', {}, z[1])); })),
      zw('Löschen', 'auf Wunsch eines Gastes'),
      h('div', { class: 'platte ga-insel' }, h('div', { class: 'ga-reihe ga-reihe--unten' }, such, kn('Suchen', gastSuchen, { id: 'ga-b-suche-kn' })),
        S.treffer ? (S.treffer.l.length ? [h('p', {}, mal(S.treffer.l.length, 'Ein Eintrag', 'Einträge') + ' zu «' + S.treffer.suche + '»:'),
          h('div', { class: 'liste', id: 'ga-b-treffer' }, S.treffer.l.map(function (t) { return h('div', {}, h('span', {}, t.titel + ': ' + t.text), h('span', {}, zeit(t.zeit))); })),
          h('div', { class: 'ga-reihe' }, kn('Endgültig löschen', gastLoeschenFenster, { dunkel: true, id: 'ga-b-weg' }))] : h('p', { id: 'ga-b-nichts' }, 'Zu «' + S.treffer.suche + '» ist nichts gespeichert.')) : null)];
  }
  function gastSuchen() {
    var suche = $('#ga-b-suche').value.trim();
    eigen('gast-suchen', { suche: suche }).then(function (d) { S.treffer = { suche: suche, l: d.treffer }; zeichne(); }).catch(fehl);
  }
  function gastLoeschenFenster() {
    var t = S.treffer;
    fenster('Endgültig', 'löschen?', h('p', {}, mal(t.l.length, 'Ein Eintrag', 'Einträge') + ' zu «' + t.suche + '» ' + (t.l.length === 1 ? 'wird' : 'werden') + ' gelöscht, bei Anfragen mit Antwortentwurf, Gespräch und den Fragen aus dem Gespräch. Das lässt sich nicht zurückholen.'),
      [link('Abbrechen', fensterZu), kn('Endgültig löschen', function () {
        eigen('gast-loeschen', { ids: t.l.map(function (x) { return x.id; }), wer: wer() }).then(function (d) {
          fensterZu(); S.treffer = null;
          return ladeBetrieb().then(function () { rahmen(); zeichne(); quittung('Gelöscht', mal(d.geloescht, 'Ein Eintrag', 'Einträge') + ' zu «' + t.suche + '» endgültig entfernt.'); });
        }).catch(function (e) { fensterMeldung(e.message); });
      }, { dunkel: true, id: 'ga-f-los' })]);
  }

  /* ---------- Name für das Protokoll ---------- */
  $('#ga-wer').addEventListener('click', function () {
    fenster('Wer', 'arbeitet gerade?', [h('p', {}, 'Ihr Name steht bei jeder Änderung im Verlauf. Eine Anmeldung gibt es noch nicht: Der Name wird nur an diesem Gerät gemerkt.'), feld('Ihr Name', 'ga-f-wer', wer() === 'Team' ? '' : wer(), { max: 60 })],
      [link('Abbrechen', fensterZu), kn('Übernehmen', function () {
        var n = $('#ga-f-wer').value.trim() || 'Team';
        try { localStorage.setItem('gaeste-wer', n); } catch (e) { /* privat */ }
        fensterZu(); rahmen(); quittung('Name übernommen', 'Ihre Änderungen stehen ab jetzt unter «' + n + '» im Verlauf.');
      }, { dunkel: true, id: 'ga-f-los' })]);
  });

  /* ---------- Start ---------- */
  function tuer(kopf, satz, mehr) { var m = $('#ga-haupt'); m.textContent = ''; haenge(m, h('div', { class: 'platte ga-tuer' }, h('h1', { class: 't-ansicht' }, kopf), h('p', {}, satz), mehr || null)); $('#ga-leiste').hidden = true; $('#ga-rand').hidden = true; document.body.classList.add('ga-ohne-rand'); }
  if (!HAUS) {
    tuer('Welches Haus?', 'In der Adresse fehlt das Haus. Die zwei Probehäuser:', h('div', { class: 'ga-reihe' },
      h('a', { class: 'kn kn--d', href: '?haus=gasterntal' }, 'Berghotel Gasterntal', h('i', { 'aria-hidden': 'true', html: PFEIL })), h('a', { class: 'kn kn--d', href: '?haus=beau-rivage' }, 'Grand Beau-Rivage', h('i', { 'aria-hidden': 'true', html: PFEIL }))));
    return;
  }
  function kleide() {        // Bilder, Tapete und Zeichen gehören dem Haus; ohne sie bleibt die Bühne der Welt
    var k = S.kleid || {}, b = document.body, z = $('#ga-zeichen'), ku = $('#ga-kulisse');
    if (k.tapete) b.style.setProperty('--ga-tapete', 'url("' + bild(k.tapete) + '")');
    if (k.schriftzug) b.style.setProperty('--ga-schriftzug', 'url("' + bild(k.schriftzug) + '")');
    if (k.kulisse) ku.insertBefore(h('img', { src: bild(k.kulisse), alt: '', decoding: 'async' }), ku.firstChild);
    if (k.zeichen) z.appendChild(h('img', { src: bild(k.zeichen), alt: '' }));
    if (k.schriftzug) z.appendChild(h('i'));
    z.classList.toggle('ga-da', !!(k.zeichen || k.schriftzug));
    var knopf = document.querySelector('[data-welt-knopf]');
    if (knopf) knopf.classList.remove('kn--d');
    $('#ga-leiste').classList.add('ga-kommt');
  }
  var fein = window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches, ruheBis = 0;
  window.addEventListener('scroll', function () { ruheBis = Date.now() + 300; }, { passive: true });
  $('#ga-haupt').addEventListener('pointermove', function (e) {      // Kacheln neigen sich zur Maus; nach dem Scrollen 300 ms Ruhe
    var k = e.target.closest ? e.target.closest('.ga-k3') : null;
    if (!fein || !k || Date.now() < ruheBis) return;
    var r = k.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
    k.classList.add('ga-folgt');
    k.style.setProperty('--ga-ny', (x * 9).toFixed(2) + 'deg'); k.style.setProperty('--ga-nx', (-y * 7).toFixed(2) + 'deg');
  });
  $('#ga-haupt').addEventListener('pointerout', function (e) {
    var k = e.target.closest ? e.target.closest('.ga-k3') : null;
    if (k && !k.contains(e.relatedTarget)) { k.classList.remove('ga-folgt'); k.style.removeProperty('--ga-nx'); k.style.removeProperty('--ga-ny'); }
  });
  eigen('start').then(function (s) {
    S.haus = s.haus; S.kleid = s.kleid || null; S.beispieleDa = !!s.beispiele_da;
    return Promise.all([eigen('stand'), ladeBetrieb()]);
  }).then(function (r) {
    S.stand = r[0];
    var z = location.hash.slice(1).split('/');
    if (BEREICHE.some(function (b) { return b[0] === z[0]; })) { S.ansicht = z[0]; S.wahl = z[1] || ''; }
    kleide(); rahmen(); zeichne();
    Welt.bei(function () { S.auftritt = true; rahmen(); zeichne(); });
    window.addEventListener('hashchange', function () { var n = location.hash.slice(1).split('/'); if ((n[0] !== S.ansicht || (n[1] || '') !== S.wahl) && BEREICHE.some(function (b) { return b[0] === n[0]; })) gehe(n[0], n[1] || ''); });
    function nachsehen() {      // jede Minute und wenn das Fenster wieder nach vorn kommt: wartet eine Anfrage?
      if (document.hidden) return;
      eigen('ueberblick').then(function (u) {
        var mehr = u.anfragen_neu > S.ue.anfragen_neu, anders = u.anfragen_gesamt !== S.ue.anfragen_gesamt || u.fragen_gesamt !== S.ue.fragen_gesamt || u.anfragen_neu !== S.ue.anfragen_neu;
        S.ue = u; rahmen();
        if (mehr) quittung('Neue Anfrage im Eingang', (ART[(u.wartet[0] || {}).art] || 'Anfrage') + ' · ' + ((u.wartet[0] || {}).name || 'ohne Namen'), [['Öffnen', function () { gehe('eingang', (u.wartet[0] || {}).id); }]]);
        if (anders) ladeBetrieb().then(function () { rahmen(); if (ruhig()) zeichne(); });
      }).catch(function () { /* beim nächsten Mal */ });
    }
    setInterval(nachsehen, 60000);
    document.addEventListener('visibilitychange', nachsehen);
    window.gaNachsehen = nachsehen;      // für den Prüflauf
  }).catch(function (e) {
    tuer(Welt.name(W) + ' startet nicht.', String(e.message || e), h('p', { class: 'angabe' }, e.stichwort ? 'Stichwort: ' + e.stichwort : ''));
  });
})();
