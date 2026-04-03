# 카드 셔플 애니메이션 개선

- **ID**: 005
- **날짜**: 2026-04-02
- **유형**: UI 개선

## 작업 요약
모든 타로 카드 선택 페이지의 셔플 애니메이션을 "모이기→섞기→펼치기" 3단계 시퀀스로 개선.

## 변경 파일 목록
- `src/app/page.fifth/view.ts`: isGathering 상태 추가, 3단계 타이머 시퀀스
- `src/app/page.fifth/view.pug`: gathering 클래스 바인딩 추가
- `src/app/page.fifth/view.scss`: gathering/shuffle-stack 키프레임 추가
- `src/app/page.monthly/view.ts`: isGathering 상태 추가, 3단계 타이머 
- `src/app/page.monthly/view.pug`: gathering 클래스 바인딩 추가
- `src/app/page.monthly/view.scss`: gathering/shuffle-stack 키프레임 추가
- `src/app/page.page.tarotw/view.ts`: isShuffleAnimating 상태, 1.2s 타이머
- `src/app/page.page.tarotw/view.pug`: shuffle-animating 클래스 바인딩
- `src/app/page.page.tarotw/view.scss`: grid-shuffle 키프레임 추가
- `src/app/page.fourth/view.ts`: isShuffleAnimating 상태, 1.2s 타이머
- `src/app/page.fourth/view.pug`: shuffle-animating 클래스 바인딩
- `src/app/page.fourth/view.scss`: grid-shuffle 키프레임 추가
