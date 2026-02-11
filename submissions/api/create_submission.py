from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from students.models import Student
from assignments.models import Assignment
from submissions.models import Submission
from submissions.schemas import SubmissionCreateSchema


def create_submission(request, data: SubmissionCreateSchema):
    student = get_object_or_404(Student, id=data.student_id)

    assignment = get_object_or_404(Assignment, id=data.assignment_id)

    if data.submitted_at > assignment.due_date:
        raise HttpError(400, "Дата сдачи прошла")

    submission = Submission.objects.create(
        student=student,
        assignment=assignment,
        file_path=data.file_path,
        submitted_at=data.submitted_at
    )

    return {
        "id": submission.id,
        "student_id": submission.student_id,
        "assignment_id": submission.assignment_id,
        "file_path": submission.file_path,
        "submitted_at": submission.submitted_at,
        "student_name": submission.student.full_name,
        "assignment_title": submission.assignment.title,
        "course_title": submission.assignment.course.title,
    }

