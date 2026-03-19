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
