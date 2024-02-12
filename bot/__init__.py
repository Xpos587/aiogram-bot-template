from aiogram import Bot as _Bot

from bot.settings import Settings


class Bot(_Bot):
    settings: Settings
