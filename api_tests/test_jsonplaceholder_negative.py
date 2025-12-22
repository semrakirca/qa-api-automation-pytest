import pytest


def test_invalid_endpoint_returns_404(api, base_url, timeout):
    r = api.get(f"{base_url}/not-a-real-endpoint", timeout=timeout)
    assert r.status_code == 404


@pytest.mark.parametrize("bad_id", ["abc", "1.5", "-1"])
def test_get_post_with_invalid_id_format_behaves_safely(api, base_url, timeout, bad_id):
    """
    Negative-ish test:
    JSONPlaceholder bazen 404, bazen {} gibi davranabilir.
    Bizim amacımız: sistemin 500 gibi crash etmemesi ve stabil cevap vermesi.
    """
    r = api.get(f"{base_url}/posts/{bad_id}", timeout=timeout)

    assert r.status_code in (200, 404)

    if r.status_code == 200:
        # 200 dönüyorsa body en azından JSON olmalı ve beklenmedik crash olmamalı
        body = r.json()
        assert isinstance(body, dict)


def test_filter_comments_by_postId_returns_only_that_post(api, base_url, timeout):
    """
    Positive+validation but used as 'data integrity' check.
    Bu tarz testler gerçek projede çok değerlidir.
    """
    post_id = 1
    r = api.get(f"{base_url}/comments", params={"postId": post_id}, timeout=timeout)

    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert all(item["postId"] == post_id for item in body)


def test_create_post_with_missing_fields_returns_deterministic_response(api, base_url, timeout):
    """
    JSONPlaceholder 'fake' create yapar ve validation yapmayabilir.
    Gerçek sistemde 400 beklerdik.
    Burada amacımız: response JSON mu, id dönüyor mu, crash var mı?
    """
    payload = {"title": "only title"}  # body ve userId yok
    r = api.post(f"{base_url}/posts", json=payload, timeout=timeout)

    # JSONPlaceholder genelde 201 döner.
    assert r.status_code in (201, 400)

    body = r.json()
    assert isinstance(body, dict)
    # 201 ise id dönmeli (mock davranışı)
    if r.status_code == 201:
        assert "id" in body


def test_response_content_type_is_json_for_posts(api, base_url, timeout):
    r = api.get(f"{base_url}/posts/1", timeout=timeout)
    assert r.status_code == 200
    assert "application/json" in r.headers.get("Content-Type", "")


def test_api_does_not_return_5xx_for_basic_requests(api, base_url, timeout):
    """
    Sağlamlık testi: 5xx (server error) görürsek ortam/servis sorunu olabilir.
    """
    endpoints = ["/posts", "/comments", "/albums"]
    for ep in endpoints:
        r = api.get(f"{base_url}{ep}", timeout=timeout)
        assert r.status_code < 500, f"{ep} returned {r.status_code}"
