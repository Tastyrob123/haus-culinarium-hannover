"""Werkbank Culinarium: Lade- und Wege-Skripte aus der Werkbank des Schäfli (dort Schlössli und Ruedihus; nur kopiert).
VORLADEN_JS Bänder laden vorab · FRUEH_JS Bilder anderthalb Bildschirme früher · WB_JS «Zurück zur Werkbank» an dieselbe Stelle · KARUSSELL_JS Karusselle vorab."""
VORLADEN_JS = ('<script id="rh-vorladen">(function(){if(!("IntersectionObserver" in window))return;(window.requestIdleCallback||function(f){setTimeout(f,700)})(function(){'
               'var kand=[].slice.call(document.querySelectorAll(".band,.aga-reihe,.vh-felder,.ins-dev,.lu-seiten,[class*=reihe],[class*=zug],[class*=leiste]"));'
               '[].forEach.call(document.querySelectorAll("main *"),function(e){var c=getComputedStyle(e).overflowX;if((c==="auto"||c==="scroll")&&e.scrollWidth>e.clientWidth+4&&kand.indexOf(e)<0)kand.push(e)});'
               'var io=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;io.unobserve(x.target);'
               '[].forEach.call(x.target.querySelectorAll("img[loading=lazy]"),function(i){i.loading="eager"})})},{rootMargin:"120% 0px 120% 0px"});'
               'kand.forEach(function(e){if(e.querySelector("img[loading=lazy]"))io.observe(e)})})})();</script>')

FRUEH_JS = ('<script id="rh-frueh">(function(){if(!("IntersectionObserver" in window))return;'
            'var io=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;io.unobserve(x.target);x.target.loading="eager"})},{rootMargin:"0px 0px 150% 0px"});'
            '[].forEach.call(document.querySelectorAll("main img[loading=lazy],body>section img[loading=lazy],section img[loading=lazy]"),function(i){io.observe(i)})})();</script>')

WB_JS = r'''<script id="rh-zurueck">(function(){
var WEB=/^\/(?:(?:index|abend|abende|bar|leute|weg|dirty-chicken|impressum|datenschutz|termine-pflege|404)\.html)?$/;   /* die Seiten der Website von Culinarium: dort nie ein Weg zurück (Memory «Zur Werkbank») */
function ziel(a){try{var u=new URL(a.getAttribute('href'),location.href);if(!/^https?:$/.test(u.protocol))return null;
 if(/\.pdf$/i.test(u.pathname))return null;
 if(u.origin===location.origin){if(u.pathname===location.pathname)return null;if(WEB.test(u.pathname))return null;return u}
 if(/^127\.0\.0\.1$|localhost/.test(u.hostname)&&/_werkzeuge\//.test(u.pathname))return u;return null}catch(e){return null}}
function merk(ev){var a=ev.target.closest&&ev.target.closest('a[href]');if(!a)return;var u=ziel(a);if(!u)return;var y=Math.round(scrollY);
 if(u.origin!==location.origin&&/_werkzeuge\//.test(u.pathname)){var sk=a.closest('section[id]');u.searchParams.set('wb','de'+(sk&&/^[a-z0-9-]{1,40}$/.test(sk.id)?'.'+sk.id:''));u.searchParams.set('wy',y);u.searchParams.set('wbo',location.origin)}else u.searchParams.set('wb',y);a.href=u.toString();try{sessionStorage.setItem('wb-y',String(y))}catch(e){}
 if(ev.type!=='click'||ev.defaultPrevented||ev.metaKey||ev.ctrlKey||ev.shiftKey)return;
 /* Robert 19.10.2026 01:18 / Endprüfung: nur die sieben Werkzeuge (mit Anleitungen) öffnen einen neuen Tab, den «Zurück zur Werkbank» wieder schliesst;
    Analyse, Drucksachen, Unterlagen, Mappe und die übrigen Beigaben im selben Tab, Safari-Zurück und der Knopf landen an der Stelle */
 var werkzeug=/^\/(?:maison|studio|_?werkzeuge)\//.test(u.pathname);
 ev.preventDefault();if(werkzeug)window.open(a.href,'_blank');else location.href=a.href}
document.addEventListener('click',merk,true);document.addEventListener('auxclick',merk,true);
var q=new URLSearchParams(location.search),y=q.get('y'),zur=false;
try{var nav=performance.getEntriesByType('navigation')[0];if(y===null&&nav&&nav.type==='back_forward'){y=sessionStorage.getItem('wb-y');zur=true}}catch(e){}
if(y===null||!/^\d+$/.test(y))return;y=+y;
try{history.scrollRestoration='manual'}catch(e){}
var st=document.createElement('style');st.textContent='html.wb-sofort,html.wb-sofort *{transition:none!important;animation-duration:0s!important;animation-delay:0s!important;scroll-behavior:auto!important}';document.head.appendChild(st);
document.documentElement.classList.add('wb-sofort');
function fertigOben(){var grenze=y+innerHeight*.15;[].forEach.call(document.querySelectorAll('[data-a],.odo,.zt,.roll,img.ld'),function(e){var r=e.getBoundingClientRect();if(r.top+scrollY<grenze&&!e.classList.contains('da')){e.classList.add('da')}})}
function geh(){window.scrollTo(0,y);fertigOben()}
function los(){geh();requestAnimationFrame(function(){geh();requestAnimationFrame(function(){document.documentElement.classList.remove('wb-sofort')})});
 var n=0,t=setInterval(function(){n++;if(Math.abs(scrollY-y)>40&&n<12&&!wegd)geh();if(n>=12)clearInterval(t)},150);
 if(!zur){q.delete('y');history.replaceState(history.state,'',location.pathname+(q.toString()?'?'+q:'')+location.hash)}}
var wegd=false;['wheel','touchstart','keydown'].forEach(function(k){addEventListener(k,function(){wegd=true},{once:true,passive:true})});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',los);else los();
addEventListener('load',function(){if(!wegd&&Math.abs(scrollY-y)>40)geh()});
})();</script>'''

KARUSSELL_JS = ('<script id="rh-karussell">(function(){var K=[].slice.call(document.querySelectorAll("#register .rgw,[data-wfa],[data-rgw]"));if(!K.length)return;'
                'function hol(k){[].forEach.call(k.querySelectorAll("img"),function(i){try{i.fetchPriority="high"}catch(e){}i.loading="eager";if(i.decode)i.decode().catch(function(){})})}'
                'if(!("IntersectionObserver" in window)){K.forEach(hol);return}'
                'var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){io.unobserve(x.target);hol(x.target)}})},{rootMargin:"300% 0px 300% 0px"});'
                'K.forEach(function(k){io.observe(k)})})();</script>')

