from fastapi import FastAPI,Query
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

class SchemaHotel(BaseModel):
    address: str
    name: str
    starts: int
    has_spa: bool

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)


@app.get('/hotels')
def get_hotels(location : str,
               date_from: date,
               date_last: date,
               has_spa: Optional[bool] = None,
               stars: Optional[int] = Query(None,ge=1,le=5),
               ) -> list[SchemaHotel]:
    hotels = [ 
        {
            "address": "Гагарина 1, Алтай",
            "name" : "Алтай статус",
            "stars": 5,
        }
    ]
    return hotels

class SchemaBookingPost(BaseModel):
    room_id: int
    date_from: date
    date_last: date



@app.post('/bookings')
def add_booking(booking: SchemaBookingPost):
    pass