from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from cls.Flight import Flight
from db import DBWorker


class TaskStatus(Enum):
    """Класс статуса задачи"""
    PLANNED = 0
    RUNNING = 1
    FINISHED = 2
    DENIED = 3


@dataclass
class Task:
    """
    Дата класс с данными задачи
    TODO:
        - remove potential SQL injection in update and write_to_db
    """
    id: int | None
    flight: Flight
    status: TaskStatus
    start_time: datetime
    finish_time: datetime
    bus_list: list["Bus"]

    def update(self, db: DBWorker):
        if self.id is None:
            raise ValueError("started task update without id")
        db.execute(f"UPDATE Task SET flight_id = '{self.flight.id}',\
            status = '{self.status}', \
            start_time = '{self.start_time.strftime('%H:%M')}',\
            finish_time = '{self.finish_time.strftime('%H:%M')}',\
            WHERE id = '{self.id}'")

    def write_to_db(self, db: DBWorker, commit=True):
        s = f"INSERT INTO Task (flight_id, status, start_time, finish_time) VALUES " \
            f"({self.flight.id}, {TaskStatus.PLANNED.value}, '{self.start_time}', '{self.finish_time}')"
        db.execute(s, commit=commit)
