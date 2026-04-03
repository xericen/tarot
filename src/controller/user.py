# auth controller
class Controller(wiz.controller("base")):
    def __init__(self):
        super().__init__()
        if not wiz.session.has("id"):
            wiz.response.status(401, message="login required")
