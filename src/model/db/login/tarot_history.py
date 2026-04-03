import peewee as pw
base = wiz.model("portal/season/orm").base("login_db")

class Model(base):
    class Meta:
        db_table = 'tarot_history'

    id = pw.BigAutoField()
    user_id = pw.BigIntegerField(index=True)
    tarot_type = pw.CharField(max_length=32)
    cards = pw.TextField()
    card_ids = pw.CharField(max_length=255, default='')
    result_summary = pw.TextField(null=True)
    result_data = pw.TextField(null=True)
    mood_tags = pw.CharField(max_length=255, default='')
    created_at = pw.DateTimeField(constraints=[pw.SQL('DEFAULT CURRENT_TIMESTAMP')])
