import httpx
from fastapi import HTTPException

from app.core.config import settings


async def fetch_news(country: str = "us", page: int = 1, page_size: int = 10):
    params = {
        "country": country,
        "page": page,
        "pageSize": page_size,
        "apiKey": settings.NEWS_API_KEY,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.NEWS_API_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch news")
        return response.json()
