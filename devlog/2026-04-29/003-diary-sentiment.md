# 다이어리 + AI 감정 분석

- **ID**: 003
- **날짜**: 2026-04-29
- **유형**: 기능 추가

## 작업 요약
사용자가 일상을 기록하면 **Gemini AI가 자동으로 감정을 분석**해 카테고리(joy/sad/angry/anxious/calm/excited/neutral)·점수(-1.0~1.0)·1줄 요약을 생성해주는 다이어리 기능을 구현. 작성·목록·상세·수정·삭제·통계까지 단일 SPA 페이지(`/diary`)에서 모드 토글로 처리. 타로 히스토리와 양방향 연결(다이어리 작성 시 최근 타로 기록 선택 가능).

## 변경 파일 목록

### DB 마이그레이션
- **MySQL `tarot.diary` 테이블 신규 생성**:
  - `diary_id BIGINT PK AI`, `user_id`, `diary_date`, `title`, `content`, `mood`, `sentiment`, `sentiment_score FLOAT`, `ai_summary`, `related_draw_id`, `created_at`, `updated_at`
  - 인덱스: `idx_user`, `idx_date`, `idx_user_date`
- **신규** `src/model/db/tarot/diary.py`: Peewee 스키마

### 백엔드 (page.diary/api.py)
- **신규** `src/app/page.diary/api.py`:
  - `list()`: 사용자별 다이어리 페이지네이션 + 관련 타로 히스토리 조인
  - `get(diary_id)`: 단건 조회 + 관련 타로 상세
  - `list_recent_tarot()`: 작성 시 연결할 최근 타로 20건
  - `save()`: 신규/수정 통합. 저장 시 `_analyze_sentiment()` 자동 호출
  - `_analyze_sentiment()`: Gemini 2.5-flash로 감정 분석. JSON 형식 응답 파싱. **i18n.py 헬퍼 사용** → 사용자 언어로 summary 생성
  - `remove(diary_id)`: 본인 글만 삭제
  - `stats()`: 최근 90일 감정 분포 통계

### 프론트엔드 (page.diary)
- **신규** `src/app/page.diary/app.json`: viewuri `/diary`, layout `layout.navbar`, controller `member`
- **신규** `view.ts`: `mode: 'list' | 'write' | 'detail'` 단일 SPA 페이지
  - URL `?id=xxx`로 상세 직접 진입, `?mode=write`로 작성 진입
  - `SENTIMENT_LABEL` 4언어 매핑 (joy/sad/angry/anxious/calm/excited/neutral) + 색상 + 이모지
  - `MOOD_OPTIONS` 8종 이모지 선택
  - `lang:change` 이벤트 구독 → `cdr.detectChanges()`
- **신규** `view.pug`: 3가지 뷰 모드(list/write/detail) — 모두 i18n `t()` 헬퍼 적용
  - 목록: 통계 막대 차트 + 카드 그리드 + 빈 상태
  - 작성: 날짜·제목·기분이모지·본문·관련타로선택 + AI 감정 분석 버튼
  - 상세: AI 요약 카드(감정 점수 시각화) + 관련 타로 표시 + 수정/삭제
- **신규** `view.scss`: 다크 그라디언트 디자인 + 반응형(모바일 1단 그리드)

### i18n / 네비
- **수정** `src/assets/i18n/i18n.js`: 4개 언어 사전에 `nav.diary` 키 추가 (다이어리/Diary/ダイアリー/日记)
- **수정** `src/app/component.nav/view.pug`: 로그인 사용자 대상으로 📔 다이어리 메뉴 추가 (스위처/사용자명 왼쪽)
- **수정** `src/app/component.nav/view.scss`: `.app-nav__menu` 스타일 추가 (모바일에선 라벨 숨김)

## 검증
- `wiz project build --project=main -c` 성공
- `GET /diary` → 200 (SPA 라우팅)
- `POST /wiz/api/page.diary/list` → 401 (인증 없을 때 정상 거부 = API 라우팅 정상 등록)
- 빌드 산출물 `build/src/app/page.diary/` 존재

## 핵심 동작
1. 로그인 → 네비 📔 다이어리 클릭
2. "새 다이어리" → 제목·본문·기분·관련 타로 선택 → 저장 시 백엔드가 Gemini로 감정 분석 (1~3초)
3. 결과: sentiment(카테고리), sentiment_score(-1~1), ai_summary(1줄 요약) 자동 채워짐
4. 목록에서 최근 90일 감정 분포 막대 차트 확인 가능
5. 다국어 대응: 사용자 언어(ko/en/ja/zh)로 AI 요약 자동 생성

## 후속 개선 (필요 시 todo)
- 캘린더 뷰 / 월별 그리드
- 감정 변화 라인 차트 (timeline 데이터는 API에서 이미 반환 중)
- 프로필 페이지 내 탭 통합
- 다이어리 검색
