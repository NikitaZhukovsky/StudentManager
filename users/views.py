from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken
from .schemas import RegisterSchema, LoginSchema, TokenSchema
from ninja import Router


auth_router = Router()


@auth_router.post("/register", response={200: TokenSchema})
def register(request, data: RegisterSchema):
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, f"Пользователь с таким email уже существует")
    try:
        user = User.objects.create_user(username=data.username,
                                        email=data.email,
                                        password=data.password)
    except Exception as e:
        raise HttpError(400, f"Ошибка создания пользователя {e}")

    refresh = RefreshToken.for_user(user)

    return {"access": str(refresh.access_token),
            "refresh": str(refresh)}


@auth_router.post("/login")
def login(request, data: LoginSchema):
    try:
        user_obj = User.objects.get(email=data.email)

        user = authenticate(username=user_obj.username, password=data.password)
    except Exception as e:
        raise HttpError(400, f'Ошибка: {e}')

    if not user:
        raise HttpError(400, "Некорректные данные")

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

