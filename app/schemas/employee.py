from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Alice Smith"])
    email: EmailStr = Field(..., examples=["alice@example.com"])
    department: str = Field(..., min_length=1, max_length=100, examples=["Engineering"])
    salary: float = Field(..., gt=0, examples=[75000.0])


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = Field(None, gt=0)


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    salary: float
