from fastapi import APIRouter, HTTPException

from app.models.student import Student
from app.repositories.student import get_student_by_id, list_students

router = APIRouter(tags=["students"])


@router.get("/students", response_model=list[Student])
def get_students() -> list[Student]:
    return list_students()


@router.get("/students/{student_id}", response_model=Student)
def get_student(student_id: str) -> Student:
    try:
        parsed_student_id = int(student_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="student id must be a valid number",
        ) from exc

    student = get_student_by_id(parsed_student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    return student
