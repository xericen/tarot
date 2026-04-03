import peewee as pw
base = wiz.model("portal/season/orm").base("tarot_db")

class Model(base):
    class Meta:
        db_table = 'fortunes'

    card_id = pw.IntegerField(primary_key=True)
    message = pw.TextField()
