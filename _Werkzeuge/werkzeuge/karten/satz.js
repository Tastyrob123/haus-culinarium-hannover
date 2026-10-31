/* satz.js · Satz der Karten. EINE Datei für die Vorschau im Werkzeug und für die PDF (druck.html), damit beide gleich sind.
   Aus den Daten einer Karte entstehen Bausteine, sie werden im Browser mit satz.css gemessen und ausgeglichen auf volle
   Seiten verteilt. Abgeleitet aus dem Satz am Grand Beau-Rivage (mission-control/karte.js, 11./12.10.2026).

   Regeln des Umbruchs (Robert 12.10.2026), hier erzwungen und mit regeln() nachgeprüft:
     · Kein Gericht steht allein auf einer Seite.
     · Keine Rubrik wird von ihrem ersten Gericht getrennt (auch nicht, wenn zwischen beiden eine Erläuterung steht).
     · Nichts läuft über den Rand des Blatts.

   KT_SATZ.setze(karte, ort, opt) → { seiten: [html], wo: [{teil, i}], regeln: [Verstösse] }
     ort  unsichtbarer Kasten im Dokument zum Messen (ohne transform)
     opt  { haus: Name des Hauses, bearbeiten: data-k an jedem Text, allergene: {schluessel: Wort},
            zeichen: Zeichnung des Hauses (steht dann statt des Namens da), zeichenMass: [breite, höhe] } */
(function (G) {
  'use strict';
  var LUFT = 6.0;   // mm, höchstens so viel zusätzliche Luft je Zwischenraum
  var VERSION = 5;  // hochzählen, wenn sich am Satz etwas ändert: gespeicherte PDF gelten dann als veraltet

  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;'); }
  function zelle(x) { return x === '' || x == null ? '&nbsp;' : esc(x); }

  /* ein Baustein → HTML. k: Pfad für das Schreiben in der Karte (data-k an jedem Text), sonst leer */
  function baustein(u, k, opt) {
    var p = function (f) { return k ? ' data-k="' + k + '.' + f + '"' : ''; };
    var koepfe = function () {
      return u.koepfe && u.koepfe.length ? '<span class="kt-rk">' + u.koepfe.map(function (x, i) { return '<b' + p('koepfe.' + i) + '>' + zelle(x) + '</b>'; }).join('') + '</span>' : '';
    };
    switch (u.t) {
      case 'rubrik':
        return '<h2 class="kt-rubrik' + (u.koepfe && u.koepfe.length ? ' kt-rubrik--tafel' : '') + '"><span><span' + p('titel') + '>' + esc(u.titel) + '</span>' +
          (u.en ? '<small' + p('en') + '>' + esc(u.en) + '</small>' : '') + (u.zusatz ? '<small' + p('zusatz') + '>' + esc(u.zusatz) + '</small>' : '') + '</span>' + koepfe() + '</h2>';
      case 'land': return '<h3 class="kt-zw kt-zw--land"' + p('text') + '>' + esc(u.text) + '</h3>';
      case 'zw': return '<h3 class="kt-zw"><span' + p('text') + '>' + esc(u.text) + '</span>' + koepfe() + '</h3>';
      case 'kopf': return '<p class="kt-tkopf"' + p('text') + '>' + esc(u.text) + '</p>';
      case 'zeile': return '<div class="kt-tz"><span' + p('name') + '>' + esc(u.name) + '</span><b' + p('preis') + '>' + zelle(u.preis) + '</b></div>';
      case 'notiz': return '<p class="kt-tnote' + (u.en ? ' kt-fr' : '') + '"' + p('text') + '>' + esc(u.text) + '</p>';
      case 'gericht': case 'frei': {
        var zl = (u.zeilen || []).map(function (z, i) {
          var zp = z.preise || [], kl = [z.en && !zp.length ? 'kt-fr' : '', zp.length ? 'kt-mp' : '', z.fett ? 'kt-halb' : ''].filter(Boolean).join(' ');
          return '<p' + (kl ? ' class="' + kl + '"' : '') + '><span' + p('zeilen.' + i + '.text') + '>' + esc(z.text) + '</span>' +
            zp.map(function (x, j) { return '<b' + p('zeilen.' + i + '.preise.' + j) + '>' + zelle(x) + '</b>'; }).join('') + '</p>';
        }).join('');
        var al = (u.allergene || []).length ? '<p class="kt-al">Enthält: ' + u.allergene.map(function (a) { return esc((opt && opt.allergene && opt.allergene[a]) || a); }).join(', ') + '</p>' : '';
        var ein = u.einheiten || [], mit = ein.some(Boolean);
        var pr = (u.preise || []).map(function (x, i) {
          return '<span class="kt-pz">' + (mit && ein[i] ? '<em' + p('einheiten.' + i) + '>' + esc(ein[i]) + '</em>' : '') + '<b' + p('preise.' + i) + '>' + zelle(x) + '</b></span>';
        }).join('');
        var kopf = u.name ? '<h4><span' + p('name') + '>' + esc(u.name) + '</span>' + (u.zusatz ? ' <small' + p('zusatz') + '>' + esc(u.zusatz) + '</small>' : '') + '</h4>' : '';
        return '<div class="kt-po' + (u.name ? '' : ' kt-po--frei') + '"><div class="kt-po__t">' + kopf + zl + al + '</div>' +
          ((u.preise || []).length ? '<div class="kt-po__p' + (!mit && u.preise.length > 1 ? ' kt-po__p--reihe' : '') + '">' + pr + '</div>' : '') + '</div>';
      }
    }
    return '';
  }

  /* Zeichen des Hauses (reine Zeichnung aus kleid.py, nimmt die Farbe der Welt an). Breit = Schriftzug statt rundem Zeichen. */
  function zeichen(opt, kl) { var m = opt.zeichenMass || [1, 1]; return '<span class="' + kl + (m[0] / m[1] > 1.6 ? ' kt-z--breit' : '') + '" aria-hidden="true">' + opt.zeichen + '</span>'; }
  function klassen(meta) { return (meta.kl || '').split(/\s+/).filter(Boolean).map(function (x) { return 'kt-' + x; }).join(' '); }
  function blatt(meta, innen, kl, attr) {
    var f = meta.format || [210, 297];
    return '<section' + (attr || '') + ' class="kt-blatt ' + kl + '" style="width:' + f[0] + 'mm;height:' + f[1] + 'mm">' + innen + '</section>';
  }
  function deckel(meta, d, k, opt) {
    var p = function (f) { return k ? ' data-k="' + k + '.' + f + '"' : ''; };
    var z = (d.zeilen || []).map(function (x, i) { return '<p class="kt-deck__z"' + p('zeilen.' + i) + '>' + esc(x) + '</p>'; }).join('');
    return blatt(meta, '<div class="kt-deck">' + (opt && opt.zeichen ? zeichen(opt, 'kt-deck__m') : opt && opt.haus ? '<p class="kt-deck__haus">' + esc(opt.haus) + '</p>' : '') + '<h1' + p('titel') + '>' + esc(d.titel) + '</h1><i></i>' +
      (d.unter ? '<p class="kt-deck__u"' + p('unter') + '>' + esc(d.unter) + '</p>' : '') + z + '</div>', 'kt-blatt--deck ' + klassen(meta), ' data-kt-art="deckel"');
  }
  function innenblatt(meta, inhalt, k, opt) {
    var fuss = meta.fuss ? '<p class="kt-fuss"' + (k ? ' data-k="fuss"' : '') + '>' + esc(meta.fuss) + '</p>' : '';
    return blatt(meta, '<header class="kt-leiste">' + (opt && opt.zeichen ? zeichen(opt, 'kt-leiste__z') : '<b>' + esc((opt && opt.haus) || '') + '</b>') + '</header><div class="kt-inhalt"><div class="kt-fluss">' + inhalt + '</div>' + fuss + '</div>',
      klassen(meta), ' data-kt-art="innen"');
  }

  function istKopf(u) { return u.t === 'rubrik' || u.t === 'land' || u.t === 'zw' || u.t === 'kopf'; }
  /* Kopf-Kette ab k: alle Köpfe, Erläuterungen direkt dahinter, dann der erste Eintrag (bei Tafelzeilen zwei) */
  function kette(units, k) {
    var j = k;
    while (j < units.length && (istKopf(units[j]) || (j > k && units[j].t === 'notiz'))) j++;
    if (j < units.length) { j++; if (j < units.length && units[j - 1].t === 'zeile' && units[j].t === 'zeile') j++; }
    return j;
  }

  /* Verteilen: so viele Seiten wie nötig, ausgeglichen gefüllt */
  function packe(units, masse, budget) {
    function hoehe(k, erste) { var m = masse[k]; return m[0] + (erste ? 0 : m[1]) + m[2]; }
    /* Ausgleichs-Umbruch nie vor dem letzten Eintrag einer Rubrik und nie direkt nach ihrem ersten */
    function schluss(k) { return k > 0 && !vorspann(units, k) && !vorspann(units, k - 1) && (k + 1 >= units.length || vorspann(units, k + 1)); }
    function zweites(k) { return k > 1 && !vorspann(units, k) && !vorspann(units, k - 1) && vorspann(units, k - 2); }
    var gesamt = 0; for (var q = 0; q < units.length; q++) gesamt += hoehe(q, false);
    function lauf(n) {
      var ziel = gesamt / n, seiten = [], akt = [], voll = 0, gesetzt = 0, k = 0;
      while (k < units.length) {
        var j = istKopf(units[k]) ? kette(units, k) : k + 1, h = 0;
        for (var i = k; i < j; i++) h += hoehe(i, (!akt.length) && i === k);
        if (akt.length && voll + h > budget) { seiten.push(akt); akt = []; voll = 0; continue; }
        var restPasst = (gesamt - gesetzt) <= (n - seiten.length - 1) * budget * 0.96;
        if (akt.length && seiten.length < n - 1 && voll + h > ziel && voll >= ziel * 0.8 && restPasst && !schluss(k) && !zweites(k)) { seiten.push(akt); akt = []; voll = 0; continue; }
        for (i = k; i < j; i++) akt.push(i);
        voll += h; gesetzt += h; k = j;
      }
      if (akt.length) seiten.push(akt);
      return seiten;
    }
    var n = Math.max(1, Math.ceil(Math.trunc(gesamt) / Math.trunc(budget))), seiten = [];
    for (var r = 0; r < 6; r++) { seiten = lauf(n); if (seiten.length <= n) break; n = seiten.length; }
    seiten = allein_beheben(units, seiten, hoehe, budget);
    return seiten.map(function (sp) {
      var voll = 0; sp.forEach(function (i) { voll += hoehe(i, i === sp[0]); });
      return { i: sp, rest: Math.max(0, budget - voll) };
    });
  }
  /* Vorspann = Kopf, oder Erläuterung, die direkt unter einem Kopf steht. Alles andere ist ein Eintrag. */
  function kopfDavor(units, i) { var j = i; while (j > 0 && units[j].t === 'notiz') j--; return istKopf(units[j]); }
  function vorspann(units, i) { return istKopf(units[i]) || (units[i].t === 'notiz' && kopfDavor(units, i)); }
  function eintraege(units, sp) { return sp.filter(function (i) { return !vorspann(units, i); }).length; }

  /* Steht auf einer Seite nur ein einziger Eintrag, holt sie sich den letzten Eintrag der Seite davor samt dessen Köpfen
     (oder gibt, ganz am Anfang, ihren an die nächste Seite ab). Nur solange die Höhe reicht. */
  function allein_beheben(units, seiten, hoehe, budget) {
    function voll(sp) { var v = 0; sp.forEach(function (i) { v += hoehe(i, i === sp[0]); }); return v; }
    var gesamt = eintraege(units, units.map(function (_, i) { return i; }));
    if (gesamt < 2) return seiten;
    for (var runde = 0; runde < 12; runde++) {
      var s = -1;
      for (var x = 0; x < seiten.length; x++) if (eintraege(units, seiten[x]) === 1) { s = x; break; }
      if (s < 0) break;
      if (s > 0) {
        var vor = seiten[s - 1], ab = vor.length - 1;
        while (ab > 0 && vorspann(units, vor[ab - 1])) ab--;   // den letzten Eintrag samt Kopf-Kette
        var neuVor = vor.slice(0, ab), neu = vor.slice(ab).concat(seiten[s]);
        if (voll(neu) <= budget) {
          if (neuVor.length) { seiten[s - 1] = neuVor; seiten[s] = neu; } else { seiten.splice(s - 1, 2, neu); }
          continue;
        }
      }
      if (s + 1 < seiten.length) {
        var zus = seiten[s].concat(seiten[s + 1]);
        if (voll(zus) <= budget) { seiten.splice(s, 2, zus); continue; }
        var nach = seiten[s + 1], bis = istKopf(units[nach[0]]) ? kette(units, nach[0]) - nach[0] : 1, mit = seiten[s].concat(nach.slice(0, bis));
        if (bis < nach.length && voll(mit) <= budget) { seiten[s] = mit; seiten[s + 1] = nach.slice(bis); continue; }
      }
      break;
    }
    return seiten;
  }

  /* Die Regeln des Umbruchs nachprüfen. Rückgabe: Liste von Verstössen in Alltagssprache (leer = gut). */
  function regeln(units, seiten, name) {
    var aus = [], gesamt = eintraege(units, units.map(function (_, i) { return i; }));
    function was(u) { return u.titel || u.name || u.text || ((u.zeilen || [])[0] || {}).text || ''; }
    seiten.forEach(function (sp, n) {
      var e = eintraege(units, sp), letzter = units[sp[sp.length - 1]];
      if (gesamt > 1 && e === 1) aus.push('Seite ' + (n + 1) + ' von «' + name + '»: «' + was(units[sp.filter(function (i) { return !vorspann(units, i); }).pop()]) + '» steht allein auf der Seite.');
      if (vorspann(units, sp[sp.length - 1])) aus.push('Seite ' + (n + 1) + ' von «' + name + '»: «' + was(letzter) + '» steht am Seitenende ohne ihren ersten Eintrag.');
      if (n > 0 && !vorspann(units, sp[0]) && sp[0] > 0 && vorspann(units, sp[0] - 1)) aus.push('Seite ' + (n + 1) + ' von «' + name + '»: «' + was(units[sp[0]]) + '» ist von seiner Rubrik getrennt.');
    });
    return aus;
  }

  /* Messen im Browser: eine leere Seite (freie Höhe) und eine Seite mit allen Bausteinen in voller Höhe */
  function messe(meta, units, ort, opt) {
    var mm = function (x) { return x / 96 * 25.4; };
    var leer = innenblatt(meta, '', '', opt).replace('<section ', '<section data-leer="1" ');
    var voll = innenblatt(Object.assign({}, meta, { fuss: '' }), units.map(function (u) { return baustein(u, '', opt); }).join(''), '', opt)
      .replace('class="kt-fluss"', 'class="kt-fluss" style="justify-content:flex-start"').replace('<section ', '<section data-mess="1" ').replace(/height:[\d.]+mm"/, 'height:auto;overflow:visible"');
    ort.innerHTML = leer + voll;
    var budget = mm(ort.querySelector('[data-leer] .kt-fluss').getBoundingClientRect().height);
    var masse = [].map.call(ort.querySelector('[data-mess] .kt-fluss').children, function (x) {
      var c = getComputedStyle(x); return [mm(x.getBoundingClientRect().height), mm(parseFloat(c.marginTop)), mm(parseFloat(c.marginBottom))];
    });
    ort.innerHTML = '';
    return { budget: budget - 0.6, masse: masse };   // 0,6 mm Reserve gegen Rundung beim Druck
  }

  function setze(daten, ort, opt) {
    opt = opt || {};
    var meta = daten, aus = [], wo = [], verstoesse = [], b = !!opt.bearbeiten;
    (daten.teile || []).forEach(function (t, ti) {
      if (t.art === 'deckel') { aus.push(deckel(meta, t, b ? 'teile.' + ti : '', opt)); wo.push({ teil: ti, i: [] }); return; }
      var units = [], idx = [];
      (t.posten || []).forEach(function (u, i) { if (!u.aus) { units.push(u); idx.push(i); } });
      /* Rubriken und Zwischentitel am Ende, auf die kein Eintrag mehr folgt (eben angelegt), werden nicht gedruckt (modell.py: gedruckte_posten) */
      while (units.length && vorspann(units, units.length - 1)) { units.pop(); idx.pop(); }
      if (!units.length) return;
      var m = messe(meta, units, ort, opt), seiten = packe(units, m.masse, m.budget);
      verstoesse = verstoesse.concat(regeln(units, seiten.map(function (s) { return s.i; }), daten.name || ''));
      seiten.forEach(function (sp) {
        var luft = Math.min(sp.rest, LUFT * Math.max(1, sp.i.length - 1)), rest = sp.rest - luft;
        var halter = rest > 0.5 ? '<i class="kt-rest" style="flex:0 0 ' + rest.toFixed(1) + 'mm"></i>' : '';
        var innen = sp.i.map(function (i) { return baustein(units[i], b ? 'teile.' + ti + '.posten.' + idx[i] : '', opt); }).join('') + halter;
        aus.push(innenblatt(meta, innen, b ? '1' : '', opt));
        wo.push({ teil: ti, i: sp.i.map(function (i) { return idx[i]; }) });
      });
    });
    return { seiten: aus, wo: wo, regeln: verstoesse };
  }

  /* Nach dem Einsetzen ins Dokument: läuft irgendwo Inhalt über den Rand des Blatts? */
  function ueberlauf(wurzel) {
    var aus = [];
    [].forEach.call(wurzel.querySelectorAll('.kt-blatt'), function (bl, n) {
      var innen = bl.querySelector('.kt-inhalt') || bl.querySelector('.kt-deck'); if (!innen) return;
      var rand = bl.getBoundingClientRect(), s = rand.height / bl.offsetHeight || 1;
      [].forEach.call(innen.querySelectorAll('.kt-fluss > *, .kt-fuss, .kt-deck > *'), function (x) {
        var r = x.getBoundingClientRect();
        if (r.height && (r.bottom - rand.bottom > 1.5 * s || r.right - rand.right > 1.5 * s)) aus.push('Seite ' + (n + 1) + ': Inhalt läuft über den Rand des Blatts.');
      });
    });
    return aus.filter(function (x, i) { return aus.indexOf(x) === i; });
  }

  /* Schriften laden, bevor gemessen wird: alles einmal unsichtbar setzen, dann auf die Schriften warten */
  function vorbereiten(daten, ort, opt) {
    var alle = [];
    (daten.teile || []).forEach(function (t) {
      if (t.art === 'deckel') alle.push(deckel(daten, t, '', opt));
      else alle.push(innenblatt(daten, (t.posten || []).map(function (u) { return baustein(u, '', opt); }).join(''), '', opt));
    });
    ort.innerHTML = alle.join('');
    ort.getBoundingClientRect();
    return document.fonts.ready.then(function () { ort.innerHTML = ''; });
  }

  G.KT_SATZ = { VERSION: VERSION, LUFT: LUFT, esc: esc, baustein: baustein, setze: setze, vorbereiten: vorbereiten, regeln: regeln, ueberlauf: ueberlauf, istKopf: istKopf };
})(typeof window !== 'undefined' ? window : globalThis);
