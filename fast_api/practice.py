from fastapi import FastAPI
import uuid

app = FastAPI(title="My API", version="1.0.0")

@app.get("/health")
def health():
    return{"status": "ok"}

# path parameter

@app.get("/products/{product_id}")
def product(product_id: uuid.UUID):
    return{"product id": {product_id}}

# Why does declaring /users/{user_id} before /users/me break the /users/me route?
# declare the fixed path before the dynamic one, or fixed gets swallowed as a dynamic one

# query parameter

@app.get("/search")
def search_param(query: str, page: int=1, page_size: int = 20):
    return{"query": query, "page" : page, "page size ": page_size }
