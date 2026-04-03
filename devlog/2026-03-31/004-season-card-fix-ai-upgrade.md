# [Season 카드 + 전체] 서버 오류 수정, AI 모델 전환, 응답 구조 수정

- **ID**: 004
- **날짜**: 2026-03-31
- **유형**: 버그 수정

## 작업 요약
1. 모든 타로 API의 Google AI 패키지를 `google.generativeai` (deprecated) → `google.genai` (v1.13)로 전환
2. AI 모델을 `gemini-2.0-flash` (서비스 종료) → `gemini-2.5-flash`로 변경
3. 모든 API의 응답 구조 이중 중첩 문제 수정 (`wiz.response.status(200, data={...})` → `wiz.response.status(200, **{...})`)

## 변경 파일 목록
### 백엔드
- `src/app/page.fifth/api.py`: google.genai + gemini-2.5-flash + 응답 구조 수정
- `src/app/page.fourth/api.py`: google.genai + gemini-2.5-flash + 응답 구조 수정
- `src/app/page.page.tarotw/api.py`: google.genai + gemini-2.5-flash + 응답 구조 수정
- `src/app/page.page.tarot/api.py`: google.genai + gemini-2.5-flash + 응답 구조 수정

### 패키지
- `google-genai==1.13.0` 설치 (Python 3.12 호환)
