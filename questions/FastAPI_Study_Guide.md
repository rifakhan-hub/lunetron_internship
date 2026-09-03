# FastAPI Complete Study Guide

A structured path from fundamentals to production-ready patterns, with runnable code and practice questions after every section.

---

## 0. Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install fastapi uvicorn[standard] pydantic sqlalchemy python-multipart python-jose[cryptography] passlib[bcrypt] pytest httpx
```

Run any app with:
```bash
uvicorn main:app --reload
```
Interactive docs are auto-generated at `http://127.0.0.1:8000/docs` (Swagger UI) and `/redoc`.

---

## 1. Your First App

```python
# main.py
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}
```

**Key ideas**
- `FastAPI()` creates the app instance — it's the central object everything attaches to.
- Route decorators (`@app.get`, `@app.post`, etc.) map an HTTP method + path to a Python function.
- FastAPI infers request/response schemas from Python type hints, then generates OpenAPI docs automatically.

**Practice**
1. Add a `GET /health` endpoint returning `{"status": "ok"}`.
2. What's the difference between `@app.get("/")` and `@app.post("/")`? When would you use each?

---

## 2. Path Parameters

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id: int, order_id: int):
    return {"user_id": user_id, "order_id": order_id}
```

- Type hints (`item_id: int`) enforce validation automatically — visiting `/items/abc` returns a `422 Unprocessable Entity` with a clear error, no manual checking needed.
- **Order matters**: if you have both `/users/me` and `/users/{user_id}`, declare the fixed path (`/users/me`) *before* the dynamic one, or `me` gets swallowed as a `user_id`.

**Practice**
1. Write a route `/products/{product_id}` where `product_id` must be a `str` of exactly UUID-like text (hint: use `uuid.UUID` as the type).
2. Why does declaring `/users/{user_id}` before `/users/me` break the `/users/me` route?

---

## 3. Query Parameters

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10, q: Optional[str] = None):
    result = {"skip": skip, "limit": limit}
    if q:
        result["q"] = q
    return result
```

- Function parameters *not* found in the path are automatically treated as query parameters.
- Giving a default value (`skip: int = 0`) makes it optional; `Optional[str] = None` allows omission entirely.
- Required query params: just omit the default → `q: str` (no default) makes `q` mandatory.

**Practice**
1. Build `/search` with required `query: str` and optional `page: int = 1`, `page_size: int = 20`.
2. Call `/items/?limit=abc` — what status code and error do you expect, and why?

---

## 4. Request Body with Pydantic

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Must be greater than zero")
    tax: Optional[float] = None

@app.post("/items/")
def create_item(item: Item):
    total = item.price + (item.tax or 0)
    return {"item": item, "price_with_tax": total}
```

- `BaseModel` subclasses define the shape, types, and validation rules of incoming JSON.
- `Field(...)` adds extra validation (`gt`, `lt`, `max_length`, etc.) and OpenAPI metadata.
- FastAPI parses the JSON body, validates it against `Item`, and gives you a fully-typed Python object — invalid data auto-returns `422` with details on exactly which field failed.

**Practice**
1. Add a `Signup` model with `username: str` (3–20 chars), `email: str`, `age: int` (must be ≥ 18). Use `Field` constraints.
2. What HTTP status code does FastAPI return by default when body validation fails?

---

## 5. Combining Path, Query, and Body Params

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, notify: bool = False):
    return {"item_id": item_id, "item": item, "notify": notify}
```
FastAPI figures out the source of each parameter by matching names against the path, then treating primitive types as query params, and Pydantic models as the body — all in one signature.

**Practice**
1. Write `PATCH /users/{user_id}` accepting a body `UserUpdate` (all fields optional) and a query flag `dry_run: bool = False`.

---

## 6. Response Models & Status Codes

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

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
```

- `response_model` shapes and filters the *outgoing* data — even if you return extra fields, only the declared ones are serialized.
- Use `status_code=` to set the correct HTTP semantics (`201` for creation, `204` for no-content deletes, etc.)

**Practice**
1. Create `GET /items/{item_id}` returning `ItemOut`, and explain why hiding `internal_note` this way is safer than manually stripping dict keys.
2. What status code should `DELETE /items/{item_id}` return on success if there's no response body?

---

## 7. Error Handling

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_db = {1: "Widget"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "name": fake_db[item_id]}
```

Custom exception handlers:
```python
from fastapi import Request
from fastapi.responses import JSONResponse

class OutOfStockError(Exception):
    def __init__(self, item: str):
        self.item = item

@app.exception_handler(OutOfStockError)
def out_of_stock_handler(request: Request, exc: OutOfStockError):
    return JSONResponse(status_code=409, content={"error": f"{exc.item} is out of stock"})
```

**Practice**
1. Add a `403 Forbidden` response for accessing `/admin` without a query param `is_admin=true`.
2. Why is raising `HTTPException` preferable to returning `{"error": "..."}` with a `200` status?

---

## 8. Dependency Injection (`Depends`)

```python
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid token")
    return x_token

@app.get("/secure-data/")
def get_secure_data(token: str = Depends(verify_token)):
    return {"data": "sensitive info", "token_used": token}
```

Class-based dependencies with shared state (e.g., pagination):
```python
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/products/")
def list_products(pagination: Pagination = Depends()):
    return {"skip": pagination.skip, "limit": pagination.limit}
```

**Key ideas**
- `Depends()` lets FastAPI call a function (or class) *before* your route, injecting its return value.
- Great for auth checks, DB sessions, shared query logic — keeps route functions clean and testable.
- Dependencies can depend on other dependencies (nested), and FastAPI caches results per-request by default.

**Practice**
1. Write a `get_db()` dependency that yields a fake DB session and closes it afterward (`yield` pattern).
2. Explain in your own words why `Depends` improves testability compared to hardcoding logic inside the route.

---

## 9. Async vs Sync Routes

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/sync-task")
def sync_task():
    import time
    time.sleep(2)  # blocks the worker thread
    return {"done": True}

@app.get("/async-task")
async def async_task():
    await asyncio.sleep(2)  # non-blocking, frees the event loop
    return {"done": True}
```

- Use `async def` when your route awaits I/O (DB calls with an async driver, HTTP calls, async file I/O).
- If your code is synchronous/blocking (e.g., a sync ORM call, CPU-heavy work), keep `def` — FastAPI automatically runs sync routes in a threadpool so they don't block the event loop.
- **Mistake to avoid**: writing `async def` but calling blocking code (like `time.sleep` or `requests.get`) inside it — this blocks the entire event loop for all users.

**Practice**
1. You're calling a synchronous third-party SDK with no async support. Should your route be `def` or `async def`? Why?
2. What actually breaks if you use `time.sleep()` inside an `async def` route under load?

---

## 10. Database Integration (SQLAlchemy)

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

```python
# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base

class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
```

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ItemCreate(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.ItemDB(name=item.name, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

**Practice**
1. Add a `DELETE /items/{item_id}` route that removes a row and returns `204 No Content`.
2. Why does `get_db()` use `yield` instead of `return`?

---

## 11. Authentication (OAuth2 + JWT)

```python
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

fake_users_db = {"alice": {"username": "alice", "hashed_password": pwd_context.hash("wonderland")}}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/me")
def read_current_user(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
```

**Practice**
1. Add role-based access: extend the token payload with a `"role"` claim, then create a dependency `require_admin` that raises `403` if role isn't `"admin"`.
2. Why do we hash passwords with `bcrypt` instead of storing them as plain text or using simple encryption?

---

## 12. File Uploads

```python
from fastapi import FastAPI, File, UploadFile
from typing import List

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents), "content_type": file.content_type}

@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile] = File(...)):
    return {"filenames": [f.filename for f in files]}
```

**Practice**
1. Modify the single-file upload to reject files larger than 5 MB with a `413` error.

---

## 13. Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification scheduled"}
```
The response returns immediately; `write_log` runs *after* the response is sent. For heavier async workloads (retries, distributed workers), use Celery or a task queue instead.

**Practice**
1. When would `BackgroundTasks` be insufficient, and you'd reach for Celery/RQ instead?

---

## 14. Middleware & CORS

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start)
    return response
```

**Practice**
1. Why does the browser block cross-origin requests without CORS middleware, even if the API itself works fine via `curl`?

---

## 15. Routers (Structuring Larger Apps)

```python
# routers/items.py
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
def list_items():
    return [{"name": "Widget"}]

@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

```python
# main.py
from fastapi import FastAPI
from routers import items

app = FastAPI()
app.include_router(items.router)
```

**Practice**
1. Split a hypothetical app with `users`, `items`, and `orders` resources into three routers and wire them into `main.py`.

---

## 16. Testing

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI"}

def test_create_item():
    response = client.post("/items/", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201
    assert response.json()["name"] == "Widget"
```
Run with `pytest`. `TestClient` spins up the app in-process — no real server or network calls needed.

**Practice**
1. Write a test that asserts a `404` is returned when fetching a nonexistent item.

---

## Full Quiz (Answers at the Bottom)

1. What decorator would you use to handle a `DELETE` request at `/items/{item_id}`?
2. True or False: FastAPI validates path parameter types automatically based on type hints.
3. What's the default HTTP status code FastAPI returns for a validation error?
4. What class do you subclass to define a request body schema?
5. What's the purpose of the `response_model` parameter?
6. Which function do you call inside a route to manually raise an HTTP error?
7. What does `Depends()` do?
8. When should a route function be declared `async def` vs plain `def`?
9. What pattern does `get_db()` typically use (`return` or `yield`), and why?
10. What two things does `OAuth2PasswordBearer` do in a JWT auth flow?
11. What's the difference between `UploadFile` and simply reading raw bytes from the request body?
12. Why might `BackgroundTasks` be insufficient for sending 10,000 emails?
13. What does `CORSMiddleware` protect against, and who enforces it (the API or the browser)?
14. What's the benefit of `APIRouter` over defining all routes directly on `app`?
15. What tool/class lets you test FastAPI endpoints without running a live server?

### Answers

1. `@app.delete("/items/{item_id}")`
2. True — e.g. `item_id: int` auto-rejects non-integer values with a `422`.
3. `422 Unprocessable Entity`.
4. `pydantic.BaseModel`.
5. It filters and shapes the outgoing JSON, hiding fields not declared in the model and validating the response shape — independent of what the DB object contains.
6. `raise HTTPException(status_code=..., detail=...)`.
7. It declares a reusable dependency (function or class) that FastAPI calls before the route and injects the result as a parameter — used for auth, DB sessions, shared logic.
8. Use `async def` when the route awaits non-blocking I/O (async DB drivers, `httpx`, `asyncio.sleep`); use plain `def` for blocking/sync code, since FastAPI runs those in a threadpool automatically.
9. `yield` — it lets FastAPI run cleanup code (closing the session) after the response is sent, even if an exception occurred, similar to a context manager.
10. It tells FastAPI where to expect the token (`Authorization: Bearer <token>` header) for docs/Swagger UI, and acts as a dependency that extracts the raw token string for you to decode.
11. `UploadFile` streams the file to disk/memory efficiently via `SpooledTemporaryFile` and exposes metadata (`filename`, `content_type`) without loading the whole file into memory at once, unlike reading raw bytes directly.
12. Background tasks run in the same process after the response — no retry logic, no persistence if the server crashes, no distributed scaling. A dedicated queue (Celery/RQ) handles retries, monitoring, and horizontal scaling.
13. CORS protects against unauthorized cross-origin browser requests reading responses from your API; it's enforced by the **browser**, not the server (a `curl` or server-to-server call ignores CORS entirely).
14. It lets you group related routes with a shared prefix/tags/dependencies and organize a large app into modules instead of one giant `main.py`.
15. `fastapi.testclient.TestClient` (built on `httpx`), used with `pytest`.

---

## Suggested Practice Project

Build a small **Task Manager API**:
- `POST /tasks` — create a task (title, description, due_date)
- `GET /tasks` — list with pagination + filter by `completed`
- `GET /tasks/{id}` — get one
- `PATCH /tasks/{id}` — update
- `DELETE /tasks/{id}` — delete
- Add JWT auth so each user only sees their own tasks
- Persist to SQLite via SQLAlemy
- Write pytest tests for every endpoint

This single project touches every concept in this guide.
