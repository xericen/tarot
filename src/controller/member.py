# auth controller
class Controller(wiz.controller("base")):
    def __init__(self):
        super().__init__()
        if not wiz.session.has("id"):
            wiz.response.status(401, message="login required")

        # DB에 유저가 실제 존재하는지 검증 (세션-DB 불일치 방지)
        try:
            Users = wiz.model("db/login/users")
            user_id = wiz.session.get("id")
            Users.get(Users.id == int(user_id))
        except Exception:
            wiz.session.clear()
        if not wiz.session.has("id"):
            wiz.response.status(401, message="login required")
