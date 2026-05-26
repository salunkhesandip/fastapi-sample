# Router Patterns

## Template

```python
from fastapi import APIRouter, HTTPException, status
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app import store

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=list[EmployeeResponse])
def list_employees():
    return store.get_all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    employee = store.get_by_id(employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return employee


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate):
    return store.create(payload.model_dump())


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, payload: EmployeeUpdate):
    updated = store.update(employee_id, payload.model_dump(exclude_unset=True))
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return updated


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):
    if not store.delete(employee_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
```

## Rules

- Route HTTP only — delegate logic to `store`
- `response_model` on every route
- `status.HTTP_*` constants — never hardcode integers
- `HTTPException` for client errors (404, 422)
