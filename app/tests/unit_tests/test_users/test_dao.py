import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "user_id,email, exists_present",
    [(1, "test@test.com", True), (2, "artem@example.com", True), (3, "", False)],
)
async def test_find_user_by_id(user_id, email, exists_present):
    user = await UsersDAO.find_by_id(user_id)
    if exists_present:
        assert user
        assert user["Users"].email == email
        assert user["Users"].id == user_id
    else:
        assert not user
