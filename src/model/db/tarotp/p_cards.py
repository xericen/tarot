import peewee as pw
base = wiz.model("portal/season/orm").base("tarotp_db")

class Model(base): 
    class Meta:
        db_table = 'p_cards'

    id          = pw.IntegerField(primary_key=True) 
    card_name   = pw.CharField(max_length=100)
    description = pw.TextField(null=True)          
