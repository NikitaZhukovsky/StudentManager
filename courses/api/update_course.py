from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from courses.models import Course
from courses.schemas import CourseUpdateSchema


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

