// JTech LMS Service Worker — offline caching + background sync
const CACHE = 'jtech-lms-v1';
const ASSETS = [
  '/',
  '/courses/',
  '/offline/',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css',
];

// Install — pre-cache core shell
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).catch(() => {}));
  self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE).map(k => caches.delete(k))
    ))
  );
  self.clients.claim();
});

// Fetch strategy:
// - HTML pages: network-first, fallback to cache, fallback to offline page
// - Static assets / images: cache-first
// - Lesson video files: cache-first for SD downloads (offline study for tier-2/3)
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // HTML navigation
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(req, clone));
        return res;
      }).catch(() => caches.match(req).then(r => r || caches.match('/offline/')))
    );
    return;
  }

  // Video files (for offline download — Tier-2/3 use case)
  if (req.destination === 'video' || url.pathname.includes('/media/videos/')) {
    e.respondWith(
      caches.match(req).then(cached => cached || fetch(req).then(res => {
        // Cache SD videos only (size-conscious)
        if (url.pathname.includes('/videos/sd/')) {
          const clone = res.clone();
          caches.open(CACHE + '-videos').then(c => c.put(req, clone));
        }
        return res;
      }))
    );
    return;
  }

  // Static assets — cache-first
  if (['style', 'script', 'image', 'font'].includes(req.destination)) {
    e.respondWith(
      caches.match(req).then(cached => cached || fetch(req).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(req, clone));
        return res;
      }))
    );
    return;
  }

  // Default: try network, fallback to cache
  e.respondWith(fetch(req).catch(() => caches.match(req)));
});

// Background sync for lesson progress (when offline student comes back online)
self.addEventListener('sync', e => {
  if (e.tag === 'sync-progress') {
    e.waitUntil(syncProgress());
  }
});

async function syncProgress() {
  // Future: replay queued progress updates when back online
  const cache = await caches.open(CACHE + '-progress-queue');
  // Implementation left for v2 — uses IndexedDB queue for offline-taught lessons
}
