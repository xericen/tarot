# 전체 타로 API 500 에러 수정 + 토스 스타일 모바일 반응형 디자인 적용

- **ID**: 001
- **날짜**: 2026-03-24
- **유형**: 버그 수정 + 디자인 변경

## 작업 요약
4개 타로 페이지(page.fifth, page.fourth, page.page.tarot, page.page.tarotw)에서 발생하는 API 500 에러를 수정하고, 전체 페이지를 토스 스타일 모바일 반응형 디자인으로 전환했다.

## 에러 원인
1. **`google-generativeai` 패키지 미설치** — 모든 API에서 import 실패로 500 에러 발생
2. **`wiz.response.status()` 잘못된 호출 패턴** — dict를 positional arg로 전달하는 대신 kwargs(`data=...`)로 전달해야 함
3. **page.fifth의 `def tarot_result(**params):`** — WIZ api.py 함수는 인자 없이 `def function():` 형태여야 함

## 변경 파일 목록

### 패키지 설치
- `google-generativeai` pip 설치

### API 수정 (4개)
- `src/app/page.fifth/api.py` — 함수 시그니처 수정 + response 패턴 수정
- `src/app/page.fourth/api.py` — response 패턴 수정, unused import 제거
- `src/app/page.page.tarot/api.py` — response 패턴 수정
- `src/app/page.page.tarotw/api.py` — response 패턴 수정

### 프론트엔드 수정
- `src/app/page.fifth/view.ts` — API 응답 처리 간소화 (unwrapPayload 제거)

### 디자인 변경 (토스 스타일 + 모바일 반응형)
- `src/app/page.main/view.pug` — 메뉴 리스트 UI로 전환
- `src/app/page.main/view.ts` — 불필요한 toastr 제거
- `src/app/page.main/view.scss` — 토스 스타일 전체 재작성
- `src/app/page.fifth/view.pug` — BEM 클래스 기반 토스 스타일
- `src/app/page.fifth/view.scss` — 모바일 반응형 + :host 추가
- `src/app/page.fourth/view.pug` — 토스 스타일 폼 + 결과 UI
- `src/app/page.fourth/view.ts` — selectCard/resetSelection에 service.render() 추가
- `src/app/page.fourth/view.scss` — 토스 스타일 + :host 추가
- `src/app/page.page.tarot/view.pug` — 토스 스타일 입력/결과 UI
- `src/app/page.page.tarot/view.scss` — 전체 재작성
- `src/app/page.page.tarotw/view.pug` — 토스 스타일 + 가이드 섹션
- `src/app/page.page.tarotw/view.scss` — 토스 스타일 + 2x2 그리드 슬롯 + :host 추가
- `src/app/component.related/view.pug` — 리스트형 네비게이션으로 변경
- `src/app/component.related/view.scss` — 토스 스타일 리스트 아이템
