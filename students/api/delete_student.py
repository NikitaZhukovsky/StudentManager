from django.shortcuts import get_object_or_404
from students.models import Student


def delete_student(request, student_id: int):
    student = get_object_or_404(Student, id=student_id)
    student.delete()

    return {"message": "Студент удален"}

