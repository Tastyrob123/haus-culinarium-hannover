// Culinarium · Station 05 · Prüfaufnahmen (nur _qa), unsichtbar, eine Browser-Instanz nach der anderen. Aufruf: node pruefung.js chromium|webkit
const path=require('path'),os=require('os');module.paths.push(path.join(os.homedir(),'Aussen-Pruefung','node_modules'));
const pw=require('playwright');
const B='http://127.0.0.1:8978/haus/'+encodeURIComponent('Culinarium Hannover')+'/_kette/05-markenbauer/marke/';
const Q=path.join(__dirname,'..','_qa');const art=process.argv[2]||'chromium';
(async()=>{const b=await pw[art].launch();const fehler=[];const bericht=[];
 const neu=async(w,h,m)=>{const c=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:m||1});const p=await c.newPage();
   p.on('console',x=>{if(x.type()==='error')fehler.push(w+' '+x.text())});p.on('pageerror',e=>fehler.push(w+' '+String(e)));
   p.on('response',r=>{if(r.status()>=400)fehler.push(r.status()+' '+r.url())});p.on('requestfailed',r=>fehler.push('fehlgeschlagen '+r.url()));return p};
 const alle=async p=>{await p.evaluate(async()=>{document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager');for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,90))}scrollTo(0,0);
   document.querySelectorAll('[data-a],[data-r],[data-g],.paar,.hz').forEach(e=>e.classList.add('da'))});await p.waitForTimeout(3000);await p.waitForFunction(()=>[...document.images].every(i=>i.complete),null,{timeout:20000}).catch(()=>{})};
 const pruef=async(p,n)=>{const r=await p.evaluate(()=>{const kaputt=[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src.split('/').pop());
   const breit=document.documentElement.scrollWidth-innerWidth;const ueber=[...document.querySelectorAll('body *')].filter(e=>{const q=e.getBoundingClientRect();return q.width>0&&(q.right>innerWidth+1)&&getComputedStyle(e).position!=='fixed'&&!e.closest('.faecher,.leiste__k,.welt-wahl')}).slice(0,6).map(e=>e.tagName+'.'+String(e.className).slice(0,30));
   const fonts=[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family);return {kaputt,breit,ueber,fonts:[...new Set(fonts)]}});bericht.push(n+' '+JSON.stringify(r))};
 const seiten=[['markenbuch.html','mb'],['probe.html','probe-a'],['probe.html?welt=b','probe-b'],['logo-richtig-falsch/index.html','rf']];
 for(const [w,h,m] of [[1440,900,1],[390,844,1]]){const p=await neu(w,h,m);
   for(const [u,n] of seiten){await p.goto(B+u,{waitUntil:'networkidle'});await alle(p);await pruef(p,art+' '+w+' '+n);
     await p.screenshot({path:path.join(Q,art+'-'+w+'-'+n+'.jpg'),fullPage:true,quality:60});}
   await p.context().close();}
 console.log(bericht.join('\n'));console.log('fehler:',JSON.stringify(fehler));await b.close()})();
