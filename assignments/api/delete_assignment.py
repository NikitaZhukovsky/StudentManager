from django.shortcuts import get_object_or_404
from assignments.models import Assignment


def delete_assignment(request, assignment_id: int):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment_title = assignment.title
    assignment.delete()

    return {"message": f"Задание '{assignment_title}' удалено"}

