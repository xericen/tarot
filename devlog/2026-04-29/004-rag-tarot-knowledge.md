# RAG 기반 타로 해석 고도화 (ChromaDB + 78장 지식 베이스)

- **ID**: 004
- **날짜**: 2026-04-29
- **유형**: 기능 추가

## 작업 요약
타로 78장 카드별 지식 청크(정방향/역방향 + love/finance/health/work 4영역 = 카드당 6청크 = **총 468 청크**)를 ChromaDB(`all-MiniLM-L6-v2` 기본 임베딩)에 저장하고, AI 응답 생성 시 카드 이름 + 사용자 질문으로 top-k 검색해 **Gemini 프롬프트에 컨텍스트로 동적 주입**하는 RAG 파이프라인을 구축. 외부 임베딩 API 의존성 없는 로컬 벡터 DB. 미구축 시 빈 컨텍스트 반환으로 graceful degradation.

## 변경 파일 목록

### 인프라
- `chromadb` 패키지 설치 (1.5.8)
- **신규** `data/rag/` 디렉토리 — ChromaDB persistent 저장소 (~2MB sqlite + parquet)
- **신규** `scripts/build_rag_db.py`:
  - DB의 `fortunes` 테이블에서 78장 한국어 키워드 로드
  - 78장 × 6 청크(`upright`, `reversed`, `love`, `finance`, `health`, `work`) 생성
  - Major Arcana 22장 + Minor Arcana 56장(슈트별 element/domain/energy 매핑: 불·물·공기·흙)
  - 한국어 카드명 매핑 78개 포함
  - 배치 100개씩 ChromaDB에 add → 총 468개 저장 검증

### 검색 모듈
- **신규** `src/model/rag.py`:
  - `Model = {"is_ready", "query", "build_context"}` dict 형태로 export
  - `_get_collection()`: lazy init + **sys.path 정리**로 chromadb 내부 `import struct`가 프로젝트의 `src/model/struct.py`와 충돌하는 문제 회피
  - `query(card_names, user_query, k=5, max_chars=1800)`: 카드별 분배 검색 + 중복 제거
  - `build_context(card_names, user_query)`: 프롬프트에 바로 붙일 수 있는 컨텍스트 문자열 생성. 결과 없으면 빈 문자열 반환 (graceful degradation)

### Prompt 통합
- **수정** `src/app/page.page.tarot/api.py` (`_get_ai_fortune`):
  - `wiz.model("rag")["build_context"]([card_name], "오늘의 운세 해석")` 호출
  - 프롬프트 본문 안에 `[RAG 참고 자료 — 타로 지식 베이스]` 블록을 동적 삽입
  - 자료가 없는 경우 일반 타로 지식으로 보완하라는 지시문 포함
  - i18n 헬퍼와 함께 사용되어 다국어 + RAG 동시 작동

## 검증
- `python3 scripts/build_rag_db.py` 실행 → "✅ 완료: 468개 청크 저장"
- `data/rag/chroma.sqlite3` 2,052,096 bytes 생성
- `wiz project build --project=main` 성공 (normal 빌드 — 시그니처 변경 없음)
- 샘플 검색 `"The Fool 사랑"` → top-3 청크 정상 반환

## 동작 흐름
1. 사용자가 일일 타로 카드 뽑기 → `_get_ai_fortune(card_name, ...)` 호출
2. `wiz.model("rag")["build_context"]([card_name], "오늘의 운세 해석")` 실행
3. ChromaDB에서 카드 이름과 의미적으로 가까운 청크 5개 검색
4. 검색 결과를 `[RAG 참고 자료]\n[The Fool · upright] ... \n[The Fool · love] ...` 형태로 프롬프트 본문에 삽입
5. Gemini가 자료를 참조하여 더 일관성 있는 해석 생성

## 한계 및 후속
- **현재는 일일 타로 prompt 1곳만 적용**. 시즌/연간/월간/오늘/AI 채팅의 prompt에도 동일 패턴(`wiz.model("rag")`) 확장 필요 (FN-0005에 등록)
- 영/일/중 다국어 청크는 미구축 — 한국어 청크 + Gemini 출력 언어 지시문으로 대체. 추후 4언어 청크 빌드 가능
- 임베딩 모델은 ChromaDB 기본(all-MiniLM-L6-v2). 한국어 성능 한계 존재 — 추후 multilingual 모델로 교체 가능
- 영역별 해석 청크는 템플릿 기반(`gen_love`, `gen_finance` 등). 추후 Gemini로 사전 생성한 고품질 청크로 대체 가능

## 사용 패턴 (재사용)
```python
# api.py에서 RAG 컨텍스트 동적 주입
try:
    rag = wiz.model("rag")
    rag_context = rag["build_context"]([card_name], "사용자 질문")
except Exception:
    rag_context = ""

prompt = f"""기본 프롬프트...
{rag_context}
⚠️ 출력 언어: {lang_label}
{lang_instruction}
..."""
```

```bash
# RAG DB 재구축 (운영자)
python3 /opt/app/project/main/scripts/build_rag_db.py
```
