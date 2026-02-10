from ninja import Router, Query
from ninja_jwt.authentication import JWTAuth
from typing import List
from submissions.api.submissions_list import list_submissions
from submissions.api.create_submission import create_submission
from submissions.api.submission_detail import get_submission
from submissions.api.update_submission import update_submission
from submissions.api.delete_submission import delete_submission
from submissions.schemas import (
    SubmissionCreateSchema,
    SubmissionUpdateSchema,
    SubmissionGetSchema,
    SubmissionFilterSchema
)

submission_router = Router(auth=JWTAuth())

submission_router.get("/", response=List[SubmissionGetSchema])(list_submissions)
submission_router.post("/", response=SubmissionGetSchema)(create_submission)
submission_router.get("/{submission_id}/", response=SubmissionGetSchema)(get_submission)
submission_router.patch("/{submission_id}/", response=SubmissionGetSchema)(update_submission)
submission_router.delete("/{submission_id}/")(delete_submission)