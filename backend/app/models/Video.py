from uuid import uuid4

from app.models.Document import Document
from sqlalchemy import Column, ForeignKey, String, select, Boolean, Integer
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.utils.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    url = Column(String)
    channel_id = Column(String, ForeignKey("channels.id"))
    channel = relationship("Channel", back_populates="videos")
    is_active = Column(Boolean, default=True)
    claims = relationship("CopyClaim", back_populates="video", lazy="selectin")

    @classmethod
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
        videos = (await db.execute(select(cls))).scalars().all()
        return videos

    @classmethod
    async def update(cls, db: AsyncSession, id: int, video_update):
        video = await cls.get(db, id)
        for key, value in video_update.dict().items():
            if value:
                setattr(video, key, value)
        await db.commit()
        return video