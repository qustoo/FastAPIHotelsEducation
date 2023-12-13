from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Query, Request
from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.rooms.dao import RoomDAO


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(
        ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
    ),
) -> list[SRoomInfo]:
    result = await RoomDAO.get_rooms_by_times(hotel_id, date_from, date_to)
    return result
