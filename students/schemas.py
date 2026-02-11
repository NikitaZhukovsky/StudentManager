from typing import Optional
from ninja import Schema
from pydantic import EmailStr


class StudentCreateSchema(Schema):
    full_name: str
    email: EmailStr


class StudentUpdateSchema(Schema):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentGetSchema(Schema):
    id: int
    full_name: str
    email: str


class StudentFilterSchema(Schema):
    search: Optional[str] = None
    order_by: Optional[str] = "id"


