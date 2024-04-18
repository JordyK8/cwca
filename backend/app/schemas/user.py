
from typing import Optional
from pydantic import BaseModel

from app.schemas.document import Document


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]
    username: Optional[str]

class User(UserBase):
    id: str
    is_active: bool
    documents: list[Document] = []

    class Config:
        from_attributes = True
