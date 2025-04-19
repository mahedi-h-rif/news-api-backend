from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Article(BaseModel):
    source: dict
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    publishedAt: datetime
    content: Optional[str]


class NewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[Article]
