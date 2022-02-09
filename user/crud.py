from fastapi import HTTPException

from user import auth_service

from .models import User
from .schemas import UserCreate, UserInDB


async def create_user(new_user: UserCreate) -> UserInDB:
    new_password = auth_service.create_salt_and_hashed_password(
        plaintext_password=new_user.password
    )
    new_user_params = new_user.copy(update=new_password.dict())
    new_user_updated = UserInDB(**new_user_params.dict())
    created_user = User(**new_user_updated.dict())
    created_user.save()

    return UserInDB.from_orm(created_user)


async def get_user_by_username(user_name: str) -> UserInDB:
    found_user = User.get(User.user_name == user_name)
    if found_user:
        return UserInDB.from_orm(found_user)
    raise HTTPException(status_code=404, detail="User with given username not found")
