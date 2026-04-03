# [랜덤 타로] Step 2 UI 간소화 + 연도 동적화 + 카드 이미지 개선

- **ID**: 005
- **날짜**: 2026-03-31
- **유형**: 기능 추가

## 작업 요약
연간 타로(page.page.tarotw)에 Season 카드와 동일한 Step 2 UI 간소화를 적용하고, 연도를 동적으로 표시하며, 카드 이미지에 object-fit을 추가하여 전체 이미지가 보이도록 개선.

## 변경 파일 목록
- `src/app/page.page.tarotw/view.pug`: 히어로/폼을 Step 1에서만 표시, 사용자 요약 바 추가, 연도를 currentYear로 동적 변경
- `src/app/page.page.tarotw/view.ts`: currentYear 프로퍼티 추가
- `src/app/page.page.tarotw/view.scss`: 사용자 요약 스타일 추가, 카드에 object-fit: cover 추가
