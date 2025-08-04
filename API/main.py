from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from models import imporovedItem, ItemResponse
from fastapi import HTTPException
from customException import ItemNotFoundError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get_user/{id}")
def get_id(id: int):
    return {"id":id, "description":"user id returned"}

@app.get("/query/")
def query(start: int , limit: int):
    fake_db = [i for i in range (10)]
    return {"item": i for i in fake_db[start:limit]}
 
# sen this localhost:8000/query/?start=2&limit=9
# ?-> start query
# &-> seperates


class Item(BaseModel):
    name : str
    id : int
    description : Optional[str] = "none "
    is_offer : bool
    
@app.post("/items/", response_model=ItemResponse) #filter and send in ItemResponse foramt only  
async def create_item(item:imporovedItem):
    item_dict=imporovedItem.model_dump()
    if imporovedItem.is_offer:
        item_dict.update({"offer_message":f"item {item.name} running on a offer"})
    return item_dict
    
items_db = {
    "item1": {"name": "Super Widget", "price": 99.99},
    "item2": {"name": "Mega Gadget", "price": 149.50}
}

@app.get("/get_product/{id}")
async def get_product(id :str):
    if id not in items_db.keys():
        raise HTTPException(status_code=404 , detail="Item not in DB")
    return items_db[id]
    
@app.exception_handler(ItemNotFoundError)
async def item_not_found_exception_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Oops! The item with ID '{exc.item_id}' could not be located."}
    )
    
@app.get("/get_product_id/{id}")
async def get_product(id :str):
    if id not in items_db.keys():
        raise ItemNotFoundError(item_id=id)
    return items_db[id]




from fastapi import Depends, FastAPI


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    """A dependency function for common query parameters."""
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    # In a real app, you'd use these params to query the DB
    return {"message": "Users list", "params": commons}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    # This endpoint reuses the exact same logic
    return {"message": "Items list", "params": commons}


# Yield 

async def get_db_session():
    """Dependency that simulates a database session."""
    print("--> Yielding database session...")
    db_session = "FAKE_DATABASE_SESSION_OBJECT"
    try:
        yield db_session
    finally:
        # This code runs after the response has been sent
        print("--> Closing database session.")


@app.get("/things/{thing_id}")
async def get_thing(thing_id: str, db: str = Depends(get_db_session)):
    print(f"--- Processing request for thing: {thing_id} using DB session: {db}")
    if thing_id == "error":
        raise HTTPException(status_code=500, detail="An intentional error occurred.")
    return {"thing": thing_id}