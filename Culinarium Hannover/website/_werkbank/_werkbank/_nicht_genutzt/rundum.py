#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, «Rund um den Aufenthalt» (12.10.2026, Master 5b Punkt 9): die kleinen Seiten und Abschnitte gesammelt,
vor der Reise, im Zimmer, gleich gegenüber. Alle drei gibt es schon, zum Öffnen und Ausprobieren.

Eigen fürs Ruedihus: drei Stücke statt sechs (mehr gibt es hier nicht, und was schon bei «Für Ihre Gäste» oder den Ideen steht, wiederholt sich nicht);
die Bilder tragen die Einkerbung der Ruedihus-Seite mit einem Wort, wann der Gast die Seite braucht.
Aufnahmen: node _werkbank/sammlung.js → ansichten/Sammlung/<name>.jpg.   Eingehängt in haus.py über EIGENE (key 'rundum', nach 'gaeste')."""
import os

W = os.path.dirname(os.path.abspath(__file__))
_SM = os.path.join(W, 'ansichten', 'Sammlung')
_PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'

RUNDUM = [  # Bild, Wort in der Einkerbung, Titel, Satz, [(Knopf, Ziel)]
    ('anreise', 'Vor der Reise', 'Vor Ihrer Anreise', 'Wer gebucht hat, sagt hier, wann er kommt, ob in der Stube ein Tisch bereitstehen soll und ob er im Spa einen Termin möchte. Alles zusammen landet bei Ihnen.',
     [('Seite öffnen', '../anreise.html')]),
    ('mappe', 'Im Zimmer', 'Zimmermappe', 'Auf dem Nachttisch steht eine Karte mit einem Code. Der Gast scannt ihn und hat die Zeiten des Hauses und die Rezeption im Chat auf dem Handy, in seiner Sprache.',
     [('Seite öffnen', '../mappe.html'), ('Karte ansehen', '../drucksachen/index.html#mappekarte')]),
    ('spa', 'Gleich gegenüber', 'Spa im Nachbarhaus', 'Hallenbad, Saunen und Massagen liegen im Waldhotel Doldenhorn. Auf der Seite «Das Haus» steht das mit Bild und einem Knopf, der hinüberführt.',
     [('Abschnitt öffnen', '../haus.html#spa')]),
]
RUNDUM = [r for r in RUNDUM if os.path.exists(os.path.join(_SM, r[0] + '.jpg'))]
BILDER = [('ru-' + r[0], os.path.join(_SM, r[0] + '.jpg'), 1280, dict(schnitt=16 / 10, lage=(.5, 0))) for r in RUNDUM]


def bau(k):
    e, bild = k['e'], k['bild']
    karten = ''.join(f'''<article class="ru-k" data-a="auf" style="--i:{i % 3}">
        <a class="ru-k__b" href="{wege[0][1]}" target="_blank" rel="noopener">{bild('ru-' + n, t)}<span class="ru-k__kerbe">{e(wort)}</span></a>
        <div class="ru-k__t"><h3>{e(t)}</h3><p>{e(x)}</p>
        <p class="ru-k__l">{''.join(f'<a class="pfeil" href="{h}" target="_blank" rel="noopener">{e(kt)}{_PF}</a>' for kt, h in wege)}</p></div></article>'''
                     for i, (n, wort, t, x, wege) in enumerate(RUNDUM))
    return f'''
<section class="fl {k['fl']} blatt ru" id="rundum">
  <div class="in">
    {k['kopf']()}
    <div class="ru-g ru-g--{len(RUNDUM)}">{karten}</div>
  </div>
</section>'''


EINTRAG = dict(key='rundum', nach='gaeste', nav='', name='Weitere Seiten', zeilen=['Rund um', 'den Aufenthalt.'],
               text='Neben Startseite, Zimmern, Stuben und dem Haus gibt es kleine Seiten, die einem Gast vor der Reise, im Zimmer und am freien Nachmittag weiterhelfen. Jede davon lässt sich schon öffnen und ausprobieren.',
               bau=bau)

CSS = '''
/* ---------- Rund um den Aufenthalt (rundum.py, 12.10.2026): drei Stücke auf Papier, Bild mit Einkerbung wie auf der Ruedihus-Seite ---------- */
.ru-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(40px,4.2vw,70px) clamp(22px,2.6vw,44px)}
.ru-k{display:flex;flex-direction:column}
.ru-k__b{position:relative;display:block;border-radius:clamp(16px,1.6vw,24px);overflow:hidden;aspect-ratio:16/10;background:var(--navy);
  box-shadow:0 0 0 1px rgba(125,79,39,.3),0 30px 40px -28px rgba(60,34,12,.6),0 10px 18px -12px rgba(60,34,12,.3)}
.ru-k__b img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 0;transform-origin:50% 22%;transition:transform 2.2s cubic-bezier(.16,1,.3,1)}
.ru-k__kerbe{position:absolute;left:0;bottom:0;padding:9px 18px 8px 16px;border-radius:0 18px 0 0;background:var(--papier);font-family:var(--serif);font-weight:700;font-size:clamp(.96rem,1.04vw,1.08rem);line-height:1.2;color:var(--tinte)}
.ru-k__kerbe::before,.ru-k__kerbe::after{content:'';position:absolute;width:18px;height:18px;background:radial-gradient(circle at 100% 0,transparent 17.5px,var(--papier) 18px)}
.ru-k__kerbe::before{left:0;top:-18px}.ru-k__kerbe::after{right:-18px;bottom:0}
.fl--creme .ru-k__kerbe{background:var(--creme)}.fl--creme .ru-k__kerbe::before,.fl--creme .ru-k__kerbe::after{background:radial-gradient(circle at 100% 0,transparent 17.5px,var(--creme) 18px)}
.ru-k__t{flex:1;display:flex;flex-direction:column;padding:0 4px}
.ru-k h3{margin:clamp(20px,2vw,28px) 0 0;font-family:var(--serif);font-weight:700;font-size:clamp(1.44rem,1.76vw,1.8rem);line-height:1.12;color:var(--tinte)}
.ru-k h3::after{content:'';display:block;width:44px;height:2px;margin:14px 0 14px;background:var(--messing)}
.ru-k p{margin:0;max-width:40ch;font-size:clamp(.98rem,1.04vw,1.06rem);line-height:1.62;color:rgba(42,26,14,.84)}
.ru-k .ru-k__l{display:flex;flex-wrap:wrap;gap:2px 24px;margin-top:auto;padding-top:16px;max-width:none}
.ru-k__l .pfeil{color:var(--tinte);text-decoration:none;white-space:nowrap}
@media(hover:hover){.ru-k:hover .ru-k__b img{transform:scale(1.06);transition-duration:2.8s}}
@media(max-width:1000px){.ru-g{grid-template-columns:repeat(2,minmax(0,1fr))}.ru-g--3 .ru-k:last-child{grid-column:1/-1;max-width:calc(50% - clamp(11px,1.3vw,22px));margin-inline:auto}}
@media(max-width:640px){.ru-g{grid-template-columns:1fr;gap:46px}.ru-g--3 .ru-k:last-child{grid-column:auto;max-width:none}}
@media (prefers-reduced-motion:reduce){.ru-k__b img{transition:none;transform:none!important}}
'''
