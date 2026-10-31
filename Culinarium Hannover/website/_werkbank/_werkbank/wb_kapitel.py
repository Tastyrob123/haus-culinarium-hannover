#!/usr/bin/env python3
"""Werkbank Culinarium in Kapiteln (Werkbank-Chat Culinarium, 28.10.2026). Aufbau und Technik aus wb_kapitel.py der Taverne zum Schäfli (dort aus dem
Schlössli und dem Ruedihus), nur kopiert und umgeschrieben; Kleid und Worte von Culinarium. Läuft als Nachbau-Schritt nach dem Kit (haus.nach_bau) und stellt werkbank/index.html um:

  Auftakt · Brief · Worum es geht (Rechner, einmal) · Register
  I Was wir gefunden haben   die vier stärksten Funde aus dem Befund des Spähers, heute nur Instagram (sb_befund.py)
  II Ihre Marke              Handschrift-Tafel und Das Hausbuch
  III Ihre Website           Vergleich, Ideen, Gefüge, alle Seiten, Für Ihre Gäste
  IV Karten und Unterlagen   die Karten des Kartenmachers (Station 10) neben der heutigen Fassung
  V Eure Werkzeuge           Laptop mit La Maison und sechs Werkzeugen, «Einmal ändern, überall richtig.»
  VI Für draußen             Papier mit drei Karten (Untersetzer, Drucksachen, Mails), Feed, Dateien
  VII Geprüft
  VIII Das Angebot           Was Sie bekommen, Woche für Woche, «Ein Vorschlag.» (sb_angebot.py)
  Schluss · Fuss «Alles auf einen Blick» · Impressum
Kein Laufband (seitwärts laufende Bänder sind abgelehnt, Tasty-Sprache E), keine Rezeption im Chat (die Website hat keinen), keine Vision."""
import base64, datetime, html, io, json, os, re
from PIL import Image
import kern as K
import rh_kapitel as KP, rh_werkzeuge as WK, rh_strom as SB, rh_worum as VT, rh_impressum as IM, sb_worum as SW, sb_befund as BE, sb_angebot as SA
import fuss_faecher as FU, mails_reihe as ML, namen_fall as NF, orte_kurs as OK

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
ZIEL = os.path.join(ROOT, 'werkbank')
IMG = os.path.join(ZIEL, 'img')
PF, LI, RE = K.PF, K.LI, K.RE
STAND = datetime.date.today().strftime('%d.%m.%Y')
_ZVB = __import__('re').search(r'viewBox="([^"]+)"', open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', '..', '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium-zeichen.svg'), encoding='utf-8').read()).group(1)   # viewBox des «C» (29.10.)
ZEICHEN = f'<svg class="kap__z" viewBox="{_ZVB}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'   # das «C» der Wortmarke
VERTRAUEN = ('Ein Entwurf von Robert Reff, Tasty Studios, Hamburg, nicht die offizielle Website von Culinarium. Wer den Link nicht hat, findet die Seite nicht, '
             'in keiner Suchmaschine. Fotos, Plakate, Zeichen und Texte gehören Culinarium, dem Walk on the Wild Side und den jeweiligen Fotografen.')
LUPE = os.path.expanduser('~/Desktop/Website-Projekte/_Befund-Vorschlaege/lupe/EINBAU.md')
M, VORAB = {}, {}


# ------------------------------------------------------------------ Bilder
def webp(quelle, name, breite, q=82, schnitt=None, lage=(.5, .5)):
    """Bild nach werkbank/img/<name>.webp, dazu ein kleines echtes Abbild als Hintergrund (nie ein leerer Kasten). Gibt (Breite, Höhe) zurück."""
    im = quelle if isinstance(quelle, Image.Image) else Image.open(quelle)
    im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') and (name == 'ins-geraet' or name.startswith('bf-h-')) else 'RGB')
    if schnitt:
        w, h = im.size
        if w / h > schnitt:
            nw = round(h * schnitt); x0 = round((w - nw) * lage[0]); im = im.crop((x0, 0, x0 + nw, h))
        else:
            nh = round(w / schnitt); y0 = round((h - nh) * lage[1]); im = im.crop((0, y0, w, y0 + nh))
    if im.width > breite:
        im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    im.save(os.path.join(IMG, name + '.webp'), 'WEBP', quality=q, method=5)
    if im.mode == 'RGB':
        k = im.copy(); k.thumbnail((40, 40)); b = io.BytesIO(); k.save(b, 'WEBP', quality=40)
        VORAB[name] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    M[name] = im.size
    return im.size


def haus(key):
    return K.hausbild(key)


def bild(name, alt='', lazy=True, klasse=''):
    w, h = M[name]
    vor = f' style="background-image:url({VORAB[name]})"' if name in VORAB else ''
    return f'<img src="img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}"{" loading=\"lazy\" decoding=\"async\"" if lazy else ""} class="ld{(" " + klasse) if klasse else ""}"{vor}>'


# ------------------------------------------------------------------ Bausteine im Kleid dieser Werkbank
def kopf(_nr, name, zeilen, text):
    return (f'<div class="kopfzeile"><div><p class="kap kap--z" data-a="auf">{ZEICHEN}<span>{e(name)}</span></p>{K.titel(zeilen)}</div>'
            f'<div class="lauf"><p data-a="worte">{text}</p></div></div>')


def kopfk(anker, zeilen, text):
    return f'<div class="kopfzeile"><div>{KP.kap(anker)}{K.titel(zeilen)}</div><div class="lauf"><p data-a="worte">{text}</p></div></div>'


def gangfuss():
    return (f'<div class="gang__f"><button class="rund" type="button" data-zur aria-label="Zurück">{LI}</button><button class="rund" type="button" data-vor aria-label="Weiter">{RE}</button>'
            '<div class="gang__b"><i></i></div><div class="gang__z"></div></div>')


def kapitel(anker, teil):
    """Erster Abschnitt eines Kapitels: der Kopf trägt «Kapitel N» und den Namen des Kapitels, der Abschnitt den Anker."""
    teil = re.sub(r'<p class="kap kap--z"[^>]*>.*?</p>', lambda _m: KP.kap(anker), teil, count=1, flags=re.S)
    return re.sub(r'(<section\b[^>]*>)', lambda _m: _m.group(1) + f'<span class="k-anker" id="{anker}"></span>', teil, count=1)


def ers(t, alt, neu, n=1):
    if t.count(alt) != n:
        raise SystemExit(f'wb_kapitel: «{alt[:80]}» trifft {t.count(alt)}× statt {n}×')
    return t.replace(alt, neu)


# ------------------------------------------------------------------ die gebaute Seite in Abschnitte zerlegen
def zerlege(main):
    """Oberste <section>-Blöcke von <main>; was zwischen zwei Abschnitten steht (Skripte, Laufzeile), gehört zum Abschnitt davor."""
    teile, tiefe, start = [], 0, None
    for m in re.finditer(r'<section\b|</section>', main):
        if m.group(0) == '<section':
            if tiefe == 0:
                if start is not None:
                    teile.append(main[start:m.start()])
                start = m.start()
            tiefe += 1
        else:
            tiefe -= 1
    if start is not None:
        teile.append(main[start:])
    kopf_ = main[:main.index('<section')] if '<section' in main else main
    bloecke = {}
    for t in teile:
        mid = re.match(r'<section\b[^>]*\bid="([^"]+)"', t)
        if mid:
            bloecke[mid.group(1)] = t
        elif 'auftakt' in t[:200]:
            bloecke['auftakt'] = t
    return kopf_, bloecke


def zaehle():
    H = K.H
    z = json.load(open(os.path.join(W, 'zahlen.json'), encoding='utf-8'))
    z['gaeste_seiten'] = len([s for s in H.SEITEN if s[4] != 'recht'])
    recht = [d for d in ('impressum.html', 'datenschutz.html', 'agb.html') if os.path.exists(os.path.join(os.path.dirname(ROOT), d))]   # die Website liegt eine Ebene über dem Revier
    z['seiten'] = z['gaeste_seiten'] + len(recht)   # gezählt wie Le Bureau: alle Seiten der Website, das Rechtliche mit (Oberchef 21.10.2026)
    z['mails'] = len(ML.LISTE)
    return z


ZAHLWORT = {3: 'drei', 4: 'vier', 5: 'fünf', 6: 'sechs', 7: 'sieben', 8: 'acht', 9: 'neun', 10: 'zehn', 11: 'elf', 12: 'zwölf', 14: 'vierzehn', 15: 'fünfzehn', 20: 'zwanzig', 30: 'dreissig'}


# ------------------------------------------------------------------ neue und geänderte Abschnitte
def papier_mails(z):
    """Die Mails als dritte Karte im Papier (Master 5b-neu: nie als eigener Abschnitt)."""
    ml = [x for x in ML.LISTE if os.path.exists(os.path.join(IMG, f'ml-{x[0]}.webp'))]
    for x in ml:
        M['ml-' + x[0]] = Image.open(os.path.join(IMG, f'ml-{x[0]}.webp')).size
    orte = [(7, 1, 22, -2), (39, 1, 22, 2), (71, 1, 22, -2), (7, 52, 22, 2), (39, 52, 22, -2), (71, 52, 22, 2)]   # zwei Reihen mit Abstand, keine leere Fläche (Robert 29.10.2026)
    karten = ''.join(f'<a class="bogenb mlp" href="../mails/{x[1]}/index.html" target="_blank" rel="noopener" data-a="schweb" style="left:{l}%;top:{tp}%;width:{w}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i}">{bild("ml-" + x[0], "Mail: " + x[2])}</a>'
                     for i, (x, (l, tp, w, r)) in enumerate(zip(ml, orte)))
    return (f'<div class="pk pk--mail" data-a="kipp" style="--i:2"><div class="pk__b">{karten}</div><h3>{str(ZAHLWORT.get(len(ml), len(ml))).capitalize()} Mails</h3>'
            f'<p>Was ein Gast nach seiner Buchung, seinem Eintrag auf der Warteliste und vor dem Abend im Postfach findet. Namen und Daten darin sind ausgedacht.</p>'
            f'{K.kn("Mails ansehen", "../mails/index.html", neu=True)}</div>') if ml else ''


def papier_postkarten():
    """Die Postkarten als eigener Punkt im Papier (Robert über den Oberchef 29.10.2026): eine Karte je Plakat, Bild im Kartenständer (nichts überdeckt)."""
    if not os.path.exists(os.path.normpath(os.path.join(ZIEL, '../postkarten/index.html'))):
        return ''
    n = len(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postkarten_plan.json')))['karten'])   # Zahl aus dem Plan der Gestaltung
    return (f'<div class="pk pk--post" data-a="kipp" style="--i:3"><div class="pk__b"><img src="../postkarten/img/staender.webp" width="1400" height="900" alt="Die Postkarten im Kartenständer" loading="lazy" decoding="async"></div>'
            f'<h3>{n} Postkarten</h3><p>Eine zu jedem Plakat, mit Beschnitt für die Druckerei und als Sammelbogen SRA3.</p>'
            f'{K.kn("Postkarten ansehen", "../postkarten/index.html", neu=True)}</div>')


def schluss():
    stube = [w for w in WK.WERKZEUGE if w[0] == 'maison'][0]
    return f'''<section class="schluss" id="schluss">
  {bild('sb-schluss', klasse='schluss__b')}
  <div class="in">
    <p class="kap kap--z" data-a="auf">{ZEICHEN}<span>Bis Montag</span></p>
    {K.titel(['Die Kerzen', 'brennen schon.'], 'h2', 't1')}
    <div class="lauf">
      <p data-a="worte">Was hier liegt, ist für Culinarium gemacht: die Seite, die Werkzeuge, jedes Blatt. Öffnet es, so oft ihr mögt, und sagt mir, wo es noch nicht nach euren Abenden aussieht.</p>
    </div>
    <div class="rh-gruss" data-a="auf"><p class="rh-gruss__t">Bis Montag<span class="rh-gruss__b">{bild('robert', 'Robert Reff')}</span></p>
      <p class="rh-gruss__n"><img class="rh-gruss__sig" src="img/unterschrift.webp" width="{M['unterschrift'][0]}" height="{M['unterschrift'][1]}" alt="Unterschrift Robert Reff" loading="lazy" decoding="async"><span>Robert Reff · Tasty Studios</span></p></div>
    {OK.block('schluss')}
    <div class="kn-reihe" data-a="auf">{K.kn('Website ansehen', '../index.html', neu=True)}{K.kn(NF.akk(stube[1]) + ' öffnen', stube[6], 'kn--linie', neu=True) if stube[6] else ''}</div>
  </div>
</section>'''


def fuss_wege():
    """«Alles auf einen Blick» nach Wichtigkeit: die Website, die Zentrale und die Werkzeuge, dann Gäste, Karten, Papier, Untersetzer, Feed, Dateien, Befund, Prüfbericht."""
    w = {x[0]: x for x in WK.WERKZEUGE}
    wege = [('website', 'Die neue Website', '../index.html')]
    wege += [(k, w[k][1], w[k][6]) for k in ('maison', 'bureau', 'carte', 'reception', 'livre', 'registre', 'imprimerie') if w[k][6]]
    wege += [('gaeste', 'Für eure Gäste', '../abend.html')]
    wege += [x for x in (('unterlagen', 'Eure Karten', '../unterlagen/index.html'), ('drucksachen', 'Drucksachen', '../drucksachen/index.html'), ('etiketten', 'Untersetzer', '../untersetzer/index.html'), ('postkarten', 'Postkarten', '../postkarten/index.html'), ('sticker', 'Sticker', '../sticker/index.html'), ('beigaben', 'Beigaben', '../beigaben/index.html'))
             if os.path.exists(os.path.normpath(os.path.join(ZIEL, x[2])))]
    if os.path.exists(os.path.join(ROOT, 'feed', 'index.html')):
        wege.append(('feed', 'Der Feed', '../feed/index.html'))
    wege += [x for x in (('material', 'Dateien', '../material/index.html'), ('analyse', 'Der Befund', '../befund/index.html'), ('geprueft', 'Geprüft', 'geprueft/index.html'))
             if os.path.exists(os.path.normpath(os.path.join(ZIEL, x[2])))]
    return wege


def eigene_titel(t):
    """Eigene Überschriften, Kapitelnamen und Schlusssatz des Hauses (haus.py TITEL_NEU, KAP_NAME_NEU, TEXT_NEU, SCHLUSS_SATZ_NEU; Werkbank-Regel 14; aus der Werkbank des Waldhotel Doldenhorn kopiert, 17.10.2026).
    Ersetzt nur ganze Titel im Markup von K.titel und ganze Kapitelnamen, nichts im Fliesstext."""
    H = K.H
    for (a1, a2), (n1, n2) in getattr(H, 'TITEL_NEU', {}).items():
        alt = f'<span class="z"><span>{e(a1)}</span></span><span class="z"><span><em>{e(a2)}</em></span></span>'
        t = t.replace(alt, f'<span class="z"><span>{e(n1)}</span></span><span class="z"><span><em>{e(n2)}</em></span></span>')
    for a, n in getattr(H, 'KAP_NAME_NEU', {}).items():
        t = re.sub(r'(<p class="kap[^"]*"[^>]*>(?:<svg.*?</svg>)?<span>)' + re.escape(e(a)) + r'(</span></p>)', lambda m: m.group(1) + e(n) + m.group(2), t)
    for a, n in getattr(H, 'TEXT_NEU', []):
        if a in t:
            t = t.replace(a, e(n))
        else:
            print('wb_kapitel: Übergang nicht gefunden (Quelle geändert?):', a[:60])
    if getattr(H, 'SCHLUSS_SATZ_NEU', None):
        t = t.replace(H.SCHLUSS_SATZ_NEU[0], H.SCHLUSS_SATZ_NEU[1])
    return t


def anwenden(pfad):
    os.makedirs(IMG, exist_ok=True)
    M.clear(); VORAB.clear()
    KP.BEFUND_DA = True
    z = zaehle()
    t = open(pfad, encoding='utf-8').read()
    for n in ('robert',):
        M[n] = Image.open(os.path.join(IMG, n + '.webp')).size
    WK.bilder(lambda q, n, b, qu=86: webp(q, n, b, qu))
    SB.bilder(lambda q, n, b, qu=82: webp(q, n, b, qu))
    BE.bilder(lambda q, n, b, qu=84: webp(q, n, b, qu))
    SW.bilder(lambda q, n, b, qu, schnitt=None, lage=(.5, .5): webp(q, n, b, qu, schnitt, lage), lambda key: K.H.bild(key))
    SA.bilder(lambda q, n, b, qu, schnitt=None, lage=(.5, .5): webp(q, n, b, qu, schnitt, lage), haus)
    BE.kopiere_analyse()
    AN_ = os.path.join(W, 'ansichten')
    for n, q in (('gpm-website', os.path.join(AN_, 'Rechner', 'Startseite.jpg')), ('gpm-karten', os.path.join(ROOT, 'unterlagen', 'img', 'n-abend-01.webp')),
                 ('gpm-werkzeuge', os.path.join(AN_, 'Werkzeuge', 'bureau.jpg')), ('gpm-daten', os.path.join(AN_, 'Gaeste', 'warteliste.jpg')),
                 ('gpm-suche', os.path.join(AN_, 'Rechner', 'Der Weg.jpg')), ('gpm-offen', haus(K.H.bild('m7')))):
        if os.path.exists(q):
            webp(q, n, 1040, 80, 16 / 9, (.5, 0))
    webp(haus(K.H.SCHLUSS['bild']), 'sb-schluss', 1920, 80)   # die Bar bei Nacht von draußen (kein Foto zweimal auf der Werkbank)
    import shutil
    shutil.copy2(os.path.join(ZIEL, 'eigen', 'unterschrift.webp'), os.path.join(IMG, 'unterschrift.webp'))
    M['unterschrift'] = Image.open(os.path.join(IMG, 'unterschrift.webp')).size
    k = dict(e=e, bild=bild, kn=K.kn, kap=K.kap, titel=K.titel, kopf=kopf, kopfk=kopfk, m=M, z=z, PF=PF, LI=LI, RE=RE, lokal=KP.LOKAL, gangfuss=gangfuss)

    a, b = t.index('<main id="oben">') + len('<main id="oben">'), t.index('</main>')
    vor_main, B = zerlege(t[a:b])

    def nimm(n, muss=True):
        if n not in B:
            if muss:
                raise SystemExit(f'wb_kapitel: Abschnitt «{n}» fehlt in der gebauten Seite')
            return ''
        return B[n]

    auftakt = nimm('auftakt').replace('Diese Werkbank ist', 'Diese Seite ist')
    brief = nimm('brief')
    worum = SW.blatt(k)
    register = KP.register(kopf(0, 'Register', ['Acht Kapitel,', 'ein Abend.'], 'Vom Befund, wie Culinarium heute im Netz steht, bis zum Vorschlag am Ende. Jedes Kapitel lässt sich direkt öffnen.'))
    k1 = BE.abschnitt(k, kopfk)
    hs = kapitel('k2', nimm('handschrift'))
    livre = [w for w in WK.WERKZEUGE if w[0] == 'livre'][0]
    if livre[6]:
        zeile = (f'<div class="kn-reihe rh-livre" data-a="auf"><p>Wortmarke, Schriften, Farben, Plakate und Fotos liegen in einem eigenen Werkzeug: {e(livre[1])}, die Marke zum Arbeiten, mit den Hausregeln zum Nachschlagen.</p>'
                 f'{K.kn(NF.akk(livre[1]) + " öffnen", livre[6], neu=True)}</div>')
        i = hs.rindex('</section>'); j = hs.rindex('</div>', 0, i)
        hs = hs[:j] + zeile + hs[j:]
    vergleich = kapitel('k3', nimm('vergleich'))
    un = kapitel('k4', nimm('unterlagen'))
    fen_haus = nimm('fenster-haus')
    fen_tisch = nimm('fenster-tisch')
    wk, fehlt = WK.abschnitt(k, KP.platzhalter)
    pa = kapitel('k6', nimm('papier'))
    mk = papier_mails(z) + papier_postkarten()
    if mk:
        i = pa.index('<div class="papier">'); tiefe, j = 0, i
        for mm in re.finditer(r'<div\b|</div>', pa[i:]):
            tiefe += 1 if mm.group(0) == '<div' else -1
            if tiefe == 0:
                j = i + mm.start(); break
        pa = pa[:j] + mk + pa[j:]
    material = nimm('material').replace('<span>Material</span>', '<span>Dateien</span>')
    gp = kapitel('k7', nimm('geprueft'))
    k8 = SA.angebot(k)

    folge = [auftakt, brief, register, k1, hs, vergleich, nimm('ideen'), nimm('gefuege'), nimm('seiten'), nimm('gaeste', False), un,
             fen_haus, wk, pa, nimm('feed', False), material, gp, fen_tisch, k8, schluss()]
    t = t[:a] + vor_main + '\n'.join(x for x in folge if x) + '\n' + t[b:]

    t = re.sub(r'<nav aria-label="Abschnitte">.*?</nav>', '<nav aria-label="Kapitel">' + KP.leiste() + '</nav>', t, count=1, flags=re.S)
    t = t.replace('<b>CULINARIUM</b><span>Werkbank</span>', '<b>CULINARIUM</b><span>Entwurf</span>')
    t = re.sub(r'<title>[^<]*</title>', '<title>Alles auf einen Blick · Culinarium</title>', t, count=1)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\1Alles auf einen Blick · Culinarium', t)

    fi, fj = t.index('<nav class="in wege wf"'), t.index('<div class="in fuss__u">')
    t = t[:fi] + FU.abschnitt(fuss_wege()).replace('<nav class="in wege wf"', '<nav class="in wege wf" id="uebersicht"', 1) + '\n' + t[fj:]
    fu_a = t.index('<div class="in fuss__u">'); fu_b = t.index('</div></footer>', fu_a)
    t = t[:fu_a] + (f'<div class="in fuss__u">\n  <div><b>Entwurf</b><p>{VERTRAUEN}</p></div>\n'
                    f'  <div class="r mono"><span>robert@tasty-studios.de</span><a href="impressum.html">Impressum und Datenschutz</a><span>Stand {STAND}</span></div>\n') + t[fu_b:]
    t = eigene_titel(t)
    open(pfad, 'w', encoding='utf-8').write(t)

    # Eigene Datei kapitel.css (Schlössli 20.10.2026): andere Bauten des Kits (Unterlagen, Drucksachen) schreiben werkbank.css neu und löschten so die Kapitel.
    css_p = os.path.join(ZIEL, 'werkbank.css')
    alt = open(css_p, encoding='utf-8').read()
    MARKE = '/* ================= Kapitel (wb_kapitel.py, Werkbank-Chat 17.10.2026) ================= */'
    if MARKE in alt:
        open(css_p, 'w', encoding='utf-8').write(alt[:alt.index(MARKE)])
    neu = K.faerbe(KP.CSS + VT.CSS + SW.CSS + WK.CSS + SB.CSS + BE.CSS + SA.CSS + OK.CSS)
    neu = re.sub(r'url\(\.\./assets/img/tapete\.webp\) 50% 0/\d+px auto', 'var(--muster) 50% 0/var(--musterb) auto', neu)
    import sb_farbe as _sf
    open(os.path.join(ZIEL, 'kapitel.css'), 'w', encoding='utf-8').write('/* Kapitel der Werkbank Culinarium (wb_kapitel.py), eigene Datei */\n' + _sf.ohne_fett(_sf.faerbe(neu + EIGEN_CSS)))
    t = open(pfad, encoding='utf-8').read()
    if 'kapitel.css' not in t:
        t = re.sub(r'(<link rel="stylesheet" href="werkbank\.css[^"]*">)', lambda m_: m_.group(1) + f'\n<link rel="stylesheet" href="kapitel.css?v={int(datetime.datetime.now().timestamp())}">', t, count=1)
        open(pfad, 'w', encoding='utf-8').write(t)

    open(os.path.join(ZIEL, 'impressum.html'), 'w', encoding='utf-8').write(IM.impressum_html('../', 'index.html', 'Zurück zu «Alles auf einen Blick»'))
    unterseiten()
    if fehlt:
        print('wb_kapitel: im Laptop fehlen Bildschirme:', fehlt)
    print('wb_kapitel: Kapitel gesetzt,', z)


# Was nur für diese Werkbank gilt (nach der Vorlage, darum zuletzt)
EIGEN_CSS = '''
/* Werkbank-Regel 1 (Robert 17.10.2026): seitliches Scrollen und Wischen in Bändern und Kacheln bleibt wie im Kit. Behoben ist nur das Hängenbleiben:
   was seitlich scrollt, hat kein eigenes senkrechtes Scrollen (overflow-x:auto macht overflow-y sonst zu auto) und hält das Mausrad nicht fest,
   das senkrechte Scrollen läuft immer an die Seite weiter. Kein wheel-Handler, kein preventDefault. */
.band,.wahl,.vh-wahl,.ins-reiter,.brett-scroll,.schritte,.bfk-liste,.fb__reiter{overflow-y:hidden!important;overscroll-behavior-y:auto!important}
.gf__tel .tel>div{overflow-y:hidden!important;overscroll-behavior:auto!important}
/* Zeichen der Bühne «Einmal ändern» und der Karte: das Medaillon in Gold */
.fbs__zeichen{fill:currentColor!important;color:var(--gold)}
.ag-z{fill:currentColor!important;color:#b78f51}
/* Das Hausbuch unter der Handschrift-Tafel */
.rh-livre{justify-content:center;align-items:center;flex-wrap:wrap;gap:16px 22px;margin-top:clamp(30px,3.4vw,52px)}
.rh-livre p{flex-basis:100%;max-width:56ch;margin:0 auto 4px;text-align:center;font-family:var(--serif);font-size:clamp(1.08rem,1.2vw,1.24rem);line-height:1.5;color:rgba(251,245,234,.86)}
.fl--papier .rh-livre p,.fl--creme .rh-livre p{color:var(--tinte)}
/* Mails als dritte Karte im Papier: hochkant, oben bündig */
.pk--mail .pk__b{position:relative}
.pk--post .pk__b{overflow:hidden;border-radius:clamp(14px,1.6vw,22px)}.pk--post .pk__b img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.mlp img{aspect-ratio:856/1227!important}
/* Schluss: das Haus zur blauen Stunde bleibt Held, die Schrift steht ruhig darüber (Foto gedämpft, kein Verlauf); Gruss wie beim Rivage:
   Porträt rund rechts, Unterschrift rechtsbündig, darunter klein Name, Tasty Studios, Hamburg (Master Website-Bau 2, Robert 17.10.2026) */
.schluss__b{filter:brightness(.5) saturate(.92)}
.rh-gruss{display:flex;flex-direction:column;align-items:center;max-width:560px;margin:clamp(26px,3vw,44px) auto 0;text-align:center}   /* Robert 29.10.2026: alles auf einer Mitte */
.rh-gruss__t{display:flex;align-items:center;gap:clamp(16px,1.6vw,24px);margin:0;font-family:var(--serif);font-weight:700;font-size:clamp(1.3rem,1.8vw,1.8rem);color:#fbf5ea;text-shadow:0 2px 14px rgba(15,8,3,.85)}
.rh-gruss__b{display:block;width:clamp(78px,6.6vw,104px);aspect-ratio:1;border-radius:50%;overflow:hidden;box-shadow:0 0 0 1px rgba(15,8,3,.3),0 0 0 5px #fbf5ea,0 0 0 6px rgba(183,143,81,.6),0 18px 24px -14px rgba(0,0,0,.7)}
.rh-gruss__b img{display:block;width:100%;height:100%;object-fit:cover}
.rh-gruss__n{display:flex;flex-direction:column;align-items:center;gap:4px;margin:clamp(16px,2vw,24px) 0 0}   /* Robert 18.10.2026: kleiner, nicht am Rand, Luft */
.rh-gruss__sig{display:block;width:clamp(112px,9vw,150px);height:auto;filter:invert(1) brightness(1.6) sepia(.4);transform:rotate(-3deg)}
.rh-gruss__n span{font-family:var(--mono);font-size:clamp(9px,2.5vw,10.5px);letter-spacing:.12em;white-space:nowrap;text-transform:uppercase;color:rgba(251,245,234,.82)}
/* Befund: der Weg zur ganzen Analyse mittig unter der Lupe */
.lu-weg{justify-content:center;margin-top:clamp(24px,2.6vw,40px)}
/* Register: Ziffern und Kopf im Kleid von Culinarium */
.rgw .wfa__texte h3{font-weight:400}
.kap--k .kap__z{display:block;margin:10px auto 8px}
'''


def unterseiten():
    """Die Seiten neben «Alles auf einen Blick» (Prüfbericht, Unterlagen, Drucksachen, Zündhölzer, Feed, Mails, Dateien): für das Haus heisst die Werkbank
    «Alles auf einen Blick», das Material «Dateien», und nichts öffnet ein Mailprogramm (Robert 17.10.2026). Die Adresse steht als Text."""
    for rel in ('werkbank/geprueft', 'unterlagen', 'drucksachen', 'untersetzer', 'feed', 'mails', 'material', 'werkbank/anleitung', 'befund'):
        p = os.path.join(ROOT, rel, 'index.html')
        if not os.path.exists(p):
            continue
        t = open(p, encoding='utf-8').read()
        t = t.replace('<span>Werkbank</span></a>', '<span>Entwurf</span></a>').replace('<span>Werkbank</span>', '<span>Entwurf</span>')
        t = t.replace(' · Werkbank Culinarium</title>', ' · Culinarium</title>').replace('Werkbank · Culinarium', 'Alles auf einen Blick · Culinarium')
        t = t.replace('>Zurück zur Werkbank<', '>Zurück zu «Alles auf einen Blick»<').replace('>Zur Werkbank<', '>Alles auf einen Blick<')
        t = t.replace('<b>Werkbank zum Entwurf</b>', '<b>Entwurf</b>')
        t = t.replace('Jedes Bild trägt eine Beschreibung', 'Jedes Bild hat eine Beschreibung')
        t = re.sub(r'Jede der (\d+)(\s|&nbsp;|\u00a0)Seiten trägt', r'Jede der \1 Seiten hat', t)   # Seitenzahl ohne das Rechtliche, wie überall gezählt
        t = re.sub(r'(A|a)lle dreizehn(\s|&nbsp;|\u00a0)Seiten', lambda m: m.group(1) + 'lle zwölf Seiten und das Rechtliche', t)
        t = re.sub(r'<a class="kn[^"]*" href="mailto:[^"]*">Robert schreiben<i>.*?</i></a>', '', t, flags=re.S)
        t = re.sub(r'<a href="mailto:([^"?]+)">([^<]*)</a>', r'<span>\2</span>', t)
        t = re.sub(r'<a[^>]*href="https://www\.instagram\.com/tasty[^"]*"[^>]*>[^<]*</a>', '', t)
        t = t.replace('Fehlt Ihnen eine Datei oder ein Format, schreiben Sie mir gern.', 'Fehlt euch eine Datei oder ein Format, lege ich sie gern dazu.')
        # Robert 18.10.2026 ~14:55: die Werkzeug-Knöpfe «… nicht auf die Landingpage von der Werkbank, sondern in die Bereiche rein … wenn ich dann
        # die Karten gesehen habe»: am Ende der Unterseite, nach den neuen Stücken, ein eigener Ausklang mit einem Knopf (online nur Vorschau)
        _pf = '<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i></a>'
        _w = {x[0]: x[6] for x in WK.WERKZEUGE}
        _wz = {k_: v_ for k_, v_ in {'unterlagen': (f'Diese Karten pflegt ihr selbst, {NF.in_(WK.NAMEN["carte"])}.', _w.get('carte'), 'Karten selbst ändern'),
               'drucksachen': (f'Neue Plakate und Drucksachen setzt ihr selbst, {NF.in_(WK.NAMEN["imprimerie"])}.', _w.get('imprimerie'), 'Drucksache selbst setzen')}.items() if v_[1]}
        if rel in _wz and 'ausklang--werkzeug' not in t:
            satz, weg, text = _wz[rel]
            t = t.replace('<section class="ausklang">', f'<section class="ausklang ausklang--werkzeug"><div class="in"><p data-a="auf">{satz}</p><div class="kn-reihe" data-a="auf"><a class="kn" href="{weg}" target="_blank" rel="noopener">{text}{_pf}</div></div></section>\n<section class="ausklang">', 1)
        if rel == 'material':
            t = t.replace('<title>Material · Culinarium</title>', '<title>Dateien · Culinarium</title>').replace('<span>Material</span>', '<span>Dateien</span>').replace('<b>Material zum Entwurf</b>', '<b>Dateien zum Entwurf</b>')
            t = material_nachtragen(t)
            t = t.replace('Ihre Unterlagen als Idee im Stil der neuen Seite, jede als PDF.', 'Eure Karten im neuen Satz, jede als PDF.')
            t = mit_vorschau(t, os.path.join(ROOT, 'material'))
        if rel == 'werkbank/geprueft':
            t = pruef_bilder(t)
            # Demo-Check Schäfli 21.10.2026: der Kit schreibt jedem Haus Zimmer und Booking in den Prüfbericht; Culinarium sind Abende ohne Zimmer
            for _a, _b in (('Adresse, Telefon, Buchung, Restaurants und Öffnungszeiten', 'Adresse, Termine, Plätze und Zeiten der Abende'),
                           ('Ihre Zimmer, Restaurants und Angebote auch wirklich lesen', 'eure Abende, Menüs und Plakate auch wirklich lesen'),
                           ('gleiche Angaben auf Booking, Tripadvisor und den Portalen', 'gleiche Angaben auf Tripadvisor und den Portalen')):
                t = t.replace(_a, _b)
        open(p, 'w', encoding='utf-8').write(t)


VS_CSS = ('<style id="sb-vorschau">.dateien li a{display:flex;align-items:center;gap:16px}.dt-b{flex:none;display:block;width:clamp(64px,6vw,88px);aspect-ratio:4/3;border-radius:8px;overflow:hidden;'
          'background:var(--creme);box-shadow:0 8px 14px -10px rgba(4,16,35,.5)}.dt-b img{display:block;width:100%;height:100%;object-fit:contain;object-position:50% 50%;padding:4px;box-sizing:border-box}.dateien li a>span:not(.dt-b){flex:1}'
          '.gp__bild{display:block;width:100%;max-width:520px;aspect-ratio:16/9;margin:18px 0 6px;border-radius:16px;overflow:hidden;box-shadow:0 26px 34px -24px rgba(4,16,35,.6)}.gp__bild img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 0}</style>')


def mit_vorschau(t, ordner):
    """Robert 20.10.2026 «in allen Tools Bilder dazu»: jede Datei in der Liste mit ihrem Bild (erste Seite der PDF, das Bild selbst), aus den Dateien des Ordners."""
    import hashlib, subprocess, urllib.parse
    vz = os.path.join(ordner, '_vorschau'); os.makedirs(vz, exist_ok=True)

    def eins(m):
        href = html.unescape(m.group(2)); q = os.path.join(ordner, urllib.parse.unquote(href))
        if 'class="dt-b"' in m.group(0) or not os.path.exists(q):
            return m.group(0)
        n = hashlib.sha1(href.encode()).hexdigest()[:12]; z = os.path.join(vz, n + '.webp')
        if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(q):
            ext = os.path.splitext(q)[1].lower()
            try:
                if ext == '.pdf':
                    subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-r', '30', '-png', '-singlefile', q, z[:-5]], check=True)
                    im = Image.open(z[:-5] + '.png'); os.remove(z[:-5] + '.png')
                elif ext in ('.jpg', '.jpeg', '.png', '.webp'):
                    im = Image.open(q)
                elif ext == '.txt' and os.path.exists(os.path.join(ROOT, 'feed', 'avatar.jpg')):
                    im = Image.open(os.path.join(ROOT, 'feed', 'avatar.jpg'))
                elif ext == '.svg':   # Tor 4 30.10.2026: das Logo bekommt sein Bild (QuickLook zeichnet die SVG, auf den Inhalt zugeschnitten)
                    import tempfile, shutil
                    from PIL import ImageOps
                    tmp = tempfile.mkdtemp(); subprocess.run(['qlmanage', '-t', '-s', '480', '-o', tmp, q], check=True, capture_output=True)
                    roh = Image.open(os.path.join(tmp, os.path.basename(q) + '.png')).convert('RGB'); shutil.rmtree(tmp, ignore_errors=True)
                    box = ImageOps.invert(roh).getbbox(); im = roh.crop(box) if box else roh
                else:
                    im = None
                if im is None:
                    return m.group(0)
                im = im.convert('RGB'); im.thumbnail((240, 240)); im.save(z, 'WEBP', quality=78)
            except Exception:
                return m.group(0)
        return m.group(1) + f'<span class="dt-b"><img src="_vorschau/{n}.webp" alt="" loading="lazy" decoding="async"></span>'
    t = re.sub(r'(<li[^>]*><a href="([^"]+)"[^>]*>)(?!<span class="dt-b">)', eins, t)   # Gestaltung 28.10.2026: nur einmal; vorher kam bei jedem Bau ein weiteres Bild dazu (13 gleiche Vorschauen je Datei)
    if 'id="sb-vorschau"' not in t:
        t = t.replace('</head>', VS_CSS + '</head>', 1)
    else:
        t = re.sub(r'<style id="sb-vorschau">.*?</style>', lambda m: VS_CSS, t, count=1, flags=re.S)   # neuer Stand der Regeln auch auf gebauten Seiten
    return t


def pruef_bilder(t):
    """Prüfbericht: jeder Teil mit seinem Bild unter der Überschrift."""
    B = {'Die Website': 'gpm-website', 'Die Karten': 'gpm-karten', 'Die sieben Werkzeuge': 'gpm-werkzeuge', 'Ihre Daten und die Ihrer Gäste': 'gpm-daten', 'Die Suche': 'gpm-suche', 'Was offen bleibt': 'gpm-offen'}
    for h2, n in B.items():
        if os.path.exists(os.path.join(IMG, n + '.webp')) and f'../img/{n}.webp' not in t:
            t = t.replace(f'<h2>{h2}</h2>', f'<h2>{h2}</h2><span class="gp__bild"><img src="../img/{n}.webp" alt="" loading="lazy" decoding="async"></span>', 1)
    if 'id="sb-vorschau"' not in t:
        t = t.replace('</head>', VS_CSS + '</head>', 1)
    return t


def material_nachtragen(t):
    """Abgleich Beigaben gegen material/ (Regel 8, 17.10.2026): der Kit legt nur die Drucksachen aus papier_plan.json in «02 Drucksachen»; die weiteren
    aus papier_mehr.json fehlten dort. Sie werden dazugelegt (nur kopiert, nichts gelöscht) und in die Liste der Dateien-Seite eingetragen."""
    import shutil
    H = K.H
    p_mehr = os.path.join(W, 'papier_mehr.json')
    mehr = json.load(open(p_mehr, encoding='utf-8')).get('druck', []) if os.path.exists(p_mehr) else []
    ordner = os.path.join(ROOT, 'material', '02 Drucksachen')
    zeilen = ''
    for x in mehr:
        q = os.path.join(ROOT, 'drucksachen', 'pdf', f"{H.KURZ}-{x['id']}.pdf")
        name = f"{H.NAME} {x['name'].replace('«', '').replace('»', '').replace('/', ' ')}.pdf"
        if not os.path.exists(q):
            continue
        if not os.path.exists(os.path.join(ordner, name)):
            os.makedirs(ordner, exist_ok=True); shutil.copy2(q, os.path.join(ordner, name))
        href = '02 Drucksachen/' + name
        if f'href="{html.escape(href)}"' not in t and 'id="o2"' in t:
            zeilen += f'<li data-a="auf" style="--i:6"><a href="{html.escape(href)}" target="_blank" rel="noopener"><span>{e(x["name"])}</span><i>{PF}</i></a></li>'
    if zeilen:
        i = t.index('id="o2"'); j = t.index('</ul>', i)
        t = t[:j] + zeilen + t[j:]
    return t
