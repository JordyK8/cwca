
from pydantic import BaseModel


class DocumentBase(BaseModel):
    title: str
    description: str | None = None


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: int
    owner_id: str

    class Config:
        from_attributes = True