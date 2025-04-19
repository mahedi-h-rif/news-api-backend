from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.db import AsyncSessionLocal

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/db-health")
async def db_health():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError as e:
        return {"status": "error", "database": "not connected", "details": str(e)}
