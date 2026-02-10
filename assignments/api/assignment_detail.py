from django.shortcuts import get_object_or_404
from assignments.models import Assignment


def get_assignment(request, assignment_id: int):
    assignment = get_object_or_404(
        Assignment.objects.select_related('course'),
        id=assignment_id
    )

    return {
        "id": assignment.id,
        "title": assignment.title,
        "description": assignment.description,
        "course_id": assignment.course_id,
        "course_title": assignment.course.title,
        "due_date": assignment.due_date
    }

