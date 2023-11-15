from fastapi import APIRouter, Depends, Request
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.bookings.schemas import SBooking
from app.database import async_session_maker
from app.bookings.models import Bookings
from sqlalchemy import select
from app.bookings.dao import BookingDAO
from pprint import pprint
router = APIRouter(
    prefix="/bookings",
    tags=['Бронирование']
)

@router.get("")
async def get_bookings(user : Users = Depends(get_current_user)): # -> list[SBooking]:
    return await BookingDAO.find_all(user_id = 1)#user["Users"].id)
    
    #print(user,type(user),user.email)
    #return await BookingDAO.find_one_or_none
    #return await BookingDAO.find_all()