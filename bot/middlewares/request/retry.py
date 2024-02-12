import asyncio
import logging
from typing import Final

from aiogram import Bot
from aiogram.client.session.middlewares.base import (
    BaseRequestMiddleware,
    NextRequestMiddlewareType,
)
from aiogram.dispatcher.dispatcher import DEFAULT_BACKOFF_CONFIG
from aiogram.exceptions import (
    RestartingTelegram,
    TelegramBadRequest,
    TelegramNetworkError,
    TelegramRetryAfter,
    TelegramServerError,
)
from aiogram.methods import AnswerCallbackQuery, Response, TelegramMethod
from aiogram.methods.base import TelegramType
from aiogram.utils.backoff import Backoff, BackoffConfig

logger: logging.Logger = logging.getLogger(__name__)
DEFAULT_MAX_RETRIES: Final[int] = 7


async def bad_req(
    e: TelegramBadRequest,
    bot: Bot,
    make_request: NextRequestMiddlewareType[TelegramType],
    method: TelegramMethod[TelegramType],
) -> None:
    if "message is not modified" in str(e):
        logger.info("Message not modified, skipping retry.")
    elif "query is too old" in str(e):
        logger.info("Query is too old, skipping retry.")
        pass
    elif "can't parse entities" in str(e) and hasattr(method, "parse_mode"):
        original_parse_mode = method.parse_mode
        method.parse_mode = None
        try:
            await make_request(bot, method)
        finally:
            method.parse_mode = original_parse_mode


class RetryRequestMiddleware(BaseRequestMiddleware):
    backoff_config: BackoffConfig
    max_retries: int

    __slots__ = ("backoff_config", "max_retries")

    def __init__(
        self,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self.backoff_config = backoff_config
        self.max_retries = max_retries

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[TelegramType],
        bot: Bot,
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:
        backoff: Backoff = Backoff(config=self.backoff_config)
        retries: int = 0

        while True:
            retries += 1
            try:
                return await make_request(bot, method)
            except TelegramRetryAfter as e:
                if isinstance(method, AnswerCallbackQuery):
                    raise
                if retries == self.max_retries:
                    raise
                logger.error(
                    "Request '%s' failed due to rate limit."
                    "Sleeping %s seconds.",
                    type(method).__name__,
                    e.retry_after,
                )
                backoff.reset()
                await asyncio.sleep(e.retry_after)

            except TelegramBadRequest as e:
                await bad_req(e, bot, make_request, method)
                raise

            except (
                TelegramServerError,
                RestartingTelegram,
                TelegramNetworkError,
            ) as e:
                if retries == self.max_retries:
                    raise
                logger.error(
                    "Request '%s' failed due to %s - %s. Sleeping %s seconds.",
                    type(method).__name__,
                    type(e).__name__,
                    e,
                    backoff.next_delay,
                )
                await backoff.asleep()
