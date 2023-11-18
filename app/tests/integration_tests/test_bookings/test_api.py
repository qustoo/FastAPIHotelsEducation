from pprint import pprint
import pytest

from app.tests.conftest import AsyncClient

@pytest.mark.parametrize("room_id,date_from,date_to,status_code",
                         [
                             *[(4,'2030-05-01','2030-05-15',200)] * 8,
                             (4,'2030-05-01','2030-05-15',409),
                             (4,'2030-05-01','2030-05-15',409)

                         ])
async def test_add_and_get_booking(room_id, date_from,date_to,
                                    status_code,authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.post("/bookings/add",params = {
        "room_id" : room_id,
        "date_from" : date_from,
        "date_to" : date_to,
    })
    assert response.status_code == status_code


    # response = await authenticated_async_client.get('/bookings')

    # await len(response.json()) == booked_rooms
    # assert response.status_code == status_code



async def test_get_and_delete_booking(authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("/bookings")
    existing_bookings = [booking["Bookings"]["id"] for booking in response.json()]
    for booking_id in existing_bookings:
        response = await authenticated_async_client.delete(
            f"/bookings/{booking_id}",
        )

    response = await authenticated_async_client.get("/bookings")
    assert len(response.json()) == 0