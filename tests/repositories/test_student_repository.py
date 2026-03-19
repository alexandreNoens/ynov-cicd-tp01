from collections.abc import Callable

import pytest

from app.exceptions.student import StudentEmailAlreadyExistsError
from app.models.student import Student, StudentCreate
from app.repositories.student import (
    create_student,
    get_student_by_id,
    list_students,
)


def test_list_students_returns_students_ordered_by_id() -> None:
    students = list_students()

    assert isinstance(students, list)
    assert len(students) == 5
    assert all(isinstance(student, Student) for student in students)
    assert [student.id for student in students] == [1, 2, 3, 4, 5]
    assert students[0].firstName == "Harry"
    assert students[1].firstName == "Hermione"


def test_get_student_by_id_returns_student_when_found() -> None:
    student = get_student_by_id(1)

    assert isinstance(student, Student)
    assert student.id == 1
    assert student.firstName == "Harry"


def test_get_student_by_id_returns_none_when_missing() -> None:
    student = get_student_by_id(999)

    assert student is None


def test_create_student_returns_created_student_with_generated_id(
    student_create_factory: Callable[..., StudentCreate],
) -> None:
    created_student = create_student(student_create_factory())

    assert isinstance(created_student, Student)
    assert created_student.id == 6
    assert created_student.firstName == "Neville"
    assert created_student.email == "neville.longbottom@hogwarts.edu"


def test_create_student_raises_error_when_email_already_exists(
    student_create_factory: Callable[..., StudentCreate],
) -> None:
    with pytest.raises(StudentEmailAlreadyExistsError):
        create_student(
            student_create_factory(
                firstName="Harry",
                lastName="Potter",
                email="harry.potter@hogwarts.edu",
                grade=18,
                field="informatique",
            )
        )
