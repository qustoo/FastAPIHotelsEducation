from httpx import AsyncClient
import pytest
from app.tests.conftest import AsyncClient


@pytest.mark.parametrize(
    "location,date_from,date_to,status_code,full_detail",
    [
        ("Алтай", "2023-01-01", "2023-01-10", 200, None),
        (
            "Алтай",
            "2023-01-01",
            "2023-03-03",
            400,
            "you cannot booked room more then 1 mounth",
        ),
        ("Алтай", "2023-05-01", "2023-03-03", 400, "Incorrect order of dates"),
    ],
)
async def test_get_hotels_by_location(
    location, date_from, date_to, status_code, full_detail, async_client: AsyncClient
):
    # hotels/bylocation

    response = await async_client.get(
        "hotels/bylocation",
        params={"location": location, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        assert response.json()["detail"] == full_detail
