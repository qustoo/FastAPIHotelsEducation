from datetime import date
from fastapi import APIRouter, Depends, Request

from app.hotels.dao import HotelDAO

router = APIRouter(prefix="/hotels",
                   tags=['Hotels'])


@router.get("/all")
async def get_hotels():
    return await HotelDAO.get_all_hotels()


@router.get("/bylocation")
async def get_hotels_by_location( location: str, date_from: date, date_to: date):
    hotels = await HotelDAO.get_hotels_by_location(location,date_from,date_to)
    return hotels