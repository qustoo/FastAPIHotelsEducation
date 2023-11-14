from app.database import Base
from sqlalchemy import Column,Integer,String,JSON


class Hotels(Base):
    __tablename__ = "hotels"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    location = Column(String)
    services = Column(JSON)
    rooms_quantity = Column(Integer)
    image_ig = Column(Integer)