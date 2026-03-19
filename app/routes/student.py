from fastapi import APIRouter

from app.models.student import Student
from app.repositories.student import list_students

router = APIRouter(tags=["students"])


@router.get("/students", response_model=list[Student])
def get_students() -> list[Student]:
    return list_students()
