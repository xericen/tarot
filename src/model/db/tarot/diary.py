import peewee as pw
base = wiz.model("portal/season/orm").base("tarot_db")

class Model(base):
    class Meta:
        db_table = 'diary'

    diary_id      = pw.BigAutoField()
    user_id       = pw.IntegerField(index=True)
    diary_date    = pw.DateField(index=True)              # 다이어리가 가리키는 날짜 (YYYY-MM-DD)
    title         = pw.CharField(max_length=200)
    content       = pw.TextField()
    mood          = pw.CharField(max_length=20, null=True)        # 사용자가 선택한 기분 이모지/태그
    sentiment     = pw.CharField(max_length=20, null=True)        # AI 감정 카테고리 (joy/sad/...)
    sentiment_score = pw.FloatField(null=True)                    # -1.0 ~ 1.0
    ai_summary    = pw.TextField(null=True)                       # AI 1줄 요약
    related_draw_id = pw.BigIntegerField(null=True)               # 관련 타로 기록 (draws.draw_id)
    created_at    = pw.DateTimeField(default=__import__('datetime').datetime.now)
    updated_at    = pw.DateTimeField(default=__import__('datetime').datetime.now)
