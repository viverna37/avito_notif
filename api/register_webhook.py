"""Регистрация вебхука в Avito.

Запуск:
  python -m api.register_webhook

Перед запуском:
- в .env должны быть AVITO_CLIENT_ID / AVITO_CLIENT_SECRET
- API_URL должен указывать на публичный URL твоего сервиса (https://...)
- WEBHOOK_TOKEN должен совпадать с secret, который ты задаёшь при регистрации вебхука

После регистрации Avito начнет слать события на:
  {API_URL}/avito/webhook
"""

import asyncio

from api.config import load_config
from api.services.avito_client import AvitoClient


async def main() -> None:
    config = load_config()

    # куда Avito будет стучаться
    webhook_url = f"{config.api.base_url.rstrip('/')}/avito/webhook"

    avito = AvitoClient(
        client_id=config.avito.client_id,
        client_secret=config.avito.client_secret,
        token_url="https://api.avito.ru/token",
    )

    res = await avito.register_webhook(
        register_url="https://api.avito.ru/messenger/v3/webhook",
        webhook_url=webhook_url,
        secret=config.api.webhook_token,
    )

    print("Webhook registered:")
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
