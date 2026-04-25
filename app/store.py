from typing import Dict
from app.schemas.employee import EmployeeResponse

_store: Dict[int, EmployeeResponse] = {}
_counter: int = 0


def get_next_id() -> int:
    global _counter
    _counter += 1
    return _counter


def get_all() -> list[EmployeeResponse]:
    return list(_store.values())


def get_by_id(employee_id: int) -> EmployeeResponse | None:
    return _store.get(employee_id)


def create(data: dict) -> EmployeeResponse:
    employee_id = get_next_id()
    employee = EmployeeResponse(id=employee_id, **data)
    _store[employee_id] = employee
    return employee


def update(employee_id: int, data: dict) -> EmployeeResponse | None:
    existing = _store.get(employee_id)
    if not existing:
        return None
    updated = existing.model_copy(update={k: v for k, v in data.items() if v is not None})
    _store[employee_id] = updated
    return updated


def delete(employee_id: int) -> bool:
    if employee_id not in _store:
        return False
    del _store[employee_id]
    return True


def reset() -> None:
    """Clear all data — intended for testing only."""
    global _counter
    _store.clear()
    _counter = 0
