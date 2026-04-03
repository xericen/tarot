import datetime
import json as _json
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from google import genai

Cards = wiz.model("db/tarott/tarot_cards")

import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = open("/opt/app/data/gemini_key.txt").read().strip()
        os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    except Exception:
        pass
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

MONTH_NAMES = {
    1: "1월", 2: "2월", 3: "3월", 4: "4월",
    5: "5월", 6: "6월", 7: "7월", 8: "8월",
    9: "9월", 10: "10월", 11: "11월", 12: "12월"
}

KST = datetime.timezone(datetime.timedelta(hours=9))

def _save_history(cards_str, summary="", card_ids="", result_data=""):
    try:
        session = wiz.model("portal/season/session").use()
        user_id = session.get("id")
        if user_id:
            TarotHistory = wiz.model("db/login/tarot_history")
            TarotHistory.create(user_id=int(user_id), tarot_type="monthly", cards=cards_str, card_ids=card_ids, result_summary=summary, result_data=result_data)
    except Exception:
        pass

def _get_ai_monthly(card_name, user_name, month_str, concern, is_reversed=False):
    try:
        reversed_text = "(역방향/Reversed)" if is_reversed else "(정방향/Upright)"
        reversed_instruction = ""
        if is_reversed:
            reversed_instruction = "\n이 카드는 역방향(Reversed)으로 나왔습니다. 역방향의 의미를 반영하여 해석해주세요."
        prompt = f"""당신은 전문 타로 리더입니다. '{user_name}'님이 {month_str} 월간 타로에서 '{card_name}' 카드를 뽑았습니다. {reversed_text}{reversed_instruction}
관심 분야: {concern}

이 카드의 의미를 바탕으로 {month_str} 한 달 운세를 한국어로 상세히 알려주세요.

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이 JSON만):
{{
  "subtitle": "카드의 핵심 의미를 짧게 (예: 새로운 시작 · 무한한 가능성)",
  "overview": "이달의 전체 운세 개관 (3~4문장, 따뜻하고 구체적으로)",
  "career": "직업/학업 운세 (2~3문장)",
  "love": "애정/인간관계 운세 (2~3문장)",
  "finance": "재정 운세 (2~3문장)",
  "health": "건강/에너지 운세 (2~3문장)",
  "advice": "이 달을 잘 보내기 위한 조언 (2~3문장, '{user_name}'님이라고 부르며 감성적으로)",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
  "lucky_day": "이 달의 행운의 날짜 또는 요일 (예: 매주 수요일, 15일경)",
  "closing": "'{user_name}'님께 드리는 이 달의 한마디 (임팩트 있는 2~3문장)"
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
        print(f"AI monthly fortune error: {e}")
        return None

def monthly_draw():
    name = (wiz.request.query("name", True) or "").strip()
    concern = wiz.request.query("concern", True)
    raw_card_id = wiz.request.query("card_id", True)
    is_reversed_str = wiz.request.query("is_reversed", "false")
    is_reversed = is_reversed_str.lower() == "true"

    if not name:
        wiz.response.status(400, message="name is required")

    try:
        card_id = int(raw_card_id)
    except Exception:
        wiz.response.status(400, message="invalid card_id")

    now = datetime.datetime.now(KST)
    current_month = now.month
    current_year = now.year
    month_str = f"{current_year}년 {MONTH_NAMES.get(current_month, str(current_month) + '월')}"

    card_name = TAROT_CARDS[card_id] if 0 <= card_id < len(TAROT_CARDS) else f"Card {card_id}"

    ai_result = _get_ai_monthly(card_name, name, month_str, concern, is_reversed)

    if ai_result and isinstance(ai_result, dict):
        data = {
            "card_id": card_id,
            "card_name": card_name,
            "is_reversed": is_reversed,
            "image_url": f"/assets/TarotCard/{card_id}.jpg",
            "month": month_str,
            "subtitle": ai_result.get("subtitle", ""),
            "overview": ai_result.get("overview", ""),
            "career": ai_result.get("career", ""),
            "love": ai_result.get("love", ""),
            "finance": ai_result.get("finance", ""),
            "health": ai_result.get("health", ""),
            "advice": ai_result.get("advice", ""),
            "keywords": ai_result.get("keywords", []),
            "lucky_day": ai_result.get("lucky_day", ""),
            "closing": ai_result.get("closing", ""),
        }
    else:
        data = {
            "card_id": card_id,
            "card_name": card_name,
            "is_reversed": is_reversed,
            "image_url": f"/assets/TarotCard/{card_id}.jpg",
            "month": month_str,
            "subtitle": "",
            "overview": "운세 정보를 불러올 수 없습니다.",
            "career": "", "love": "", "finance": "", "health": "",
            "advice": "", "keywords": [], "lucky_day": "", "closing": "",
        }

    _save_history(card_name, data.get("closing", "")[:200], card_ids=str(card_id), result_data=json.dumps(data, ensure_ascii=False))
    wiz.response.status(200, **data)
