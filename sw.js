// Funciona sin internet: guarda la app, las librerías y los pedazos de mapa ya vistos.
const APP="vacunatorio-61fcae8ce2", TILES="mapa-tiles-v1", MAX_TILES=3000;
const ARCHIVOS=["./","index.html","manifest.json","icon-192.png","icon-512.png","icon-maskable-512.png","carnet/ninos-1.jpg","carnet/ninos-2.jpg","carnet/adultos-1.jpg","carnet/adultos-2.jpg",
 "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js",
 "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js",
 "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js",
 "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css",
 "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js","https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"];
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
  if(e.request.mode==="navigate"){ e.respondWith(fetch(e.request.url,{cache:"no-cache"}).then(r=>{ const cp=r.clone(); caches.open(APP).then(c=>c.put("index.html",cp)); return r; }).catch(()=>caches.match("index.html"))); return; }
  e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(r=>{ if(r.ok&&(u.origin===location.origin||u.hostname==="cdnjs.cloudflare.com")){ const cp=r.clone(); caches.open(APP).then(c=>c.put(e.request,cp)); } return r; })));
});
