# app/models.py

from sqlalchemy import Boolean, Column, Integer, String, Float
from .database import Base # Use a relative import

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
    is_offer = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    owner = Column(String, nullable=True) #added to test the migration