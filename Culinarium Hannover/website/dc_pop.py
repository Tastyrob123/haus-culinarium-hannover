#!/usr/bin/env python3
"""Dirty Chicken · Abschnitt «Das erste Pop-up» (Robert 28.10.2026: «15 aber anderes bild» aus dirty-chicken-popup-wahl.html).
Fassung 15 «Senkrecht»: der Titel läuft senkrecht am linken Rand, in der Mitte ein hohes Bild, rechts die Angaben rechtsbündig.
Bild: der Burger im Papier mit Schriftzug (DZId0KMoAtq) statt des Standbilds aus dem Film; Robert 28.10.2026: «so ne Foto-Collage … mit 3 Bildern insgesamt, eins davon das Logo»: oben der Burger, darunter Zeichen und Sauce (84676), Kante an Kante, nichts überlappt.
Robert: «dieser Datumsbezug liegt ja in der Vergangenheit … das liest sich gerade, als würde das noch anstehen.» Deshalb Kicker «Rückblick» und der Satz in der Vergangenheit.
Ersetzt den alten Steckbrief (dc-pop). Aussehen am Ende von assets/culinarium.css (Block «Dirty Chicken · Pop-up»). Stand davor *.vor-pop15-2026-10-28."""
import bau
from bau import foto, zl, sw

KICK = 'Rückblick'
TEXT = 'So fing es an: ein Nachmittag und Abend im Tiedthof, mit Gastschicht an der Bar und Musik.'
FAKTEN = [('Wann', '30. Mai 2026, 14 bis 22 Uhr'), ('Wo', 'AM:PM Café im Tiedthof, Goseriede 4'), ('Was', 'Dirty Food, Dirty Drinks &amp; Live Music'),
          ('Gastschicht', 'Martin Bauermann, Beluga Vodka Berlin'), ('Danach', 'Aftershow im NATE'), ('Mit dabei', 'AM:PM, Walk on the Wild Side, Beluga, NATE')]


def popup():
    vz = '<dl class="pp-vz rechts sw auf" style="--i:3">%s</dl>' % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in FAKTEN)
    return '''<section class="vab dc-ab ess pps15" id="popup" data-ton="nacht" data-lauf="Das erste Pop-up"><div class="vi pp15">
<h2 class="pp15-senk zl auf-spaet" aria-label="Das erste Pop-up."><span class="z"><span style="--i:0">Das erste Pop-up.</span></span></h2>
<div class="pp15-bild pp15-collage"><div class="pp15-c gross">%s</div><div class="pp15-c">%s</div><div class="pp15-c">%s</div></div>
<div class="pp15-rechts"><p class="ek sw auf" style="--i:0"><span>%s</span></p>%s%s</div></div></section>''' % (
        foto('dc_burger', 'pp15-s', '(max-width:860px) 100vw, 36vw', pos='50% 55%'), foto('dc_zeichen', 'pp15-s', '(max-width:860px) 50vw, 18vw', pos='50% 50%'),
        foto('dn_sosse', 'pp15-s', '(max-width:860px) 50vw, 18vw', pos='50% 55%'), KICK, sw(TEXT, 'p', 'ex', 1), vz)
