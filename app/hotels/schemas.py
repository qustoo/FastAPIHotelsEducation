from typing import List, Optional

from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: Optional[int]

    class Config:
        from_attributes = True


class SHotelInfo(SHotel):
    rooms_left: int

    class Config:
        from_attributes = True
