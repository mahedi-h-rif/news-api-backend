import logging

from fastapi import FastAPI

from app.core.config import settings
from app.db.db import engine
from app.db.models import Base
from app.routes import health, news

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title=settings.APP_NAME)


# Run on app startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Tables created")


# Register routes
app.include_router(health.router, tags=["Health"])
app.include_router(news.router, tags=["News"])

# App startup logs
logger.info("🚀 App started in development mode")
logger.info(
    f"📦 DB connected to: {settings.db_host}:{settings.db_port}/{settings.db_name}"
)
