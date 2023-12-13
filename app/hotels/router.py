import asyncio
from datetime import date, datetime, timedelta
from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, Query, Request
from app.exceptions import ErrorOrderOfDates, IsToLongPeriodToBooked
from app.hotels.schemas import SHotel, SHotelInfo
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/all", response_model=List[SHotel], response_model_exclude_none=True)
async def get_hotels():
    return await HotelDAO.get_all_hotels()

@router.get("/id/{hotel_id}", include_in_schema=True)
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    return await HotelDAO.find_one_or_none(id=hotel_id)



@router.get(
    "/bylocation", response_model=list[SHotelInfo], response_model_exclude_none=True
)
# @cache(expire=60) redis cache
async def get_hotels_by_location_and_time(
    date_from: Annotated[
        date, Query(..., description=f"Например, {datetime.now().date()}")
    ] = date(2023, 1, 1),
    date_to: Annotated[
        date,
        Query(
            ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
        ),
    ] = date(2023, 1, 15),
    location: str = "Алтай",
):
    if date_from > date_to:
        raise ErrorOrderOfDates
    if (date_to - date_from).days > 31:
        raise IsToLongPeriodToBooked
    hotels = await HotelDAO.get_hotels_by_location(location, date_from, date_to)
    return hotels
