from uuid import uuid4

from app.models.Document import Document
from sqlalchemy import Column, ForeignKey, String, select, Boolean, Integer
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(String, primary_key=True)
    external_id = Column(String, unique=True)
    name = Column(String, unique=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="channels")
    videos = relationship("Video", back_populates="channel", lazy="selectin")
    is_active = Column(Boolean, default=True)

    @classmethod
    async def create(cls, db: AsyncSession, id=None, **kwargs):
        if not id:
            id = uuid4().hex

        transaction = cls(id=id, **kwargs)
        db.add(transaction)@classmethod
    async def create(cls, db: AsyncSession, id=None, **kwargs):
        if not id:
            id = uuid4().hex

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
        channels = (await db.execute(select(cls))).scalars().all()
        return channels

    @classmethod
    async def update(cls, db: AsyncSession, id: int, channel_update):
        channel = await cls.get(db, id)
        for key, value in channel_update.dict().items():
            if value:
                setattr(channel, key, value)
        await db.commit()
        return channel

    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        channel = await cls.get(db, id)
        db.delete(channel)
        await db.commit()
        return channel

    @classmethod
    async def get_by_owner(cls, db: AsyncSession, owner_id):
        return await db.execute(select(cls).where(cls.owner_id == owner_id)).scalars().all()

    @classmethod
    async def assign_owner(cls, db: AsyncSession, channel, owner_id):
        channel.owner_id = owner_id
        await db.commit()
        return channel
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
        channels = (await db.execute(select(cls))).scalars().all()
        return channels

    @classmethod
    async def update(cls, db: AsyncSession, id: int, channel_update):
        channel = await cls.get(db, id)
        for key, value in channel_update.dict().items():
            if value:
                setattr(channel, key, value)
        await db.commit()
        return channel

    @classmethod
    async def delete(cls, db: AsyncSession, id: int):
        channel = await cls.get(db, id)
        db.delete(channel)
        await db.commit()
        return channel

    @classmethod
    async def get_by_owner(cls, db: AsyncSession, owner_id):
        return await db.execute(select(cls).where(cls.owner_id == owner_id)).scalars().all()

    @classmethod
    async def assign_owner(cls, db: AsyncSession, channel, owner_id):
        channel.owner_id = owner_id
        await db.commit()
        return channel