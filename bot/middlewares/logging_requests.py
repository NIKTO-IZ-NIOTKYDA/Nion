from typing import (
    Callable,
    Dict,
    Any,
    Awaitable
)

from aiogram import BaseMiddleware
from aiogram.types import Message

from other.log.colors import purple
from other.log.logging import logging


class LoggingMessageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = logging(Name='MW', Color=purple)


    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        self.logger.info(str(data['event_context'].user.id), f'Received \'{data['event_update'].message.text}\'')

        return await handler(event, data)


class LoggingCallbackQueryMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = logging(Name='MW', Color=purple)


    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        self.logger.info(str(data['event_context'].user.id), f'Received [\'{data['event_update'].callback_query.data}\']')

        return await handler(event, data)
