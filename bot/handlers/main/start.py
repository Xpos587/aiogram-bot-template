from typing import Any, Final

from aiogram import Router
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext

from services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.message(Command("start"))
async def start_command(
    message: Message, i18n: I18nContext, user: DBUser
) -> TelegramMethod[Any]:
    return message.answer(text=i18n.start(name=user.mention))
