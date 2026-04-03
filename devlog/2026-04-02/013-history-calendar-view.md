# 기록 캘린더 뷰 추가

- **ID**: 013
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
프로필 페이지에 리스트/캘린더 탭 전환 추가. 캘린더 뷰에서 월 단위 네비게이션, 날짜별 기록 표시(보라색 점), 날짜 클릭 시 해당일 기록 상세 표시.

## 변경 파일 목록

### 프로필 페이지 (page.profile)
- `view.pug`: 섹션 헤더에 목록/캘린더 탭 토글, 캘린더 그리드(월 네비게이션+요일 헤더+날짜 셀+점), 날짜 선택 시 상세 카드 목록
- `view.ts`: viewMode, calYear, calMonth, calendarCells, selectedCalDate 상태, setViewMode(), prevMonth(), nextMonth(), selectCalDate(), buildCalendar() 메서드
- `view.scss`: 탭 토글, 캘린더 네비게이션, 7열 그리드, 날짜 셀, 기록 있는 날 캘린더 스타일, 상세 패널 스타일
