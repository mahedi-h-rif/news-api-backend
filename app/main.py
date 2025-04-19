# app/main.py
import logging

from fastapi import FastAPI

from app.core.config import settings
from app.routes import news
from app.routes.health import router as health_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 App started in %s mode", settings.ENVIRONMENT)


app.include_router(news.router, tags=["News"])

app.include_router(health_router)

logger.info("🚀 App started in development mode")
logger.info(
    f"📦 DB connected to: {settings.db_host}:{settings.db_port}/{settings.db_name}"
)
