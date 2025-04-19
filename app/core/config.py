import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "News API")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    PORT: int = int(os.getenv("PORT", 8000))

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_name: str = os.getenv("DB_NAME", "news_db")
    db_user: str = os.getenv("DB_USER", "news_user")
    db_password: str = os.getenv("DB_PASSWORD", "12345678")

    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    NEWS_API_URL: str = os.getenv(
        "NEWS_API_URL", "https://newsapi.org/v2/top-headlines?country=us"
    )


settings = Settings()
