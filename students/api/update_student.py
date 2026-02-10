from django.shortcuts import get_object_or_404
from students.models import Student
from students.schemas import StudentUpdateSchema


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

