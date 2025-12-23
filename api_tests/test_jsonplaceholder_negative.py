import pytest

pytestmark = pytest.mark.regression


def test_invalid_endpoint_returns_404(client):
    res = client.get_raw("/not-a-real-endpoint")
    assert res.status_code == 404


@pytest.mark.parametrize("bad_id", ["abc", "1.5", "-1"])
def test_get_post_with_invalid_id_format_behaves_safely(client, bad_id):
    res = client.get_post(bad_id)

    assert res.status_code in (200, 404)

    if res.status_code == 200:
        assert isinstance(res.json, dict)


def test_filter_comments_by_postId_returns_only_that_post(client):
    post_id = 1
    res = client.list_comments(post_id=post_id)

    assert res.status_code == 200
    body = res.json
    assert isinstance(body, list)
    assert len(body) > 0
    assert all(item["postId"] == post_id for item in body)


def test_create_post_with_missing_fields_returns_deterministic_response(client):
    # JSONPlaceholder fake create: 201 dönebilir; biz "crash olmasın" diye kontrol ediyoruz
    # res = client._post("/posts", payload={"title": "only title"})  # body/userId yok
    res = client.create_post_raw({"title": "only title"})


    assert res.status_code in (201, 400)

    assert isinstance(res.json, dict) or res.json is None
    if res.status_code == 201 and isinstance(res.json, dict):
        assert "id" in res.json


def test_response_content_type_is_json_for_posts(client):
    res = client.get_post(1)
    assert res.status_code == 200
    assert "application/json" in res.headers.get("Content-Type", "")


def test_api_does_not_return_5xx_for_basic_requests(client):
    checks = [
        ("posts", client.get_raw("/posts")),
        ("comments", client.get_raw("/comments")),
        ("albums", client.list_albums()),
    ]

    for name, res in checks:
        assert res.status_code < 500, f"{name} returned {res.status_code}"

