#!/usr/bin/env python3
"""Dirty Chicken · Abschnitt «Nacht» nach dem Essen (Robert 28.10.2026, 00:00: «15» aus dirty-chicken-nacht-wahl.html).
Fassung 15 «Der Rahmen»: der Opening-Film steht unbeschnitten in der Mitte, zehn Fotos kommen beim Ankommen von oben, unten, links und rechts
herein und schliessen sich als Rahmen um ihn; darüber Kicker, Titel «Jenau meen Ding wa.» und der Satz, mittig.
Bilder: Glas 84612, Mannschaft 84558, Tisch DZiug6EoMRr, Karte 84626 (oben) · Theke 84611, Mannschaft DZIjZWNCGZT-1, Drinks 84683, Plakat (unten) · Tisch 84678 (links), Mannschaft DZIjZWNCGZT-2 (rechts).
Ersetzt den alten Teil «Dirty Food, Dirty Drinks» (dc-film). Aussehen am Ende von assets/culinarium.css (Block «Dirty Chicken · Nacht»). Stand davor *.vor-nacht15-2026-10-28."""
import bau
from bau import foto, zl, sw

KICK = 'Dirty Drinks &amp; Live-Musik'
TEXT = 'Die Drinks kommen von der Bar, die Musik vom Pop-up, und am Ende steht die ganze Mannschaft hinter dem Tresen. Opening 2026: „Wat ne Sause.“'
RAHMEN = {'o': ['dn_glas', 'dn_team', 'dc_tisch', 'dn_karte'], 'u': ['dn_bar', 'dc_team', 'dn_drinks', 'dc_plakat_ganz'], 'l': 'dn_tisch', 'r': 'dc_team2'}


def film():
    return ('<figure class="film nx15-f" style="--lq:url(assets/film/opening.webp);aspect-ratio:9/16"><video muted playsinline preload="none" poster="assets/film/opening.webp?v=%s" data-src="assets/film/opening.mp4?v=%s" aria-label="Opening 2026 bei Dirty Chicken"></video>'
            '<button class="film-nochmal" type="button" aria-label="Film noch einmal abspielen">Noch einmal</button></figure>') % (bau.VERSION, bau.VERSION)


def reihe(ks):
    return ''.join('<div class="nx15-b" style="--i:%d">%s</div>' % (i, foto(k, '', '(max-width:860px) 50vw, 22vw', auf=False, pos='50% 40%')) for i, k in enumerate(ks))


def nacht():
    kopf = '<div class="vk nx-kopf mitte"><p class="ek sw auf" style="--i:0"><span>%s</span></p>%s%s</div>' % (KICK, zl(['Jenau meen', 'Ding wa.'], 'h2', 'et'), sw(TEXT, 'p', 'ex', 2))
    return '''<section class="vab dc-ab ess nxs15" id="nacht" data-ton="nacht" data-lauf="Nacht"><div class="vi">%s</div>
<div class="nx15-rahmen auf"><div class="nx15-reihe o">%s</div><div class="nx15-mitte"><div class="nx15-seite l">%s</div><div class="nx15-film">%s</div><div class="nx15-seite r">%s</div></div><div class="nx15-reihe u">%s</div></div></section>''' % (
        kopf, reihe(RAHMEN['o']), foto(RAHMEN['l'], '', '(max-width:860px) 50vw, 46vw', auf=False), film(),
        foto(RAHMEN['r'], '', '(max-width:860px) 50vw, 46vw', auf=False, pos='50% 40%'), reihe(RAHMEN['u']))
