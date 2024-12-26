from aiogram import Router

from other.lessons import Lessons
import other.log.colors as colors
import other.log.logging as logging

lessons: Lessons = Lessons()
router = Router(name=__name__)
admin_router = Router(name=__name__)
log = logging.logging(Name='HANDLER', Color=colors.green)


def GetRouter() -> Router: return router


def GetLessons() -> Lessons: return lessons
