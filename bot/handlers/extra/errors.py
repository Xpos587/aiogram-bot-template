import logging
from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram_i18n import I18nContext

router: Final[Router] = Router(name=__name__)

logger: logging.Logger = logging.getLogger(__name__)


@router.error(ExceptionTypeFilter(Exception), F.update.message)
async def handle_some_error(error: ErrorEvent, i18n: I18nContext) -> Any:
    logger.error(
        f"{error.exception} occurred at "
        f"{error.exception.__traceback__.tb_frame.f_code.co_filename}:"
        f"{error.exception.__traceback__.tb_lineno}"
    )
    return error.update.message.answer(text=i18n.something_went_wrong())
