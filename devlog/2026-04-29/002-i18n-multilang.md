# i18n 4개 언어 지원 (KR/EN/JA/ZH) + AI 응답 다국어 인프라

- **ID**: 002
- **날짜**: 2026-04-29
- **유형**: 기능 추가

## 작업 요약
ngx-translate 의존성 없이 **순수 JS 기반 경량 i18n 시스템**을 구축. `window.__t()` 헬퍼와 `lang:change` 커스텀 이벤트로 전체 사이트 언어 전환을 구현. 우측 상단 사용자 이름 왼쪽에 언어 스위처(🇰🇷 KR / 🇺🇸 EN / 🇯🇵 JA / 🇨🇳 ZH) 추가. 백엔드는 쿠키에서 lang 코드를 읽어 Gemini 프롬프트에 언어 지시문을 동적으로 주입.

## 변경 파일 목록

### 프론트엔드 i18n 인프라
- **신규** `src/assets/i18n/i18n.js`: 4개 언어 사전(`DICT.ko/en/ja/zh`) + `window.__t(key, fallback?, vars?)` 헬퍼 + `localStorage 'season-tarot-lang'` + `cookie 'lang'` 동기화 + `lang:change` CustomEvent dispatch
- **수정** `src/angular/index.pug`: `<script src="/assets/i18n/i18n.js">`를 Angular 부트 전에 로드

### 언어 스위처 컴포넌트
- **신규** `src/app/component.lang.switcher/`
  - `app.json`: namespace `lang.switcher`, selector `wiz-component-lang-switcher`
  - `view.ts`: 4개 언어 옵션, `HostListener('document:click')`로 외부 클릭 시 드롭다운 닫기, `lang:change` 구독
  - `view.pug`: 플래그 이모지 + 언어 코드 표시 트리거 + 드롭다운 메뉴
  - `view.scss`: backdrop-filter 반투명 pill 버튼, z-index 1200, 페이드인 애니메이션

### 네비/홈 i18n 적용
- **수정** `src/app/component.nav/view.pug`: `wiz-component-lang-switcher`를 `.app-nav__user` 직전에 삽입, 브랜드명 `{{ t('app.brand') }}` 적용
- **수정** `src/app/component.nav/view.ts`: `t(key, fallback?)` 헬퍼 + `ChangeDetectorRef` + `lang:change` 구독으로 즉시 재렌더
- **수정** `src/app/page.main/view.ts`: `t(key, fallback, vars)` (변수 치환 포함) + `currentYear` + `lang:change` 구독
- **수정** `src/app/page.main/view.pug`: 모든 한국어 문자열을 `{{ t('main.*') }}` 키로 치환 (배지/설명/CTA/카드 메뉴 5종)

### AI 응답 다국어 백엔드
- **신규** `src/model/i18n.py`:
  - `LANG_LABELS`, `LANG_INSTRUCTIONS` (ko/en/ja/zh)
  - `get_lang(default='ko')`: 쿠키 → query 순으로 언어 코드 추출
  - `lang_label(code=None)`, `lang_instruction(code=None)` 헬퍼
  - `Model = {...}` dict 형태로 export → `wiz.model("i18n")["lang_label"]()`로 호출
- **수정** `src/app/page.page.tarot/api.py`: `_get_ai_fortune()` 내부에서 `wiz.model("i18n")` 로드 → 프롬프트 상단에 `⚠️ 출력 언어: {lang_label}\n{lang_instruction}` 라인 추가. 한국어 하드코딩 제거. JSON 키는 영문 유지하고 값만 사용자 언어로 작성하도록 지시

## 검증 결과
- `wiz project build --project=main -c` 성공
- `GET /assets/i18n/i18n.js` → 200, 15,495 bytes
- HTML `<head>`에 i18n 스크립트 + PWA 메타 정상 렌더링
- 빌드 산출물: `build/src/app/component.lang.switcher/` 존재

## 한계 및 후속 작업
- 풀 i18n 적용은 `page.main` + `component.nav`까지 진행. **로그인/타로 결과/프로필 페이지는 추후 점진 확장**(FN-0002의 후속 todo로 재등록)
- AI 다국어는 `page.page.tarot` (일일 타로) prompt에만 적용. 시즌/연간/월간/오늘/AI 채팅 5종 prompt도 동일 패턴(`wiz.model("i18n")`)으로 확대 필요

## 작업 패턴 (재사용)
```python
# api.py에서 사용자 언어 인지하여 Gemini 프롬프트에 주입
i18n = wiz.model("i18n")
lang_label = i18n["lang_label"]()        # "한국어 (Korean)" / "English" / ...
lang_instruction = i18n["lang_instruction"]()  # "응답은 반드시 ..."
prompt = f"...\n⚠️ 출력 언어: {lang_label}\n{lang_instruction}\n..."
```

```pug
//- view.pug에서 i18n 키 치환
h1 {{ t('home.title') }}
p {{ t('main.menu.yearly.desc', null, { year: currentYear }) }}
```

```typescript
// view.ts 헬퍼 패턴
public t(key: string, fallback?: string, vars?: any): string {
    const w: any = window;
    return w.__t ? w.__t(key, fallback, vars) : (fallback || key);
}
```
