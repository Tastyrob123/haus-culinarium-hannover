#!/usr/bin/env python3
"""Werkbank Taverne zum Schäfli, Kapitel «Ihre Werkzeuge» (Vorlage Schlössli) (Station 11, 19.10.2026; Aufbau, Stil und Skript aus rh_werkzeuge.py des Landgasthofs Ruedihus,
dort aus dem Waldhotel Doldenhorn und dem Carlton-Europe, nur gelesen und kopiert). Ein Laptop für alle sieben: La Maison als Eingang, dann die sechs Werkzeuge
(Namen aus _werkzeuge/oberflaeche/kleid/culinarium.js). Reiter oben und Pfeile; nur der
Bildschirm blendet über, rechts wechselt der Text. Ein Klick auf den Bildschirm lädt das echte Werkzeug in den Laptop (29.10.2026, über den Werkbank-Server als gleiche Herkunft); gross öffnet es der Knopf daneben.

  Gehäuse     geraete/laptop-geraet.png (Blender, aus der Werkbank des Ruedihus übernommen), Lage des Bildschirms aus geraete/laptop.json
  Bildschirme ansichten/Werkzeuge/<schlüssel>.jpg (sb_werkzeuge.js, Aufnahme der gelieferten Werkzeuge)
  Adressen    aus den Paketen der sieben Werkzeug-Chats: ../_kette/11-werkbank/werkzeuge/<teil>/stand.json, Feld «adresse», erst wenn «liegt vor»
              oder «bestätigt». Bis dahin steht im Laptop ein Platzhalter (nur lokal)."""
import html, json, os
import namen_fall as NF
from PIL import Image

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJEKT = os.path.dirname(os.path.dirname(ROOT))   # Projektordner Culinarium (ROOT ist website/_werkbank)
GERAET = os.path.join(W, 'geraete', 'laptop-geraet.png')
_L = json.load(open(os.path.join(W, 'geraete', 'laptop.json'), encoding='utf-8'))
FOTOS = os.path.join(W, 'ansichten', 'Werkzeuge')
LJ = {'fenster': list(_L['fenster']), 'schirm': list(_L['schirm'])}
ONLINE = os.environ.get('ONLINE') == '1'
TEIL = {'maison': 'zentrale', 'bureau': 'website', 'carte': 'karten', 'reception': 'gaeste', 'livre': 'marke', 'registre': 'besuche', 'imprimerie': 'druck'}


def stand(key):
    p = os.path.join(PROJEKT, '_kette', '11-werkbank', 'werkzeuge', TEIL[key], 'stand.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def _weg(key):
    """Adresse des Werkzeugs, wie sein Chat sie gemeldet hat; nur wenn es vorliegt."""
    st = stand(key)
    if ADRESSEN.get(key):   # Culinarium: die Adresse aus werkzeuge.json (aus den Lieferungen, immer 127.0.0.1) geht vor
        st = dict(st, adresse=ADRESSEN[key])
    if st.get('adresse'):   # Fehlerbuch 10a: Wege zwischen Werkzeugen immer 127.0.0.1, nie localhost
        st['adresse'] = st['adresse'].replace('://localhost:', '://127.0.0.1:')
    if st.get('zustand') in ('liegt vor', 'bestätigt') and st.get('adresse'):
        return st['adresse']
    # Robert 20.10.2026 «Da fehlt ein Tool»: alle sieben stehen immer in der Werkbank. Solange ein Werkzeug-Chat noch baut, zeigt sie seinen Stand
    # (gemeldete Adresse oder sein Prüfserver), sofern der antwortet.
    weg = st.get('adresse') or PRUEF.get(key, '')
    if weg and not ONLINE:
        try:
            import urllib.request
            if urllib.request.urlopen(weg, timeout=4).status == 200:
                return weg
        except Exception:
            pass
    return ''


PRUEF = {}   # Prüfserver der Werkzeug-Chats (Ports 9061–9067, AUFTRAG-GEMEINSAM.md); Adresse aus ihrer Lieferung, siehe ADRESSEN
ADRESSEN = {}   # wird aus _werkbank/werkzeuge.json gelesen (Adressen, die die Werkzeug-Chats als «fertig» melden)
try:
    ADRESSEN = json.load(open(os.path.join(W, 'werkzeuge.json'), encoding='utf-8'))
    PRUEF.update(ADRESSEN)
except Exception:
    pass


def quelle(name):
    eigen = os.path.join(FOTOS, name + '.jpg')
    return eigen if os.path.exists(eigen) else None


# Schlüssel, Name, Rolle, Satz, Punkte, Ansichten [(Bild, Name)], Öffnen, Anleitung, liefert
WERKZEUGE = [
    ('maison', 'La Maison', 'Der Eingang', 'Wer die Werkzeuge öffnet, landet hier: Culinarium, die sechs Werkzeuge und bei jedem, was gerade zu tun ist.',
     ['Alle Werkzeuge an einem Ort', 'Bei jedem, was offen ist', 'Ein Rundgang für alle, die neu dazukommen'],
     [('maison', 'Der Eingang')], _weg('maison'), '', 'culinarium-maison'),
    ('bureau', 'Le Bureau', 'Website', 'Ein neuer Abend mit Tag, Beginn, Preis, Plätzen und seinem Plakat, ein frischer Satz, ein neues Foto von der Tafel. Alles wartet zuerst im Entwurf; auf die Website kommt es erst mit «Veröffentlichen».',
     ['Die nächsten Abende pflegen, je Abend mit Plakat', 'Jeden Text und jedes Foto dort ändern, wo es steht', 'Jeder frühere Stand lässt sich zurückholen'],
     [('bureau', 'Übersicht'), ('bureau-2', 'Termine')], _weg('bureau'), '', 'culinarium-bureau'),
    ('carte', 'La Carte', 'Karten', 'Zu jedem Abend gehört eine Karte am Platz: Gang für Gang Rudis Teller und Momos Drink, vom Apéritif bis zum Absacker. Was hier steht, steht sofort auf der Karte, so wie sie auf dem Tisch liegt, und als PDF zum Drucken.',
     ['Teller und Drink je Gang eintragen', 'Die Karte als PDF für den Tisch', 'Frühere Abende mit ihrer Karte'],
     [('carte', 'Der nächste Abend'), ('carte-2', 'Die Karte')], _weg('carte'), '', 'culinarium-carte'),
    ('reception', 'La Réception', 'Gäste', 'Wer auf die Warteliste will, einen Platz am Abend sucht, die lange Tafel für eine eigene Feier möchte oder eine Frage hat: Alles kommt hier an, nach Art geordnet, mit einem Brief als Entwurf für die Antwort.',
     ['Warteliste, Plätze, Feiern und Nachrichten', 'Zu jeder Anfrage ein Antwortbrief als Entwurf', 'Was Gäste im Chat fragen und was der Chat weiß'],
     [('reception', 'Übersicht'), ('reception-2', 'Nach Art')], _weg('reception'), '', 'culinarium-reception'),
    ('livre', 'Le Livre', 'Marke', 'Ein Magazin fragt nach einem Foto der Tafel, die Druckerei nach der Wortmarke. Beides liegt hier bereit, zusammen mit Farben, Schriften und den Plakaten.',
     ['Fotos nach Tafel, Bar, Tellern und Drinks', 'Wortmarke und Farben der Plakate', 'Fremde Entwürfe gegen die Marke prüfen'],
     [('livre', 'Übersicht'), ('livre-2', 'Arbeiten')], _weg('livre'), '', 'culinarium-livre'),
    ('registre', 'Le Registre', 'Besuche', 'Wer sieht sich die Seite an, aus Hannover oder von weiter weg? Und welche Seiten lagen vor dem gebuchten Platz? Hier steht es, gezählt ohne Cookies und ohne Namen.',
     ['Woher die Besuche kommen', 'Welche Seiten vor dem Platz an der Tafel lagen', 'Im Entwurf mit erfundenen Zahlen'],
     [('registre', 'Übersicht'), ('registre-2', 'Herkunft und Seiten')], _weg('registre'), '', 'culinarium-registre'),
    ('imprimerie', 'L’Imprimerie', 'Plakate und Papier', 'Jeder Abend hat sein Plakat. Ihr beschreibt den Abend, und die Werkstatt malt dafür drei bis fünf neue Plakate im Stil eurer bisherigen, vorn und hinten. Ihr wählt eins und setzt im Editor Texte, Datum und Farbe.',
     ['«Abend beschreiben»: drei bis fünf neue Plakate, vorn und hinten', '«Plakat-Motive»: Rudis eigene Illustrationen', 'PDF in A3, Bilder für Instagram und die Story'],
     [('imprimerie', 'Übersicht'), ('imprimerie-2', 'Abend beschreiben'), ('imprimerie-3', 'Editor')], _weg('imprimerie'), '', 'culinarium-imprimerie'),   # Neuaufnahme 29.10. (Oberchef): Übersicht, Abend mit 3 fertigen Vorschlägen, Editor
]
# Die Namen der sieben Werkzeuge für Culinarium, eine Stelle: das Kleid der Werkzeuge (_werkzeuge/oberflaeche/kleid/culinarium.js, WO_HAUS.namen, Schreiber: Chat «culinarium-maison»).
# Bis Robert gewählt hat, stehen dort die Arbeitsnamen; die Liste hier gilt nur, wenn das Kleid fehlt. Schlüssel, Dateinamen und Adressen bleiben die des Stamms.
NAMEN_HAUS = {'maison': 'La Maison', 'bureau': 'Le Bureau', 'carte': 'La Carte', 'reception': 'La Réception',
              'livre': 'Le Livre', 'registre': 'Le Registre', 'imprimerie': 'L’Imprimerie'}
try:
    import re as _re
    _k = open(os.path.join(PROJEKT, '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium.js'), encoding='utf-8').read()
    _n = dict(_re.findall(r"(\w+): '([^']+)'", _re.search(r'namen:\s*\{([^}]*)\}', _k).group(1)))
    NAMEN_HAUS.update({k: _n[t] for k, t in TEIL.items() if t in _n})
except Exception:
    pass
for _i, _w in enumerate(WERKZEUGE):
    WERKZEUGE[_i] = (_w[0], NAMEN_HAUS[_w[0]]) + tuple(_w[2:])
NAMEN = {w[0]: w[1] for w in WERKZEUGE}
STUBE = NAMEN['maison']
import rh_strom as SB  # noqa: E402  (nach NAMEN: rh_strom liest die Namen)
STROM = []
PLATZ = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='


def setze(**neu):
    for key, d in neu.items():
        for i, w in enumerate(WERKZEUGE):
            if w[0] == key:
                w = list(w)
                for f, j in (('name', 1), ('rolle', 2), ('satz', 3), ('punkte', 4), ('ansichten', 5), ('auf', 6), ('anl', 7)):
                    if f in d:
                        w[j] = d[f]
                WERKZEUGE[i] = tuple(w)


# Anleitungen, wie die Werkzeug-Chats sie liefern (werkzeuge.json, Schlüssel «<werkzeug>:anleitung»); nur wenn das Werkzeug selbst da ist
for _w in list(WERKZEUGE):
    if _w[6] and ADRESSEN.get(_w[0] + ':anleitung'):
        setze(**{_w[0]: dict(anl=ADRESSEN[_w[0] + ':anleitung'])})


def bilder(webp):
    """Gehäuse und Bildschirme nach werkbank/img. webp(quelle, name, breite, q) aus wb_kapitel."""
    m = {'ins-geraet': webp(Image.open(GERAET).convert('RGBA'), 'ins-geraet', 2000, 88)}
    verh = LJ['fenster'][0] / LJ['fenster'][1]
    for key, *_r in WERKZEUGE:
        for b, _ in _r[4]:
            q = quelle(b)
            if not q:
                continue
            im = Image.open(q).convert('RGB')
            if abs(im.width / im.height - verh) > .002:   # oben bündig auf das Format des Bildschirms
                im = im.crop((0, 0, im.width, min(im.height, round(im.width / verh)))) if im.width / im.height < verh else im.crop(((im.width - round(im.height * verh)) // 2, 0, (im.width + round(im.height * verh)) // 2, im.height))
            m['ins-bild-' + b] = webp(im, 'ins-bild-' + b, 1800, 86)
    return m


def abschnitt(k, ph):
    """k: Bausteine aus bau.py; ph: kapitel.platzhalter."""
    M, kn = k['m'], k['kn']
    siegel = '<svg class="ins-s" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22.5"/><path d="m15.5 24.5 5.5 5.5 11-12"/></svg>'
    pf_l = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>'
    pf_r = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'
    zeiger = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 3.5v14.2l3.9-3.2 2.7 6 2.3-1-2.7-5.9 5.3-.4z"/></svg>'
    gw, gh = M['ins-geraet']
    sx, sy, sw, sh = (v * 100 for v in LJ['schirm'])
    fb = LJ['fenster'][0]
    reiter = ''.join(f'<button type="button" class="ins-r" data-i="{i}" aria-selected="{"true" if i == 0 else "false"}" role="tab"><small>{e(rolle)}</small><span>{e(name)}</span></button>'
                     for i, (_, name, rolle, *_x) in enumerate(WERKZEUGE))
    # Reihen gleichmässig (Robert 20.10.2026): sieben Reiter als vier und drei, die zweite Reihe mittig, nie sechs und einer allein
    _n = len(WERKZEUGE); _vorn = -(-_n // 2) if _n > 4 else _n
    reiter = reiter.replace('</button>', '</button><i class="ins-bruch" aria-hidden="true"></i>', _vorn).replace('<i class="ins-bruch" aria-hidden="true"></i>', '', _vorn - 1) if _n > 4 else reiter
    schirme, minis, texte, fehlt = [], [], [], []
    for i, (key, name, rolle, satz, punkte, ansichten, auf, anl, wer) in enumerate(WERKZEUGE):
        da = [(b, t) for b, t in ansichten if 'ins-bild-' + b in M]
        if not da:
            fehlt.append((name, wer))
            schirme.append(f'<div class="ins-sc ins-sc--ph{" an" if i == 0 else ""}" data-i="{i}" data-j="0"><p>Platzhalter · nur lokal</p><b>{e(name)}</b><span>Bildschirmfoto folgt mit der Lieferung von {e(wer)}</span></div>')
            if not k['lokal']:
                ph(name + ' im Laptop', wer, 'Bildschirmfoto fehlt')
        for j, (b, t) in enumerate(da):
            fw, fh = M['ins-bild-' + b]
            schirme.append(f'<img src="{PLATZ}" data-src="img/ins-bild-{b}.webp" width="{fw}" height="{fh}" alt="{e(name)}: {e(t)}" class="ins-sc{" an" if i == 0 and j == 0 else ""}" data-i="{i}" data-j="{j}" decoding="async">')
        if len(da) > 1:
            minis.append(f'<div class="ins-mini{" an" if i == 0 else ""}" data-i="{i}">' + ''.join(
                f'<button type="button" class="ins-m" data-j="{j}" aria-pressed="{"true" if j == 0 else "false"}">{e(t)}</button>' for j, (_, t) in enumerate(da)) + '</div>')
        li = ''.join(f'<li>{siegel}<span>{e(x)}</span></li>' for x in punkte)
        knoepfe = (kn(f'{NF.akk(name)} öffnen', auf, neu=True) if auf else '') + (kn('Anleitung', anl, 'kn--linie', neu=True) if anl else '')
        texte.append(f'<article class="ins-t{" an" if i == 0 else ""}" data-i="{i}" data-url="{auf if (da and auf) else ""}" role="tabpanel" aria-label="{e(name)}"><p class="ins-t__r">{e(rolle)}</p><h3>{e(name)}</h3>'
                     f'<p class="ins-t__s">{e(satz)}</p><ul class="ins-t__l">{li}</ul><div class="kn-reihe">{knoepfe}</div></article>')
    strom = ''.join(f'<li class="wzs" data-a="auf" style="--i:{i}"><div class="wzs__q"><b>{e(q)}</b><span>{e(was)}</span></div><i class="wzs__p" aria-hidden="true"></i>'
                    f'<ul class="wzs__z">{"".join(f"<li>{e(z)}</li>" for z in ziele)}</ul></li>' for i, (q, was, ziele) in enumerate(STROM))
    buehne = SB.html_(k, {w[1]: w[3] for w in WERKZEUGE}) or f'<div class="wz-strom"><h3 class="wz-strom__t" data-a="auf">Einmal ändern, <em>überall richtig.</em></h3><ul>{strom}</ul></div>'
    return f'''
<section class="fl fl--navy tapete blatt ins" id="k5" tabindex="-1">
  <div class="in">
    <span class="k-anker" id="werkzeuge"></span>{k['kopfk']('k5', ['Sieben Werkzeuge', 'für euren Abend.'], f'Ein Abend kommt dazu, ein Menü steht, ein Gast fragt nach einem Platz. Dafür gibt es je ein Werkzeug, und {NF.klein(STUBE)} führt zu allen.')}
    <div class="ins-lauf" style="--nw:{len(WERKZEUGE)}"><div class="ins-stick">
    <div class="ins-leiste" data-a="auf"><div class="ins-reiter" role="tablist" aria-label="Werkzeuge">{reiter}</div>
      <div class="ins-pf"><button type="button" class="ins-zu" aria-label="Voriges Werkzeug">{pf_l}</button><button type="button" class="ins-vor" aria-label="Nächstes Werkzeug">{pf_r}</button></div></div>
    <div class="ins-buehne">
      <div class="ins-g">
        <div class="ins-dev" style="aspect-ratio:{gw}/{gh}">
          <div class="ins-dev__e" data-b="{fb}" role="button" tabindex="0" aria-label="Werkzeug zum Bedienen öffnen" style="left:{sx:.4f}%;top:{sy:.4f}%;width:{sw:.4f}%;height:{sh:.4f}%">{''.join(schirme)}<span class="ins-klick" aria-hidden="true"><span class="ins-klick__a">Zum Bedienen klicken</span><span class="ins-klick__b">Wird geöffnet …</span><i>{zeiger}</i></span></div>
          <img class="ins-dev__g" src="img/ins-geraet.webp" width="{gw}" height="{gh}" alt="" decoding="async" loading="lazy">
        </div>
        <div class="ins-minis">{''.join(minis)}</div>
        <p class="ins-hinweis">{zeiger}Ein Klick auf den Bildschirm macht das Werkzeug hier bedienbar, mit Probe-Daten.</p>
      </div>
      <div class="ins-texte">{''.join(texte)}</div>
    </div>
    </div></div>
    {buehne}
  </div>
  {JS}
</section>''', fehlt


JS = r"""<script>(function(){var s=document.getElementById('k5');if(!s)return;
var R=[].slice.call(s.querySelectorAll('.ins-r')),T=[].slice.call(s.querySelectorAll('.ins-t')),SC=[].slice.call(s.querySelectorAll('.ins-sc')),MI=[].slice.call(s.querySelectorAll('.ins-mini'));
var rahmen=null,dev=s.querySelector('.ins-dev'),akt=0,ansicht={},still=matchMedia('(prefers-reduced-motion:reduce)').matches;
function lade(img){if(img&&img.getAttribute&&img.getAttribute('data-src')){img.src=img.getAttribute('data-src');img.removeAttribute('data-src')}return img}
function bereit(img){lade(img);if(!img.decode)return Promise.resolve();return Promise.race([img.decode().catch(function(){}),new Promise(function(r){setTimeout(r,700)})])}
function schirm(i,j){return s.querySelector('.ins-sc[data-i="'+i+'"][data-j="'+j+'"]')}
var wahl=0;function zeigSchirm(neu){if(!neu)return;var mein=++wahl;bereit(neu).then(function(){if(mein!==wahl)return;
SC.forEach(function(x){if(x===neu)return;if(x.classList.contains('an')){x.classList.add('bleibt');x.style.zIndex=0}else{x.classList.remove('bleibt');x.style.zIndex=0}});
neu.classList.remove('bleibt');neu.style.zIndex=1;neu.classList.add('an');
setTimeout(function(){if(mein!==wahl)return;SC.forEach(function(x){if(x!==neu){x.classList.remove('an','bleibt');x.style.zIndex=0}})},420)})}   /* Robert 18.10.2026 21:31: beim Zurückgehen lag das vorige Bild beim Ausblenden über dem neuen (gleiche Ebene, später im Code) und flackerte auf; Ausblendende liegen jetzt immer unter dem gezeigten */
function vorab(i){var n=(i+1)%T.length;[].forEach.call(s.querySelectorAll('.ins-sc[data-i="'+i+'"],.ins-sc[data-i="'+n+'"]'),lade)}
function zeig(n){n=(n+T.length)%T.length;if(n===akt)return;weg();akt=n;
R.forEach(function(r,i){r.setAttribute('aria-selected',i===n?'true':'false')});
T.forEach(function(t,i){t.classList.toggle('an',i===n)});MI.forEach(function(m){m.classList.toggle('an',+m.getAttribute('data-i')===n)});
zeigSchirm(schirm(n,ansicht[n]||0));vorab(n)}
var lauf=s.querySelector('.ins-lauf'),tak=0,pinAn=function(){return false};   /* Robert 15.10.2026: der Laptop zieht nicht mehr mit, Reiter und Pfeile wechseln */
function geh(n){n=(n+T.length)%T.length;if(!pinAn()){zeig(n);return}var r=lauf.getBoundingClientRect(),h=lauf.offsetHeight-innerHeight;scrollTo({top:scrollY+r.top+((n+.5)/T.length)*h,behavior:'smooth'})}
function scrollen(){tak=0;if(!pinAn()||rahmen)return;var r=lauf.getBoundingClientRect(),h=lauf.offsetHeight-innerHeight,p=Math.max(0,Math.min(.9999,-r.top/h));var i=Math.floor(p*T.length);if(i!==akt&&r.top<innerHeight&&r.bottom>0)zeig(i)}
addEventListener('scroll',function(){if(!tak)tak=requestAnimationFrame(scrollen)},{passive:true});
R.forEach(function(r,i){r.addEventListener('click',function(){geh(i)})});
s.querySelector('.ins-vor').addEventListener('click',function(){geh(akt+1)});s.querySelector('.ins-zu').addEventListener('click',function(){geh(akt-1)});

var x0=null,bu=s.querySelector('.ins-buehne');bu.addEventListener('pointerdown',function(ev){if(ev.pointerType!=='mouse')x0=ev.clientX});
bu.addEventListener('pointerup',function(ev){if(x0===null)return;var d=ev.clientX-x0;x0=null;if(Math.abs(d)>50)zeig(akt+(d<0?1:-1))});
MI.forEach(function(m){var i=+m.getAttribute('data-i'),B=[].slice.call(m.querySelectorAll('.ins-m'));B.forEach(function(b,j){b.addEventListener('click',function(){weg();
B.forEach(function(x,k){x.setAttribute('aria-pressed',k===j?'true':'false')});ansicht[i]=j;zeigSchirm(schirm(i,j))})})});
var ebene=s.querySelector('.ins-dev__e'),FB=+ebene.getAttribute('data-b')||1440;
new IntersectionObserver(function(E,o){if(E[0].isIntersecting){[].forEach.call(s.querySelectorAll('.ins-sc[data-j="0"]'),lade);o.disconnect()}},{rootMargin:'250% 0px'}).observe(dev);
new IntersectionObserver(function(E,o){if(E[0].isIntersecting){SC.forEach(lade);o.disconnect()}},{rootMargin:'100% 0px'}).observe(dev);
if(still||!('IntersectionObserver' in window))dev.classList.add('da');
else new IntersectionObserver(function(E,o){if(E[0].isIntersecting){dev.classList.add('da');o.disconnect()}},{threshold:.18}).observe(dev);
/* Zum Bedienen: ein Klick auf den Bildschirm lädt dort das echte Werkzeug in genau diesem Rechteck; das Foto bleibt stehen, bis es steht. Nur mit Maus. */
var fein=matchMedia('(hover:hover) and (pointer:fine)').matches,warte=0;
function mass(){if(!rahmen)return;var k=ebene.clientWidth/FB;rahmen.style.height=(ebene.clientHeight/k).toFixed(2)+'px';rahmen.style.transform='scale('+k.toFixed(6)+')'}
function weg(){clearTimeout(warte);if(rahmen){rahmen.remove();rahmen=null}ebene.classList.remove('live','laedt');document.documentElement.classList.remove('ins-ruhe')}
function zeigLive(f){if(f!==rahmen||f.classList.contains('da'))return;clearTimeout(warte);f.classList.add('da');ebene.classList.remove('laedt');ebene.classList.add('live')}
/* Robert 19.10.2026 01:18: «wenn ich bei den Tools drin bin, dass jedes Mal ein neuer Tab eröffnet wird»: das Werkzeug läuft nicht mehr im Laptop der Seite
   (Safaris Zurück blätterte sonst dieses eingebettete Werkzeug zurück und liess eine leere Fläche stehen), sondern öffnet in einem neuen Tab,
   mit der Höhe der Werkbank für «Zurück zur Werkbank». */
function live(){var u=T[akt].getAttribute('data-url');if(!u)return;try{var x=new URL(u,location.href),y=Math.round(scrollY);if(x.origin!==location.origin){x.searchParams.set('wb','de.k5');x.searchParams.set('wy',y);x.searchParams.set('wbo',location.origin)}else x.searchParams.set('wb',y);try{sessionStorage.setItem('wb-y',String(y))}catch(e){}window.open(x.toString(),'_blank')}catch(e){window.open(u,'_blank')}}
function lokal(u){try{var x=new URL(u,location.href);if(x.origin!==location.origin&&/^\/_werkzeuge\//.test(x.pathname)&&!/^\/_werkzeuge\/maison\//.test(x.pathname)&&/^(127\.0\.0\.1|localhost)$/.test(location.hostname))return x.pathname+x.search}catch(e){}return u}
/* Robert 29.10.2026: «zum Bedienen klicken und dann da drin scrollen, so wie es bei den anderen Werkbänken ist»: wieder im Laptop, gross über den Knopf daneben */
function liveAlt(){if(rahmen)return;var u=T[akt].getAttribute('data-url');if(!u)return;u=lokal(u);
if(ansicht[akt]){ansicht[akt]=0;var m=s.querySelector('.ins-mini[data-i="'+akt+'"]');if(m)[].forEach.call(m.querySelectorAll('.ins-m'),function(x,k){x.setAttribute('aria-pressed',k===0?'true':'false')});zeigSchirm(schirm(akt,0))}
var f=document.createElement('iframe');f.className='ins-live';f.title=T[akt].getAttribute('aria-label');
var fremd=true;try{fremd=new URL(u,location.href).origin!==location.origin}catch(x){}
f.onload=function(){var n=0,alt=-1,ruhig=0;if(fremd){setTimeout(function(){zeigLive(f)},900);return}(function pruef(){if(f!==rahmen)return;var t=-1,offen=0;try{var d=f.contentDocument,w=f.contentWindow;t=d.body.innerText.length;
offen=[].filter.call(d.images,function(i){var q=i.getBoundingClientRect();return q.bottom>0&&q.top<w.innerHeight&&q.width>4&&!i.complete}).length}catch(x){}
if(t<0){setTimeout(function(){zeigLive(f)},900);return}ruhig=(t>=200&&t===alt&&!offen)?ruhig+1:0;
if(ruhig>=3){setTimeout(function(){zeigLive(f)},120);return}alt=t;if(++n>80){zeigLive(f);return}setTimeout(pruef,150)})()};
rahmen=f;ebene.classList.add('laedt');document.documentElement.classList.add('ins-ruhe');f.src=u;ebene.appendChild(f);mass();
warte=setTimeout(function(){zeigLive(f)},15000)}
if(true){ebene.addEventListener('click',function(){if(!rahmen)liveAlt()});
ebene.addEventListener('keydown',function(ev){if((ev.key==='Enter'||ev.key===' ')&&!rahmen){ev.preventDefault();ev.stopPropagation();liveAlt()}});
s.querySelector('.ins-vor').addEventListener('click',weg);s.querySelector('.ins-zu').addEventListener('click',weg);
addEventListener('resize',mass);if('ResizeObserver' in window)new ResizeObserver(mass).observe(ebene);
new IntersectionObserver(function(E){if(!E[0].isIntersecting)weg()},{threshold:0}).observe(dev)}
else{ebene.removeAttribute('role');ebene.removeAttribute('tabindex');ebene.removeAttribute('aria-label')}
})();</script>"""

CSS = '''
/* ---------- Kapitel 5 «Ihre Werkzeuge» (werkzeuge_kapitel.py, 15.10.2026): ein Laptop, nur der Bildschirm wechselt ---------- */
.ins-leiste{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:clamp(10px,1.4vw,24px)}
.ins-reiter{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}.ins-bruch{flex-basis:100%;height:0}
.ins-r{position:relative;flex:none;display:flex;flex-direction:column;align-items:center;gap:3px;padding:11px 20px 12px;border:0;border-radius:999px;cursor:pointer;color:#fbf6ea;
  background:linear-gradient(180deg,#1b3561 0%,#0a1c3b 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.14),inset 0 -1px 0 rgba(0,0,0,.4),0 0 0 1px rgba(220,198,143,.32),0 14px 24px -14px rgba(0,0,0,.85);
  transition:box-shadow .4s,background .5s,color .4s}
.ins-r small{font-family:var(--mono);font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(220,198,143,.85);transition:color .4s}
.ins-r span{font-family:var(--serif);font-size:clamp(1rem,1.14vw,1.16rem);line-height:1.1;white-space:nowrap}
.ins-r:hover{box-shadow:inset 0 1px 0 rgba(255,255,255,.18),inset 0 -1px 0 rgba(0,0,0,.4),0 0 0 1px rgba(220,198,143,.7),0 16px 26px -14px rgba(0,0,0,.9)}
.ins-r[aria-selected="true"]{color:var(--tinte);background:linear-gradient(180deg,#fbf3e2 0%,#e6d4ad 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -1px 0 rgba(110,88,44,.35),0 0 0 1px rgba(220,198,143,.9),0 16px 30px -14px rgba(0,0,0,.9)}
.ins-r[aria-selected="true"] small{color:var(--taupe)}
.ins-pf{flex:none;display:flex;gap:10px}
.ins-pf button{width:48px;height:48px;border-radius:50%;display:grid;place-items:center;color:var(--tinte);background:radial-gradient(circle at 35% 30%,#fbf3e2,#cfbd98);box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 10px 18px -8px rgba(0,0,0,.6)}
.ins-pf svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6}
.ins-buehne{display:grid;gap:clamp(30px,4vw,72px);align-items:center;margin-top:clamp(30px,3.4vw,56px);touch-action:pan-y}
@media(min-width:1000px){.ins-buehne{grid-template-columns:minmax(0,1.6fr) minmax(0,1fr)}}
.ins-dev{position:relative;width:100%;opacity:0;transform:translate3d(0,160px,0) scale(.94)}
.ins-dev.da{opacity:1;transform:none;transition:opacity 1.1s cubic-bezier(.4,0,.2,1),transform 2.2s cubic-bezier(.16,1,.3,1)}
.ins-dev__g{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:2;pointer-events:none;-webkit-user-select:none;user-select:none}
.ins-dev__e{position:absolute;z-index:1;overflow:hidden;background:#0c0e16;outline:0}
.ins-sc{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 0;opacity:0;z-index:1;transition:opacity .38s cubic-bezier(.4,0,.2,1)}
.ins-sc.an{opacity:1}.ins-sc.bleibt{opacity:1!important;transition:none}
.ins-sc--ph{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;text-align:center;padding:6%;background:repeating-linear-gradient(135deg,#101a30 0 16px,#0c1426 16px 32px);color:#fbf6ea}
.ins-sc--ph p{font-family:var(--mono);font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:#e0a96a}
.ins-sc--ph b{font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,2.6vw,2.6rem)}
.ins-sc--ph span{font-size:.86rem;opacity:.7}
.ins-live{position:absolute;left:0;top:0;width:1440px;height:932px;max-width:none;border:0;background:#0c0e16;transform-origin:0 0;opacity:0;pointer-events:none;z-index:4;transition:opacity .3s linear}
.ins-live.da{opacity:1;pointer-events:auto}
html.ins-ruhe :is(.stapel .tel,.runter i,.zeile__z,.namenzug div,.wb-band__zug,.glanz){animation-play-state:paused!important}
.vh-was li::before{content:'';width:.78em;height:.82em;transform:none;background:var(--gold);-webkit-mask:url(eigen/zeichen-c.svg) center/contain no-repeat;mask:url(eigen/zeichen-c.svg) center/contain no-repeat;top:.22em}
/* Trenner im Namenszug und Listenzeichen: das «C» aus dem Kleid als Maske (29.10.2026, vorher das «x» aus der Schrift) */
.namenzug span::after{content:'';display:inline-block;width:.62em;height:.66em;border-radius:0;background:var(--messing);-webkit-mask:url(eigen/zeichen-c.svg) center/contain no-repeat;mask:url(eigen/zeichen-c.svg) center/contain no-repeat;vertical-align:-.04em}
.ins-klick{display:none}
@media(hover:hover) and (pointer:fine){
  .ins-dev__e{cursor:pointer}.ins-dev__e.laedt{cursor:progress}.ins-dev__e.live{cursor:auto}
  .ins-klick{position:absolute;right:2.6%;bottom:4.2%;z-index:3;display:flex;align-items:center;gap:11px;padding:4px 4px 4px 17px;border-radius:999px;pointer-events:none;
    font-family:var(--mono);font-size:.64rem;letter-spacing:.14em;text-transform:uppercase;line-height:1;white-space:nowrap;color:var(--tinte);background:linear-gradient(180deg,#fbf3e2 0%,#e6d4ad 100%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -1px 0 rgba(110,88,44,.35),0 0 0 1px rgba(220,198,143,.9),0 16px 28px -10px rgba(0,0,0,.8);transition:opacity .3s}
  .ins-klick i{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,#1b3561 0%,#0a1c3b 100%)}
  .ins-klick svg{width:15px;height:15px;fill:none;stroke:#f0e3c2;stroke-width:1.7;stroke-linejoin:round}
  .ins-klick__b{display:none}.ins-dev__e.laedt .ins-klick__a{display:none}.ins-dev__e.laedt .ins-klick__b{display:inline}
  .ins-dev__e.live .ins-klick{opacity:0}
  .ins-dev__e:has(.ins-sc--ph.an) .ins-klick{display:none}
}
.ins-minis{display:grid;margin-top:8px}
.ins-hinweis{display:none;align-items:center;justify-content:center;gap:10px;margin:14px 0 0;font-family:var(--serif);font-size:.98rem;color:rgba(251,246,234,.7)}
@media(hover:hover) and (pointer:fine){.ins-hinweis{display:flex}}
.ins-hinweis svg{width:18px;height:18px;flex:none;fill:none;stroke:var(--gold);stroke-width:1.4;stroke-linejoin:round}
.ins-mini{grid-area:1/1;display:flex;justify-content:center;gap:8px;flex-wrap:wrap;opacity:0;visibility:hidden;transition:opacity .16s linear,visibility 0s .16s}
.ins-mini.an{opacity:1;visibility:visible;transition:opacity .3s linear .16s,visibility 0s .16s}
.ins-m{padding:8px calc(16px - .08em) 8px calc(16px + .08em);border-radius:999px;font-family:var(--mono);font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(251,246,234,.7);box-shadow:inset 0 0 0 1px rgba(220,198,143,.35)}
.ins-m[aria-pressed="true"]{color:var(--tinte);background:var(--creme)}
@supports (font:-apple-system-body){.ins-m{padding:8px 16px}}   /* Sperrung hinter dem letzten Buchstaben: Chromium rückt die Schrift um die halbe Sperrung nach rechts, Safari zeichnet sie schon mittig (Messlauf 30.10.) */
.ins-texte{display:grid;grid-template-columns:minmax(0,1fr)}   /* nie breiter als die Spalte (Tor 30.10., 1000 px) */
.ins-t{grid-area:1/1;width:100%;max-width:33rem;margin-inline:auto;text-align:center;opacity:0;visibility:hidden;transition:opacity .16s linear,visibility 0s .16s}
.ins-t.an{opacity:1;visibility:visible;transition:opacity .3s linear .16s,visibility 0s .16s}
.ins-t>*{translate:0 10px;opacity:0;transition:opacity .16s linear,translate .16s ease}
.ins-t.an>*{translate:0 0;opacity:1;transition:opacity .4s cubic-bezier(.22,.61,.36,1),translate .55s cubic-bezier(.22,.61,.36,1)}
.ins-t.an>:nth-child(2){transition-delay:.06s}.ins-t.an>:nth-child(3){transition-delay:.1s}.ins-t.an>:nth-child(4){transition-delay:.14s}.ins-t.an>:nth-child(5){transition-delay:.18s}
.ins-t__r{display:flex;align-items:center;justify-content:center;gap:16px;font-family:var(--mono);font-size:.72rem;letter-spacing:.3em;text-indent:.3em;text-transform:uppercase;color:var(--gold)}
.ins-t__r::before,.ins-t__r::after{content:'';flex:none;width:clamp(26px,3vw,46px);height:1px;background:rgba(220,198,143,.55)}
.ins-t h3{margin-top:clamp(16px,1.6vw,22px);font-family:var(--serif);font-weight:400;font-size:clamp(2.5rem,4.2vw,4.3rem);line-height:1;color:#fbf6ea}
.ins-t h3::after{content:'';display:block;width:clamp(54px,5vw,78px);height:1px;margin:clamp(20px,2vw,28px) auto 0;background:rgba(220,198,143,.7)}
.ins-t__s{margin:clamp(20px,2vw,28px) auto 0;max-width:37ch;font-family:var(--serif);font-size:clamp(1.1rem,1.26vw,1.3rem);line-height:1.55;color:rgba(251,246,234,.9);text-wrap:balance}
.ins-t__l{margin-top:clamp(24px,2.6vw,36px);text-align:left;border-bottom:1px solid rgba(220,198,143,.22)}
.ins-t__l li{display:flex;align-items:center;gap:16px;padding:13px 6px;border-top:1px solid rgba(220,198,143,.22);font-size:.98rem;line-height:1.45;color:rgba(251,246,234,.86)}
.ins-s{flex:none;width:22px;height:22px;color:var(--gold)}
.ins-s circle{fill:none;stroke:currentColor;stroke-width:1.6}.ins-s path{fill:none;stroke:currentColor;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.ins .ins-t .kn-reihe{justify-content:center;margin-top:clamp(26px,2.8vw,40px)}
.wz-strom{margin-top:clamp(64px,7vw,110px)}
.wz-strom__t{margin:0 0 clamp(22px,2.4vw,34px);font-family:var(--serif);font-weight:400;font-size:clamp(1.7rem,2.4vw,2.5rem);color:#fbf6ea;text-align:center}
.wz-strom__t em{font-style:normal;color:var(--gold)}
.wz-strom>ul{margin:0 auto;max-width:1060px;display:grid;gap:12px}
.wzs{display:grid;grid-template-columns:minmax(0,1fr) 60px minmax(0,1.6fr);align-items:center;gap:16px;padding:16px 20px;border-top:1px solid rgba(220,198,143,.22)}
.wzs__q b{display:block;font-family:var(--serif);font-weight:400;font-size:1.3rem;color:var(--gold)}
.wzs__q span{display:block;margin-top:4px;font-size:.95rem;color:rgba(251,246,234,.8)}
.wzs__p{position:relative;height:1px;background:linear-gradient(90deg,rgba(220,198,143,.2),rgba(220,198,143,.9))}
.wzs__p::after{content:'';position:absolute;right:-1px;top:-4px;width:8px;height:8px;border-top:1px solid #dcc68f;border-right:1px solid #dcc68f;transform:rotate(45deg)}
.wzs__z{display:flex;flex-wrap:wrap;gap:6px 0}
.wzs__z li{padding:0 14px;font-family:var(--serif);font-size:1.08rem;color:#fbf6ea}
.wzs__z li:first-child{padding-left:0}.wzs__z li+li{border-left:1px solid rgba(220,198,143,.45)}
@media(max-width:700px){.ins-bruch{display:none}.ins-leiste{flex-direction:column;align-items:stretch}.ins-reiter{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;scrollbar-width:none;margin-inline:calc(var(--rand)*-1);padding:4px var(--rand)}.ins-reiter::-webkit-scrollbar{display:none}.ins-pf{justify-content:flex-end}.wzs{grid-template-columns:1fr;gap:10px}.wzs__p{display:none}}
@media(prefers-reduced-motion:reduce){.ins-t,.ins-t>*,.ins-sc,.ins-mini,.ins-dev{transition:none!important;translate:none!important}.ins-dev{opacity:1;transform:none}}
'''
