from handlers.bodys.core import Core

class Body(Core):
    lessons_id: str
    homework: str | None
    photo: list[int] | None
    url: str | None
