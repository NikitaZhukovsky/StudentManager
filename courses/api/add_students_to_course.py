from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from courses.models import Course
from students.models import Student
from courses.schemas import AddStudentsToCourseSchema


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

