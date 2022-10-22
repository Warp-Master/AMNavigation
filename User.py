from dataclasses import dataclass
from enum import Enum


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
