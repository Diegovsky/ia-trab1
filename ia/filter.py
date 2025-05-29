import csv
import json
import pydantic
import os
from typing import Annotated
from ia.common import EntryOut

os.chdir("dados")


def sp(field: str) -> list[str]:
    if len(field) == 0:
        return []
    return field.split(",")


def med(field: str) -> int:
    a, b = field.split(" - ")
    a = float(a)
    b = float(b)
    return int((a + b) / 2)


CommaList = Annotated[list[str], pydantic.BeforeValidator(sp)]


class EntryIn(pydantic.BaseModel):
    app_id: int
    name: str
    release_date: str
    owners: Annotated[int, pydantic.BeforeValidator(med)]
    price: float
    meta_score: float
    categories: CommaList
    genres: CommaList
    tags: CommaList
    total_reviews: int
    steam_score: float

    positive: float
    negative: float


with open("to_filter.csv") as f:
    reader = csv.DictReader(f)
    h = pydantic.TypeAdapter(list[EntryIn]).validate_python(reader)

outs = {o.app_id: dict(o) for o in h}


def agg(field_name: str):
    # Tag -> int
    conj: dict[str, int] = {}
    next_num = 0
    for entry in outs.values():
        tags: list[str] = entry[field_name]
        out_tags = []
        for tag in tags:
            if tag not in conj:
                conj[tag] = next_num
                next_num += 1

            out_tags.append(conj[tag])

        entry[field_name] = out_tags

    with open(f"{field_name}.json", "w") as f:
        # {"a": 10} -> [("a", 10)] -> [(10, "a")]
        o = list((v, k) for k, v in conj.items())
        o.sort()
        r = [tag for num, tag in o]
        json.dump(r, f)


agg("categories")
agg("genres")
agg("tags")

with open("ia.json", "wb") as f:
    Tp = pydantic.TypeAdapter(dict[int, EntryOut])
    vals = Tp.validate_python(outs)
    f.write(Tp.dump_json(vals, indent=2))
