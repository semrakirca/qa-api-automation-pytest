from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    json: Any
    headers: Dict[str, str]
    text: str


class JSONPlaceholderClient:
    """
    Minimal API client wrapper.
    - Centralizes base_url, session, default timeout
    - Provides small helper methods for endpoints
    """
   
    def __init__(self, base_url: str, session: requests.Session, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.session = session
        self.timeout = timeout

    def _get(self, path: str, params: Optional[dict] = None) -> ApiResponse:
        r = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        return ApiResponse(
            status_code=r.status_code,
            json=self._safe_json(r),
            headers=dict(r.headers),
            text=r.text,
        )

    def _post(self, path: str, payload: Optional[dict] = None) -> ApiResponse:
        r = self.session.post(f"{self.base_url}{path}", json=payload, timeout=self.timeout)
        return ApiResponse(
            status_code=r.status_code,
            json=self._safe_json(r),
            headers=dict(r.headers),
            text=r.text,
        )

    @staticmethod
    def _safe_json(resp: requests.Response) -> Any:
        try:
            return resp.json()
        except Exception:
            return None

    # ---- Endpoints ----

    def list_posts(self) -> ApiResponse:
        return self._get("/posts")

    def get_post(self, post_id: str | int) -> ApiResponse:
        return self._get(f"/posts/{post_id}")

    def create_post(self, title: str, body: str, user_id: int) -> ApiResponse:
        payload = {"title": title, "body": body, "userId": user_id}
        return self._post("/posts", payload)

    def list_comments(self, post_id: Optional[int] = None) -> ApiResponse:
        params = {"postId": post_id} if post_id is not None else None
        return self._get("/comments", params=params)
    def get_raw(self, path: str) -> ApiResponse:
        # For negative tests like /not-a-real-endpoint
        if not path.startswith("/"):
            path = "/" + path
        return self._get(path)

    def create_post_raw(self, payload: dict) -> ApiResponse:
        return self._post("/posts", payload)
