from ninja import Schema
from pydantic import EmailStr, field_validator


class RegisterSchema(Schema):
    username: str
    email: EmailStr
    password: str
    password_confirm: str

    @field_validator('password_confirm')
    def passwords_mathc(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Пароли не совпадают')
        return v


class LoginSchema(Schema):
    email: EmailStr
    password: str


class TokenSchema(Schema):
    access: str
    refresh: str

