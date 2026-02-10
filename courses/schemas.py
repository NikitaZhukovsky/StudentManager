from ninja import Schema
from typing import Optional, List
from students.schemas import StudentGetSchema


class CourseGetSchema(Schema):
    id: int
    title: str
    code: str
    students: List[StudentGetSchema] = []


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


class RemoveStudentsFromCourseSchema(Schema):
    student_ids: List[int]

