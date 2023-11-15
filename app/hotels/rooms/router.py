from datetime import date
from fastapi import APIRouter, Depends, Request
from app.hotels.rooms.dao import RoomDAO


router = APIRouter(prefix="/rooms",
                   tags=['Rooms'])



@router.get("/{hotel_id}/rooms")
async def get_all_rooms(hotel_id : int,date_from: date, date_to: date):
    result = await RoomDAO.get_all_rooms_by_dates(hotel_id,date_from,date_to)
    return result
