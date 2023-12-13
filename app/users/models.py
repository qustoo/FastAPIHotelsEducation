from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    booking: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f"Id = {self.id}; User {self.email}"
