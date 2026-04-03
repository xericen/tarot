# DB: tarot_cards(id, name, description)
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from google import genai

Cards = wiz.model("db/tarott/tarot_cards")

import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
_ai_client = genai.Client(api_key=GEMINI_API_KEY)

import json as _json

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

def _save_history(cards_str, summary="", card_ids="", result_data=""):
    try:
        session = wiz.model("portal/season/session").use()
        user_id = session.get("id")
        if user_id:
            TarotHistory = wiz.model("db/login/tarot_history")
            TarotHistory.create(user_id=int(user_id), tarot_type="today", cards=cards_str, card_ids=card_ids, result_summary=summary, result_data=result_data)
    except Exception:
        pass

def _get_ai_fortune_today(card_name, is_reversed=False, user_name=""):
    try:
        reversed_text = "(역방향/Reversed)" if is_reversed else "(정방향/Upright)"
        reversed_instruction = ""
        if is_reversed:
            reversed_instruction = "\n이 카드는 역방향(Reversed)으로 나왔습니다. 역방향의 의미를 반영하여 해석해주세요."
        name_text = f"'{user_name}'님" if user_name else "질문자"
        prompt = f"""당신은 전문 타로 리더입니다. {name_text}의 오늘의 타로에서 '{card_name}' 카드가 선택되었습니다. {reversed_text}{reversed_instruction}
이 카드의 의미와 상징을 바탕으로 {name_text}의 오늘의 운세를 한국어로 알려주세요.

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이 JSON만):
{{
  "keyword": "카드를 대표하는 키워드 (2~3개, 쉼표 구분)",
  "fortune": "오늘의 운세 (3~4문장, 따뜻하고 구체적으로)",
  "guide": {{
    "good": "하기 좋은 일 (2~3가지)",
    "caution": "주의사항 (1~2가지)"
  }},
  "lucky_color": "행운의 색 (한 가지, 한국어로)",
  "lucky_tip": "오늘 하루를 위한 행운의 팁 (1~2문장)"
}}"""
        def _call():
            return _ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        with ThreadPoolExecutor(max_workers=1) as ex:
            response = ex.submit(_call).result(timeout=20)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3].strip()
        return _json.loads(text)
    except Exception as e:
        print(f"AI fortune error: {e}")
        return None

def tarot_result():
    raw = wiz.request.query("card_id", True)
    is_reversed_str = wiz.request.query("is_reversed", "false")
    is_reversed = is_reversed_str.lower() == "true"
    user_name = wiz.request.query("name", "")

    try:
        card_id = int(raw)
    except Exception:
        wiz.response.status(400, message="invalid card_id")

    card_name = TAROT_CARDS[card_id] if 0 <= card_id < len(TAROT_CARDS) else f"Card {card_id}"

    ai_result = _get_ai_fortune_today(card_name, is_reversed, user_name)

    if ai_result and isinstance(ai_result, dict):
        data = {
            "card_id": card_id,
            "card_name": card_name,
            "is_reversed": is_reversed,
            "image_url": f"/assets/TarotCard/{card_id}.jpg",
            "keyword": ai_result.get("keyword", ""),
            "fortune": ai_result.get("fortune", ""),
            "guide_good": ai_result.get("guide", {}).get("good", ""),
            "guide_caution": ai_result.get("guide", {}).get("caution", ""),
            "lucky_color": ai_result.get("lucky_color", ""),
            "lucky_tip": ai_result.get("lucky_tip", ""),
        }
    else:
        data = {
            "card_id": card_id,
            "card_name": card_name,
            "is_reversed": is_reversed,
            "image_url": f"/assets/TarotCard/{card_id}.jpg",
            "keyword": "",
            "fortune": "운세 정보를 불러올 수 없습니다.",
            "guide_good": "",
            "guide_caution": "",
            "lucky_color": "",
            "lucky_tip": "",
        }
    _save_history(card_name, data.get("fortune", "")[:200], card_ids=str(card_id), result_data=json.dumps(data, ensure_ascii=False))
    wiz.response.status(200, **data)
