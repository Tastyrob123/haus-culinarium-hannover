/* Culinarium · «Platz buchen» in 15 Fassungen (nur Wahlseite). Liest dieselben Vorschau-Termine wie buchen.js und bucht über denselben Dialog. */
(function () {
  'use strict';
  var KEY = 'culinarium-termine-vorschau';
  var BEISPIEL = [
    { id: 'b1', datum: '2026-11-27', zeit: '19:00', preis: 89, plaetze: 14, gebucht: 5 },
    { id: 'b2', datum: '2026-11-28', zeit: '17:00', preis: 89, plaetze: 14, gebucht: 11 },
    { id: 'b3', datum: '2026-12-18', zeit: '19:00', preis: 89, plaetze: 14, gebucht: 0 },
    { id: 'b4', datum: '2026-12-19', zeit: '17:00', preis: 89, plaetze: 14, gebucht: 14 }
  ];
  var TAGE = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  var TK = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'];
  var MON = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  var B = window.BW || { bild: {}, marke: '' };
  var PFEIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var TEXT = 'Such dir deinen Abend aus und zahl direkt. Dein Platz an der Tafel steht, das Ticket kommt per Mail.';

  function lesen() {
    try { var t = JSON.parse(localStorage.getItem(KEY)); if (Array.isArray(t)) return t; } catch (e) {}
    return BEISPIEL.map(function (x) { return Object.assign({}, x); });
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function eur(n) { return n.toFixed(2).replace('.', ',') + ' EUR'; }
  function zwei(n) { return (n < 10 ? '0' : '') + n; }
  function info(x) {
    var p = x.datum.split('-'), d = new Date(+p[0], +p[1] - 1, +p[2]), n = +x.plaetze, g = Math.min(+x.gebucht, n), frei = Math.max(0, n - g);
    var S = Math.min(n, 14);
    return { id: esc(x.id), d: d, tag: d.getDate(), wt: TAGE[d.getDay()], wk: TK[d.getDay()], mon: MON[d.getMonth()], kurz: zwei(d.getDate()) + '.' + zwei(d.getMonth() + 1) + '.',
      jahr: d.getFullYear(), zeit: esc(x.zeit), n: n, g: g, frei: frei, voll: !frei, preis: eur(+x.preis), eur: +x.preis,
      S: S, weg: Math.round(g * S / n) };
  }
  function termine() {
    return lesen().slice().sort(function (a, b) { return (a.datum + a.zeit).localeCompare(b.datum + b.zeit); }).map(info);
  }
  /* Plätze an der Tafel: vergeben wird paarweise gegenüber, von der Mitte nach aussen */
  function sitze(t) {
    var reihenfolge = [], o = [3, 2, 4, 1, 5, 0, 6], weg = {};
    o.forEach(function (k) { reihenfolge.push(k, k + 7); });
    reihenfolge = reihenfolge.filter(function (k) { return k < t.S; });
    for (var i = 0; i < t.weg; i++) weg[reihenfolge[i]] = 1;
    var r = []; for (var j = 0; j < t.S; j++) r.push(!!weg[j]); return r;
  }
  function img(k, cls, pos) {
    return '<img class="' + (cls || '') + '" src="' + B.bild[k] + '" alt="" loading="lazy" decoding="async"' + (pos ? ' style="object-position:' + pos + '"' : '') + '>';
  }
  function knopf(t, txt) {
    return t.voll ? '<span class="bw-aus">Ausgebucht</span>' :
      '<button class="knopf" type="button" data-buchen="' + t.id + '"><span>' + (txt || 'Platz buchen') + '</span><i>' + PFEIL + '</i></button>';
  }
  function fr(t) { return t.voll ? 'Alle ' + t.n + ' Plätze vergeben' : 'Noch ' + t.frei + ' von ' + t.n + ' Plätzen frei'; }
  function kopf(cls, text) {
    return '<div class="bw-kopf ' + (cls || '') + '"><p class="tb-kicker mono">Die nächsten Abende</p><h2 class="tb-titel">Platz buchen.</h2>' +
      '<p class="tb-text">' + (text || TEXT) + '</p><p class="bw-hinweis mono">Vorschau · Termine und Zahlung sind nur simuliert</p></div>';
  }
  function leer() { return '<p class="tb-leer">Gerade steht kein Termin fest. Trag dich unten auf die Warteliste ein.</p>'; }
  function je(T, f) { return T.map(f).join(''); }
  function reihe(n, f) { var s = ''; for (var i = 0; i < n; i++) s += f(i); return s; }

  var R = {};

  /* 1 Sitzplan der Tafel: jeder Abend als Tafel von oben, sieben Stühle je Seite, freie Plätze leuchten in Kerze */
  R[1] = function (T) {
    return '<div class="bw-in bw01"><div class="bw01-oben">' + kopf() + '<figure class="bw01-f">' + img('tafelleer', '', '50% 55%') + '</figure></div>' +
      '<div class="bw01-liste">' + je(T, function (t) {
        var s = sitze(t);
        var st = function (a, b) { return reihe(b - a, function (i) { return '<i class="' + (s[a + i] ? 'weg' : '') + '" style="--i:' + i + '"></i>'; }); };
        var halb = Math.ceil(t.S / 2);
        return '<article class="bw01-r' + (t.voll ? ' voll' : '') + '"><div class="bw01-dat"><b class="bw-z">' + t.tag + '</b><span><strong>' + t.wt + '</strong>' + t.mon + ' · ab ' + t.zeit + '</span></div>' +
          '<div class="bw01-tafel io" role="img" aria-label="' + fr(t) + '"><div class="bw01-reihe o" style="--s:' + halb + '">' + st(0, halb) + '</div><div class="bw01-tisch"></div>' +
          '<div class="bw01-reihe u" style="--s:' + halb + '">' + st(halb, t.S) + '</div></div>' +
          '<div class="bw01-rechts"><p class="bw-m">' + fr(t) + '</p><p class="bw01-preis"><b class="bw-z">' + t.preis + '</b><span class="bw-m">pro Person</span></p>' + knopf(t) + '</div></article>';
      }) + '</div></div>';
  };

  /* 2 Vierzehn Kerzen: je Platz eine Kerze, vergebene sind heruntergebrannt, freie brennen */
  R[2] = function (T) {
    return '<div class="bw02"><figure class="bw02-f">' + img('kerze2', '', '50% 60%') + '</figure><div class="bw-in bw02-in">' +
      kopf('', 'Jede Kerze ist ein Platz an der Tafel. Wo sie noch brennt, ist er frei.') + '<div class="bw02-reihe">' + je(T, function (t) {
        var s = sitze(t);
        return '<article class="bw02-k' + (t.voll ? ' voll' : '') + '"><p class="bw02-dat"><b class="bw-z">' + t.tag + '</b><span><strong>' + t.wt + '</strong>' + t.mon + ' · ab ' + t.zeit + '</span></p>' +
          '<div class="bw02-kerzen io" role="img" aria-label="' + fr(t) + '">' + s.map(function (w, i) { return '<i class="' + (w ? 'aus' : '') + '" style="--i:' + i + '"></i>'; }).join('') + '</div>' +
          '<p class="bw-m">' + (t.voll ? 'Alle Kerzen heruntergebrannt' : 'Noch ' + t.frei + ' Kerzen brennen') + '</p>' +
          '<p class="bw02-preis"><b class="bw-z">' + t.preis + '</b><span class="bw-m">pro Person</span></p>' + knopf(t) + '</article>';
      }) + '</div></div></div>';
  };

  /* 3 Plakate am Brett: jeder Abend sein eigenes Plakat in eigener Farbe, ausgebuchte bekommen den Streifen */
  var FARBEN = ['#CF7233', '#9C3D3A', '#3F6E5A', '#C29A3A', '#8953A9', '#2F5D8A'];
  R[3] = function (T) {
    return '<div class="bw-in bw03">' + kopf() + '<div class="bw03-wand">' + je(T, function (t, i) {
      return '<article class="bw03-p' + (t.voll ? ' voll' : '') + '" style="--ak:' + FARBEN[i % FARBEN.length] + ';--rot:' + [-1.6, 1.2, -.8, 1.8][i % 4] + 'deg">' +
        '<span class="bw03-nadel"></span><div class="bw03-papier"><p class="bw03-mit">A UNiQUE EXPERiENCE BY MOMO X RUDI</p><div class="bw03-marke">' + B.marke + '</div>' +
        '<p class="bw03-dat bw-z">' + t.kurz + '</p><p class="bw03-tag">' + t.wt + ' · ab ' + t.zeit + '</p><span class="bw03-linie"></span>' +
        '<p class="bw-m">' + fr(t) + '</p><p class="bw03-preis bw-z">' + t.preis + '</p>' + knopf(t) + '</div>' +
        (t.voll ? '<p class="bw03-streifen io">Ausgebucht</p>' : '') + '</article>';
    }) + '</div></div>';
  };

  /* 4 Wie Rudis Zeilen: Termine in Versalien wie Rudis Speisekarte, das Foto daneben wechselt mit dem Abend */
  var BILD4 = ['tafelleer', 'kerze2', 'anstossen', 'kerze3', 'toast', 'glaeser'];
  R[4] = function (T) {
    return '<div class="bw-in bw04"><div class="bw04-links"><figure class="bw04-f">' + BILD4.map(function (k, i) { return img(k, i ? '' : 'an'); }).join('') + '</figure></div>' +
      '<div class="bw04-rechts">' + kopf() + '<div class="bw04-liste">' + je(T, function (t, i) {
        return '<article class="bw04-z' + (t.voll ? ' voll' : '') + '" data-bild="' + (i % BILD4.length) + '"><h3 class="bw04-zeilen"><span>' + t.wt + '</span><span>' + t.tag + '. ' + t.mon + '</span><span>ab ' + t.zeit + ' Uhr</span></h3>' +
          '<div class="bw04-seite"><p class="bw-m">' + (t.voll ? 'Ausgebucht' : 'Noch ' + t.frei + ' von ' + t.n + ' frei') + '</p><p class="bw04-preis bw-z">' + t.preis + '</p>' + (t.voll ? '' : knopf(t, 'Buchen')) + '</div></article>';
      }) + '</div></div></div>';
  };

  /* 5 Der Ticketblock: so viele Tickets am Block, wie Plätze frei sind; das oberste reisst man ab */
  R[5] = function (T) {
    return '<div class="bw-in bw05">' + kopf() + '<div class="bw05-reihe">' + je(T, function (t) {
      var unter = Math.max(0, Math.min(t.frei, 14) - 1);
      return '<article class="bw05-b' + (t.voll ? ' voll' : '') + '"><div class="bw05-block" style="--n:' + unter + '">' +
        reihe(unter, function (k) { return '<i style="--i:' + (k + 1) + '"></i>'; }) +
        (t.voll ? '<div class="bw05-pappe"><p class="bw-m">Block leer</p><p class="bw-z">' + t.kurz + '</p></div>' :
          '<div class="bw05-ticket"><div class="bw05-haupt"><p class="bw-m">Culinarium · Momo x Rudi</p><p class="bw05-dat"><b class="bw-z">' + t.tag + '</b><span>' + t.wt + '<br>' + t.mon + ' ' + t.jahr + '</span></p>' +
          '<p class="bw-m">ab ' + t.zeit + ' · Haasemannstraße 13</p></div><div class="bw05-abriss"><b class="bw-z">' + t.eur + '</b><span class="bw-m">EUR</span></div></div>') +
        '</div><p class="bw05-zahl">' + (t.voll ? 'Alle ' + t.n + ' Tickets vergeben' : '<b class="bw-z">' + t.frei + '</b> ' + (t.frei === 1 ? 'Ticket' : 'Tickets') + ' am Block') + '</p>' + knopf(t, 'Ticket abreissen') + '</article>';
    }) + '</div></div>';
  };

  /* 6 Vierzehn Gläser: auf dem Tresen, gefüllte sind vergeben, die leeren warten; sie werden von links abgestellt */
  function glas(voll, i) {
    return '<svg class="' + (voll ? 'v' : '') + '" style="--i:' + i + '" viewBox="0 0 24 40" aria-hidden="true">' +
      (voll ? '<path class="fl" d="M4.3 8H19.7Q19 15.6 12 16.9Q5 15.6 4.3 8Z"/>' : '') +
      '<path class="gl" d="M3 4H21Q21 16.4 12 18Q3 16.4 3 4ZM12 18V35M6.5 36.2H17.5"/></svg>';
  }
  R[6] = function (T) {
    return '<div class="bw-in bw06">' + kopf('', 'Volle Gläser sind vergeben. Die leeren stehen schon da und warten auf dich.') + je(T, function (t) {
      var s = sitze(t);
      return '<article class="bw06-r' + (t.voll ? ' voll' : '') + '"><div class="bw06-dat"><b class="bw-z">' + t.tag + '</b><span><strong>' + t.wt + '</strong>' + t.mon + ' · ab ' + t.zeit + '</span></div>' +
        '<div class="bw06-tresen io" role="img" aria-label="' + fr(t) + '">' + s.map(function (w, i) { return glas(w, i); }).join('') + '</div>' +
        '<div class="bw06-rechts"><p class="bw-m">' + fr(t) + '</p><p class="bw06-preis bw-z">' + t.preis + '</p>' + knopf(t) + '</div></article>';
    }) + '</div>';
  };

  /* 7 Das Reservierungsbuch: eine Seite je Abend, vergebene Zeilen durchgestrichen, in die erste freie schreibt man sich ein */
  R[7] = function (T) {
    return '<div class="bw-in bw07"><div class="bw07-kopf">' + kopf('', 'Das Buch liegt an der Bar. Jede Zeile ist ein Platz an der Tafel. Such dir eine freie aus.') + '</div><div class="bw07-buch">' + je(T, function (t) {
      var erst = true;
      var zeilen = reihe(t.S, function (i) {
        if (i < t.weg) return '<p class="weg io" style="--i:' + i + '"><span>vergeben</span></p>';
        var h = '<button class="frei' + (erst ? ' erst' : '') + '" type="button" data-buchen="' + t.id + '"><span>' + (erst ? 'Dein Name hier?' : '') + '</span>' + (erst ? '<em>Eintragen ' + PFEIL + '</em>' : '') + '</button>';
        erst = false; return h;
      });
      return '<article class="bw07-s' + (t.voll ? ' voll' : '') + '"><header><p class="bw07-tag bw-z">' + t.wt + ', ' + t.tag + '. ' + t.mon + '</p><p class="bw-m">ab ' + t.zeit + ' · ' + t.preis + ' pro Person</p></header>' +
        '<div class="bw07-zeilen">' + zeilen + '</div><footer class="bw-m">' + (t.voll ? 'Seite voll, alle ' + t.n + ' Plätze vergeben' : 'Noch ' + t.frei + ' von ' + t.n + ' Zeilen frei') + '</footer></article>';
    }) + '</div></div>';
  };

  /* 8 Platzkarten auf der Tafel: je Abend eine gefaltete Karte auf dem Foto der gedeckten Tafel */
  R[8] = function (T) {
    return '<div class="bw08"><div class="bw-in">' + kopf() + '<div class="bw08-buehne"><figure class="bw08-f">' + img('tafelleer', '', '50% 50%') + '</figure><div class="bw08-karten">' + je(T, function (t, i) {
      return '<article class="bw08-k' + (t.voll ? ' voll' : '') + '" style="--i:' + i + '"><div class="bw08-vorn"><p class="bw-m">Culinarium · Momo x Rudi</p><p class="bw08-dat bw-z">' + t.wk + ' ' + t.kurz + '</p>' +
        '<p class="bw08-zeit">ab ' + t.zeit + ' · ' + t.preis + '</p><p class="bw08-frei bw-m">' + (t.voll ? 'Alle Plätze vergeben' : 'Noch ' + t.frei + ' Plätze frei') + '</p>' + knopf(t, 'Buchen') + '</div></article>';
    }) + '</div></div></div></div>';
  };

  /* 9 Anstossen: Freitag und Samstag eines Wochenendes als Paar, die beiden Hälften steigen getrennt auf und treffen sich an der Naht */
  var PAARE = [['toast', 'anstossen'], ['glaeser', 'kerze1'], ['kerze2', 'tablett'], ['service', 'kartglas']];
  function woche(d) { var x = new Date(d); x.setDate(x.getDate() - (d.getDay() + 6) % 7); return x.toDateString(); }
  R[9] = function (T) {
    var W = [], idx = {};
    T.forEach(function (t) { var k = woche(t.d); if (!(k in idx)) { idx[k] = W.length; W.push([]); } W[idx[k]].push(t); });
    return '<div class="bw-in bw09">' + kopf() + '<div class="bw09-wochen">' + W.map(function (w, wi) {
      var tage = w.map(function (t) { return t.tag + '.'; }).join(' + ') + ' ' + w[w.length - 1].mon;
      return '<div class="bw09-paar' + (w.length === 1 ? ' einzeln' : '') + '"><p class="bw09-we bw-m">Wochenende ' + tage + '</p><div class="bw09-naht io">' + w.map(function (t, i) {
        return '<article class="bw09-h' + (t.voll ? ' voll' : '') + '" style="--i:' + i + '"><figure>' + img(PAARE[wi % PAARE.length][i % 2]) + '</figure><div class="bw09-info">' +
          '<p class="bw09-dat"><b class="bw-z">' + t.tag + '</b><span><strong>' + t.wt + '</strong>ab ' + t.zeit + '</span></p><p class="bw-m">' + fr(t) + ' · ' + t.preis + '</p>' + knopf(t) + '</div></article>';
      }).join('') + '</div></div>';
    }).join('') + '</div></div>';
  };

  /* 10 Abende im Band: hohe Fotokarten zum Seitwärts-Blättern, am Ende die Warteliste */
  var BILD10 = ['kerze2', 'anstossen', 'kerze3', 'toast', 'glaeser', 'tablett'];
  R[10] = function (T) {
    return '<div class="bw10"><div class="bw-in bw10-kopf">' + kopf() + '<div class="bw10-pfeile"><button type="button" data-bw10="-1" aria-label="Zurück">' + PFEIL + '</button><button type="button" data-bw10="1" aria-label="Weiter">' + PFEIL + '</button></div></div>' +
      '<div class="bw10-band">' + je(T, function (t, i) {
        var s = sitze(t);
        return '<article class="bw10-k' + (t.voll ? ' voll' : '') + '"><figure>' + img(BILD10[i % BILD10.length]) + '</figure><div class="bw10-oben"><b class="bw-z">' + t.tag + '</b><span><strong>' + t.wt + '</strong>' + t.mon + ' · ab ' + t.zeit + '</span></div>' +
          '<div class="bw10-unten"><div class="bw10-sitze" aria-hidden="true">' + s.map(function (w) { return '<i class="' + (w ? 'weg' : '') + '"></i>'; }).join('') + '</div>' +
          '<p class="bw-m">' + fr(t) + '</p><p class="bw10-preis"><b class="bw-z">' + t.preis + '</b><span class="bw-m">pro Person</span></p>' + knopf(t) + '</div></article>';
      }) + '<a class="bw10-k bw10-ende" href="#warteliste"><p class="bw-z">Kein Abend passt?</p><span class="bw-m">Auf die Warteliste ' + PFEIL + '</span></a></div></div>';
  };

  /* 11 Der nächste Abend gross: Tage bis dahin, Foto durch die Tür, die übrigen Abende als ruhige Zeilen darunter */
  R[11] = function (T) {
    var n = T.filter(function (t) { return !t.voll; })[0] || T[0], rest = T.filter(function (t) { return t !== n; });
    var heute = new Date(); heute.setHours(0, 0, 0, 0);
    var tage = Math.round((n.d - heute) / 864e5);
    var bis = tage <= 0 ? '<b class="bw-z">Heute</b>' : tage === 1 ? '<b class="bw-z">Morgen</b>' : '<span class="bw-m">in</span><b class="bw-z">' + tage + '</b><span class="bw-m">Tagen</span>';
    var s = sitze(n);
    return '<div class="bw-in bw11"><div class="bw11-buehne"><figure class="bw11-f io">' + img('kerze3', '', '50% 50%') + '</figure><div class="bw11-text">' +
      '<p class="tb-kicker mono">Der nächste Abend</p><h2 class="tb-titel">Platz buchen.</h2><p class="bw11-in">' + bis + '</p>' +
      '<p class="bw11-wann">' + n.wt + ', ' + n.tag + '. ' + n.mon + ' ' + n.jahr + ', ab ' + n.zeit + '</p>' +
      '<div class="bw11-sitze" aria-hidden="true">' + s.map(function (w) { return '<i class="' + (w ? 'weg' : '') + '"></i>'; }).join('') + '</div><p class="bw-m">' + fr(n) + '</p>' +
      '<div class="bw11-preis"><b class="bw-z">' + n.preis + '</b><span>pro Person, Essen und Drinks</span></div>' + knopf(n) +
      '<p class="bw-hinweis mono">Vorschau · Termine und Zahlung sind nur simuliert</p></div></div>' +
      (rest.length ? '<div class="bw11-weitere"><p class="tb-kicker mono">Danach</p>' + je(rest, function (t) {
        return '<div class="bw11-z' + (t.voll ? ' voll' : '') + '"><b class="bw-z">' + t.kurz + '</b><span>' + t.wt + ' ab ' + t.zeit + '</span><span class="bw-m">' + (t.voll ? 'Ausgebucht' : 'Noch ' + t.frei + ' frei') + '</span><span class="bw11-p">' + t.preis + '</span>' + (t.voll ? '' : knopf(t, 'Buchen')) + '</div>';
      }) + '</div>' : '') + '</div>';
  };

  /* 12 Die Strichliste: an der Schiefertafel der Bar, je vergebenem Platz ein Kreidestrich, freie in Kerze */
  R[12] = function (T) {
    return '<div class="bw-in bw12"><div class="bw12-tafel">' + kopf('', 'Wie an der Bar: Jeder Kreidestrich ist ein vergebener Platz, die hellen in Kerze sind noch frei.') + '<div class="bw12-zeilen">' + je(T, function (t) {
      var g = '', k = 0;
      for (var a = 0; a < t.S; a += 5) {
        g += '<span class="bw12-g">';
        for (var b = a; b < Math.min(a + 5, t.S); b++, k++) g += '<i class="' + (b < t.weg ? 'w' : 'f') + (b - a === 4 ? ' quer' : '') + '" style="--i:' + k + ';--d:' + [-3, 2, -1, 3, 0][b % 5] + 'deg"></i>';
        g += '</span>';
      }
      return '<article class="bw12-r' + (t.voll ? ' voll' : '') + '"><p class="bw12-dat"><b class="bw-z">' + t.wk + ' ' + t.kurz + '</b><span class="bw-m">ab ' + t.zeit + '</span></p>' +
        '<div class="bw12-striche io" role="img" aria-label="' + fr(t) + '">' + g + '</div><p class="bw12-frei"><b class="bw-z">' + t.frei + '</b><span class="bw-m">frei</span></p>' +
        '<p class="bw12-preis bw-z">' + t.preis + '</p>' + knopf(t, 'Buchen') + '</article>';
    }) + '</div></div></div>';
  };

  /* 13 Die Einladung: je Abend ein Umschlag, die Karte schaut heraus und kommt beim Überfahren ein Stück weiter */
  R[13] = function (T) {
    return '<div class="bw-in bw13">' + kopf() + '<div class="bw13-reihe">' + je(T, function (t) {
      return '<article class="bw13-u' + (t.voll ? ' voll' : '') + '"><div class="bw13-umschlag"><div class="bw13-ruecken"></div><div class="bw13-karte"><p class="bw13-du">Du bist eingeladen</p>' +
        '<p class="bw13-dat bw-z">' + t.tag + '</p><p class="bw13-wann">' + t.wt + ', ' + t.mon + '<br>ab ' + t.zeit + '</p><p class="bw-m">' + (t.voll ? 'Alle Plätze vergeben' : 'Noch ' + t.frei + ' von ' + t.n + ' frei') + ' · ' + t.preis + '</p></div>' +
        '<div class="bw13-tasche"><p class="bw13-an bw-m">An dich · Haasemannstraße 13</p>' + (t.voll ? '<span class="bw13-siegel bw-m">voll</span>' : '') + '</div></div>' + knopf(t, 'Zusagen') + '</article>';
    }) + '</div></div>';
  };

  /* 14 An der Bonschiene: je Abend ein Bon wie am Pass, unter die Schiene geklemmt */
  R[14] = function (T) {
    var z = function (a, b, c) { return '<p' + (c ? ' class="' + c + '"' : '') + '><span>' + a + '</span><span>' + b + '</span></p>'; };
    return '<div class="bw-in bw14">' + kopf('', 'Wie die Bons am Pass, an dem Rudi anrichtet: ein Bon je Abend, darauf, was noch frei ist.') + '<div class="bw14-schiene"><div class="bw14-leiste"></div><div class="bw14-bons">' + je(T, function (t, i) {
      return '<article class="bw14-b' + (t.voll ? ' voll' : '') + '" style="--i:' + i + ';--rot:' + [-1.2, .9, -.6, 1.4][i % 4] + 'deg"><div class="bw14-papier io"><p class="c">WALK ON THE WILD SIDE</p><p class="c">HAASEMANNSTR. 13 · LINDEN</p><hr>' +
        '<p class="c gross">CULINARIUM</p><p class="c">MOMO X RUDI</p><hr>' + z('TAG', t.wk.toUpperCase() + ' ' + t.kurz + t.jahr) + z('BEGINN', t.zeit) + z('PLÄTZE', t.n) + z('VERGEBEN', t.g) + '<hr>' +
        z('FREI', t.frei, 'gross') + z('PRO PERSON', t.preis) + '<hr>' + (t.voll ? '<p class="c gross">*** AUSGEBUCHT ***</p>' : '<p class="c">DANKE, BIS BALD</p>') + '</div>' + knopf(t, 'Buchen') + '</article>';
    }) + '</div></div></div>';
  };

  /* 15 Die Gästewand: vierzehn Plätze in zwei Reihen wie die Tafel, vergebene zeigen einen Gast, freie sind leer und anklickbar */
  R[15] = function (T) {
    return '<div class="bw-in bw15">' + kopf('', 'Zwei Reihen zu sieben, wie an der Tafel. Wo noch niemand sitzt, ist dein Platz.') + '<div class="bw15-liste">' + je(T, function (t, ti) {
      var s = sitze(t), erst = true;
      return '<article class="bw15-r' + (t.voll ? ' voll' : '') + '"><div class="bw15-dat"><p class="bw15-tag"><b class="bw-z">' + t.tag + '</b><span><strong>' + t.wt + '</strong>' + t.mon + ' · ab ' + t.zeit + '</span></p>' +
        '<p class="bw-m">' + fr(t) + '</p><p class="bw15-preis bw-z">' + t.preis + '</p>' + knopf(t) + '</div><div class="bw15-tafel" style="--s:' + Math.ceil(t.S / 2) + '">' + s.map(function (w, i) {
          if (w) return '<figure class="bw15-t">' + img('t' + zwei((i + ti * 3) % 14 + 1)) + '</figure>';
          var h = '<button class="bw15-t frei' + (erst ? ' erst' : '') + '" type="button" data-buchen="' + t.id + '" aria-label="Platz buchen"><span>' + (erst ? 'Dein Platz' : '+') + '</span></button>';
          erst = false; return h;
        }).join('') + '</div></article>';
    }) + '</div></div>';
  };

  /* ---------- zeichnen, beobachten, buchen */
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('an'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -12% 0px' }) : null;

  function zeichnen(sofort) {
    var T = termine();
    [].forEach.call(document.querySelectorAll('.bw[data-bw]'), function (el) {
      var n = +el.dataset.bw;
      el.innerHTML = T.length ? R[n](T) : '<div class="bw-in">' + kopf() + leer() + '</div>';
      [].forEach.call(el.querySelectorAll('.io'), function (x) { if (sofort || !io) x.classList.add('an'); else io.observe(x); });
    });
  }
  zeichnen(false);

  document.addEventListener('click', function (e) {
    var b = e.target.closest('.bw [data-buchen]');
    if (b) { e.preventDefault(); var o = document.querySelector('[data-termine] [data-buchen="' + b.dataset.buchen + '"]'); if (o) o.click(); return; }
    var p = e.target.closest('[data-bw10]');
    if (p) { var band = p.closest('.bw10').querySelector('.bw10-band'); band.scrollBy({ left: +p.dataset.bw10 * band.clientWidth * .7, behavior: 'smooth' }); }
  });
  /* Rudis Zeilen: der Abend unter dem Finger bestimmt das Foto */
  function zeile(e) {
    var z = e.target.closest && e.target.closest('.bw04-z'); if (!z) return;
    var f = z.closest('.bw04').querySelector('.bw04-f');
    [].forEach.call(f.children, function (im, i) { im.classList.toggle('an', i === +z.dataset.bild); });
  }
  document.addEventListener('mouseover', zeile);
  document.addEventListener('focusin', zeile);
  /* nach dem Buchen neu zeichnen, ohne die Bewegung zu wiederholen */
  var dlg = document.getElementById('tb-dialog');
  if (dlg && 'MutationObserver' in window) new MutationObserver(function () { if (dlg.hidden) zeichnen(true); }).observe(dlg, { attributes: true, attributeFilter: ['hidden'] });
})();
