const CACHE = "calcpro-v1";
const FILES = ["/", "/index.html", "/install.html", "/css/style.css", "/css/install.css",
  "/js/calculator.js", "/js/app.js", "/js/install.js", "/js/sw.js", "/manifest.json",
  "/icons/icon-192.png", "/icons/icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request).then(h => h || fetch(e.request).catch(() => caches.match("/index.html"))));
});
