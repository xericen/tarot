import peewee as pw
base = wiz.model("portal/season/orm").base("tarotp_db")

class Model(base): 
    class Meta:
        db_table = 'p_fortunes'

    fortune_id = pw.AutoField()                       # AUTO_INCREMENT PK
    card_id    = pw.IntegerField()                    # cards.id FK
    category   = pw.CharField(max_length=20)          # 사업운/애정운/학업운/취업운
    position   = pw.CharField(max_length=10)          # past/present/future
    message    = pw.TextField()
