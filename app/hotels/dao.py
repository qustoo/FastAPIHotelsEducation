from datetime import date

from fastapi import logger
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker,engine
from app.hotels.models import Hotels
from sqlalchemy import func, insert, select,and_,or_
from app.dao.base import BaseDAO

class HotelDAO(BaseDAO):
    model = Hotels


    @classmethod
    async def get_all_hotels(cls):
        async with async_session_maker() as session:
            all_hotels = select(cls.model)
            result = await session.execute(all_hotels)
            return result.mappings().all()


    # поиск по паттерну региона, like('%location%')
    @classmethod
    async def get_hotels_by_location(cls, location: str, date_from: date, date_to: date): 
        booked_rooms = (
            select(Bookings.room_id, 
                   func.count(Bookings.room_id).label("rooms_booked")
                   ).select_from(Bookings
                   ).where(
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                   ).group_by(
                     Bookings.room_id  
                   ).cte("booked_rooms")
        )
        booked_hotels = (
            select(Rooms.hotel_id, func.sum(
                    Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
            ).label("rooms_left"))
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )
        quary = (
                select(
                Hotels.__table__.columns,
                booked_hotels.c.rooms_left,
                )
                .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
                .where(
                    and_(
                        booked_hotels.c.rooms_left > 0,
                        Hotels.location.like(f"%{location}%"),
                    )
                )
        )
        #logger.debug(booked_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

        async with async_session_maker() as session:   
            result = await session.execute(quary)
            return result.mappings().all()


