import string
from typing import Optional

from pydantic import EmailStr, constr, validator

from app.schemas import CoreModel, DateTimeModelMixin


# simple check for valid user_name
def validate_user_name(user_name: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(
        char in allowed for char in user_name
    ), "Invalid characters in user_name."
    assert len(user_name) >= 3, "user_name must be 3 characters or more."
    return user_name


class AccessToken(CoreModel):
    access_token: str
    token_type: str


class RefreshToken(CoreModel):
    refresh_token: str
    token_type: str


class TokenData(CoreModel):
    user_name: Optional[str] = None


class UserBase(CoreModel):
    """
    Leaving off password and salt from base model
    """

    email: Optional[EmailStr]
    user_name: Optional[str]
    is_active: bool = True


class UserCreate(CoreModel):
    """
    Email, user_name, and password are required for registering a new user
    """

    email: EmailStr
    password: constr(min_length=7, max_length=100)
    user_name: str

    @validator("user_name", pre=True)
    def user_name_is_valid(cls, user_name: str) -> str:
        return validate_user_name(user_name)

    class Config:
        orm_mode = True


class UserLogin(CoreModel):
    """
    username and password are required for logging in the user
    """

    user_name: str
    password: constr(min_length=7, max_length=100)

    @validator("user_name", pre=True)
    def username_is_valid(cls, user_name: str) -> str:
        return validate_user_name(user_name)


class UserInDB(DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """

    id: Optional[int]
    password: constr(min_length=7, max_length=100)
    salt: str

    class Config:
        orm_mode = True


class UserPublic(DateTimeModelMixin, UserBase):
    user_name: str
    email: EmailStr
    access_token: Optional[str]
    refresh_token: Optional[str]

    class Config:
        orm_mode = True


class UserPassword(CoreModel):
    """
    Users password schema
    """

    password: constr(min_length=7, max_length=100)
    salt: str

    class Config:
        orm_mode = True
