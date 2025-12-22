import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_list_posts_returns_200_and_list():
    r = requests.get(f"{BASE_URL}/posts", timeout=10)
    assert r.status_code == 200

    body = r.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert {"userId", "id", "title", "body"}.issubset(body[0].keys())


def test_get_single_post_returns_expected_id():
    post_id = 1
    r = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=10)
    assert r.status_code == 200

    body = r.json()
    assert body["id"] == post_id
    assert isinstance(body["title"], str)
    assert isinstance(body["body"], str)


def test_create_post_returns_201_and_echoes_payload():
    payload = {"title": "Semra QA API test", "body": "test body", "userId": 1}
    r = requests.post(f"{BASE_URL}/posts", json=payload, timeout=10)
    assert r.status_code == 201

    body = r.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


def test_get_non_existing_post_returns_empty_object_or_404():
    r = requests.get(f"{BASE_URL}/posts/9999", timeout=10)
    assert r.status_code in (200, 404)

    if r.status_code == 200:
        assert r.json() == {}
