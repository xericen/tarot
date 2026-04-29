# PWA(설치형 모바일 앱) 전환

- **ID**: 001
- **날짜**: 2026-04-29
- **유형**: 기능 추가

## 작업 요약

Season Tarot을 PWA로 전환. 매니페스트, 아이콘 셋, Service Worker, 설치 프롬프트 UI를 통합하여 모바일 홈 화면 설치와 오프라인 동작이 가능한 설치형 웹앱으로 업그레이드.

## 변경 파일 목록

### 신규 자산 (PWA)
- `src/assets/pwa/icon.svg` — 보라색+골드 타로 컨셉 앱 아이콘 (3장 카드 + 별 모티프)
- `src/assets/pwa/icon-192.png` — 192x192 표준 아이콘
- `src/assets/pwa/icon-512.png` — 512x512 표준 아이콘
- `src/assets/pwa/icon-180.png` — iOS apple-touch-icon
- `src/assets/pwa/icon-maskable-512.png` — Maskable 아이콘
- `src/assets/pwa/sw.js` — Service Worker 본문
- `config/pwa/sw.js` — `portal/season/route/pwa.swjs` 라우트가 서빙하는 SW (sw.js 복사본)

### 설정 오버라이드
- `config/season.py` — `pwa_title`/`pwa_theme_color`/`pwa_icon_*` 등 PWA 메타 오버라이드 (기존 `portal/season` 패키지의 manifest 라우트가 이 값을 참조)

### 컴포넌트 (설치 배너)
- `src/app/component.pwa.install/app.json` — 컴포넌트 메타
- `src/app/component.pwa.install/view.ts` — beforeinstallprompt 이벤트 처리, 24h 닫기 기억
- `src/app/component.pwa.install/view.pug` — 하단 플로팅 설치 배너
- `src/app/component.pwa.install/view.scss` — 보라+골드 디자인, 모바일 최적화
- `src/app/component.pwa.install/api.py` — 빈 파일 (배너는 클라이언트 전용)

### HTML 통합
- `src/angular/index.pug` — 매니페스트/theme-color/apple-touch-icon/og 메타 추가, SW 등록 스크립트 추가, beforeinstallprompt 이벤트 핸들러 등록
- `src/angular/app/app.component.pug` — `<wiz-component-pwa-install>` 글로벌 마운트

## 동작 흐름

1. 페이지 로드 → SW 등록(`/sw.js`, scope `/`)
2. 브라우저가 PWA 설치 가능 판단 → `beforeinstallprompt` 이벤트 발생
3. `window.__pwaInstallPrompt`에 캐시 + `pwa:installable` 커스텀 이벤트 디스패치
4. 설치 배너 컴포넌트가 이벤트 수신 → 화면에 노출
5. 사용자가 "설치" 클릭 → `prompt.prompt()` 호출 → 브라우저 네이티브 다이얼로그
6. 설치 완료 → `appinstalled` 이벤트 → 배너 숨김

## 캐싱 전략 (Service Worker)

| 리소스 | 전략 |
|--------|------|
| API (`/wiz/api/*`) | network-first + offline JSON fallback |
| 이미지 | cache-first |
| 정적 자산 (`/assets/*`, `*.js`, `*.css`) | stale-while-revalidate |
| HTML 페이지 | network-first + offline fallback to `/` |

## 검증

- `curl http://localhost:3000/sw.js` → 200, 4111 bytes
- `curl http://localhost:3000/manifest.json` → 200, JSON (Season Tarot, #2A1B4E)
- HTML `<head>`에 manifest/theme/icon/og 메타 모두 출력 확인
- 모바일 Chrome에서 "홈 화면에 추가" 메뉴 노출 가능 (HTTPS 환경 필수)

## 주의 사항

- **HTTPS 필수**: Service Worker는 localhost를 제외하면 HTTPS에서만 동작
- **기존 라우트 활용**: `portal/season`에 이미 `/sw.js`, `/manifest.json` 라우트가 있어, 신규 라우트 생성 대신 `config/pwa/sw.js` + `config/season.py` 오버라이드로 통합
