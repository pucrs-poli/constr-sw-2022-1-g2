from pickletools import int4
from typing import List, Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

###############################################################################

class TurmaCreate(BaseModel):
    ano: int
    semestre: int
    num_turma: int


class Turma(TurmaCreate):
    id: int

    class Config:
        orm_mode = True

