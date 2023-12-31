from datetime import date
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker
from app.bookings.models import Bookings
from sqlalchemy import func, insert, select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.logger import logger


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_bookings_by_room_id(cls, _room_id: int):
        async with async_session_maker() as session:
            quary = (
                select(Bookings)
                .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
                .where(cls.model.room_id == _room_id)
            )
            result = await session.execute(quary)
            return result.scalars().all()

    @classmethod
    async def find_bookings_with_images(cls, user_id: int):
        async with async_session_maker() as session:
            quary = (
                select(Bookings.__table__.columns)
                .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
                .where(Bookings.user_id == user_id)
            )
            result = await session.execute(quary)
            return result.scalars().all()

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        with booked_rooms as
        (
            select * from bookings
            where room_id = 1
            and (date_from >= '2023-05-15' and date_from <= '2023-06-20')
            or (date_from <= '2023-05-15' and date_to > '2023-05-15')
        )
        select rooms.quantity - count(booked_rooms.room_id)  from rooms --
        left join booked_rooms using (id)
        where rooms.id = 1
        group by rooms.quantity,booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
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
                        )
                    )
                    .cte("booked_rooms")
                )
                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(
                        booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                    )
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar()
                if rooms_left and rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )
                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as err:
            if isinstance(err, SQLAlchemyError):
                msg = "database "
            elif isinstance(err, Exception):
                msg = "Unknown "
            msg += "Exc: cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)
