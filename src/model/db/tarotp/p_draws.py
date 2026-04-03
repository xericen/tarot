import peewee as pw
base = wiz.model("portal/season/orm").base("tarotp_db")

class Model(base):   
    class Meta:
        db_table = 'p_draws'

    draw_id    = pw.AutoField()                       # AUTO_INCREMENT PK
    user_id    = pw.IntegerField()                    # users.user_id FK
    category   = pw.CharField(max_length=20)          # 사업운/애정운/학업운/취업운
    card_id    = pw.IntegerField()                    # cards.id FK
    position   = pw.CharField(max_length=10)          # past/present/future
    created_at = pw.TimestampField()
