from fastapi import FastAPI

from api.lifespan import lifespan
from api.routers.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hosting API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(health_router)
    app.include_router(notif_router)

    return app

app = create_app()


