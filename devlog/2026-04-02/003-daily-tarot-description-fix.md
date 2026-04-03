# 일일 타로 결과 설명 미표시 버그 수정

- **ID**: 003
- **날짜**: 2026-04-02
- **유형**: 버그 수정

## 작업 요약
일일 타로에서 카드 뽑기 후 카드 이미지만 표시되고 AI 해석(재정운/애정운/건강운/포커스)이 안 나오는 문제 수정. 로딩 스피너 조건 오류 수정 + AI 실패 시 fallback 데이터 보강.

## 변경 파일 목록
- `src/app/page.page.tarot/view.pug`: 로딩 조건 `isLoading && isCardDrawn` → `isLoading`, 입력 폼 조건에 `!isLoading` 추가
- `src/app/page.page.tarot/view.ts`: drawCard에서 isCardDrawn=false 먼저 설정
- `src/app/page.page.tarot/api.py`: fallback 데이터에 기본 설명 텍스트 추가
