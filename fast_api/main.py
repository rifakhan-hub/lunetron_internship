from fastapi import FastAPI

app = FastAPI()     # creates application object

@app.get("/")       # decorator that says "when someone sends a GET request to /, run this function."
def read_root():
    return{"message": "Hello, FastAPI"}     # return value (a dict) is automatically converted to JSON.