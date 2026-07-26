from app.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)


def test_email_check():
    response = client.post(
        "/email",
        json={
            "sender": "fraud420@gmail.com",
            "body": "Looking for Loans? Give your Bank Crendentials and get it within an hour",
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert "label" in result
    assert "score" in result
    assert "certainty" in result
    assert "reason" in result


def test_audio_check():
    with open(r"tests/test_audio.m4a", "rb") as audio:
        response = client.post("/audio", files={"file": audio})
        assert response.status_code == 200
        result = response.json()
        assert "label" in result
        assert "score" in result
        assert "certainty" in result
        assert "reason" in result


@pytest.fixture
def audio():
    with open(r"tests/test_audio.m4a", "rb") as audio:
        yield audio.read()


def test1(audio):
    with client.websocket_connect("/ws") as websocket:
        websocket.send_bytes(audio)
        result = websocket.receive_json()
        assert "label" in result
        assert "score" in result
        assert "certainty" in result
        assert "reason" in result
