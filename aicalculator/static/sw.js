const CACHE_NAME = "mathcalc-cache-v1";
const urlsToCache = [
  "/",
  "/static/icon-192.png",
  "/static/icon-512.png",
  "/static/manifest.json"
];

// Install Event - cache app shell
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch Event - serve from cache or network
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
