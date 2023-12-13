from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column


class Bookings(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[datetime] = mapped_column(Date)
    date_to: Mapped[datetime] = mapped_column(Date)
    price: Mapped[int] = mapped_column(default=1000)
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))
    user: Mapped["Users"] = relationship(back_populates="booking")
    room: Mapped["Rooms"] = relationship(back_populates="booking")
