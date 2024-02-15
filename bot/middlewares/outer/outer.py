from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.filters import ChatStates


class OuterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        state: FSMContext = data["state"]

        if isinstance(event, CallbackQuery):
            await state.set_state(ChatStates.ReadyToRespond)
        elif isinstance(event, Message):
            message: Message = event
            if message.text and message.text.startswith("/"):
                await message.delete()
                await state.set_state(ChatStates.ReadyToRespond)

        return await handler(event, data)
