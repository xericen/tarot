# 타로 결과 하단 챗봇 버튼 추가

- **ID**: 010
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
5개 타로 결과 페이지(일일/연간/시즌/랜덤/월간) 모두에 "AI 타로 리더와 대화하기" 챗봇 버튼 추가. 다시보기 버튼 아래에 보라색-핑크 그라데이션 버튼으로 배치.

## 변경 파일 목록

### 일일 타로 (page.page.tarot)
- `view.pug`: `.tarot-daily__action`에 chat 버튼 추가
- `view.scss`: `.tarot-daily__btn--chat` 스타일 추가

### 연간 타로 (page.page.tarotw)
- `view.pug`: `.tarot-yearly__result-action`에 chat 버튼 추가
- `view.scss`: `.tarot-yearly__btn--chat` 스타일 추가

### 시즌 카드 (page.fourth)
- `view.pug`: `.tarot-season__result-action`에 chat 버튼 추가
- `view.scss`: `.tarot-season__btn--chat` 스타일 추가

### 오늘의 타로 (page.fifth)
- `view.pug`: 결과 영역에 chat 버튼 추가
- `view.scss`: `.tarot-today__btn--chat` 스타일 추가

### 월간 타로 (page.monthly)
- `view.pug`: `.tarot-monthly__result-action`에 chat 버튼 추가
- `view.scss`: `.tarot-monthly__btn--chat` 스타일 추가
