# 기록 통계 페이지 추가

- **ID**: 014
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
프로필 페이지에 '통계' 탭 추가. Top 5 카드 랭킹, 슈트별 분포 바 차트, 감정 태그별 카드 패턴 분석, 기간별 필터(전체/1주/1달/3달) 구현.

## 변경 파일 목록

### 프로필 페이지 (page.profile)
- `api.py`: stats() 함수 추가 — card_count, suit_distribution, mood_patterns 통계 계산, 기간 필터
- `view.pug`: 통계 탭 버튼, 기간 필터, 총 리딩 수, Top 카드 랭킹, 슈트별 바 차트, 감정별 패턴
- `view.ts`: statsPeriod/statsData/suitList/moodPatternList 상태, loadStats() 메서드, setViewMode stats 분기
- `view.scss`: 통계 카드, 랭킹 넘버링, 바 차트, 감정 패턴 스타일
