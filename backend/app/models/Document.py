from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select

from app.utils.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    url = Column(String)
    owner = relationship("User", back_populates="documents")

    @classmethod
    async def create(cls, db, **kwargs):
        # await FileModule.upload_file(kwargs['file'], path=f'{kwargs["owner_id"]}/documents/{kwargs["title"]}')
        # kwargs['url'] =
        transaction = cls(**kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction
    
    @classmethod
    async def get(cls, db, id):
        return await db.get(cls, id)
    
    @classmethod
    async def get_all(cls, db):
        return await db.execute(select(cls)).scalars().all()
    
    @classmethod
    async def update(cls, db, id, document_update):
        document = await cls.get(db, id)
        for key, value in document_update.dict().items():
            if value:
                setattr(document, key, value)
        await db.commit()
        return document
    
    @classmethod
    async def delete(cls, db, id):
        document = await cls.get(db, id)
        db.delete(document)
        await db.commit()
        return document
    
    @classmethod
    async def get_by_owner(cls, db, owner_id):
        return await db.execute(select(cls).where(cls.owner_id == owner_id)).scalars().all()
    
    @classmethod
    async def assign_owner(cls, db, document, owner_id):
        document.owner_id = owner_id
        await db.commit()
        return document


