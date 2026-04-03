# 히스토리 상세 보기 기능 추가

- **ID**: 023
- **날짜**: 2026-04-02
- **유형**: 기능 추가

## 작업 요약
타로 히스토리에 전체 결과 데이터를 저장하고, 프로필 페이지에서 과거 리딩 결과를 상세히 다시 볼 수 있는 모달 추가.

## 변경 파일 목록

### DB 마이그레이션
- `model/db/login/tarot_history.py`: `result_data` TEXT 컬럼 추가
- ALTER TABLE 실행: `tarot_history ADD COLUMN result_data TEXT NULL`

### 5개 타로 페이지 (_save_history 수정)
- `page.page.tarot/api.py`: _save_history에 result_data 파라미터 추가, json.dumps(data) 전달
- `page.fourth/api.py`: 동일 패턴, resp_data dict 생성하여 전달
- `page.fifth/api.py`: 동일 패턴 + json import 추가
- `page.monthly/api.py`: 동일 패턴
- `page.page.tarotw/api.py`: 동일 패턴, resp_data dict 생성하여 전달

### 프로필 페이지 (상세 보기)
- `page.profile/api.py`: detail() 함수 추가 (history_id로 조회, result_data JSON 파싱 반환)
- `page.profile/view.ts`: selectedDetail, detailLoading 상태 + showDetail(), closeDetail() 메서드
- `page.profile/view.pug`: 상세 보기 버튼 + overlay 모달 (일일/오늘/시즌/월간/연간 타입별 결과 렌더링)
- `page.profile/view.scss`: detail-overlay, detail-modal, detail-card-row 등 모달 스타일
