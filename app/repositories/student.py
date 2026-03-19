import sqlite3

from app.db import get_connection
from app.exceptions.student import StudentEmailAlreadyExistsError, StudentNotFoundError
from app.models.student import Student, StudentCreate


def list_students() -> list[Student]:
    query = """
    SELECT id, firstName, lastName, email, grade, field
    FROM students
    ORDER BY id ASC
    """
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(query).fetchall()

    return [Student(**dict(row)) for row in rows]


def get_student_by_id(student_id: int) -> Student | None:
    query = """
    SELECT id, firstName, lastName, email, grade, field
    FROM students
    WHERE id = ?
    """
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(query, (student_id,)).fetchone()

    if row is None:
        return None

    return Student(**dict(row))


def create_student(student: StudentCreate) -> Student:
    query = """
    INSERT INTO students (firstName, lastName, email, grade, field)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                query,
                (
                    student.firstName,
                    student.lastName,
                    student.email,
                    student.grade,
                    student.field,
                ),
            )
            created_student_id = cursor.lastrowid
    except sqlite3.IntegrityError as exc:
        if "students.email" in str(exc):
            raise StudentEmailAlreadyExistsError() from exc
        raise

    created_student = get_student_by_id(created_student_id)
    if created_student is None:
        raise RuntimeError("created student could not be retrieved")

    return created_student


def update_student(student_id: int, student: StudentCreate) -> Student:
    query = """
    UPDATE students
    SET firstName = ?, lastName = ?, email = ?, grade = ?, field = ?
    WHERE id = ?
    """
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                query,
                (
                    student.firstName,
                    student.lastName,
                    student.email,
                    student.grade,
                    student.field,
                    student_id,
                ),
            )
            if cursor.rowcount == 0:
                raise StudentNotFoundError()
    except sqlite3.IntegrityError as exc:
        if "students.email" in str(exc):
            raise StudentEmailAlreadyExistsError() from exc
        raise

    updated_student = get_student_by_id(student_id)
    if updated_student is None:
        raise RuntimeError("updated student could not be retrieved")

    return updated_student


def delete_student(student_id: int) -> None:
    query = """
    DELETE FROM students
    WHERE id = ?
    """
    with get_connection() as connection:
        cursor = connection.execute(query, (student_id,))
        if cursor.rowcount == 0:
            raise StudentNotFoundError()
