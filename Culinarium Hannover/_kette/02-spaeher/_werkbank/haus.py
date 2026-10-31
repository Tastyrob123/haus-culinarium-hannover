"""Culinarium Hannover: Haken für das Werkbank-Kit, nur für die Befund-Seite des Spähers (Station 2, 25.10.2026).
Farben aus der Marke: Schiefer-Violett #3A3845 und Off-White #FAF4F4 (Pixel-Histogramm der Plakate, Kundenprofil Blatt 5),
Nacht aus dem Himmel des Mondfrau-Plakats (#2c2944, gemessen 25.10.2026), Punkt Ochsenblut #881301 (März-Plakat 2026).
Gold (Champagner) ist eine Arbeitsfarbe. Zeichen = ein «C» in doppeltem Rahmen wie die Wortmarke der Plakate, gesetzt in Fraunces:
Arbeitszeichen, nicht das Logo des Kunden. Marke, Schrift und Farbwelten legt erst Station 5 fest."""
import os, sys
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'Culinarium Hannover'
KURZ = 'culinarium-hannover'
LEISTE = 'Culinarium'
PORT = 8978
RECHTE = 'Culinarium Hannover (Rudolf Napieraj, Momo, Derya Ivkin) und den jeweiligen Fotografen (Irina Voronov, focusonbiz_hannover, Recap 02/2025 ohne Namen); Herkunft der Plakat-Illustrationen offen.'
SEITEN = []
ETIKETTEN = dict(ordner='etiketten', name='Etiketten', einzahl='Etikett')

FARBEN = dict(nacht='#2c2944', tief='#1c1a2b', navy='#3a3845', blau='#4b4859', papier='#faf4f4', creme='#efe5e2', weiss='#fdfafa',
              gold='#d4b483', messing='#a8875c', taupe='#8a7468', tinte='#2a2833', punkt='#881301', rot='#881301')
SCHRIFT = dict(titel=('Fraunces', 'fraunces-var.woff2'), titel_folge="Georgia,'Times New Roman',serif", ersatz="local('Georgia');size-adjust:100%")
DRUCKSCHRIFT = []
ZEICHEN = K.svg_innen(os.path.join(ROOT, 'assets/logo/zeichen.svg'))
WORT = K.text_pfad(os.path.join(ROOT, 'assets/fonts/fraunces-var.woff2'), 'CULINARIUM', .06)
MUSTER = 'url("muster.svg")'
MUSTER_B = '240px'
CSS = '''
/* Befund: Tabellen und Belege */
.bf-tab{width:100%;border-collapse:collapse;margin-top:clamp(18px,2vw,28px);font-size:15px}
.bf-tab th,.bf-tab td{text-align:left;padding:12px 14px;border-bottom:1px solid color-mix(in srgb,currentColor 14%,transparent);vertical-align:top}
.bf-tab th{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.7;font-weight:400}
.bf-beleg{font-family:var(--mono);font-size:12px;opacity:.72;word-break:break-word}
.bf-offen{color:var(--rot)}
.fl--nacht .bf-offen{color:#e98a72}
.bf-liste{list-style:none;padding:0;margin:clamp(18px,2vw,28px) 0 0;display:grid;gap:14px}
.bf-liste li{padding:18px 20px;border-radius:22px;background:color-mix(in srgb,currentColor 5%,transparent);box-shadow:inset 0 2px 6px rgba(0,0,0,.08)}
.bf-liste b{display:block;font-family:var(--serif);font-weight:400;font-size:20px;margin-bottom:4px}
.bf-fam{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin-top:clamp(22px,2.4vw,34px)}
.bf-fam a{display:block;border-radius:26px;overflow:hidden;color:inherit;text-decoration:none;background:color-mix(in srgb,currentColor 6%,transparent)}
.bf-fam img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.bf-fam div{padding:16px 18px 20px}
.bf-fam b{display:block;font-family:var(--serif);font-weight:400;font-size:21px}
.bf-fam small{display:block;font-family:var(--mono);font-size:11.5px;opacity:.72;margin-top:6px;line-height:1.5}
.bf-zwei{display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,2vw,28px);margin-top:clamp(22px,2.4vw,34px)}
.bf-zwei>div{padding:22px 24px;border-radius:26px;background:color-mix(in srgb,currentColor 5%,transparent);box-shadow:inset 0 2px 6px rgba(0,0,0,.08)}
.bf-zwei h3{font-family:var(--serif);font-weight:400;font-size:24px;margin:0 0 10px}
.bf-zwei ul{margin:0;padding:0;list-style:none;line-height:1.55}
.bf-zwei li{padding:9px 0;border-top:1px solid color-mix(in srgb,currentColor 14%,transparent)}
.bf-zwei li:first-child{border-top:0;padding-top:0}
.bf-urteil{font-family:var(--serif);font-size:clamp(30px,3.6vw,52px);line-height:1.12;margin:0}
.bf-urteil em{font-style:normal;color:var(--gold)}
.bf-plakate{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(14px,1.8vw,24px);margin-top:clamp(22px,2.4vw,34px)}
.bf-plakate figure{margin:0;border-radius:22px;overflow:hidden;background:color-mix(in srgb,currentColor 6%,transparent)}
.bf-plakate img{display:block;width:100%;aspect-ratio:1;object-fit:cover}
.bf-plakate figcaption{font-family:var(--mono);font-size:11.5px;opacity:.75;padding:12px 14px 14px;line-height:1.5}
@media (max-width:640px){.bf-plakate{grid-template-columns:1fr 1fr}.bf-plakate figure:last-child{grid-column:1/-1}}
@media (max-width:760px){.bf-zwei{grid-template-columns:1fr}}
@media (max-width:640px){.bf-tab,.bf-tab tbody,.bf-tab tr,.bf-tab td{display:block;width:100%}.bf-tab thead{display:none}.bf-tab tr{padding:12px 0;border-bottom:1px solid color-mix(in srgb,currentColor 14%,transparent)}.bf-tab td{border:0;padding:2px 0;font-size:15px}.bf-tab td:first-child{font-family:var(--serif);font-size:19px;margin-bottom:4px}}
'''
