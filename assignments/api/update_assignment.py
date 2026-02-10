from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from datetime import date
from courses.models import Course
from assignments.models import Assignment
from assignments.schemas import AssignmentUpdateSchema


def update_assignment(request, assignment_id: int, data: AssignmentUpdateSchema):
    assignment = get_object_or_404(
        Assignment.objects.select_related('course'),
        id=assignment_id
    )

    if data.title is not None:
        assignment.title = data.title

    if data.description is not None:
        assignment.description = data.description

    if data.course_id is not None and data.course_id != assignment.course_id:
        course = get_object_or_404(Course, id=data.course_id)
        assignment.course = course

    if data.due_date is not None:
        if data.due_date < date.today():
            raise HttpError(400, "Дата сдачи не может быть в прошлом")
        assignment.due_date = data.due_date

    assignment.save()

    return {
        "id": assignment.id,
        "title": assignment.title,
        "description": assignment.description,
        "course_id": assignment.course_id,
        "course_title": assignment.course.title,
        "due_date": assignment.due_date
    }

