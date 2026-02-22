from fastapi import FastAPI

from api.lifespan import lifespan
from api.routers.avito_webhook import router as avito_router

app = FastAPI(title="Avito → Telegram", lifespan=lifespan)
app.include_router(avito_router)


@app.get("/health")
async def health():
    return {"status": "ok"}