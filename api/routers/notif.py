from fastapi import APIRouter

notif_router = APIRouter()

@notif_router.get("/notif/{token}")
async def notif():
    return {"status": "ok"}