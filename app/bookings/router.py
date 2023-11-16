from datetime import date
from fastapi import APIRouter, Depends, Request
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.bookings.schemas import SBooking
from app.database import async_session_maker
from app.bookings.models import Bookings
from sqlalchemy import select
from app.bookings.dao import BookingDAO
router = APIRouter(
    prefix="/bookings",
    tags=['Бронирование']
)

@router.get("")
async def get_bookings(user : Users = Depends(get_current_user)): # -> list[SBooking]:
    return await BookingDAO.find_all(user_id = user["Users"].id)

@router.post("/add")
async def add_booking(
    room_id : int, date_from : date, date_to: date,
    user : Users = Depends(get_current_user)):
    booking =await BookingDAO.add(user["Users"].id,room_id,date_from,date_to)
    if not booking:
        raise RoomCannotBeBooked 
    
@router.delete("{booking_id}")
async def remove_bookings(booking_id : int,user : Users = Depends(get_current_user)):
    await BookingDAO.remove(id=booking_id,user_id = user["Users"].id)
    return    