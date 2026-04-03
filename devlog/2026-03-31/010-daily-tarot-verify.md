# [일일 타로] 이미지/메시지 표시 검증 완료

- **ID**: 010
- **날짜**: 2026-03-31
- **유형**: 검증

## 작업 요약
일일 타로(page.page.tarot) 카드 이미지 미표시 및 메시지 없음 문제를 점검. 핵심 원인인 API 응답 이중 래핑 (`data={...}` → `**{...}`)은 FN-0004에서 이미 수정되어 정상 동작 확인. 히어로 조건부 표시도 FN-0006에서 적용됨.

## 검증 내역
- API: `wiz.response.status(200, card_id=..., card_name=..., message=..., image_url=...)` 정상 반환
- 프론트엔드: `data.card_name`, `data.message`, `data.image_url` 직접 접근 확인
- 이미지 파일: `bundle/src/assets/TarotCard/` 에 0.jpg ~ 77.jpg (78장) 존재 확인
- 히어로: `*ngIf="!isCardDrawn"` 조건으로 결과 표시 시 숨김 (FN-0006)
