from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

items = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/items")
def create_item(item: str):
    items.append(item)
    return {"items": items}


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < len(items):
        return {"item_id": item_id, "item": items[item_id]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")