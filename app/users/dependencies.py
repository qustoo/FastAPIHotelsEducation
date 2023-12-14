from datetime import datetime
from fastapi import Depends, Request, status
from jose import jwt, JWTError
from app.exceptions import (
    TokenAbsentException,
    UserIsNotPresentException,
    IncorrectTokenFormatException,
)
from app.users.dao import UsersDAO
from app.config import settings


def get_token(request: Request):
    token = request.cookies.get("bookings_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(
    token: str = Depends(get_token),
):  # зависимость от функции, сначала вызывваем get_token, потом get_current_user
    try:
        print('token',token)
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError as err:
        print(f'{err=}')
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenAbsentException
    user_email: str = payload.get("sub")
    user = await UsersDAO.find_one_or_none(email=user_email)
    if not user:
        raise UserIsNotPresentException
    return user
