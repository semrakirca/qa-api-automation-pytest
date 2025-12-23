import pytest
import requests

from clients.jsonplaceholder_client import JSONPlaceholderClient

BASE_URL = "https://jsonplaceholder.typicode.com"
DEFAULT_TIMEOUT = 10


@pytest.fixture(scope="session")
def api_session():
    s = requests.Session()
    s.headers.update({
        "Accept": "application/json",
        "User-Agent": "semra-qa-api-tests/1.0",
    })
    return s


@pytest.fixture(scope="session")
def client(api_session):
    return JSONPlaceholderClient(
        base_url=BASE_URL,
        session=api_session,
        timeout=DEFAULT_TIMEOUT
    )
