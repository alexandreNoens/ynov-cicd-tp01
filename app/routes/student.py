import json
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.exceptions.student import StudentEmailAlreadyExistsError
from app.models.student import Student, StudentCreate
from app.repositories.student import (
    create_student,
    get_student_by_id,
    list_students,
)

router = APIRouter(tags=["students"])


@router.get("/students", response_model=list[Student])
def get_students() -> list[Student]:
    return list_students()


@router.post("/students", response_model=Student, status_code=201)
def post_student(payload: dict[str, Any]) -> Student:
    try:
        student_to_create = StudentCreate(**payload)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=json.loads(exc.json())) from exc

    try:
        return create_student(student_to_create)
    except StudentEmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail="student email already exists",
        ) from exc


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
