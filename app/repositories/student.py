import sqlite3

from app.db import get_connection
from app.models.student import Student


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
