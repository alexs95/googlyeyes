import pytest
from cv2 import imread, IMREAD_COLOR
from numpy import ndarray
from starlette.testclient import TestClient

from app.main import app
from app.service.googly import GooglyEyes


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def googly() -> GooglyEyes:
    yield GooglyEyes("models/shape_predictor_68_face_landmarks.dat")


@pytest.fixture()
def aeroplane() -> ndarray:
    yield imread("tests/images/aeroplane.jpg", IMREAD_COLOR)


@pytest.fixture()
def selfie() -> ndarray:
    yield imread("tests/images/selfie.jpg", IMREAD_COLOR)


@pytest.fixture()
def group() -> ndarray:
    yield imread("tests/images/group.jpg", IMREAD_COLOR)
