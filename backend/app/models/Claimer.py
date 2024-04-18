from uuid import uuid4

from app.models.Document import Document
from sqlalchemy import Column, String, select, Boolean, Optional
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.utils.database import Base

class Claimer(Base):
    __tablename__ = "claimers"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    phone = Column(Optional(String))

    claims = relationship("CopyClaim", back_populates="claimer", lazy="selectin")

    @classmethod
    async def create(cls, db: AsyncSession, id=None, **kwargs):
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
        
        return transaction@classmethod
    async def create(cls, db: AsyncSession, id=None, **kwargs):
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
        claimers = (await db.execute(select(cls))).scalars().all()
        return claimers
    
    @classmethod
    async def update(cls, db: AsyncSession, id: int, claimer_update):
        claimer = await cls.get(db, id)
        for key, value in claimer_update.dict().items():
            if value:
                setattr(claimer, key, value)
        await db.commit()
        return claimer
    
    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        claimer = await cls.get(db, id)
        db.delete(claimer)
        await db.commit()
        return claimer

    @classmethod
    async def get(cls, db: AsyncSession, id: str):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        claimers = (await db.execute(select(cls))).scalars().all()
        return claimers
    
    @classmethod
    async def update(cls, db: AsyncSession, id: int, claimer_update):
        claimer = await cls.get(db, id)
        for key, value in claimer_update.dict().items():
            if value:
                setattr(claimer, key, value)
        await db.commit()
        return claimer
    
    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        claimer = await cls.get(db, id)
        db.delete(claimer)
        await db.commit()
        return claimer