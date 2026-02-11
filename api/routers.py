from ninja import NinjaAPI
from users.views import auth_router
from students.router import student_router
from courses.router import course_router
from assignments.router import assignment_router
from submissions.router import submission_router

api = NinjaAPI(
    version='1.0.0',
)

api.add_router("/users/", auth_router, tags=["Users"])
api.add_router("/students", student_router, tags=["Students"])
api.add_router("/course", course_router, tags=["Courses"])
api.add_router("/assignments", assignment_router, tags=["Assignments"])
api.add_router("/submissions", submission_router, tags=["Submissions"])

