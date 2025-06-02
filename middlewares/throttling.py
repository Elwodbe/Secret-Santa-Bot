from aiogram import BaseMiddleware, types
from aiogram.dispatcher.flags import get_flag
from aiogram.exceptions import Throttled
from aiogram.types import Message
from aiogram.dispatcher.event.handler import CancelHandler


from typing import Callable, Dict, Any
import asyncio


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 1.0, key_prefix: str = "antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Any],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        dispatcher = data["dispatcher"]
        limit = get_flag(handler, "throttling_rate_limit") or self.rate_limit
        key = get_flag(handler, "throttling_key") or f"{self.prefix}{handler.__name__}"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as throttled:
            await self.message_throttled(event, throttled)
            raise CancelHandler()
        return await handler(event, data)

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        if throttled.exceeded_count <= 2:
            await message.reply("Too many requests!")
