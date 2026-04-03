# 카드 뒤집힘(리버스) 기능 추가

- **ID**: 002
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
타로 카드 뽑기 시 50% 확률로 역방향(Reversed) 결정 로직을 모든 타로 페이지에 추가. 역방향 카드는 UI에서 180° 회전 + "Reversed" 배지 표시. AI 프롬프트에 역방향 의미 반영하여 해석 차별화.

## 변경 파일 목록

### 백엔드 (api.py) - 5개 페이지
- `src/app/page.page.tarot/api.py`: import random 추가, 서버에서 is_reversed 결정, AI 프롬프트에 역방향 지시 추가
- `src/app/page.page.tarotw/api.py`: reversed 파라미터 수신, AI 프롬프트에 역방향 해석 반영
- `src/app/page.fourth/api.py`: reversed 파라미터 수신, _get_ai_fortune_season에 is_reversed 파라미터 추가
- `src/app/page.fifth/api.py`: is_reversed 파라미터 수신, _get_ai_fortune_today에 역방향 반영
- `src/app/page.monthly/api.py`: is_reversed 파라미터 수신, _get_ai_monthly에 역방향 반영

### 프론트엔드 (view.ts) - 4개 페이지 (page.page.tarot는 서버 결정)
- `src/app/page.page.tarot/view.ts`: isReversed 프로퍼티 추가, API 응답에서 is_reversed 수신
- `src/app/page.page.tarotw/view.ts`: reversedCards 배열 추가, 선택 시 리버스 상태 저장, API에 reversed 전달
- `src/app/page.fourth/view.ts`: reversedCards/selectedReversed 추가, API에 reversed 전달
- `src/app/page.fifth/view.ts`: reversedCards 추가, 선택 시 리버스 결정, API에 is_reversed 전달
- `src/app/page.monthly/view.ts`: reversedCards 추가, 선택 시 리버스 결정, API에 is_reversed 전달

### UI (view.pug + view.scss) - 5개 페이지
- `src/app/page.page.tarot/view.pug`: [class.reversed] 바인딩, Reversed 배지 추가
- `src/app/page.fifth/view.pug`: [class.reversed] 바인딩, Reversed 배지 추가
- `src/app/page.monthly/view.pug`: [class.reversed] 바인딩, Reversed 배지 추가
- `src/app/page.fourth/view.pug`: [class.reversed] 바인딩, Reversed 배지 추가
- `src/app/page.page.tarotw/view.pug`: [class.reversed] 바인딩, Reversed 배지 추가
- 5개 view.scss: `.reversed { transform: rotate(180deg); }` + `__reversed-badge` 스타일 추가
