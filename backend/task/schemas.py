from pydantic import BaseModel


class UserIp(BaseModel):
    address: str
