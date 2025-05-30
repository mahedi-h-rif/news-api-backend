from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.auth.dependencies import get_current_client
from app.core.config import settings
from app.db.db import AsyncSessionLocal
from app.db.models import News
from app.schemas.news import NewsResponse
from app.services.news_api import create_news

router = APIRouter()

NEWS_API_URL = settings.NEWS_API_URL
NEWS_API_KEY = settings.NEWS_API_KEY


@router.get(
    "/news", response_model=NewsResponse, dependencies=[Depends(get_current_client)]
)
async def fetch_news(page: int = Query(1, ge=1), page_size: int = Query(10, le=100)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NEWS_API_URL}&apiKey={NEWS_API_KEY}")
        response.raise_for_status()
        data = response.json()
        return data


@router.post("/news/save", dependencies=[Depends(get_current_client)])
async def save_news():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NEWS_API_URL}&apiKey={NEWS_API_KEY}")
        response.raise_for_status()
        data = NewsResponse(**response.json())

    async with AsyncSessionLocal() as session:
        for article in data.articles:
            await create_news(session, article)

    return {"status": "success", "message": f"{len(data.articles)} articles processed"}


@router.get("/news/latest", dependencies=[Depends(get_current_client)])
async def get_latest_news(skip: int = 0, limit: int = 3):
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(News).order_by(News.created_at.desc()).offset(skip).limit(limit)
            )
            latest_news = result.scalars().all()

            if not latest_news:
                raise HTTPException(status_code=404, detail="No news found")

        return {"status": "success", "latest_news": latest_news}

    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e)}


@router.get(
    "/news/headlines/country/{country_code}", dependencies=[Depends(get_current_client)]
)
async def get_headlines_by_country(country_code: str):
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(News)
                .filter(
                    News.source == country_code
                )  # optional: if you're storing country in DB
                .order_by(News.published_at.desc())
                .limit(10)
            )
            headlines = result.scalars().all()

        if not headlines:
            raise HTTPException(
                status_code=404, detail="No headlines found for the given country"
            )

        return {"status": "success", "headlines": headlines}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get(
    "/news/headlines/source/{source_id}", dependencies=[Depends(get_current_client)]
)
async def get_headlines_by_source(source_id: str):
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(News)
                .filter(News.source == source_id)
                .order_by(News.published_at.desc())
                .limit(10)
            )
            headlines = result.scalars().all()

        if not headlines:
            raise HTTPException(
                status_code=404, detail="No headlines found for the given source"
            )

        return {"status": "success", "headlines": headlines}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/news/headlines/filter", dependencies=[Depends(get_current_client)])
async def filter_headlines(country: Optional[str] = None, source: Optional[str] = None):
    if not country and not source:
        raise HTTPException(
            status_code=400, detail="Provide at least one of 'country' or 'source'."
        )

    if country and source:
        raise HTTPException(
            status_code=400, detail="Cannot use both 'country' and 'source' together."
        )

    params = {"apiKey": settings.NEWS_API_KEY}
    if country:
        params["country"] = country
    elif source:
        params["sources"] = source

    try:
        response = httpx.get("https://newsapi.org/v2/top-headlines", params=params)
        response.raise_for_status()
        return NewsResponse(**response.json())

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching filtered headlines: {str(e)}"
        )
