from handlers.bodies.core import Core


class Body(Core):
    username: str
    first_name: str | None
    last_name: str | None
    send_notifications: bool
    blocked_bot: bool
    role_ids: list[int]
