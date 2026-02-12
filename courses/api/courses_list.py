from ninja import Query
from ninja.pagination import paginate, PageNumberPagination
from django.db.models import Q
from courses.models import Course
from courses.schemas import CourseFilterSchema


@paginate(PageNumberPagination, page_size=10)
def list_courses(
        request,
        filters: CourseFilterSchema = Query(...)
):
    queryset = Course.objects.all().prefetch_related('students')

    if filters.search:
        queryset = queryset.filter(
            Q(title__icontains=filters.search) |
            Q(code__icontains=filters.search)
        )

    order_field = filters.order_by

    queryset = queryset.order_by(order_field)

    return queryset

