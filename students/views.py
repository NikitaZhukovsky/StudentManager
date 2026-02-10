from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from django.db.models import Q
from typing import List
from .models import Student
from .schemas import (
    StudentCreateSchema,
    StudentUpdateSchema,
    StudentGetSchema,
    StudentFilterSchema
)

student_router = Router(auth=JWTAuth())


@student_router.get("/", response=List[StudentGetSchema])
@paginate(PageNumberPagination, page_size=10)
def list_students(
        request,
        filters: StudentFilterSchema = Query(...)
):
    queryset = Student.objects.all()

    if filters.search:
        queryset = queryset.filter(
            Q(full_name__icontains=filters.search) |
            Q(email__icontains=filters.search)
        )

    order_field = filters.order_by
    if filters.order.lower() == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(order_field)

    return queryset


@student_router.post("/", response=StudentGetSchema)
def create_student(request, data: StudentCreateSchema):
    student = Student.objects.create(
        full_name=data.full_name,
        email=data.email
    )
    return {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email
    }


@student_router.get("/{student_id}/", response=StudentGetSchema)
def get_student(request, student_id: int):
    student = get_object_or_404(Student, id=student_id)
    return {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email
    }


@student_router.patch("/{student_id}/", response=StudentGetSchema)
def update_student(request, student_id: int, data: StudentUpdateSchema):

    student = get_object_or_404(Student, id=student_id)

    if data.full_name is not None:
        student.full_name = data.full_name
    if data.email is not None:
        student.email = data.email

    student.save()

    return {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email
    }


@student_router.delete("/{student_id}/")
def delete_student(request, student_id: int):
    student = get_object_or_404(Student, id=student_id)
    student.delete()

    return {"success": True, "message": "Студент удален"}