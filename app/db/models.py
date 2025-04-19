from sqlalchemy import Column, DateTime, Integer, String

from app.db.db import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    url = Column(String)
    published_at = Column(DateTime)
