import json
import datetime

Users = wiz.model("db/login/users")
TarotHistory = wiz.model("db/login/tarot_history")
session = wiz.model("portal/season/session").use()

def profile():
    user_id = session.get("id")
    if not user_id:
        wiz.response.status(401, message="로그인이 필요합니다.")

    try:
        user = Users.get(Users.id == int(user_id))
    except Users.DoesNotExist:
        wiz.response.status(404, message="사용자를 찾을 수 없습니다.")

    history_rows = (TarotHistory
        .select()
        .where(TarotHistory.user_id == int(user_id))
        .order_by(TarotHistory.created_at.desc())
        .limit(50))

    history = []
    for row in history_rows:
        history.append({
            "id": row.id,
            "tarot_type": row.tarot_type,
            "cards": row.cards,
            "card_ids": row.card_ids if row.card_ids else "",
            "result_summary": row.result_summary,
            "mood_tags": row.mood_tags if row.mood_tags else "",
            "created_at": row.created_at.strftime("%Y-%m-%d %H:%M") if row.created_at else ""
        })

    wiz.response.status(200, **{
        "name": user.name,
        "email": user.email,
        "history": history
    })


def logout():
    session.clear()
    wiz.response.status(200, message="로그아웃 성공")

def save_mood():
    history_id = wiz.request.query("history_id", True)
    mood_tags = wiz.request.query("mood_tags", "")
    user_id = session.get("id")
    if not user_id:
        wiz.response.status(401, message="로그인이 필요합니다.")

    try:
        row = TarotHistory.get(
            (TarotHistory.id == int(history_id)) &
            (TarotHistory.user_id == int(user_id))
        )
        row.mood_tags = mood_tags
        row.save()
    except TarotHistory.DoesNotExist:
        wiz.response.status(404, message="기록을 찾을 수 없습니다.")
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, message="저장 완료")

def stats():
    user_id = session.get("id")
    if not user_id:
        wiz.response.status(401, message="로그인이 필요합니다.")

    period = wiz.request.query("period", "all")

    import datetime
    query = TarotHistory.select().where(TarotHistory.user_id == int(user_id))
    now = datetime.datetime.now()
    if period == "week":
        since = now - datetime.timedelta(days=7)
        query = query.where(TarotHistory.created_at >= since)
    elif period == "month":
        since = now - datetime.timedelta(days=30)
        query = query.where(TarotHistory.created_at >= since)
    elif period == "3month":
        since = now - datetime.timedelta(days=90)
        query = query.where(TarotHistory.created_at >= since)

    rows = list(query)
    total = len(rows)

    card_count = {}
    suit_count = {"Major Arcana": 0, "Wands": 0, "Cups": 0, "Swords": 0, "Pentacles": 0}
    mood_card_map = {}

    for row in rows:
        cards = [c.strip() for c in row.cards.split(",") if c.strip()]
        moods = [m.strip() for m in (row.mood_tags or "").split(",") if m.strip()]

        for card in cards:
            card_count[card] = card_count.get(card, 0) + 1
            if "of Wands" in card or card in ["Ace of Wands"]:
                suit_count["Wands"] += 1
            elif "of Cups" in card:
                suit_count["Cups"] += 1
            elif "of Swords" in card:
                suit_count["Swords"] += 1
            elif "of Pentacles" in card:
                suit_count["Pentacles"] += 1
            else:
                suit_count["Major Arcana"] += 1

            for mood in moods:
                if mood not in mood_card_map:
                    mood_card_map[mood] = {}
                mood_card_map[mood][card] = mood_card_map[mood].get(card, 0) + 1

    top_cards = sorted(card_count.items(), key=lambda x: -x[1])[:5]

    mood_patterns = {}
    for mood, cards in mood_card_map.items():
        top = sorted(cards.items(), key=lambda x: -x[1])[:3]
        mood_patterns[mood] = [{"card": c, "count": n} for c, n in top]

    wiz.response.status(200,
        total=total,
        top_cards=[{"card": c, "count": n} for c, n in top_cards],
        suit_distribution=suit_count,
        mood_patterns=mood_patterns
    )

def detail():
    history_id = wiz.request.query("history_id", True)
    user_id = session.get("id")
    if not user_id:
        wiz.response.status(401, message="로그인이 필요합니다.")

    try:
        row = TarotHistory.get(
            (TarotHistory.id == int(history_id)) &
            (TarotHistory.user_id == int(user_id))
        )
    except TarotHistory.DoesNotExist:
        wiz.response.status(404, message="기록을 찾을 수 없습니다.")
    except Exception as e:
        wiz.response.status(400, message=str(e))

    result_data = None
    if row.result_data:
        try:
            result_data = json.loads(row.result_data)
        except Exception:
            result_data = row.result_data

    wiz.response.status(200, result_data=result_data)
