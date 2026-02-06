from ninja import NinjaAPI
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja_jwt.tokens import RefreshToken
from .schemas import RegisterSchema, LoginSchema, TokenSchema

api = NinjaAPI(version='1.0.0')


@api.post("/register", response={200: TokenSchema})
def register(request, data: RegisterSchema):
    if User.objects.filter(email=data.email).exists():
        return 400, {"detail": "Пользователь с таким email уже существует"}
    try:
        user = User.objects.create_user(username=data.username,
                                        email=data.email,
                                        password=data.password)
    except Exception as e:
        return 400, {"detail": f"Ошибка создания пользователя {e}"}

    refresh = RefreshToken.for_user(user)

    return 200, {"access": str(refresh.access_token),
                 "refresh": str(refresh)}


@api.post("/login")
def login(request, data: LoginSchema):
    try:
        user_obj = User.objects.get(email=data.email)

        user = authenticate(username=user_obj.username, password=data.password)
    except Exception as e:
        user = None
        raise f'Ошибка: {e}'

    if not user:
        return {"error": "Некорректные данные"}

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

