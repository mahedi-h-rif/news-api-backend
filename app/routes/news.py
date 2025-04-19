from fastapi import APIRouter, Query

from app.schemas.news import NewsResponse
from app.services.news_api import fetch_news

router = APIRouter()


@router.get("/news", response_model=NewsResponse)
async def get_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
):
    return await fetch_news(page=page, page_size=page_size)
