from django.shortcuts import get_object_or_404
from courses.models import Course


def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course_title = course.title

    course.delete()

    return {
        "message": f"Курс '{course_title}' удален"
    }

