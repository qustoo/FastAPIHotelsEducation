from datetime import date
from pprint import pprint
from fastapi import APIRouter, Depends, Request
from fastapi.background import BackgroundTasks
from fastapi.exceptions import ResponseValidationError
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.bookings.schemas import SBooking, SBookingInfo, SBookingDates
from app.database import async_session_maker
from app.bookings.models import Bookings
from sqlalchemy import select
from app.bookings.dao import BookingDAO
from fastapi_versioning import VersionedFastAPI, version

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/byimages")
async def get_bookings_with_images(
    user: Users = Depends(get_current_user),
) -> list[SBooking]:
    result = await BookingDAO.find_bookings_with_images(user_id=user["Users"].id)
    pprint(result)
    return result


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user),
):  # -> list[SBookingDates]:
    return await BookingDAO.find_all(user_id=user["Users"].id)


@router.post("/add")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user["Users"].id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return booking
    # background_tasks: BackgroundTasks,
    # вариант с встроенным BackgroundTasks
    # background_tasks.add_task()


@router.delete("/{booking_id}")
async def remove_bookings(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.remove(id=booking_id, user_id=user["Users"].id)
    return
