from fastapi import FastAPI,Query
from fastapi.staticfiles import StaticFiles
from typing import Optional
from datetime import date
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images

app = FastAPI()

app.mount(path='/static',app=StaticFiles(directory='app/static'),name="static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)


# Откуда можем принимать запросы
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Отвечает за запрос куки
    allow_methods=["GET","POST","OPTION","DELETE","PATCH","PUT"],
    allow_headers=["Content-Type","Set-Cookie","Access-Control-Allow-Origin","Access-Control-Allow-Headers", "Authorization"],
)