# 결과 페이지 전용 카드 AI 채팅 컴포넌트

- **ID**: 021
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
새 `component.card.chat` 컴포넌트 생성 — 타로 결과 페이지에서 뽑은 카드 정보를 기반으로 AI에게 추가 질문할 수 있는 인라인 채팅. 기존 routerLink="/Lchat/user" 버튼(범용 루카리오 채팅으로 이동)을 대체.

## 변경 파일 목록

### 신규 생성: component.card.chat
- `component.card.chat/app.json`: component 모드, controller: base, 셀렉터 wiz-component-card-chat
- `component.card.chat/view.ts`: @Input cardData, 토글 열기/닫기, 대화 히스토리, wiz.call('chat') 호출
- `component.card.chat/view.pug`: 토글 버튼 + 채팅 패널(header/body/footer), typing indicator
- `component.card.chat/view.scss`: 보라색 테마, 400px 고정 높이 패널, 메시지 버블
- `component.card.chat/api.py`: Gemini 2.5 Flash, 카드 컨텍스트 포함 시스템 프롬프트, 20초 타임아웃

### 수정: 5개 결과 페이지
- `page.page.tarot/view.ts`: cardData getter 추가 (cardName, isReversed)
- `page.page.tarot/view.pug`: routerLink 버튼 → wiz-component-card-chat 태그
- `page.fifth/view.ts`: cardData getter 추가 (cardInfo 기반)
- `page.fifth/view.pug`: routerLink 버튼 → wiz-component-card-chat 태그
- `page.fourth/view.ts`: cardData getter 추가 (finalCards 기반, 다중 카드+label)
- `page.fourth/view.pug`: routerLink 버튼 → wiz-component-card-chat 태그
- `page.monthly/view.ts`: cardData getter 추가 (result + selectedReversed)
- `page.monthly/view.pug`: routerLink 버튼 → wiz-component-card-chat 태그
- `page.page.tarotw/view.ts`: cardData getter 추가 (finalResults 기반, season label)
- `page.page.tarotw/view.pug`: routerLink 버튼 → wiz-component-card-chat 태그
