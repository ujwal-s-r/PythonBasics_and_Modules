# app/schemas.py

from pydantic import BaseModel
from typing import Optional

# Shared properties
class ItemBase(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = False
    description: Optional[str] = None

# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass

# Properties to return to client
class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True # Pydantic V2, replaces orm_mode