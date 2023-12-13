from typing import Optional
from app.database import Base
from sqlalchemy import Column,Integer,String,JSON
from sqlalchemy.orm import relationship,Mapped,mapped_column


class Hotels(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String(50),nullable=False)
    location: Mapped[str] = mapped_column(String(100))
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[str] = mapped_column(nullable=True)
    rooms: Mapped[list['Rooms']] = relationship(back_populates='hotel')
    def __str__(self):
        return f"Отель {self.name} Локация {self.location[:20]}"