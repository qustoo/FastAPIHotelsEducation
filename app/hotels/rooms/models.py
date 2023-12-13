from typing import Optional
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship,mapped_column,Mapped
from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    hotel_id: Mapped[str] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str] = mapped_column(String(50),nullable=False)
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[Optional[list[str]]] = mapped_column(JSON,nullable=False)
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel: Mapped['Hotels'] = relationship(back_populates='rooms')
    booking: Mapped[list['Bookings']] = relationship(back_populates='room')

    def __str__(self):
        return f"Комната {self.name}"