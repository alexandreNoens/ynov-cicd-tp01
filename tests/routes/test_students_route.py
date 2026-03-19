from collections.abc import Callable

from fastapi.testclient import TestClient


def test_get_students_returns_json_array_with_status_200(client: TestClient) -> None:
    response = client.get("/students")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 5
    assert payload[0]["firstName"] == "Harry"


def test_get_student_returns_json_object_with_status_200_when_found(
    client: TestClient,
) -> None:
    response = client.get("/students/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["firstName"] == "Harry"


def test_get_student_returns_404_when_id_does_not_exist(client: TestClient) -> None:
    response = client.get("/students/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "student not found"}


def test_get_student_returns_400_when_id_is_not_a_valid_number(
    client: TestClient,
) -> None:
    response = client.get("/students/not-a-number")

    assert response.status_code == 400
    assert response.json() == {"detail": "student id must be a valid number"}


def test_post_student_returns_201_and_created_student(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    response = client.post("/students", json=student_payload_factory())

    assert response.status_code == 201
    payload = response.json()
    assert payload["id"] == 6
    assert payload["firstName"] == "Neville"
    assert payload["email"] == "neville.longbottom@hogwarts.edu"


def test_post_student_returns_400_when_a_required_field_is_missing(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    payload = student_payload_factory()
    payload.pop("email")
    response = client.post("/students", json=payload)

    assert response.status_code == 400


def test_post_student_returns_400_when_first_name_is_too_short(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    response = client.post("/students", json=student_payload_factory(firstName="N"))

    assert response.status_code == 400


def test_post_student_returns_400_when_last_name_is_too_short(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    response = client.post("/students", json=student_payload_factory(lastName="L"))

    assert response.status_code == 400


def test_post_student_returns_400_when_email_is_invalid(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    response = client.post(
        "/students",
        json=student_payload_factory(email="invalid-email"),
    )

    assert response.status_code == 400


def test_post_student_returns_409_when_email_already_exists(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    response = client.post(
        "/students",
        json=student_payload_factory(email="harry.potter@hogwarts.edu"),
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "student email already exists"}


def test_post_student_returns_400_when_grade_is_below_range(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    response = client.post("/students", json=student_payload_factory(grade=-1))

    assert response.status_code == 400


def test_post_student_returns_400_when_grade_is_above_range(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    response = client.post("/students", json=student_payload_factory(grade=21))

    assert response.status_code == 400


def test_post_student_returns_400_when_field_is_invalid(
    client: TestClient,
    student_payload_factory: Callable[..., dict[str, object]],
) -> None:
    response = client.post(
        "/students",
        json=student_payload_factory(field="biologie"),
    )

    assert response.status_code == 400
