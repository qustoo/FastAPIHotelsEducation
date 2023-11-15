from fastapi import APIRouter, HTTPException
from app.users.auth import get_password_hash
from app.users.dao import UsersDAO

from app.users.schemas import SUserRegister

router = APIRouter(
    prefix="/auth",
    tags = ['Auth & Пользователи']
)

@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(401,"sth go error")
    hashed_password= get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email,hashed_password=hashed_password)