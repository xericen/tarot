# [오늘의 타로] 카드 호버 애니메이션 추가

- **ID**: 001
- **날짜**: 2026-03-31
- **유형**: 기능 추가

## 작업 요약
오늘의 타로(page.fifth) 페이지에서 카드에 마우스를 올리면 카드가 살짝 위로 올라가는 호버 애니메이션을 추가했다. 모바일 터치 환경(:active)도 동일하게 지원한다.

## 변경 파일 목록
### 스타일
- `src/app/page.fifth/view.scss`: `.card-wrapper.spread:not(.selected):hover img.card` 및 `:active` 호버 효과 추가 (translateY(-18px) scale(1.06), box-shadow 강화, transition 개선)
