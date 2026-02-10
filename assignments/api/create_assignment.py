from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from datetime import date
from courses.models import Course
from assignments.models import Assignment
from assignments.schemas import AssignmentCreateSchema


def create_assignment(request, data: AssignmentCreateSchema):
    course = get_object_or_404(Course, id=data.course_id)

    if data.due_date < date.today():
        raise HttpError(400, "Дата сдачи не может быть в прошлом")

    assignment = Assignment.objects.create(
        title=data.title,
        description=data.description,
        course=course,
        due_date=data.due_date
    )

    return {
        "id": assignment.id,
        "title": assignment.title,
        "description": assignment.description,
        "course_id": assignment.course_id,
        "course_title": assignment.course.title,
        "due_date": assignment.due_date
    }

