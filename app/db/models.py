from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.db.db import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), unique=True, nullable=False)
    source = Column(String(100), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    country_code = Column(String(10), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
