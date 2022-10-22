from dataclasses import dataclass
from datetime import datetime

from Flight import Flight
from Bus import Bus


@dataclass
class Task:
    id: int
    flight: Flight
    status: str
    start_time: datetime
    finish_time: datetime
    bus_list: list[Bus]
