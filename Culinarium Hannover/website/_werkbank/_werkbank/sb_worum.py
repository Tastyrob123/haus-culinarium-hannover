#!/usr/bin/env python3
"""Werkbank Culinarium, Blatt «Worum es geht» zwischen Brief und Register (Werkbank-Chat 28.10.2026; Aufbau und Kleid wie sb_worum.py des Schäfli,
Rechnung eigen für Culinarium). Im Vordergrund steht die Rechnung für die Abende: ein Wochenende mehr im Jahr, gebucht ohne Nachricht, und Plätze,
die über die Warteliste wieder besetzt werden. Keine Zahl ohne Quelle: Preis des letzten Abends aus website/bau.py › ABENDE (zuletzt «89,00 EUR»,
September 2026), Plätze aus der Website («Vierzehn Plätze an einer Tafel», Beitrag DFqbLG2s_dc), Abende im Jahr nach den Beiträgen 2025 (drei Wochenenden
mit Freitag und Samstag, fakten.json › termine). Alles andere ist als Annahme beschriftet und lässt sich überschreiben. Kein Agenturpreis, keine Zusage."""
import html, os, re

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
_BAU = open(os.path.join(os.path.dirname(ROOT), 'bau.py'), encoding='utf-8').read()
_PREIS = int(re.findall(r"'(\d+),00 EUR'", _BAU)[-1])   # Preis des letzten Abends in der Liste der Abende
ANNAHMEN = [  # Schlüssel, Zeile, Wert, Einheit, Beschriftung
    ('mehr', 'Abende mehr im Jahr', 2, '', 'Annahme · ein Wochenende mit Freitag und Samstag'),
    ('plaetze', 'Plätze an der Tafel', 14, '', 'laut eurer Seite'),
    ('preis', 'Preis je Platz', _PREIS, 'EUR', f'zuletzt {_PREIS} EUR, September 2026'),
    ('abende', 'Abende im Jahr heute', 6, '', 'Annahme · 2025 waren es drei Wochenenden'),
    ('frei', 'Plätze je Abend, über die Warteliste neu besetzt', 1, '', 'Annahme'),
]


def _eur(x):
    return f"{round(x):,}".replace(',', '.')


def blatt(k):
    v = {key: wert for key, _z, wert, _e, _q in ANNAHMEN}
    fest = v['mehr'] * v['plaetze'] * v['preis']
    lunch = v['frei'] * (v['abende'] + v['mehr']) * v['preis']
    felder = ''.join(f'<div class="vt-feld"><div class="vt-feld__l"><span>{e(z)}</span><small>{e(q)}</small></div><label class="vt-feld__w"><input type="text" inputmode="decimal" value="{wert}" data-k="{key}" aria-label="{e(z)}">'
                     + (f'<em>{e(ein)}</em>' if ein else '') + '</label></div>' for key, z, wert, ein, q in ANNAHMEN)
    gruende = [('Buchen ohne Nachricht', 'Abend wählen, Plätze wählen, zahlen: Das Ticket kommt per Mail. Niemand muss erst schreiben und auf eine Antwort warten.'),
               ('Die Warteliste füllt freie Plätze', 'Ist ein Abend voll, trägt sich der Gast ein. Wird ein Platz frei, wisst ihr, wen ihr fragen könnt.'),
               ('Gefunden werden', 'Wer heute «Culinarium Hannover» sucht, landet bei anderen Betrieben. Eine eigene Adresse ändert das.')]
    fotos = ['vt-g-1', 'vt-g-2', 'vt-g-3']
    gr = ''.join(f'<li>' + (f'<span class="vt-gb">{k["bild"](f, t)}</span>' if f in k['m'] else '') + f'<b>{e(t)}</b><span>{e(x)}</span></li>' for (t, x), f in zip(gruende, fotos))
    return f'''
<section class="fl fl--navy tapete blatt vt" id="worum">
  <div class="in">
    {k['kopf'](0, 'Worum es geht', ['Ein Abend mehr,', 'kein Platz bleibt leer.'], 'Die neue Seite soll zwei Dinge leichter machen: einen weiteren Abend füllen, ohne dass jede Buchung eine Nachricht braucht, und Plätze, die kurzfristig frei werden, über die Warteliste wieder besetzen. Hier steht ein Rechenbeispiel mit Annahmen; jede davon ersetzt ihr rechts durch eure eigene Zahl.')}
    <div class="ag-blatt vt-r" data-a="hoch">
      <div class="vt-r__t">
        <p class="ag-r__n">Die Rechnung</p>
        <h3>Ein Rechenbeispiel.</h3>
        <p class="vt-r__lead">Mit den Annahmen rechts: <b data-vt="feste">{v['mehr']}</b> Abende mehr im Jahr bringen <b data-vt="fest">{_eur(fest)}</b> Euro. Und wird an jedem Abend <b data-vt="lunch">{v['frei']}</b> Platz über die Warteliste neu besetzt, kommen <b data-vt="lunchsumme">{_eur(lunch)}</b> Euro im Jahr dazu.</p>
        <p class="ag-r__n vt-gr__k">Drei Wege an die Tafel</p>
        <ul class="vt-gr">{gr}</ul>
        <p class="vt-gegen__satz">Ob es so kommt, entscheidet nicht die Seite allein. Instagram, Empfehlungen und euer Ruf haben ihren Teil daran. Versprechen kann ich diese Zahlen nicht.</p>
      </div>
      <div class="vt-r__r">
        <p class="vt-r__k">Tragt eure eigenen Zahlen ein</p>
        {felder}
        <div class="vt-ergebnis">
          <div class="vt-erg"><b data-vt="fest">{_eur(fest)}</b><span>EUR</span><small>die Abende mehr im Jahr</small></div>
          <div class="vt-erg"><b data-vt="lunchsumme">{_eur(lunch)}</b><span>EUR</span><small>Plätze aus der Warteliste im Jahr</small></div>
          <div class="vt-erg vt-erg--gross"><b data-vt="summe">{_eur(fest + lunch)}</b><span>EUR</span><small>Rechenbeispiel zusammen</small></div>
        </div>
      </div>
    </div>
  </div>
</section>
{JS}'''



def bilder(webp, haus):
    for n, key, lage in (('vt-g-1', 'toast', (.5, .45)), ('vt-g-2', 'lachen', (.5, .45)), ('vt-g-3', 'schildtag', (.5, .45))):
        webp(haus(key), n, 520, 80, 3 / 2, lage)


JS = '''<script id="vt-rechner">
(function(){var S=document.getElementById('worum');if(!S)return;
var nf=new Intl.NumberFormat('de-DE',{maximumFractionDigits:0});
function w(el){var t=String(el.value).replace(/[\\u2019'\\u202f\\u00a0 ]/g,'').replace(/,/g,'.');var v=parseFloat(t);return isFinite(v)&&v>=0?v:null}
function setze(k,t){[].forEach.call(S.querySelectorAll('[data-vt="'+k+'"]'),function(x){x.textContent=t})}
function rechne(){var v={};[].forEach.call(S.querySelectorAll('input[data-k]'),function(i){var x=w(i);i.classList.toggle('falsch',x===null);v[i.getAttribute('data-k')]=x===null?0:x});
var fest=v.mehr*v.plaetze*v.preis,lunch=v.frei*(v.abende+v.mehr)*v.preis;
setze('feste',nf.format(v.mehr));setze('lunch',nf.format(v.frei));setze('fest',nf.format(fest));setze('lunchsumme',nf.format(lunch));setze('summe',nf.format(fest+lunch))}
[].forEach.call(S.querySelectorAll('input[data-k]'),function(i){i.addEventListener('input',rechne)});rechne()})();
</script>'''


CSS = '''
/* Blatt des Rechenbeispiels (Bauart des Blatts aus rh_angebot.py des Ruedihus) */
.ag-blatt{position:relative;padding:clamp(28px,3.8vw,64px);border-radius:clamp(22px,2.4vw,34px);background:linear-gradient(rgba(251,252,254,.94),rgba(251,252,254,.94)),var(--weiss) url(../assets/zeichen/tapete-hell.svg) 50% 0/224px auto;color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 50px 70px -46px rgba(0,0,0,.95)}
.ag-blatt::before,.ag-blatt::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(15,54,120,.4);border-radius:clamp(14px,1.6vw,24px);inset:clamp(10px,1.1vw,16px)}
.ag-blatt::after{inset:clamp(15px,1.5vw,22px);border-color:rgba(15,54,120,.18);border-radius:clamp(11px,1.3vw,19px)}
.ag-r__n{margin:0 0 12px;font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--taupe)}
.vt-r{color:var(--tinte)}
.vt-gr li{display:grid;grid-template-columns:clamp(92px,9vw,128px) 1fr;column-gap:16px;align-items:start}
.vt-gr li>.vt-gb{grid-row:1/span 2;display:block;border-radius:12px;overflow:hidden;aspect-ratio:3/2}.vt-gr li>.vt-gb img{display:block;width:100%;height:100%;object-fit:cover}
.vt-gr li>b,.vt-gr li>span:not(.vt-gb){grid-column:2}
'''
