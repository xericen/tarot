# [Season 카드] Step 2 UI 개선 — 카드 선택 화면 간소화

- **ID**: 003
- **날짜**: 2026-03-31
- **유형**: 기능 추가

## 작업 요약
Season 카드(page.fourth) 페이지에서 이름·고민 입력 후 "카드 선택하기"를 누르면 Step 2로 전환되도록 개선. Step 2에서는 상단 SEASON카드 타이틀·이미지·입력폼을 숨기고, "김민주 (사업운)" 형태로 사용자 정보 요약만 표시. 카드가 바로 보이도록 레이아웃 변경.

## 변경 파일 목록
- `src/app/page.fourth/view.pug`: 히어로/폼 섹션에 `!showCards` 조건 추가, 사용자 요약 바(`.tarot-season__user-summary`) 추가
- `src/app/page.fourth/view.scss`: `.tarot-season__user-summary` 스타일 추가, 카드 영역 margin 축소
