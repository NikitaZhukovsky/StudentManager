from django.shortcuts import get_object_or_404
from submissions.models import Submission


def get_submission(request, submission_id: int):
    submission = get_object_or_404(
        Submission.objects.select_related(
            'student', 'assignment', 'assignment__course'
        ),
        id=submission_id
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

