from ninja import NinjaAPI
from users.views import auth_router
from students.views import student_router


api = NinjaAPI(
    version='1.0.0',
)

api.add_router("/users/", auth_router, tags=["Users"])
api.add_router("/students", student_router, tags=["Students"])

