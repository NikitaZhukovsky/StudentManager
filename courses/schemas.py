from ninja import Schema
from typing import Optional, List


class StudentSimpleSchema(Schema):
    id: int
    full_name: str
    email: str


class CourseGetSchema(Schema):
    id: int
    title: str
    code: str
    students: List[StudentSimpleSchema] = []  # Добавляем обратно


class CourseCreateSchema(Schema):
    title: str
    code: str


class CourseUpdateSchema(Schema):
    title: Optional[str]
    code: Optional[str]


class CourseFilterSchema(Schema):
    search: Optional[str] = None
    order_by: str = "id"
    order: str = "asc"


class AddStudentsToCourseSchema(Schema):
    student_ids: List[int]

