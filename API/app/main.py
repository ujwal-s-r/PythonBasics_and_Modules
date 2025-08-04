# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, models, schemas
from .database import async_sessionmaker, engine

# Create tables (For development only. In production, use Alembic.)
# This is a temporary measure to get our app working without migrations first.
# We will replace this with Alembic in the next lesson.
"""async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)"""

app = FastAPI()

# Dependency to get a DB session
async def get_db():
    async with async_sessionmaker() as session:
        yield session

@app.post("/items/", response_model=schemas.Item)
async def create_item_endpoint(
    item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)
):
    # In a real app, you might want to check if an item with this name already exists
    return await crud.create_item(db=db, item=item)


@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item_endpoint(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item