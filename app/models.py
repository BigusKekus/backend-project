from dataclasses import dataclass
from typing import Dict


@dataclass
class User:
    id: int
    username: str


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Currency:
    id: int
    code: str


@dataclass
class Record:
    id: int
    amount: float
    category_id: int
    currency_id: int


# "база даних" в оперативці
DB: Dict[str, Dict[int, object]] = {
    "users": {},
    "categories": {},
    "currencies": {},
    "records": {},
}

SEQ: Dict[str, int] = {
    "users": 1,
    "categories": 1,
    "currencies": 1,
    "records": 1,
}
