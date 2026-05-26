# Schema Patterns

## Template

```python
from pydantic import BaseModel, EmailStr, Field


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: str
    salary: float = Field(..., gt=0)


class EmployeeUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    department: str | None = None
    salary: float | None = Field(None, gt=0)


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    salary: float
```

## Rules

- `Create`: required fields with `Field(...)` validation
- `Update`: all optional (`| None = None`); router uses `model_dump(exclude_unset=True)`
- `Response`: flat, all required, no secrets or internal artifacts
- Email fields → `EmailStr` (requires `pydantic[email]`)
