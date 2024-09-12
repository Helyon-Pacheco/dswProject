from typing import Optional
from pydantic import Field, EmailStr
from .entity_base import EntityBase

class Customer(EntityBase):
    name: str = Field(..., alias="Name")
    email: EmailStr = Field(..., alias="Email")
    password: str = Field(..., alias="Password")
    address: Optional[str] = Field(None, alias="Address")
    phone: Optional[str] = Field(None, alias="Phone")
    