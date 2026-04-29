"""
RAG (Retrieval-Augmented Generation) 헬퍼
- 타로 78장 카드 지식 베이스를 chromadb에 저장 (build_rag_db.py)
- query() : 카드 이름 + 사용자 질문으로 top-k 청크 검색 → 프롬프트 컨텍스트 반환
- ChromaDB 기본 임베딩(all-MiniLM-L6-v2) 사용. Gemini API 의존성 없음.
"""

import os

RAG_DB_DIR = "/opt/app/project/main/data/rag"
COLLECTION_NAME = "tarot_knowledge"

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is not None:
        return _collection
    try:
        # chromadb 내부의 `import struct`가 src/model/struct.py와 충돌하지 않도록
        # sys.path에서 model 디렉토리를 임시 제거
        import sys as _sys
        original_path = list(_sys.path)
        _sys.path = [p for p in _sys.path if "/src/model" not in p and not p.endswith("/src/model")]
        # 표준 struct 모듈을 강제 로드
        if "struct" in _sys.modules:
            mod = _sys.modules["struct"]
            if not hasattr(mod, "pack"):
                del _sys.modules["struct"]
                import struct as _real_struct  # noqa
        try:
            import chromadb
        finally:
            _sys.path = original_path
        _client = chromadb.PersistentClient(path=RAG_DB_DIR)
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
        return _collection
    except Exception as e:
        print(f"[rag] chroma init error: {e}")
        return None


def is_ready():
    """RAG DB 구축 여부 (도큐먼트 1개 이상)"""
    col = _get_collection()
    if col is None:
        return False
    try:
        return col.count() > 0
    except Exception:
        return False


def query(card_names, user_query="", k=5, max_chars=1800):
    """카드 이름 리스트 + 질문으로 top-k 청크 검색.
    프롬프트에 그대로 붙일 수 있는 문자열을 반환. RAG 미준비 시 빈 문자열.
    """
    col = _get_collection()
    if col is None:
        return ""
    try:
        if col.count() == 0:
            return ""
    except Exception:
        return ""

    if isinstance(card_names, str):
        card_names = [card_names]

    parts = []
    seen = set()
    try:
        per_card_k = max(2, k // max(1, len(card_names)))
        for cn in card_names:
            q = f"{cn} {user_query}".strip()
            res = col.query(query_texts=[q], n_results=per_card_k)
            docs = res.get("documents", [[]])[0]
            metas = res.get("metadatas", [[]])[0]
            for d, m in zip(docs, metas):
                key = (m.get("card_name", ""), m.get("chunk_type", ""))
                if key in seen:
                    continue
                seen.add(key)
                parts.append(f"[{m.get('card_name', '?')} · {m.get('chunk_type', '?')}] {d}")
    except Exception as e:
        print(f"[rag] query error: {e}")
        return ""

    text = "\n".join(parts)
    if len(text) > max_chars:
        text = text[:max_chars] + "..."
    return text


def build_context(card_names, user_query=""):
    """프롬프트 주입용 RAG 컨텍스트 문자열 생성. 빈 결과 시 빈 문자열."""
    snippets = query(card_names, user_query)
    if not snippets:
        return ""
    return (
        "\n[RAG 참고 자료 — 타로 지식 베이스]\n"
        f"{snippets}\n"
        "위 자료를 참고하되, 자료에 없는 내용은 일반 타로 지식으로 보완하여 자연스럽게 해석하세요.\n"
    )


Model = {
    "is_ready": is_ready,
    "query": query,
    "build_context": build_context,
}
