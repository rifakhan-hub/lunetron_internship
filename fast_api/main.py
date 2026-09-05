from fastapi import FastAPI, status
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()     # creates application object

@app.get("/")       # decorator that says "when someone sends a GET request to /, run this function."
def read_root():
    return{"message": "Hello, FastAPI"}     # return value (a dict) is automatically converted to JSON.

# path parameters

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id: int, order_id: int):
    return {"user_id": user_id, "order_id": order_id}

# query parameters
# Function parameters not found in the path are automatically treated as query parameters.
# extra key-value pairs added after a ?, used to filter, sort, paginate, or search. They come in key=value pairs, separated by &.

@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10, q: Optional[str] = None):
    result = {"skip": skip, "limit": limit}
    if q:
        result["q"] = q
    return result
# Giving a default value (skip: int = 0) makes it optional; Optional[str] = None allows omission entirely.
# Required query params: just omit the default → q: str (no default) makes q mandatory.

class Item(BaseModel):      # BaseModel subclasses define the shape, types, and validation rules of incoming JSON.
    name: str
    description: Optional[str] = None
    price: float = Field(       # Field(...) adds extra validation (gt, lt, max_length, etc.) and OpenAPI metadata.
                        gt=0, 
                        description="Must be greater than zero"
                        )
    tax: Optional[float] = None

@app.post("/items/")
def create_item(item: Item):
    total = item.price + (item.tax or 0)
    return {"item": item, "price_with_tax": total}



#4 Request Body with Pydantic
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Must be greater than zero")
    tax: Optional[float] = None

@app.post("/items/")
def create_item(item: Item):
    total = item.price + (item.tax or 0)
    return {"item": item, "price_with_tax": total}


#5. Combining Path, Query, and Body Params
class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, notify: bool = False):
    return {"item_id": item_id, "item": item, "notify": notify}


#6 Response Models & Status Codes
class ItemIn(BaseModel):
    name: str
    price: float
    internal_note: str  # we don't want to expose this

class ItemOut(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemIn):
    # internal_note is stored but not returned, because response_model filters it out
    return item


