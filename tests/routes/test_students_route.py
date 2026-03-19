from fastapi.testclient import TestClient

from app.db import reset_db
from app.main import app


def test_get_students_returns_json_array_with_status_200() -> None:
    reset_db()
    client = TestClient(app)

    response = client.get("/students")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 5
    assert payload[0]["firstName"] == "Harry"
