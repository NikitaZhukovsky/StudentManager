from ninja import Query
from ninja.pagination import paginate, PageNumberPagination
from django.db.models import Q
from datetime import date
from assignments.models import Assignment
from assignments.schemas import AssignmentGetSchema, AssignmentFilterSchema


@paginate(PageNumberPagination, page_size=10)
def list_assignments(
        request,
        filters: AssignmentFilterSchema = Query(...)
):
    queryset = Assignment.objects.all().select_related('course')

    if filters.search:
        queryset = queryset.filter(
            Q(title__icontains=filters.search) |
            Q(description__icontains=filters.search)
        )

    if filters.course_id:
        queryset = queryset.filter(course_id=filters.course_id)

    if filters.upcoming:
        queryset = queryset.filter(due_date__gte=date.today())

    order_field = filters.order_by

    queryset = queryset.order_by(order_field)

    return [
        {
            "id": assignment.id,
            "title": assignment.title,
            "description": assignment.description,
            "course_id": assignment.course_id,
            "course_title": assignment.course.title,
            "due_date": assignment.due_date
        }
        for assignment in queryset
    ]

