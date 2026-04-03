import peewee as pw
base = wiz.model("portal/season/orm").base("login_db")

class Model(base):
    class Meta:
        db_table = 'users'

    id = pw.BigAutoField()                       # 자동 증가 기본키
    name = pw.CharField(max_length=100, null=False)   # 이름
    email = pw.CharField(max_length=255, unique=True, null=False)  # 이메일(고유)
    password = pw.CharField(max_length=255, null=False)  # 비밀번호 해시
    approved = pw.BooleanField(default=False)    # 관리자 승인 여부
    created_at = pw.DateTimeField(constraints=[pw.SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = pw.DateTimeField(constraints=[pw.SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')])
