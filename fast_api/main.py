from fastapi import FastAPI
from typing import Optional

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


