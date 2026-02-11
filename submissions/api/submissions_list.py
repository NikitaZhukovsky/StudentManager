from ninja import Query
from ninja.pagination import paginate, PageNumberPagination
from submissions.models import Submission
from submissions.schemas import SubmissionGetSchema, SubmissionFilterSchema


@paginate(PageNumberPagination, page_size=10)
def list_submissions(
        request,
        filters: SubmissionFilterSchema = Query(...)
):
    queryset = Submission.objects.all().select_related(
        'student', 'assignment', 'assignment__course'
    )

    if filters.student_id:
        queryset = queryset.filter(student_id=filters.student_id)

    if filters.assignment_id:
        queryset = queryset.filter(assignment_id=filters.assignment_id)

    if filters.course_id:
        queryset = queryset.filter(assignment__course_id=filters.course_id)

    if filters.from_date:
        queryset = queryset.filter(submitted_at__gte=filters.from_date)

    if filters.to_date:
        queryset = queryset.filter(submitted_at__lte=filters.to_date)

    order_field = filters.order_by
    if filters.order.lower() == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(order_field)

    return [
        {
            "id": submission.id,
            "student_id": submission.student_id,
            "assignment_id": submission.assignment_id,
            "file_path": submission.file_path,
            "submitted_at": submission.submitted_at,
            "student_name": submission.student.full_name,
            "assignment_title": submission.assignment.title,
            "course_title": submission.assignment.course.title,
        }
        for submission in queryset
    ]

