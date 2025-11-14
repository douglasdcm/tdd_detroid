from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel
from typing import Annotated, Literal
from pydantic import AfterValidator, Field, HttpUrl

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database",
            max_length=5,
        ),
    ] = None,
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
    filter_query: Annotated[FilterParams, Query()] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    if id:
        results.update({"id": id})
    return results


class Image(BaseModel):
    url: HttpUrl = Field(examples=["https://example.com"])
    name: str = Field(examples=["Foo"])
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "name": "Foo",
    #                 "url": "https://example.com",
    #             }
    #         ]
    #     }
    # }


class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300,
        examples=["The description of the item"],
    )
    price: float = Field(examples=[2.34, 1.23])
    tax: float | None = Field(examples=[1.23], default=None)
    image: Image | None = None
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "name": "Foo",
    #                 "description": "A very nice Item",
    #                 "price": 35.4,
    #                 "tax": 3.2,
    #                 "image": {
    #                     "name": "Foo",
    #                     "url": "https://example.com",
    #                 },
    #             }
    #         ]
    #     }
    # }


class User(BaseModel):
    username: str = Field(examples=["FooBla"])
    full_name: str | None = Field(default=None, examples=["Foo Bla"])


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[
        int, Path(title="The ID of the item to get", description="The ID of the item to get", ge=1)
    ],
):
    return {"item_id": item_id}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    importance: Annotated[int, Body()],
    item: Item,
    q: str | None = None,
    user: User | None = None,
):
    result = {
        "item_id": item_id,
        **item.model_dump(),
        "item": item,
        "user": user,
        "importance": importance,
    }
    if q:
        result.update({"q": q})
    return result