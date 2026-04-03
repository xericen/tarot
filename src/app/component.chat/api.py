import random
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from google import genai

import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
_ai_client = genai.Client(api_key=GEMINI_API_KEY)

TAROT_CARDS = [
    "The Fool","The Magician","The High Priestess","The Empress","The Emperor",
    "The Hierophant","The Lovers","The Chariot","Strength","The Hermit",
    "Wheel of Fortune","Justice","The Hanged Man","Death","Temperance",
    "The Devil","The Tower","The Star","The Moon","The Sun","Judgement","The World",
    "Ace of Wands","Two of Wands","Three of Wands","Four of Wands","Five of Wands",
    "Six of Wands","Seven of Wands","Eight of Wands","Nine of Wands","Ten of Wands",
    "Page of Wands","Knight of Wands","Queen of Wands","King of Wands",
    "Ace of Cups","Two of Cups","Three of Cups","Four of Cups","Five of Cups",
    "Six of Cups","Seven of Cups","Eight of Cups","Nine of Cups","Ten of Cups",
    "Page of Cups","Knight of Cups","Queen of Cups","King of Cups",
    "Ace of Swords","Two of Swords","Three of Swords","Four of Swords","Five of Swords",
    "Six of Swords","Seven of Swords","Eight of Swords","Nine of Swords","Ten of Swords",
    "Page of Swords","Knight of Swords","Queen of Swords","King of Swords",
    "Ace of Pentacles","Two of Pentacles","Three of Pentacles","Four of Pentacles","Five of Pentacles",
    "Six of Pentacles","Seven of Pentacles","Eight of Pentacles","Nine of Pentacles","Ten of Pentacles",
    "Page of Pentacles","Knight of Pentacles","Queen of Pentacles","King of Pentacles"
]

SYSTEM_PROMPT = """당신은 '루카리오'라는 이름의 신비로운 AI 타로 리더입니다.
성격: 따뜻하고 공감적이며, 약간 신비로운 말투를 사용합니다. 이모지를 적절히 사용합니다.
역할: 사용자의 고민을 들어주고, 타로 카드를 통해 조언을 제공합니다.

대화 규칙:
1. 항상 한국어로 대화합니다.
2. 사용자의 고민을 충분히 공감해주세요.
3. 사용자가 고민을 이야기하면, 카드를 뽑아볼 것을 제안하세요.
4. [CARD_DRAWN] 태그가 포함된 메시지에는 해당 카드에 대한 상세한 타로 해석을 제공하세요.
5. 해석은 사용자의 고민과 연관지어 구체적이고 따뜻하게 해주세요.
6. 답변은 3-5문장으로 적절히 짧게 유지하세요."""

def chat():
    message = wiz.request.query("message", True)
    history_str = wiz.request.query("history", "[]")

    try:
        history = json.loads(history_str)
    except Exception:
        history = []

    contents = []
    contents.append({"role": "user", "parts": [{"text": SYSTEM_PROMPT}]})
    contents.append({"role": "model", "parts": [{"text": "네, 루카리오로서 타로 리딩을 시작하겠습니다."}]})

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
    except Exception as e:
        print(f"Chat AI error: {e}")
        reply = "잠시 영감이 흐려졌어요... 다시 한번 말씀해주시겠어요? 🔮"

    wiz.response.status(200, reply=reply)

def draw_card():
    concern = wiz.request.query("concern", "")
    history_str = wiz.request.query("history", "[]")
    client_card_id = wiz.request.query("card_id", "")
    client_is_reversed = wiz.request.query("is_reversed", "")

    try:
        history = json.loads(history_str)
    except Exception:
        history = []

    if client_card_id:
        card_id = int(client_card_id)
        is_reversed = client_is_reversed.lower() == 'true'
    else:
        card_id = random.randint(0, 77)
        is_reversed = random.random() < 0.5
    card_name = TAROT_CARDS[card_id]
    reversed_text = "(역방향/Reversed)" if is_reversed else "(정방향/Upright)"

    card_message = f"[CARD_DRAWN] 카드: {card_name} {reversed_text}. 사용자의 고민: {concern}"

    contents = []
    contents.append({"role": "user", "parts": [{"text": SYSTEM_PROMPT}]})
    contents.append({"role": "model", "parts": [{"text": "네, 루카리오로서 타로 리딩을 시작하겠습니다."}]})

    for msg in history[-10:]:
        role = "model" if msg.get("role") == "bot" else "user"
        contents.append({"role": role, "parts": [{"text": msg.get("text", "")}]})

    contents.append({"role": "user", "parts": [{"text": card_message}]})

    try:
        def _call_card():
            return _ai_client.models.generate_content(model='gemini-2.5-flash', contents=contents)
        with ThreadPoolExecutor(max_workers=1) as ex:
            response = ex.submit(_call_card).result(timeout=20)
        reply = response.text.strip()
    except Exception as e:
        print(f"Card AI error: {e}")
        reply = f"✨ {card_name} 카드가 나왔네요! 이 카드는 당신에게 새로운 시작의 에너지를 보내고 있어요."

    wiz.response.status(200,
        reply=reply,
        card_id=card_id,
        card_name=card_name,
        is_reversed=is_reversed,
        image_url=f"/assets/TarotCard/{card_id}.jpg"
    )
