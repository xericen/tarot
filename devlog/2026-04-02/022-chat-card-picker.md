# AI 타로 리더 채팅 카드 뽑기 UI 개선

- **ID**: 022
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
component.chat의 카드 뽑기를 서버 랜덤 자동 배정에서 사용자 선택 방식으로 변경. "카드 뽑기" 클릭 시 7장의 뒷면 카드가 표시되고, 사용자가 선택하면 뒤집힌 후 AI 해석 요청.

## 변경 파일 목록

### component.chat
- `view.ts`: pickerCards/pickerReversed/pickerFlipped/pickerSelected 상태 추가. drawCard()에서 7장 셔플하여 picker UI 표시. selectPickerCard()에서 카드 뒤집기 + 800ms 딜레이 후 draw_card API 호출 (card_id, is_reversed 파라미터 전달)
- `view.pug`: chat-card-picker 영역 추가 (7장 뒷면 카드 표시, 클릭시 뒤집기). showDrawButton과 showCardPicker 조건 분리
- `view.scss`: chat-card-picker 스타일 (카드 56px 너비, 호버 이동, 선택시 보라색 테두리)
- `api.py`: draw_card()에서 client_card_id/client_is_reversed 파라미터 수신. 값이 있으면 클라이언트 선택 사용, 없으면 기존 랜덤 유지 (하위 호환)
