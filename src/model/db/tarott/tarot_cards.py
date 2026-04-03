import peewee as pw

base = wiz.model("portal/season/orm").base("tarott_db")

class Model(base):
    class Meta:
        db_table = 'tarot_cards'

    id          = pw.AutoField()                      # AUTO_INCREMENT PK
    name        = pw.CharField(max_length=100)        # 카드 이름
    description = pw.TextField()                      # 카드 설명
