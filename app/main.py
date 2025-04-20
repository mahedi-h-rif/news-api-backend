import logging

from fastapi import FastAPI

from app.auth import oauth2
from app.core.config import settings
from app.db.db import engine
from app.db.models import Base
from app.routes import health, news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Tables created")


app.include_router(health.router, tags=["Health"])
app.include_router(news.router, tags=["News"])


app.include_router(oauth2.router, tags=["Auth"])


logger.info("🚀 App started in development mode")
logger.info(
    f"📦 DB connected to: {settings.db_host}:{settings.db_port}/{settings.db_name}"
)
