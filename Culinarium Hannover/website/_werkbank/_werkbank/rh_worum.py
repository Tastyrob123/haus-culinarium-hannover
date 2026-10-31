"""Werkbank Culinarium: nur noch das CSS des Rechner-Blatts (Bauart aus rh_worum.py des Ruedihus über das Schäfli), das wb_kapitel.py als VT.CSS einhängt.
Das Blatt selbst baut sb_worum.py mit den Zahlen von Culinarium."""
CSS = '''
/* ---------- «Worum es geht» (vertrieb.py, 16.10.2026): Blatt zwischen Brief und Register, Rechner mit richtigen Feldern ---------- */
.vt .kopfzeile{margin-bottom:clamp(30px,3.4vw,54px)}
.vt-r{display:grid;gap:clamp(26px,3.4vw,64px);align-items:start}
@media(min-width:960px){.vt-r{grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr)}}
/* Robert 18.10.2026: beide Spalten schliessen bündig ab, kein Leerraum unter der rechten Karte */
@media(min-width:960px){.vt-r{align-items:stretch}.vt-r__r{display:flex;flex-direction:column}.vt-ergebnis{flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-around}}
.vt-r__t h3{margin:0;font-family:var(--serif);font-weight:400;font-size:clamp(1.9rem,2.7vw,2.9rem);line-height:1.08;color:var(--tinte)}
.vt-r__t>p{margin:16px 0 0;max-width:46ch;font-family:var(--serif);font-size:clamp(1.06rem,1.16vw,1.22rem);line-height:1.6;color:rgba(12,21,38,.82)}
.vt-r__lead{margin:16px 0 0;max-width:40ch;font-family:var(--serif);font-size:clamp(1.24rem,1.5vw,1.6rem)!important;line-height:1.48!important;color:var(--tinte)!important}
.vt-r__lead b{font-weight:400;color:#8a6f35;font-variant-numeric:tabular-nums}
.vt-gegen{margin-top:clamp(24px,2.8vw,40px);padding:clamp(20px,2.2vw,30px);border-radius:18px;background:linear-gradient(180deg,#0f2a55,#0b1f40);color:#fbf6ea;box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 0 0 1px rgba(220,198,143,.5),0 30px 40px -30px rgba(6,20,43,.8)}
.vt-gegen .ag-r__n{color:var(--gold)}
.vt-gegen__z{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:9px 0;border-bottom:1px solid rgba(220,198,143,.2);font-family:var(--serif);font-size:clamp(1.04rem,1.14vw,1.2rem)}
.vt-gegen__z b{font-weight:400;font-variant-numeric:tabular-nums}
.vt-gegen__z--s{color:var(--gold)}
.vt-gegen__z i{font-style:normal}
.vt-gegen__z:last-of-type{border-bottom:0}
.vt-gegen__satz{margin:12px 0 0;padding-top:14px;border-top:1px solid rgba(220,198,143,.5);font-family:var(--serif);font-size:clamp(1rem,1.08vw,1.12rem);line-height:1.5;color:rgba(251,246,234,.86)}
.vt-gr__k{margin-top:clamp(24px,2.8vw,38px)!important}
.vt-gr{margin:0;padding:0;list-style:none}
.vt-gr li{position:relative;padding:12px 0 12px 30px;border-bottom:1px solid rgba(150,125,64,.22)}
.vt-gr li:last-child{border-bottom:0}
.vt-gr li::before{content:"";position:absolute;left:4px;top:1.15em;width:12px;height:6px;border-left:2px solid #8a6f35;border-bottom:2px solid #8a6f35;transform:rotate(-45deg)}
.vt-gr b{display:block;font-family:var(--serif);font-weight:400;font-size:clamp(1.1rem,1.2vw,1.26rem);color:var(--tinte)}
.vt-gr span{display:block;margin-top:3px;font-family:var(--serif);font-size:clamp(.98rem,1.04vw,1.08rem);line-height:1.5;color:rgba(12,21,38,.76)}
.vt-erg--gross b{font-size:clamp(2.8rem,3.8vw,4rem)}
.vt-erg--gross{padding-top:14px}
.vt-r__k{margin:0 0 14px;font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:#967d40}
.vt-feld{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 18px;align-items:center;padding:12px 0;border-bottom:1px solid rgba(150,125,64,.22)}
.vt-feld:last-of-type{border-bottom:0}
.vt-feld__l span{display:block;font-family:var(--serif);font-size:clamp(1.14rem,1.24vw,1.32rem);line-height:1.3;color:var(--tinte)}
.vt-feld__l small{display:block;margin-top:4px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#967d40}
.vt-feld__w{display:flex;align-items:baseline;gap:8px;min-width:8.6em;padding:9px 16px 9px 14px;border-radius:12px;background:rgba(255,255,255,.72);box-shadow:inset 0 1px 2px rgba(60,40,10,.08),inset 0 0 0 1px rgba(150,125,64,.42);cursor:text;transition:box-shadow .3s}
.vt-feld__w:focus-within{box-shadow:inset 0 1px 2px rgba(60,40,10,.08),inset 0 0 0 1.5px #967d40}
.vt-feld__w input{flex:1 1 auto;width:6.5em;min-width:0;appearance:none;-webkit-appearance:none;background:transparent;border:0;padding:0;text-align:right;font-family:var(--serif);font-size:clamp(1.6rem,1.9vw,2rem);line-height:1.1;color:var(--tinte)}
.vt-feld__w input:focus{outline:0;color:#6d5a2c}
.vt-feld__w em{flex:none;font-family:var(--serif);font-style:italic;font-size:clamp(1rem,1.06vw,1.1rem);color:rgba(12,21,38,.62)}
.vt-ergebnis{margin-top:clamp(18px,2vw,26px);padding:clamp(18px,2vw,26px) clamp(20px,2.2vw,28px);border-radius:18px;background:linear-gradient(180deg,#fbf3e2,#f0e3c4);box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.5)}
.vt-r__u{margin:0 0 12px;padding-bottom:12px;border-bottom:1px solid rgba(150,125,64,.3);font-family:var(--serif);font-style:italic;font-size:clamp(1rem,1.06vw,1.1rem);color:rgba(12,21,38,.7)}
.vt-r__u b{font-weight:400;font-style:normal;color:var(--tinte)}
.vt-erg{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;padding:8px 0}
.vt-erg+.vt-erg{border-top:1px solid rgba(150,125,64,.22)}
.vt-erg b{font-family:var(--serif);font-weight:400;font-size:clamp(2.4rem,3.2vw,3.4rem);line-height:1;color:#967d40;font-variant-numeric:tabular-nums}
.vt-erg span{font-family:var(--serif);font-style:italic;font-size:clamp(1.1rem,1.2vw,1.3rem);color:#967d40}
.vt-erg small{flex-basis:100%;font-family:var(--serif);font-size:clamp(1.02rem,1.08vw,1.14rem);color:rgba(12,21,38,.78)}
@media(max-width:600px){.vt-feld{grid-template-columns:1fr}.vt-feld__w{min-width:0}}
/* ---------- Kapitel 1, die vier Funde auf der Bühne der Befunde (vertrieb.py): Bedeutung unter dem Klartext, Fenster am Rechner ---------- */
.bfk-bed{flex-basis:100%;order:2;display:grid;gap:8px 18px;margin-top:4px}
@media(min-width:700px){.bfk-bed{grid-template-columns:1fr 1fr}}
.bfk-bed span{display:block;padding:10px 14px;border-radius:12px;color:var(--tinte);background:linear-gradient(180deg,#fbf3e2,#ecdfc0);box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(220,198,143,.7);font-family:var(--serif);font-size:clamp(.94rem,1vw,1.04rem);line-height:1.42}
.bfk-bed b{display:block;margin-bottom:2px;font-family:var(--mono);font-weight:500;font-size:.64rem;letter-spacing:.18em;text-transform:uppercase;color:#8a6f35}
.bfk .bfx--fenster .bfx-fen{width:min(100%,400px)}
.bfk .bfx-fen__s{position:relative}
.bfk .bfx--fenster .bfx-kreis{inset:0}
.bfx--handy .bfx-tel__s img{border-radius:32px}
.bfk-b__t small{white-space:normal}
.bfk-wahl{flex-wrap:wrap}
@media(max-width:600px){.bfk .bfx--handy{max-width:142px}.bfk .bfx--handy .bfx-tel{height:min(60vh,300px)}.bfk .bfx--handy figcaption{max-width:100%;margin-top:10px}.bfk .bfx--handy figcaption span{font-size:.8rem}}
@media (prefers-reduced-motion:reduce){.vt .ag-blatt[data-a]{opacity:1;transform:none}}
'''
