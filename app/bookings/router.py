from datetime import date
from pprint import pprint
from fastapi import APIRouter, Depends, Request
from fastapi.background import BackgroundTasks
from fastapi.exceptions import ResponseValidationError
from pydantic import TypeAdapter
from app.tasks.task import send_booking_confirmation
from app.exceptions import NoSuchBookings, RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.bookings.schemas import SBooking, SBookingInfo, SBookingDates, SNewBooking
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
    result = await BookingDAO.find_bookings_with_images(user_id=user.id)
    pprint(result)
    return result


@router.get("/is_booked/{id}")
async def get_bookings_by_id(id: int):
    return await BookingDAO.find_bookings_by_room_id(id)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[SBookingInfo]:
    bookings = await BookingDAO.find_all(user_id=user.id)
    if not bookings:
        return []
        # raise NoSuchBookings
    return bookings


@router.post("/add")
@version(1)
async def add_booking(
    new_booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user.id, new_booking.room_id, new_booking.date_from, new_booking.date_to
    )
    if not booking:
        raise RoomCannotBeBooked
    booking = TypeAdapter(SBooking).validate_python(booking).model_dump()
    # Вызов задачи
    send_booking_confirmation.delay(booking, user.email)
    return booking
    # вариант с встроенным BackgroundTasks
    # background_tasks.add_task(send_booking_confirmation,booking,user.email)


@router.delete("/{booking_id}")
async def remove_bookings(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.remove(id=booking_id, user_id=user.id)
