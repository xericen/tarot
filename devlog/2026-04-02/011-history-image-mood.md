# 기록 카드 상세 정보 강화 (이미지 + 감정 태그)

- **ID**: 011
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
타로 히스토리 DB에 card_ids/mood_tags 필드 추가, 5개 타로 API에서 card_ids 저장, 프로필 페이지에 카드 썸네일과 감정 태그(선택/수정/저장) UI 구현.

## 변경 파일 목록

### DB 모델
- `src/model/db/login/tarot_history.py`: card_ids, mood_tags 필드 추가
- MySQL `login.tarot_history` 테이블: ALTER TABLE로 2개 컬럼 추가

### 타로 API (card_ids 저장)
- `page.page.tarot/api.py`: _save_history에 card_ids 파라미터 추가 및 호출부 수정
- `page.page.tarotw/api.py`: 동일
- `page.fourth/api.py`: 동일
- `page.fifth/api.py`: 동일
- `page.monthly/api.py`: 동일

### 프로필 페이지
- `api.py`: history 응답에 id, card_ids, mood_tags 포함, save_mood() 함수 추가
- `view.ts`: getCardImages(), getMoodTags(), startEditMood(), toggleMoodTag(), saveMoodTags() 메서드, moodOptions 배열, tarotTypeMap에 monthly 추가
- `view.pug`: 카드 썸네일, 무드 태그 표시, 무드 편집 UI (토글 옵션 + 저장/취소)
- `view.scss`: 썸네일, 무드 태그, 무드 편집 관련 스타일 추가
