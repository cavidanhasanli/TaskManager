from contextvars import ContextVar
from os import environ

import peewee

DATABASE_NAME = environ.get("MYSQL_DATABASE")
USER = environ.get("MYSQL_USER")
PASSWORD = environ.get("MYSQL_PASSWORD")
HOST = environ.get("MYSQL_HOST")
PORT = environ.get("MYSQL_PORT")

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = peewee.MySQLDatabase(
    DATABASE_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
)

db._state = PeeweeConnectionState()
