from pydantic import BaseModel
from typing import Any, Dict, Optional


class WebhookPayloadValue(BaseModel):
    chat_id: Optional[str] = None
    content: Optional[Dict[str, Any]] = None


class WebhookPayload(BaseModel):
    type: Optional[str] = None
    value: Optional[WebhookPayloadValue] = None


class AvitoWebhook(BaseModel):
    payload: Optional[WebhookPayload] = None