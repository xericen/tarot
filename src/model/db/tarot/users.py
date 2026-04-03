import peewee as pw
base = wiz.model("portal/season/orm").base("tarot_db")

class Model(base):   # 반드시 이름이 Model 이어야 함
    class Meta:
        db_table = 'users'

    user_id   = pw.AutoField()            # AUTO_INCREMENT PK
    name      = pw.CharField(max_length=80)
    created_at = pw.TimestampField()
