from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from google import genai
import json

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
            TarotHistory.create(user_id=int(user_id), tarot_type="yearly", cards=cards_str, card_ids=card_ids, result_summary=summary, result_data=result_data)
    except Exception:
        pass

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

SEASONS = ["봄", "여름", "가을", "겨울"]

def yearly_fortune():
    name = (wiz.request.query("name", True) or "").strip()
    love_status = wiz.request.query("love_status", True) or ""
    job_status = wiz.request.query("job_status", True) or ""
    selected = wiz.request.query("selected", True) or ""
    reversed_str = wiz.request.query("reversed", "") or ""

    if not name:
        wiz.response.status(400, message="name is required")
    if not selected:
        wiz.response.status(400, message="selected cards required")

    selected_ids = [int(x) for x in selected.split(",") if x.isdigit()]
    if len(selected_ids) != 4:
        wiz.response.status(400, message="exactly 4 cards must be selected")

    reversed_flags = []
    if reversed_str:
        reversed_flags = [x.strip().lower() == "true" for x in reversed_str.split(",")]
    while len(reversed_flags) < len(selected_ids):
        reversed_flags.append(False)

    results = []
    card_info_list = []
    for i, (season, card_id) in enumerate(zip(SEASONS, selected_ids)):
        card_name = TAROT_CARDS[card_id] if 0 <= card_id < len(TAROT_CARDS) else f"Card {card_id}"
        is_reversed = reversed_flags[i]
        reversed_text = "(역방향/Reversed)" if is_reversed else "(정방향/Upright)"
        card_info_list.append({
            "season": season,
            "card_id": card_id,
            "card_name": card_name,
            "is_reversed": is_reversed,
            "reversed_text": reversed_text,
        })

    # 단일 프롬프트로 4계절 운세 한번에 요청
    cards_desc = "\n".join([
        f"- {c['season']}: '{c['card_name']}' {c['reversed_text']}"
        for c in card_info_list
    ])
    try:
        prompt = f"""당신은 전문 타로 리더입니다. '{name}'님의 연간 타로 운세입니다.
연애 상태: {love_status}, 직업 상태: {job_status}

4계절에 각각 다음 카드가 선택되었습니다:
{cards_desc}

역방향(Reversed) 카드는 역방향의 의미를 반영하여 해석해주세요.
각 시즌의 운세를 한국어로 3-4문장으로 구체적이고 따뜻하게 알려주세요.

반드시 아래 JSON 배열 형식으로만 응답하세요. 다른 텍스트 없이 JSON만 출력하세요:
[{{"season":"봄","message":"운세 내용"}},{{"season":"여름","message":"운세 내용"}},{{"season":"가을","message":"운세 내용"}},{{"season":"겨울","message":"운세 내용"}}]"""
        def _call():
            return _ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        with ThreadPoolExecutor(max_workers=1) as ex:
            response = ex.submit(_call).result(timeout=20)
        raw = response.text.strip()
        # JSON 블록 추출
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        ai_results = json.loads(raw)
    except Exception as e:
        print(f"AI fortune error: {e}")
        ai_results = None

    season_map = {}
    if ai_results and isinstance(ai_results, list):
        for item in ai_results:
            season_map[item.get("season", "")] = item.get("message", "")

    for c in card_info_list:
        message = season_map.get(c["season"], f"{c['card_name']} 카드가 {c['season']}에 나왔습니다.")
        results.append({
            "season": c["season"],
            "card_id": c["card_id"],
            "card_name": c["card_name"],
            "is_reversed": c["is_reversed"],
            "message": message,
            "image_url": f"/assets/TarotCard/{c['card_id']}.jpg"
        })

    cards_str = ", ".join([r["card_name"] for r in results])
    summary = " / ".join([f"{r['season']}: {r['card_name']}" for r in results])
    ids_str = ",".join([str(r["card_id"]) for r in results])
    resp_data = dict(name=name, love_status=love_status, job_status=job_status, results=results)
    _save_history(cards_str, summary[:200], card_ids=ids_str, result_data=json.dumps(resp_data, ensure_ascii=False))

    wiz.response.status(200,
        name=name,
        love_status=love_status,
        job_status=job_status,
        results=results
    )
