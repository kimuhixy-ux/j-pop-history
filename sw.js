const CACHE_VERSION = "j-pop-history-v9-phase4-adsense-canonical";
const PRECACHE = ["./","./index.html","./about.html","./privacy.html","./manifest.json","./css/style.css","./js/main.js","./js/router.js","./js/data.js","./js/sync.js","./js/config.js","./js/affiliate.js","./js/donate.js","./js/components/artist-card.js","./js/views/timeline.js","./js/views/artists.js","./js/views/artist-detail.js","./js/views/songs.js","./js/views/genres.js","./js/views/relations.js","./js/views/guide.js","./js/views/glossary.js","./js/views/favorites.js","./js/views/stats.js","./js/vendor/d3.v7.min.js","./data/artists.json","./data/genres.json","./data/relations.json","./data/album_guide.json","./data/glossary.json","./icons/icon-192.png","./icons/icon-512.png"];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_VERSION).then(cache => cache.addAll(PRECACHE)));
  self.skipWaiting();
});
self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_VERSION).map(key => caches.delete(key)))));
  self.clients.claim();
});
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET" || new URL(event.request.url).origin !== location.origin) return;
  event.respondWith(fetch(event.request).then(response => {
    const copy = response.clone();
    caches.open(CACHE_VERSION).then(cache => cache.put(event.request, copy));
    return response;
  }).catch(() => caches.match(event.request)));
});
