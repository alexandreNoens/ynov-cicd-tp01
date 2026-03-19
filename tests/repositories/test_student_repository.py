from app.db import reset_db
from app.models.student import Student
from app.repositories.student import list_students


def test_list_students_returns_students_ordered_by_id() -> None:
    reset_db()

    students = list_students()

    assert isinstance(students, list)
    assert len(students) == 5
    assert all(isinstance(student, Student) for student in students)
    assert [student.id for student in students] == [1, 2, 3, 4, 5]
    assert students[0].firstName == "Harry"
    assert students[1].firstName == "Hermione"