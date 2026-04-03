# 비밀번호 찾기 이메일 검증 추가

- **ID**: 015
- **날짜**: 2026-04-02
- **유형**: 버그 수정

## 작업 요약
비밀번호 찾기 Step 1에서 존재하지 않는 이메일+이름이어도 Step 2로 넘어가는 문제 수정. 서버 검증 API(verify_reset) 추가.

## 변경 파일 목록
- `src/app/page.login/api.py`: `verify_reset` 함수 추가 (이메일+이름으로 DB 조회, 없으면 404)
- `src/app/page.login/view.ts`: `nextResetStep()`에서 서버 호출로 존재 여부 확인 후 Step 전환
