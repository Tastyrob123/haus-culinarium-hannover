#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Landgasthof Ruedihus, Abschnitt «Mails» (12.10.2026, Master 5b Punkt 15): drei Mails im Ton des Hauses, gross und von vorn.

Eigen fürs Ruedihus: drei Fälle statt zehn, in einer Sprache, und nur solche, die es im Entwurf wirklich gibt (Tischanfrage, Vor Ihrer Anreise,
Gutschein). Darum kein Band zum Blättern, sondern drei hohe Blätter nebeneinander, Name und Satz darunter, ein Knopf zur Übersicht.
Quelle: mails/_src/bau.py (Wortlaut, Angaben aus daten.py), Aufnahmen mails/_src/aufnahme.js → ansichten/Mails/NN.jpg.
Eingehängt am Ende von haus.py über H.EIGENE (key 'mails', nach 'rezeption'). Fehlen die Aufnahmen, fällt der Abschnitt weg."""
import json, os

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
_Q = os.path.join(ROOT, 'mails', '_src', 'werkbank.json')
_A = os.path.join(W, 'ansichten', 'Mails')
LISTE = [x for x in (json.load(open(_Q)) if os.path.exists(_Q) else []) if os.path.exists(os.path.join(_A, x[0] + '.jpg'))]
BEREIT = len(LISTE) >= 3
BILDER = [('ml-' + nr, os.path.join(_A, nr + '.jpg'), 1100, dict(q=84)) for nr, *_ in LISTE]
ZAHL = {3: 'Drei', 4: 'Vier', 5: 'Fünf', 6: 'Sechs'}.get(len(LISTE), str(len(LISTE)))
_PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'


def bau(k):
    e, bild, kn = k['e'], k['bild'], k['kn']
    blaetter = ''.join(f'''<a class="mr-k" href="../mails/{ordner}/index.html" target="_blank" rel="noopener" data-a="heben" style="--vz:{i * 140}ms">
        <span class="mr-k__b">{bild('ml-' + nr, 'Die Mail «' + name + '»')}</span>
        <h3>{e(name)}</h3><p>{e(satz)}</p><span class="pfeil">Mail lesen{_PF}</span></a>''' for i, (nr, ordner, name, satz) in enumerate(LISTE))
    return f'''
<section class="fl {k['fl']} blatt mr" id="mails">
  <div class="in">
    {k['kopf']()}
    <div class="mr-g">{blaetter}</div>
    <div class="kn-reihe" data-a="auf" style="margin-top:clamp(30px,3.6vw,56px);justify-content:center">{kn('Alle Mails ansehen', '../mails/index.html', neu=True)}</div>
  </div>
</section>'''


EINTRAG = dict(key='mails', nach='rezeption', nav='Mails', name='Mails', zeilen=[f'{ZAHL} Mails,', 'im Ton Ihres Hauses.'],
               text='Was ein Gast nach einer Anfrage oder vor der Reise von Ihnen bekommt, sieht aus wie die neue Seite. Drei Fälle als Idee: die Tischanfrage, die Woche vor der Anreise und der Gutschein. Namen und Daten darin sind Beispielwerte.',
               bau=bau)

CSS = '''
/* ---------- Mails: drei hohe Blätter von vorn, Name und Satz darunter (mails_reihe.py, 12.10.2026) ---------- */
.mr-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(18px,2.6vw,44px);max-width:1280px;margin:0 auto}
.mr-k{display:flex;flex-direction:column;color:inherit;text-decoration:none}
.mr-k__b{display:block;aspect-ratio:640/900;border-radius:clamp(16px,1.7vw,24px);overflow:hidden;background:var(--papier);box-shadow:0 0 0 1px rgba(201,133,67,.3),0 44px 56px -32px rgba(0,0,0,.95),0 14px 22px -14px rgba(0,0,0,.6)}
.mr-k__b img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 0;transform-origin:50% 12%;transition:transform 2.2s cubic-bezier(.16,1,.3,1)}
@media(hover:hover){.mr-k:hover .mr-k__b img{transform:scale(1.04);transition-duration:2.8s}}
.mr-k h3{margin:clamp(20px,2vw,28px) 0 0;font-family:var(--serif);font-weight:700;font-size:clamp(1.4rem,1.76vw,1.8rem);line-height:1.12;color:#fbf5ea}
.mr-k h3::after{content:'';display:block;width:44px;height:2px;margin:14px 0;background:var(--gold);opacity:.85}
.mr-k p{margin:0 0 16px;max-width:40ch;font-size:clamp(.98rem,1.04vw,1.06rem);line-height:1.6;color:rgba(251,245,234,.84)}
.mr-k .pfeil{margin-top:auto;align-self:flex-start;color:var(--gold)}
.mr [data-a="heben"]{opacity:1;transform:translate3d(0,130px,0) scale(.97);transform-origin:50% 100%;transition:transform 2.1s cubic-bezier(.16,1,.3,1);transition-delay:var(--vz,0ms)}
.mr [data-a="heben"].da{transform:none}
@media(max-width:860px){.mr-g{grid-template-columns:1fr;max-width:440px}.mr-k__b{aspect-ratio:640/700}}
@media (prefers-reduced-motion:reduce){.mr [data-a="heben"]{transform:none;transition:none}.mr-k__b img{transition:none;transform:none!important}}
'''
