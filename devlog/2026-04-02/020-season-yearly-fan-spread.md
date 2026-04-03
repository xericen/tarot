# 시즌 카드 + 연간 타로 fan-spread UI 변환

- **ID**: 020
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
page.fourth(시즌 카드)와 page.page.tarotw(연간 타로)의 카드 선택 UI를 그리드 레이아웃에서 fan-spread(부채꼴 펼침) 방식으로 변환. gather→shuffle→spread 3단계 애니메이션 적용.

## 변경 파일 목록

### page.fourth (시즌 카드 - 3장 선택)
- `page.fourth/view.ts`: shuffleArray(), shuffleCards()(3단계), getSpreadTransform(), startCardSelection() 추가. isShuffleAnimating → isSpread/isShuffling/isGathering 상태로 변경
- `page.fourth/view.pug`: card-container를 fan-spread 방식으로 변경 (spread/shuffling/gathering 클래스, transitionDelay 적용). "다시 선택하기" 버튼 제거, "카드 섞기"만 유지
- `page.fourth/view.scss`: 그리드 card-container → position:absolute fan-spread. grid-shuffle → shuffle-stack 키프레임. card-wrapper에 spread/gathering/shuffling 상태별 스타일

### page.page.tarotw (연간 타로 - 4장 선택)
- `page.page.tarotw/view.ts`: 동일 패턴 적용 (4장 선택). shuffleArray(), shuffleCards(3단계), getSpreadTransform() 추가
- `page.page.tarotw/view.pug`: 동일 fan-spread 패턴 적용
- `page.page.tarotw/view.scss`: 동일 fan-spread CSS. 반응형 카드 크기 업데이트
