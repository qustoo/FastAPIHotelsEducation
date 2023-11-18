import pytest
from datetime import datetime
from app.bookings.dao import BookingDAO

async def test_add_get_booking():
    new_booking = await BookingDAO.add(
        user_id = 2,
        room_id = 2, 
        date_from =datetime.strptime('2023-07-10',"%Y-%M-%d"),
        date_to = datetime.strptime('2023-07-24',"%Y-%M-%d")
    )
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None


@pytest.mark.parametrize("user_id,room_id",
                         [
                            (2,2),
                            (2,3),
                            (1,4),
                            (1,4),
                         ])
async def test_crud_operation_with_bookings(user_id,room_id):
    # Добавление бронирования
    new_booking = await BookingDAO.add(
                user_id = user_id,
                room_id = room_id, 
                date_from =datetime.strptime('2023-07-10',"%Y-%M-%d"),
                date_to = datetime.strptime('2023-07-24',"%Y-%M-%d"))
    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    # Проверка на добавление
    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
    assert new_booking is not None

    # Удаление
    await BookingDAO.remove(id = new_booking['Bookings'].id,
                            user_id = user_id)
    
    # Проверка на удаление 
    removed_booking = await BookingDAO.find_by_id(new_booking['Bookings'].id)
    assert removed_booking is None