from uuid import uuid4

from app.models.Document import Document
from sqlalchemy import Column, String, select, Boolean, Integer
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.utils.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    documents = relationship("Document", back_populates="owner", lazy="selectin")
    channels = relationship("Channel", back_populates="owner", lazy="selectin")


    @classmethod
    async def create(cls, db: AsyncSession, id=None, **kwargs):
        print('kwargs and id', kwargs, id)
        if not id:
            id = uuid4().hex

        #remove password from kwargs
        password = kwargs.pop('password')
        hashed_password = password + "notreallyhashed"
        kwargs['hashed_password'] = hashed_password

        transaction = cls(id=id, **kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, id: str):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        users = (await db.execute(select(cls))).scalars().all()
        print('users', users)
        return users
    
    @classmethod
    async def update(cls, db: AsyncSession, id: int, user_update):
        user = await cls.get(db, id)
        for key, value in user_update.dict().items():
            if value:
                setattr(user, key, value)
        await db.commit()
        return user
    
    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        user = await cls.get(db, id)
        db.delete(user)
        await db.commit()
        return user
    
    @classmethod
    async def assign_document(cls, db: AsyncSession, user_id: int, document_id: int):
        user = await cls.get(db, user_id)
        document = await Document.get(db, document_id)
        user.documents.append(document)
        await db.commit()
        return user