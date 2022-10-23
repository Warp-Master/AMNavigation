from dataclasses import dataclass
from enum import Enum
from db import database


class Group(Enum):
    ADMIN = 0
    DISPATCHER = 1
    DRIVER = 2
    VIEWER = 3


@dataclass
class User:
    id: int
    login: str
    pwd_hash: str
    salt: str
    group: Group
    name: str


def update(self):
    database.execute(f"UPDATE User SET login = '{self.login}',\
        pwd_hash = '{self.pwd_hash}', \
        salt = '{self.salt}',\
        group_id = '{self.group}',\
        name = '{self.name}',\
        WHERE id = '{self.id}'")
