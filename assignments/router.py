from ninja import Router
from ninja_jwt.authentication import JWTAuth
from typing import List
from assignments.api.assignments_list import list_assignments
from assignments.api.create_assignment import create_assignment
from assignments.api.assignment_detail import get_assignment
from assignments.api.update_assignment import update_assignment
from assignments.api.delete_assignment import delete_assignment
from assignments.schemas import (
    AssignmentCreateSchema,
    AssignmentUpdateSchema,
    AssignmentGetSchema,
    AssignmentFilterSchema
)

assignment_router = Router(auth=JWTAuth())

assignment_router.get("/", response=List[AssignmentGetSchema])(list_assignments)
assignment_router.post("/", response=AssignmentGetSchema)(create_assignment)
assignment_router.get("/{assignment_id}/", response=AssignmentGetSchema)(get_assignment)
assignment_router.patch("/{assignment_id}/", response=AssignmentGetSchema)(update_assignment)
assignment_router.delete("/{assignment_id}/")(delete_assignment)

