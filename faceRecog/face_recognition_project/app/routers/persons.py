# app/routers/persons.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_db
from app import crud

router = APIRouter()


class PersonCreate(BaseModel):
    name: str


class PersonResponse(BaseModel):
    id: int
    name: str
    created_at: str


@router.post("/", response_model=PersonResponse)
def create_person(person: PersonCreate):
    """ایجاد person جدید"""
    with get_db() as db:
        result = crud.create_person(db, person.name)

    if result is None:
        raise HTTPException(status_code=500, detail="Failed to create person")

    return result


@router.get("/{person_id}", response_model=PersonResponse)
def get_person(person_id: int):
    """دریافت person با ID"""
    with get_db() as db:
        person = crud.get_person(
            db, person_id
        )  # تغییر از get_person_by_id به get_person

    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    return person


@router.get("/")
def get_all_persons():
    """دریافت تمام persons"""
    with get_db() as db:
        persons = crud.get_all_persons(db)

    return {"persons": persons}


@router.delete("/{person_id}")
def delete_person(person_id: int):
    """حذف person"""
    with get_db() as db:
        success = crud.delete_person(db, person_id)

    if not success:
        raise HTTPException(status_code=404, detail="Person not found")

    return {"message": "Person deleted successfully"}
