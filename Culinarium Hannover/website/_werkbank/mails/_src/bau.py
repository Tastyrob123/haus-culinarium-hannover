#!/usr/bin/env python3
"""Culinarium: elf Mail-Vorlagen an Gäste (drei vom 28.10., acht vom Prüfchat Gestaltung 29.10., darunter der Gutschein), als Idee zum Entwurf (Werkbank-Chat 28.10.2026; Bauart aus mails/_src/bau.py des Schäfli, Kleid und Worte eigen).

Drei Fälle, die es im Entwurf wirklich gibt (Seite «Der Abend»: Platz buchen, «das Ticket kommt per Mail», und die Warteliste):
  01 Dein Ticket          gleich nach der Buchung (Abend, Beginn, Plätze, Preis, Ort)
  02 Auf der Warteliste   gleich nach dem Eintrag (Abend, Plätze, Name)
  03 Ein Platz ist frei   wenn für einen vollen Abend ein Platz frei wird (wofür die Warteliste da ist)
Im Du wie die Website. Echter Text oben, Fotos mit Beschreibung und unter 100 KB, lesbar auch mit gesperrten Bildern; Tabellen und feste Stile,
Titel in Georgia (Mailprogramme laden Fraunces nicht). Preis, Zeiten und Adresse aus der Website (website/bau.py, abend.html), Beispielwerte erfunden
und so beschriftet. Culinarium hat keine eigene Mailadresse; geantwortet wird auf die Mail. Wortlaut von Tasty Studios, als Vorschlag. Gebaut, nie verschickt.

Aufruf:  python3 mails/_src/bau.py  → mails/NN-<fall>/index.html, mails/index.html, mails/img/;  danach WB_PORT=9088 node mails/_src/aufnahme.js"""
import html, json, os, re, sys, glob

HIER = os.path.dirname(os.path.abspath(__file__)); MAILS = os.path.dirname(HIER); ROOT = os.path.dirname(MAILS); WEB = os.path.dirname(ROOT)
from PIL import Image  # noqa: E402
_BAU = open(os.path.join(WEB, 'bau.py'), encoding='utf-8').read()
PREIS = re.findall(r"'(\d+,00) EUR'", _BAU)[-1] + ' EUR'   # Preis des letzten Abends (website/bau.py › ABENDE)

e = html.escape
HOLZ, RUSS, TIEF, PAPIER, BLATT, TINTE, KERZE, GOLD, LICHT = '#222028', '#16151a', '#0f0e13', '#f2eaea', '#faf4f4', '#26242d', '#f5a689', '#ef7649', '#b1adac'
SERIF = "Georgia,'Times New Roman',serif"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
ADRESSE = 'Walk on the Wild Side · Haasemannstraße 13 · 30449 Hannover'
GRUSS = 'Momo, Derya und Rudi'
STAND = '30.10.2026'

FAELLE = [
    dict(nr='01', wann='Gleich nach der Buchung', ordner='01-ticket', name='Dein Ticket', satz='Kommt gleich nach der Buchung: Abend, Beginn, Plätze und der Weg zur Bar, das Ticket zum Vorzeigen.',
         betreff='Dein Platz an der Tafel ist gebucht', titel=('Dein Platz', 'an der Tafel.'), foto=('kerze2', 'Gäste und Kerzen an der langen Tafel'),
         text=['Hallo Lena', 'Schön, dass du dabei bist. Dein Platz an der Tafel ist gebucht, das Ticket steht unten in dieser Mail.',
               'Zum Ankommen gibt es einen Aperitif, danach drei Gänge aus der Küche und zu jedem Gang einen Drink, den Momo dir an der Tafel erklärt.',
               'Verträgst du etwas nicht, schreib es uns einfach als Antwort auf diese Mail.'],
         karte=('Dein Ticket', [('Abend', 'Freitag, 27. November 2026'), ('Beginn', '19:00 Uhr'), ('Plätze', '2'), ('Preis', f'{PREIS} je Platz'), ('Nr.', 'C-0412')]),
         knopf=('Den Weg ansehen', 'weg.html'), dazu=ADRESSE + '. Die Bar liegt an der Ecke Haasemannstraße und Rampenstraße.'),
    dict(nr='02', wann='Gleich nach dem Eintrag auf der Warteliste', ordner='02-warteliste', name='Auf der Warteliste', satz='Kommt nach dem Eintrag auf der Warteliste: welcher Abend, wie viele Plätze, und dass wir uns melden, sobald einer frei wird.',
         betreff='Du stehst auf der Warteliste', titel=('Du stehst', 'auf der Liste.'), foto=('glaeser', 'Zwei Gläser stoßen an'),
         text=['Hallo Jonas', 'Danke für deinen Eintrag. Der Abend ist gerade voll, du stehst auf der Warteliste.',
               'Wird ein Platz frei, schreiben wir dir sofort. Und sobald der nächste Abend feststeht, erfährst du es vor allen anderen.'],
         karte=('Dein Eintrag', [('Abend', 'Freitag oder Samstag, egal'), ('Plätze', '2'), ('Name', 'Jonas Becker')]),
         knopf=('Alle Abende ansehen', 'abende.html'), dazu='Willst du deinen Eintrag ändern, antworte einfach auf diese Mail.'),
    dict(nr='03', wann='Wenn für einen vollen Abend ein Platz frei wird', ordner='03-frei', name='Ein Platz ist frei', satz='Kommt, wenn für einen vollen Abend ein Platz frei wird: an die Gäste auf der Warteliste, mit dem Weg zum Buchen.',
         betreff='Ein Platz an der Tafel ist frei geworden', titel=('Ein Platz', 'ist frei geworden.'), foto=('service', 'Ein Teller wird an die Tafel gebracht'),
         text=['Hallo Jonas', 'Gute Nachricht: Für den Abend, auf dessen Warteliste du stehst, ist ein Platz frei geworden.',
               'Wir halten ihn bis morgen Abend für dich frei; danach fragen wir den Nächsten auf der Liste.'],
         karte=('Der Abend', [('Abend', 'Samstag, 28. November 2026'), ('Beginn', '17:00 Uhr'), ('Frei', '1 Platz'), ('Preis', f'{PREIS} je Platz')]),
         knopf=('Jetzt buchen', 'abend.html#termine-buchen'), dazu='Passt es dir doch nicht, musst du nichts tun; du bleibst auf der Liste.'),
    dict(nr='04', wann='Am Tag vor dem Abend', ordner='04-erinnerung', name='Morgen an der Tafel', satz='Kommt am Tag vor dem Abend: wann es losgeht, wie man hinfindet, und dass man Unverträgliches noch sagen kann.',
         betreff='Morgen Abend sitzt du an der Tafel', titel=('Morgen Abend', 'ist dein Platz gedeckt.'), foto=('kerze3', 'Kerzen auf der gedeckten Tafel'),
         text=['Hallo Lena', 'Morgen ist es so weit. Die Tafel wird gedeckt, Rudi bereitet die Gänge vor, und Momo stellt die Drinks zusammen.',
               'Komm gern ein paar Minuten früher, der Aperitif wartet. Verträgst du etwas nicht, sag es uns bis morgen Mittag als Antwort auf diese Mail.'],
         karte=('Morgen', [('Abend', 'Freitag, 27. November 2026'), ('Beginn', '19:00 Uhr'), ('Plätze', '2'), ('Nr.', 'C-0412')]),
         knopf=('Den Weg ansehen', 'weg.html'), dazu=ADRESSE + '.'),
    dict(nr='05', wann='Am Morgen nach dem Abend', ordner='05-danke', name='Danke für den Abend', satz='Kommt am Morgen danach: ein Dank, die Karte des Abends zum Nachlesen und der Weg auf die Liste für den nächsten.',
         betreff='Danke, dass du an der Tafel warst', titel=('Danke', 'für den Abend.'), foto=('toast', 'Gläser heben sich über der Tafel'),
         text=['Hallo Lena', 'Schön, dass du gestern an der Tafel gesessen hast. Wir hoffen, jeder Teller und jeder Drink ist dir in Erinnerung geblieben.',
               'Die Karte des Abends steht unten, falls du einen Drink nachschlagen willst. Und sobald der nächste Abend feststeht, bist du die Erste, die es erfährt.'],
         karte=('Die Karte von gestern', [('Apéritif', 'Sauerteig | Tomate | Butter'), ('Vorspeise', 'Miso | Sellerie | Röstzwiebeln'), ('Hauptgang', 'Spinat | braune Butter | Parmesan'), ('Dessert', 'Kaffee | Molke | Amaretto')]),
         knopf=('Alle Abende ansehen', 'abende.html'), dazu='Willst du uns etwas sagen, antworte einfach auf diese Mail. Momo und Rudi lesen mit.'),
    dict(nr='06', wann='Wenn der nächste Termin feststeht', ordner='06-termin', name='Der nächste Abend steht', satz='Kommt an die Gäste der Liste, sobald der nächste Abend feststeht: Datum, Beginn, Preis und der Weg zum Buchen, vor allen anderen.',
         betreff='Der nächste Abend steht fest', titel=('Der nächste Abend', 'steht fest.'), foto=('anstossen', 'Gäste stossen an der Tafel an'),
         text=['Hallo Jonas', 'Du stehst auf unserer Liste, darum erfährst du es zuerst: Der nächste Abend an der langen Tafel steht fest.',
               'Rudi hat die Gänge geschrieben, Momo arbeitet an den Drinks. Die Plätze sind ab heute für dich buchbar, ab übermorgen für alle.'],
         karte=('Der Abend', [('Freitag', '18. Dezember 2026, 19:00 Uhr'), ('Samstag', '19. Dezember 2026, 17:00 Uhr'), ('Preis', f'{PREIS} je Platz')]),
         knopf=('Platz buchen', 'abend.html#termine-buchen'), dazu='Termine und Preis sind im Entwurf Beispielwerte.'),
    dict(nr='07', wann='Eine Woche nach dem Abend', ordner='07-rueckblick', name='Rückblick mit Fotos', satz='Kommt eine Woche nach dem Abend: ein paar Fotos von der Tafel und der Weg zu allen Bildern auf Instagram.',
         betreff='So war der Abend an der Tafel', titel=('So war', 'der Abend.'), foto=('lachen', 'Gäste lachen an der Tafel'),
         text=['Hallo Lena', 'Eine Woche ist der Abend her, und wir denken noch gern daran: an die Gänge, die Drinks und an eure Gespräche an der langen Tafel.',
               'Ein paar Fotos stehen jetzt auf Instagram. Vielleicht findest du dich darauf wieder.'],
         karte=('Der Abend', [('Datum', 'Freitag, 27. November 2026'), ('Gänge', 'drei, dazu Apéritif und Absacker'), ('Drinks', 'fünf von Momo')]),
         knopf=('Fotos ansehen', 'index.html'), dazu='Gefällt dir ein Foto besonders, schreib es uns. Wir schicken es dir gern in voller Grösse.'),
    dict(nr='08', wann='Als Antwort auf eine Anfrage für eine Feier', ordner='08-feier', name='Eure Feier an der Tafel', satz='Antwort auf eine Anfrage für einen Geburtstag oder eine Feier: was möglich ist, wie viele Plätze, und wie es weitergeht.',
         betreff='Eure Feier an der langen Tafel', titel=('Eure Feier', 'an der langen Tafel.'), foto=('tafelleer', 'Die gedeckte lange Tafel'),
         text=['Hallo Mara', 'Danke für deine Anfrage. Ein Geburtstag an der langen Tafel: Das machen wir gern.',
               'Rudi schreibt euch ein eigenes Menü, Momo stellt die Drinks dazu, und die Tafel gehört an dem Abend nur euch. Sag uns, wie viele ihr seid und was euch wichtig ist, dann melden wir uns mit einem Vorschlag.'],
         karte=('Deine Anfrage', [('Anlass', 'Geburtstag'), ('Wunschtermin', 'Samstag, 16. Januar 2027'), ('Gäste', 'etwa zwölf')]),
         knopf=('Die Tafel ansehen', 'abend.html'), dazu='Name, Termin und Anzahl sind Beispielwerte.'),
    dict(nr='09', wann='Vor einem Pop-up von Dirty Chicken', ordner='09-dirty-chicken', name='Dirty Chicken ist zurück', satz='Kommt vor einem Pop-up von Dirty Chicken: wann, wo, und dass es ohne Anmeldung geht.',
         betreff='Dirty Chicken ist wieder da', titel=('Dirty Chicken', 'ist wieder da.'), foto=('dc_burger', 'Das Chicken Sandwich von Dirty Chicken'),
         text=['Hallo Jonas', 'Aus demselben Haus kommt noch etwas anderes: Dirty Chicken macht wieder ein Pop-up, mit Sandwiches, Dirty Drinks und Live-Musik.',
               'Anmelden musst du dich nicht. Komm vorbei, solange der Vorrat reicht.'],
         karte=('Das Pop-up', [('Wann', 'Samstag, 30. Mai, ab 18:00 Uhr'), ('Wo', 'AM:PM Café im Tiedthof'), ('Instagram', '@dirtychicken.hannover')]),
         knopf=('Dirty Chicken ansehen', 'dirty-chicken.html'), dazu='Datum und Ort sind die des ersten Pop-ups, hier als Beispiel.'),
    dict(nr='10', wann='An die Gäste, die schon an der Tafel sassen', ordner='10-stammgaeste', name='Für dich zuerst', satz='Kommt an Gäste, die schon an der Tafel sassen: ein Platz am nächsten Abend wird für sie freigehalten, bevor er für alle aufgeht.',
         betreff='Wir halten einen Platz für dich frei', titel=('Wir halten einen Platz', 'für dich frei.'), foto=('kerze2', 'Gäste und Kerzen an der langen Tafel'),
         text=['Hallo Lena', 'Du hast schon an der Tafel gesessen, darum fragen wir dich zuerst: Für den nächsten Abend halten wir einen Platz für dich frei.',
               'Sag uns bis Sonntag Bescheid, ob du dabei bist. Danach geben wir den Platz an die Warteliste weiter.'],
         karte=('Für dich', [('Abend', 'Freitag, 18. Dezember 2026'), ('Beginn', '19:00 Uhr'), ('Frei bis', 'Sonntag, 22. November')]),
         knopf=('Platz annehmen', 'abend.html#termine-buchen'), dazu='Passt es dir nicht, musst du nichts tun.'),
    dict(nr='11', wann='Wenn jemand einen Abend verschenkt', ordner='11-gutschein', name='Ein Abend als Geschenk', satz='Geht an den Beschenkten: wer ihm den Abend schenkt, für wie viele, bis wann, und der Gutschein als PDF im Anhang.',
         betreff='Ein Abend an der langen Tafel, für dich', titel=('Ein Abend', 'an der langen Tafel.'), foto=('anstossen', 'Gäste stossen an der Tafel an'),
         text=['Hallo Lena', 'Jonas schenkt dir einen Abend an der langen Tafel: drei Gänge aus Rudis Küche und zu jedem Gang einen Drink, den Momo dir an der Tafel erklärt.',
               'Den Gutschein findest du im Anhang. Such dir einen Abend aus und schreib uns auf Instagram, dann halten wir deinen Platz frei.'],
         karte=('Dein Gutschein', [('Von', 'Jonas Becker'), ('Personen', '2'), ('Gültig bis', '[Datum]'), ('Nr.', 'C-[0000]')]),
         knopf=('Alle Abende ansehen', 'abende.html'), dazu='Wert und Gültigkeit legt das Haus noch fest; bis dahin stehen sie in Klammern.'),
]


def _bild(key):
    b = sorted(int(m.group(1)) for p in glob.glob(os.path.join(WEB, 'assets', 'bild', key + '-*.webp')) if (m := re.search(r'-(\d+)\.webp$', p)))
    return os.path.join(WEB, 'assets', 'bild', f'{key}-{b[-1]}.webp')


def bilder():
    """Fotos 1000 px, unter 100 KB (Qualität sinkt, bis es passt). Quelle: Bildregister der Website (geschärfte Fassungen kommen von selbst nach)."""
    os.makedirs(os.path.join(MAILS, 'img'), exist_ok=True)
    for f in FAELLE + [dict(foto=('trio', ''))]:
        key = f['foto'][0]
        im = Image.open(_bild(key)).convert('RGB'); w, h = im.size; nh = round(w * 9 / 16)
        if nh < h:
            y = round((h - nh) * (.3 if key == 'trio' else .5)); im = im.crop((0, y, w, y + nh))
        im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        z = os.path.join(MAILS, 'img', key + '.jpg')
        for br, qu in ((1000, 80), (1000, 72), (1000, 64), (900, 66), (820, 64), (760, 62)):
            k = im.resize((br, round(im.height * br / im.width)), Image.LANCZOS) if br < im.width else im
            k.save(z, quality=qu, optimize=True, progressive=True)
            if os.path.getsize(z) < 100_000:
                break


def mail(f, basis):
    """basis: Adresse der Website, relativ aus dem Ordner der Mail (Vorschau) oder voll (Versand)."""
    zeilen = ''.join(f'<tr><td style="padding:11px 0;border-top:1px solid #4a4855;font:400 11px/1.3 {SANS};letter-spacing:.14em;text-transform:uppercase;color:{LICHT};width:38%">{e(k)}</td>'
                     f'<td style="padding:11px 0;border-top:1px solid #4a4855;font:400 16px/1.35 {SANS};color:{BLATT}">{e(v)}</td></tr>' for k, v in f['karte'][1])
    absaetze = f'<p style="margin:0 0 14px;font:400 20px/1.3 {SANS};color:{TINTE}">{e(f["text"][0])}</p>' + ''.join(
        f'<p style="margin:0 0 14px;font:400 16px/1.62 {SANS};color:#3a3845">{e(t)}</p>' for t in f['text'][1:])
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>{e(f['betreff'])} · Culinarium</title></head>
<body style="margin:0;padding:0;background:{PAPIER}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{PAPIER}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:{BLATT};border-radius:22px;overflow:hidden">
  <tr><td align="center" style="background:{HOLZ};padding:34px 30px 30px">
    <img src="../img/logo.png" width="240" alt="Culinarium · A unique experience" style="display:block;border:0;width:240px;max-width:72%;height:auto;margin:0 auto">
    <h1 style="margin:28px 0 0;font:400 clamp(28px,7.4vw,36px)/1.15 {SERIF};color:{BLATT}">{e(f['titel'][0])}<br><span style="color:{KERZE}">{e(f['titel'][1])}</span></h1>
  </td></tr>
  <tr><td style="padding:34px clamp(22px,6vw,40px) 8px">{absaetze}</td></tr>
  <tr><td style="padding:6px 28px 6px"><img src="../img/{f['foto'][0]}.jpg" width="544" alt="{e(f['foto'][1])}" style="display:block;border:0;width:100%;height:auto;border-radius:16px"></td></tr>
  <tr><td style="padding:10px 28px 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{HOLZ};border-radius:16px">
    <tr><td style="padding:22px 26px 12px"><div style="font:400 10.5px/1.2 {SANS};letter-spacing:.2em;text-transform:uppercase;color:{KERZE};padding-bottom:12px">{e(f['karte'][0])} · Beispielwerte</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{zeilen}</table></td></tr></table></td></tr>
  <tr><td align="center" style="padding:26px 40px 8px"><a href="{basis}{f['knopf'][1]}" style="display:inline-block;padding:16px 30px;border-radius:999px;background:{HOLZ};font:400 12px/1 {SANS};letter-spacing:.16em;text-transform:uppercase;color:{BLATT};text-decoration:none">{e(f['knopf'][0])} &nbsp;↗</a></td></tr>
  <tr><td style="padding:14px 40px 30px"><p style="margin:0;font:400 15px/1.6 {SANS};color:#5b5763;text-align:center">{e(f['dazu'])}</p>
    <img src="../img/trio.jpg" width="520" alt="Drei aus dem Team vor der Bar" style="display:block;border:0;width:100%;max-width:520px;height:auto;margin:26px auto 0;border-radius:16px">
    <p style="margin:16px 0 0;font:400 17px/1.4 {SANS};color:{TINTE};text-align:center">Bis bald an der Tafel, {e(GRUSS)}</p></td></tr>
  <tr><td align="center" style="background:{RUSS};padding:26px 30px"><div style="font:400 13px/1.6 {SANS};color:{LICHT}">{e(ADRESSE)}<br>Freitag ab 19:00 · Samstag ab 17:00</div></td></tr>
</table>
</td></tr></table>
</body></html>
'''


def eingebettet(f):
    """Robert 18.10.2026 23:35 «die E-Mails laden zu lange … bis die offen sind»: die Mail steht direkt in der Seite (kein eingebettetes Fenster,
    das Safari beim Aufklappen erst nachzeichnet). Dieselbe Mail wie im Ordner, nur die Bildwege von hier aus."""
    t = mail(f, '../')
    t = t[t.index('<body'):]; t = t[t.index('>') + 1:t.rindex('</body>')]
    return t.replace('src="../img/', 'src="img/')


def uebersicht():
    # Robert 18.10.2026 (Website-Master Punkt 15): Mails nebeneinander im Band, obere Hälfte mit weichem Auslauf, «Ganze Mail» auf und zu,
    # Nummer, Titel, Absender und Wann darüber; Pfeile am Laptop, am Handy eine nach der anderen
    pf = lambda d: f'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="{d}"/></svg>'
    karten = ''.join(f'''<article class="mb hr" style="--i:{min(i, 4)}">
  <header class="mb-ueber"><span class="mb-nr">{f['nr']}</span><span class="mb-ueber__t"><b>{e(f['name'])}</b><small><span>Von</span> Culinarium</small><small><span>Wann</span> {e(f['wann'])}</small><small><span>Betreff</span> {e(f['betreff'])}</small></span></header>
  <div class="mb-blatt"><div class="mb-in">{eingebettet(f)}</div></div>
  <p class="mb-ganz"><button type="button" class="mb-kn" aria-expanded="false"><span class="a">Ganze Mail</span><span class="z">Weniger zeigen</span><i>{pf('M4 6l4 4 4-4')}</i></button></p>
</article>''' for i, f in enumerate(FAELLE))
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Elf Mails · Culinarium</title>
<style>
@font-face{{font-family:'Petrona';font-weight:100 900;font-display:swap;src:url('../assets/schrift/fraunces-soft.woff2') format('woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400 600;font-display:swap;src:url('../assets/schrift/instrument.woff2') format('woff2')}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:{RUSS};color:{BLATT};font:400 17px/1.6 'Instrument Sans',system-ui,sans-serif;--rand:clamp(20px,4.6vw,76px)}}
header.kopf{{padding:clamp(56px,8vw,120px) var(--rand) clamp(30px,4vw,60px);text-align:center}}
header.kopf img{{width:clamp(50px,5.9vw,92px);height:auto}}
h1{{margin:clamp(14px,1.6vw,24px) 0 0;font:340 clamp(2rem,4.6vw,4.2rem)/1.08 'Petrona',Georgia,serif}}h1 em{{font-style:normal;color:{KERZE}}}
header.kopf p{{max-width:60ch;margin:clamp(18px,2.1vw,32px) auto 0;color:rgba(250,244,244,.86)}}
main{{padding:0 0 clamp(60px,8vw,120px)}}
.band{{display:flex;gap:clamp(20px,2.4vw,40px);align-items:flex-start;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-padding-inline:var(--rand);padding:4px var(--rand) 34px;scrollbar-width:none;-webkit-overflow-scrolling:touch}}
.band::-webkit-scrollbar{{display:none}}
.band:focus-visible{{outline:2px solid {KERZE};outline-offset:-2px}}
.mb{{flex:0 0 clamp(300px,34vw,520px);scroll-snap-align:start}}
.mb:last-child{{margin-inline-end:var(--rand)}}
.mb-ueber{{display:flex;gap:16px;align-items:flex-start;margin:0 4px 18px}}
.mb-nr{{font:400 2.3rem/.9 'Petrona',Georgia,serif;color:{KERZE}}}
.mb-ueber__t{{display:flex;flex-direction:column;gap:5px;min-width:0}}
.mb-ueber__t b{{font:340 1.3rem/1.2 'Petrona',Georgia,serif}}
.mb-ueber__t small{{font-size:.86rem;line-height:1.4;color:rgba(250,244,244,.74)}}
.mb-ueber__t small span{{display:inline-block;min-width:5.4em;font:400 10px/1.4 ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;color:{KERZE}}}
.mb-blatt{{position:relative;height:640px;border-radius:20px;overflow:hidden;background:{PAPIER};box-shadow:0 0 0 1px rgba(239,118,73,.3),0 40px 50px -30px rgba(0,0,0,.9);-webkit-mask-image:linear-gradient(#000 68%,transparent);mask-image:linear-gradient(#000 68%,transparent)}}
.mb.auf .mb-blatt{{-webkit-mask-image:none;mask-image:none}}
.mb-in{{position:relative}}.mb-in table{{max-width:100%}}
.mb-ganz{{position:relative;margin:18px 0 0;text-align:center}}
.mb.auf .mb-ganz{{margin-top:22px}}
.mb-kn{{display:inline-flex;align-items:center;gap:12px;padding:8px 8px 8px 22px;border:0;border-radius:999px;cursor:pointer;font:400 11.5px/1 ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;color:{BLATT};
  background:linear-gradient(180deg,#3a3845,{HOLZ} 60%,{TIEF});box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 0 0 1px rgba(239,118,73,.38),0 14px 22px -12px rgba(0,0,0,.8)}}
.mb-kn i{{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;color:{TINTE};background:linear-gradient(180deg,#faf4f4,{KERZE} 55%,{GOLD});box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}}
.mb-kn svg{{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}}
.mb-kn .z,.mb.auf .mb-kn .a{{display:none}}.mb.auf .mb-kn .z{{display:inline}}.mb.auf .mb-kn svg{{transform:rotate(180deg)}}
.mb-kn:focus-visible{{outline:2px solid {LICHT};outline-offset:3px}}
.pfeile{{display:flex;justify-content:center;gap:14px;margin-top:4px}}
.pf{{width:52px;height:52px;border:0;border-radius:50%;cursor:pointer;display:grid;place-items:center;color:{TINTE};background:linear-gradient(180deg,#faf4f4,{KERZE} 55%,{GOLD});box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 12px 20px -10px rgba(0,0,0,.7)}}
.pf svg{{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.pf:disabled{{opacity:.35;cursor:default}}
footer{{padding:26px var(--rand) 40px;text-align:center;font-size:.92rem;color:rgba(250,244,244,.6);border-top:1px solid rgba(239,118,73,.2)}}
footer a{{color:{LICHT}}}
/* Hereinkommen wie auf den anderen Werkbank-Seiten: heben, nur transform und opacity, bei reduced-motion sofort da */
html.js .hr{{opacity:0;transform:translate3d(0,34px,0) scale(.985)}}
html.js .hr.da{{opacity:1;transform:none;transition:opacity .9s cubic-bezier(.2,.7,.2,1) calc(var(--i,0) * 110ms),transform 1.2s cubic-bezier(.16,1,.3,1) calc(var(--i,0) * 110ms)}}
@media (prefers-reduced-motion:reduce){{html.js .hr{{opacity:1;transform:none;transition:none}}}}
@media (max-width:760px){{.mb{{flex-basis:calc(100vw - 2 * var(--rand))}}.pfeile{{display:none}}}}
@media (hover:none){{.pfeile{{display:none}}}}
</style></head>
<body>
<script>if (!matchMedia('(prefers-reduced-motion:reduce)').matches && 'IntersectionObserver' in window) document.documentElement.classList.add('js');</script>
<header class="kopf"><img class="hr" style="--i:0" src="img/zeichen.png" alt="" width="72"><h1 class="hr" style="--i:1">Elf Mails,<br><em>so persönlich wie der Abend.</em></h1>
<p class="hr" style="--i:2">Was ein Gast nach der Buchung oder auf der Warteliste von euch bekommt, kommt im Kleid der neuen Seite. Elf Fälle als Idee, von der Buchung bis zum Abend danach. Namen, Daten und Nummern sind Beispielwerte, Preis, Zeiten und Adresse sind eure.</p></header>
<main><div class="band" id="mband" tabindex="0" aria-label="Die elf Mails, zum Blättern">{karten}</div>
<div class="pfeile hr" style="--i:2"><button type="button" class="pf" data-r="-1" aria-label="Vorige Mail">{pf('M10 3 5 8l5 5')}</button><button type="button" class="pf" data-r="1" aria-label="Nächste Mail">{pf('m6 3 5 5-5 5')}</button></div></main>
<footer class="hr">Entwurf von Robert Reff, Tasty Studios. Stand {STAND}. <a href="../werkbank/index.html#papier">Zurück zu «Alles auf einen Blick»</a></footer>
<script>
(function () {{
  /* Hereinkommen: Kopf, Band und Fuss heben sich, sobald sie ins Bild kommen; die Mails im Band kommen zusammen mit dem Band */
  if (document.documentElement.classList.contains('js')) {{
    var io = new IntersectionObserver(function (es) {{ es.forEach(function (e) {{ if (!e.isIntersecting) return; io.unobserve(e.target);
      (e.target.id === 'mband' ? [].slice.call(e.target.querySelectorAll('.hr')) : [e.target]).forEach(function (x) {{ x.classList.add('da'); }}); }}); }}, {{ rootMargin: '0px 0px -8% 0px', threshold: 0 }});
    [].forEach.call(document.querySelectorAll('header.kopf .hr,.pfeile,footer'), function (x) {{ io.observe(x); }}); io.observe(document.getElementById('mband'));
  }}
}})();
(function () {{
  /* die Mail steht in der Seite; zu sieht man den oberen Teil, auf die ganze Mail, sofort */
  var ms = [].slice.call(document.querySelectorAll('.mb'));
  function lage(m) {{ var bl = m.querySelector('.mb-blatt'), i = bl.querySelector('.mb-in'); bl.style.height = (m.classList.contains('auf') ? i.scrollHeight : Math.min(640, i.scrollHeight)) + 'px'; }}
  ms.forEach(function (m) {{
    var k = m.querySelector('.mb-kn');
    [].forEach.call(m.querySelectorAll('img'), function (im) {{ if (!im.complete) im.addEventListener('load', function () {{ lage(m); }}, {{ once: true }}); }});
    lage(m);
    k.addEventListener('click', function () {{ var auf = m.classList.toggle('auf'); k.setAttribute('aria-expanded', auf); lage(m); if (!auf) m.scrollIntoView({{ block: 'nearest' }}); }});
  }});
  var rt = 0; addEventListener('resize', function () {{ clearTimeout(rt); rt = setTimeout(function () {{ ms.forEach(lage); kl(); }}, 120); }});
  /* Pfeile am Laptop blättern das Band um eine Mail */
  var b = document.getElementById('mband'), p = document.querySelectorAll('.pf');
  function schritt() {{ return ms[0].getBoundingClientRect().width + parseFloat(getComputedStyle(b).columnGap || 0); }}
  function kl() {{ p[0].disabled = b.scrollLeft < 4; p[1].disabled = b.scrollLeft > b.scrollWidth - b.clientWidth - 4; }}
  [].forEach.call(p, function (x) {{ x.addEventListener('click', function () {{ b.scrollBy({{ left: +x.dataset.r * schritt(), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }}); }}); }});
  b.addEventListener('scroll', kl, {{ passive: true }}); kl();
}})();
</script>
</body></html>
'''


def main():
    bilder()
    for f in FAELLE:
        z = os.path.join(MAILS, f['ordner']); os.makedirs(z, exist_ok=True)
        open(os.path.join(z, 'index.html'), 'w', encoding='utf-8').write(mail(f, '../../'))
    open(os.path.join(MAILS, 'index.html'), 'w', encoding='utf-8').write(uebersicht())
    json.dump([[f['nr'], f['ordner'], f['name'], f['satz']] for f in FAELLE], open(os.path.join(HIER, 'werkbank.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(FAELLE), 'Mails gebaut:', ', '.join(f['ordner'] for f in FAELLE))


if __name__ == '__main__':
    main()
