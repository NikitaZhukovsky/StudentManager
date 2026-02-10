from ninja import Query
from ninja.pagination import paginate, PageNumberPagination
from django.db.models import Q
from students.models import Student
from students.schemas import StudentFilterSchema


@paginate(PageNumberPagination, page_size=10)
def list_students(
        request,
        filters: StudentFilterSchema = Query(...)
):
    queryset = Student.objects.all()

    if filters.search:
        queryset = queryset.filter(
            Q(full_name__icontains=filters.search) |
            Q(email__icontains=filters.search)
        )

    order_field = filters.order_by
    if filters.order.lower() == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(order_field)

    return queryset

