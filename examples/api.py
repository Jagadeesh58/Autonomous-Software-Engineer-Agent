"""
api.py - Sample FastAPI service with Pydantic validation.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Autonomous Agent Item API")


class Item(BaseModel):
    name: str
    price: float


items = []


@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI Service"}


@app.post("/items")
async def create_item(item: Item):
    items.append(item)
    return {"message": "Item added successfully", "item": item}


@app.get("/items")
async def read_items():
    return items


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
