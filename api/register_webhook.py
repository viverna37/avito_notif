import asyncio
from api.config import settings
from api.services.avito_client import AvitoClient

async def main():
    avito = AvitoClient(settings.avito_client_id, settings.avito_client_secret, settings.avito_token_url)
    res = await avito.register_webhook(
        register_url=settings.avito_register_webhook_url,
        url="https://your-domain.ru/avito/webhook",
        secret=settings.webhook_secret if settings.webhook_secret else None
    )
    print(res)

asyncio.run(main())