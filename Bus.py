from dataclasses import dataclass
from Task import Task
from User import User


@dataclass
class Bus:
    id: int
    current_task: Task
    driver_id: User
    capacity: int
    status: str
    location_id: int
