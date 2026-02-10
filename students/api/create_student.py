from students.models import Student
from students.schemas import StudentCreateSchema, StudentGetSchema


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

