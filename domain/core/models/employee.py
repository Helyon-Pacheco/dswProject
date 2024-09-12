from typing import Optional
from pydantic import Field, EmailStr
from .entity_base import EntityBase

class Employee(EntityBase):
    name: str = Field(..., alias="Name")
    email: EmailStr = Field(..., alias="Email")
    password: str = Field(..., alias="Password")
    role: Optional[str] = Field(None, alias="Role")
    