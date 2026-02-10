from django.shortcuts import get_object_or_404
from students.models import Student


def get_student(request, student_id: int):
    student = get_object_or_404(Student, id=student_id)
    return {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email
    }

