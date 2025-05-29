import pydantic


class EntryTest(pydantic.BaseModel):
    name: str
    release_date: str
    owners: int
    price: float
    categories: list[int]
    genres: list[int]
    tags: list[int]


class EntryOut(EntryTest):
    steam_score: float
