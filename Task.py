from dataclasses import dataclass
from datetime import datetime
from db import database

from Flight import Flight
# from Bus import Bus


@dataclass
class Task:
    id: int
    flight: Flight
    status: str
    start_time: datetime
    finish_time: datetime
    bus_list: list["Bus"]


def update(self):
    database.execute(f"UPDATE Task SET flight_id = '{self.flight.id}',\
        status = '{self.status}', \
        load_time = '{self.start_time.strftime('%H:%M')}',\
        unload_time = '{self.finish_time.strftime('%H:%M')}',\
        WHERE id = '{self.id}'")