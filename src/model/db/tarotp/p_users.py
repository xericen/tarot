import peewee as pw
base = wiz.model("portal/season/orm").base("tarotp_db")

class Model(base):  
    class Meta:
        db_table = 'p_users'

    user_id    = pw.AutoField()                       # AUTO_INCREMENT PK
    name       = pw.CharField(max_length=80)
    created_at = pw.TimestampField()
