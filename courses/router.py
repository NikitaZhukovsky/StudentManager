from ninja import Router
from ninja_jwt.authentication import JWTAuth
from typing import List
from courses.api.courses_list import list_courses
from courses.api.create_course import create_course
from courses.api.course_detail import get_course
from courses.api.update_course import update_course
from courses.api.delete_course import delete_course
from courses.api.add_students_to_course import add_students_to_course
from courses.api.delete_students_from_course import remove_students_from_course
from courses.schemas import (
    CourseCreateSchema,
    CourseUpdateSchema,
    CourseGetSchema,
    CourseFilterSchema,
    AddStudentsToCourseSchema,
    RemoveStudentsFromCourseSchema
)

course_router = Router(auth=JWTAuth())

course_router.get("/", response=List[CourseGetSchema])(list_courses)
course_router.post("/", response=CourseGetSchema)(create_course)
course_router.get("/{course_id}/", response=CourseGetSchema)(get_course)
course_router.patch("/{course_id}/", response=CourseGetSchema)(update_course)
course_router.delete("/{course_id}/")(delete_course)
course_router.post("/{course_id}/students/", response=CourseGetSchema)(add_students_to_course)
course_router.delete("/{course_id}/students/", response=CourseGetSchema)(remove_students_from_course)

