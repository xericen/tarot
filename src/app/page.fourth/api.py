import datetime
import json as _json
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from google import genai

Users    = wiz.model("db/tarotp/p_users")
Draws    = wiz.model("db/tarotp/p_draws")
Fortunes = wiz.model("db/tarotp/p_fortunes")
Cards    = wiz.model("db/tarotp/p_cards")

KST = datetime.timezone(datetime.timedelta(hours=9))
POSITIONS = ["past", "present", "future"]
LABELS = {"past": "과거", "present": "현재", "future": "미래"}

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
if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = open("/opt/app/data/gemini_key.txt").read().strip()
        os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    except Exception:
        pass
_ai_client = genai.Client(api_key=GEMINI_API_KEY)

def _save_history(cards_str, summary="", card_ids="", result_data=""):
    try:
        session = wiz.model("portal/season/session").use()
        user_id = session.get("id")
        if user_id:
            TarotHistory = wiz.model("db/login/tarot_history")
            TarotHistory.create(user_id=int(user_id), tarot_type="season", cards=cards_str, card_ids=card_ids, result_summary=summary, result_data=result_data)
    except Exception:
        pass

def _get_ai_fortune_season(card_name, category, position_label, user_name, is_reversed=False):
    # 이 함수는 더 이상 개별 호출되지 않음 (하위 호환용 유지)
    return None

def _get_ai_fortunes_combined(card_info_list, category, user_name):
    """3장 카드 운세 + 총평을 1회 Gemini 호출로 통합 요청"""
    try:
        cards_desc = "\n".join([
            f"- {c['label']}: '{c['card_name']}' {'(역방향/Reversed)' if c['is_reversed'] else '(정방향/Upright)'}"
            for c in card_info_list
        ])
        prompt = f"""당신은 전문 타로 리더입니다. '{user_name}'님이 Season 카드에서 '{category}' 분야를 선택했고, 과거·현재·미래 위치에 각각 다음 카드를 뽑았습니다:
{cards_desc}

역방향(Reversed) 카드는 역방향의 의미를 반영하여 해석해주세요.

반드시 아래 JSON 형식으로만 응답하세요 (다른 텍스트 없이 JSON만):
{{
  "cards": [
    {{
      "label": "과거",
      "subtitle": "카드의 핵심 의미를 짧게",
      "message": "{category}에 대한 과거의 운세 (3~4문장, 구체적이고 따뜻하게, '{user_name}'님이라고 부르며)",
      "keywords": ["키워드1", "키워드2", "키워드3", "키워드4"],
      "flow_word": "과거를 한 단어로 (예: 방어, 각성)"
    }},
    {{
      "label": "현재",
      "subtitle": "카드의 핵심 의미를 짧게",
      "message": "{category}에 대한 현재의 운세 (3~4문장)",
      "keywords": ["키워드1", "키워드2", "키워드3", "키워드4"],
      "flow_word": "현재를 한 단어로"
    }},
    {{
      "label": "미래",
      "subtitle": "카드의 핵심 의미를 짧게",
      "message": "{category}에 대한 미래의 운세 (3~4문장)",
      "keywords": ["키워드1", "키워드2", "키워드3", "키워드4"],
      "flow_word": "미래를 한 단어로"
    }}
  ],
  "closing": "3장의 흐름을 하나의 스토리로 엮어 '{user_name}'님께 드리는 감성적인 총평 (2~3문장)"
}}"""
        def _call():
            return _ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        with ThreadPoolExecutor(max_workers=1) as ex:
            response = ex.submit(_call).result(timeout=30)
        text = response.text.strip()
        if "```" in text:
            parts = text.split("```")
            for block in parts[1:]:
                block = block.strip()
                if block.startswith("json"):
                    block = block[4:].strip()
                if block.startswith("{"):
                    text = block
                    break
        return _json.loads(text)
    except Exception as e:
        print(f"AI combined fortune error: {e}")
        return None

def tarot_draw_three():
    name = (wiz.request.query("name", True) or "").strip()
    category = wiz.request.query("concern", True)
    selected = wiz.request.query("selected", True)
    reversed_str = wiz.request.query("reversed", "") or ""

    if not name:
        wiz.response.status(400, message="name is required")
    if not selected:
        wiz.response.status(400, message="selected cards required")

    selected_ids = [int(x) for x in selected.split(",") if x.isdigit()]
    if len(selected_ids) != 3:
        wiz.response.status(400, message="exactly 3 cards must be selected")

    reversed_flags = []
    if reversed_str:
        reversed_flags = [x.strip().lower() == "true" for x in reversed_str.split(",")]
    while len(reversed_flags) < len(selected_ids):
        reversed_flags.append(False)

    now = datetime.datetime.now(KST)

    user = Users.get_or_none(Users.name == name)
    if not user:
        user = Users.create(name=name, created_at=now)

    # 카드 정보 수집
    card_info_list = []
    for idx, (pos, card_id) in enumerate(zip(POSITIONS, selected_ids)):
        is_reversed = reversed_flags[idx]
        card_name = TAROT_CARDS[card_id] if 0 <= card_id < len(TAROT_CARDS) else f"Card {card_id}"
        card_info_list.append({
            "label": LABELS[pos],
            "card_id": card_id,
            "card_name": card_name,
            "is_reversed": is_reversed,
            "position": pos,
        })

    # 1회 통합 Gemini 호출
    ai_combined = _get_ai_fortunes_combined(card_info_list, category, name)

    results = []
    for idx, info in enumerate(card_info_list):
        ai_card = None
        if ai_combined and isinstance(ai_combined, dict):
            cards_list = ai_combined.get("cards", [])
            if idx < len(cards_list):
                ai_card = cards_list[idx]

        if ai_card and isinstance(ai_card, dict):
            results.append({
                "label": info["label"],
                "card_id": info["card_id"],
                "card_name": info["card_name"],
                "is_reversed": info["is_reversed"],
                "subtitle": ai_card.get("subtitle", ""),
                "message": ai_card.get("message", f"{category} ({info['label']}) 운세입니다."),
                "keywords": ai_card.get("keywords", []),
                "flow_word": ai_card.get("flow_word", info["label"]),
            })
        else:
            results.append({
                "label": info["label"],
                "card_id": info["card_id"],
                "card_name": info["card_name"],
                "is_reversed": info["is_reversed"],
                "subtitle": info["card_name"],
                "message": f"{info['card_name']} 카드가 {info['label']}를 비추고 있습니다. {category}에 대한 {info['label']}의 기운을 느껴보세요.",
                "keywords": [info["card_name"]],
                "flow_word": info["label"],
            })

        fortune = (Fortunes.select().where(
            Fortunes.card_id == info["card_id"],
            Fortunes.category == category,
            Fortunes.position == info["position"]
        ).first())
        if fortune:
            try:
                Draws.create(user_id=user.user_id, category=category, card_id=info["card_id"], position=info["position"], created_at=now)
            except Exception as e:
                print(f"Draw record error: {e}")

    flow_words = [r["flow_word"] for r in results]
    closing_message = ""
    if ai_combined and isinstance(ai_combined, dict):
        closing_message = ai_combined.get("closing", "")

    cards_str = ", ".join([r["card_name"] for r in results])
    summary = f"{category} - " + " / ".join([f"{r['label']}: {r['card_name']}" for r in results])
    ids_str = ",".join([str(info["card_id"]) for info in card_info_list])
    resp_data = dict(user_id=user.user_id, name=user.name, category=category, results=results, flow_words=flow_words, closing_message=closing_message)
    _save_history(cards_str, summary[:200], card_ids=ids_str, result_data=json.dumps(resp_data, ensure_ascii=False))

    wiz.response.status(200,
        user_id=user.user_id,
        name=user.name,
        category=category,
        results=results,
        flow_words=flow_words,
        closing_message=closing_message
    )
