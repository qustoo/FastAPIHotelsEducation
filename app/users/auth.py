from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.users.dao import UsersDAO
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(_email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=_email)
    if not user and not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict) -> str:
    print(data)
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt
