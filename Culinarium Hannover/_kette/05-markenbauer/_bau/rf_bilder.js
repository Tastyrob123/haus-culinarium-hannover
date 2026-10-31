// Bilder für «Logo richtig und falsch» (marke/logo-richtig-falsch/*.png), aus der Seite selbst, unsichtbar.
const path=require('path'),os=require('os');module.paths.push(path.join(os.homedir(),'Aussen-Pruefung','node_modules'));
const pw=require('playwright');const RF=path.join(__dirname,'..','marke','logo-richtig-falsch');
(async()=>{const b=await pw.chromium.launch();const p=await (await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:2})).newPage();
await p.goto('http://127.0.0.1:8978/haus/'+encodeURIComponent('Culinarium Hannover')+'/_kette/05-markenbauer/marke/logo-richtig-falsch/index.html',{waitUntil:'networkidle'});
await p.evaluate(()=>document.querySelectorAll('[data-r],[data-g]').forEach(e=>e.classList.add('da')));await p.waitForTimeout(2500);
const karten=await p.$$('.regel');let i=0;
for(const k of karten){const t=await k.$eval('h3',h=>h.textContent);const art=await k.evaluate(e=>e.classList.contains('regel--f')?'falsch':'richtig');
 const n=art+'-'+t.toLowerCase().replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
 await (await k.$('.regel__f')).screenshot({path:path.join(RF,n+'.png')});i++}
console.log(i,'Bilder');await b.close()})();
