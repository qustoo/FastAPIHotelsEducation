from httpx import AsyncClient
import pytest

# Запуск с отображением print'а в тесте -> pytest -v -s
@pytest.mark.parametrize("email,password,status_code",
                         [
                             ("kot@pes.com","kotopes",200),
                             ("kot@pes.com","kotopes",409),
                             ("pes@kot.com","kotopes",200),
                             ("abced","kotopes",422),

                         ])
async def test_register_user(email : str, password: str, status_code : int, async_client: AsyncClient):
    response = await async_client.post("/auth/register", json = {
        "email": email, 
        "password": password
    })
    print(response)
    assert response.status_code == status_code

@pytest.mark.parametrize("email,password,status_code",
                         [
                             ("test@test.com","test",200),
                             ("artem@example.com","artem",200)
                         ])
async def test_login_user(email,password,status_code,async_client):
    response = await async_client.post("/auth/login", json = {
        "email": email, 
        "password": password
    })
    assert response.status_code == status_code