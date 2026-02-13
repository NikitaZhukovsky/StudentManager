from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from courses.models import Course
from courses.schemas import RemoveStudentsFromCourseSchema


def remove_students_from_course(
        request,
        course_id: int,
        data: RemoveStudentsFromCourseSchema
):
    course = get_object_or_404(Course, id=course_id)

    enrolled_students = course.students.filter(id__in=data.student_ids)
    to_remove_ids = list(enrolled_students.values_list('id', flat=True))

    if not to_remove_ids:
        raise HttpError(400, "Ни один из указанных студентов не записан на этот курс")

    course.students.remove(*to_remove_ids)

    return {
        "id": course.id,
        "title": course.title,
        "code": course.code,
        "students": list(course.students.values('id', 'full_name', 'email')),
        "removed_students": to_remove_ids,
        "removed_count": len(to_remove_ids)
    }

