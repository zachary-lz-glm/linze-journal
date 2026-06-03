const CACHE_NAME = 'kb-v38';
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

  // HTML 永远走网络，不缓存，push 后手机刷新即更新
  if (url.pathname.endsWith('/') || url.pathname.endsWith('.html')) {
    e.respondWith(
      fetch(e.request)
        .then(r => { const c = r.clone(); caches.open(CACHE_NAME).then(cache => cache.put(e.request, c)); return r; })
        .catch(() => caches.match(e.request).then(c => c || new Response('Offline', { status: 503 })))
    );
    return;
  }

  // 非 HTML 资源走 network-first + 超时回退缓存
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
