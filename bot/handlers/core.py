from aiogram import Router

from other.lessons import Lessons
import other.log.colors as colors
import other.log.logging as logging
from middlewares.logging_requests import LoggingMessageMiddleware, LoggingCallbackQueryMiddleware

lessons: Lessons = Lessons()

router = Router(name=__name__)
router.message.middleware(LoggingMessageMiddleware())
router.callback_query.middleware(LoggingCallbackQueryMiddleware())

log = logging.logging(Name='HANDLER', Color=colors.green)


def GetRouter() -> Router: return router


def GetLessons() -> Lessons: return lessons
