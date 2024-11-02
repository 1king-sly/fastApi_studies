# from fastapi import FastAPI
# from pydantic import BaseModel
#
#
# app = FastAPI()
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
# @app.get("/")
# # http://127.0.0.1:8000/
# async def root():
#     return {"message": "Hello World"}
#
# @app.post("/items/")
# # http://127.0.0.1:8000/items
#
# async def create_item(item: Item):
#     return item
# @app.get("/hello/{name}")
# # http://127.0.0.1:8000/hello/Byrone
#
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
#
# @app.get("/items/")
# # http://127.0.0.1:8000/items/?skip=0&limit=10
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]
#
#
# @app.get("/items/{item_id}")
# # http://127.0.0.1:8000/items/123?q=some_query
# async def read_item(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}
#
#
# class Image(BaseModel):
#     url:str
#     name:str
#
# class Blog(BaseModel):
#     name:str
#     desc:str
#     slug:str
#     image:Image | None = None
#     authors:list[str] | None = None
#
# @app.post("/blogs/")
# async def create_blog(blog: Blog):
#     return {"blog": blog.model_dump(exclude_unset=True)}
#



from typing import Annotated

from fastapi import FastAPI, File, UploadFile,HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()


# @app.post("/files/")
# async def create_files(files: Annotated[list[bytes], File()]):
#     return {"file_sizes": [len(file) for file in files]}
#
#
# @app.post("/uploadfiles/")
# async def create_upload_files(files: list[UploadFile]):
#     if not files:
#         raise HTTPException(status_code=400, detail="No files uploaded")
#
#     return {"filenames": [file.filename for file in files]}
#
#
# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)



from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data


from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response