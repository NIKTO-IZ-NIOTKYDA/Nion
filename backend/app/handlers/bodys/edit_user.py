from handlers.bodys.core import Core

class Body(Core):
    username: str
    first_name: str | None
    last_name: str | None
    send_notifications: bool
    role_ids: list[int]
