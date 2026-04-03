# 일일 타로 카드선택 UI 변경

- **ID**: 018
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
일일 타로(page.page.tarot)를 이름 입력 → 카드 자동 배정 방식에서 fan-spread 카드 선택 방식으로 변경.

## 변경 파일 목록
- `src/app/page.page.tarot/view.pug` — fan-spread 카드 선택 영역 추가
- `src/app/page.page.tarot/view.ts` — shuffleCards/selectCard/showFortune 로직 추가
- `src/app/page.page.tarot/view.scss` — card-container/wrapper/slot 스타일 추가
- `src/app/page.page.tarot/api.py` — card_id/is_reversed 파라미터 수신 추가
