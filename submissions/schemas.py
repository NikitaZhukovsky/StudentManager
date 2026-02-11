from ninja import Schema
from typing import Optional
from datetime import date


class SubmissionGetSchema(Schema):
    id: int
    student_id: int
    assignment_id: int
    file_path: str
    submitted_at: date
    student_name: str
    assignment_title: str
    course_title: str


class SubmissionCreateSchema(Schema):
    student_id: int
    assignment_id: int
    file_path: str
    submitted_at: date


class SubmissionUpdateSchema(Schema):
    student_id: Optional[int] = None
    assignment_id: Optional[int] = None
    file_path: Optional[str] = None
    submitted_at: Optional[date] = None


class SubmissionFilterSchema(Schema):
    student_id: Optional[int] = None
    assignment_id: Optional[int] = None
    course_id: Optional[int] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    order_by: str = "id"

