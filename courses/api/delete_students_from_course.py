from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from courses.models import Course
from courses.schemas import RemoveStudentsFromCourseSchema


def remove_students_from_course(
        request,
        course_id: int,
        data: RemoveStudentsFromCourseSchema
):
    course = get_object_or_404(Course.objects.prefetch_related('students'), id=course_id)

    current_student_ids = set(course.students.values_list('id', flat=True))
    requested_to_remove_ids = set(data.student_ids)

    to_remove_ids = current_student_ids.intersection(requested_to_remove_ids)
    not_enrolled_ids = requested_to_remove_ids - current_student_ids

    if not to_remove_ids:
        if not_enrolled_ids:
            raise HttpError(400, f"Студенты с ID {list(not_enrolled_ids)} не записаны на этот курс")
        raise HttpError(400, "Нет студентов для удаления")

    if to_remove_ids:
        course.students.remove(*to_remove_ids)

    course.refresh_from_db()

    response_data = {
        "id": course.id,
        "title": course.title,
        "code": course.code,
        "students": list(course.students.values('id', 'full_name', 'email')),
        "removed_students": list(to_remove_ids),
        "removed_count": len(to_remove_ids)
    }

    if not_enrolled_ids:
        raise HttpError(400, f"Студенты с ID {list(not_enrolled_ids)} не были записаны на курс" )
    return response_data

