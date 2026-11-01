/* Demo-Weiche (Walk on the Wild Side, 1.11.2026): die Werkzeuge laufen online ohne Server.
   Jede Anfrage an den Server wird mit den aufgenommenen Beispielwerten beantwortet; Speichern und Veröffentlichen
   antworten «geklappt», ändern aber nichts. Wege mit «/» am Anfang werden auf den Ordner dieser Demo umgebogen. */
(function () {
  'use strict';
  var KARTE = window.__DEMO_KARTE || {}, POST = window.__DEMO_POST || {}, LINKS = window.__DEMO_LINKS || {};
  var me = document.currentScript && document.currentScript.src || '';
  var BASE = me.replace(/_demo\/shim\.js.*$/, '');           // Wurzel der Demo, endet mit «/»
  var U = new URL(BASE, location.href), ORIGIN = U.origin, BPATH = U.pathname;
  window.__DEMO = { BASE: BASE };

  function norm(p) {                                       // Weg relativ zur Wurzel (ohne «/» vorn), mit Suche
    try {
      var u = new URL(p, location.href);
      if (/^127\.0\.0\.1$|^localhost$/.test(u.hostname)) { var l = LINKS[u.port]; if (l) return { aussen: l + '' }; return { weg: u.pathname.replace(/^\//, '') + u.search, nur: u.pathname.replace(/^\//, '') }; }
      if (u.origin !== ORIGIN) return null;
      var pfad = u.pathname;
      if (pfad.indexOf(BPATH) === 0) pfad = pfad.slice(BPATH.length); else pfad = pfad.replace(/^\//, '');
      return { weg: pfad + u.search, nur: pfad };
    } catch (e) { return null; }
  }
  function ziel(p) {                                       // Datei in der Demo für einen Weg (oder null)
    var n = norm(p); if (!n) return null; if (n.aussen) return n.aussen;
    var w = n.weg, d = decodeURIComponent;
    var f = KARTE[w] || KARTE[n.nur];
    if (!f) { try { f = KARTE[d(w)] || KARTE[d(n.nur)]; } catch (e) {} }
    if (!f && /\/$/.test(n.nur)) f = KARTE[n.nur + 'index.html'];
    return BASE + (f || n.nur);
  }
  window.__demoZiel = ziel;

  function antwort(text, typ, st) { return new Response(text, { status: st || 200, headers: { 'Content-Type': typ || 'application/json' } }); }
  function postAntwort(m, p) {
    var n = norm(p) || { nur: '' }, k = m + ' ' + n.nur, r = POST[k];
    if (r) return fetchOrig(BASE + r.f).then(function (x) { return x.text(); }).then(function (t) { return antwort(t, r.ct, r.st >= 400 ? 200 : r.st); });
    return Promise.resolve(antwort(JSON.stringify({ ok: true, demo: true, hinweis: 'Demo: nichts wurde wirklich geändert.' })));
  }

  var fetchOrig = window.fetch.bind(window);
  window.fetch = function (inp, init) {
    var url = typeof inp === 'string' ? inp : (inp && inp.url) || String(inp);
    var m = ((init && init.method) || (inp && inp.method) || 'GET').toUpperCase();
    var n = norm(url);
    if (!n) return fetchOrig(inp, init);
    if (n.aussen) return fetchOrig(inp, init);
    if (m !== 'GET' && m !== 'HEAD') return postAntwort(m, url);
    var z = ziel(url);
    return fetchOrig(z, { method: m, cache: 'no-store' }).then(function (r) {
      if (r.ok) return r;
      return antwort(JSON.stringify({ ok: true, demo: true, liste: [], eintraege: [] }));
    }, function () { return antwort(JSON.stringify({ ok: true, demo: true })); });
  };

  var XO = XMLHttpRequest.prototype.open, XS = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.open = function (m, url) {
    var a = [].slice.call(arguments); this.__m = String(m).toUpperCase();
    if (norm(url) && this.__m === 'GET') a[1] = ziel(url);
    else if (norm(url) && this.__m !== 'GET') { this.__demoPost = url; a[0] = 'GET'; a[1] = BASE + '_demo/ok.json'; }
    return XO.apply(this, a);
  };
  XMLHttpRequest.prototype.send = function (b) { return XS.call(this, this.__demoPost ? null : b); };
  if (navigator.sendBeacon) navigator.sendBeacon = function () { return true; };
  if (window.EventSource) window.EventSource = function () { this.close = function () {}; this.addEventListener = function () {}; };

  /* src/href schon beim Setzen umbiegen (sonst geht die erste Anfrage an die Wurzel) */
  function lokal(v) { return typeof v === 'string' && (v.charAt(0) === '/' && v.charAt(1) !== '/' || /^https?:\/\/(127\.0\.0\.1|localhost)[:/]/.test(v)); }
  [['HTMLImageElement', 'src'], ['HTMLScriptElement', 'src'], ['HTMLLinkElement', 'href'], ['HTMLIFrameElement', 'src'], ['HTMLSourceElement', 'src'],
   ['HTMLVideoElement', 'src'], ['HTMLAudioElement', 'src'], ['HTMLAnchorElement', 'href'], ['HTMLVideoElement', 'poster']].forEach(function (z) {
    var K = window[z[0]]; if (!K) return;
    var d = Object.getOwnPropertyDescriptor(K.prototype, z[1]); if (!d || !d.set) return;
    Object.defineProperty(K.prototype, z[1], { configurable: true, enumerable: d.enumerable, get: d.get, set: function (v) { d.set.call(this, lokal(v) ? ziel(v) : v); } });
  });
  var setA = Element.prototype.setAttribute;
  Element.prototype.setAttribute = function (n, v) {
    if ((n === 'src' || n === 'href' || n === 'poster') && lokal(v)) v = ziel(v);
    return setA.call(this, n, v);
  };

  /* Wege in Attributen umbiegen (src, href, srcset, poster, action), auch für später eingefügte Teile */
  var ATTR = ['src', 'href', 'poster', 'data-src'];
  function biege(el) {
    if (!el || el.nodeType !== 1) return;
    for (var i = 0; i < ATTR.length; i++) {
      var a = ATTR[i], v = el.getAttribute(a);
      if (!v || el.__demoGebogen === v) continue;
      if (/^(#|data:|blob:|mailto:|tel:|javascript:|https?:\/\/(?!127\.0\.0\.1|localhost))/i.test(v)) continue;
      if (v.charAt(0) === '/' || /^https?:\/\/(127\.0\.0\.1|localhost)/.test(v)) {
        var z = ziel(v); if (z) { el.__demoGebogen = z; el.setAttribute(a, z); if (a === 'href' && el.tagName === 'A' && /^https:\/\/claude\.ai/.test(z)) el.target = '_blank'; }
      }
    }
    var st = el.getAttribute('style');
    if (st && /url\(\s*['"]?\/(?!\/)/.test(st)) setA.call(el, 'style', st.replace(/url\(\s*(['"]?)(\/(?!\/)[^'")]+)\1\s*\)/g, function (_, q, p) { return 'url(' + q + ziel(p) + q + ')'; }));
    if (el.tagName === 'STYLE' && /url\(\s*['"]?\/(?!\/)/.test(el.textContent)) el.textContent = el.textContent.replace(/url\(\s*(['"]?)(\/(?!\/)[^'")]+)\1\s*\)/g, function (_, q, p) { return 'url(' + q + ziel(p) + q + ')'; });
    var ss = el.getAttribute('srcset');
    if (ss && /(^|,)\s*\//.test(ss)) el.setAttribute('srcset', ss.replace(/(^|,\s*)(\/[^\s,]+)/g, function (_, a, p) { return a + ziel(p); }));
  }
  function alle(root) { if (root.nodeType !== 1) return; biege(root); var l = root.querySelectorAll('[src],[href],[srcset],[poster],[data-src],[style],style'); for (var i = 0; i < l.length; i++) biege(l[i]); }
  new MutationObserver(function (ms) {
    for (var i = 0; i < ms.length; i++) {
      var m = ms[i];
      if (m.type === 'attributes') biege(m.target);
      else for (var j = 0; j < m.addedNodes.length; j++) alle(m.addedNodes[j]);
    }
  }).observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['src', 'href', 'srcset', 'poster', 'data-src', 'style'] });
  document.addEventListener('DOMContentLoaded', function () { alle(document.documentElement); });

  /* Seitenwechsel per Skript auf andere Wege («location.href = '/…'») */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
    var h = a.getAttribute('href'); if (h && h.charAt(0) === '/') { e.preventDefault(); location.href = ziel(h); }
  }, true);
  var asg = window.Location && Location.prototype.assign;
  if (asg) Location.prototype.assign = function (u) { var n = norm(u); return asg.call(this, n ? ziel(u) : u); };
  var rep = window.Location && Location.prototype.replace;
  if (rep) Location.prototype.replace = function (u) { var n = norm(u); return rep.call(this, n ? ziel(u) : u); };
  var wo = window.open; window.open = function (u) { var a = [].slice.call(arguments); if (u && norm(u)) a[0] = ziel(u); return wo.apply(window, a); };

  /* kleines Band: «Demo mit Beispielwerten» */
  document.addEventListener('DOMContentLoaded', function () {
    if (window.top !== window || document.getElementById('demoBand')) return;
    var b = document.createElement('div'); b.id = 'demoBand';
    b.textContent = 'Demo mit Beispielwerten · nichts wird wirklich geändert';
    b.setAttribute('style', 'position:fixed;left:50%;bottom:10px;transform:translateX(-50%);z-index:2147483646;pointer-events:none;padding:6px 14px;border-radius:999px;font:500 10px/1.2 system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#f8f3eb;background:rgba(19,14,13,.78);box-shadow:0 0 0 1px rgba(216,178,100,.5);white-space:nowrap;max-width:calc(100vw - 24px);overflow:hidden;text-overflow:ellipsis');
    document.body.appendChild(b);
  });
})();
