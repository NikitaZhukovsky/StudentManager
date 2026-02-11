from ninja import Schema
from pydantic import EmailStr, field_validator


class RegisterSchema(Schema):
    username: str
    email: EmailStr
    password: str
    password_confirm: str

    @field_validator('password_confirm')
    def passwords_mathc(cls, value, info):
        if 'password' in info.data and value != info.data['password']:
            raise ValueError('Пароли не совпадают')
        return value


class LoginSchema(Schema):
    email: EmailStr
    password: str


class TokenSchema(Schema):
    access: str
    refresh: str

