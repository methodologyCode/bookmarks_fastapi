from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_response_json():
    response = client.get("/", params={'url': 'https://www.youtube.com/'})
    assert response.status_code == 200
    assert "url" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "favicon" in response.json()
    assert "message" not in response.json()


def test_valid_response_answer():
    response = client.get("/", params={'url': 'https://www.youtube.com/'})
    assert response.status_code == 200
    assert response.json() == {
        "url": "https://www.youtube.com/",
        "title": "YouTube",
        "description":
            "Смотрите любимые видео, слушайте любимые песни, загружайте собственные ролики и делитесь ими с друзьями, близкими и целым миром.",
        "favicon": "https://www.youtube.com/s/desktop/7c155e84/img/favicon.ico"}


def test_not_valid_url_schema():
    response = client.get("/", params={'url': 'htps://www.youtube.com/'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Email syntax\"s not valid'}


def test_not_valid_requests_to_service():
    response = client.get("/", params={'url': 'https://www.yoe.com/'})
    assert response.status_code == 200
    assert response.json() == {'response': 'Сервис не доступен'}
