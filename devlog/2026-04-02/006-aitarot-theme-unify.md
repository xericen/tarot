# AItarot 페이지 테마 통일

- **ID**: 006
- **날짜**: 2026-04-02
- **유형**: 리팩토링

## 작업 요약
page.second(`/AItarot/:id?`)의 디자인을 다른 타로 페이지와 동일한 보라색 그라디언트 테마로 전면 변경. 인라인 스타일 제거 후 BEM 네이밍 기반 SCSS로 전환.

## 변경 파일 목록

### page.second (AItarot)
- `view.pug`: 인라인 스타일 전면 제거, BEM 클래스(`.aitarot__*`) 구조로 재작성. 히어로 + 리더 카드 + 관련 페이지(wiz-component-related) 구조
- `view.scss`: `:host` 블록 추가, 보라색 그라디언트 배지/타이틀/버튼, 카드형 리더 소개 UI, 다른 타로 페이지와 동일한 max-width(480px)/배경색(#f7f7fb)/그라디언트 컬러 체계 적용
