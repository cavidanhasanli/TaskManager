import peewee

from app.database import db
from user.models import User


class BaseModel(peewee.Model):
    class Meta:
        database = db


class UserIpDetail(BaseModel):

    id = peewee.AutoField()
    ip = peewee.CharField(null=False, max_length=255)
    details = peewee.CharField(null=False, max_length=255)
    user_id = peewee.ForeignKeyField(User, backref="useripdetail", on_delete="CASCADE")
