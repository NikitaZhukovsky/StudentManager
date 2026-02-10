from ninja import NinjaAPI
from users.views import auth_router


api = NinjaAPI(version='1.0.0')


api.add_router("/users/", auth_router, tags=["Users"])
