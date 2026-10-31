#!/usr/bin/env python3
"""Namenstafel der sieben Werkzeuge · Culinarium Hannover (28.10.2026). Drei Sätze, je Werkzeug Name + ein Satz + Alternative.
python3 namen.py  → tafel.html (dann bild.js → _Oberchef/zeigen/culinarium/namen-tafel.png)"""
import html
WZ = ['Zentrale', 'Website pflegen', 'Karten', 'Gäste-Chat-Team', 'Marke', 'Besuche', 'Drucksachen']
SAETZE = [
  ('A', 'An der Bar', 'Die Welt der Bar Walk on the Wild Side: Tresen, Fenster, Karte, Plakatwand.', [
    ('Der Tresen', 'Hier beginnt alles: ein Blick auf alle Werkzeuge und ihren Stand.', 'Die Theke'),
    ('Das Schaufenster', 'Die Website selbst pflegen: Texte, Fotos, Abende, Hinweise.', 'Die Fensterfront'),
    ('Die Pairing-Karte', 'Gänge und Drinks je Abend schreiben, daraus entstehen Karte und PDF.', 'Die Barkarte'),
    ('Das Gästebuch', 'Fragen der Gäste zu Abenden, Plätzen und Unverträglichkeiten, mit Antwortentwurf.', 'Die Anfragenmappe'),
    ('Das Markenbuch', 'Wortmarke, Fotos, Farben und Schriften des Hauses an einem Ort.', 'Das Markenbuch'),
    ('Die Besucherliste', 'Wer die Website besucht: woher, wann, welche Abende, wer reservieren geht.', 'Die Strichliste'),
    ('Die Plakatwerkstatt', 'Plakate je Abend, Karten und Beiträge in der Sprache des Hauses entwerfen.', 'Die Siebdruckerei'),
  ]),
  ('B', 'Der Abend', 'Die Welt eines Pairing-Abends: Pass, Programm, Tafel, Rezeptur.', [
    ('Der Pass', 'Wo alles zusammenkommt: alle Werkzeuge und ihr Stand auf einen Blick.', 'Die Abendtafel'),
    ('Das Programmheft', 'Die Website selbst pflegen: was kommt, wer kocht, wie man hinfindet.', 'Der Aushang'),
    ('Das Menüblatt', 'Jeder Gang mit seinem Drink, je Abend gesetzt und druckfertig.', 'Die Gangfolge'),
    ('Das Tischbuch', 'Anfragen zu Plätzen und Abenden beantworten, das Wissen des Chats pflegen.', 'Die Gästemappe'),
    ('Die Rezeptur', 'Die Marke als Rezept: Zeichen, Farben, Schriften, Fotos, Regeln.', 'Die Hausrezeptur'),
    ('Der Abendzettel', 'Besuche der Website: welche Abende gefragt sind und wer bucht.', 'Das Eingangsbuch'),
    ('Die Plakatpresse', 'Für jeden Abend sein eigenes Plakat, dazu Karten und Beiträge.', 'Die Druckerei'),
  ]),
  ('C', 'Linden, Haasemannstraße', 'Die Welt des Ortes: Hinterzimmer, Fassade, Tür, Klebewand.', [
    ('Das Hinterzimmer', 'Wo geplant wird: von hier zu allen Werkzeugen, mit ihrem Stand.', 'Das Büro'),
    ('Die Fassade', 'Was nach aussen leuchtet: die Website selbst pflegen.', 'Die Leuchtschrift'),
    ('Die Abendkarte', 'Menü und Drinks für jeden Abend, als Karte am Platz und als PDF.', 'Das Kreideboard'),
    ('Die Platzanfragen', 'Was Gäste fragen und wissen wollen, mit Antwortentwurf fürs Team.', 'Der Tischplan'),
    ('Der Stempel', 'Alles, was das Culinarium erkennbar macht: Marke, Fotos, Farben.', 'Die Markenkiste'),
    ('Die Türliste', 'Wer durch die Tür der Website kommt, ohne Cookies und Namen.', 'Die Besucherzählung'),
    ('Der Plakatdruck', 'Plakate, Karten und Beiträge im Stil der Abende, druckfertig.', 'Die Klebewand'),
  ]),
]
e = html.escape
def satz(b, t, unter, reihen):
    zs = ''.join(f'<li><span class="wz">{e(WZ[i])}</span><b>{e(n)}</b><p>{e(s)}</p><small>oder: {e(a)}</small></li>' for i, (n, s, a) in enumerate(reihen))
    return f'<section><header><i>{b}</i><div><h2>{e(t)}</h2><p>{e(unter)}</p></div></header><ol>{zs}</ol></section>'
seite = f'''<!doctype html><html lang="de"><meta charset="utf-8"><title>Namenstafel Culinarium</title>
<style>
@font-face{{font-family:F;src:url(/assets/schrift/fraunces-soft.woff2);font-weight:100 900}}
@font-face{{font-family:I;src:url(/assets/schrift/instrument.woff2);font-weight:400 600}}
@font-face{{font-family:U;src:url(/assets/schrift/urbanist.woff2);font-weight:100 900}}
@font-face{{font-family:M;src:url(/assets/schrift/dmmono.woff2)}}
*{{box-sizing:border-box;margin:0}}body{{background:#16151A url(/assets/zeichen/tapete-dunkel.svg) 0 0/224px;color:#FAF4F4;font:400 17px/1.5 I;padding:64px 64px 56px;width:1800px}}
.kopf{{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:40px}}
.kopf svg{{width:420px;height:47px;color:#FAF4F4;display:block;margin-bottom:22px}}
h1{{font:300 64px/1 F;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144;letter-spacing:-.015em}}
.kopf p{{font:400 13px/1.6 U;letter-spacing:.16em;text-transform:uppercase;color:#F5A689;text-align:right;max-width:520px}}
.x{{display:block;width:96px;height:14px;margin:14px 0 0;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='96' height='14'%3E%3Cpath d='M0 7h38M58 7h38' stroke='%23F5A689' stroke-opacity='.5'/%3E%3Cpath d='M43.5 2.5l9 9M52.5 2.5l-9 9' stroke='%23EF7649' stroke-width='1.6' stroke-linecap='round'/%3E%3C/svg%3E")}}
.reihe{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}}
section{{background:#FAF4F4;color:#26242D;border-radius:10px;border-top:3px solid #EF7649;padding:30px 30px 18px;box-shadow:0 40px 60px -40px #000}}
header{{display:flex;gap:18px;align-items:flex-start;padding-bottom:18px;border-bottom:1px solid rgba(38,36,45,.14)}}
header i{{font:300 58px/.9 F;font-style:normal;color:#B15736;font-variation-settings:"SOFT" 100,"opsz" 144}}
h2{{font:340 32px/1.05 F;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144}}
header p{{font-size:14.5px;color:#5B5763;margin-top:6px}}
ol{{list-style:none;padding:0}}li{{padding:15px 0 14px;border-bottom:1px solid rgba(38,36,45,.1)}}li:last-child{{border:0}}
.wz{{display:block;font:500 11px/1.4 U;letter-spacing:.16em;text-transform:uppercase;color:#B15736}}
li b{{display:block;font:360 27px/1.15 F;font-variation-settings:"SOFT" 100,"opsz" 144;margin:2px 0 3px}}
li p{{font-size:15px;line-height:1.45;color:#3A3845}}li small{{display:block;font:400 12.5px/1.5 M;color:#5B5763;margin-top:5px}}
.fuss{{margin-top:26px;font:400 13px/1.6 M;color:rgba(250,244,244,.7)}}
</style><body>
<div class="kopf"><div><svg viewBox="0 0 364.78 40.36"><use href="/assets/zeichen/marke.svg#wm"/></svg><h1>Drei Namenssätze für die sieben Werkzeuge</h1><span class="x"></span></div>
<p>Culinarium Hannover · Momo x Rudi in der Bar Walk on the Wild Side · Name zuerst nach dem, was das Werkzeug tut</p></div>
<div class="reihe">{''.join(satz(*s) for s in SAETZE)}</div>
<p class="fuss">Bis zur Wahl gelten die Arbeitsnamen La Maison · Le Bureau · La Carte · La Réception · Le Livre · Le Registre · L’Imprimerie. Gewählte Namen stehen an einer Stelle: _werkzeuge/oberflaeche/kleid/culinarium.js. Mischen aus den Sätzen geht.</p>
</body></html>'''
open(__file__.replace('namen.py', 'tafel.html'), 'w', encoding='utf-8').write(seite)
print('tafel.html')
