from pydantic import BaseModel
from datetime import datetime
from typing import List

# Todo and Todo tasks categories


class Categories(BaseModel):
    categories: str

    class Config:
        orm_mode = True


class DisplayTodos(BaseModel):
    tasks: str
    categories: Categories

    class Config:
        orm_mode = True


class DisplayCategories(BaseModel):
    categories: str
    tasks: List[DisplayTodos]

    class Config:
        orm_mode = True


class Todos(BaseModel):
    tasks: str
    # time: datetime
