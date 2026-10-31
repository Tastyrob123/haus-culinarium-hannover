#!/usr/bin/env python3
"""Culinarium Hannover · Startseite: 15 Fassungen der Überleitung zwischen Einstieg (#auftakt) und «Abend und Haus» (#ebenen).
Robert 26.10.2026: «wir müssen irgendwie noch eine Überleitung haben zwischen den beiden Abschnitten» (abgelehnt: mittiger Satz mit senkrechter Linie).
Liest die fertige index.html (nach bau.py / varianten.py), setzt zwischen Auftakt und #ebenen einen Rahmen mit Fassung 0 (heutiger Stand, nichts dazwischen)
und den Fassungen 1 bis 15, bindet assets/ueberleitung.css und .js ein. Läuft beliebig oft, ohne sich zu verdoppeln.
Pfeiltasten ← →, schmale Leiste unten mit Nummer und Vorschaubild, Stand in der Adresse (?u=N), beim Wechsel springt die Seite an die Überleitung.
Jede Fassung hat eine eigene Anordnung und genau eine eigene Bewegung; nur transform und opacity, nativer Scroll.
Fakten nur aus den Quellen der Seite: Haasemannstraße 13, 30449 Hannover-Linden; Bar Donnerstag bis Samstag ab 19 Uhr; Culinarium Freitag ab 19, Samstag ab 17 Uhr.
Nur Fotos aus Rudis Dateien (keine Gast- oder Fremdbilder), keines, das im Einstieg oder in «Abend und Haus» schon steht.
Aufruf: python3 website/ueberleitung.py   (läuft auch am Ende von varianten.py)
Vorschaubilder: python3 website/ueberleitung.py daumen   (nimmt jede Fassung in WebKit auf, Playwright aus ~/Aussen-Pruefung)
Fest einbauen: WAHL = Nummer setzen und neu bauen (Leiste und Pfeiltasten aus)."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, BILD, VERSION, marke

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))
ANF, END = '<!--ueberleitung-->', '<!--/ueberleitung-->'

WAHL = 1   # Robert 26.10.2026: «1» (Darüber); 0 = alle Fassungen zum Durchklicken

STRASSE = 'Haasemannstraße 13'
ORT = '30449 Hannover-Linden'


def b(k, sizes, cls='', pos=None, ratio=False):
    """Foto ohne die Auftritte der Seite: jede Fassung bewegt ihre Bilder selbst. Geladen wird erst, wenn die Fassung gezeigt wird.
    ratio=True: Rahmen im Seitenverhältnis des Fotos, nichts wird beschnitten (Köpfe bleiben ganz)."""
    m = META[k]
    _q, p, alt = BILD[k]
    srcset = ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in m['stufen'])
    st = '--lq:url(%s)' % m['lq'] + (';aspect-ratio:%d/%d' % (m['w'], m['h']) if ratio else '')
    return ('<figure class="ul-b%s" style="%s"><img data-ul="%s" sizes="%s" alt="%s" decoding="async" style="object-position:%s"></figure>'
            % ((' ' + cls) if cls else '', st, srcset, sizes, E(alt), pos or p))


def zl(zeilen, cls, tag='p', i0=0):
    """Zeilen aus dem Schlitz."""
    t = ' '.join(re.sub('<[^>]+>', '', z) for z in zeilen)
    inner = ''.join('<span class="ul-z"><span style="--i:%d">%s</span></span>' % (i0 + i, z) for i, z in enumerate(zeilen))
    return '<%s class="ul-zl %s" aria-label="%s">%s</%s>' % (tag, cls, E(t), inner, tag)


F = []   # (Name, Klasse, Inhalt)

# 1 Darüber: keine Lücke mehr; der Einstieg sinkt beim Weiterscrollen langsam ab, die Bildwand schiebt sich randlos über seine Unterkante
F.append(('Darüber', 'ul1', ''))

# 2 Fenster: das Tablett mit den Gläsern steht, die Seite zieht darüber; mittig die Adresse
F.append(('Fenster', 'ul2', '''<div class="ul2-fenster"><div class="ul2-schicht">%s<i class="ul2-hof"></i></div>
%s</div>''' % (b('tablett', '100vw', pos='50% 46%'), zl([E(STRASSE) + ',', 'Hannover-Linden.'], 'ul2-satz'))))

# 3 Tür auf: zwei Türflügel mit dem Namen der Bar gehen beim Scrollen auseinander, dahinter der Blick auf die Tafel
F.append(('Tür auf', 'ul3', '''<div class="ul3-rahmen">%s<div class="ul3-fl ul3-l"><span>Walk on the</span></div><div class="ul3-fl ul3-r"><span>Wild Side</span></div></div>
<p class="ul3-zeile mono">%s · %s</p>''' % (b('kerze3', '(max-width:860px) 100vw, 80vw', pos='50% 52%'), E(STRASSE), E(ORT))))

# 4 Anstossen: draussen und drinnen, zwei Bilder steigen getrennt herauf und kommen an der Naht zusammen (Bewegungsidee des Hauses)
F.append(('Anstoßen', 'ul4', '''<div class="ul4-paar"><div class="ul4-a">%s<p class="mono">Draußen · %s</p></div><div class="ul4-b">%s<p class="mono">Drinnen · Kerzen auf dem Tisch</p></div></div>''' % (
    b('barnacht', '(max-width:860px) 50vw, 46vw', pos='50% 40%'), E(STRASSE), b('loch', '(max-width:860px) 50vw, 46vw', pos='50% 60%'))))

# 5 Farbkante: ein Band in der Abendfarbe als harte Kante, der Name der Bar zieht beim Scrollen gross hindurch
WORT = 'Walk on the Wild Side'
F.append(('Farbkante', 'ul5', '''<div class="ul5-band"><p class="ul5-wort" aria-label="%s"><span class="ul5-lauf" aria-hidden="true">%s</span></p>
<p class="ul5-info mono">%s · %s</p></div>''' % (WORT, ('<span>%s</span><i>·</i>' % WORT) * 4, E(STRASSE), E(ORT))))

# 6 Laufschrift: eine schmale Zeile zwischen zwei Haarlinien, die ruhig durchläuft
LAUF = ['Walk on the Wild Side', STRASSE, 'Hannover-Linden', 'Bar: Donnerstag bis Samstag ab 19 Uhr', 'Culinarium: an einzelnen Wochenenden']
lauf = ''.join('<span>%s</span><i></i>' % E(x) for x in LAUF)
F.append(('Laufschrift', 'ul6', '''<div class="ul6-band" aria-label="%s"><div class="ul6-lauf" aria-hidden="true">%s%s</div></div>''' % (
    E(' · '.join(LAUF)), lauf, lauf)))

# 7 Schräge: die Nacht des Einstiegs kippt schräg in die warme Fläche der Bildwand, an der Kante die Naht in Kerze; die Fläche steigt von unten herein
F.append(('Schräge', 'ul7', '<div class="ul7-feld"><div class="ul7-schub"><i class="ul7-keil"></i>'
          '<svg class="ul7-kante" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><line x1="100" y1="0" x2="0" y2="100"/></svg></div></div>'))

# 8 Treppe: von der Strasse an die Tafel, vier Hochformate steigen von links nach rechts wie Stufen, eins nach dem anderen
TREPPE = [('fassade', '50% 50%'), ('fensterdraussen', '50% 50%'), ('flur', '50% 50%'), ('kerze3', '50% 50%')]
F.append(('Treppe', 'ul8', '''<div class="ul8-feld">%s<div class="ul8-stufen">%s</div></div>''' % (
    zl(['Von der Straße', 'an die Tafel.'], 'ul8-t'),
    ''.join('<div class="ul8-s" style="--i:%d">%s</div>' % (i, b(k, '(max-width:860px) 46vw, 26vw', pos=p, ratio=True)) for i, (k, p) in enumerate(TREPPE)))))

# 9 Öffnen: ein Fenster auf die Bar bei Nacht geht beim Scrollen auf, das Bild darin bleibt stehen
F.append(('Öffnen', 'ul9', '<div class="ul9-rahmen"><div class="ul9-gegen">%s</div></div>' % b('barlicht', '(max-width:860px) 100vw, 82vw', pos='50% 56%')))

# 10 Schild: an der Kante hängt ein Strassenschild in Schiefer, es pendelt aus
F.append(('Schild', 'ul10', '''<div class="ul10-haken"><div class="ul10-schild"><i class="ul10-seil ul10-sl"></i><i class="ul10-seil ul10-sr"></i>
<p class="ul10-str">Haasemann&shy;straße <b>13</b></p><p class="ul10-ort mono">Hannover · Linden</p></div></div>'''))

# 11 Lichter an: drei Bilder liegen im Dunkeln und gehen beim Scrollen nacheinander an
LICHT = [('schaumglas', '50% 50%'), ('loch', '50% 50%'), ('kartglas', '50% 50%')]
F.append(('Lichter an', 'ul11', '<div class="ul11-reihe">%s</div>' % ''.join(
    '<div class="ul11-z">%s</div>' % b(k, '(max-width:860px) 33vw, 30vw', pos=p) for k, p in LICHT)))

# 12 Speisefolge: der Weg durch den Abend in der Schreibweise von Rudis Karten, Wort für Wort aus dem Schlitz
F.append(('Speisefolge', 'ul12', '''<div class="ul12-feld">%s<p class="ul12-unter mono">Walk on the Wild Side · %s · Hannover-Linden</p></div>''' % (
    zl(['DRAUSSEN&#160;<i>/</i>', 'AN&#160;DER&#160;THEKE&#160;<i>/</i>', 'AN&#160;DER&#160;TAFEL'], 'ul12-zeilen'), E(STRASSE))))

# 13 Durchblick: das Loch in der Wand der Bar als Form; dahinter wandert der Blick auf die Tafel beim Scrollen
F.append(('Durchblick', 'ul13', '''<div class="ul13-wand"><div class="ul13-loch"><div class="ul13-tief">%s</div></div>
<p class="ul13-zeile mono">Durch die Wand · an die Tafel</p></div>''' % b('t09', '(max-width:860px) 100vw, 60vw', pos='50% 50%')))

# 14 Klappkarte: eine Karte in Schiefer klappt auf wie ein Buch, links das Fenster der Bar, rechts die Adresse und die Abende
F.append(('Klappkarte', 'ul14', '''<div class="ul14-buch"><div class="ul14-vorn">%s</div>
<div class="ul14-rechts"><div class="ul14-deckel">%s</div><p class="mono ul14-k">Hier findet Culinarium statt</p><p class="ul14-str">%s</p><p class="ul14-ort">%s</p>
<p class="mono ul14-zeit"><span>Freitag ab 19 Uhr</span><span>Samstag ab 17 Uhr</span></p></div></div>''' % (
    b('fensterdraussen', '(max-width:860px) 46vw, 30vw', pos='50% 50%'), marke('wm'), E(STRASSE), E(ORT))))

# 15 Ausrichten: drei Fotos liegen schräg wie hingeworfen und richten sich beim Scrollen zu einer geraden Reihe aus
AUS = [('kartglas', '50% 50%', -7, 40), ('w3', '50% 50%', 4.5, -26), ('g5', '50% 50%', -3.5, 30)]
F.append(('Ausrichten', 'ul15', '<div class="ul15-reihe">%s</div>' % ''.join(
    '<div class="ul15-z" data-dreh="%s" data-y="%s" data-x="%d">%s</div>' % (d, y, i - 1, b(k, '(max-width:860px) 33vw, 26vw', pos=p))
    for i, (k, p, d, y) in enumerate(AUS))))


# ------------------------------------------------------------------ Rahmen
def rahmen():
    teile = [] if WAHL else ['<div class="ul-f ul0" data-nr="0" data-name="Heute" hidden></div>']
    for i, (name, cls, inner) in enumerate(F, 1):
        if WAHL and i != WAHL:   # versandfertig (Robert 28.10.2026): nur die gewählte Fassung, keine versteckten
            continue
        teile.append('<div class="ul-f %s" data-nr="%d" data-name="%s" hidden>%s</div>' % (cls, i, E(name), inner))
    # Fassung sofort beim Lesen zeigen, nicht erst nach dem Laden des Skripts (kein Springen)
    sofort = ('<script>(function(){var s=document.getElementById("ueberleitung"),n=parseInt(new URLSearchParams(location.search).get("u"),10);'
              'if(%d)n=%d;if(!(n>=0&&n<=%d))n=1;var f=s.querySelector(\'.ul-f[data-nr="\'+n+\'"]\');f.hidden=false;s.dataset.an=n;'
              'document.documentElement.dataset.ul=n;f.querySelectorAll("img[data-ul]").forEach(function(i){i.srcset=i.dataset.ul;i.removeAttribute("data-ul")})})()</script>') % (
        WAHL, WAHL, len(F))
    leiste = ('<nav class="ul-leiste" id="ul-leiste" aria-label="Fassungen der Überleitung"' + (' hidden style="display:none"' if WAHL else '') + '>'
              '<button class="ul-pfeil" type="button" data-ul-schritt="-1" aria-label="Vorige Fassung">‹</button>'
              '<div class="ul-daumen">%s</div>'
              '<button class="ul-pfeil" type="button" data-ul-schritt="1" aria-label="Nächste Fassung">›</button>'
              '<p class="ul-name" aria-live="polite"></p></nav>') % ''.join(
        '<button type="button" data-ul-nr="%d" aria-label="Fassung %d: %s"><img src="assets/ueberleitung/u%d.jpg?v=%s" alt="" loading="lazy" width="64" height="36"><b>%d</b></button>'
        % (i, i, E(n), i, VERSION, i) for i, n in enumerate(['Heute'] + [x[0] for x in F]))
    if WAHL:
        leiste = ''
    return ('%s<section class="ul" id="ueberleitung" data-ton="nacht" aria-label="Weg in die Bar"' + (' data-fest="1"' if WAHL else '') + '>%s</section>%s%s%s') % (
        ANF, ''.join(teile), sofort, leiste, END)


def main():
    pfad = os.path.join(HIER, 'index.html')
    h = open(pfad, encoding='utf-8').read()
    if ANF in h:   # schon eingebaut: alten Rahmen entfernen
        h = h[:h.index(ANF)] + h[h.index(END) + len(END):]
    m = re.search(r'<section class="vab v-ebenen[^"]*"[^>]*id="ebenen"', h)
    assert m, '#ebenen in index.html nicht gefunden (erst bau.py / varianten.py laufen lassen)'
    assert h.rfind('</section>', 0, m.start()) > h.find('id="auftakt"') > 0, 'Auftakt steht nicht direkt vor #ebenen'
    h = h[:m.start()] + rahmen() + h[m.start():]
    h = re.sub(r'\n?<link rel="stylesheet" href="assets/ueberleitung\.css[^>]*>', '', h)
    h = re.sub(r'\n?<script src="assets/ueberleitung\.js[^>]*></script>', '', h)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/ueberleitung.css?v=%s">\n</head>' % VERSION, 1)
    h = h.replace('</body>', '<script src="assets/ueberleitung.js?v=%s" defer></script>\n</body>' % VERSION, 1)
    open(pfad, 'w', encoding='utf-8').write(h)
    print('index.html: Überleitung mit %d Fassungen%s' % (len(F), ', fest Nr. %d' % WAHL if WAHL else ''))


def daumen():
    """Vorschaubilder der Leiste: jede Fassung bei 1440 × 900 in WebKit, die Seite an der Überleitung, als 160 × 90."""
    ziel = os.path.join(HIER, 'assets', 'ueberleitung')
    os.makedirs(ziel, exist_ok=True)
    js = r'''
const path=require('path'),os=require('os');module.paths.push(path.join(os.homedir(),'Aussen-Pruefung','node_modules'));
const pw=require('playwright');
(async()=>{const [url,ziel,n]=process.argv.slice(2);const br=await pw.webkit.launch({headless:true});
const pg=await (await br.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1})).newPage();
for(let i=0;i<=+n;i++){await pg.goto(url+'?u='+i,{waitUntil:'load'});await pg.addStyleTag({content:'.ul-leiste{display:none!important}'});
await pg.evaluate(()=>window.ulHin&&window.ulHin());await pg.waitForTimeout(500);
await pg.evaluate(()=>{window.scrollBy(0,innerHeight*.18)});await pg.waitForTimeout(2600);
await pg.screenshot({path:path.join(ziel,'u'+i+'.png'),clip:{x:0,y:45,width:1440,height:810}});}
await br.close();})().catch(e=>{console.error(e);process.exit(1)});'''
    skript = os.path.join(ziel, '_aufnahme.js')
    open(skript, 'w').write(js)
    url = 'http://127.0.0.1:8978/haus/Culinarium%20Hannover/website/index.html'
    try:
        subprocess.run(['node', skript, url, ziel, str(len(F))], check=True)
    finally:
        os.remove(skript)
    from PIL import Image
    for i in range(len(F) + 1):
        p = os.path.join(ziel, 'u%d.png' % i)
        im = Image.open(p).convert('RGB').resize((160, 90), Image.LANCZOS)
        im.save(os.path.join(ziel, 'u%d.jpg' % i), 'JPEG', quality=82)
        os.remove(p)
    print('Vorschaubilder', len(F) + 1)


if __name__ == '__main__':
    if 'daumen' in sys.argv:
        daumen()
    else:
        main()
