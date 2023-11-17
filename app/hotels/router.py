import asyncio
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, Request
from app.hotels.schemas import SHotel
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO

router = APIRouter(prefix="/hotels",
                   tags=['Hotels'])


@router.get("/all")
async def get_hotels():
    return await HotelDAO.get_all_hotels()


@router.get("/bylocation")
@cache(expire=60)
async def get_hotels_by_location( location: str, date_from: date, date_to: date):
    await asyncio.sleep(2) # в первый раз будем ждать, затем результат кэшируется и ответ моментальный в течении 60 секунд
    hotels = await HotelDAO.get_hotels_by_location(location,date_from,date_to)
    return hotels