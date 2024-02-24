import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from bot.settings import settings


async def to_admins(bot: Bot, text: str, **kwargs) -> None:
    admin_ids = settings.get_admin_ids()
    tasks = []
    for user_id in admin_ids:
        tasks.append(send_message(bot, user_id, text, **kwargs))
    await asyncio.gather(*tasks)


async def send_message(bot: Bot, user_id: int, text: str, **kwargs) -> None:
    try:
        await bot.send_message(user_id, text, **kwargs)
    except TelegramBadRequest as e:
        if "chat not found" in str(e):
            return
        raise
