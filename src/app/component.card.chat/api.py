import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from google import genai

import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = open("/opt/app/data/gemini_key.txt").read().strip()
        os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    except Exception:
        pass
_ai_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """당신은 타로 카드 전문 상담사입니다.
사용자가 방금 뽑은 타로 카드가 있으며, 이 카드에 대해 더 깊은 질문을 합니다.

대화 규칙:
1. 항상 한국어로 대화합니다.
2. 사용자가 뽑은 카드 정보를 기반으로 구체적이고 따뜻한 조언을 제공하세요.
3. 카드의 상징, 의미, 사용자 상황과의 연관성을 풍부하게 설명해주세요.
4. 답변은 3-5문장으로 적절히 유지하세요.
5. 이모지를 적절히 사용하세요."""

def chat():
    message = wiz.request.query("message", True)
    history_str = wiz.request.query("history", "[]")
    card_context_str = wiz.request.query("card_context", "{}")

    try:
        history = json.loads(history_str)
    except Exception:
        history = []

    try:
        card_context = json.loads(card_context_str)
    except Exception:
        card_context = {}

    cards = card_context.get("cards", [])
    user_name = card_context.get("userName", "")
    concern = card_context.get("concern", "")

    card_info_text = ""
    if cards:
        card_info_text = "\n\n[사용자가 뽑은 카드 정보]\n"
        for c in cards:
            direction = "역방향(Reversed)" if c.get("is_reversed") else "정방향(Upright)"
            label = c.get("label", "")
            label_text = f" ({label})" if label else ""
            card_info_text += f"- {c.get('card_name', 'Unknown')}{label_text}: {direction}\n"
        if concern:
            card_info_text += f"\n사용자의 고민/주제: {concern}\n"

    context_prompt = SYSTEM_PROMPT + card_info_text

    contents = []
    contents.append({"role": "user", "parts": [{"text": context_prompt}]})
    contents.append({"role": "model", "parts": [{"text": "네, 뽑으신 카드에 대해 상세히 안내해 드리겠습니다."}]})

    for msg in history[-10:]:
        role = "model" if msg.get("role") == "bot" else "user"
        contents.append({"role": role, "parts": [{"text": msg.get("text", "")}]})

    contents.append({"role": "user", "parts": [{"text": message}]})

    try:
        def _call():
            return _ai_client.models.generate_content(model='gemini-2.5-flash', contents=contents)
        with ThreadPoolExecutor(max_workers=1) as ex:
            response = ex.submit(_call).result(timeout=20)
        reply = response.text.strip()
    except FuturesTimeoutError:
        reply = "응답 시간이 초과됐어요. 잠시 후 다시 질문해 주세요 🔮"
    except Exception as e:
        print(f"Card chat AI error: {e}")
        reply = "잠시 연결이 불안해졌어요... 다시 질문해 주세요 🔮"

    wiz.response.status(200, reply=reply)
