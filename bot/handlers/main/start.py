from typing import Any, Final

from aiogram import Router
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.enums.callback_query_type import CallbackQueryType as CQT
from bot.keyboards import Button, common_keyboard
from services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.message(Command("start"))
async def start_command(
    message: Message, i18n: I18nContext, user: DBUser
) -> TelegramMethod[Any]:
    return message.answer(
        text=i18n.start(name=user.mention),
        reply_markup=common_keyboard(
            rows=[
                (
                    Button(i18n.btn.orange(), callback_data=CQT.ORANGE),
                    Button(i18n.btn.lime(), callback_data=CQT.LIME),
                ),
                Button(
                    i18n.btn.source(),
                    url="https://github.com/Xpos587/aiogram-template",
                ),
            ]
        ),
    )
