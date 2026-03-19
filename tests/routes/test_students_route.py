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


def test_get_student_returns_json_object_with_status_200_when_found() -> None:
    reset_db()
    client = TestClient(app)

    response = client.get("/students/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["firstName"] == "Harry"


def test_get_student_returns_404_when_id_does_not_exist() -> None:
    reset_db()
    client = TestClient(app)

    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "student not found"}


def test_get_student_returns_400_when_id_is_not_a_valid_number() -> None:
    reset_db()
    client = TestClient(app)

    response = client.get("/students/not-a-number")

    assert response.status_code == 400
    assert response.json() == {"detail": "student id must be a valid number"}
