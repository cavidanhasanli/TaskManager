from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from user import auth_service

from ..schemas import (
    AccessToken,
    RefreshToken,
    UserCreate,
    UserInDB,
    UserLogin,
    UserPublic,
)

router = APIRouter()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post(
    "/create",
    tags=["user registration"],
    description="Register the User",
    response_model=UserPublic,
)
async def user_create(user: UserCreate) -> UserInDB:
    from ..crud import create_user

    return await create_user(user)


@router.post(
    "/login",
    tags=["user login"],
    description="Log in the User",
    response_model=UserPublic,
)
async def user_login(user: UserLogin, Authorize: AuthJWT = Depends()) -> UserPublic:
    from ..crud import get_user_by_username

    found_user = await get_user_by_username(user_name=user.user_name)
    if auth_service.verify_password(
        password=user.password, salt=found_user.salt, hashed_pw=found_user.password
    ):
        # If the provided password is valid one then we are going to create an access token
        access_token = auth_service.create_access_token_for_user(
            user=found_user, Authorize=Authorize
        )
        refresh_token = auth_service.create_refresh_token_for_user(
            user=found_user, Authorize=Authorize
        )
        access_token = AccessToken(access_token=access_token, token_type="bearer")
        refresh_token = RefreshToken(refresh_token=refresh_token, token_type="bearer")
        return UserPublic(
            **found_user.dict(),
            access_token=access_token.access_token,
            refresh_token=refresh_token.refresh_token,
        )
    raise HTTPException(status_code=401, detail="Incorrect password provided")


@router.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()) -> AccessToken:
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return AccessToken(access_token=new_access_token, token_type="bearer")


@router.get("/user")
async def user(Authorize: AuthJWT = Depends()):
    from ..crud import get_user_by_username

    try:
        Authorize.jwt_required()

        current_user = Authorize.get_jwt_subject()
        found_user = await get_user_by_username(user_name=current_user)
    except Exception as err:
        raise HTTPException(
            status_code=400, detail=f"JWT Operation failed with {err}"
        ) from err

    return {"user": current_user, "email": found_user.email}
