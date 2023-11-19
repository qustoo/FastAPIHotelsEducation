import asyncio
from datetime import date, datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, Query, Request
from app.exceptions import ErrorOrderOfDates,IsToLongPeriodToBooked
from app.hotels.schemas import SHotel, SHotelInfo
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO

router = APIRouter(prefix="/hotels",
                   tags=['Hotels'])


@router.get("/all")
async def get_hotels():
    return await HotelDAO.get_all_hotels()


@router.get("/bylocation")
#@cache(expire=60) redis cache
async def get_hotels_by_location(location: str, 
                                date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
                                date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
) -> list[SHotelInfo]:
    if date_from > date_to:
        raise ErrorOrderOfDates
    if (date_to - date_from).days > 31:
        raise IsToLongPeriodToBooked
    #await asyncio.sleep(2) # в первый раз будем ждать, затем результат кэшируется и ответ моментальный в течении 60 секунд
    hotels = await HotelDAO.get_hotels_by_location(location,date_from,date_to)
    return hotels