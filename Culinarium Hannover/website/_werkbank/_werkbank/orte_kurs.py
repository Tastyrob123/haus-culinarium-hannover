#!/usr/bin/env python3
"""Werkbank Culinarium: «Meine drei Orte», das Kursblatt mit Hamburg, Koh Phangan und Siargao (Robert 29.10.2026: «meine hamburg siargao koh phangan
animation einfügen wie wir sie mal hatte»). Titel, Satz und Kursblatt (SVG) kommen unverändert aus dem Werkbank-Kit (bau.py › orte, Brief-Art «lang»;
werkbank.css › .kurs, @keyframes welle, beides lädt die Werkbank ohnehin).
Robert 1.11.2026: «soll mehr wie ein Ticket sein, kein Kasten». Form wie im Walk on the Wild Side (orte_kurs.py dort, übernommen): Kopfzeile, Hauptteil,
Perforation mit zwei ausgeschnittenen Kerben (Maske, Website-Master 13: nie Kreise über die Kante), Abriss hell; unter 620 px liegt der Abriss unten.
Kleid des Culinarium: Fläche Nacht (#16151A/#1C1B21), Abriss Warmweiss (#FAF4F4), Kopfzeile und Akzente in Kerze (var(--gold)), Schriften über --serif/--mono.
Gebraucht im Brief (brief_blatt.py, neben der Unterschrift) und im Schluss (wb_kapitel.py › schluss, unter der Unterschrift)."""
import os
import re

_HIER = os.path.dirname(os.path.abspath(__file__))
_KIT = next((p for p in (os.path.join(os.path.expanduser('~'), 'Desktop', 'Website-Projekte', '_Werkbank-Kit', 'bau.py'),
                         os.path.normpath(os.path.join(_HIER, '..', '..', '..', '..', '_Werkbank-Kit', 'bau.py')))   # Kit im Ordner des Hauses (Cloud)
             if os.path.exists(p)), None)


def block(art):
    """Der Block «orte» aus dem Kit als Ticket; art = 'brief' oder 'schluss' für die Lage im Kleid."""
    h = re.search(r"orte = '''(.*?)'''", open(_KIT, encoding='utf-8').read(), re.S).group(1).strip()
    innen = h[h.index('>') + 1:h.rindex('</div>')].strip()
    return (f'<div class="tk ok ok--{art}" data-a="kipp" style="--i:2"><div class="tk__f">'
            f'<div class="tk__h"><p class="tk__kopf"><span>Kursblatt</span><span>Robert Reff · Tasty Studios</span></p>{innen}</div>'
            '<div class="tk__a" aria-hidden="true"><span class="tk__nr">N° 3</span><b>3</b><small>Orte</small>'
            '<span class="tk__l">Hamburg<br>Koh Phangan<br>Siargao</span></div>'
            '</div></div>')


CSS = """
/* ---------- «Meine drei Orte» als Ticket im Kleid des Culinarium (orte_kurs.py, Robert 1.11.2026): Kursblatt aus dem Kit, Form wie im Walk on the Wild Side ---------- */
.ok .kurs text{fill:rgba(250,244,244,.72)}
.ok .kurs .ort{fill:#faf4f4}
.ok .kurs .weg,.ok .kurs .welle{stroke:var(--gold)}
.ok .kurs .pkt{fill:#faf4f4}.ok .kurs .da0{fill:var(--gold)}
/* Schatten an der Hülle (drop-shadow folgt der Maske), Fläche Nacht mit Kerben an der Naht, Abriss Warmweiss */
.tk{--ab:clamp(112px,22%,168px);--k:12px;color:#faf4f4;text-align:left;filter:drop-shadow(0 22px 26px rgba(8,7,10,.55)) drop-shadow(0 3px 6px rgba(8,7,10,.38))}
.tk__f{display:grid;grid-template-columns:minmax(0,1fr) var(--ab);border-radius:20px;overflow:hidden;background:linear-gradient(180deg,#1c1b21,#16151a);
  -webkit-mask:radial-gradient(circle at calc(100% - var(--ab)) 0,#0000 var(--k),#000 calc(var(--k) + .6px)) top/100% 51% no-repeat,radial-gradient(circle at calc(100% - var(--ab)) 100%,#0000 var(--k),#000 calc(var(--k) + .6px)) bottom/100% 51% no-repeat;
  mask:radial-gradient(circle at calc(100% - var(--ab)) 0,#0000 var(--k),#000 calc(var(--k) + .6px)) top/100% 51% no-repeat,radial-gradient(circle at calc(100% - var(--ab)) 100%,#0000 var(--k),#000 calc(var(--k) + .6px)) bottom/100% 51% no-repeat}
.tk__h{padding:clamp(20px,2.4vw,32px);min-width:0}
.tk__kopf{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:0 0 16px;padding-bottom:11px;border-bottom:1px solid rgba(239,118,73,.32);font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.tk h3{font-family:var(--serif);font-weight:400;font-size:1.5rem;line-height:1.14;margin:0 0 6px;color:#faf4f4}
.tk h3+p{color:rgba(250,244,244,.76);font-size:1rem;margin:0}
.tk__a{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:22px 12px;text-align:center;background:#faf4f4;color:#16151a}
.tk__a::before{content:'';position:absolute;left:0;top:calc(var(--k) + 6px);bottom:calc(var(--k) + 6px);border-left:2px dashed rgba(22,21,26,.3)}
.tk__nr{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:#b15736}
.tk__a b{font-family:var(--serif);font-weight:400;font-size:clamp(46px,5vw,64px);line-height:1;margin-top:6px;color:#ef7649}
.tk__a small{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase}
.tk__l{margin-top:10px;padding-top:10px;border-top:1px solid rgba(22,21,26,.16);font-family:var(--mono);font-size:9.5px;line-height:1.7;letter-spacing:.12em;text-transform:uppercase;color:rgba(22,21,26,.72)}
.ok--schluss{width:min(100%,560px);margin:clamp(22px,2.6vw,36px) auto 0}
@media (max-width:620px){
  .tk{--abh:96px}
  .tk__f{grid-template-columns:1fr;
    -webkit-mask:radial-gradient(circle at 0 calc(100% - var(--abh)),#0000 var(--k),#000 calc(var(--k) + .6px)) left/51% 100% no-repeat,radial-gradient(circle at 100% calc(100% - var(--abh)),#0000 var(--k),#000 calc(var(--k) + .6px)) right/51% 100% no-repeat;
    mask:radial-gradient(circle at 0 calc(100% - var(--abh)),#0000 var(--k),#000 calc(var(--k) + .6px)) left/51% 100% no-repeat,radial-gradient(circle at 100% calc(100% - var(--abh)),#0000 var(--k),#000 calc(var(--k) + .6px)) right/51% 100% no-repeat}
  .tk__a{height:var(--abh);box-sizing:border-box;flex-direction:row;flex-wrap:wrap;gap:4px 14px;padding:12px 20px}
  .tk__a::before{left:calc(var(--k) + 6px);right:calc(var(--k) + 6px);top:0;bottom:auto;border-left:0;border-top:2px dashed rgba(22,21,26,.3)}
  .tk__a b{font-size:40px;margin:0}.tk__nr{width:100%}.tk__l{margin:0;padding:0 0 0 14px;border-top:0;border-left:1px solid rgba(22,21,26,.16)}
}
"""
