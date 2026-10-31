"""Instagram-Feed von Culinarium als Idee. Das Haus hat ein Profil: @culinarium_hannover, 1.079 Follower, 305 gefolgt, 28 Beiträge
(abgelesen ohne Anmeldung, _qa/spaeher/ig-profil-handy.txt, Stand 25.10.2026); dort vor allem die Plakate der Abende.
Fotos: nur die eigenen (Fotos des Hauses aus dem Bildregister der Website website/assets/bild, damit die geschärften Fassungen von selbst
nachkommen, und Rudis Plakate), keine Gästefotos, keine Fotos Dritter, keine erzeugten Bilder. Texte zu den Beiträgen: Tasty Studios.

Fassung 2 «Ein Abend in Folgen» (Oberchef 29.10.2026, Robert: «diese gerade Reihe in der Mitte … mit den Plakaten … total monoton und billig …
mach so … 36 Beiträge … als hätte den so ein richtig professionelles Studio gemacht»). Ersetzt Fassung 1 «Momo x Rudi» (Plakat-Säule in der Mitte,
Sicherung feed_daten.py.vor-feed-2026-10-29).
Wie ein Studio plant: keine feste Spalte, jede Reihe anders gemischt. Von oben nach unten erzählt der Feed in Folgen: Ankündigung, Abend,
Teller, Drink, Menschen, Rückblick, dann wieder von vorn. Dazwischen Rudis Zeilen als reine Schrift (Fraunces 360 auf Nacht oder Warmweiss),
zwei Stimmen aus dem Haus, Karussell-Deckblätter und Reel-Titel. Neun Plakate (Fassung 2b mit 60 Beiträgen; die ersten 36 unverändert), ganz und nie angeschnitten, verteilt, nie zwei
neben- oder untereinander. Jedes Foto einmal. Hell und dunkel, warm und kühl, nah und weit wechseln; das «C» aus Rudis Wortmarke ist das
einzige Zeichen. Echte Gästestimmen mit Wortlaut gibt es in den Quellen nicht; die Zitate sind Momo und Rudi (Website, Team-Seite und Beiträge)."""
import glob, os, re
import feed_bogen

_HIER = os.path.dirname(os.path.abspath(__file__))
_WEB = os.path.dirname(os.path.dirname(_HIER))


def quelle(key):
    """Größte Fassung des Fotos im Bildregister der Website (website/assets/bild/<key>-<breite>.webp)."""
    b = sorted(int(m.group(1)) for p in glob.glob(os.path.join(_WEB, 'assets', 'bild', key + '-*.webp')) if (m := re.search(r'-(\d+)\.webp$', p)))
    if not b:
        raise FileNotFoundError(key)
    return os.path.join(_WEB, 'assets', 'bild', f'{key}-{b[-1]}.webp')


PROFIL = {'name': 'culinarium_hannover', 'titel': 'Culinarium', 'art': 'Food Pairing',
          'bio': ['CULINARIUM · a unique experience', 'Ein Menü, fünf passende Drinks, eine lange Tafel. Im Walk on the Wild Side, Linden.'],
          'link': 'culinarium-hannover.de',
          'zahlen': {'beitraege': '28', 'follower': '1.079', 'gefolgt': '305'}, 'stand': '25.10.2026'}
HIGHLIGHTS = [('Abende', quelle('p_DbYnkdkjrNy'), .5), ('Teller', quelle('r01'), .5), ('Drinks', quelle('g2'), .5),
              ('Tafel', quelle('t07'), .5), ('Linden', quelle('ecke'), .5)]
TON = (.98, 1.03, 1.0, 1.0)
REGEL = 'bogen'
SEITE = dict(
    titel=['Wie es', 'weitergeht.'],
    text1='Euer Feed bleibt, wie er ist. Darauf bauen die nächsten 60 Beiträge auf, so wie ihr sie nach und nach postet: der Abend im November mit Ankündigung, «Noch drei Plätze» und Danke, der Abend im Dezember, Dirty Chicken und die Abende 2027. Dazwischen Rudis Teller, Momos Gläser, die Leute und die Bar.',
    text2='Kein Foto, das schon auf eurem Profil steht, kommt nochmal vor; nur eure Plakate zeigen wir gezielt wieder, «Aus dem Archiv». Mit dem Schalter seht ihr euren Feed heute und mit den nächsten 60; die Nummern zeigen die Reihenfolge zum Posten.',
    aufbau='Die nächsten 60 Beiträge über eurem heutigen Feed, nummeriert in der Reihenfolge des Postens',
    texte='Ideen von mir, Zeilen und Stimmen vom Haus',
    bilder='eure eigenen Fotos, die noch nie gepostet wurden, und eure Plakate')

_C = '<i class="c"></i>'   # das «C» aus Rudis Wortmarke (eigen/zeichen-c.svg als Maske), einziges Zeichen
BOGEN_CSS = (
    "@font-face{font-family:'F';src:url('../assets/schrift/fraunces-soft.woff2') format('woff2');font-weight:100 900}"
    "@font-face{font-family:'M';src:url('../assets/schrift/dmmono.woff2') format('woff2')}"
    "@font-face{font-family:'S';src:url('../assets/schrift/instrument.woff2') format('woff2');font-weight:400 600}"
    '.st{--nacht:#16151A;--weiss:#FAF4F4;--kerze:#EF7649;--hell:#F5A689;--schiefer:#3A3845}'
    '.n,.w{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:150px 120px}'
    '.n{background:var(--nacht) url(../assets/zeichen/tapete-dunkel.svg) 0 0/224px 224px;color:var(--weiss)}'
    '.w{background:var(--weiss) url(../assets/zeichen/tapete-hell.svg) 0 0/224px 224px;color:var(--nacht)}'
    '.c{display:block;width:74px;height:78px;background:var(--kerze);-webkit-mask:url(../_werkbank/eigen/zeichen-c.svg) center/contain no-repeat;mask:url(../_werkbank/eigen/zeichen-c.svg) center/contain no-repeat}'
    '.w .c{background:var(--schiefer)}'
    '.kop{position:absolute;top:118px;left:0;right:0;display:flex;justify-content:center}'
    '.fu{position:absolute;bottom:112px;left:0;right:0;font:400 25px/1 M;letter-spacing:.08em;text-transform:uppercase;color:var(--hell)}'
    '.w .fu{color:#8a5a45}'
    '.zl{font:360 112px/1.04 F;font-variation-settings:"SOFT" 100,"opsz" 144;text-transform:uppercase;text-wrap:balance;letter-spacing:-.005em}'
    '.zl span{display:block;white-space:nowrap}.zl b{font-weight:360;color:var(--kerze)}'
    '.ti{font:360 128px/1.02 F;font-variation-settings:"SOFT" 100,"opsz" 144;text-wrap:balance;letter-spacing:-.01em}'
    '.zi{font:360 98px/1.1 F;font-variation-settings:"SOFT" 100,"opsz" 144;text-wrap:balance}'
    '.zi::before{content:"«";color:var(--kerze)}.zi::after{content:"»";color:var(--kerze)}'
    '.da{margin-top:60px;font:400 33px/1.7 M;letter-spacing:.08em;color:var(--hell)}'
    '.sa{margin-top:52px;max-width:760px;font:400 38px/1.42 S;text-wrap:balance;opacity:.86}'
    '.ki2{font:400 26px/1 M;letter-spacing:.1em;text-transform:uppercase;color:var(--hell);margin-bottom:40px}'
    '.v{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:150px 110px;background:#8953A9 url(../assets/zeichen/tapete-dc.svg) 0 0/224px 224px;color:#FAF4F4}'
    '.v .ki2,.v .fu{color:#FAF4F4}'
    '.li{width:110px;height:2px;background:var(--kerze);margin:56px auto 0}'
    # Plakate ganz, nichts beschnitten, auf der Nacht oder dem Warmweiss der Website
    '.pl{position:absolute;inset:0;display:grid;place-items:center}'
    '.pl.n,.pl.w{display:grid;padding:0}'
    '.pl img{display:block;width:82%;height:auto;box-shadow:0 30px 44px -18px rgba(0,0,0,.6),0 0 0 1px rgba(22,21,26,.08)}'
    # Karussell-Deckblatt und Reel-Titel: Foto randlos, Titel im unteren Drittel auf einem Verlauf
    '.fo{position:absolute;inset:0}.fo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
    '.fo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,14,19,0) 38%,rgba(15,14,19,.86) 100%)}'
    '.fo .tx{position:absolute;left:96px;right:96px;bottom:118px;z-index:2;color:var(--weiss);text-align:left}'
    '.fo .ki{font:400 25px/1 M;letter-spacing:.1em;text-transform:uppercase;color:var(--hell);margin-bottom:26px}'
    '.fo .ti{font-size:104px;line-height:1.02}'
    '.fo .wi{position:absolute;top:96px;right:96px;z-index:2;font:400 25px/1 M;letter-spacing:.1em;color:var(--weiss);padding:14px 20px;border:1.5px solid rgba(250,244,244,.6);border-radius:999px}'
)



def zeile(teile, ton='n', fuss='Rudi · vom Pass'):
    """Rudis Zeile als reine Schrift, Schrägstriche in Kerze."""
    z = ''.join(f'<span>{t}{" <b>/</b>" if i < len(teile) - 1 else ""}</span>' for i, t in enumerate(teile))
    gr = min(116, int(820 / (.68 * (max(len(t) for t in teile) + 2))))   # längstes Wort samt « /» passt in eine Zeile
    return f'<div class="{ton}"><div class="kop">{_C}</div><p class="zl" style="font-size:{gr}px">{z}</p><p class="fu">{fuss}</p></div>'


def plakat(pid, ton='n'):
    return '<div class="pl ' + ton + '"><img src="{bild:' + quelle('p_' + pid) + '}" alt=""></div>'


def deckblatt(key, kicker, titel, wink):
    return '<div class="fo"><img src="{bild:' + quelle(key) + '}" alt=""><span class="wi">' + wink + '</span><div class="tx"><p class="ki">' + kicker + '</p><p class="ti">' + titel + '</p></div></div>'


def tafel(titel, satz='', fuss='', ton='n', da='', kicker=''):
    """Schrift-Beitrag auf Nacht (n), Warmweiss (w) oder im Violett von Dirty Chicken (v, ohne das «C»)."""
    kop = '' if ton == 'v' else f'<div class="kop">{_C}</div>'
    return (f'<div class="{ton}">{kop}' + (f'<p class="ki2">{kicker}</p>' if kicker else '') + f'<p class="ti">{titel}</p>'
            + (f'<p class="da">{da}</p>' if da else '') + (f'<p class="sa">{satz}</p>' if satz else '') + (f'<p class="fu">{fuss}</p>' if fuss else '') + '</div>')


def zitat(satz, wer, ton='w'):
    return f'<div class="{ton}"><div class="kop">{_C}</div><p class="zi">{satz}</p><p class="fu">{wer}</p></div>'


F = lambda key, art, fx=.5, fy=.5: dict(art='foto', bild=quelle(key), fx=fx, fy=fy, _art=art)
H = lambda html, art: dict(art='html', html=html, _art=art)

# Fassung 3 «Fortsetzung» (Oberchef 29.10.2026, Robert: «die werden jetzt nicht ihren gesamten Feed löschen … man muss gucken, was sie an
# Bildern benutzt haben, damit wir jetzt diese 60 Beiträge darauf aufbauen können … zwischendurch noch so die nächsten Veranstaltungen»).
# Die 60 Beiträge sind die nächsten, die das Haus nach und nach postet, hier in der Reihenfolge des Postens (1 = zuerst). Kein Foto, das schon
# auf @culinarium_hannover steht (Abgleich feed_bestand.py im Kit, Bericht feed/bestand.json); Ausnahme: Rudis Plakate, gezielt als
# «Aus dem Archiv» wieder gepostet. Ein Jahr in Folgen: Abend im November (27./28.11.) und im Dezember (18./19.12., Beispieltermine der
# Website), Dirty Chicken, dann die Abende 2027, deren Termine noch nicht feststehen ([Datum]). Je Abend: Ankündigung, Countdown,
# «Noch drei Plätze» (Exklusivität, nie Druck), der Abend, Danke, Rückblick. Darunter stehen im Profil die echten bisherigen Beiträge.
# Arten für den Nachbar-Abgleich: text, plakat, cover, teller, drink, mensch, tafel, bar, dc.
JAHR = [
    # ---- November 2026: der Abend am 27. und 28. November
    (H(tafel('Der nächste Abend.', da='27 / 11 / 26 · 19:00 UHR<br>28 / 11 / 26 · 17:00 UHR', fuss='Vierzehn Plätze · eine lange Tafel'), 'text'),
     'Der nächste Abend an der langen Tafel: Freitag, 27. November, ab 19 Uhr und Samstag, 28. November, ab 17 Uhr. Vierzehn Plätze. Schreib uns, wenn einer davon deiner sein soll.'),
    (F('kerze2', 'tafel', .5, .45), 'So sieht es aus, kurz bevor der erste Gang kommt. Kerzen an, Gläser bereit, jeder Platz gedeckt.'),
    (H(zeile(['Lauch', 'Blumenkohl', 'Chipotle'], 'w'), 'text'), 'So schreibt Rudi seine Teller: drei, vier Wörter, und jedes davon zählt.'),
    (F('g1', 'drink'), 'Schaum, Garnitur, und Momo erklärt dir am Tisch, was im Glas passiert.'),
    (H(plakat('CzMcqNcMCqG'), 'plakat'), 'Aus dem Archiv: das Plakat zum November 2023, aus den ersten Abenden unter dem Namen Culinarium. Drei Jahre später steht wieder ein November an.'),
    (F('m2', 'teller'), 'Mit dem Brenner über jeden Teller, einzeln. Am Pass hat nichts Eile.'),
    (H(deckblatt('kerze3', '27 / 11 / 26', 'Noch eine Woche.', 'Freitag'), 'cover'), 'Noch eine Woche bis zum Abend im November. Die Kerzen sind bestellt, die Karte wird geschrieben.'),
    (H(zitat('Du sagst mir, was du magst, ich mache dir einen Drink.', 'Momo · hinter der Bar'), 'text'), 'Eine Karte gibt es an Momos Theke nicht. Du erzählst, er mixt.'),
    (F('momo', 'mensch', .5, .35), 'Momo, hinter der Bar des Walk on the Wild Side. Jeder Drink des Abends geht durch seine Hände.'),
    (H(tafel('Noch drei Plätze.', satz='Für Samstag, 28. November, ab 17 Uhr.', fuss='Eine lange Tafel · vierzehn Gäste', ton='w'), 'text'),
     'Für Samstag, 28. November, sind noch drei Plätze an der Tafel frei. Wenn einer davon deiner sein soll, schreib uns eine Nachricht.'),
    (F('anstossen', 'tafel', .5, .4), 'Heute Abend. Der erste Schluck, und ab hier gehört die Tafel euch.'),
    (F('roq1', 'teller', .5, .55), 'BLUMENKOHL / ROQUEFORT / KAPERN / QUINOA. Daneben das Glas, das Momo dazu gemixt hat.'),
    (H(deckblatt('t03', 'Rückblick · November', 'Danke für zwei Abende.', '1 / 8'), 'cover'), 'Danke für Freitag und Samstag. Wisch dich durch die Abende, vom ersten Glas bis zum letzten Teller.'),
    # ---- Dezember 2026: der letzte Abend des Jahres, 18. und 19. Dezember
    (H(tafel('Noch ein Abend in diesem Jahr.', da='18 / 12 / 26 · 19:00 UHR<br>19 / 12 / 26 · 17:00 UHR', fuss='Vierzehn Plätze · eine lange Tafel', ton='w'), 'text'),
     'Noch ein Abend in diesem Jahr: Freitag, 18. Dezember, ab 19 Uhr und Samstag, 19. Dezember, ab 17 Uhr.'),
    (H(deckblatt('klaeren', 'Tasting und Schulung', 'Was im Glas passiert', '1 / 5'), 'cover'),
     'Fatwashing, Milkwashing, Klärung mit Enzymen: Wisch dich durch, Momo erklärt dir alle drei. Am Abend selbst zeigt er es dir am Tisch.'),
    (F('tarte', 'teller', .5, .55), 'Tarte mit roten Früchten und Eis. Zum Schluss etwas Leichtes.'),
    (F('schildnacht', 'bar', .5, .45), 'Haasemannstraße 13, Ecke Rampenstraße. Am Schild erkennst du die Bar schon von weitem.'),
    (H(zeile(['Aubergine', 'Kokos', 'Limette', 'Sesam'], 'n'), 'text'), 'Rudis neuester Teller, so wie er ihn schreibt.'),
    (F('glasnacht', 'drink'), 'Im Stielglas, auf dem dunklen Tisch. Ruhig, klar, für den zweiten Gang.'),
    (H(tafel('Samstag ausgebucht.', satz='Wird ein Platz frei, erfährt es zuerst, wer auf der Warteliste steht.', fuss='19 / 12 / 26'), 'text'),
     'Der Samstag ist ausgebucht. Wird ein Platz frei, erfährst du es als Erstes: Schreib uns eine Nachricht, dann stehst du auf der Warteliste. Für Freitag gibt es noch Plätze.'),
    (H(deckblatt('pass4', 'Am Pass', 'Jeder Teller von Hand angerichtet', 'Film'), 'cover'), 'Ein paar Minuten am Pass, bevor die Teller an die Tafel gehen. Ton an.'),
    (F('rudi', 'mensch', .5, .4), 'Rudi erklärt dir seinen Teller selbst, am Tisch, bevor du den ersten Bissen nimmst.'),
    (H(plakat('C17kqAXLfs_', 'w'), 'plakat'), 'Aus dem Archiv: das Plakat zum Januar 2024, Motto «Flashback».'),
    (F('t10', 'tafel', .5, .4), 'Ein Abend an der langen Tafel. Fremde zu Beginn, Tischnachbarn zum Dessert.'),
    (H(tafel('Danke für 2026.', satz='Für jeden Platz an der Tafel, für die Gespräche und für die Ruhe zwischen den Gängen.', fuss='Momo · Rudi', ton='w'), 'text'),
     'Danke für 2026. Wenn du dabei warst, weißt du, was wir meinen. Wir sehen uns im neuen Jahr an der Tafel.'),
    # ---- Winter: Teller, Glas, Leute
    (F('beete', 'teller', .5, .55), 'Rote Bete mit Schaum. Gemüse steht bei Rudi oft im Mittelpunkt.'),
    (F('d2', 'drink'), 'Hell, mit Minze. Für einen Gast, der es frisch mag.'),
    (H(plakat('DJw8OqGMY1G'), 'plakat'), 'Aus dem Archiv: das Plakat zum Juni 2025, die Gärtnerin.'),
    (H(zitat('Was für ein Abend!', 'Culinarium · Rückblick'), 'text'), 'Aus einem Rückblick des Hauses: Was für ein Abend! Mit unglaublichen Gästen und einer einzigartigen Atmosphäre im Walk on the Wild Side.'),   # belegt: Recap-Beitrag von @culinarium_hannover (_quelle/extern/ig); ersetzt das Dirty-Chicken-Zitat (Tor 30.10.2026, K20)
    (F('anrichten', 'teller'), 'Konzentration am Pass. Jeder Teller wird angerichtet, als wäre er der einzige.'),
    # ---- Frühjahr: Dirty Chicken
    (H(tafel('Dirty Chicken.', da='WALK ON THE WILD SIDE', kicker='Pop-up', fuss='Fried Chicken · Dirty Drinks · Musik', ton='v'), 'dc'),
     'Aus demselben Haus: Dirty Chicken kommt wieder in den Walk on the Wild Side, die Termine stehen auf @dirtychicken.hannover. Fried Chicken, das kracht, Pommes, Krautsalat und Dirty Drinks von der Bar.'),
    (F('trio2', 'mensch', .5, .4), 'Die Leute hinter Culinarium, vor der Bar. Dahinter stehen immer dieselben.'),
    (F('dn_tisch', 'dc'), 'Dirty Chicken von oben: Sandwich, Chunks, Pommes, Krautsalat. Alles zum Teilen.'),
    # ---- Frühjahr 2027: der nächste Culinarium-Abend, Termin noch offen
    (H(tafel('Der nächste Abend.', da='FREITAG · 19:00 UHR<br>SAMSTAG · 17:00 UHR', fuss='Vierzehn Plätze · eine lange Tafel'), 'text'),
     'Der erste Abend 2027 an der langen Tafel: Freitag ab 19 Uhr und Samstag ab 17 Uhr. Vierzehn Plätze, wer auf der Warteliste steht, erfährt es zuerst.'),
    (F('spag', 'teller', .5, .55), 'SPAGHETTI-EIS / KIWI / WEISSE SCHOKOLADE. Ein Dessert, das dich anlächelt.'),
    (H(plakat('DFqbLG2s_dc', 'w'), 'plakat'), 'Aus dem Archiv: das Plakat zum Februar 2025, der Panther auf dem Thron.'),
    (H(deckblatt('kerze1', 'Freitag · 19:00 Uhr', 'Noch drei Tage.', 'Freitag'), 'cover'), 'Noch drei Tage. Momo stellt die Gläser bereit, Rudi schreibt die Zeilen für die Karte.'),
    (F('service', 'mensch', .5, .4), 'Der Teller kommt an deinen Platz, und mit ihm der Satz, was darauf liegt.'),
    (H(zeile(['Hokkaido', 'Kürbiskernöl', 'Haselnuss'], 'n'), 'text'), 'Ein Gang im Glas, und daneben der passende Drink von Momo.'),
    (F('r09', 'teller'), 'Ein Teller auf Porzellan mit grünem Rand. Rudis Sinn für den Rahmen.'),
    (H(deckblatt('d3', 'Signature Drinks', 'Durchs Sieb, ins Glas', 'Film'), 'cover'), 'Wie ein Drink von Momo entsteht, in einer Minute.'),
    (F('ecke', 'bar'), 'Die Hausecke in Linden, Haasemannstraße 13. Hier hat alles angefangen.'),
    (H(plakat('C8cgYVSouVT'), 'plakat'), 'Aus dem Archiv: das Plakat zum Juli 2024, dem ersten Abend mit «by Momo x Rudi».'),
    # ---- Sommer 2027
    (H(tafel('Ein Abend im Sommer.', da='FREITAG · 19:00 UHR<br>SAMSTAG · 17:00 UHR', fuss='Vierzehn Plätze · eine lange Tafel', ton='w'), 'text'),
     'Ein Abend im Sommer an der langen Tafel: Freitag ab 19 Uhr und Samstag ab 17 Uhr. Wer auf der Warteliste steht, erfährt es zuerst.'),
    (H(deckblatt('glaeser', 'Signature Drinks', 'Fünf Drinks, ein Abend', '1 / 6'), 'cover'),
     'Fünf Drinks, ein Abend: Wisch dich durch, vom Apéritif bis zum Absacker. Jeder passt zu genau einem Gang.'),
    (F('r01', 'teller'), 'Blumenkohl mit Kürbis, auf weissem Porzellan. Jeder Teller sieht aus, als hätte er nur auf dich gewartet.'),
    (F('momo_hoch', 'mensch', .5, .3), 'Momo vor seiner Bar. Hier entsteht jeder der fünf Drinks.'),
    (H(tafel('Black Pearl', satz='Black Sesam fatwashed Tequila, Guave, Grapefruit, Limette.', fuss='Momo · Signature Drink', kicker='Momos Drink zum Dessert'), 'text'),
     'Black Pearl, zum Dessert: Tequila, mit schwarzem Sesam fatgewaschen. Wie das geht, erklärt dir Momo am Tisch.'),
    (H(plakat('DPwlqcfiKcA', 'w'), 'plakat'), 'Aus dem Archiv: das Plakat zum November 2025. Der Freitag war ausverkauft, bevor die Kerzen brannten.'),
    (H(tafel('Ausgebucht.', satz='Danke an alle, die dabei sind. Für den nächsten Abend gilt wieder: Die Warteliste erfährt es zuerst.', fuss='Freitag und Samstag', ton='w'), 'text'),
     'Beide Abende im Sommer sind ausgebucht. Danke. Wer nicht dabei ist: Die Warteliste erfährt den nächsten Termin zuerst.'),
    (F('hok2', 'teller', .5, .55), 'Das Dessert neben seinem Drink. So ist der Abend gedacht: immer beides.'),
    (F('r08', 'teller'), 'Zwei Knödel mit Kräutern. Einfach klingt anders, wenn Rudi es anrichtet.'),
    (H(tafel('Dit ist wahre Liebe!', kicker='Dirty Chicken', fuss='Pop-up aus dem Walk on the Wild Side', ton='v'), 'dc'),
     'Dirty Chicken, Rudis Pop-up mit Fried Chicken, Pommes, Krautsalat und Dirty Drinks. Die nächsten Termine stehen auf @dirtychicken.hannover.'),
    # ---- Herbst 2027: der nächste Abend, Termin noch offen
    (F('team_alle', 'mensch'), 'Das ganze Team hinter der Theke. Keiner von ihnen steht zufällig da.'),
    (H(deckblatt('ws29', 'Signature Drinks', 'Geklärt, Glas für Glas', 'Film'), 'cover'), 'Wie ein Drink klar wird, ohne leiser zu werden. Ton an.'),
    (F('coupe', 'drink'), 'Ein Drink und ein Dessert auf dem Tresen, für den letzten Moment des Abends.'),
    (H(plakat('C56bJeds8PF', 'w'), 'plakat'), 'Aus dem Archiv: das Plakat zum April 2024, der erste Abend, an dem Rudi gekocht hat.'),
    (H(zeile(['Rote Beete', 'Zwiebel', 'Parmesan'], 'w'), 'text'), 'Noch eine von Rudis Zeilen. Gemüse steht bei ihm im Mittelpunkt, und jedes Wort sagt dir, was kommt.'),
    (H(deckblatt('flur', 'Seit 2017 in Linden', 'Wie es kam', '1 / 6'), 'cover'), 'Von der Bar in Linden bis zum ausgebuchten Abend an der langen Tafel: Wisch dich durch die Geschichte.'),
    (H(tafel('Der nächste Abend.', da='FREITAG · 19:00 UHR<br>SAMSTAG · 17:00 UHR', fuss='Vierzehn Plätze · eine lange Tafel'), 'text'),   # ohne Platzhalter (Oberchef 30.10.2026): belegter Wochentag und Uhrzeit statt [DATUM]
     'Der nächste Abend an der langen Tafel: Freitag ab 19 Uhr und Samstag ab 17 Uhr. Vierzehn Plätze. Wer auf der Warteliste steht, erfährt den Termin zuerst.'),
]
assert len(JAHR) == 60, len(JAHR)

# Im Profil steht der zuletzt gepostete Beitrag oben links: die Reihenfolge des Postens umgekehrt, Reihe für Reihe zu drei.
_RASTER = list(reversed(JAHR))
FEED = [_RASTER[i:i + 3] for i in range(0, 60, 3)]


def nachbarn():
    """Gleiche Art nie nebeneinander oder untereinander (Schrift, Plakat, Titel, Teller, Glas, Mensch, Tafel, Bar, Dirty Chicken)."""
    art = [[st['_art'] for st, _ in r] for r in FEED]
    return [(r + 1, c + 1, art[r][c]) for r in range(len(art)) for c in range(3)
            if (c < 2 and art[r][c] == art[r][c + 1]) or (r + 1 < len(art) and art[r][c] == art[r + 1][c])]


BESTAND_AUSNAHMEN = ('p_', 'pl_', 'ill_', 'po_', 'pr_')   # Rudis Plakate dürfen wieder gepostet werden (Robert 29.10.2026); alles andere nie doppelt
BESTAND_KANDIDATEN = []   # wird unten aus dem Bildregister der Website gefüllt: der Bericht nennt jedes schon gepostete Foto

BOGEN = []
for _r, _reihe in enumerate(FEED):
    for _c, (st, text) in enumerate(_reihe):
        st = {k: v for k, v in st.items() if k != '_art'}
        kurz = (os.path.basename(st['bild']).rsplit('-', 1)[0] if st['art'] == 'foto' else re.sub(r'\W+', '', re.sub(r'<[^>]+>', ' ', st['html']))[:14] or 'tafel')
        BOGEN.append(dict(id=f'{_r + 1:02d}{_c + 1}-{kurz}', r=_r, c=_c, texte=[text], **st))
P = feed_bogen.p_liste(BOGEN)
BISHER = 28   # Beiträge auf @culinarium_hannover heute (Profil, 25.10.2026); im Profil der Werkbank stehen sie unter den 60 neuen
PROFIL['zahlen']['beitraege'] = str(len(P) + BISHER)   # Gesamtzahl nach dem Nachposten
BESTAND_KANDIDATEN = sorted({re.sub(r'-\d+\.webp$', '', f) for f in os.listdir(os.path.join(_WEB, 'assets', 'bild')) if f.endswith('.webp')}
                            - {x for x in ('',)})
# Instagram-Bestand des Hauses für den Abgleich: alle Beiträge von @culinarium_hannover und der Beitrag von Rudi mit Culinarium als Mitautor
# (erscheint auch im Profil von Culinarium). Dieselben Beiträge stehen im Profil der Werkbank unter den 60 neuen (feed_leicht.py).
IG_BESTAND = ['../../_quelle/extern/ig/*.jpg', '../../_quelle/extern/ig-team/*_DLSA60BMwiG-*.jpg']
