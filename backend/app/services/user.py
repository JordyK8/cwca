from fastapi import HTTPException
from app.models.User import User
import app.schemas.user as user_schema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.User import User as UserDBModel
from typing import List
from sqlalchemy import update

from app.dependencies import DBSessionDep

class UserService:
    def __init__(self):
        self.db_session: AsyncSession = DBSessionDep
        self.schema = user_schema.User

    async def create(self, user: user_schema.UserCreate):
        hashed_password = user.password + "notreallyhashed"
        new_user = User(email=user.email, hashed_password=hashed_password)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get(self, user_id: int):
        user = (await self.db_session.scalars(select(UserDBModel).where(UserDBModel.id == user_id))).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_all(self) -> List[user_schema.User]:
        q = await self.db_session.execute(select(UserDBModel).order_by(User.id))
        print('q', q)
        return q.scalars().all()

    async def update(self, id: int, user_update: user_schema.UserUpdate) -> user_schema.User:
        q = update(UserDBModel).where(UserDBModel.id == id)
        for name, value in user_update.dict().items():
            if value:
                q = q.values({name: value})
        q.execution_options(synchronize_session="fetch")
        updated_user = await self.db_session.execute(q)
        return updated_user