
from pydantic import BaseModel, EmailStr, Field


class Employee(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2)
    department: str
    salary: float = Field(gt=0)
    email: EmailStr
