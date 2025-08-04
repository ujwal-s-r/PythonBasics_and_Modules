from pydantic import BaseModel, Field
from typing import Optional

class imporovedItem(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50,
        title="Item Name",
        description="The name of the item (3-50 characters)"
    )
    description: Optional[str] = Field(
        None, 
        title="Item Description",
        max_length=300
    )
    price: float = Field(
        gt=0, # gt = "greater than"
        description="The price must be greater than zero"
    )
    is_offer: bool = False
    
class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_offer: bool
    
    
    # in models.py

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Boolean, Integer

# This is the base class for all our models
class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"

    # Columns are defined using modern Mapped and mapped_column
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    price: Mapped[float] = mapped_column(Float)
    is_offer: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str | None] = mapped_column(String(300), nullable=True)