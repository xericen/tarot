# 시즌 카드 고민 선택 변경 가능하도록 수정

- **ID**: 003
- **날짜**: 2026-04-06
- **유형**: 기능 추가

## 작업 요약
시즌 카드(`page.fourth`)에서 고민 선택 시 즉시 `isLocked = true`가 되어 변경 불가하던 문제를 수정. `onLoveStatusChange()`에서 `isLocked = true` 제거하고, `startCardSelection()`에서만 잠금 처리. select의 `[disabled]` 조건에서도 `isLocked` 제거하여 카드 선택 단계 진입 전까지 고민을 자유롭게 변경 가능.

## 변경 파일 목록
### 프론트엔드
- `src/app/page.fourth/view.ts`: `onLoveStatusChange()`에서 `isLocked = true` 제거
- `src/app/page.fourth/view.pug`: select의 `[disabled]` 조건에서 `isLocked` 제거
