from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.config import load_config
from database.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = load_config()
    app.state.config = config

    await db.init(config.db.url)
    await db.create_tables()
    yield
    await db.close()