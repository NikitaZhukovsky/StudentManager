from ninja.errors import HttpError
from courses.models import Course
from courses.schemas import CourseCreateSchema


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

