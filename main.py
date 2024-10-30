from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.get("/")
# http://127.0.0.1:8000/
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
# http://127.0.0.1:8000/items

async def create_item(item: Item):
    return item
@app.get("/hello/{name}")
# http://127.0.0.1:8000/hello/Byrone

async def say_hello(name: str):
    return {"message": f"Hello {name}"}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
# http://127.0.0.1:8000/items/?skip=0&limit=10
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
# http://127.0.0.1:8000/items/123?q=some_query
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


