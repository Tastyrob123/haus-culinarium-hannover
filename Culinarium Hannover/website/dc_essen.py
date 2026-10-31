#!/usr/bin/env python3
"""Dirty Chicken · Abschnitt «Essen» direkt nach dem Fenster (Robert 27.10.2026 abends: «Nummer 18» aus dirty-chicken-essen-wahl.html,
«aber ich möchte zwischen den Chicken Chunks, dem Sandwich und dem Pommes und Krautsalat durchklicken können, dass mir andere Bilder angezeigt werden»).
Fassung 18 «Dirty Food, gross»: zwei Zeilen Versalien in Umrisslinie laufen gegenläufig hinter einem Bild; rechts der Kicker, der Titel und die Karte als Zeilen.
Neu: die drei Zeilen sind Knöpfe. Antippen tauscht das Bild an derselben Stelle (das gewählte schiebt sich von unten herauf, nichts springt).
Bilder: Chicken Chunks = Chunks mit Sauce und Glas (Instagram DZIo4FHIqRR), Sandwich = 84673, Pommes & Krautsalat = 84607.
Aussehen am Ende von assets/culinarium.css (Block «Dirty Chicken · Essen»), Bewegung am Ende von assets/culinarium.js. Stand davor *.vor-essen18-2026-10-27."""
import bau
from bau import foto, zl, sw

GERICHTE = [('Chicken Chunks', 'Spicy Glaze, grüne Sauce', 'dc_drink', '50% 50%'),
            ('Sandwich', 'Paprika-Honig-Mayo, eingelegte Zwiebeln', 'dn_burger', '50% 55%'),
            ('Pommes &amp; Krautsalat', 'kommen immer mit', 'dn_salat', '50% 50%')]


def lauf(woerter, cls):
    eins = ' · '.join(woerter) + ' · '
    return '<div class="e18-lauf %s" aria-hidden="true"><p>%s</p><p>%s</p></div>' % (cls, eins, eins)


def essen():
    bilder = ''.join('<div class="e18-b" data-s="%d">%s</div>' % (i, foto(k, '', '(max-width:860px) 100vw, 44vw', auf=False, pos=p))
                     for i, (_n, _s, k, p) in enumerate(GERICHTE))
    zeilen = ''.join('<button type="button" class="ez e18-z sw auf%s" data-s="%d" aria-pressed="%s" style="--i:%d"><b>%s</b><span>%s</span></button>' % (
        ' an' if i == 0 else '', i, 'true' if i == 0 else 'false', 2 + i, n, s) for i, (n, s, _k, _p) in enumerate(GERICHTE))
    return '''<section class="vab dc-ab ess es18" id="essen" data-ton="nacht" data-lauf="Essen"><div class="e18">%s%s
<div class="vi e18-mitte auf"><div class="e18-bild e18-wahl" data-wahl="0">%s</div><div class="vk"><p class="ek sw auf" style="--i:0"><span>Dirty Food</span></p>%s<div class="ezl e18-zeilen" role="group" aria-label="Was auf den Tisch kommt">%s</div></div></div></div></section>''' % (
        lauf(['DIRTY FOOD', 'DIRTY DRINKS', 'SANDWICHES &amp; MORE'], 'a'), lauf(['CHICKEN CHUNKS', 'SPICY GLAZE', 'PICKLED ONIONS'], 'b'),
        bilder, zl(['Dirty', 'Food.'], 'h2', 'et'), zeilen)
