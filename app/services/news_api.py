import httpx
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models import News
from app.schemas.news import Article


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


async def create_news(session: AsyncSession, article: Article):
    news = News(
        title=article.title,
        description=article.description,
        url=article.url,
        source=article.source.get("name"),
        published_at=article.publishedAt,
    )
    session.add(news)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()  # in case of duplicate URL
