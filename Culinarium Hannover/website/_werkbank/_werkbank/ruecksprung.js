/* Werkbank Culinarium: Rücksprung-Höhe (Robert 1.11.2026: «wenn ich in etwas reingehe, z. B. Feed, und dann mit den Pfeiltasten im Browser zurückgehe,
   will ich nicht immer ganz oben auf der Werkbank landen, sondern auf der Höhe, von der ich komme»).
   Je Seite die Höhe in sessionStorage (Schlüssel «rs:<Pfad>»), gemerkt bei pagehide und bei jedem Klick auf einen Link. Beim Zurück/Vor:
   aus dem bfcache (pageshow persisted) nur nachstellen, wenn der Browser woanders steht; nach neuem Laden (Navigation «back_forward») nach dem
   Aufbau dorthin, ohne den Auftakt neu abzuspielen (was über der Stelle liegt, gilt als gezeigt; Übergänge kurz aus). Kein unload-Handler,
   damit der bfcache bleibt. Beim normalen Laden tut das Skript nichts. ruecksprung.py setzt es als <script id="ruecksprung"> in alle Seiten. */
(function(){
var id=null;try{id=history.state&&history.state.rs;if(!id){id=Date.now().toString(36)+Math.random().toString(36).slice(2,6);history.replaceState(Object.assign({},history.state||{},{rs:id}),'')}}catch(e){}
var K='rs:'+location.pathname+(id?':'+id:'');   /* je Eintrag im Verlauf: dieselbe Seite zweimal im Verlauf behält zwei Höhen */
function merk(){try{sessionStorage.setItem(K,String(Math.round(window.scrollY||0)))}catch(e){}}
function hol(){try{var v=sessionStorage.getItem(K);return v&&/^\d+$/.test(v)?+v:null}catch(e){return null}}
addEventListener('pagehide',merk);
document.addEventListener('click',function(ev){var a=ev.target&&ev.target.closest&&ev.target.closest('a[href]');if(a&&(a.getAttribute('href')||'').charAt(0)!=='#')merk()},true);
function gezeigt(y){var g=y+innerHeight*1.2;[].forEach.call(document.querySelectorAll('[data-a],.odo,.zt,.roll,img.ld'),function(e){if(e.classList.contains('da'))return;var r=e.getBoundingClientRect();if(r.top+scrollY<g)e.classList.add('da')})}
addEventListener('pageshow',function(ev){if(!ev.persisted)return;var y=hol();if(y===null)return;gezeigt(y);if(Math.abs(scrollY-y)>40)scrollTo(0,y)});
var nav=null;try{nav=performance.getEntriesByType('navigation')[0]}catch(e){}
var typ=nav?nav.type:(performance.navigation&&performance.navigation.type===2?'back_forward':'');
if(typ!=='back_forward')return;
var y=hol();if(y===null||y<40)return;
try{history.scrollRestoration='manual'}catch(e){}
var H=document.documentElement,st=document.createElement('style');
st.textContent='html.rs-sofort,html.rs-sofort *{transition:none!important;animation-duration:0s!important;animation-delay:0s!important;scroll-behavior:auto!important}';
document.head.appendChild(st);H.classList.add('rs-sofort');
var weg=false;['wheel','touchstart','keydown','mousedown'].forEach(function(k){addEventListener(k,function(){weg=true},{once:true,passive:true})});
function geh(){if(weg)return;scrollTo(0,y);gezeigt(y)}
function los(){geh();requestAnimationFrame(function(){geh();requestAnimationFrame(function(){H.classList.remove('rs-sofort')})});
 var n=0,t=setInterval(function(){n++;if(Math.abs(scrollY-y)>40)geh();if(n>=14||weg)clearInterval(t)},150)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',los);else los();
addEventListener('load',function(){if(Math.abs(scrollY-y)>40)geh()});
})();
