from ninja import Schema
from typing import Optional
from datetime import date


class AssignmentGetSchema(Schema):
    id: int
    title: str
    description: Optional[str]
    course_id: int
    due_date: date
    course_title: str


class AssignmentCreateSchema(Schema):
    title: str
    description: Optional[str] = None
    course_id: int
    due_date: date


class AssignmentUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    course_id: Optional[int] = None
    due_date: Optional[date] = None


class AssignmentFilterSchema(Schema):
    search: Optional[str] = None
    course_id: Optional[int] = None
    upcoming: Optional[bool] = None
    order_by: str = "id"

