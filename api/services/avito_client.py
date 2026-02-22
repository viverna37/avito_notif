import time
import httpx


class AvitoClient:
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

        self._token: str | None = None
        self._exp: float = 0.0

    async def get_self_user_id(self, access_token: str):
        url = "https://api.avito.ru/core/v1/accounts/self"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)

        if r.status_code != 200:
            raise Exception(r.text)

        return r.json()["id"]

    async def _get_token(self) -> str:
        now = time.time()
        if self._token and now < self._exp:
            return self._token

        # Avito OAuth обычно требует form-urlencoded: data= (НЕ json=)
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
        self._exp = now + expires_in - 60  # запас 60 сек
        return token

    async def register_webhook(self, register_url: str, url: str, secret: str | None = None) -> dict:
        token = await self._get_token()
        body = {"url": url}
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

    async def send_avito_message(self,
            access_token: str,
            chat_id: str,
            text: str,
    ):
        url = f"https://api.avito.ru/messenger/v1/accounts/{self.get_self_user_id(access_token)}/chats/{chat_id}/messages"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "message": {
                "text": text
            },
            "type": "text"
        }

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(url, headers=headers, json=payload)

        if r.status_code != 200:
            raise Exception(f"Send error: {r.status_code} {r.text}")

        return r.json()