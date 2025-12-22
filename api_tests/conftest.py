import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

DEFAULT_TIMEOUT = 10


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api():
    s = requests.Session()
    s.headers.update({
        "Accept": "application/json",
        "User-Agent": "semra-qa-api-tests/1.0",
    })
    return s


@pytest.fixture(scope="session")
def timeout():
    return DEFAULT_TIMEOUT
