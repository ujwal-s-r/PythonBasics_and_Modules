# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List # Import List for the read_items endpoint

from . import crud, schemas
from .database import async_sessionmaker

# I am adding the `read_items_endpoint` which was part of our earlier lessons
# but was not explicitly included in the final CRUD lesson, for completeness.

app = FastAPI()

# Dependency to get a DB session
async def get_db():
    """
    Dependency that provides a database session for a single request.
    """
    async with async_sessionmaker() as session:
        yield session

@app.post("/items/", response_model=schemas.Item, status_code=201)
async def create_item_endpoint(
    item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new item in the database.
    """
    # In a real app, you would add a check here to see if an item with the same
    # name already exists to avoid violating the unique constraint.
    # For example:
    # db_item = await crud.get_item_by_name(db, name=item.name)
    # if db_item:
    #     raise HTTPException(status_code=400, detail="Item with this name already registered")
    return await crud.create_item(db=db, item=item)


@app.get("/items/", response_model=List[schemas.Item])
async def read_items_endpoint(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of items with pagination.
    """
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item_endpoint(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single item by its ID.
    """
    db_item = await crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=schemas.Item)
async def update_item_endpoint(
    item_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing item by its ID.
    """
    updated_item = await crud.update_item(db=db, item_id=item_id, item_update=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@app.delete("/items/{item_id}", response_model=schemas.Item)
async def delete_item_endpoint(item_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an item by its ID.
    """
    deleted_item = await crud.delete_item(db=db, item_id=item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item