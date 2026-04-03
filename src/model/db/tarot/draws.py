import peewee as pw
base = wiz.model("portal/season/orm").base("tarot_db")

class Model(base):
    class Meta:
        db_table = 'draws'

    draw_id = pw.BigAutoField()
    user_id = pw.IntegerField()
    card_id = pw.IntegerField()
