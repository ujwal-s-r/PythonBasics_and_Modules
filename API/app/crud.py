"""This file will contain all the functions that directly interact 
with the database. This isolates our data logic from our API routing logic."""
# app/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_item(db: AsyncSession, item_id: int):
    """Reads a single item from the database by its ID."""
    result = await db.get(models.Item, item_id)
    return result

async def create_item(db: AsyncSession, item: schemas.ItemCreate):
    """Creates a new item in the database."""
    # Create a SQLAlchemy model instance from our Pydantic schema
    db_item = models.Item(**item.model_dump())
    db.add(db_item) # Add the instance to the session
    await db.commit() # Commit the changes to the DB
    await db.refresh(db_item) # Refresh the instance to get the new ID
    return db_item