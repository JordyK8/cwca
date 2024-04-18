from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import get_db
from app.schemas.user import UserBase, UserCreate, UserUpdate, User
from app.models.User import User as UserModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}", response_model=UserBase)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserModel.get(db, user_id)
    return user


@router.get("/", response_model=list[User])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await UserModel.get_all(db)
    print('users', users)
    return users


@router.post("/", response_model=UserBase)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await UserModel.create(db, **user.dict())
    return user


@router.put(
    "/{user_id}",
    response_model=UserBase,
)
async def update(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update user by id
    """
    
    user = await UserModel.update(db, user_id, user_update)
    return user