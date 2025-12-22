import pytest


def test_list_posts_returns_200_and_list(api, base_url, timeout):
    r = api.get(f"{base_url}/posts", timeout=timeout)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text[:200]}"

    body = r.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert {"userId", "id", "title", "body"}.issubset(body[0].keys())


@pytest.mark.parametrize("post_id", [1, 2, 3, 10])
def test_get_single_post_returns_expected_id(api, base_url, timeout, post_id):
    r = api.get(f"{base_url}/posts/{post_id}", timeout=timeout)
    assert r.status_code == 200

    body = r.json()
    assert body["id"] == post_id
    assert isinstance(body["title"], str)
    assert isinstance(body["body"], str)


def test_create_post_returns_201_and_echoes_payload(api, base_url, timeout):
    payload = {"title": "Semra QA API test", "body": "test body", "userId": 1}
    r = api.post(f"{base_url}/posts", json=payload, timeout=timeout)
    assert r.status_code == 201

    body = r.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


def test_get_non_existing_post_returns_empty_object_or_404(api, base_url, timeout):
    r = api.get(f"{base_url}/posts/9999", timeout=timeout)
    assert r.status_code in (200, 404)

    if r.status_code == 200:
        assert r.json() == {}
