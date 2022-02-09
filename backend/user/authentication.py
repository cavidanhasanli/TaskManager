from typing import Optional

import bcrypt
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext

from .schemas import UserInDB, UserPassword

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authenticate:
    def create_salt_and_hashed_password(
        self, *, plaintext_password: str
    ) -> UserPassword:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plaintext_password, salt=salt)
        return UserPassword(salt=salt, password=hashed_password)

    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().decode()

    @staticmethod
    def hash_password(*, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    @staticmethod
    def verify_password(*, password: str, salt: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password + salt, hashed_pw)

    @staticmethod
    def create_access_token_for_user(
        *, user: UserInDB, Authorize: AuthJWT
    ) -> Optional[str]:
        if not user or not isinstance(user, UserInDB):
            return None
        return Authorize.create_access_token(subject=user.user_name)

    @staticmethod
    def create_refresh_token_for_user(
        *, user: UserInDB, Authorize: AuthJWT
    ) -> Optional[str]:
        if not user or not isinstance(user, UserInDB):
            return None
        return Authorize.create_refresh_token(subject=user.user_name)
