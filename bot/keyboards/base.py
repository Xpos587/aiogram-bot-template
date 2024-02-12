from typing import Optional, Union

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder,
)


class Button:
    def __init__(
        self,
        text: str,
        callback_data: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.text = text
        self.callback_data = callback_data
        self.url = url


def common_keyboard(
    buttons: list[Button],
    is_inline: bool = True,
    is_persistent: Optional[bool] = None,
    resize_keyboard: bool = True,
    one_time_keyboard: Optional[bool] = None,
    input_field_placeholder: Optional[str] = None,
    selective: Optional[bool] = None,
    row_width: int = 1,
) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
    """
    Common keyboards builder helper.
    """
    if is_inline:
        inline_keyboard = InlineKeyboardBuilder()
        inline_temp_row = []
        for button in buttons:
            inline_temp_row.append(
                InlineKeyboardButton(
                    text=button.text,
                    callback_data=button.callback_data,
                    url=button.url,
                )
            )
            if len(inline_temp_row) == row_width:
                inline_keyboard.row(*inline_temp_row)
                inline_temp_row = []
        if inline_temp_row:
            inline_keyboard.row(*inline_temp_row)
    else:
        reply_keyboard = ReplyKeyboardBuilder()
        reply_temp_row = []
        for button in buttons:
            reply_temp_row.append(KeyboardButton(text=button.text))
            if len(reply_temp_row) == row_width:
                reply_keyboard.row(*reply_temp_row)
                reply_temp_row = []
        if reply_temp_row:
            reply_keyboard.row(*reply_temp_row)

    return reply_keyboard.as_markup(
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        selective=selective,
    )


__all__ = ["ReplyKeyboardRemove"]
