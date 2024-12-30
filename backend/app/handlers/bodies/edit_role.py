from handlers.bodies.core import Core


class Body(Core):
    RoleID: int
    user_ids: list[int]
    name: str
    permissions: dict
