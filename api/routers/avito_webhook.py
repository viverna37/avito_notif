from os import access

from fastapi import APIRouter, Request, Header, HTTPException, Depends

from api.config import Config
from api.deps import get_avito, get_tg, get_config, get_chats_repository
from api.models.webhook import AvitoWebhook
from api.services.signature import verify_hmac_sha256
from database.repository.chats_repository import ChatsRepository

router = APIRouter(prefix="/avito", tags=["avito"])


@router.post("/webhook")
async def avito_webhook(
        request: Request,
        x_avito_messenger_signature: str | None = Header(default=None),
        config: Config = Depends(get_config),
        chats_repository: ChatsRepository = Depends(get_chats_repository)

):
    raw = await request.body()

    ok = verify_hmac_sha256(raw, config.api.webhook_token, x_avito_messenger_signature)
    if not ok:
        raise HTTPException(status_code=401, detail="Bad signature")


    data = await request.json()

    # мягкий парсинг
    hook = AvitoWebhook.model_validate(data)
    chat_id = hook.payload.value.chat_id if (hook.payload and hook.payload.value) else None
    text = ""
    if hook.payload and hook.payload.value and hook.payload.value.content:
        text = str(hook.payload.value.content.get("text") or "")

    if not chat_id:
        return {"ok": True}

    tg = get_tg()
    avito = get_avito()

    # уведомление тебе о любом входящем
    await tg.send(f"💬 Avito сообщение\nchat_id: {chat_id}\n{text}")
    is_new_chat = await chats_repository.get_chat(str(chat_id))
    # автоответ только на новый chat_id
    if is_new_chat:
        try:
            await avito.send_message(access_token, chat_id, text)
            await tg.send(f"✅ Автоответ отправлен (новый чат): {chat_id}")
        except Exception as e:
            await tg.send(f"⚠️ Не смог отправить автоответ: {e}")

    return {"ok": True}
