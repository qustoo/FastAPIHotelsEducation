from datetime import date
from app.hotels.models import Hotels

from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker,engine
from sqlalchemy import func, insert, select,and_,or_
from app.dao.base import BaseDAO

class RoomDAO(BaseDAO):
    model = Rooms

    '''
    Получение списка комнат
    Пример эндпоинта: /hotels/1/rooms.
    HTTP метод: GET.
    HTTP код ответа: 200.
    Описание: возвращает список всех номеров определенного отеля.
    Нужно быть авторизованным: нет.
    Параметры: параметр пути hotel_id и параметры запроса date_from, date_to.
    Ответ пользователю: для каждого номера должно быть указано: id, hotel_id, name,
    description, services, price, quantity, image_id, total_cost (стоимость бронирования
    номера за весь период), rooms_left (количество оставшихся номеров).
    '''
    @classmethod
    async def get_all_rooms_by_dates(cls,hotel_id: int,date_from : date, date_to :date):
        booked_rooms = (
            select(Bookings.room_id, Bookings.total_cost, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
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
            .group_by(Bookings.room_id, Bookings.total_cost)
            .cte("booked_rooms")
        )
        
        quary = (
            select(
                Rooms.__table__.columns,
                #(Rooms.price * (date_to - date_from).days).label("total_cost"),
                (Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left"),
            )
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(
                Rooms.hotel_id == hotel_id
            )
        )
        #quary = select("*").select_from(Rooms).where(Rooms.hotel_id == hotel_id)
        async with async_session_maker() as session:
            result = await session.execute(quary)
            return result.mappings().all()
        
    # список всех комнат определенного отеля
    @classmethod
    async def get_all_rooms_by_hotel_id(cls,hotel_id):
        quary = select("*").select_from(Rooms).where(Rooms.hotel_id == hotel_id)
        async with async_session_maker() as session:
            result = await session.execute(quary)
            return result.mappings().all()

