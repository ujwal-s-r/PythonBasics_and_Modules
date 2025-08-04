# app/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_item(db: AsyncSession, item_id: int):
    """Reads a single item from the database by its ID."""
    result = await db.get(models.Item, item_id)
    return result

async def create_item(db: AsyncSession, item: schemas.ItemCreate):
    """Creates a new item in the database."""
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def update_item(db: AsyncSession, item_id: int, item_update: schemas.ItemCreate):
    """Updates an existing item in the database."""
    db_item = await db.get(models.Item, item_id)
    if not db_item:
        return None

    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def delete_item(db: AsyncSession, item_id: int):
    """Deletes an item from the database."""
    db_item = await db.get(models.Item, item_id)
    if not db_item:
        return None
    
    await db.delete(db_item)
    await db.commit()
    return db_item