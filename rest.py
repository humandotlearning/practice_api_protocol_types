from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item( BaseModel ):
    id: int
    name: str


DB: dict[int, Item] = {}

@app.get("/items/{item_id}")
def get_item(item_id:int):
    return DB.get(item_id) or {"error": " Not found"}

@app.post("/item", status_code=201)
def create_item(item: Item):
    DB[item.id] = item
    return item

