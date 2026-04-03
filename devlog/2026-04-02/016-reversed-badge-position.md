# Reversed 배지 위치 변경 (오른쪽 → 카드 위)

- **ID**: 016
- **날짜**: 2026-04-02
- **유형**: UI 개선

## 작업 요약
모든 타로 결과 페이지에서 Reversed 배지를 카드 이미지 오른쪽에서 위쪽으로 이동.

## 변경 파일 목록
- `page.page.tarot/view.pug`, `view.scss` — 배지를 img 위로 이동
- `page.fifth/view.pug`, `view.scss` — 동일
- `page.fourth/view.pug`, `view.scss` — img-wrap 래퍼 추가, 배지 상단 배치
- `page.monthly/view.pug`, `view.scss` — flex-direction column으로 변경, 배지 상단  
- `page.page.tarotw/view.pug`, `view.scss` — img-wrap 래퍼 추가, 배지 상단
- `component.chat/view.pug`, `view.scss` — 배지를 img 위로 이동, 색상 통일
