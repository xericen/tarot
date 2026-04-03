# 10건 일괄 개선 (로그인 로고, 페이지네이션, 히어로 이모지, 카드방향, 채팅, 다시보기, 애니메이션, 78장 피커)

- **ID**: 001
- **날짜**: 2026-04-03
- **유형**: 기능 추가 / 버그 수정

## 작업 요약
10개 요구사항을 일괄 구현: 로그인 페이지 로고 이미지 교체, 타로 기록 페이지네이션(5개/페이지), 5개 타로 페이지 히어로 이모지 아이콘, 카드 방향 불일치 수정, 채팅 입력/전송 버그 수정, 다시보기 change detection 수정, 좌→우 순차 카드 펼침 애니메이션, 셔플 riffle 애니메이션 개선, AI 78장 수평 스크롤 카드 피커.

## 변경 파일 목록

### 로그인 로고 (FN-0001)
- `page.login/view.pug` — h1 텍스트 → img.login-card__logo(seasontarot.png)
- `page.login/view.scss` — .login-card__logo 스타일 추가 (180px)

### 페이지네이션 (FN-0002)
- `page.profile/view.ts` — currentPage, pageSize=5, totalPages/paginatedHistory/pageNumbers getter, goToPage(), onSearchChange()
- `page.profile/view.pug` — paginatedHistory *ngFor, 페이지 버튼 UI
- `page.profile/view.scss` — .profile__pagination, __page-btn 스타일

### 히어로 이모지 (FN-0003)
- 5개 타로 페이지 view.pug — __hero-img img → __hero-icon span.__hero-emoji
- 5개 타로 페이지 view.scss — __hero-img → __hero-icon/__hero-emoji 스타일

### 카드 방향 (FN-0004)
- page.fifth/fourth/monthly/page.tarotw view.pug — [class.reversed] 바인딩 추가 (팬스프레드 + 슬롯)
- 4개 페이지 view.scss — img.card.reversed, slot img.reversed transform: rotate(180deg)

### 채팅 버그 (FN-0005)
- component.chat/view.ts — inputText='' → service.render() → nativeElement.value=''
- component.chat/view.pug — #chatInput ref, [disabled]="isLoading"
- component.card.chat/view.ts, view.pug — 동일 패턴 적용

### 다시보기 (FN-0006)
- 4개 타로 페이지 view.pug — userName input에 (input)="service.render()" 추가

### 순차 펼침 (FN-0007)
- 4개 타로 페이지 view.pug — transitionDelay i*0.025
- 4개 타로 페이지 view.scss — .card-wrapper transition 0.5s

### 셔플 (FN-0008)
- 4개 타로 페이지 view.scss — @keyframes shuffle-riffle (10단계, 1s)
- 4개 타로 페이지 view.ts — setTimeout 1000ms

### 78장 피커 (FN-0009)
- component.chat/view.ts — 78장 allCards, 후속 메시지 추가
- component.chat/view.pug — .chat-card-picker__scroll 수평 스크롤
- component.chat/view.scss — overflow-x: auto, 44×66px 카드, scrollbar 스타일
