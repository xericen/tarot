# [오늘의 타로] AI 운세 결과를 구조화된 항목으로 개선

- **ID**: 002
- **날짜**: 2026-03-31
- **유형**: 기능 추가

## 작업 요약
오늘의 타로(page.fifth) 페이지의 AI 운세 결과를 단순 메시지에서 구조화된 5개 항목(키워드, 오늘의 운세, 행동 가이드, 행운의 색, 행운의 팁)으로 개선했다. Gemini AI 프롬프트를 JSON 응답 형식으로 변경하고, 파싱 로직과 UI를 새로 구성했다.

## 변경 파일 목록
### 백엔드
- `src/app/page.fifth/api.py`: AI 프롬프트를 JSON 응답 형식으로 변경, 응답 파싱 로직 추가, 반환 데이터 구조 확장 (keyword, fortune, guide_good, guide_caution, lucky_color, lucky_tip)

### 프론트엔드
- `src/app/page.fifth/view.ts`: TarotCardInfo 인터페이스 확장, showResult 메서드의 데이터 매핑 업데이트
- `src/app/page.fifth/view.pug`: 결과 화면을 5개 섹션별 카드로 재구성
- `src/app/page.fifth/view.scss`: 결과 섹션 스타일 추가 (.tarot-today__sections, __section, __guide-item 등)
