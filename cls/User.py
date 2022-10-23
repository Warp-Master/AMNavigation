from dataclasses import dataclass
from enum import Enum
from db import DBWorker


class Group(Enum):
    """Группа пользователя"""
    ADMIN = 0
    DISPATCHER = 1
    DRIVER = 2
    VIEWER = 3


@dataclass
class User:
    """Датакласс юзера"""
    id: int
    login: str
    pwd_hash: str
    salt: str
    group: Group
    name: str

    def update(self, db: DBWorker):
        """Обновление данных в бд"""
        db.execute(f"UPDATE Users SET login = '{self.login}',\
            pwd_hash = '{self.pwd_hash}', \
            salt = '{self.salt}',\
            group_id = '{self.group}',\
            name = '{self.name}',\
            WHERE id = '{self.id}'")
