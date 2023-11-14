from fastapi import APIRouter
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
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.find_all()