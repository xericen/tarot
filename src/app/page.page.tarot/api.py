import datetime
import json as _json
import json
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from peewee import fn
from google import genai

Users    = wiz.model("db/tarot/users")
Draws    = wiz.model("db/tarot/draws")
Fortunes = wiz.model("db/tarot/fortunes")
Cards = wiz.model("db/tarot/cards")

KST = datetime.timezone(datetime.timedelta(hours=9))

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

import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
_ai_client = genai.Client(api_key=GEMINI_API_KEY)

def _save_history(cards_str, summary="", card_ids="", result_data=""):
    try:
        session = wiz.model("portal/season/session").use()
        user_id = session.get("id")
        if user_id:
            TarotHistory = wiz.model("db/login/tarot_history")
            TarotHistory.create(user_id=int(user_id), tarot_type="daily", cards=cards_str, card_ids=card_ids, result_summary=summary, result_data=result_data)
    except Exception:
        pass

def _get_ai_fortune(card_name, user_name, is_reversed=False):
    try:
        reversed_text = "(역방향/Reversed)" if is_reversed else "(정방향/Upright)"
        reversed_instruction = ""
        if is_reversed:
            reversed_instruction = "\n이 카드는 역방향(Reversed)으로 나왔습니다. 역방향의 의미를 반영하여 해석해주세요. 역방향은 카드의 긍정적 에너지가 억압되거나 내면으로 향하는 것을 의미합니다."
        prompt = f"""당신은 전문 타로 리더입니다. '{user_name}'님이 일일 타로에서 '{card_name}' 카드를 뽑았습니다. {reversed_text}{reversed_instruction}
이 카드의 의미와 상징을 바탕으로 오늘의 운세를 한국어로 섹션별로 구체적으로 알려주세요.

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이 JSON만):
{{
  "subtitle": "카드의 핵심 의미를 한 줄로 (예: 결단 보류 · 내면의 방어막)",
  "finance": "재정운 (2~3문장, 구체적이고 따뜻하게)",
  "love": "애정운 (2~3문장)",
  "health": "건강운 (2~3문장)",
  "focus": "오늘의 포커스 — 집중해야 할 것 (2~3문장)",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4"],
  "one_word": "{user_name}님께 드리는 오늘의 한마디 (임팩트 있는 2~3문장, 감성적으로)"
}}"""
        def _call_gemini():
            return _ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_call_gemini)
            response = future.result(timeout=20)
        text = response.text.strip()
        if "```" in text:
            lines = text.split("```")
            for block in lines[1:]:
                block = block.strip()
                if block.startswith("json"):
                    block = block[4:].strip()
                if block.startswith("{"):
                    text = block
                    break
        return _json.loads(text)
    except Exception as e:
        print(f"AI fortune error: {e}")
        return None

def tarot_draw():
    name = (wiz.request.query("name", True) or "").strip()
    if not name:
        wiz.response.status(400, message="name is required")

    raw_card_id = wiz.request.query("card_id", None)
    is_reversed_str = wiz.request.query("is_reversed", "false")
    is_reversed = is_reversed_str.lower() == "true"

    now = datetime.datetime.now(KST)

    user = Users.get_or_none(Users.name == name)
    if not user:
        user = Users.create(name=name, created_at=now)

    if raw_card_id is not None and raw_card_id != "":
        card_id = int(raw_card_id)
    else:
        fortune = Fortunes.select().order_by(fn.Rand()).first()
        if not fortune:
            wiz.response.status(500, message="no fortunes")
        card_id = int(fortune.card_id)
        is_reversed = random.random() < 0.5

    try:
        Draws.create(user_id=user.user_id, card_id=card_id)
    except Exception:
        pass
    card_name = TAROT_CARDS[card_id] if 0 <= card_id < len(TAROT_CARDS) else f"Card #{card_id}"
    is_reversed = random.random() < 0.5

    ai_result = _get_ai_fortune(card_name, name, is_reversed)

    if ai_result and isinstance(ai_result, dict):
        data = {
            "card_id": card_id,
            "card_name": card_name,
            "is_reversed": is_reversed,
            "image_url": f"/assets/TarotCard/{card_id}.jpg",
            "subtitle": ai_result.get("subtitle", ""),
            "finance": ai_result.get("finance", ""),
            "love": ai_result.get("love", ""),
            "health": ai_result.get("health", ""),
            "focus": ai_result.get("focus", ""),
            "keywords": ai_result.get("keywords", []),
            "one_word": ai_result.get("one_word", ""),
        }
    else:
        reversed_label = " (역방향)" if is_reversed else ""
        data = {
            "card_id": card_id,
            "card_name": card_name,
            "is_reversed": is_reversed,
            "image_url": f"/assets/TarotCard/{card_id}.jpg",
            "subtitle": f"{card_name}{reversed_label} · 오늘의 카드",
            "finance": f"{card_name} 카드가 재정 면에서 신중함을 권하고 있어요. 오늘은 큰 지출보다 안정적인 관리에 집중하면 좋겠습니다. 작은 절약이 나중에 큰 기쁨이 될 거예요.",
            "love": f"오늘 {card_name} 카드는 인간관계에서 따뜻한 에너지를 보내고 있어요. 소중한 사람에게 먼저 연락해보세요. 작은 관심이 큰 행복으로 돌아올 거예요.",
            "health": f"{card_name} 카드가 건강에 대해 균형을 이야기하고 있어요. 충분한 수면과 가벼운 스트레칭으로 몸과 마음의 조화를 찾아보세요.",
            "focus": f"오늘 {card_name} 카드는 당신에게 가장 중요한 한 가지에 집중하라고 말하고 있어요. 여러 일을 동시에 하기보다 하나에 온 마음을 쏟아보세요.",
            "keywords": [card_name, "균형", "집중", "새로운 시작"],
            "one_word": f"{name}님, 오늘 {card_name} 카드가 당신 곁에 있어요. 이 카드는 당신의 하루를 특별하게 만들어줄 에너지를 품고 있답니다. 자신을 믿고 한 걸음씩 나아가세요!",
        }

    _save_history(card_name, data.get("one_word", "")[:200], card_ids=str(card_id), result_data=json.dumps(data, ensure_ascii=False))

    wiz.response.status(200, **data)
