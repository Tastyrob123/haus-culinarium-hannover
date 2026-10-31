#!/usr/bin/env python3
"""Werkbank Culinarium (Vorlage Schäfli, dort Schlössli und Ruedihus): Fuss «Alles auf einen Blick» als Fächer mit freigestellten Objekten (12.10.2026, Master 5b Punkt 23).

Vorn das gewählte Objekt, je zwei dahinter kleiner und leiser; Pfeile, Tippen, Pfeiltasten, Wischen. Das vordere Objekt und «Öffnen» führen zum Weg.
Über dem Fächer steht die Überschrift allein, ohne Zeichen (Robert 12.10.2026). Die Objekte kommen aus objekte_bau.py (eigene Stücke des Hauses),
nach_bau() legt sie als WebP nach werkbank/eigen/. Bewegt wird nur über transform und opacity.
Eingehängt in haus.py: wege_abschnitt = fuss_faecher.abschnitt (Haken des Kits), CSS am Dateiende."""
import html, os
import rh_werkzeuge as _WK

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
OBJ = os.path.join(W, 'objekte')

WEGE_OBJEKTE = {   # Weg → (Datei in objekte/, Bildbeschreibung, Satz)
    'website': ('website', 'Ein Laptop mit der neuen Startseite von Culinarium', 'Der Entwurf mit allen Seiten: der Abend, die Plakate, das Haus, die Leute, der Weg und Dirty Chicken.'),
    'gaeste': ('gaeste', 'Ein Laptop mit «Platz buchen»', 'Platz buchen, die Warteliste, das Menü, die Zeiten, die Fragen und der Weg.'),
    'unterlagen': ('unterlagen', 'Die Karten der Abende, neu gesetzt', 'Die Karte jedes Abends mit Rudis Gängen und Momos Drinks.'),
    'drucksachen': ('drucksachen', 'Drucksachen für Tafel und Tür', 'Ideen für Papier, von der Karte am Platz bis zum Briefbogen.'),
    'etiketten': ('etiketten', 'Vier Untersetzer für die Theke', 'Zwölf Untersetzer für Momos Drinks, im Kleid eurer Plakate.'),
    'feed': ('feed', 'Ein Laptop mit dem Feed für Instagram', 'Ein Feed aus euren eigenen Fotos und Plakaten, im Raster eigens für Culinarium geplant.'),
    'material': ('material', 'Drucksachen und ein Untersetzer', 'Jede Datei dieses Entwurfs in einem Ordner, zum Durchsehen und Laden.'),
    'geprueft': ('geprueft', 'Ein Blatt mit vier Haken und einem Stempel', 'Was durchgegangen wurde, in Alltagssprache, und was offen bleibt.'),
    'maison': ('maison', 'Ein Laptop mit dem Eingang zu den Werkzeugen', 'Der Eingang für euch alle, von dort geht es in jedes Werkzeug.'),
    'bureau': ('bureau', 'Ein Laptop mit dem Werkzeug für die Website', 'Hier tragt ihr Abende ein und schreibt in die Website, zuerst in der Vorschau.'),
    'carte': ('carte', 'Ein Laptop mit dem Werkzeug für die Karten', 'Gänge und Drinks je Abend, daraus die Karte am Platz und auf der Website.'),
    'reception': ('reception', 'Ein Laptop mit dem Werkzeug für die Gäste', 'Buchungen, Warteliste und Fragen an einem Ort, mit einer Antwort zu jeder.'),
    'livre': ('livre', 'Ein Laptop mit dem Werkzeug für die Marke', 'Fotos, Plakate, Wortmarke und Farben als Dateien, dazu die Hausregeln.'),
    'registre': ('registre', 'Ein Laptop mit dem Werkzeug für die Besuche', 'Woher die Gäste kommen und was sie ansehen, ohne Cookies, hier mit Beispielwerten.'),
    'imprimerie': ('imprimerie', 'Ein Laptop mit dem Werkzeug für Plakate und Papier', 'Das Plakat für den nächsten Abend, geändert auf dem Blatt, die PDF für die Druckerei.'),
    'analyse': ('analyse-h', 'Ein Laptop mit dem Befund', 'Wie Culinarium heute im Netz steht, mit allen Punkten und ihren Bildern.'),
    'vorschlag': ('vorschlag', 'Culinarium auf einem hellen Blatt', 'Ein Vorschlag: was euch gehört, die Betreuung und wo die KI arbeitet.'),
}
BEREIT = os.path.exists(os.path.join(OBJ, 'website.png'))


def bilder():
    """Objekte als WebP nach werkbank/eigen/ (nur wenn neu); erst fertig schreiben, dann austauschen."""
    from PIL import Image
    z = os.path.join(ROOT, 'werkbank', 'eigen')
    os.makedirs(z, exist_ok=True)
    for name in [v[0] for v in WEGE_OBJEKTE.values()] + ['analyse-h']:   # analyse-h: Handy für die Kapitel-Übersicht (rh_kapitel.py)
        q, ziel = os.path.join(OBJ, name + '.png'), os.path.join(z, f'fo-{name}.webp')
        if os.path.exists(q) and (not os.path.exists(ziel) or os.path.getmtime(ziel) < os.path.getmtime(q)):
            tmp = ziel + f'.{os.getpid()}.tmp'
            Image.open(q).save(tmp, 'WEBP', quality=86, method=6)
            os.replace(tmp, ziel)


def abschnitt(wege):
    e = html.escape
    wege = [(n, t, h) for n, t, h in wege if n in WEGE_OBJEKTE and os.path.exists(os.path.join(OBJ, WEGE_OBJEKTE[n][0] + '.png'))]
    # Werkbank-Regel 15 (17.10.2026): Laptops nur Website, Besucherbuch und Analyse; die Analyse rückt hinter die Drucksachen,
    # damit zwischen zwei Laptops je fünf Plätze liegen (vorn und je zwei Nachbarn sind sichtbar, also nie zwei Laptops im Blick)
    namen = [n for n, _, _ in wege]
    if 'analyse' in namen and 'drucksachen' in namen:
        a = wege.pop(namen.index('analyse'))
        wege.insert([n for n, _, _ in wege].index('drucksachen') + 1, a)
    # Robert 18.10.2026 ~01:50: «unten sind 18 Sachen … reduzieren auf eine überschaubare Menge … nicht sagen, alles im Blick, sondern die wichtigsten
    # Sachen im Blick»: sechs Stücke; die Website ist der einzige Laptop (Regel 15), die Analyse kommt als Handy
    WICHTIG = ['website', 'maison', 'unterlagen', 'gaeste', 'analyse', 'drucksachen', 'etiketten']
    wege = sorted([w for w in wege if w[0] in WICHTIG], key=lambda w: WICHTIG.index(w[0]))
    k, halb = len(wege), len(wege) // 2
    pf_l = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>'
    pf_r = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'
    pf_o = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
    blaetter = ''.join(f'<a class="fblatt" href="{h}" target="_blank" rel="noopener" data-i="{i}" data-p="{((i + halb) % k) - halb}">'
                       f'<img src="eigen/fo-{WEGE_OBJEKTE[n][0]}.webp" width="1000" height="1000" alt="{e(WEGE_OBJEKTE[n][1])}" loading="lazy" decoding="async"></a>'
                       for i, (n, t, h) in enumerate(wege))
    texte = ''.join(f'<div{" class=\"an\"" if i == 0 else ""}><h3>{e(t)}</h3><p>{e(WEGE_OBJEKTE[n][2])}</p><a class="kn kn--klein" href="{h}" target="_blank" rel="noopener">Öffnen<i>{pf_o}</i></a></div>'
                    for i, (n, t, h) in enumerate(wege))
    return f"""<nav class="in wege wf" aria-label="Das Wichtigste von Culinarium">
  <div class="wf__kopf"><b class="wege__t">Das Wichtigste von Culinarium</b></div>
  <div class="wfa" data-wfa aria-roledescription="Karussell" aria-label="Das Wichtigste von Culinarium">
    <div class="wfa__b">{blaetter}</div>
    <div class="wfa__fuss">
      <button type="button" class="wf__pf" data-f="-1" aria-label="Zurück">{pf_l}</button>
      <div class="wfa__texte" aria-live="polite">{texte}</div>
      <button type="button" class="wf__pf" data-f="1" aria-label="Weiter">{pf_r}</button>
    </div>
    <p class="wfa__zahl"><span data-f-zahl>1</span> / {k}</p>
  </div>
</nav>
<script>
(function () {{
  var f = document.querySelector('.wf [data-wfa]'); if (!f) return;
  var bl = [].slice.call(f.querySelectorAll('.fblatt')), tx = [].slice.call(f.querySelectorAll('.wfa__texte>div')), zahl = f.querySelector('[data-f-zahl]'), n = bl.length, ist = 0, halb = Math.floor(n / 2);
  function zeige(k) {{
    ist = (k % n + n) % n;
    bl.forEach(function (b, i) {{ var p = ((i - ist + n + halb) % n) - halb; b.setAttribute('data-p', p); b.setAttribute('aria-hidden', p !== 0); b.tabIndex = p === 0 ? 0 : -1; }});
    tx.forEach(function (t, i) {{ t.classList.toggle('an', i === ist); [].forEach.call(t.querySelectorAll('a'), function (a) {{ a.tabIndex = i === ist ? 0 : -1; }}); }});
    if (zahl) zahl.textContent = ist + 1;
  }}
  [].forEach.call(f.querySelectorAll('[data-f]'), function (b) {{ b.addEventListener('click', function () {{ zeige(ist + (+b.getAttribute('data-f'))); }}); }});
  bl.forEach(function (b, i) {{ b.addEventListener('click', function (e) {{ if (i !== ist) {{ e.preventDefault(); zeige(i); }} }}); }});
  f.setAttribute('tabindex', '0');
  f.addEventListener('keydown', function (e) {{ if (e.key === 'ArrowRight') zeige(ist + 1); else if (e.key === 'ArrowLeft') zeige(ist - 1); }});
  var x0 = null, st = f.querySelector('.wfa__b');
  st.addEventListener('touchstart', function (e) {{ x0 = e.touches[0].clientX; }}, {{ passive: true }});
  st.addEventListener('touchend', function (e) {{ if (x0 === null) return; var d = e.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(d) > 40) zeige(ist + (d < 0 ? 1 : -1)); }}, {{ passive: true }});
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es, o) {{ es.forEach(function (x) {{ if (x.isIntersecting) {{ f.classList.add('da'); o.disconnect(); }} }}); }}, {{ threshold: .25 }}).observe(f); else f.classList.add('da');
  zeige(0);
}})();
</script>"""


CSS = """
/* ---------- Fuss «Alles auf einen Blick» als Fächer (fuss_faecher.py, 12.10.2026): nur transform und opacity ---------- */
.fuss:has(.wf){background:linear-gradient(rgba(23,13,6,.8),rgba(23,13,6,.8)),var(--muster) 50% 0/var(--musterb) auto,var(--tief)}
.fuss .wf{display:block;text-align:center;overflow:hidden}
.fuss .wf .wege__t{display:block;font-family:var(--serif);font-weight:700;font-size:clamp(2.1rem,5.5vw,5.9rem);line-height:1.04;margin:0;color:#fbf5ea}
.wf .wfa{position:relative;margin-top:clamp(10px,1.6vw,30px);outline:none}
.wf .wfa__b{position:relative;height:clamp(240px,34vw,500px)}
.wf .wfa__b::before{content:'';position:absolute;left:50%;top:50%;width:min(70vw,760px);height:min(52vw,560px);transform:translate(-50%,-50%);border-radius:50%;
  background:radial-gradient(closest-side,rgba(243,205,148,.13),rgba(243,205,148,.04) 55%,transparent);pointer-events:none}
.wf .fblatt{position:absolute;left:50%;top:0;height:100%;aspect-ratio:1;margin:0;display:block;cursor:pointer;
  --x:0%;--s:.5;--o:0;transform:translateX(calc(-50% + var(--x))) scale(var(--s));opacity:var(--o);pointer-events:none;
  transition:transform .95s cubic-bezier(.2,.8,.2,1),opacity .6s cubic-bezier(.2,.8,.2,1)}
.wf .fblatt img{width:100%;height:100%;object-fit:contain;display:block}
.wf .fblatt[data-p="0"]{--x:0%;--s:1;--o:1;z-index:5;pointer-events:auto}
.wf .fblatt[data-p="-1"]{--x:-74%;--s:.66;--o:.5;z-index:4;pointer-events:auto}
.wf .fblatt[data-p="1"]{--x:74%;--s:.66;--o:.5;z-index:4;pointer-events:auto}
.wf .fblatt[data-p="-2"]{--x:-128%;--s:.46;--o:.2;z-index:3;pointer-events:auto}
.wf .fblatt[data-p="2"]{--x:128%;--s:.46;--o:.2;z-index:3;pointer-events:auto}
.wf .fblatt[data-p="-3"]{--x:-170%}.wf .fblatt[data-p="3"]{--x:170%}
.wf .wfa:not(.da) .fblatt{--x:0%;--s:.7;--o:0}
.wf .wfa__fuss{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:clamp(14px,3vw,50px);max-width:820px;margin:0 auto}
.wf .wfa__texte{display:grid;text-align:center}
.wf .wfa__texte>div{grid-area:1/1;display:flex;flex-direction:column;align-items:center;opacity:0;visibility:hidden;transform:translateY(14px);transition:opacity .4s ease,transform .6s ease,visibility 0s .45s}
.wf .wfa__texte>div.an{opacity:1;visibility:visible;transform:none;transition:opacity .6s ease .15s,transform .8s ease .15s}
.wf .wfa__texte h3{margin:0;font-family:var(--serif);font-weight:700;font-size:clamp(1.7rem,2.7vw,2.7rem);line-height:1.08;color:#fbf5ea}
.wf .wfa__texte h3::after{content:'';display:block;width:64px;height:2px;margin:clamp(12px,1.3vw,18px) auto 0;background:var(--gold);opacity:.85}
.wf .wfa__texte p{margin:clamp(12px,1.2vw,16px) auto 0;max-width:46ch;font-size:clamp(1.04rem,1.14vw,1.16rem);line-height:1.56;color:rgba(251,245,234,.84)}
.wf .wfa__texte .kn{margin-top:clamp(18px,1.8vw,26px);align-self:center}
.wf__pf{width:56px;height:56px;border-radius:50%;display:grid;place-items:center;cursor:pointer;color:#fbf5ea;border:1px solid rgba(201,133,67,.45);
  background:radial-gradient(circle at 50% 30%,#4b2f19,#321f10 60%,#1f1209);box-shadow:0 14px 22px -12px rgba(0,0,0,.9),inset 0 1px 0 rgba(255,236,200,.14);transition:border-color .4s}
.wf__pf svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.wf__pf:hover{border-color:rgba(243,205,148,.9)}
.wf .wfa__zahl{max-width:none;margin:clamp(18px,2vw,28px) 0 0;text-align:center;font-family:var(--mono);font-size:.82rem;letter-spacing:.24em;color:var(--gold)}
@media(max-width:700px){
  .wf .wfa__b{height:min(78vw,340px)}
  .wf .fblatt[data-p="-1"]{--x:-62%;--s:.55;--o:.4}.wf .fblatt[data-p="1"]{--x:62%;--s:.55;--o:.4}
  .wf .fblatt[data-p="-2"],.wf .fblatt[data-p="2"]{--o:0}
  .wf .wfa__fuss{grid-template-columns:1fr 1fr;justify-items:center;row-gap:20px}
  .wf .wfa__texte{grid-column:1/-1;grid-row:1}
  .wf .wfa__fuss>button:first-of-type{justify-self:end}.wf .wfa__fuss>button:last-of-type{justify-self:start}
}
@media(prefers-reduced-motion:reduce){.wf .fblatt,.wf .wfa__texte>div{transition:none}}
"""
