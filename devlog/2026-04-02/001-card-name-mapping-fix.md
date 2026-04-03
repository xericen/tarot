# 타로 카드 이름↔이미지 매핑 통일

- **ID**: 001
- **날짜**: 2026-04-02
- **유형**: 버그 수정

## 작업 요약
3개의 서로 다른 DB 테이블(cards, tarot_cards, p_cards)에 저장된 카드 이름이 실제 이미지(0~77.jpg)와 불일치하여 King 카드가 Queen으로 표시되는 문제 수정. 이미지 파일과 정확히 일치하는 검증된 TAROT_CARDS 정적 리스트를 모든 페이지에 추가하여 DB 의존을 제거함.

## 변경 파일 목록

### 카드 이름 매핑 통일
- `src/app/page.page.tarot/api.py`: TAROT_CARDS 리스트 추가, DB Cards 조회 대신 리스트 인덱싱 사용
- `src/app/page.fourth/api.py`: TAROT_CARDS 리스트 추가, DB p_cards 조회 대신 리스트 인덱싱 사용
- `src/app/page.fifth/api.py`: TAROT_CARDS 리스트 추가, DB tarot_cards 조회(+1 오프셋) 대신 리스트 인덱싱 사용
- `src/app/page.monthly/api.py`: TAROT_CARDS 리스트 추가, DB tarot_cards 조회(+1 오프셋) 대신 리스트 인덱싱 사용

## 검증 내역
- TarotCard/0~77.jpg 이미지 전수 확인 (코트카드 16장 집중 검증)
- 모든 이미지가 표준 RWS 순서(Page→Knight→Queen→King)와 일치 확인
- TAROT_CARDS 리스트와 page.page.tarotw의 기존 리스트 동일성 확인
