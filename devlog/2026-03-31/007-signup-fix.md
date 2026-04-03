# [회원가입] API 응답 형식 수정, 자동 승인, 리다이렉트 경로 수정

- **ID**: 007
- **날짜**: 2026-03-31
- **유형**: 버그 수정

## 작업 요약
회원가입 및 로그인 전체 플로우 수정. API를 `wiz.response.json()` → `wiz.response.status()` 표준 패턴으로 전환하고, 회원가입 시 자동 승인(approved=True)으로 변경하여 가입 후 즉시 로그인 가능하도록 수정. 프론트엔드 응답 처리 및 리다이렉트 경로도 수정.

## 변경 파일 목록

### page.login/api.py
- `wiz.response.json({"code", "data"})` → `wiz.response.status(code, message=...)` 표준 패턴으로 전환
- `approved=False` → `approved=True` 자동 승인
- 불필요한 `import hashlib` 제거

### page.login/view.ts
- 로그인 성공 리다이렉트: `/dashboard` (미존재) → `/main/user`
- 응답 에러 메시지 처리: `data` (object) → `data?.message` 안전 접근
- 회원가입 성공 후: 전체 새로고침(`location.href`) → 로그인 폼 전환 (`showSignup = false`)
- ngOnInit: `service.auth.allow()` 호출을 try/catch로 안전하게 래핑
- 성공 메시지: "관리자 승인 후 로그인 가능합니다" → "로그인해주세요"
