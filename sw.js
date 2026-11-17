/* Network first, so every online visit gets the newest version; the cache is only the offline fallback. */
const C = 'pert-guide-v2';
const CORE = ['./', './index.html', './manifest.webmanifest', './icon.svg', './icon-192.png'];
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(CORE))); });
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const ours = r.url.startsWith(self.location.origin), fonts = /fonts\.(googleapis|gstatic)\.com/.test(r.url);
  if (!ours && !fonts) return;
  e.respondWith(
    fetch(r, r.mode === 'navigate' ? { cache: 'no-cache' } : {})
      .then(res => { if (res.ok || res.type === 'opaque') { const cp = res.clone(); caches.open(C).then(c => c.put(r, cp)); } return res; })
      .catch(() => caches.match(r, { ignoreSearch: true }).then(m => m || (r.mode === 'navigate' ? caches.match('./index.html') : Response.error()))));
});
