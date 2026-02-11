from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from datetime import date
from students.models import Student
from assignments.models import Assignment
from submissions.models import Submission
from submissions.schemas import SubmissionUpdateSchema


def update_submission(request, submission_id: int, data: SubmissionUpdateSchema):
    submission = get_object_or_404(
        Submission.objects.select_related(
            'student', 'assignment', 'assignment__course'
        ),
        id=submission_id
    )

    if data.student_id is not None:
        student = get_object_or_404(Student, id=data.student_id)
        submission.student = student

    if data.assignment_id is not None:
        assignment = get_object_or_404(Assignment, id=data.assignment_id)

        submission.assignment = assignment

    if data.file_path is not None:
        submission.file_path = data.file_path

    if data.submitted_at is not None:
        if data.submitted_at > date.today():
            raise HttpError(400, "Дата сдачи не может быть в будущем")
        submission.submitted_at = data.submitted_at

    submission.save()

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

