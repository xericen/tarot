# 시즌 카드 AI 해석 시간 최적화

- **ID**: 017
- **날짜**: 2026-04-02
- **유형**: 성능 최적화

## 작업 요약
page.fourth(시즌 카드) API에서 Gemini 4회 순차 호출(3장 운세 + 1회 총평)을 1회 통합 프롬프트로 변경하여 응답 시간 약 75% 단축.

## 변경 파일 목록
- `src/app/page.fourth/api.py`: `_get_ai_fortunes_combined()` 함수 추가, `tarot_draw_three()` 리팩토링
