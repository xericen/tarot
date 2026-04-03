# [전체 UI] 모바일 최적화 — 네비게이션 심플화, 레이아웃 정리, 히어로 조건부 표시

- **ID**: 006
- **날짜**: 2026-03-31
- **유형**: 리팩토링

## 작업 요약
전체 페이지에서 불필요한 헤더/네비게이션 요소를 제거하고 토스 스타일의 심플한 모바일 레이아웃으로 개선. Bootstrap 기반 navgar를 커스텀 미니멀 네비게이션으로 교체하고, 레이아웃 구조를 flex 기반으로 리팩토링.

## 변경 파일 목록

### component.nav (네비게이션 컴포넌트)
- `view.pug`: Bootstrap navbar(메뉴, 드롭다운, 검색바, 로그인 버튼) 전체 제거 → 로고+브랜드명+유저아이콘 미니멀 헤더로 교체
- `view.scss`: Bootstrap 의존 스타일 제거 → 커스텀 `.app-nav` BEM 스타일 적용
- `view.ts`: `@Input() title`, 검색 로직 제거 → 최소 컴포넌트로 경량화

### layout.navbar (레이아웃)
- `view.pug`: 인라인 스타일 wrapper 제거 → `.app-layout` flex 구조로 변경
- `view.scss`: `:host` flex 레이아웃 + `.app-content` overflow-y 스크롤 영역 설정

### page.main (메인 페이지)
- `view.pug`: "2025년" 하드코딩 → `{{ currentYear }}년` 동적 연도로 변경
- `view.ts`: `currentYear` 프로퍼티 추가

### page.page.tarot (일일 타로)
- `view.pug`: 히어로 섹션에 `*ngIf="!isCardDrawn"` 추가 — 결과 표시 시 히어로 숨김
