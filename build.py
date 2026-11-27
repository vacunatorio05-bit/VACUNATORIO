import json,re,sys
src=open('src/app.html').read()
VER=__import__('hashlib').sha1(src.encode()).hexdigest()[:10]
head='''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0d6b6e">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="manifest" href="manifest.json">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}</style>
</head><body>
'''
tail='''
<script>
if("serviceWorker" in navigator){ window.addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{})); }
</script>
</body></html>
'''
open('index.html','w').write(head+src+tail)
json.dump({"name":"Vacunatorio Tres Cerritos","short_name":"Vacunatorio","lang":"es-AR","start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":"#f3f6f5","theme_color":"#0d6b6e",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any maskable"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]},open('manifest.json','w'),ensure_ascii=False,indent=1)
open('sw.js','w').write('''// Funciona sin internet: guarda la app, las librerías y los pedazos de mapa ya vistos.
const APP="vacunatorio-%s", TILES="mapa-tiles-v1", MAX_TILES=3000;
const ARCHIVOS=["./","index.html","manifest.json","icon-192.png","icon-512.png",
 "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js",
 "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js",
 "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"];
self.addEventListener("install",e=>{ e.waitUntil(caches.open(APP).then(c=>Promise.all(ARCHIVOS.map(u=>c.add(u).catch(()=>{}))))); self.skipWaiting(); });
self.addEventListener("activate",e=>{ e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==APP&&k!==TILES).map(k=>caches.delete(k))))); self.clients.claim(); });
async function recortar(){ const c=await caches.open(TILES); const ks=await c.keys(); for(let i=0;i<ks.length-MAX_TILES;i++) await c.delete(ks[i]); }
self.addEventListener("fetch",e=>{
  const u=new URL(e.request.url); if(e.request.method!=="GET") return;
  if(u.hostname.endsWith("tile.openstreetmap.org")){
    e.respondWith(caches.open(TILES).then(async c=>{ const hit=await c.match(e.request); if(hit) return hit;
      try{ const r=await fetch(e.request); if(r.ok){ c.put(e.request,r.clone()); recortar(); } return r; }catch(_){ return new Response("",{status:504}); } }));
    return;
  }
  if(e.request.mode==="navigate"){ e.respondWith(fetch(e.request).then(r=>{ const cp=r.clone(); caches.open(APP).then(c=>c.put("index.html",cp)); return r; }).catch(()=>caches.match("index.html"))); return; }
  e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(r=>{ if(r.ok&&(u.origin===location.origin||u.hostname==="cdnjs.cloudflare.com")){ const cp=r.clone(); caches.open(APP).then(c=>c.put(e.request,cp)); } return r; })));
});
'''%VER)
print("ok",VER)
