from numpy import ndarray, array_equal

from app.service.googly import GooglyEyes


def test_detect_with_one_face(googly: GooglyEyes, selfie: ndarray) -> None:
    assert len(googly.detect(selfie)) == 2


def test_detect_with_multiple_faces(googly: GooglyEyes, group: ndarray) -> None:
    assert len(googly.detect(group)) == 10


def test_detect_with_no_faces(googly: GooglyEyes, aeroplane: ndarray) -> None:
    assert len(googly.detect(aeroplane)) == 0


def test_googlify_with_two_eyes(googly: GooglyEyes, selfie: ndarray) -> None:
    a = selfie.copy()
    eyes = googly.detect(selfie)
    b = googly.googlify(eyes, selfie)
    assert not array_equal(a, b)


def test_googlify_with_no_eyes(googly: GooglyEyes, aeroplane: ndarray) -> None:
    a = aeroplane.copy()
    eyes = googly.detect(aeroplane)
    b = googly.googlify(eyes, aeroplane)
    assert array_equal(a, b)


def test_googlify_with_multiple_eyes(googly: GooglyEyes, group: ndarray) -> None:
    a = group.copy()
    eyes = googly.detect(group)
    b = googly.googlify(eyes, group)
    assert not array_equal(a, b)
