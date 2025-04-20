# 📰 News API Backend

A secure, scalable FastAPI backend for fetching, storing, and filtering news articles from the [NewsAPI.org](https://newsapi.org/) using OAuth2 client credentials authentication, PostgreSQL for persistent storage, and full Docker support.

---

## ✅ Features

- 🔐 OAuth2 client credentials-based JWT authentication  
- 🗞 Integrates with NewsAPI to fetch & filter articles  
- 🧠 Async SQLAlchemy ORM + PostgreSQL  
- 📦 Dockerized with multi-service setup (App + DB)  
- 🧪 Unit tested with Pytest  
- 📋 Pydantic-based schema validation  
- 📁 Clean, modular project structure  
- 🚀 Ready for production with Uvicorn  

---

## 🧱 Tech Stack

| Component        | Tech                      |
|------------------|---------------------------|
| Framework        | FastAPI                   |
| Auth             | OAuth2 + JWT              |
| Database         | PostgreSQL + SQLAlchemy   |
| HTTP Client      | httpx (async)             |
| External API     | NewsAPI                   |
| Containerization | Docker + Docker Compose   |
| Testing          | Pytest                    |

---

## 🗂️ Project Structure

```
.
├── app
│   ├── main.py                # Entry point for FastAPI app
│   ├── core/
│   │   └── config.py          # Configuration from .env
│   ├── db/
│   │   ├── session.py         # Async DB session
│   │   └── base.py            # Base metadata
│   ├── models/
│   │   └── news.py            # SQLAlchemy models
│   ├── schemas/
│   │   └── news.py            # Pydantic schemas
│   ├── services/
│   │   └── news.py            # Business logic for NewsAPI
│   ├── routes/
│   │   └── news.py            # Route handlers
│   ├── auth/
│   │   ├── auth.py            # JWT creation & verification
│   │   └── oauth2.py          # OAuth2 client credentials
├── tests/                     # Pytest unit tests
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Multi-service setup (App + DB)
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # Project documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/mahedi-h-rif/news-api-backend.git
cd news-api-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/newsdb
SECRET_KEY=super-secret-key
NEWS_API_KEY=your_newsapi_key
NEWS_API_URL=https://newsapi.org/v2/top-headlines?country=us
```

---

## 🐳 Dockerized Setup

### 1. Build and run with Docker Compose

```bash
docker-compose up --build
```

### 2. Access endpoints

- Docs: http://localhost:8000/docs  
- Health: http://localhost:8000/health

---

## 🔐 Authentication Guide

The API uses OAuth2 with client credentials flow.

### 1. Get an access token

```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=blockstak-client&client_secret=blockstak-secret"
```

### 2. Use the token

Add it in headers for authorized requests:

```http
Authorization: Bearer <your_token>
```

---

## 🧪 Run Tests

```bash
pytest tests/
```

This will test:
- Auth token creation and protection  
- News fetch + save logic  
- Country/source filter logic  
- Error cases and validation  

---

## 🛣️ API Endpoints Summary

| Method | Endpoint                                | Description                          |
|--------|-----------------------------------------|--------------------------------------|
| GET    | `/health`                               | check app is running                       |
| POST   | `/token`                                | Get JWT using client credentials     |
| GET    | `/news`                                 | Fetch latest news from NewsAPI       |
| POST   | `/news/save`                            | Save news to DB                      |
| GET    | `/news/latest`                          | Retrieve saved news from DB          |
| GET    | `/news/headlines/country/{country}`     | Filter by country                    |
| GET    | `/news/headlines/source/{source}`       | Filter by source                     |
| GET    | `/news/headlines/filter?country=xx`     | Filter using query params            |

---

## 🧑‍💻 Local Development (without Docker)

```bash
uvicorn app.main:app --reload
```

> Make sure PostgreSQL is running and `.env` is configured properly.

---

## 🛠 Future Improvements

- 🔁 Auto-refresh tokens  
- 📈 Prometheus + Grafana metrics  
- 🔒 Rate limiting with Redis  
- 🔁 Background task scheduling  
- 🧊 Redis caching layer  
- 🌍 Multi-language news support  

---


---

## 📢 Contact

Have questions or suggestions? Reach out via [GitHub Issues](https://github.com/your-org/news-api-backend/issues).

