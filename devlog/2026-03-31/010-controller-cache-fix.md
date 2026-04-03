# 컨트롤러 캐시 우회 + 인증 시스템 수정

- **ID**: 010
- **날짜**: 2026-03-31
- **유형**: 버그 수정

## 작업 요약
WIZ 프레임워크의 컨트롤러 바이트코드 캐시로 인해 `user.py` 수정사항이 런타임에 반영되지 않는 문제를 해결. 캐시 키가 컨트롤러 이름 기반이므로 새 이름 `member.py`로 컨트롤러를 생성하여 캐시를 우회. 비인증 API 호출 시 302 redirect 대신 401 JSON 응답이 정상 반환되도록 수정.

## 원인 분석
- `season/lib/core/wiz.py`의 `controller()` 메서드가 `wiz.server.cache`에 컨트롤러 바이트코드를 캐시
- 캐시 키: `controller.code#{project_name}` 딕셔너리의 네임스페이스(=컨트롤러 이름)
- 파일 변경 시 디스크에서 재로드하지 않고 캐시된 컴파일 코드를 재사용
- 이전 `user.py`의 `wiz.response.redirect()` 코드가 캐시에 잔존

## 해결 방법
- 새 컨트롤러 `member.py` 생성 (캐시에 없는 새 이름)
- 모든 보호 페이지의 `app.json`에서 `"controller": "user"` → `"controller": "member"` 변경

## 변경 파일 목록

### 신규 생성
- `src/controller/member.py`: 인증 컨트롤러 (base 상속, 401 JSON 반환)

### app.json 수정
- `src/app/page.fifth/app.json`: controller → member
- `src/app/page.fourth/app.json`: controller → member
- `src/app/page.main/app.json`: controller → member
- `src/app/page.monthly/app.json`: controller → member
- `src/app/page.page.tarot/app.json`: controller → member
- `src/app/page.page.tarotw/app.json`: controller → member
- `src/app/page.profile/app.json`: controller → member
- `src/app/page.second/app.json`: controller → member

## 검증 결과
- 비인증 API: `{"code": 401, "data": {"message": "login required"}}` ✅
- 인증 API: `{"code": 200, ...}` + 정상 데이터 반환 ✅
- 루트 URL `/`: Angular SPA 정상 서빙 ✅
- `/auth/check`: 로그인 상태 정상 반환 ✅
