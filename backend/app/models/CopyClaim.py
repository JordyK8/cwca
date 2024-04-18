from uuid import uuid4

from app.models.Document import Document
from sqlalchemy import Column, ForeignKey, String, select, Boolean, Integer
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.utils.database import Base

class CopyClaim(Base):
    __tablename__ = "copy_claims"

    id = Column(String, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    url = Column(String)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="pending")
    video_id = Column(String, ForeignKey("videos.id"))
    video = relationship("Video", back_populates="copy_claims")
    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="copy_claims")
    claimer_video_id = Column(String, ForeignKey("videos.id"))
    claimer_video = relationship("Video", back_populates="copy_claims")

    
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
        copy_claims = (await db.execute(select(cls))).scalars().all()
        return copy_claims

    @classmethod
    async def update(cls, db: AsyncSession, id: int, copy_claim_update):
        copy_claim = await cls.get(db, id)
        for key, value in copy_claim_update.dict().items():
            if value:
                setattr(copy_claim, key, value)
        await db.commit()
        return copy_claim