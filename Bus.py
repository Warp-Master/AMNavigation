from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from Task import Task
from User import User


class BusStatus(Enum):
    WAITING = 0
    MOVING = 1
    LOADING = 2
    UNLOADING = 3


@dataclass
class Bus:
    id: int
    task: Task | None
    driver: User
    capacity: int
    status: BusStatus
    location_id: int | None
    free_location_id: int | None
    free_time: datetime | None

    def __lt__(self, other: "Bus"):
        return self.capacity < other.capacity

    def __gt__(self, other: "Bus"):
        return self.capacity > other.capacity
