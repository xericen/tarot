# [프로필] 세션 인증, 프로필 페이지, 타로 기록 DB 구현

- **ID**: 008
- **날짜**: 2026-03-31
- **유형**: 기능 추가

## 작업 요약
로그인 시 세션 설정, 프로필 페이지 생성, 타로 조회 기록 저장 기능을 전체적으로 구현. 네비게이션에 로그인 상태 표시 추가.

## 변경 파일 목록

### DB
- `src/model/db/login/tarot_history.py`: 타로 기록 DB 모델 (user_id, tarot_type, cards, result_summary, created_at)
- MySQL `login.tarot_history` 테이블 생성

### 인증/세션
- `page.login/api.py`: 로그인 시 `session.set(id, name, email)` 추가, `logout()` 함수 추가

### 네비게이션
- `component.nav/api.py`: (신규) 세션 체크 API
- `component.nav/view.ts`: 로그인 상태 확인 후 사용자명 표시
- `component.nav/view.pug`: 로그인 시 이름+프로필 링크, 비로그인 시 로그인 아이콘 표시
- `component.nav/view.scss`: 사용자 표시 스타일 추가
- `component.nav/app.json`: controller "base" 추가, title input 제거

### 프로필 페이지 (신규)
- `page.profile/app.json`: 페이지 설정
- `page.profile/view.ts`: 프로필 데이터 로드 + 로그아웃
- `page.profile/view.pug`: 사용자 정보 + 타로 기록 목록
- `page.profile/view.scss`: 토스 스타일 프로필 UI
- `page.profile/api.py`: 프로필 조회 (사용자 정보 + 타로 기록 50건)

### 타로 API (기록 저장 추가)
- `page.fifth/api.py`: 오늘의 타로 결과 저장 (type: today)
- `page.fourth/api.py`: Season 카드 결과 저장 (type: season)
- `page.page.tarot/api.py`: 일일 타로 결과 저장 (type: daily)
- `page.page.tarotw/api.py`: 연간 타로 결과 저장 (type: yearly)
