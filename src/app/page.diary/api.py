import datetime
import json as _json

Diary = wiz.model("db/tarot/diary")
TarotHistory = wiz.model("db/login/tarot_history")
session = wiz.model("portal/season/session").use()

KST = datetime.timezone(datetime.timedelta(hours=9))


def _require_user():
    user_id = session.get("id")
    if not user_id:
        wiz.response.status(401, message="로그인이 필요합니다.")
    return int(user_id)


def _to_dict(row):
    return {
        "diary_id": row.diary_id,
        "user_id": row.user_id,
        "diary_date": row.diary_date.strftime("%Y-%m-%d") if row.diary_date else "",
        "title": row.title,
        "content": row.content,
        "mood": row.mood or "",
        "sentiment": row.sentiment or "",
        "sentiment_score": row.sentiment_score,
        "ai_summary": row.ai_summary or "",
        "related_draw_id": row.related_draw_id,
        "created_at": row.created_at.strftime("%Y-%m-%d %H:%M") if row.created_at else "",
        "updated_at": row.updated_at.strftime("%Y-%m-%d %H:%M") if row.updated_at else "",
    }


def list():
    user_id = _require_user()
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 30))
    rows = (Diary
        .select()
        .where(Diary.user_id == user_id)
        .order_by(Diary.diary_date.desc(), Diary.created_at.desc())
        .paginate(page, dump))
    total = Diary.select().where(Diary.user_id == user_id).count()
    items = [_to_dict(r) for r in rows]

    # 관련 타로 카드 정보 첨부
    draw_ids = [it["related_draw_id"] for it in items if it.get("related_draw_id")]
    history_map = {}
    if draw_ids:
        try:
            for h in TarotHistory.select().where(TarotHistory.id.in_(draw_ids)):
                history_map[h.id] = {
                    "tarot_type": h.tarot_type,
                    "cards": h.cards,
                    "result_summary": (h.result_summary or "")[:120]
                }
        except Exception:
            pass
    for it in items:
        rid = it.get("related_draw_id")
        it["related_tarot"] = history_map.get(rid) if rid else None

    wiz.response.status(200, items=items, total=total, page=page, dump=dump)


def get():
    user_id = _require_user()
    diary_id = int(wiz.request.query("diary_id", True))
    try:
        row = Diary.get((Diary.diary_id == diary_id) & (Diary.user_id == user_id))
    except Diary.DoesNotExist:
        wiz.response.status(404, message="다이어리를 찾을 수 없습니다.")
    item = _to_dict(row)
    if item.get("related_draw_id"):
        try:
            h = TarotHistory.get(TarotHistory.id == item["related_draw_id"])
            item["related_tarot"] = {
                "tarot_type": h.tarot_type,
                "cards": h.cards,
                "card_ids": h.card_ids if h.card_ids else "",
                "result_summary": h.result_summary
            }
        except Exception:
            item["related_tarot"] = None
    wiz.response.status(200, item=item)


def list_recent_tarot():
    """다이어리 작성 시 연결할 수 있는 최근 타로 기록 (최근 20건)"""
    user_id = _require_user()
    rows = (TarotHistory
        .select()
        .where(TarotHistory.user_id == user_id)
        .order_by(TarotHistory.created_at.desc())
        .limit(20))
    items = []
    for r in rows:
        items.append({
            "id": r.id,
            "tarot_type": r.tarot_type,
            "cards": r.cards,
            "result_summary": (r.result_summary or "")[:80],
            "created_at": r.created_at.strftime("%Y-%m-%d") if r.created_at else "",
        })
    wiz.response.status(200, items=items)


def _analyze_sentiment(title, content):
    """Gemini로 감정 분석. 실패 시 None 반환."""
    try:
        from google import genai
        import os
        key = os.environ.get("GEMINI_API_KEY", "")
        if not key:
            try:
                key = open("/opt/app/data/gemini_key.txt").read().strip()
            except Exception:
                pass
        if not key:
            return None

        i18n = wiz.model("i18n")
        lang_label = i18n["lang_label"]()
        lang_instruction = i18n["lang_instruction"]()

        client = genai.Client(api_key=key)
        prompt = f"""다음 다이어리를 분석해주세요.

제목: {title}
본문: {content}

다음 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{{
  "sentiment": "감정 카테고리 (joy/sad/angry/anxious/calm/excited/neutral 중 하나, 영어 키 그대로)",
  "sentiment_score": "-1.0 ~ 1.0 사이의 실수 (음수=부정적, 양수=긍정적, 0=중립)",
  "summary": "본문 핵심을 한 줄(40자 이내)로 요약"
}}

⚠️ 출력 언어: {lang_label}
{lang_instruction}
sentiment 키 값은 반드시 영문 카테고리 그대로 두고, summary 값만 위 언어로 작성하세요."""
        try:
            resp = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        except Exception:
            resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
        text = (resp.text or "").strip()
        if "```" in text:
            for block in text.split("```")[1:]:
                block = block.strip()
                if block.startswith("json"):
                    block = block[4:].strip()
                if block.startswith("{"):
                    text = block
                    break
        data = _json.loads(text)
        sentiment = data.get("sentiment", "neutral")
        try:
            score = float(data.get("sentiment_score", 0))
        except Exception:
            score = 0.0
        score = max(-1.0, min(1.0, score))
        summary = (data.get("summary") or "")[:200]
        return {"sentiment": sentiment, "sentiment_score": score, "summary": summary}
    except Exception as e:
        print(f"sentiment analyze error: {e}")
        return None


def save():
    user_id = _require_user()
    diary_id = wiz.request.query("diary_id", "")
    diary_date = wiz.request.query("diary_date", "").strip()
    title = (wiz.request.query("title", "") or "").strip()
    content = (wiz.request.query("content", "") or "").strip()
    mood = (wiz.request.query("mood", "") or "").strip()
    related_draw_id = wiz.request.query("related_draw_id", "")

    if not title:
        wiz.response.status(400, message="제목을 입력해주세요.")
    if not content:
        wiz.response.status(400, message="내용을 입력해주세요.")
    if not diary_date:
        diary_date = datetime.datetime.now(KST).strftime("%Y-%m-%d")

    # 날짜 파싱
    try:
        dt = datetime.datetime.strptime(diary_date, "%Y-%m-%d").date()
    except Exception:
        wiz.response.status(400, message="날짜 형식이 올바르지 않습니다.")

    related = None
    if related_draw_id:
        try:
            related = int(related_draw_id)
        except Exception:
            related = None

    # AI 감정 분석
    analysis = _analyze_sentiment(title, content) or {}

    now = datetime.datetime.now()
    if diary_id and str(diary_id).isdigit():
        # 수정
        try:
            row = Diary.get((Diary.diary_id == int(diary_id)) & (Diary.user_id == user_id))
        except Diary.DoesNotExist:
            wiz.response.status(404, message="다이어리를 찾을 수 없습니다.")
        row.diary_date = dt
        row.title = title[:200]
        row.content = content
        row.mood = mood[:20] if mood else None
        row.sentiment = analysis.get("sentiment")
        row.sentiment_score = analysis.get("sentiment_score")
        row.ai_summary = analysis.get("summary")
        row.related_draw_id = related
        row.updated_at = now
        row.save()
        result_id = row.diary_id
    else:
        # 신규
        row = Diary.create(
            user_id=user_id,
            diary_date=dt,
            title=title[:200],
            content=content,
            mood=mood[:20] if mood else None,
            sentiment=analysis.get("sentiment"),
            sentiment_score=analysis.get("sentiment_score"),
            ai_summary=analysis.get("summary"),
            related_draw_id=related,
            created_at=now,
            updated_at=now,
        )
        result_id = row.diary_id

    wiz.response.status(200, diary_id=result_id, analysis=analysis)


def remove():
    user_id = _require_user()
    diary_id = int(wiz.request.query("diary_id", True))
    try:
        row = Diary.get((Diary.diary_id == diary_id) & (Diary.user_id == user_id))
    except Diary.DoesNotExist:
        wiz.response.status(404, message="다이어리를 찾을 수 없습니다.")
    row.delete_instance()
    wiz.response.status(200, message="삭제되었습니다.")


def stats():
    """감정 통계 (최근 90일)"""
    user_id = _require_user()
    since = datetime.date.today() - datetime.timedelta(days=90)
    rows = (Diary
        .select()
        .where((Diary.user_id == user_id) & (Diary.diary_date >= since))
        .order_by(Diary.diary_date.asc()))
    counts = {}
    timeline = []
    for r in rows:
        s = r.sentiment or "neutral"
        counts[s] = counts.get(s, 0) + 1
        timeline.append({
            "date": r.diary_date.strftime("%Y-%m-%d"),
            "score": r.sentiment_score if r.sentiment_score is not None else 0
        })
    wiz.response.status(200, counts=counts, timeline=timeline, total=len(timeline))
