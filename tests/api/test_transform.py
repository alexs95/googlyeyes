from cv2 import imdecode, IMREAD_COLOR, imencode
from numpy import uint8, array_equal, frombuffer, ndarray, ones
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient


def test_transform_returns_modified_image(client: TestClient, selfie: ndarray) -> None:
    _, stream = imencode(".jpg", selfie)
    response = client.post("/api/transform/", files={"file": ("selfie.jpg", stream.tobytes(), "image/jpeg")})
    response_selfie = imdecode(frombuffer(response.content, dtype=uint8), IMREAD_COLOR)
    assert response.status_code == 200
    assert not array_equal(selfie, response_selfie)


def test_transform_returns_identical_image_if_there_are_no_eyes(client: TestClient) -> None:
    black = ones((600, 600, 3))
    _, stream = imencode(".jpg", black.copy())
    response = client.post("/api/transform/", files={"file": ("black.jpg", stream.tobytes(), "image/jpeg")})
    response_black = imdecode(frombuffer(response.content, dtype=uint8), IMREAD_COLOR)
    assert response.status_code == 200
    assert array_equal(black, response_black)


def test_transform_returns_400_if_image_is_not_jpeg(client: TestClient) -> None:
    black = ones((600, 600, 3))
    _, stream = imencode(".png", black.copy())
    response = client.post("/api/transform/", files={"file": ("black.png", stream.tobytes(), "image/png")})
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_transform_returns_400_if_image_is_too_large(client: TestClient) -> None:
    black = ones((1500, 1500, 3))
    _, stream = imencode(".jpg", black.copy())
    response = client.post("/api/transform/", files={"file": ("black.jpg", stream.tobytes(), "image/jpeg")})
    assert response.status_code == HTTP_400_BAD_REQUEST

