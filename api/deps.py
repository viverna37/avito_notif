from typing import AsyncGenerator, Any

from fastapi import Depends

from api.config import load_config, Config
from api.services.avito_client import AvitoClient
from api.services.telegram import TelegramNotifier
from database.db import db
from database.repository.chats_repository import ChatsRepository


# ---------- DB ----------
async def get_session() -> AsyncGenerator[Any, Any]:
    async with db.session() as session:
        yield session


# ---------- SERVICES ----------
def get_config() -> Config:
    config = load_config()
    return config


def get_avito():
    config = get_config()
    _avito = AvitoClient(config.avito.client_id, config.avito.client_secret, "https://api.avito.ru/token")
    return _avito


def get_tg():
    config = get_config()

    _tg = TelegramNotifier(config.tg_bot.token, config.tg_bot.admin_id)

    return _tg


def get_chats_repository(
        session=Depends(get_session),
) -> ChatsRepository:
    return ChatsRepository(
        session
    )
