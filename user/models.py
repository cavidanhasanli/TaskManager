import peewee

from app.database import db


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    id = peewee.AutoField()
    email = peewee.CharField(unique=True, index=True)
    user_name = peewee.CharField(unique=True, index=True)
    password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)
    created_at = peewee.DateTimeField(null=True)
    updated_at = peewee.DateTimeField(null=True)
    salt = peewee.CharField(null=True)
