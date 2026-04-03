session = wiz.model("portal/season/session").use()

def check():
    user_id = session.get("id")
    if user_id:
        name = session.get("name", "")
        email = session.get("email", "")
        wiz.response.status(200, logged_in=True, name=name, email=email)
    wiz.response.status(200, logged_in=False)
