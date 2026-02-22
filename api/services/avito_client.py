import time
from typing import Optional

import httpx


class AvitoClient:
    """Мини-клиент Avito:
    - OAuth2 client_credentials (кеширует токен)
    - Получение self account id (user_id) (кеширует)
    - Отправка сообщения в чат
    - Регистрация webhook
    """

    def __init__(self, client_id: str, client_secret: str, token_url: str = "https://api.avito.ru/token"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

        self._token: Optional[str] = None
        self._token_exp: float = 0.0

        self._user_id: Optional[int] = None

    async def get_access_token(self) -> str:
        print("TOKEN_URL =", self.token_url)
        now = time.time()
        if self._token and now < self._token_exp:
            return self._token

        # Avito OAuth: form-urlencoded
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        if r.status_code != 200:
            raise RuntimeError(f"Avito token error: {r.status_code} {r.text}")

        payload = r.json()
        token = payload["access_token"]
        expires_in = int(payload.get("expires_in", 3600))

        self._token = token
        self._token_exp = now + expires_in - 60
        return token

    async def get_self_user_id(self) -> int:
        if self._user_id is not None:
            return self._user_id

        token = await self.get_access_token()
        url = "https://api.avito.ru/core/v1/accounts/self"
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, headers={"Authorization": f"Bearer {token}"})

        if r.status_code != 200:
            raise RuntimeError(f"Avito self account error: {r.status_code} {r.text}")

        self._user_id = int(r.json()["id"])
        return self._user_id

    async def register_webhook(
        self,
        register_url: str,
        webhook_url: str,
        secret: Optional[str] = None,
    ) -> dict:
        print("REGISTER_WEBHOOK_URL =", register_url)
        print("WEBHOOK_URL =", webhook_url)

        token = await self.get_access_token()
        body = {"url": webhook_url}
        if secret:
            body["secret"] = secret

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(
                register_url,
                headers={"Authorization": f"Bearer {token}"},
                json=body,
            )

        if r.status_code not in (200, 201):
            raise RuntimeError(f"Register webhook error: {r.status_code} {r.text}")

        return r.json()

    async def send_message_text(self, chat_id: str, text: str) -> dict:
        """Отправка текстового сообщения по доке:
        POST /messenger/v1/accounts/{user_id}/chats/{chat_id}/messages
        body: {"message": {"text": "..."}, "type": "text"}
        """
        token = await self.get_access_token()
        user_id = await self.get_self_user_id()

        url = f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages"
        payload = {"message": {"text": text}, "type": "text"}

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

        if r.status_code != 200:
            raise RuntimeError(f"Send message error: {r.status_code} {r.text}")

        return r.json()
