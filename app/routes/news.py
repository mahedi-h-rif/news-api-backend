import httpx
from fastapi import APIRouter, Query

from app.core.config import settings
from app.db.db import AsyncSessionLocal
from app.schemas.news import NewsResponse
from app.services.news_api import create_news

router = APIRouter()

NEWS_API_URL = settings.NEWS_API_URL
NEWS_API_KEY = settings.NEWS_API_KEY


@router.get("/news", response_model=NewsResponse)
async def get_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
):
    return await fetch_news(page=page, page_size=page_size)


router = APIRouter()


@router.get("/news", response_model=NewsResponse)
async def fetch_news():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NEWS_API_URL}&apiKey={NEWS_API_KEY}")
        response.raise_for_status()
        data = response.json()
        return data


@router.post("/news/save")
async def save_news():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NEWS_API_URL}&apiKey={NEWS_API_KEY}")
        response.raise_for_status()
        data = NewsResponse(**response.json())

    async with AsyncSessionLocal() as session:
        for article in data.articles:
            await create_news(session, article)
    return {"status": "success", "message": f"{len(data.articles)} articles processed"}
