from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app import store

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[EmployeeResponse])
def list_employees():
    return store.get_all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    employee = store.get_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate):
    return store.create(payload.model_dump())


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, payload: EmployeeUpdate):
    employee = store.update(employee_id, payload.model_dump())
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):
    if not store.delete(employee_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
