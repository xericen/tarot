session = wiz.model("portal/season/session").use()
Users = wiz.model("db/login/users")

def check():
    user_id = session.get("id")
    if user_id:
        try:
            user = Users.get(Users.id == int(user_id))
        except Exception:
            session.clear()
            wiz.response.status(200, logged_in=False)
        wiz.response.status(200, logged_in=True, name=user.name, email=user.email)
    wiz.response.status(200, logged_in=False)
