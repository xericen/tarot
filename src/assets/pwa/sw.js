/**
 * Season Tarot Service Worker
 * - 정적 자산 precache
 * - 런타임 캐싱: 이미지 (cache-first), API (network-first)
 * - 오프라인 fallback: 캐시된 홈 화면
 */
const VERSION = 'v1.0.0';
const STATIC_CACHE = `season-tarot-static-${VERSION}`;
const RUNTIME_CACHE = `season-tarot-runtime-${VERSION}`;
const IMAGE_CACHE = `season-tarot-image-${VERSION}`;

// 앱 셸: 첫 설치 시 사전 캐싱할 핵심 자산
const PRECACHE_URLS = [
    '/',
    '/assets/pwa/manifest.webmanifest',
    '/assets/pwa/icon-192.png',
    '/assets/pwa/icon-512.png',
    '/assets/pwa/icon.svg',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) =>
            cache.addAll(PRECACHE_URLS).catch(() => {})
        ).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys
                    .filter((k) => !k.endsWith(VERSION))
                    .map((k) => caches.delete(k))
            )
        ).then(() => self.clients.claim())
    );
});

function isImage(req) {
    return req.destination === 'image' ||
        /\.(?:png|jpg|jpeg|webp|gif|svg|ico)$/i.test(new URL(req.url).pathname);
}

function isAPI(url) {
    return url.pathname.startsWith('/wiz/api/') ||
        url.pathname.startsWith('/api/');
}

function isStatic(url) {
    return url.pathname.startsWith('/assets/') ||
        url.pathname.endsWith('.js') ||
        url.pathname.endsWith('.css') ||
        url.pathname.endsWith('.woff') ||
        url.pathname.endsWith('.woff2');
}

self.addEventListener('fetch', (event) => {
    const req = event.request;
    if (req.method !== 'GET') return;

    const url = new URL(req.url);
    if (url.origin !== self.location.origin) return;

    // API: network-first
    if (isAPI(url)) {
        event.respondWith(
            fetch(req).catch(() =>
                caches.match(req).then((r) => r || new Response(
                    JSON.stringify({ code: 503, message: 'offline' }),
                    { headers: { 'Content-Type': 'application/json' } }
                ))
            )
        );
        return;
    }

    // 이미지: cache-first
    if (isImage(req)) {
        event.respondWith(
            caches.open(IMAGE_CACHE).then((cache) =>
                cache.match(req).then((cached) =>
                    cached || fetch(req).then((res) => {
                        if (res && res.status === 200) cache.put(req, res.clone());
                        return res;
                    }).catch(() => cached)
                )
            )
        );
        return;
    }

    // 정적 자산: stale-while-revalidate
    if (isStatic(url)) {
        event.respondWith(
            caches.open(STATIC_CACHE).then((cache) =>
                cache.match(req).then((cached) => {
                    const network = fetch(req).then((res) => {
                        if (res && res.status === 200) cache.put(req, res.clone());
                        return res;
                    }).catch(() => cached);
                    return cached || network;
                })
            )
        );
        return;
    }

    // 페이지(HTML): network-first + offline fallback (앱 셸)
    if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
        event.respondWith(
            fetch(req).then((res) => {
                const copy = res.clone();
                caches.open(RUNTIME_CACHE).then((c) => c.put(req, copy));
                return res;
            }).catch(() =>
                caches.match(req).then((r) => r || caches.match('/'))
            )
        );
        return;
    }

    // 기본: 네트워크
    event.respondWith(
        fetch(req).catch(() => caches.match(req))
    );
});

// 메시지 채널 — 클라이언트에서 SW 업데이트 트리거
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
