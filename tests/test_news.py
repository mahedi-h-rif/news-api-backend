from fastapi.testclient import TestClient

from app.auth.oauth2 import create_access_token
from app.main import app

client = TestClient(app)


def get_auth_headers():
    token = create_access_token({"sub": "blockstak-client"})
    return {"Authorization": f"Bearer {token}"}


def test_fetch_news():
    response = client.get("/news?page=1&page_size=5", headers=get_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "articles" in data
    assert isinstance(data["articles"], list)


def test_save_news():
    response = client.post("/news/save", headers=get_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data


# def test_get_latest_news():
#     response = client.get("/news/latest?limit=3", headers=get_auth_headers())
#     assert response.status_code in [200, 404]
#     data = response.json()
#     if response.status_code == 200:
#         assert data["status"] == "success"
#         assert "latest_news" in data
#     else:
#         assert data["detail"] == "No news found"


def test_get_headlines_by_country_not_found():
    response = client.get("/news/headlines/country?unknown", headers=get_auth_headers())
    assert response.status_code in [200, 404]


def test_get_headlines_by_source_not_found():
    response = client.get("/news/headlines/source?unknown", headers=get_auth_headers())
    assert response.status_code in [200, 404]


def test_filter_headlines_by_country():
    response = client.get(
        "/news/headlines/filter?country=us", headers=get_auth_headers()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok" or hasattr(data, "articles")


def test_filter_headlines_by_source():
    response = client.get(
        "/news/headlines/filter?source=bbc-news", headers=get_auth_headers()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok" or hasattr(data, "articles")


def test_filter_headlines_bad_request_missing_params():
    response = client.get("/news/headlines/filter", headers=get_auth_headers())
    assert response.status_code == 400
    assert response.json()["detail"] == "Provide at least one of 'country' or 'source'."


def test_filter_headlines_bad_request_both_params():
    response = client.get(
        "/news/headlines/filter?country=us&source=bbc-news", headers=get_auth_headers()
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Cannot use both 'country' and 'source' together."
    )


def test_unauthorized_access():
    response = client.get("/news")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
