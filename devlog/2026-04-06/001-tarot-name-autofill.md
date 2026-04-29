# 타로 페이지 이름 입력칸에 가입 이름 자동 세팅

- **ID**: 001
- **날짜**: 2026-04-06
- **유형**: 기능 추가

## 작업 요약
5개 타로 페이지에서 `ngOnInit` 시 세션의 사용자 이름(`this.service.auth.session.name`)을 `userName`에 자동 할당하도록 수정. 다시보기(reset/restart/resetSelection) 시에도 세션 이름으로 복원하여, 사용자가 별도로 수정하지 않으면 가입 시 등록한 이름으로 타로를 진행하고, 수정하면 수정한 이름으로 진행.

## 변경 파일 목록
### 프론트엔드 (view.ts)
- `src/app/page.page.tarot/view.ts`: ngOnInit에 세션 이름 할당, reset()에 세션 이름 복원
- `src/app/page.monthly/view.ts`: ngOnInit에 세션 이름 할당, resetSelection()에 세션 이름 복원
- `src/app/page.page.tarotw/view.ts`: ngOnInit에 세션 이름 할당, resetSelection()에 세션 이름 복원
- `src/app/page.fourth/view.ts`: ngOnInit에 세션 이름 할당, resetSelection()에 세션 이름 복원
- `src/app/page.fifth/view.ts`: ngOnInit에 세션 이름 할당, restart()에 세션 이름 복원
