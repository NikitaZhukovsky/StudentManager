from django.shortcuts import get_object_or_404
from submissions.models import Submission


def delete_submission(request, submission_id: int):
    submission = get_object_or_404(Submission, id=submission_id)

    student_name = submission.student.full_name
    assignment_title = submission.assignment.title

    submission.delete()

    return {
        "message": f"Работа '{assignment_title}' студента '{student_name}' удалена"
    }

