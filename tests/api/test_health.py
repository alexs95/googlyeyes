from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient


def test_health_returns_200(client: TestClient):
    response = client.get('/api/health')
    assert response.status_code == HTTP_200_OK
