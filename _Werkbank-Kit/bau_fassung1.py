#!/usr/bin/env python3
"""Baut die Werkbank eines Hauses nach <Projekt>/werkbank/.   python3 bau.py "<Projektordner>"

Aufbau und Wortlaut der festen Sätze stammen aus der Werkbank des Carlton-Europe (von Robert angenommen),
alles Eigene des Hauses steht in <Projekt>/_werkbank/haus.py. Zahlen stehen nirgends von Hand, sie werden gezählt.
Ton: Sie-Form, Schweizer Schreibung, herzlich (Master «Website-Bau», Abschnitt 5)."""
import glob, json, os, subprocess
from PIL import Image
import kern as K
from kern import H, ROOT, W, e, PF, LI, RE, HZ, kn, titel, kap, kopf, zahl, slug

ZIEL = os.path.join(ROOT, 'werkbank')
IMG = os.path.join(ZIEL, 'img')
AN = os.path.join(W, 'ansichten')
os.makedirs(IMG, exist_ok=True)
ET = H.ETIKETTEN   # dict(ordner, name, einzahl)


def zaehle():
    z = {}
    z['haupt'] = len([s for s in H.SEITEN if not (len(s) > 4 and s[4] == 'recht')])
    u = K.lies('unterlagen.json', [])
    z['unterlagen'] = len(u)
    p = K.lies('papier.json', {'druck': [], 'etiketten': []})
    z['druck'] = len(p['druck']); z['etiketten'] = len(p['etiketten'])
    f = os.path.join(ROOT, 'feed', 'feed.json')
    z['feed'] = len(json.load(open(f))['posts']) if os.path.exists(f) else 0
    return z, p, u


def bilder(liste, papier, unterlagen):
    m = {}
    w = lambda quelle, name, breite, q=78, **kw: m.__setitem__(name, K.webp(quelle, os.path.join(IMG, name + '.webp'), breite, q, **kw))
    R, Ha = os.path.join(AN, 'Rechner'), os.path.join(AN, 'Handy')
    for datei, d in liste.items():
        s = slug(d['name'])
        for k in range(1, d['rechner'] + 1):
            w(os.path.join(R, d['name'] + ('' if k == 1 else f' {k}') + '.jpg'), f'{s}-{k}', 1280, 76)
        w(os.path.join(Ha, d['name'] + '.jpg'), f'{s}-h', 440, 78)
        for k in range(2, d['rechner'] + 1):
            q = os.path.join(Ha, d['name'] + f' {k}.jpg')
            w(q if os.path.exists(q) else os.path.join(Ha, d['name'] + '.jpg'), f'{s}-h{k}', 440, 78)
    w(os.path.join(R, 'Startseite.jpg'), 'auftakt', 1440, 82)
    w(os.path.join(Ha, 'Startseite.jpg'), 'auftakt-h', 520, 82)
    if os.path.exists(os.path.join(AN, 'Heute', 'Startseite.jpg')):
        w(os.path.join(AN, 'Heute', 'Startseite.jpg'), 'alt', 1440, 80)
    for i, (quelle, _, _, _) in enumerate(H.IDEEN):
        w(os.path.join(AN, quelle + '.jpg'), f'i-{i}', 1160, 76)
    for i, (ziel, _) in enumerate(H.FAECHER):
        aus = os.path.join(W, 'roh', f'pdf-{i}'); os.makedirs(os.path.dirname(aus), exist_ok=True)
        subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-r', '110', '-png', '-singlefile', os.path.join(ROOT, 'unterlagen', 'pdf', ziel + '.pdf'), aus], check=True)
        w(aus + '.png', f'pdf-{i}', 900, 86)
    for name, (key, lage) in H.GABEN_BILDER.items():
        w(K.hausbild(key), 'g-' + name, 1000, 72, dunkel=(0.46, 0.3), schnitt=0.72, lage=lage)
    w(K.hausbild(H.SCHLUSS['bild']), 'schluss', 1920, 74, dunkel=(0.52, 0.3))
    w(K.hausbild(H.BRIEF['bild']), 'brief', 1300, 80, schnitt=1.5, lage=H.BRIEF.get('lage', (.5, .5)))
    w(os.path.join(K.KIT, 'robert.jpg'), 'robert', 400, 90)   # Roberts graues Profilbild (von seinem Instagram-Profil)
    for key, *_ in list(H.AUFTAKT['abzuege']) + list(H.MATERIAL['streu']):
        w(K.hausbild(key), 'a-' + slug(os.path.basename(key)), 640, 78)
    PR = os.path.join(W, 'roh', 'papier')
    for x in papier['etiketten'][:len(H.PAPIER['orte_e'])]:
        w(os.path.join(PR, x['id'] + '.png'), 'k-' + x['id'], 340, 84)
    for n, _, _, br, _, _ in H.PAPIER['orte_d']:
        if os.path.exists(os.path.join(PR, n + '.png')):
            w(os.path.join(PR, n + '.png'), 'b-' + n, max(200, round(br * 13)), 84)
    ZI = os.path.join(AN, 'Ziele')
    if os.path.exists(os.path.join(ZI, 'feed-handy.png')):
        w(Image.open(os.path.join(ZI, 'feed-handy.png')).convert('RGBA'), 'feed-handy', 720, 88)
        for nr, *_ in H.FEED['kacheln']:
            w(os.path.join(ROOT, 'feed', 'thumbs', f'{nr:02d}.jpg'), f'fp-{nr}', 400, 84)
        r = Image.open(os.path.join(ZI, 'feed-raster.png')).convert('RGB')
        w(r.crop((round(r.width * .04), round(r.height * .2), round(r.width * .96), round(r.height * .2 + r.width * .92 * .75))), 'z-feed', 720, 82)
    for name, quelle in (('website', os.path.join(R, 'Startseite.jpg')), ('unterlagen', os.path.join(ZI, 'unterlagen.jpg')), ('drucksachen', os.path.join(ZI, 'drucksachen.jpg')), ('etiketten', os.path.join(ZI, 'etiketten.jpg')), ('material', os.path.join(ZI, 'material.jpg'))):
        if os.path.exists(quelle):
            bq = Image.open(quelle).convert('RGB')
            if name == 'website':
                bq = bq.crop((0, 0, round(bq.height * 4 / 3), bq.height))
            w(bq, 'z-' + name, 720, 80, schnitt=4 / 3)
    return m


def gangfuss():
    return f'<div class="gang__f"><button class="rund" type="button" data-zur aria-label="Zurück">{LI}</button><button class="rund" type="button" data-vor aria-label="Weiter">{RE}</button><div class="gang__b"><i></i></div><div class="gang__z"></div></div>'


def baue():
    K.gestaltung()
    z, papier, unterlagen = zaehle()
    liste = json.load(open(os.path.join(AN, 'liste.json')))
    m = bilder(liste, papier, unterlagen)
    g = H.gefuege(z)

    def bild(name, alt='', lazy=True, klasse=''):
        w, h = m[name]
        return f'<img src="img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}"{" loading=\"lazy\" decoding=\"async\"" if lazy else ""}{f" class=\"{klasse}\"" if klasse else ""}>'

    def abzug(key, unter, klasse='', mehr=''):
        return f'<div class="abzug {klasse}" data-a="schweb"{mehr}>{bild("a-" + slug(os.path.basename(key)), lazy="abzug--" not in klasse)}<span>{e(unter)}</span></div>'

    seiten = []
    for s in H.SEITEN:
        d = liste.get(s[0])
        if d:
            seiten.append({'d': s[0], 's': slug(d['name']), 't': H.LANG.get(d['name'], d['name']), 'k': H.KURZNAME.get(d['name'], d['name']), 'x': s[3], 'n': d['rechner']})
    wahl = ''.join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}">{e(s["k"])}</button>' for i, s in enumerate(seiten))
    ideen = ''.join(
        f'<article class="idee" data-a="kipp" style="--i:{min(i, 3)}"><div class="idee__b">{bild(f"i-{i}", t)}<span class="idee__n">{i + 1:02d}</span></div><h3>{e(t)}</h3><p>{e(x)}</p></article>'.replace('<img ', f'<img style="--op:{op}" ', 1)
        for i, (_, t, x, op) in enumerate(H.IDEEN))

    et = papier['etiketten']
    kleb_html = ''.join(f'<div class="kleb" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i}">{bild("k-" + et[i]["id"])}</div>'
                        for i, (x, y, b, r) in enumerate(H.PAPIER['orte_e']) if i < len(et))
    bogen_html = ''.join(f'<div class="bogenb{" haengt" if haengt else ""}" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i}">{bild("b-" + n)}</div>'
                         for i, (n, x, y, b, r, haengt) in enumerate(H.PAPIER['orte_d']) if 'b-' + n in m)
    streu = ''.join(f'<div class="abzug" data-a="schweb" data-drift="{dr}" style="--i:{i};--r:{d}deg;--r0:{d * 3}deg">{bild("a-" + slug(os.path.basename(k)))}<span>{e(u)}</span></div>'
                    for i, (k, u, d, dr) in enumerate(H.MATERIAL['streu']))
    farben_html = ''.join(f'<li class="farbkarte" data-a="schweb" style="--i:{i};--r:0deg;--r0:{(-1) ** i * 6}deg"><i style="background:{c}"></i><span><b>{n}</b>{c}<br>{wo}</span></li>' for i, (c, n, wo) in enumerate(H.HANDSCHRIFT['farben']))
    laufworte = ''.join(f'<span>{wo}</span>' + getattr(H, 'LAUFTRENNER', HZ) for wo in H.LAUFWORTE)
    namen = ''.join(f'<span>{e(u["name"])}</span>' for u in unterlagen)
    wege = [(n, t, h) for n, t, h in (('website', 'Website', '../index.html'), ('unterlagen', 'Unterlagen', '../unterlagen/index.html'), ('drucksachen', 'Drucksachen', '../drucksachen/index.html'), ('etiketten', ET['name'], f'../{ET["ordner"]}/index.html'), ('feed', 'Feed', '../feed/index.html'), ('material', 'Material', '../material/index.html')) if 'z-' + n in m]
    A, B, U, HS, FD, PA, MA, AU, SL = H.AUFTAKT, H.BRIEF, H.UNTERLAGEN, H.HANDSCHRIFT, H.FEED, H.PAPIER, H.MATERIAL, H.AUSBLICK, H.SCHLUSS
    n_ideen = zahl(len(H.IDEEN))
    feedzahl = zahl(z['feed']) if z['feed'] else ''
    gaben = [('seite', z['haupt'], 'Eine neue Website', H.GABEN['seite'].format(n=z['haupt']), '#seiten', 'Seiten ansehen'),
             ('unterlagen', z['unterlagen'], 'Ihre Unterlagen im selben Stil', H.GABEN['unterlagen'].format(n=z['unterlagen']), '#unterlagen', 'Unterlagen ansehen'),
             ('papier', z['druck'] + z['etiketten'], 'Ideen für Papier', H.GABEN['papier'].format(d=z['druck'], e=z['etiketten']), '#papier', 'Ideen ansehen'),
             ('material', z['feed'], 'Ein Feed für Instagram', H.GABEN['feed'].format(n=feedzahl), '#feed', 'Feed ansehen')]
    gaben_html = ''.join(f'<a class="gabe" href="{ziel}" data-a="kipp" style="--i:{i}">{bild("g-" + bk, klasse="gabe__b")}<b><span class="odo" data-z="{n}"></span></b><h3>{t}</h3><p>{x}</p><span class="pfeil">{kt}{PF}</span></a>'
                         for i, (bk, n, t, x, ziel, kt) in enumerate(gaben))
    vergleich = '' if 'alt' not in m else f'''
<section class="fl fl--nacht blatt" id="vergleich">
  <div class="in">
    {kopf(3, 'Vergleich', ['Ihre Startseite,', 'einmal neu.'], 'Links sehen Sie Ihre Startseite, wie sie heute ist, rechts die neue. Schieben Sie den Griff einfach hin und her.')}
    <div class="vgl" data-a="gross">
      {bild('alt', 'Die heutige Startseite von ' + H.DOMAIN)}
      {bild('auftakt', 'Die neue Startseite', klasse='neu')}
      <span class="vgl__e vgl__e--l">Heute</span><span class="vgl__e vgl__e--r">Neu</span>
      <div class="vgl__g"><i><svg viewBox="0 0 22 22" aria-hidden="true"><path d="M8 6 3 11l5 5M14 6l5 5-5 5"/></svg></i></div>
      <input type="range" min="0" max="100" value="50" aria-label="Vergleich verschieben">
    </div>
  </div>
</section>
'''
    schriften = ''.join(f'<div class="bogen__zl"><p class="etik"><span>{e(a)}</span><span>{i + 1:02d}</span></p><div class="schrift__g schrift__g--{kl}">Aa</div><p class="schrift__n">{e(n)}</p><p class="schrift__p">{e(x)}</p><p class="schrift__b{" t3" if kl == "a" else (" mono" if kl == "m" else "")}">{e(bsp)}</p></div>'
                        for i, (a, kl, n, x, bsp) in enumerate(HS['schriften']))
    geschwister = getattr(H, 'UEBERSICHT', None)
    alle_vier = f'<a href="{geschwister[1]}">{e(geschwister[0])}</a>' if geschwister else ''

    seite = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Werkbank · {e(H.NAME)}</title>
<meta name="description" content="Ein Entwurf für die neue Website des {e(H.NAME)}, mit Unterlagen und Ideen für Papier. Alles auf einen Blick.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{H.FARBEN['nacht']}">
<link rel="preload" href="fonts/{H.SCHRIFT['titel'][1]}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="werkbank.css?v={K.v('werkbank.css')}">
</head>
<body class="haus-{H.KURZ}">
{K.sprite()}
<div class="tor" aria-hidden="true"><i></i><i></i>{HZ}<b>Werkbank</b></div>
<div class="gang-linie" aria-hidden="true"></div>
<header class="leiste"><div class="insel">
  <a class="insel__m" href="#oben">{HZ}{f"<b>{e(H.LEISTE)}</b>" if H.LEISTE else ""}<span>Werkbank</span></a>
  <nav aria-label="Abschnitte"><a href="#brief">Guten Tag</a><a href="#ideen">Ideen</a><a href="#gefuege">Gefüge</a><a href="#seiten">Seiten</a><a href="#unterlagen">Unterlagen</a><a href="#feed">Feed</a><a href="#papier">Papier</a><a href="#material">Material</a></nav>
  <a class="glanz" href="../index.html" target="_blank" rel="noopener">Zur Website{PF}</a>
</div></header>

<main id="oben">
<section class="auftakt">
  <div class="in">
    <div class="auftakt__t">
      <p class="gruss" data-a="auf">{e(H.ANREDE)}</p>
      {titel(A['titel'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:2100ms">{A['text']}</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:10">{kn('Website ansehen', '../index.html', neu=True)}{kn('Weiterlesen', '#brief', 'kn--linie')}</div>
    </div>
    <div class="stapel" aria-hidden="true">
      <div class="fen" data-a="schweb" data-drift="0.05" style="--i:2"><div class="fen__k"><i></i><i></i><i></i><span>{H.KURZ} / startseite</span></div>{bild('auftakt', lazy=False)}</div>
      {abzug(A['abzuege'][0][0], A['abzuege'][0][1], 'abzug--1', ' data-drift="-0.09"')}
      {abzug(A['abzuege'][1][0], A['abzuege'][1][1], 'abzug--2', ' data-drift="0.11"')}
      {abzug(A['abzuege'][2][0], A['abzuege'][2][1], 'abzug--3', ' data-drift="-0.06"')}
      <div class="tel" data-a="schweb">{bild('auftakt-h', lazy=False)}</div>
    </div>
  </div>
  <div class="in auftakt__fuss mono" data-a="auf" style="--i:13"><span class="runter"><i></i>Einfach nach unten scrollen</span><span>Stand {K.STAND}</span><span>Robert Reff · Tasty Studios</span></div>
</section>

<section class="fl fl--papier blatt" id="brief">
  <div class="in brief">
    <div>
      {kap(1, 'Guten Tag')}
      {titel(['Schön, dass Sie', 'hereinschauen.'])}
      <div class="lauf">
        {''.join(f'<p data-a="auf" style="--i:{i + 1}">{p}</p>' for i, p in enumerate(B['absaetze']))}
      </div>
      <div class="gastgeber" data-a="auf" style="--i:3">
        <span class="gastgeber__b">{bild('robert', 'Robert Reff')}</span>
        <p class="gastgeber__t">{B['schluss']}</p>
        <p class="gastgeber__n"><b>Robert Reff</b><span>Hamburg · Koh Phangan · Siargao</span></p>
      </div>
    </div>
    <div class="brief__r">
      <div class="brief__haus" data-a="gross">{bild('brief', B['bild_alt'])}<span class="schild">{e(B['schild'][0])}<small>{e(B['schild'][1])}</small></span></div>
      <div class="karte3" data-a="kipp" style="--i:2">
        <h3>Meine drei Orte</h3>
        <p>Zwischen diesen dreien bin ich das Jahr über unterwegs.</p>
        <svg class="kurs" viewBox="0 0 520 200" role="img" aria-label="Hamburg, Koh Phangan und Siargao als drei Punkte auf einem Kursblatt">
          <path class="weg" d="M52 52 C160 170 262 176 336 150 S446 128 478 136"/>
          <circle class="welle" cx="336" cy="150" r="7"/>
          <circle class="pkt" cx="52" cy="52" r="5"/><circle class="pkt da0" cx="336" cy="150" r="5.5"/><circle class="pkt" cx="478" cy="136" r="5"/>
          <text class="ort" x="66" y="48">Hamburg</text><text x="66" y="64">53°33' N · 9°59' O</text>
          <text class="ort" x="336" y="178" text-anchor="middle">Koh Phangan</text><text x="336" y="194" text-anchor="middle">9°44' N · 100°01' O · gerade hier</text>
          <text class="ort" x="478" y="108" text-anchor="end">Siargao</text><text x="478" y="122" text-anchor="end">9°47' N · 126°09' O</text>
        </svg>
      </div>
    </div>
  </div>
</section>

<section class="fl fl--navy tapete blatt" id="mitgebracht">
  <div class="in">
    {kopf(2, 'Mitgebracht', ['Was ich Ihnen', 'mitgebracht habe.'], 'Vier Dinge sind es geworden.')}
    <div class="gaben">{gaben_html}</div>
  </div>
</section>

<div class="zeile" aria-hidden="true" data-lauf><div class="zeile__z">{laufworte * 6}</div></div>
{vergleich}
<section class="fl fl--blau blatt" id="ideen">
  <div class="in">
    {kopf(4, 'Ideen', ['Die Ideen', 'hinter der Seite.'], f'{n_ideen} Gedanken, die ich mir zu Ihrer Seite gemacht habe. Jeder davon ist im Entwurf zu sehen.')}
    <div class="gang"><div class="band">{ideen}</div>{gangfuss()}</div>
  </div>
</section>

<section class="fl fl--nacht blatt" id="gefuege">
  <div class="in">
    {kopf(5, 'Gefüge', ['Wie alles', 'zusammenhängt.'], 'Links steht, was von Ihnen kommt. In der Mitte, was ich daraus gemacht habe, daneben die Seiten und rechts alles, was im Hintergrund mitläuft. Tippen Sie auf eine Kachel oder lassen Sie sich einmal durchführen.')}
    <div class="brett-scroll" data-a="auf"><div class="brett-box">
      <div class="brett-k" aria-hidden="true">{''.join(f'<span style="left:{fx * 100:.1f}%"><i>{i + 1:02d}</i>{s}</span>' for i, (fx, s) in enumerate(zip(g['fx'], g['sp'])))}</div>
      <div class="brett" id="brett" data-sicht><svg aria-hidden="true"></svg><div id="brett-n"></div></div>
      <div class="brett-f">{e(g['fuss'])}</div>
    </div></div>
    <div class="brett-p" aria-live="polite">
      <div class="wechsel"><div class="k" id="bp-k">{g['start'][0]}</div><div class="t" id="bp-t">{g['start'][1]}</div></div>
      <div class="wechsel"><p id="bp-p">{g['start'][2]}</p><p class="weg" id="bp-w"></p></div>
      <div class="brett-p__k"><button class="kn kn--klein" id="brett-rund" type="button">Rundgang starten<i>{PF}</i></button><button class="kn kn--linie kn--klein" id="brett-noch" type="button">Nochmal aufbauen<i>{PF}</i></button></div>
      <span class="brett-uhr"></span>
    </div>
    <p class="brett-h">Am Handy lässt sich das Brett seitlich schieben.</p>
  </div>
</section>

<section class="fl fl--papier blatt" id="seiten">
  <div class="in">
    {kopf(6, 'Seiten', ['Alle Seiten zum', 'Durchblättern.'], 'Suchen Sie sich eine Seite aus und blättern Sie mit den Pfeilen durch die Ansichten. Rechts daneben sehen Sie dieselbe Stelle am Handy. Über «Öffnen» gelangen Sie auf die echte Seite.')}
    <div class="wahl" data-a="auf" role="group" aria-label="Seite wählen">{wahl}</div>
    <div class="schau" data-a="auf" tabindex="0">
      <div class="schau__f">
        <div class="fen"><div class="fen__k"><i></i><i></i><i></i><span></span></div><div class="schau__s"></div></div>
        <button class="rund schau__p schau__p--l" type="button" data-zur aria-label="Vorige Ansicht">{LI}</button>
        <button class="rund schau__p schau__p--r" type="button" data-vor aria-label="Nächste Ansicht">{RE}</button>
        <div class="schau__u mono"><div class="schau__pk" aria-hidden="true"></div><span class="schau__z"></span></div>
      </div>
      <div class="schau__r">
        <div class="tel"><div></div></div>
        <div class="schau__t"><h3></h3><p></p><a class="kn kn--klein" href="../index.html" target="_blank" rel="noopener">Öffnen<i>{PF}</i></a></div>
      </div>
    </div>
  </div>
</section>

<section class="fl fl--navy tapete blatt" id="unterlagen">
  <div class="in">
    <div class="karten">
      <div>
        {kap(7, 'Unterlagen')}
        {titel(['Ihre Unterlagen,', 'im selben Stil.'])}
        <div class="lauf" style="margin-top:clamp(22px,2.6vw,36px)"><p data-a="worte">{U['text'].format(n=zahl(z['unterlagen']), nk=zahl(z['unterlagen']).lower())}</p></div>
        <div class="kn-reihe" data-a="auf" style="margin-top:30px">{kn('Unterlagen durchblättern', '../unterlagen/index.html', neu=True)}{kn(U['knopf2'][0], U['knopf2'][1], 'kn--linie', neu=True) if U.get('knopf2') else ''}</div>
      </div>
      <div class="faecher faecher--{len(H.FAECHER)}" data-a="auf">
        {''.join(f'<a class="blattk blattk--{i + 1}" style="--j:{i}" href="../unterlagen/index.html#{f}" target="_blank" rel="noopener">{bild(f"pdf-{i}", "Idee: " + t)}<span>{t}<b>ansehen</b></span></a>' for i, (f, t) in enumerate(H.FAECHER))}
      </div>
    </div>
    <div class="namenzug" aria-hidden="true" data-lauf><div>{namen * max(4, 24 // max(1, len(unterlagen)))}</div></div>
  </div>
</section>

<section class="fl fl--nacht blatt" id="handschrift">
  <div class="in">
    {kopf(8, 'Handschrift', ['Ihr Haus bleibt', 'Ihr Haus.'], HS['text'])}
    <div class="bogen" data-a="auf">
      <div class="bogen__z"><div class="bogen__zl">
        <p class="etik"><span>{e(HS['marke_etik'])}</span><span>{e(H.NAME)}</span></p>
        <div class="marke"><div class="marke__w">{K.wortmarke()}</div><p>{HS['marke_text']}</p></div>
      </div></div>
      <div class="bogen__z schriften">{schriften}</div>
      <div class="bogen__z"><div class="bogen__zl">
        <p class="etik"><span>Farben</span><span>{e(HS['farben_etik'])}</span></p>
        <ul class="farbkarten">{farben_html}</ul>
      </div></div>
      <div class="bogen__z tapetenband">{HZ}<div><p class="etik"><span>{e(HS['muster_etik'])}</span></p><p>{HS['muster_text']}</p></div></div>
      <div class="bogen__z"><div class="bogen__zl probe-kn">
        <div><p class="etik"><span>Knöpfe</span></p><p>Jeder Knopf hat eine kleine Kante und gibt nach, wenn man ihn drückt. Probieren Sie es gern aus.</p></div>
        <div class="kn-reihe hell"><button class="kn" type="button">Drücken Sie mich<i>{PF}</i></button><button class="kn kn--linie" type="button">Mich auch<i>{PF}</i></button></div>
      </div></div>
    </div>
  </div>
</section>
''' + ('' if 'feed-handy' not in m else f'''
<section class="fl fl--navy tapete blatt" id="feed">
  <div class="in feedb">
    <div>
      {kap(9, 'Instagram')}
      {titel(['Ein Feed', 'für Instagram.'])}
      <div class="lauf" style="margin-top:clamp(22px,2.6vw,36px)"><p data-a="worte">{FD['text1']}</p><p data-a="worte">{FD['text2']}</p></div>
      <div class="kn-reihe" data-a="auf" style="margin-top:30px">{kn('Feed ansehen', '../feed/index.html', neu=True)}</div>
    </div>
    <div class="feedb__r" aria-hidden="true">
      <div class="feedb__h" data-a="schweb" style="--i:0">{bild('feed-handy', 'Das Instagram-Profil des Hauses als Idee, auf einem Handy')}</div>
      {''.join(f'<div class="abzug feedb__k feedb__k--{i + 1}" data-a="schweb" data-drift="{dr}" style="--i:{i + 2};--r:{r}deg;--r0:{r * 3}deg">{bild("fp-" + str(nr))}<span>{e(name)}</span></div>' for i, (nr, name, r, dr) in enumerate(FD['kacheln']))}
    </div>
  </div>
</section>
''') + f'''
<section class="fl fl--tief blatt" id="papier">
  <div class="in">
    {kopf(10, 'Papier', ['Ein paar Ideen', 'für Papier.'], 'Beim Bauen sind mir noch ein paar Dinge eingefallen, die gut zu Ihrem Haus passen könnten. Das sind alles nur Ideen. Nehmen Sie sich davon, was Ihnen gefällt.')}
    <div class="papier">
      <div class="pk" data-a="kipp"><div class="pk__b">{kleb_html}</div><h3>{z['etiketten']} {e(ET['name'])}</h3><p>{PA['etik_text']}</p>{kn(ET['name'] + ' ansehen', f'../{ET["ordner"]}/index.html', neu=True)}</div>
      <div class="pk pk--hell" data-a="kipp" style="--i:1"><div class="pk__b">{bogen_html}</div><h3>{z['druck']} Drucksachen</h3><p>{PA['druck_text']}</p>{kn('Drucksachen ansehen', '../drucksachen/index.html', neu=True)}</div>
    </div>
  </div>
</section>

<section class="fl fl--papier blatt" id="material">
  <div class="in mitte">
    <div class="streu" aria-hidden="true">{streu}</div>
    {kap(11, 'Material', ' style="justify-content:center"')}
    {titel(['Alles liegt für', 'Sie bereit.'])}
    <div class="lauf" style="margin-top:clamp(22px,2.6vw,36px)"><p data-a="worte">{MA['text']}</p></div>
    <div class="kn-reihe" data-a="auf" style="margin-top:clamp(28px,3.2vw,46px);justify-content:center">{kn('Ordner öffnen', '../material/index.html', neu=True)}</div>
  </div>
</section>

<section class="fl fl--creme blatt" id="dazu">
  <div class="in">
    {kopf(12, 'Ausblick', ['Was noch', 'dazukommt.'], AU['text'])}
    <div class="dazu">
      <div class="dazu__gross" data-a="kipp">{HZ}<small>Der nächste Schritt</small><h3>Das Studio</h3><p>{AU['studio']}</p></div>
      <ul class="dazu__z">
        {''.join(f'<li data-a="auf" style="--i:{i}"><h3>{e(t)}</h3><p>{x}</p></li>' for i, (t, x) in enumerate(AU['punkte']))}
      </ul>
    </div>
  </div>
</section>

<section class="schluss" id="schluss">
  {bild('schluss', klasse='schluss__b')}
  <div class="in">
    {kap(13, 'Danke')}
    {titel(['Ich freue mich', 'auf Ihre Antwort.'], 'h2', 't1')}
    <div class="lauf">
      <p data-a="worte">Wenn Ihnen der Entwurf gefällt, freue ich mich sehr, von Ihnen zu hören. Schreiben Sie mir einfach, was Sie denken. Wünsche und Änderungen sind jederzeit willkommen.</p>
    </div>
    <p class="gruss-u" data-a="auf"><b>Freundliche Grüsse, Robert Reff</b><small>aus Koh Phangan</small></p>
    <div class="kn-reihe" data-a="auf">{kn('Robert schreiben', 'mailto:robert@tasty-studios.de?subject=' + H.NAME.replace(' ', '%20') + '%20Website')}{kn('Website ansehen', '../index.html', 'kn--linie', neu=True)}</div>
  </div>
</section>
</main>

<footer class="fuss">
<nav class="in wege" aria-label="Alles auf einen Blick">
  <b class="wege__t" data-a="auf">Alles auf einen Blick</b>
  <div class="wege__r">{''.join(f'<a class="zielk" href="{h}" target="_blank" rel="noopener" data-a="kipp" style="--i:{i}"><span class="zielk__b">{bild("z-" + n, t)}</span><span class="zielk__z"><b>{t}</b><i>{PF}</i></span></a>' for i, (n, t, h) in enumerate(wege))}</div>
</nav>
<div class="in fuss__u">
  <div><b>Werkbank zum Entwurf</b><p>Das ist ein Entwurf von Robert Reff, Tasty Studios, und nicht die offizielle Website des Hauses. Fotos, Zeichen und Texte gehören {H.RECHTE}</p></div>
  <div class="r mono">{alle_vier}<a href="mailto:robert@tasty-studios.de">robert@tasty-studios.de</a><a href="https://www.instagram.com/tasty_studios2026" target="_blank" rel="noopener">@tasty_studios2026</a><span>Stand {K.STAND}</span></div>
</div></footer>

<script>window.GEFUEGE={json.dumps(g, ensure_ascii=False)};window.SEITEN={json.dumps(seiten, ensure_ascii=False)};</script>
<script src="werkbank.js?v={K.v('werkbank.js')}"></script>
</body>
</html>
'''
    K.schreib(os.path.join(ZIEL, 'index.html'), seite)
    gebraucht = {k + '.webp' for k in m}
    for f in os.listdir(IMG):
        if f not in gebraucht:
            os.remove(os.path.join(IMG, f))
    json.dump(z, open(os.path.join(W, 'zahlen.json'), 'w'), indent=1)
    print('gebaut:', os.path.join(ZIEL, 'index.html'), z, 'Seiten:', len(seiten), 'Ansichten:', sum(s['n'] for s in seiten))


if __name__ == '__main__':
    baue()
