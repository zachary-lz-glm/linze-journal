const CACHE_NAME = 'kb-v25';
const TIMEOUT = 3000;

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== self.location.origin) return;

  e.respondWith(
    new Promise(resolve => {
      const timer = setTimeout(() => {
        caches.match(e.request).then(cached => cached && resolve(cached));
      }, TIMEOUT);

      fetch(e.request).then(response => {
        clearTimeout(timer);
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        }
        resolve(response);
      }).catch(() => {
        clearTimeout(timer);
        caches.match(e.request).then(cached => resolve(cached || new Response('Offline', { status: 503 })));
      });
    })
  );
});
