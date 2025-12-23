import pytest


@pytest.mark.smoke
def test_list_posts_returns_200_and_list(client):
    res = client.list_posts()
    assert res.status_code == 200, f"Expected 200, got {res.status_code}. Body: {res.text[:200]}"

    body = res.json
    assert isinstance(body, list)
    assert len(body) > 0
    assert {"userId", "id", "title", "body"}.issubset(body[0].keys())


@pytest.mark.smoke
@pytest.mark.parametrize("post_id", [1, 2, 3, 10])
def test_get_single_post_returns_expected_id(client, post_id):
    res = client.get_post(post_id)
    assert res.status_code == 200

    body = res.json
    assert body["id"] == post_id
    assert isinstance(body["title"], str)
    assert isinstance(body["body"], str)


@pytest.mark.smoke
def test_create_post_returns_201_and_echoes_payload(client):
    title = "Semra QA API test"
    body_text = "test body"
    user_id = 1

    res = client.create_post(title=title, body=body_text, user_id=user_id)
    assert res.status_code == 201

    body = res.json
    assert body["title"] == title
    assert body["body"] == body_text
    assert body["userId"] == user_id
    assert "id" in body


@pytest.mark.regression
def test_get_non_existing_post_returns_empty_object_or_404(client):
    res = client.get_post(9999)
    assert res.status_code in (200, 404)

    if res.status_code == 200:
        assert res.json == {}
