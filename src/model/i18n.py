"""
i18n 헬퍼 — 백엔드(api.py)에서 클라이언트 언어를 읽어 AI 프롬프트에 주입
"""

LANG_LABELS = {
    "ko": "한국어 (Korean)",
    "en": "English",
    "ja": "日本語 (Japanese)",
    "zh": "简体中文 (Simplified Chinese)",
}

LANG_INSTRUCTIONS = {
    "ko": "응답은 반드시 자연스러운 한국어로 작성하세요.",
    "en": "Respond strictly in natural English.",
    "ja": "応答は必ず自然な日本語で記述してください。",
    "zh": "请务必使用自然流畅的简体中文回复。",
}


def get_lang(default="ko"):
    """현재 요청의 사용자 언어 코드를 반환 (ko/en/ja/zh)."""
    try:
        flask = wiz.response._flask
        cookie_lang = flask.request.cookies.get("lang", None)
        if cookie_lang and cookie_lang in LANG_LABELS:
            return cookie_lang
    except Exception:
        pass
    try:
        q = wiz.request.query("lang", None)
        if q and q in LANG_LABELS:
            return q
    except Exception:
        pass
    return default


def lang_label(code=None):
    code = code or get_lang()
    return LANG_LABELS.get(code, LANG_LABELS["ko"])


def lang_instruction(code=None):
    code = code or get_lang()
    return LANG_INSTRUCTIONS.get(code, LANG_INSTRUCTIONS["ko"])


Model = {
    "get_lang": get_lang,
    "lang_label": lang_label,
    "lang_instruction": lang_instruction,
    "LANG_LABELS": LANG_LABELS,
    "LANG_INSTRUCTIONS": LANG_INSTRUCTIONS,
}
