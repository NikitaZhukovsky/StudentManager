from ninja import Router
from ninja_jwt.authentication import JWTAuth
from students.api.students_list import list_students
from students.api.create_student import create_student
from students.api.student_detail import get_student
from students.api.update_student import update_student
from students.api.delete_student import delete_student
from typing import List
from students.schemas import (
    StudentCreateSchema,
    StudentUpdateSchema,
    StudentGetSchema,
    StudentFilterSchema
)

student_router = Router(auth=JWTAuth())

student_router.get("/", response=List[StudentGetSchema])(list_students)
student_router.post("/", response=StudentGetSchema)(create_student)
student_router.get("/{student_id}/", response=StudentGetSchema)(get_student)
student_router.patch("/{student_id}/", response=StudentGetSchema)(update_student)
student_router.delete("/{student_id}/")(delete_student)


