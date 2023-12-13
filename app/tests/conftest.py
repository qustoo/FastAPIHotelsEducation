import asyncio
from datetime import datetime
import json
import pytest
from sqlalchemy import insert
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.users.models import Users
from app.hotels.rooms.models import Rooms
from app.main import app as fastapi_app
from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.drop_all
        )  # стирает все таблицы которые наследовались от base
        await conn.run_sync(
            Base.metadata.create_all
        )  # создаст все пустые таблицы которые наследовались от base

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%M-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%M-%d")

    async with async_session_maker() as session:
        for Model, Values in [
            (Hotels, hotels),
            (Rooms, rooms),
            (Users, users),
            (Bookings, booking),
        ]:
            quary = insert(Model).values(Values)
            await session.execute(quary)
        await session.commit()


# Для ассинхронных тестов
# scope="session" - запускается один раз на всю сессия прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop  # в моменте возвращаем event loop
    loop.close()


# Отдаем клиента как фикстуру
@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_client:
        yield async_client  #  каждый раз создаем клиента и отдаем его для каждой тестируемой функции


# Отдаем сессию с sqlalchemy как фикстуру
@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session


# Отдает аутентифицированного клиента
@pytest.fixture(scope="session")
async def authenticated_async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_client:
        await async_client.post(
            "/auth/login", json={"email": "test@test.com", "password": "test"}
        )
        assert async_client.cookies["bookings_access_token"]
        yield async_client  #  каждый раз создаем клиента и отдаем его для каждой тестируемой функции
