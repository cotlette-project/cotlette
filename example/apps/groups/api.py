from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import timedelta
from .models import GroupModel
# from .utils import hash_password, generate_jwt, check_password

from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse, \
    HTMLResponse


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from jose import JWTError, jwt


router = APIRouter()

# Создание таблицы при запуске приложения
@router.on_event("startup")
def create_tables():
    GroupModel.create_table()
    if not GroupModel.objects.filter(name="Owners").first():  # FIXME
        test_group = GroupModel.objects.create(name="Owners")
        print('test_group', test_group)

# # Pydantic-модель для входа пользователя
# class UserLogin(BaseModel):
#     email: str
#     password: str

# # Pydantic-модель для токена
# class Token(BaseModel):
#     access_token: str
#     token_type: str

# # Pydantic-модель для данных токена
# class TokenData(BaseModel):
#     email: Union[str] = None


# # Создание таблицы при запуске приложения
# @router.on_event("startup")
# def create_tables():
#     UserModel.create_table()


# # Создание нового пользователя (POST)
# @router.post("/", response_model=None)
# async def create_user(user: UserCreate):
#     hashed_password = await hash_password(user.password)
#     new_user = UserModel.objects.create(
#         name=user.name,
#         age=user.age,
#         email=user.email,
#         password_hash=hashed_password
#     )
#     return User(
#         name=new_user.name,
#         age=new_user.age,
#         email=new_user.email
#     )


# # Получение всех пользователей (GET)
# @router.get("/", response_model=list[User])
# def get_users():
#     users = UserModel.objects.all()
#     return [User(name=user.name, age=user.age, email=user.email) for user in users]