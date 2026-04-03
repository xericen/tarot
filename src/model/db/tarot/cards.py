import peewee as pw
base = wiz.model("portal/season/orm").base("tarot_db")

class Model(base):
    class Meta:
        db_table = 'cards'

    id = pw.BigAutoField()                  # 자동 증가 기본키
    card_name = pw.CharField(max_length=100)
