from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from redis.asyncio import ConnectionPool, Redis

from bot.enums import Locale
from bot.handlers import admin, extra, main
from bot.middlewares import (
    DBSessionMiddleware,
    OuterMiddleware,
    RetryRequestMiddleware,
    UserManager,
    UserMiddleware,
)
from services.database import create_pool
from utils import mjson

if TYPE_CHECKING:
    from bot.settings import Settings


def _setup_outer_middlewares(
    dispatcher: Dispatcher, settings: Settings
) -> None:
    pool = dispatcher["session_pool"] = create_pool(
        dsn=settings.build_postgres_dsn(),
        enable_logging=settings.sqlalchemy_logging,
    )
    i18n_middleware = dispatcher["i18n_middleware"] = I18nMiddleware(
        core=FluentRuntimeCore(
            path="lang/{locale}",
            raise_key_error=False,
            locales_map={Locale.RU: Locale.US},
        ),
        manager=UserManager(),
        default_locale=Locale.DEFAULT,
    )

    dispatcher.update.outer_middleware(DBSessionMiddleware(session_pool=pool))
    dispatcher.update.outer_middleware(UserMiddleware())
    dispatcher.update.outer_middleware(OuterMiddleware())
    i18n_middleware.setup(dispatcher=dispatcher)


def _setup_inner_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())


def create_dispatcher(settings: Settings) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with
    installed middlewares and included routers
    """
    redis: Redis = Redis(
        connection_pool=ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            username=settings.redis_user,
            password=settings.redis_password,
        )
    )

    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(
            redis=redis, json_loads=mjson.decode, json_dumps=mjson.encode
        ),
        redis=redis,
        settings=settings,
    )
    dispatcher.include_routers(admin.router, main.router, extra.router)
    _setup_outer_middlewares(dispatcher=dispatcher, settings=settings)
    _setup_inner_middlewares(dispatcher=dispatcher)
    return dispatcher


def create_bot(settings: Settings) -> Bot:
    """
    :return: Configured ``Bot`` with retry request middleware
    """
    session: AiohttpSession = AiohttpSession(
        json_loads=mjson.decode, json_dumps=mjson.encode
    )
    session.middleware(RetryRequestMiddleware())
    return Bot(
        token=settings.bot_token.get_secret_value(),
        parse_mode=ParseMode.HTML,
        session=session,
    )
