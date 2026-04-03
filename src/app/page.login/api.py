import datetime

Users = wiz.model("db/login/users")
session = wiz.model("portal/season/session").use()

def join():
    data = wiz.request.query()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if Users.select().where(Users.email == email).exists():
        wiz.response.status(400, message="이미 존재하는 이메일입니다.")

    Users.create(
        name=name,
        email=email,
        password=password,
        approved=True,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    wiz.response.status(200, message="회원가입 성공")


def login():
    data = wiz.request.query()
    email = data.get("email")
    password = data.get("password")

    try:
        user = Users.get(Users.email == email)
    except Users.DoesNotExist:
        wiz.response.status(404, message="존재하지 않는 계정")

    if user.password != password:
        wiz.response.status(401, message="비밀번호가 일치하지 않습니다")

    if not user.approved:
        wiz.response.status(403, message="관리자 승인 후 로그인 가능합니다")

    session.set(id=str(user.id), name=user.name, email=user.email)
    wiz.response.status(200, message="로그인 성공")


def logout():
    session.clear()
    wiz.response.status(200, message="로그아웃 성공")


def verify_reset():
    email = wiz.request.query("email", True)
    name = wiz.request.query("name", True)
    try:
        Users.get((Users.email == email) & (Users.name == name))
    except Users.DoesNotExist:
        wiz.response.status(404, message="이메일과 이름이 일치하는 계정을 찾을 수 없습니다.")
    wiz.response.status(200, message="계정이 확인되었습니다.")

def reset_password():
    data = wiz.request.query()
    email = data.get("email")
    name = data.get("name")
    new_password = data.get("new_password")

    try:
        user = Users.get((Users.email == email) & (Users.name == name))
    except Users.DoesNotExist:
        wiz.response.status(404, message="이메일과 이름이 일치하는 계정을 찾을 수 없습니다.")

    user.password = new_password
    user.updated_at = datetime.datetime.now()
    user.save()

    wiz.response.status(200, message="비밀번호가 성공적으로 변경되었습니다.")
