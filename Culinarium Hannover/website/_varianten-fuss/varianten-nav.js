/* Varianten durchschauen (seit 25.10.2026, Robert: «mit den Pfeiltasten … nicht mit diesen Buttons da unten»).
   Erwartet window.VARIANTEN=[[nr,name],…], window.VNR, window.VORD. ← → wechselt die Seite; man bleibt beim selben Abschnitt. */
(function(){
var L=window.VARIANTEN||[],N=window.VNR||0,O=window.VORD||'';if(!L.length)return;
var $$=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))};
function stelle(){var mitte=innerHeight/2,best=null;$$('section[id],header[id]').forEach(function(s){var r=s.getBoundingClientRect();if(r.top<=mitte&&r.bottom>mitte)best=s});
 return best?{id:best.id,off:scrollY-(best.getBoundingClientRect().top+scrollY)}:{y:scrollY}}
addEventListener('keydown',function(ev){
 if(ev.metaKey||ev.ctrlKey||ev.altKey||ev.shiftKey)return;var t=ev.target;if(t&&(t.isContentEditable||/INPUT|TEXTAREA|SELECT/.test(t.tagName)))return;
 var d=ev.key==='ArrowRight'?1:ev.key==='ArrowLeft'?-1:0;if(!d)return;ev.preventDefault();
 var i=-1;L.forEach(function(x,j){if(x[0]===N)i=j});var z=L[(i+d+L.length)%L.length][0];
 try{sessionStorage.setItem('vnav-stelle',JSON.stringify(stelle()))}catch(e){}
 location.href=O+'/'+String(z).padStart(2,'0')+'.html'});
var st=null;try{st=JSON.parse(sessionStorage.getItem('vnav-stelle')||'null');sessionStorage.removeItem('vnav-stelle')}catch(e){}
if(st){if('scrollRestoration' in history)history.scrollRestoration='manual';
 var hin=function(){var y=st.y;if(st.id){var s=document.getElementById(st.id);if(s)y=s.getBoundingClientRect().top+scrollY+st.off}if(y!=null)window.scrollTo({top:y,behavior:'instant'})};
 hin();[80,300,800,1500].forEach(function(ms){setTimeout(hin,ms)})}
})();
