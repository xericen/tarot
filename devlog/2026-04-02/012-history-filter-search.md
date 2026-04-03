# 기록 필터/검색 기능 추가

- **ID**: 012
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
프로필 페이지에 타로 기록 필터링(타입별) 및 카드 이름/요약 텍스트 검색 기능 추가. 프론트엔드 필터링으로 구현됨.

## 변경 파일 목록

### 프로필 페이지 (page.profile)
- `view.pug`: 검색 입력 필드, 타입 필터 버튼(전체/일일/오늘/시즌/연간/월간), filteredHistory 기반 리스트 렌더링
- `view.ts`: searchText, filterType, filteredHistory 상태, filterTypes 배열, setFilterType(), applyFilter() 메서드
- `view.scss`: 검색 입력, 타입 필터 버튼 스타일 추가
