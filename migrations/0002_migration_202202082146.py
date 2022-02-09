# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class User(peewee.Model):
    email = CharField(index=True, max_length=255, unique=True)
    user_name = CharField(index=True, max_length=255, unique=True)
    password = CharField(max_length=255)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)
    salt = CharField(max_length=255, null=True)
    class Meta:
        table_name = "user"


@snapshot.append
class UserIpDetail(peewee.Model):
    ip = CharField(max_length=255)
    details = CharField(max_length=255)
    class Meta:
        table_name = "useripdetail"


