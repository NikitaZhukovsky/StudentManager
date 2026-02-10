from ninja import Router, Query
from ninja.errors import HttpError
from ninja.pagination import paginate, PageNumberPagination
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from django.db.models import Q
from typing import List
from .models import Course
from students.models import Student
from .schemas import (
    CourseCreateSchema,
    CourseUpdateSchema,
    CourseGetSchema,
    CourseFilterSchema,
    AddStudentsToCourseSchema,
    RemoveStudentsFromCourseSchema
)

course_router = Router(auth=JWTAuth())


@course_router.get("/", response=List[CourseGetSchema])
@paginate(PageNumberPagination, page_size=10)
def list_courses(
        request,
        filters: CourseFilterSchema = Query(...)
):
    queryset = Course.objects.all().prefetch_related('students')

    if filters.search:
        queryset = queryset.filter(
            Q(title__icontains=filters.search) |
            Q(code__icontains=filters.search)
        )

    order_field = filters.order_by
    if filters.order.lower() == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(order_field)

    return queryset


@course_router.post("/", response=CourseGetSchema)
def create_course(request, data: CourseCreateSchema):
    if Course.objects.filter(code=data.code).exists():
        raise HttpError(400, f"Курс '{data.code}' уже существует")

    course = Course.objects.create(
        title=data.title,
        code=data.code
    )

    return {
        "id": course.id,
        "title": course.title,
        "code": course.code,
    }


@course_router.get("/{course_id}/", response=CourseGetSchema)
def get_course(request, course_id: int):
    course = get_object_or_404(Course.objects.prefetch_related('students'), id=course_id)

    return {
        "id": course.id,
        "title": course.title,
        "code": course.code,
        "students": list(course.students.values('id', 'full_name', 'email'))
    }


@course_router.patch("/{course_id}/", response=CourseGetSchema)
def update_course(request, course_id: int, data: CourseUpdateSchema):

    course = get_object_or_404(Course.objects.prefetch_related('students'), id=course_id)

    if data.title is not None:
        course.title = data.title

    if data.code is not None and data.code != course.code:
        if Course.objects.filter(code=data.code).exclude(id=course_id).exists():
            raise HttpError(400, f"Курс '{data.code}' уже существует")
        course.code = data.code

    course.save()
    course.refresh_from_db()

    return {
        "id": course.id,
        "title": course.title,
        "code": course.code,
        "students": list(course.students.values('id', 'full_name', 'email'))
    }


@course_router.delete("/{course_id}/")
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course_title = course.title

    course.delete()

    return {
        "message": f"Курс '{course_title}' удален"
    }


@course_router.post("/{course_id}/students/", response=CourseGetSchema)
def add_students_to_course(request, course_id: int, data: AddStudentsToCourseSchema):
    course = get_object_or_404(Course.objects.prefetch_related('students'), id=course_id)

    existing_students = Student.objects.filter(id__in=data.student_ids)
    existing_ids = {student.id for student in existing_students}
    not_found_ids = set(data.student_ids) - existing_ids

    if not_found_ids:
        raise HttpError(
            404, f"Студенты с ID {list(not_found_ids)} не найдены"
        )

    if existing_ids:
        course.students.add(*existing_ids)

    course.refresh_from_db()

    return {
        "id": course.id,
        "title": course.title,
        "code": course.code,
        "students": list(course.students.values('id', 'full_name', 'email')),
    }


@course_router.delete("/{course_id}/students/", response=CourseGetSchema)
def remove_students_from_course(
        request,
        course_id: int,
        data: RemoveStudentsFromCourseSchema
):
    course = get_object_or_404(Course.objects.prefetch_related('students'), id=course_id)

    current_student_ids = set(course.students.values_list('id', flat=True))
    requested_to_remove_ids = set(data.student_ids)

    to_remove_ids = current_student_ids.intersection(requested_to_remove_ids)
    not_enrolled_ids = requested_to_remove_ids - current_student_ids

    if not to_remove_ids:
        if not_enrolled_ids:
            raise HttpError(400, f"Студенты с ID {list(not_enrolled_ids)} не записаны на этот курс")
        raise HttpError(400, "Нет студентов для удаления")

    if to_remove_ids:
        course.students.remove(*to_remove_ids)

    course.refresh_from_db()

    response_data = {
        "id": course.id,
        "title": course.title,
        "code": course.code,
        "students": list(course.students.values('id', 'full_name', 'email')),
        "removed_students": list(to_remove_ids),
        "removed_count": len(to_remove_ids)
    }

    if not_enrolled_ids:
        raise HttpError(400, f"Студенты с ID {list(not_enrolled_ids)} не были записаны на курс" )
    return response_data

