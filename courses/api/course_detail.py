from django.shortcuts import get_object_or_404
from courses.models import Course


def get_course(request, course_id: int):
    course = get_object_or_404(Course.objects.prefetch_related('students'), id=course_id)

    return {
        "id": course.id,
        "title": course.title,
        "code": course.code,
        "students": list(course.students.values('id', 'full_name', 'email'))
    }

